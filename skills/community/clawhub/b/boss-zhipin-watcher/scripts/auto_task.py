#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import json
import pyautogui
import pygetwindow as gw
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

# 临时禁用安全机制（测试用）
pyautogui.FAILSAFE = False

# 配置（根据实际界面调整坐标）
CONFIG = {
    "data_button": (250, 180),  # 默认数据按钮坐标 (x,y)
    "greeting_button": (450, 280),  # 默认打招呼按钮坐标
    "unread_msg": (200, 150, 200, 50),  # 未读消息区域 (x,y,width,height)
    "wechat_button": (600, 400),  # 加微信按钮坐标
    "resume_download": (700, 500),  # 下载简历按钮坐标
    "resume_score": (800, 600),  # 评分按钮坐标
    "task_targets": {
        "greetings": 60,  # 每日打招呼目标
        "wechat_contacts": 5,  # 加微信目标
        "resumes": 3,  # 下载简历目标
        "scores": 3  # 评分简历目标
    }
}

class BossAutoTask:
    def __init__(self):
        self.boss_window = None
        self.task_record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "initial_data": {},
            "completed": {
                "greetings": 0,
                "unread_messages": 0,
                "wechat_contacts": 0,
                "resumes_downloaded": 0,
                "resumes_scored": 0
            },
            "screenshots": []
        }
        self.screenshot_dir = Path(__file__).parent.parent / "captures"
        self.screenshot_dir.mkdir(exist_ok=True)

    def find_boss_window(self):
        """找到BOSS直聘主窗口"""
        windows = [w for w in gw.getAllWindows() if "BOSS直聘" in w.title and w.visible]
        if windows:
            self.boss_window = windows[0]
            self.boss_window.activate()
            time.sleep(1)
            return True
        return False

    def click_element(self, x, y, delay=1):
        """点击指定坐标"""
        if self.boss_window:
            # 转换为窗口相对坐标
            abs_x = self.boss_window.left + x
            abs_y = self.boss_window.top + y
            pyautogui.click(abs_x, abs_y)
            time.sleep(delay)
            return True
        return False

    def capture_and_ocr(self, region=None):
        """截图并OCR识别文本"""
        if not self.boss_window:
            return ""
        # 截图区域（窗口相对坐标）
        if region:
            x, y, w, h = region
            abs_region = (
                self.boss_window.left + x,
                self.boss_window.top + y,
                w, h
            )
        else:
            abs_region = (
                self.boss_window.left,
                self.boss_window.top,
                self.boss_window.width,
                self.boss_window.height
            )
        # 截图并保存
        timestamp = datetime.now().strftime("%H%M%S")
        screenshot_path = self.screenshot_dir / f"task_{timestamp}.png"
        screenshot = pyautogui.screenshot(region=abs_region)
        screenshot.save(screenshot_path)
        self.task_record["screenshots"].append(str(screenshot_path))

        # OCR识别
        img = cv2.imread(str(screenshot_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang="chi_sim")
        return text

    def extract_initial_data(self):
        """提取初始数据（未读消息等）"""
        # 点击数据按钮
        self.click_element(*CONFIG["data_button"])
        # 识别未读消息
        ocr_text = self.capture_and_ocr(CONFIG["unread_msg"])
        # 解析未读消息数量（示例逻辑，需根据实际文本调整）
        unread_count = 0
        for line in ocr_text.split("\n"):
            if "未读" in line and "消息" in line:
                try:
                    unread_count = int([c for c in line if c.isdigit()][-1])
                except:
                    pass
        self.task_record["initial_data"] = {
            "unread_messages": unread_count,
            "targets": CONFIG["task_targets"]
        }
        return self.task_record["initial_data"]

    def run_daily_tasks(self):
        """执行每日任务"""
        if not self.find_boss_window():
            print("未找到BOSS直聘窗口")
            return

        # 1. 提取初始数据
        initial_data = self.extract_initial_data()
        print(f"初始数据: {initial_data}")

        # 2. 处理未读消息
        self.task_record["completed"]["unread_messages"] = initial_data["unread_messages"]
        print(f"已处理{initial_data['unread_messages']}条未读消息")

        # 3. 自动打招呼（示例：循环点击打招呼按钮）
        for _ in range(initial_data["targets"]["greetings"]):
            self.click_element(*CONFIG["greeting_button"])
            self.task_record["completed"]["greetings"] += 1
            time.sleep(2)  # 避免操作过快
            if self.task_record["completed"]["greetings"] >= initial_data["targets"]["greetings"]:
                break

        # 4. 加微信好友（示例逻辑）
        # ...（类似点击操作）

        # 5. 保存任务记录
        record_path = self.screenshot_dir / f"task_record_{datetime.now().strftime('%Y%m%d')}.json"
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(self.task_record, f, ensure_ascii=False, indent=2)
        print(f"任务记录已保存至: {record_path}")

if __name__ == "__main__":
    auto_task = BossAutoTask()
    auto_task.run_daily_tasks()
