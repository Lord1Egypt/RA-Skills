

#pip install uiautomation
#python scripts/webchat_download_audio.py

import uiautomation as auto
import time

NAME = "webchat_download_audio"

import pyautogui

def input_search_text(text):
    print(f"⌨️ 使用 pyautogui 输入: {text}")
    
    # 清空输入框
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.2)

    # 输入（避免中文输入法问题）
    pyautogui.write(text, interval=0.05)
    time.sleep(0.5)

def click_user_in_list(win, target_name):
    if not target_name:
        print("❌ 未提供用户名")
        return False

    print(f"🔍 搜索用户: {target_name}")

    # ① 打开搜索
    win.SendKeys('{Ctrl}f')
    time.sleep(1)

    # 👉 ② 用 pyautogui 输入（关键改造点）
    input_search_text(target_name)

    time.sleep(1)

    # ③ 优先用 UIAutomation 找
    user_item = win.ListItemControl(searchDepth=12, Name=target_name)

    if user_item.Exists(0):
        print("✅ UIAutomation 找到用户")
        user_item.Click()
        return True

    print("⚠️ UIAutomation 未找到，尝试 pyautogui 回车")

    # 👉 ④ 兜底方案：直接回车选第一个
    pyautogui.press('enter')
    time.sleep(0.5)

    return True
    
def focus_weixin():
    # 兼容“微信”和“Weixin”两种窗口名称
    weixin_win = auto.WindowControl(searchDepth=1, Name="微信")
    if not weixin_win.Exists(0):
        weixin_win = auto.WindowControl(searchDepth=1, Name="Weixin")

    if weixin_win.Exists(0):
        # 使用 WindowPattern 检查窗口状态
        # WindowVisualState: 0-Normal, 1-Maximized, 2-Minimized
        try:
            pattern = weixin_win.GetWindowPattern()
            if pattern and pattern.WindowVisualState == 2: 
                print("检测到窗口最小化，正在恢复...")
                weixin_win.Restore()
        except Exception:
            # 如果 Pattern 获取失败，强制执行一次 Restore 也是安全的
            weixin_win.Restore()
        
        weixin_win.SetActive()
        # 强制置顶再取消，确保在 OpenClaw 运行环境下窗口能弹到最前面
        weixin_win.SetTopmost(True)
        weixin_win.SetTopmost(False) 
        return weixin_win
    
    print("未发现微信窗口")
    return None

# 在你的 execute 函数中调用
def execute(target_name="文件传输助手"):
    win = focus_weixin() # 使用之前修复过的 focus 函数
    if win:
        if click_user_in_list(win, target_name):
            print("用户跳转成功")
            # 这里继续写你后续的下载音频逻辑
        else:
            print("用户跳转失败")

# if __name__ == "__main__":
#     # 替换为你微信里真实的备注名或昵称
#     target = "文件传输助手"
#     click_user_by_name(target)