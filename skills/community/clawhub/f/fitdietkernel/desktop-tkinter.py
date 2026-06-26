#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime

# 颜色配置
BG_COLOR = "#0a0a0f"
CARD_COLOR = "#12121a"
TEXT_COLOR = "#ffffff"
DIM_COLOR = "#666666"
ACCENT_COLOR = "#00ff88"
ORANGE_COLOR = "#ffa502"

DATA_FILE = "fitdiet_data.json"


class FitDietApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FitDiet Kernel")
        self.root.geometry("350x650")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.load_data()
        self.schedule = ["低", "中", "高", "中", "中", "高", "低"]
        self.macros = {"低": (95, 135, 126), "中": (147, 135, 59), "高": (315, 135, 38)}
        self.meals = {
            "高": [
                ("08:30", "早餐", "130g燕麦+蛋白粉+蓝莓"),
                ("12:00", "午餐", "4个馒头+150g肉"),
                ("17:30", "预充能", "意面+150g肉+玉米"),
                ("21:05", "PWO", "蛋白粉+蓝莓+馒头"),
            ],
            "中": [
                ("08:30", "早餐", "65g燕麦+蛋白粉+蓝莓"),
                ("12:00", "午餐", "2个馒头+150g肉"),
                ("17:30", "预充能", "意面+150g肉"),
                ("21:05", "PWO", "蛋白粉+蓝莓"),
            ],
            "低": [
                ("09:00", "早餐", "2全蛋+蛋白粉+蓝莓"),
                ("13:00", "午餐", "180g肉+牛油果"),
                ("18:00", "晚餐", "180g肉+坚果"),
                ("21:30", "睡前", "蛋白粉"),
            ],
        }

        self.checked_meals = set()
        self.setup_ui()
        self.update_time()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"weight": 89.2, "weight_history": []}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f)

    def setup_ui(self):
        # 标题
        title = tk.Label(
            self.root,
            text="FIT⚡DIET",
            font=("SF Pro Display", 24, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
        )
        title.pack(pady=(20, 5))

        tk.Label(
            self.root, text="Kernel v1.0", font=("SF Pro", 8), bg=BG_COLOR, fg=DIM_COLOR
        ).pack()

        # 今日档位
        today_idx = datetime.today().weekday()
        mode = self.schedule[today_idx]
        c, p, f = self.macros[mode]

        mode_card = tk.Frame(self.root, bg=CARD_COLOR, bd=1, relief="flat")
        mode_card.pack(fill="x", padx=15, pady=15)

        tk.Label(
            mode_card,
            text=f"今日档位: {mode}",
            font=("SF Pro", 14, "bold"),
            bg=CARD_COLOR,
            fg=ORANGE_COLOR,
        ).pack(pady=10)
        tk.Label(
            mode_card,
            text=f"碳水 {c}g  |  蛋白 {p}g  |  脂肪 {f}g",
            font=("SF Pro", 10),
            bg=CARD_COLOR,
            fg=DIM_COLOR,
        ).pack(pady=(0, 10))

        # 打卡
        check_card = tk.Frame(self.root, bg=CARD_COLOR, bd=1, relief="flat")
        check_card.pack(fill="both", expand=True, padx=15, pady=5)

        tk.Label(
            check_card,
            text="今日打卡",
            font=("SF Pro", 12, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
        ).pack(pady=10)

        self.meal_buttons = []
        for i, (t, n, d) in enumerate(self.meals[mode]):
            btn = tk.Button(
                check_card,
                text=f"{t} {n}\n{d}",
                font=("SF Pro", 9),
                bg="#1a1a25",
                fg=TEXT_COLOR,
                bd=1,
                relief="flat",
                wraplength=250,
                command=lambda idx=i: self.toggle_meal(idx),
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.meal_buttons.append(btn)

        # 体重
        weight_card = tk.Frame(self.root, bg=CARD_COLOR, bd=1, relief="flat")
        weight_card.pack(fill="x", padx=15, pady=10)

        tk.Label(
            weight_card,
            text="体重追踪",
            font=("SF Pro", 12, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
        ).pack(pady=10)

        self.weight_label = tk.Label(
            weight_card,
            text=f"{self.data['weight']} kg",
            font=("SF Pro", 28, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR,
        )
        self.weight_label.pack()

        input_frame = tk.Frame(weight_card, bg=CARD_COLOR)
        input_frame.pack(pady=10)

        self.weight_input = tk.Entry(
            input_frame,
            font=("SF Pro", 10),
            bg="#1a1a25",
            fg=TEXT_COLOR,
            bd=0,
            width=12,
        )
        self.weight_input.pack(side="left", padx=5)

        tk.Button(
            input_frame,
            text="记录",
            font=("SF Pro", 10),
            bg=ACCENT_COLOR,
            fg=BG_COLOR,
            bd=0,
            command=self.save_weight,
        ).pack(side="left")

        # 换算表
        tk.Label(
            self.root,
            text="10g碳水换算: 燕麦16g | 意面13g | 馒头0.5个 | 蓝莓72g | 红薯50g",
            font=("SF Pro", 8),
            bg=BG_COLOR,
            fg=DIM_COLOR,
        ).pack(pady=5)

        # 时间
        self.time_label = tk.Label(
            self.root, text="", font=("SF Pro", 8), bg=BG_COLOR, fg=DIM_COLOR
        )
        self.time_label.pack(pady=10)

    def toggle_meal(self, idx):
        if idx in self.checked_meals:
            self.checked_meals.remove(idx)
            self.meal_buttons[idx].configure(bg="#1a1a25", fg=TEXT_COLOR)
        else:
            self.checked_meals.add(idx)
            self.meal_buttons[idx].configure(bg=ACCENT_COLOR, fg=BG_COLOR)

    def save_weight(self):
        w = self.weight_input.get()
        if w:
            self.data["weight"] = float(w)
            self.data["weight_history"].append(
                {"d": datetime.now().strftime("%m-%d"), "w": float(w)}
            )
            self.save_data()
            self.weight_label.configure(text=f"{w} kg")
            self.weight_input.delete(0, "end")

    def update_time(self):
        now = datetime.now()
        self.time_label.configure(text=now.strftime("%Y-%m-%d %H:%M"))
        self.root.after(1000, self.update_time)


if __name__ == "__main__":
    root = tk.Tk()
    app = FitDietApp(root)
    root.mainloop()
