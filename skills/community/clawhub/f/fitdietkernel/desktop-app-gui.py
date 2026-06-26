#!/usr/bin/env python3
import PySimpleGUI as sg
import json
import os
from datetime import datetime

# 配置主题
sg.theme("DarkGreen13")

DATA_FILE = "fitdiet_data.json"


class FitDietApp:
    def __init__(self):
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
        self.window = None

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"weight": 89.2, "weight_history": []}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f)

    def build_ui(self):
        today_idx = datetime.today().weekday()
        mode = self.schedule[today_idx]
        c, p, f = self.macros[mode]

        layout = [
            [
                sg.Text(
                    "FIT⚡DIET",
                    font=("SF Pro Display", 24, "bold"),
                    text_color="#00ff88",
                    justification="center",
                )
            ],
            [
                sg.Text(
                    "Kernel v1.0",
                    font=("SF Pro", 8),
                    text_color="#666",
                    justification="center",
                )
            ],
            [sg.Text("")],
            # 今日档位
            [
                sg.Text(
                    f"今日档位: {mode}",
                    font=("SF Pro", 14, "bold"),
                    text_color="#ffa502",
                    justification="center",
                )
            ],
            [
                sg.Text(
                    f"碳水 {c}g  |  蛋白 {p}g  |  脂肪 {f}g",
                    font=("SF Pro", 10),
                    text_color="#888",
                    justification="center",
                )
            ],
            [sg.HorizontalSeparator(color="#333")],
            # 打卡
            [sg.Text("今日打卡", font=("SF Pro", 12, "bold"))],
        ]

        for i, (t, n, d) in enumerate(self.meals[mode]):
            checked = i in self.checked_meals
            btn_color = ("#00ff88", "#000") if checked else ("#1a1a25", "#fff")
            layout.append(
                [
                    sg.Button(
                        f"{t} {n}\n{d}",
                        key=f"-MEAL-{i}-",
                        font=("SF Pro", 9),
                        button_color=btn_color,
                        border_width=1,
                        size=(30, 2),
                    )
                ]
            )

        layout.extend(
            [
                [sg.HorizontalSeparator(color="#333")],
                # 体重
                [sg.Text("体重追踪", font=("SF Pro", 12, "bold"))],
                [
                    sg.Text(
                        f"{self.data['weight']} kg",
                        font=("SF Pro", 28, "bold"),
                        text_color="#00ff88",
                        justification="center",
                    )
                ],
                [
                    sg.Input(key="-WEIGHT-", size=(10, 1), font=("SF Pro", 10)),
                    sg.Button("记录", key="-SAVE-", button_color=("#00ff88", "#000")),
                ],
                # 换算表
                [sg.HorizontalSeparator(color="#333")],
                [
                    sg.Text(
                        "10g碳水换算", font=("SF Pro", 10, "bold"), text_color="#666"
                    )
                ],
                [
                    sg.Text(
                        "燕麦16g | 意面13g | 馒头0.5个\n蓝莓72g | 红薯50g | 玉米45g",
                        font=("SF Pro", 8),
                        text_color="#888",
                        justification="center",
                    )
                ],
                [sg.Text("")],
                [
                    sg.Text(
                        datetime.now().strftime("%Y-%m-%d %H:%M"),
                        font=("SF Pro", 8),
                        text_color="#444",
                        justification="center",
                    )
                ],
            ]
        )

        return sg.Window(
            "FitDietKernel", layout, finalize=True, keep_on_top=True, size=(320, 600)
        )

    def run(self):
        self.window = self.build_ui()

        while True:
            event, values = self.window.read(timeout=1000)

            if event in (sg.WIN_CLOSED, "Exit"):
                break

            if event.startswith("-MEAL-"):
                idx = int(event.split("-")[2])
                if idx in self.checked_meals:
                    self.checked_meals.remove(idx)
                else:
                    self.checked_meals.add(idx)
                self.window.close()
                self.window = self.build_ui()

            if event == "-SAVE-":
                w = values["-WEIGHT-"]
                if w:
                    self.data["weight"] = float(w)
                    self.data["weight_history"].append(
                        {"d": datetime.now().strftime("%m-%d"), "w": float(w)}
                    )
                    self.save_data()
                    self.window.close()
                    self.window = self.build_ui()

        self.window.close()


if __name__ == "__main__":
    app = FitDietApp()
    app.run()
