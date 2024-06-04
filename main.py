import tkinter as tk
from tkinter import ttk
from threading import Thread, Lock
from PIL import Image, ImageTk
import random
import time


class CakeFactoryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cake Factory Simulator")

        # Create and layout the widgets
        self.create_widgets()

        # Status labels for cream and dough
        self.label_status_cream = ttk.Label(self.master, text="", foreground="green")
        self.label_status_cream.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        self.label_status_dough = ttk.Label(self.master, text="", foreground="green")
        self.label_status_dough.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        # Initialize ingredient and product counters
        self.ingredients_for_cream = 0
        self.ingredients_for_dough = 0
        self.cream_ready = False
        self.dough_ready = False
        self.cakes_count = 0
        self.donuts_count = 0

        # Lock for thread synchronization
        self.lock = Lock()

        # Start the background threads
        self.start_threads()

    def create_widgets(self):
        # Load images
        cream_img = Image.open("cream_image.jpg")
        dough_img = Image.open("dough_image.jpg")
        cake_img = Image.open("cake_image.jpg")
        donut_img = Image.open("donut_image.png")

        # Resize images
        cream_img = cream_img.resize((60, 60), Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.BILINEAR)
        dough_img = dough_img.resize((60, 60), Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.BILINEAR)
        cake_img = cake_img.resize((60, 60), Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.BILINEAR)
        donut_img = donut_img.resize((60, 60), Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.BILINEAR)

        # Convert images to PhotoImage
        self.cream_photo = ImageTk.PhotoImage(cream_img)
        self.dough_photo = ImageTk.PhotoImage(dough_img)
        self.cake_photo = ImageTk.PhotoImage(cake_img)
        self.donut_photo = ImageTk.PhotoImage(donut_img)

        # Create and place labels and entry widgets
        self.label_ingredients_cream = ttk.Label(self.master, text="Ingredients for Cream:")
        self.label_ingredients_cream.grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(self.master, image=self.cream_photo).grid(row=0, column=2, padx=10, pady=5)

        self.label_ingredients_dough = ttk.Label(self.master, text="Ingredients for Dough:")
        self.label_ingredients_dough.grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(self.master, image=self.dough_photo).grid(row=1, column=2, padx=10, pady=5)

        self.label_cakes_count = ttk.Label(self.master, text="Cakes Produced:")
        self.label_cakes_count.grid(row=2, column=0, padx=10, pady=5)
        ttk.Label(self.master, image=self.cake_photo).grid(row=2, column=2, padx=10, pady=5)

        self.label_donuts_count = ttk.Label(self.master, text="Donuts Produced:")
        self.label_donuts_count.grid(row=3, column=0, padx=10, pady=5)
        ttk.Label(self.master, image=self.donut_photo).grid(row=3, column=2, padx=10, pady=5)

        # Create Quit button
        self.btn_quit = ttk.Button(self.master, text="Quit", command=self.master.quit)
        self.btn_quit.grid(row=6, column=0, padx=10, pady=10)

        # StringVar to store ingredient and product counts
        self.var_ingredients_cream = tk.StringVar()
        self.var_ingredients_dough = tk.StringVar()
        self.var_cakes_count = tk.StringVar()
        self.var_donuts_count = tk.StringVar()

        # Entry widgets to display counts
        self.entry_ingredients_cream = ttk.Entry(self.master, textvariable=self.var_ingredients_cream, state="readonly")
        self.entry_ingredients_cream.grid(row=0, column=1, padx=10, pady=5)

        self.entry_ingredients_dough = ttk.Entry(self.master, textvariable=self.var_ingredients_dough, state="readonly")
        self.entry_ingredients_dough.grid(row=1, column=1, padx=10, pady=5)

        self.entry_cakes_count = ttk.Entry(self.master, textvariable=self.var_cakes_count, state="readonly")
        self.entry_cakes_count.grid(row=2, column=1, padx=10, pady=5)

        self.entry_donuts_count = ttk.Entry(self.master, textvariable=self.var_donuts_count, state="readonly")
        self.entry_donuts_count.grid(row=3, column=1, padx=10, pady=5)

    def update_gui(self):
        # Update the GUI with the current counts
        self.var_ingredients_cream.set(str(self.ingredients_for_cream))
        self.var_ingredients_dough.set(str(self.ingredients_for_dough))
        self.var_cakes_count.set(str(self.cakes_count))
        self.var_donuts_count.set(str(self.donuts_count))

    def earn_ingredients_for_cream(self):
        # Continuously earn ingredients for cream
        while True:
            time.sleep(random.uniform(2, 4))
            with self.lock:
                self.ingredients_for_cream += 1
                self.update_gui()

    def earn_ingredients_for_dough(self):
        # Continuously earn ingredients for dough
        while True:
            time.sleep(random.uniform(2, 4))
            with self.lock:
                self.ingredients_for_dough += 1
                self.update_gui()

    def prepare_cream(self):
        # Continuously prepare cream if ingredients are available
        while True:
            time.sleep(random.uniform(1, 2))
            with self.lock:
                if self.ingredients_for_cream >= 4:
                    self.cream_ready = True
                    self.ingredients_for_cream -= 4
                    self.update_gui()
                    self.show_status_message("Cream is ready!")
                    self.master.after(3000, self.hide_status_message)

    def prepare_dough(self):
        # Continuously prepare dough if ingredients are available
        while True:
            time.sleep(random.uniform(1, 2))
            with self.lock:
                if self.ingredients_for_dough >= 4:
                    self.dough_ready = True
                    self.ingredients_for_dough -= 4
                    self.update_gui()
                    self.show_status_message_2("Dough is ready!")
                    self.master.after(3000, self.hide_status_message_2)

    def show_status_message(self, message):
        # Show cream status message
        self.label_status_cream.config(text=message)

    def hide_status_message(self):
        # Hide cream status message
        self.label_status_cream.config(text="")

    def show_status_message_2(self, message):
        # Show dough status message
        self.label_status_dough.config(text=message)

    def hide_status_message_2(self):
        # Hide dough status message
        self.label_status_dough.config(text="")

    def bake_cake(self):
        # Continuously bake cakes if cream and dough are ready
        while True:
            time.sleep(random.uniform(2, 4))
            with self.lock:
                if self.cream_ready and self.dough_ready:
                    self.cream_ready = False
                    self.dough_ready = False
                    self.cakes_count += 1
                    self.update_gui()

    def bake_donut(self):
        # Continuously bake donuts if cream and dough are ready
        while True:
            time.sleep(random.uniform(2, 4))
            with self.lock:
                if self.cream_ready and self.dough_ready:
                    self.cream_ready = False
                    self.dough_ready = False
                    self.donuts_count += 1
                    self.update_gui()

    def start_threads(self):
        # Start all the background threads
        Thread(target=self.earn_ingredients_for_cream, daemon=True).start()
        Thread(target=self.earn_ingredients_for_dough, daemon=True).start()
        Thread(target=self.prepare_cream, daemon=True).start()
        Thread(target=self.prepare_dough, daemon=True).start()
        Thread(target=self.bake_cake, daemon=True).start()
        Thread(target=self.bake_donut, daemon=True).start()


# Create the main application window and run the app
root = tk.Tk()
app = CakeFactoryApp(root)
root.mainloop()
