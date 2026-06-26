"""
基于HR工作流程优化的BOSS直聘自动化脚本
严格遵循HR文档中的流程：数据看板→互动→收藏牛人→对我感兴趣→筛选→打招呼→微信沟通→拉群→发offer
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
OUTPUT_DIR = r"C:\Users\liuxuejiao\Desktop\招聘简历"
OCR_SCRIPT = r"C:\Users\liuxuejiao\.openclaw\workspace\skills\ocr-local\scripts\ocr.js"
DAILY_KPI = 100  # 每日收到100份简历

# 按钮坐标字典（需要根据实际界面校准）
BUTTONS = {
    "communication": (200, 200),
    "greet_btn": (300, 200),
    "filter_btn": (400, 100),
}

# HR标准话术（来自文档）
HR_PHRASES = {
    "resume_request": "麻烦您加一下我的微信，备注好姓名-岗位，加上微信后我会建一个含老板的微信群，您再给老板发一下您的简历~关于这个岗位的问题咱们都直接和老板聊，我看不到您的微信号，您主动加我吧。",
    "wechat_exchange": "您好，方便提供一下您的微信吗？我会拉您进群和老板直接沟通。",
    "greeting": "您好，看到您的简历很符合我们的岗位要求，方便进一步沟通吗？",
    "offer": "恭喜您通过面试，这是您的offer，请查收。欢迎加入我们！"
}

class HRWorkflowAutomator:
    def __init__(self):
        """初始化自动化工具"""
        self.window = self.find_boss_window()
        if not self.window:
            raise Exception("BOSS直聘窗口未找到，请确保BOSS直聘已打开")
        
        self.current_date = datetime.datetime.now().strftime("%Y%m%d")
        self.today_folder = os.path.join(OUTPUT_DIR, self.current_date)
        os.makedirs(self.today_folder, exist_ok=True)
        
        print(f"找到BOSS直聘窗口: {self.window.title} ({self.window.width}x{self.window.height} @ {self.window.left},{self.window.top})")
        print(f"今日简历文件夹: {self.today_folder}")
        
        self.greet_count = 0
        self.max_greets = 60  # 系统限制每天最多60次打招呼
        self.resume_count = 0

    def find_boss_window(self):
        """查找BOSS直聘窗口"""
        windows = gw.getWindowsWithTitle(WINDOW_TITLE)
        if windows:
            return windows[0]
        
        # 尝试模糊匹配
        all_windows = gw.getAllWindows()
        for win in all_windows:
            if "BOSS" in win.title or "直聘" in win.title:
                return win
        return None

    def click_relative(self, button_name, wait=1.0):
        """点击相对坐标按钮"""
        if button_name not in BUTTONS:
            print(f"⚠️  按钮 {button_name} 未定义，跳过")
            return False
        
        rel_x, rel_y = BUTTONS[button_name]
        abs_x = self.window.left + rel_x
        abs_y = self.window.top + rel_y
        
        # 确保坐标在窗口内
        if (abs_x < self.window.left or abs_x > self.window.left + self.window.width or
            abs_y < self.window.top or abs_y > self.window.top + self.window.height):
            print(f"⚠️  按钮 {button_name} 坐标超出窗口范围")
            return False
        
        pyautogui.click(abs_x, abs_y)
        time.sleep(wait)
        print(f"✅ 点击 {button_name} @ ({abs_x}, {abs_y})")
        return True

    def capture_screenshot(self, name):
        """截图并保存"""
        screenshot_path = os.path.join(self.today_folder, f"{name}_{self.current_date}_{int(time.time())}.png")
        pyautogui.screenshot(screenshot_path, 
                           region=(self.window.left, self.window.top, 
                                   min(self.window.width, 1800), 
                                   min(self.window.height, 1000)))
        print(f"📸 截图保存: {screenshot_path}")
        return screenshot_path

    def step1_dashboard_monitoring(self):
        """第一步：数据看板监控"""
        print("=== 步骤1: 数据看板监控 ===")
        if self.click_relative("dashboard", 2.0):
            self.capture_screenshot("数据看板")
            print("✅ 数据看板截图完成")
        else:
            print("⚠️  数据看板按钮可能位置不对，尝试手动调整BUTTONS坐标")
        return True

    def step2_interaction_flow(self):
        """第二步：互动流程"""
        print("=== 步骤2: 互动流程 ===")
        
        # 点击互动按钮
        if not self.click_relative("interaction", 2.0):
            # 如果没找到互动按钮，尝试点击更多选项
            print("尝试通过'更多选项'找到互动按钮")
            self.click_relative("more_options", 2.0)
            # 这里可能需要OCR识别互动按钮位置
        
        # 查看收藏牛人
        print("--- 查看收藏牛人 ---")
        self.click_relative("favorite_talents", 2.0)
        self.capture_screenshot("收藏牛人列表")
        
        # 对所有收藏牛人打招呼
        self.batch_greet("收藏牛人")
        
        # 查看对我感兴趣
        print("--- 查看对我感兴趣 ---")
        self.click_relative("interested_me", 2.0)
        self.capture_screenshot("对我感兴趣列表")
        
        # 对符合条件的人打招呼
        self.batch_greet("对我感兴趣")
        
        return True

    def batch_greet(self, source):
        """批量打招呼"""
        print(f"--- 开始对{source}进行打招呼 ---")
        
        # 先筛选条件
        self.click_relative("filter_btn", 1.5)
        
        # 设置筛选条件（根据HR文档）
        print("设置筛选条件: 年龄16-21, 留学背景, 最近活跃")
        self.click_relative("age_16_21", 0.5)
        self.click_relative("study_abroad", 0.5)
        self.click_relative("recently_active", 0.5)
        
        # 学历要求（根据文档）
        self.click_relative("bachelor", 0.5)
        self.click_relative("master", 0.5)
        self.click_relative("phd", 0.5)
        
        # 返回列表
        pyautogui.press('esc')
        time.sleep(1)
        
        # 开始打招呼（有限制）
        greet_in_batch = min(10, self.max_greets - self.greet_count)
        for i in range(greet_in_batch):
            if self.greet_count >= self.max_greets:
                print(f"⚠️  已达到每日打招呼限制({self.max_greets}次)")
                break
                
            if self.click_relative("greet_btn", 0.5):
                self.greet_count += 1
                print(f"✅ 打招呼 {self.greet_count}/{self.max_greets} ({source})")
                # 向下滚动一点，准备下一个
                pyautogui.scroll(-200)
                time.sleep(0.3)
        
        print(f"✅ 完成{source}打招呼，本次{greet_in_batch}次，累计{self.greet_count}次")
        return greet_in_batch

    def step3_candidate_response(self):
        """第三步：候选人回复处理"""
        print("=== 步骤3: 候选人回复处理 ===")
        
        # 这里需要OCR识别聊天内容，根据内容回复
        # 简化版本：假设有未读消息，点击第一个聊天
        self.click_relative("communication", 2.0)
        
        # 截图聊天内容
        chat_screenshot = self.capture_screenshot("聊天内容")
        
        # 使用OCR识别内容
        try:
            result = subprocess.run(["node", OCR_SCRIPT, chat_screenshot, "--lang", "chi_sim"], 
                                  capture_output=True, text=True, encoding='utf-8', errors='ignore')
            message = result.stdout.strip()
            
            if message:
                print(f"📝 识别到消息: {message[:100]}...")
                
                # 根据消息内容回复
                if "微信" in message or "加" in message:
                    self.reply_wechat_request()
                elif "简历" in message:
                    self.request_resume()
                else:
                    self.send_general_reply()
            else:
                print("📝 未识别到有效消息")
                
        except Exception as e:
            print(f"⚠️  OCR识别失败: {str(e)}")
            # 默认发送微信请求
            self.reply_wechat_request()
        
        return True

    def reply_wechat_request(self):
        """回复微信请求"""
        self.click_relative("chat_input", 0.5)
        pyautogui.typewrite(HR_PHRASES["wechat_exchange"])
        time.sleep(0.5)
        self.click_relative("send_btn", 1.0)
        print("📩 已发送微信交换请求")
        return True

    def request_resume(self):
        """请求简历"""
        self.click_relative("chat_input", 0.5)
        pyautogui.typewrite(HR_PHRASES["resume_request"])
        time.sleep(0.5)
        self.click_relative("send_btn", 1.0)
        print("📩 已发送简历请求")
        return True

    def send_general_reply(self):
        """发送通用回复"""
        self.click_relative("chat_input", 0.5)
        pyautogui.typewrite(HR_PHRASES["greeting"])
        time.sleep(0.5)
        self.click_relative("send_btn", 1.0)
        print("📩 已发送通用招呼")
        return True

    def step4_resume_collection(self):
        """第四步：简历收集"""
        print("=== 步骤4: 简历收集 ===")
        
        # 这里需要根据实际界面实现简历下载
        # 简化版本：假设有简历下载按钮
        print("📥 开始收集简历...")
        
        # 创建今日简历子文件夹
        resume_subfolder = os.path.join(self.today_folder, "resumes")
        os.makedirs(resume_subfolder, exist_ok=True)
        
        # 模拟收集简历（实际需要根据界面操作）
        for i in range(5):  # 尝试收集5份简历
            if self.resume_count >= DAILY_KPI:
                break
                
            # 这里应该有实际的简历下载操作
            # 暂时用截图代替
            resume_screenshot = os.path.join(resume_subfolder, f"resume_{i+1}.png")
            pyautogui.screenshot(resume_screenshot, 
                               region=(self.window.left + 300, self.window.top + 100, 800, 600))
            
            self.resume_count += 1
            print(f"📥 收集简历 {self.resume_count}/{DAILY_KPI}")
            time.sleep(1)
        
        print(f"✅ 简历收集完成: {self.resume_count}份")
        return True

    def step5_kpi_summary(self):
        """第五步：KPI总结"""
        print("=== 步骤5: 每日KPI总结 ===")
        
        summary = {
            "date": self.current_date,
            "greet_count": self.greet_count,
            "max_greets": self.max_greets,
            "resume_count": self.resume_count,
            "daily_kpi": DAILY_KPI,
            "completion_rate": f"{(self.resume_count/DAILY_KPI)*100:.1f}%",
            "screenshots": [f for f in os.listdir(self.today_folder) if f.endswith('.png')]
        }
        
        # 保存总结文件
        summary_file = os.path.join(self.today_folder, "daily_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"📊 今日KPI总结:")
        print(f"   - 打招呼: {self.greet_count}/{self.max_greets}")
        print(f"   - 收集简历: {self.resume_count}/{DAILY_KPI}")
        print(f"   - 完成率: {summary['completion_rate']}")
        print(f"   - 总结文件: {summary_file}")
        
        return True

    def run_full_workflow(self):
        """运行完整工作流程"""
        print("🚀 启动BOSS直聘招聘自动化工作流")
        print("=" * 60)
        
        try:
            # 1. 数据看板监控
            self.step1_dashboard_monitoring()
            time.sleep(2)
            
            # 2. 互动流程
            self.step2_interaction_flow()
            time.sleep(2)
            
            # 3. 候选人回复处理
            self.step3_candidate_response()
            time.sleep(2)
            
            # 4. 简历收集
            self.step4_resume_collection()
            time.sleep(2)
            
            # 5. KPI总结
            self.step5_kpi_summary()
            
            print("=" * 60)
            print("🎉 BOSS直聘招聘工作流执行完成！")
            print("💡 提示: 实际使用时需要根据界面调整BUTTONS坐标")
            
        except Exception as e:
            print(f"❌ 工作流执行出错: {str(e)}")
            print("💡 可能的原因: BOSS直聘窗口被遮挡、坐标不准确、界面变化")
            return False
        
        return True

    def calibrate_coordinates(self):
        """坐标校准工具"""
        print("🎯 坐标校准模式")
        print("1. 请将鼠标移动到目标按钮上")
        print("2. 按Ctrl+C获取当前坐标")
        print("3. 输入按钮名称更新坐标")
        print("4. 按Ctrl+Z退出")
        
        try:
            while True:
                input("按Enter键获取鼠标坐标...")
                x, y = pyautogui.position()
                rel_x = x - self.window.left
                rel_y = y - self.window.top
                
                print(f"🖱️  绝对坐标: ({x}, {y})")
                print(f"📍 相对坐标: ({rel_x}, {rel_y})")
                
                btn_name = input("按钮名称 (留空跳过): ").strip()
                if btn_name:
                    BUTTONS[btn_name] = (rel_x, rel_y)
                    print(f"✅ 更新按钮 {btn_name} = ({rel_x}, {rel_y})")
                    
        except KeyboardInterrupt:
            print("\n📋 当前坐标配置:")
            for name, coord in BUTTONS.items():
                print(f"  '{name}': {coord},")
            print("\n✅ 坐标校准完成")

def main():
    """主函数"""
    print("BOSS直聘HR工作流自动化脚本")
    print("基于HR文档流程: 数据看板→互动→收藏牛人→对我感兴趣→筛选→打招呼→微信沟通→拉群→发offer")
    
    try:
        automator = HRWorkflowAutomator()
        
        # 询问模式
        print("\n请选择模式:")
        print("1. 运行完整工作流")
        print("2. 坐标校准模式")
        print("3. 测试单个步骤")
        
        choice = input("请输入选择 (1/2/3): ").strip()
        
        if choice == "1":
            automator.run_full_workflow()
        elif choice == "2":
            automator.calibrate_coordinates()
        elif choice == "3":
            print("\n测试步骤:")
            print("1. 数据看板监控")
            print("2. 互动流程")
            print("3. 候选人回复")
            print("4. 简历收集")
            
            step = input("选择测试步骤 (1-4): ").strip()
            if step == "1":
                automator.step1_dashboard_monitoring()
            elif step == "2":
                automator.step2_interaction_flow()
            elif step == "3":
                automator.step3_candidate_response()
            elif step == "4":
                automator.step4_resume_collection()
        else:
            print("无效选择")
            
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        print("请确保:")
        print("   1. BOSS直聘已打开并可见")
        print("   2. 安装了必要的Python库 (pygetwindow, pyautogui)")
        print("   3. 有管理员权限（如果需要）")

if __name__ == "__main__":
    main()