#!/usr/bin/env python3
import customtkinter as ctk
import json
import os
from datetime import datetime
from threading import Thread
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# 配置
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

DATA_FILE = "fitdiet_data.json"


class FitDietApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FitDiet Kernel")
        self.geometry("400x700")
        self.resizable(False, False)

        self.load_data()
        self.setup_ui()
        self.update_time()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "weight": 89.2,
                "target": 85,
                "weight_history": [],
                "meals": {},
            }

        # 碳循环配置
        self.schedule = ["low", "mid", "high", "mid", "mid", "high", "low"]
        self.macros = {
            "low": {"c": 95, "p": 135, "f": 126},
            "mid": {"c": 147, "p": 135, "f": 59},
            "high": {"c": 315, "p": 135, "f": 38},
        }
        self.meals_config = {
            "high": [
                ("08:30", "早餐", "130g燕麦 + 蛋白粉 + 蓝莓"),
                ("12:00", "午餐", "4个杂粮馒头 + 150g肉"),
                ("17:30", "预充能", "意面 + 150g肉 + 玉米"),
                ("21:05", "PWO", "蛋白粉 + 蓝莓 + 馒头"),
            ],
            "mid": [
                ("08:30", "早餐", "65g燕麦 + 蛋白粉 + 蓝莓"),
                ("12:00", "午餐", "2个杂粮馒头 + 150g肉"),
                ("17:30", "预充能", "意面 + 150g肉"),
                ("21:05", "PWO", "蛋白粉 + 蓝莓"),
            ],
            "low": [
                ("09:00", "早餐", "2全蛋 + 蛋白粉 + 蓝莓"),
                ("13:00", "午餐", "180g肉 + 牛油果"),
                ("18:00", "晚餐", "180g肉 + 坚果"),
                ("21:30", "睡前", "蛋白粉"),
            ],
        }

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f)

    def setup_ui(self):
        # 标题
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(20, 10))

        title_label = ctk.CTkLabel(
            title_frame,
            text="FIT⚡DIET",
            font=("SF Pro Display", 28, "bold"),
            text_color="#00ff88",
        )
        title_label.pack()

        ctk.CTkLabel(
            title_frame, text="Kernel v1.0", font=("SF Pro", 10), text_color="#666"
        ).pack()

        # 今日状态卡片
        self.today_card = ctk.CTkFrame(self, corner_radius=20)
        self.today_card.pack(fill="x", padx=15, pady=10)

        # 档位标签
        today_idx = datetime.today().weekday()
        today_mode = self.schedule[today_idx]
        mode_colors = {"low": "#5352ed", "mid": "#ffa502", "high": "#ff4757"}

        self.mode_label = ctk.CTkLabel(
            self.today_card,
            text=f"今日: {today_mode.upper()}",
            font=("SF Pro", 12, "bold"),
            text_color=mode_colors[today_mode],
        )
        self.mode_label.pack(pady=(15, 5))

        ctk.CTkLabel(
            self.today_card,
            text=f"碳水目标: {self.macros[today_mode]['c']}g",
            font=("SF Pro", 16, "bold"),
        ).pack(pady=5)

        # 进度条
        self.progress_c = ctk.CTkProgressBar(self.today_card, progress_color="#ffa502")
        self.progress_c.pack(fill="x", padx=20, pady=10)
        self.progress_c.set(0)

        # 宏量数据
        macro_frame = ctk.CTkFrame(self.today_card, fg_color="transparent")
        macro_frame.pack(fill="x", padx=15, pady=(0, 15))

        macros = self.macros[today_mode]
        for name, val in [
            ("碳水", f"{macros['c']}g"),
            ("蛋白", f"{macros['p']}g"),
            ("脂肪", f"{macros['f']}g"),
        ]:
            ctk.CTkLabel(macro_frame, text=val, font=("SF Pro", 14, "bold")).pack(
                side="left", expand=True
            )
            ctk.CTkLabel(
                macro_frame, text=name, font=("SF Pro", 10), text_color="#666"
            ).pack(side="left", padx=(0, 15))

        # 打卡卡片
        check_card = ctk.CTkFrame(self, corner_radius=20)
        check_card.pack(fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(check_card, text="今日打卡", font=("SF Pro", 14, "bold")).pack(
            pady=(15, 10)
        )

        self.meal_buttons = []
        for time, name, desc in self.meals_config[today_mode]:
            btn = ctk.CTkButton(
                check_card,
                text=f"{time} {name}\n{desc}",
                fg_color="#1a1a25",
                hover_color="#00ff88",
                border_width=1,
                border_color="#333",
                text_color="#fff",
                font=("SF Pro", 11),
                height=50,
                command=lambda b=len(self.meal_buttons): self.toggle_meal(b),
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.meal_buttons.append(btn)

        # 体重卡片
        weight_card = ctk.CTkFrame(self, corner_radius=20)
        weight_card.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(weight_card, text="体重追踪", font=("SF Pro", 14, "bold")).pack(
            pady=(15, 10)
        )

        self.weight_label = ctk.CTkLabel(
            weight_card,
            text=f"{self.data['weight']} kg",
            font=("SF Pro", 32, "bold"),
            text_color="#00ff88",
        )
        self.weight_label.pack()

        weight_input_frame = ctk.CTkFrame(weight_card, fg_color="transparent")
        weight_input_frame.pack(fill="x", padx=15, pady=10)

        self.weight_input = ctk.CTkEntry(
            weight_input_frame,
            placeholder_text="输入体重",
            fg_color="#1a1a25",
            border_color="#333",
        )
        self.weight_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            weight_input_frame,
            text="记录",
            fg_color="#00ff88",
            text_color="#000",
            width=60,
            command=self.save_weight,
        ).pack(side="left")

        # 时间显示
        self.time_label = ctk.CTkLabel(
            self, text="", font=("SF Pro", 10), text_color="#444"
        )
        self.time_label.pack(pady=10)

    def toggle_meal(self, idx):
        btn = self.meal_buttons[idx]
        if btn.cget("fg_color") == "#00ff88":
            btn.configure(fg_color="#1a1a25", text_color="#fff")
        else:
            btn.configure(fg_color="#00ff88", text_color="#000")

    def save_weight(self):
        w = self.weight_input.get()
        if not w:
            return
        self.data["weight"] = float(w)
        self.data["weight_history"].append(
            {"d": datetime.now().strftime("%m-%d"), "w": float(w)}
        )
        self.save_data()

        self.weight_label.configure(text=f"{w} kg")
        self.weight_input.delete(0, "end")

    def update_time(self):
        now = datetime.now()
        self.time_label.configure(text=now.strftime("%Y年%m月%d日 %H:%M"))
        self.after(1000, self.update_time)


if __name__ == "__main__":
    app = FitDietApp()
    app.mainloop()
