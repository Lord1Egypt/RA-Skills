"""
BOSS直聘招聘全流程自动化脚本
实现打招呼、回复、简历收集、微信沟通等完整流程
"""

import pygetwindow as gw
import pyautogui
import time
import os
import datetime
import json
import subprocess

# 配置项
WINDOW_TITLE = "BOSS直聘"
OUTPUT_DIR = "C:\Users\liuxuejiao\Desktop\招聘简历"
OCR_SCRIPT = "C:\Users\liuxuejiao\.openclaw\workspace\skills\ocr-local\scripts\ocr.js"
WECHAT_GROUP_PREFIX = "实习生-"
BOSS_WECHAT_IDS = ["孙博1", "孙博2", "孙博3"]
DAILY_KPI = 100

# 预设按钮坐标（根据实际界面调整）
BUTTONS = {
    "dashboard": (50, 30),          # 数据看板
    "interaction": (170, 30),        # 互动按钮
    "favorite_talents": (290, 30),   # 收藏牛人
    "interested_me": (410, 30),      # 对我感兴趣
    "recommendation": (530, 30),     # 推荐按钮
    "filter": (650, 30),            # 筛选按钮
    "age_filter": (100, 200),        # 年龄筛选
    "study_abroad": (200, 200),      # 留学背景
    "just_active": (300, 200),       # 刚刚活跃
    "greet": (400, 200),            # 打招呼按钮
    "chat_1": (150, 130),           # 第一个聊天
    "resume_request": (500, 600),    # 求简历
    "wechat_exchange": (600, 600),   # 换微信
    "send": (800, 600)              # 发送按钮
}

# 常用回复话术
REPLIES = {
    "resume_request": "麻烦您加一下我的微信，备注好姓名-岗位，加上微信后我会建一个含老板的微信群，您再给老板发一下您的简历~关于这个岗位的问题咱们都直接和老板聊，我看不到您的微信号，您主动加我吧。",
    "wechat_exchange": "您好，方便提供一下您的微信吗？我会拉您进群和老板直接沟通。",
    "default": "您好，感谢您的关注，我们会尽快联系您！"
}

class RecruitmentAutomator:
    def __init__(self):
        self.window = self.find_boss_window()
        if not self.window:
            raise Exception("BOSS直聘窗口未找到")
        self.current_date = datetime.datetime.now().strftime("%Y%m%d")
        self.resume_folder = os.path.join(OUTPUT_DIR, self.current_date)
        os.makedirs(self.resume_folder, exist_ok=True)
        self.resume_count = 0

    def find_boss_window(self):
        """查找BOSS直聘窗口"""
        windows = gw.getWindowsWithTitle(WINDOW_TITLE)
        return windows[0] if windows else None

    def click_button(self, button_name):
        """点击指定按钮"""
        if button_name not in BUTTONS:
            print(f"❌ 按钮 {button_name} 未定义")
            return
        x, y = BUTTONS[button_name]
        abs_x = self.window.left + x
        abs_y = self.window.top + y
        pyautogui.click(abs_x, abs_y)
        time.sleep(1)
        print(f"✅ 点击 {button_name} @ ({abs_x}, {abs_y})")

    def capture_dashboard(self):
        """截图数据看板"""
        screenshot_path = os.path.join(self.resume_folder, f"dashboard_{self.current_date}.png")
        pyautogui.screenshot(screenshot_path, region=(self.window.left, self.window.top, self.window.width, self.window.height))
        print(f"📸 数据看板截图保存到: {screenshot_path}")
        return screenshot_path

    def filter_candidates(self):
        """筛选候选人（总助实习生）"""
        self.click_button("recommendation")
        self.click_button("filter")
        # 设置年龄筛选
        self.click_button("age_filter")
        pyautogui.typewrite("16-21")
        # 选择留学背景
        self.click_button("study_abroad")
        # 选择刚刚活跃
        self.click_button("just_active")
        time.sleep(2)
        print("✅ 筛选条件设置完成")

    def greet_candidates(self):
        """批量打招呼"""
        greet_count = 0
        while greet_count < 60:  # 每天最多60次
            try:
                self.click_button("greet")
                greet_count += 1
                print(f"✅ 打招呼 {greet_count}/60")
                time.sleep(0.5)
            except:
                break
        print(f"✅ 完成打招呼 {greet_count}次")

    def process_chat(self):
        """处理聊天消息"""
        self.click_button("chat_1")
        time.sleep(1)
        # 识别消息内容
        chat_screenshot = os.path.join(self.resume_folder, f"chat_temp.png")
        pyautogui.screenshot(chat_screenshot, region=(self.window.left + 300, self.window.top + 100, 800, 500))
        # OCR识别
        result = subprocess.run(["node", OCR_SCRIPT, chat_screenshot, "--lang", "chi_sim"], capture_output=True, text=True)
        message = result.stdout.strip()
        os.remove(chat_screenshot)
        
        # 根据消息内容回复
        if "简历" in message or "微信" in message:
            self.click_button("resume_request")
            pyautogui.typewrite(REPLIES["resume_request"])
            self.click_button("send")
            print(f"📩 发送简历请求")
        else:
            self.click_button("wechat_exchange")
            pyautogui.typewrite(REPLIES["wechat_exchange"])
            self.click_button("send")
            print(f"📩 发送微信请求")

    def collect_resumes(self):
        """收集简历"""
        # 假设简历下载按钮坐标
        resume_download = (700, 300)
        abs_x = self.window.left + resume_download[0]
        abs_y = self.window.top + resume_download[1]
        pyautogui.click(abs_x, abs_y)
        time.sleep(2)
        self.resume_count += 1
        print(f"📥 收集简历 {self.resume_count}/{DAILY_KPI}")

    def run_daily_kpi(self):
        """完成每日KPI"""
        while self.resume_count < DAILY_KPI:
            self.filter_candidates()
            self.greet_candidates()
            self.process_chat()
            self.collect_resumes()
            time.sleep(5)
        print(f"🎉 今日KPI完成: {self.resume_count}份简历")

    def run_full_workflow(self):
        """运行完整工作流"""
        try:
            print("=== 开始招聘工作流 ===")
            # 1. 数据看板截图
            self.capture_dashboard()
            # 2. 互动流程
            self.click_button("interaction")
            self.click_button("favorite_talents")
            self.greet_candidates()
            self.click_button("interested_me")
            self.greet_candidates()
            # 3. 推荐筛选
            self.filter_candidates()
            self.greet_candidates()
            # 4. 处理聊天
            self.process_chat()
            # 5. 收集简历
            self.collect_resumes()
            # 6. 完成KPI
            self.run_daily_kpi()
            print("=== 工作流完成 ===")
        except Exception as e:
            print(f"❌ 工作流异常: {str(e)}")

if __name__ == "__main__":
    try:
        automator = RecruitmentAutomator()
        automator.run_full_workflow()
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
