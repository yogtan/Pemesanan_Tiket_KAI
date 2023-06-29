import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from PIL import ImageTk, Image
from tkinter import messagebox
from datetime import date, timedelta
import datetime

import mysql.connector
import numpy as np
import matplotlib.pyplot as plt


class BaseWindow:
    def __init__(self, title, image_path, label_text, label_text2):
        self.window = tk.Tk()
        self.window.title(title)

        # Mengatur ukuran jendela aplikasi
        window_width = 709
        window_height = 688
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Koneksi ke database
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Ganti dengan password MySQL Anda
            database='booking'
        )
        self.create_table()

        # Membuat frame kolom kiri (putih)
        self.left_frame = tk.Frame(self.window, bg="#E1E2E2")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Menambahkan kalimat di atas gambar
        label_teks = tk.Label(
            self.left_frame, text=label_text2, bg="#E1E2E2", fg="black", font=("Dosis ExtraBold", 18, "bold"))
        label_teks.pack(pady=(80, 20), padx=50, anchor=tk.CENTER)

        # Menambahkan gambar pada kolom kiri
        
        if image_path:
            image = Image.open(image_path)
            if image_path == "image_1.png":
                image = image.resize((200, 200), Image.ANTIALIAS)
                self.photo = ImageTk.PhotoImage(image)
                self.label_image = tk.Label(
                    self.left_frame, image=self.photo, bg="white")
                self.label_image.pack(pady=(100, 0), padx=50, anchor=tk.CENTER)
            elif image_path == "image_2.png":
                image = image.resize((200, 400), Image.ANTIALIAS)
                self.photo = ImageTk.PhotoImage(image)
                self.label_image = tk.Label(
                    self.left_frame, image=self.photo, bg="white")
                self.label_image.pack(pady=(20, 0), padx=50, anchor=tk.CENTER)

        # Menambahkan kalimat di bawah gambar
        label_teks = tk.Label(
            self.left_frame, text=label_text, bg="#E1E2E2", fg="black", font=("Dosis ExtraBold", 10))
        label_teks.pack(pady=(10, 20), padx=50, anchor=tk.CENTER)

        # Membuat frame kolom kanan (navy)
        self.right_frame = tk.Frame(self.window, bg="#1D2228")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INT AUTO_INCREMENT PRIMARY KEY,
                        nama VARCHAR(255) UNIQUE,
                        nik VARCHAR(255) UNIQUE,
                        password VARCHAR(255))''')
        self.conn.commit()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS pemesanan (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        stasiun_asal VARCHAR(255),
                        stasiun_tujuan VARCHAR(255),
                        tanggal_pergi DATE,
                        jumlah_dewasa INT,
                        jumlah_bayi INT,
                        nama_pemesan VARCHAR(255),
                        nomor_identitas VARCHAR(255),
                        no_hp VARCHAR(255)
                        ) 
        ''')
        self.conn.commit()


    def login(self):
        nama = self.entry_nama.get()
        password = self.entry_password.get()

        if not nama or not password:
            messagebox.showwarning("Peringatan", "Harap isi semua informasi.")
            return

        if self.authenticate(nama, password):
            self.nama_pengguna = nama 
            messagebox.showinfo("Selamat Datang", "Login berhasil!")
            self.open_booking_menu()
        else:
            messagebox.showerror("Error", "Nama atau kata sandi salah.")


# Fungsi untuk memeriksa nama dan kata sandi yang valid
    def authenticate(self, nama, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE nama=%s AND password=%s", (nama, password))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False

    # Fungsi untuk mendaftarkan pengguna baru

    def register(self):
        nama = self.entry_nama.get()
        nik = self.entry_nik.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not nama or not nik or not password or not confirm_password:
            messagebox.showwarning("Peringatan", "Harap isi semua informasi.")
            return

        if password != confirm_password:
            messagebox.showwarning("Peringatan", "Password dan konfirmasi password tidak cocok.")
            return
        
        if self.check_nama_exist(nama):
            messagebox.showerror("Error", "Nama sudah terdaftar.")
            return
        
        if self.check_nik_exist(nik):
            messagebox.showerror("Error", "NIK sudah terdaftar.")
            return

        self.save_user(nama, nik, password)
        messagebox.showinfo("Pendaftaran Berhasil",
                            "Akun berhasil didaftarkan.")
        self.open_login_window()

    # Fungsi untuk memeriksa apakah nama sudah terdaftar
    def check_nama_exist(self, nama):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE nama=%s", (nama,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
        
    def check_nik_exist(self, nik):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE nik=%s", (nik,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False    

    # Fungsi untuk menyimpan pengguna baru ke dalam database
    
    def save_user(self, nama, nik, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (nama, nik, password) VALUES (%s, %s, %s)", (nama, nik, password))
        self.conn.commit()

    def pemesanan(self):
        stasiun_asal = self.dropdown_stasiun_asal.get()
        stasiun_tujuan = self.dropdown_stasiun_tujuan.get()
        tanggal_pergi = self.dropdown_tanggal_pergi.get()
        jumlah_dewasa = self.dropdown_jumlah_dewasa.get()
        jumlah_bayi = self.dropdown_jumlah_bayi.get()
        nama_pemesan = self.entry_nama_pemesan.get()
        identitas_pemesan = self.entry_identitas_pemesan.get()
        no_hp_pemesan = self.entry_nohp_pemesan.get()
        
        if not stasiun_asal or not stasiun_tujuan or not tanggal_pergi or not jumlah_dewasa or not jumlah_bayi or not nama_pemesan or not identitas_pemesan or not no_hp_pemesan:
            messagebox.showwarning("Peringatan", "Harap isi semua informasi.")
            return

        self.save_pemesanan(stasiun_asal, stasiun_tujuan, tanggal_pergi, jumlah_dewasa, jumlah_bayi, nama_pemesan, identitas_pemesan, no_hp_pemesan)
        messagebox.showinfo("Pemesanan Berhasil", "Pemesanan berhasil dilakukan.")
        self.open_cetak_window()

    def save_pemesanan(self, stasiun_asal, stasiun_tujuan, tanggal_pergi, jumlah_dewasa, jumlah_bayi, nama_pemesan, nomor_identitas, no_hp):
        tanggal_pergi = datetime.datetime.strptime(tanggal_pergi, '%d/%m/%Y').strftime('%Y-%m-%d')

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO pemesanan (stasiun_asal, stasiun_tujuan, tanggal_pergi, jumlah_dewasa, jumlah_bayi, nama_pemesan, nomor_identitas, no_hp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (stasiun_asal, stasiun_tujuan, tanggal_pergi, jumlah_dewasa, jumlah_bayi, nama_pemesan, nomor_identitas, no_hp))
        self.conn.commit()

    def display_pesanan(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pemesanan ORDER BY id DESC LIMIT 1")
        pesanan = cursor.fetchone()
        self.conn.commit()

        if pesanan is not None:
            self.entry_nama.delete(0, tk.END)
            self.entry_stasiun_asal.delete(0, tk.END)
            self.entry_stasiun_tujuan.delete(0, tk.END)
            self.entry_tanggal_pergi.delete(0, tk.END)
            self.entry_jumlah_tiket.delete(0, tk.END)

            self.entry_nama.insert(tk.END, str(pesanan[6]))
            self.entry_stasiun_asal.insert(tk.END, str(pesanan[1]))
            self.entry_stasiun_tujuan.insert(tk.END, str(pesanan[2]))
            self.entry_tanggal_pergi.insert(tk.END, str(pesanan[3]))
            total_tiket = pesanan[4] + pesanan[5]
            self.entry_jumlah_tiket.insert(tk.END, str(total_tiket))

            


        

class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__("Pemesanan Tiket Kereta Api", "image_1.png", "Daftar, Segera!\nProses & Berangkat Cepat", "")

        # Label Login
        self.label_login = tk.Label(
            self.right_frame, text="LOGIN", bg="#1D2228", fg="white")
        self.label_login.configure(
            font=font.Font(family="Inter ExtraBold", size=18, weight="bold"))
        self.label_login.grid(
            row=0, column=0, pady=(150, 0), padx=160, sticky=tk.W)

        # Label dan Entri Email di kolom kanan
        self.label_nama = tk.Label(
        self.right_frame, text="Nama:", bg="#1D2228", fg="white")
        self.label_nama.grid(row=0, column=0, pady=(250, 0), padx=50, sticky=tk.W)
        self.entry_nama = tk.Entry(self.right_frame, width=50)
        self.entry_nama.grid(row=1, column=0, pady=20, padx=50, sticky=tk.W)

        # Label dan Entri Kata Sandi di kolom kanan
        self.label_password = tk.Label(
            self.right_frame, text="Kata Sandi:", bg="#1D2228", fg="white")
        self.label_password.grid(row=2, column=0, pady=10, padx=50, sticky=tk.W)
        self.entry_password = tk.Entry(
            self.right_frame, show="*", width=50)
        self.entry_password.grid(
            row=3, column=0, pady=10, padx=50, sticky=tk.W)

        # Tombol Masuk di kolom kanan
        self.button_login = tk.Button(
            self.right_frame, text="LOGIN", command=self.login, bg="#82CA60", fg="black")
        self.button_login.grid(
            row=4, column=0, pady=10, padx=180, sticky=tk.E)

        # Menambahkan tombol "Daftar"
        button_daftar = tk.Button(
            self.left_frame, text="REGISTER", command=self.open_register_window, bg="#FB8122", fg="black")
        button_daftar.pack()

        self.window.mainloop()

    def open_booking_menu(self):
        self.window.destroy()
        BookingMenuWindow()

    def open_register_window(self):
        self.window.destroy()
        RegisterWindow()


class RegisterWindow(BaseWindow):
    def __init__(self):
        super().__init__("Halaman Register", "image_1.png", "Login, Segera!\nProses & Berangkat Cepat","")

    # Label Register
        self.label_register = tk.Label(
            self.right_frame, text="REGISTER", bg="#1D2228", fg="white")
        self.label_register.configure(
            font=font.Font(family="Inter ExtraBold", size=18, weight="bold"))
        self.label_register.grid(
            row=0, column=0, pady=(150, 0), padx=135, sticky=tk.W)

        # Label dan Entry Email di kolom kanan
        self.label_nama = tk.Label(
            self.right_frame, text="Nama:", bg="#1D2228", fg="white")
        self.label_nama.grid(
            row=1, column=0, pady=(20, 0), padx=50, sticky=tk.W)
        self.entry_nama = tk.Entry(self.right_frame, width=50)
        self.entry_nama.grid(row=2, column=0, pady=5, padx=50, sticky=tk.W)


        # Label dan Entry NIK di kolom kanan
        self.label_nik = tk.Label(
            self.right_frame, text="NIK:", bg="#1D2228", fg="white")
        self.label_nik.grid(row=3, column=0, pady=10, padx=50, sticky=tk.W)
        self.entry_nik = tk.Entry(
            self.right_frame, width=50)
        self.entry_nik.grid(
            row=4, column=0, pady=5, padx=50, sticky=tk.W)

        # Label dan Entry Kata Sandi di kolom kanan
        self.label_password = tk.Label(
            self.right_frame, text="Kata Sandi:", bg="#1D2228", fg="white")
        self.label_password.grid(row=5, column=0, pady=10, padx=50, sticky=tk.W)
        self.entry_password = tk.Entry(
            self.right_frame, show="*", width=50)
        self.entry_password.grid(
            row=6, column=0, pady=5, padx=50, sticky=tk.W)

        # Label dan Entry Konfirmasi Password di kolom kanan
        self.label_confirm_password = tk.Label(
            self.right_frame, text="Konfirmasi Password:", bg="#1D2228", fg="white")
        self.label_confirm_password.grid(row=7, column=0, pady=10, padx=50, sticky=tk.W)
        self.entry_confirm_password = tk.Entry(
            self.right_frame, show="*", width=50)
        self.entry_confirm_password.grid(
            row=8, column=0, pady=5, padx=50, sticky=tk.W)

        # Tombol Register di kolom kanan
        self.button_register = tk.Button(
            self.right_frame, text="REGISTER", command=self.register, bg="#FB8122", fg="black")
        self.button_register.grid(
            row=9, column=0, pady=10, padx=180, sticky=tk.E)

        # Menambahkan tombol "Login"
        button_login = tk.Button(   
            self.left_frame, text="LOGIN", command=self.open_login_window, bg="#82CA60", fg="black")
        button_login.pack()

    def open_login_window(self):
        self.window.destroy()
        LoginWindow()  

        self.window.mainloop()


class BookingMenuWindow(BaseWindow):
    def __init__(self):
        super().__init__("Halaman Booking", "image_2.png", "", "PETA RUTE\nYOGYAKARTA")

        # Label Booking
        self.label_booking = tk.Label(
            self.right_frame, text="BELI TIKET", bg="#1D2228", fg="white")
        self.label_booking.configure(
            font=font.Font(family="Inter ExtraBold", size=18, weight="bold"))
        self.label_booking.grid(
            row=0, column=0, pady=(50, 0), padx=135, sticky=tk.W)

        
        self.label_pemesa = tk.Label(
            self.right_frame, text="PEMESANAN", bg="#1D2228", fg="white")
        self.label_pemesa.configure(
            font=font.Font(family="Inter ExtraBold", size=12, weight="bold"))
        self.label_pemesa.grid(
            row=1, column=0, pady=(50, 0), padx=50, sticky=tk.W)
        
        # Label dan Dropdown Menu Stasiun Asal di kolom kanan
        self.label_stasiun_asal = tk.Label(
            self.right_frame, text="Stasiun Asal:", bg="#1D2228", fg="white")
        self.label_stasiun_asal.grid(
            row=3, column=0, pady=(20, 0), padx=50, sticky=tk.W)
        self.dropdown_stasiun_asal = ttk.Combobox(self.right_frame, values=["Solo Balapan", "Purwosari", "Klaten", "Lempuyangan", "Klaten"], width=20)
        self.dropdown_stasiun_asal.grid(row=4, column=0, pady=5, padx=50, sticky=tk.W)

        # Label dan Dropdown Menu Stasiun Tujuan di kolom kanan
        self.label_stasiun_tujuan = tk.Label(
            self.right_frame, text="Stasiun Tujuan:", bg="#1D2228", fg="white")
        self.label_stasiun_tujuan.grid(
            row=3, column=0, pady=(20, 0), padx=230, sticky=tk.W)
        self.dropdown_stasiun_tujuan = ttk.Combobox(self.right_frame, values=["Solo Balapan", "Purwosari", "Klaten", "Lempuyangan", "Klaten"], width=20)
        self.dropdown_stasiun_tujuan.grid(row=4, column=0, pady=5, padx=230, sticky=tk.W)


        self.label_tanggal_pergi = tk.Label(
            self.right_frame, text="Tanggal Pergi:", bg="#1D2228", fg="white")
        self.label_tanggal_pergi.grid(
            row=7, column=0, pady=(20, 0), padx=50, sticky=tk.W)

        # Create a list of selectable dates for the dropdown
        today = date.today()
        dates = [today + timedelta(days=i) for i in range(7)]
        date_options = [date.strftime("%d/%m/%Y") for date in dates]

        self.dropdown_tanggal_pergi = ttk.Combobox(self.right_frame, values=date_options, width=10)
        self.dropdown_tanggal_pergi.grid(row=8, column=0, pady=5, padx=50, sticky=tk.W) 

        # Label dan Dropdown Menu Jumlah Dewasa di kolom kanan
        self.label_jumlah_dewasa = tk.Label(
            self.right_frame, text="Dewasa (>= 3 thn):", bg="#1D2228", fg="white")
        self.label_jumlah_dewasa.grid(
            row=7, column=0, pady=(20, 0), padx=154, sticky=tk.W)

        self.dropdown_jumlah_dewasa = ttk.Combobox(self.right_frame, values=["1 ", "2", "3", "4", "5"], width=13)
        self.dropdown_jumlah_dewasa.grid(row=8, column=0, pady=5, padx=154, sticky=tk.W)

        # Label dan Dropdown Menu Jumlah Bayi di kolom kanan
        self.label_jumlah_bayi = tk.Label(
            self.right_frame, text="Bayi (< 3 thn):", bg="#1D2228", fg="white")
        self.label_jumlah_bayi.grid(
            row=7, column=0, pady=(20, 0), padx=273, sticky=tk.W)

        self.dropdown_jumlah_bayi = ttk.Combobox(self.right_frame, values=["0", "1", "2", "3", "4"], width=13)
        self.dropdown_jumlah_bayi.grid(row=8, column=0, pady=5, padx=273, sticky=tk.W)

        # Data Pemesan
        self.label_pesan = tk.Label(
            self.right_frame, text="DATA PEMESAN/PENUMPANG", bg="#1D2228", fg="white")
        self.label_pesan.configure(
            font=font.Font(family="Inter ExtraBold", size=12, weight="bold"))
        self.label_pesan.grid(
            row=9, column=0, pady=(50, 0), padx=50, sticky=tk.W)

        self.label_tittle_pemesan = tk.Label(
            self.right_frame, text="Tittle:", bg="#1D2228", fg="white")
        self.label_tittle_pemesan.grid(
            row=10, column=0, pady=(20, 0), padx=50, sticky=tk.W)

        self.dropdown_tittle_pemesan = ttk.Combobox(self.right_frame, values=["Tuan", "Nyonya"], width=10)
        self.dropdown_tittle_pemesan.grid(row=11, column=0, pady=5, padx=50, sticky=tk.W)

        self.label_nama_pemesan = tk.Label(
            self.right_frame, text="Nama :", bg="#1D2228", fg="white")
        self.label_nama_pemesan.grid(
            row=10, column=0, pady=(20, 0), padx=160, sticky=tk.W)
        self.entry_nama_pemesan = tk.Entry(self.right_frame, width=35)
        self.entry_nama_pemesan.grid(row=11, column=0, pady=5, padx=160, sticky=tk.W)

        self.label_tipe_identitas = tk.Label(
            self.right_frame, text="Tipe Identitas:", bg="#1D2228", fg="white")
        self.label_tipe_identitas.grid(
            row=12, column=0, pady=(20, 0), padx=50, sticky=tk.W)

        self.dropdown_tipe_identitas = ttk.Combobox(self.right_frame, values=["NIK", "Paspor"], width=10)
        self.dropdown_tipe_identitas.grid(row=13, column=0, pady=5, padx=50, sticky=tk.W)

        self.label_identitas_pemesan = tk.Label(
            self.right_frame, text="Nomor Identitas :", bg="#1D2228", fg="white")
        self.label_identitas_pemesan.grid(
            row=12, column=0, pady=(20, 0), padx=160, sticky=tk.W)
        self.entry_identitas_pemesan = tk.Entry(self.right_frame, width=35)
        self.entry_identitas_pemesan.grid(row=13, column=0, pady=5, padx=160, sticky=tk.W)

        self.label_nohp_pemesan = tk.Label(
            self.right_frame, text="No Hp :", bg="#1D2228", fg="white")
        self.label_nohp_pemesan.grid(
            row=14, column=0, pady=(20, 0), padx=50, sticky=tk.W)
        self.entry_nohp_pemesan = tk.Entry(self.right_frame, width=13)
        self.entry_nohp_pemesan.grid(row=15, column=0, pady=5, padx=50, sticky=tk.W)

        # Tombol Masuk di kolom kanan
        self.button_pesan = tk.Button(
            self.right_frame, text="PESAN KERETA", command=self.pemesanan, bg="#82CA60", fg="black")
        self.button_pesan.grid(
            row=18, column=0, pady=20, padx=285, sticky=tk.E)
        
        # # Menambahkan tombol "Pesn Kereta"
        # button_login = tk.Button(
        #     self.left_frame, text="PESAN KERETA", command=self.pemesanan, bg="#82CA60", fg="black")
        # button_login.pack()

    def open_cetak_window(self):
        self.window.destroy()
        CetakTiketMenuWindow() 

    

        self.window.mainloop()


class CetakTiketMenuWindow(BaseWindow):
    def __init__(self):
        super().__init__("Halaman Booking", "image_1.png", "TerimaKasih Sudah Memesan!\nPesan Lagi?", "")

        # Label Booking
        self.label_booking = tk.Label(
            self.right_frame, text="CETAK TIKET", bg="#1D2228", fg="white")
        self.label_booking.configure(
            font=font.Font(family="Inter ExtraBold", size=18))
        self.label_booking.grid(
            row=0, column=0, pady=(80, 0), padx=120, sticky=tk.W)

        # Label dan Entry Nama di kolom kanan
        self.label_nama = tk.Label(
            self.right_frame, text="Nama:", bg="#1D2228", fg="white")
        self.label_nama.grid(
            row=1, column=0, pady=(20, 0), padx=50, sticky=tk.W)

        self.entry_nama = tk.Entry(self.right_frame, width=50)
        self.entry_nama.grid(row=2, column=0, pady=5, padx=50, sticky=tk.W)

        # Label dan Entry Stasiun Asal di kolom kanan
        self.label_stasiun_asal = tk.Label(
            self.right_frame, text="Stasiun Asal:", bg="#1D2228", fg="white")
        self.label_stasiun_asal.grid(
            row=3, column=0, pady=(20, 0), padx=50, sticky=tk.W)

        self.entry_stasiun_asal = tk.Entry(self.right_frame, width=50)
        self.entry_stasiun_asal.grid(row=4, column=0, pady=5, padx=50, sticky=tk.W)

        # Label dan Entry Stasiun Tujuan di kolom kanan
        self.label_stasiun_tujuan = tk.Label(
            self.right_frame, text="Stasiun Tujuan:", bg="#1D2228", fg="white")
        self.label_stasiun_tujuan.grid(
            row=5, column=0, pady=(20, 0), padx=50, sticky=tk.W)

        self.entry_stasiun_tujuan = tk.Entry(self.right_frame, width=50)
        self.entry_stasiun_tujuan.grid(row=6, column=0, pady=5, padx=50, sticky=tk.W)

        # Label dan Entry Tanggal Pergi di kolom kanan
        self.label_tanggal_pergi = tk.Label(
            self.right_frame, text="Tanggal Pergi:", bg="#1D2228", fg="white")
        self.label_tanggal_pergi.grid(
            row=7, column=0, pady=(20, 0), padx=50, sticky=tk.W)

        self.entry_tanggal_pergi = tk.Entry(self.right_frame, width=50)
        self.entry_tanggal_pergi.grid(row=8, column=0, pady=5, padx=50, sticky=tk.W)

        # Label dan Entry Jumlah Tiket di kolom kanan
        self.label_jumlah_tiket = tk.Label(
            self.right_frame, text="Jumlah Tiket:", bg="#1D2228", fg="white")
        self.label_jumlah_tiket.grid(
            row=9, column=0, pady=(20, 0), padx=50, sticky=tk.W)

        self.entry_jumlah_tiket = tk.Entry(self.right_frame, width=50)
        self.entry_jumlah_tiket.grid(row=10 , column=0, pady=5, padx=50, sticky=tk.W)


        self.display_pesanan()
       
        
        # Menambahkan tombol "Login"
        button_login = tk.Button(   
            self.left_frame, text="LOGIN", command=self.open_login_window, bg="#82CA60", fg="black")
        button_login.pack()

    def open_login_window(self):
        self.window.destroy()
        LoginWindow()  
        self.window.mainloop()



    

LoginWindow()
