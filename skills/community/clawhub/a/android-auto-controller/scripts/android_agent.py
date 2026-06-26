import uiautomator2 as u2
import argparse
import json
import time
import base64
import xml.etree.ElementTree as ET
import os  # 
from openai import OpenAI

# ==========================================
# 0. 全局配置 (从 OpenClaw 注入的环境变量中读取)
# ==========================================
# os.getenv("变量名", "默认值")
VLM_API_KEY = os.getenv("VLM_API_KEY", "sk-anything") 
VLM_BASE_URL = os.getenv("VLM_BASE_URL", "http://127.0.0.1:13009/v1")
VLM_MODEL_NAME = os.getenv("VLM_MODEL_NAME", "qwen3-vl-8b") 

# 注意：环境变量读出来都是字符串，如果是数字需要强转 int()
VLM_COORD_SCALE = int(os.getenv("VLM_COORD_SCALE", "1000"))

# ==========================================
# 1. 初始化与设备感知
# ==========================================
def init_device():
    try:
        d = u2.connect() 
        d.implicitly_wait(10.0)
        # 获取系统当前的逻辑分辨率 (Override size)
        width, height = d.window_size()
        return d, width, height
    except Exception as e:
        return None, 0, 0

def get_device_info(d, width, height):
    """
    【感知能力】获取手机的全局状态信息，供大模型初始决策使用。
    """
    try:
        # 获取基础硬件信息
        info = d.device_info
        # 获取当前正在前台运行的 App 包名和页面 Activity
        current_app = d.app_current()
        
        state = {
            "resolution": f"{width}x{height}",
            "current_package": current_app.get("package"),
            "current_activity": current_app.get("activity"),
            "brand": info.get("brand"),
            "model": info.get("model")
        }
        return f"设备状态: {json.dumps(state, ensure_ascii=False)}"
    except Exception as e:
        return f"获取设备信息失败: {str(e)}"

# ==========================================
# 2. 感知层：XML 与 视觉 分离
# ==========================================

def read_screen_xml(d):
    """
    【感知能力 - 极速版】通过底层 XML 获取屏幕可见文字。速度极快，但防抓取应用会失效。
    """
    try:
        print("🩻 正在进行底层 XML 透视扫描...")
        xml_str = d.dump_hierarchy(compressed=False)
        root = ET.fromstring(xml_str)
        visible_texts = []
        
        for node in root.iter():
            text = node.attrib.get('text', '').strip()
            desc = node.attrib.get('content-desc', '').strip()
            if text and text not in visible_texts: visible_texts.append(text)
            if desc and desc not in visible_texts: visible_texts.append(desc)
                
        if not visible_texts:
            return "扫描异常，未找到文字 (可能遇到了图片界面或系统拦截，建议切换视觉模式)。"
            
        return f"当前屏幕透视文本:\n" + " | ".join(visible_texts)
    except Exception as e:
        return f"XML读取失败: {str(e)}"

def vision_find_element(d, target_desc, width, height):
    """
    【眼睛】截图发给 vLLM (Qwen-VL)，获取目标的物理像素坐标。自带模糊匹配能力。
    """
    try:
        print(f"👀 正在呼叫 VLM 视觉引擎寻找: [{target_desc}]...")
        img_path = "vlm_temp_vision.jpg"
        d.screenshot(img_path)
        
        with open(img_path, "rb") as f:
            base64_img = base64.b64encode(f.read()).decode('utf-8')
            
        client = OpenAI(api_key=VLM_API_KEY, base_url=VLM_BASE_URL)
        
        prompt = f"""
        Analyze this screenshot of a mobile phone. You are an Android UI Automation expert.

        YOUR TASK:
        Find the precise center coordinates [x, y] of: "{target_desc}".

        CRITICAL GUIDELINES:
        1. FUZZY MATCHING ALLOWED: If the exact text is not found, look for highly similar text or semantic matches (e.g., if looking for "小九", and "小九(工作)" or "小九九" is present, target that).
        2. WECHAT SPECIFIC: If looking for the 'Send' button in WeChat, it is usually a GREEN button in the bottom right corner of the screen.

        OUTPUT SPECIFICATIONS:
        Respond ONLY with a valid JSON object in this strict format:
        {{"point": [x, y], "reason": "brief reason"}}

        If the target (or a close fuzzy match) is TRULY NOT VISIBLE on this screen, respond with: {{"point": [], "reason": "not found"}}
        """
        
        response = client.chat.completions.create(
            model=VLM_MODEL_NAME,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        result_str = response.choices[0].message.content
        decision = json.loads(result_str)
        
        point = decision.get("point", [])
        if len(point) == 2:
            vlm_x, vlm_y = point
            real_x = int(vlm_x * (width / VLM_COORD_SCALE))
            real_y = int(vlm_y * (height / VLM_COORD_SCALE))
            
            return f"视觉定位成功: 找到目标，物理坐标为 {real_x},{real_y}。请调用 click_xy 动作进行点击。"
        else:
            return f"视觉定位失败: 画面中未发现 [{target_desc}]。"
            
    except Exception as e:
        return f"视觉引擎报错: {str(e)}"
    
def vlm_analyze_and_plan(d, width, height, current_goal):
    """
    【大脑：综合感知与决策能力】截图发给 VLM，在严格的 ReAct 框架下规划唯一的一步动作。
    """
    try:
        print(f"🧐 VLM 正在观察屏幕以规划下一步 (目标: {current_goal})...")
        img_path = "vlm_plan_vision.jpg"
        d.screenshot(img_path)
        
        with open(img_path, "rb") as f:
            base64_img = base64.b64encode(f.read()).decode('utf-8')
            
        client = OpenAI(api_key=VLM_API_KEY, base_url=VLM_BASE_URL)
        
        prompt = f"""
        You are an advanced Android UI Automation Agent operating in a strict ReAct (Reasoning + Acting) framework.
        
        ULTIMATE GOAL: "{current_goal}"
        
        STRICT ReAct RULES:
        1. NO GUESSING: Base your reasoning ONLY on what is currently, visibly present in the screenshot. Do not assume previous actions succeeded.
        2. ONE STEP AT A TIME: You must ONLY output the SINGLE immediate next action. Never plan step 2 before step 1 is executed and verified.
        3. IF TARGET NOT FOUND: If the element you need is not on screen, your immediate next action MUST be 'swipe' or 'wait', or state that the task cannot proceed.
        
        SCREEN ANALYSIS GUIDE:
        1. INTERRUPTIONS: Check for banners or pop-ups. If present, recommend `wait` or `click_text` to close them.
        2. MISSING TARGETS / SCROLLING: If the user wants to interact with a specific item/contact (e.g., "小九") and it is NOT visible on the current screen, DO NOT hallucinate its presence! Recommend action `swipe` with param "up" to scroll down the list.
        3. TEXT INPUT SOP: You MUST click the text input box FIRST to bring up the keyboard. DO NOT recommend `input` until the cursor is blinking.
        4. ZERO HALLUCINATION: In your 'observation', describe ONLY exactly what is visible in the image. If you do not see the sent message bubble, state "The message is not visible."
        
        OUTPUT SPECIFICATIONS:
        Respond ONLY with a valid JSON object in this exact format:
        {{
          "observation": "What do you explicitly see on the screen right now?",
          "thought": "Based on the observation and the ULTIMATE GOAL, what is the logical SINGLE next step?",
          "recommended_action": {{
            "action": "Must be exactly one of: [vision_find, click_text, click_xy, swipe, input, open_app, press_key, wait, task_complete, task_failed]",
            "param": "The exact parameter. If no parameter, leave as empty string."
          }}
        }}
        """
        
        response = client.chat.completions.create(
            model=VLM_MODEL_NAME,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return json.dumps({"status": "error", "observation": "VLM analysis failed", "decision": str(e), "recommended_action": None}, ensure_ascii=False)

# ==========================================
# 3. 执行层：拟人化物理操作
# ==========================================

def click_by_xy(d, coordinates_str):
    """
    【执行能力】直接点击物理坐标 (x,y)，带有拟人化的按压延迟。
    """
    try:
        x_str, y_str = coordinates_str.split(',')
        x, y = int(x_str.strip()), int(y_str.strip())
        
        print(f"👆 正在模拟人手点击坐标: ({x}, {y})")
        d.touch.down(x, y)
        time.sleep(0.1)
        d.touch.up(x, y)
        time.sleep(1) 
        
        return f"执行成功: 已点击物理坐标 ({x}, {y})"
    except Exception as e:
        return f"坐标点击异常，请确保参数格式为 'x,y'。报错: {str(e)}"

def click_by_text(d, target_text):
    """
    【执行能力】基于底层 XML 属性的文字点击
    """
    try:
        if d(text=target_text).exists:
            d(text=target_text).click()
            time.sleep(1)
            return f"执行成功: 已点击文字 [{target_text}]"
        elif d(description=target_text).exists:
            d(description=target_text).click()
            time.sleep(1)
            return f"执行成功: 已点击图标描述 [{target_text}]"
        else:
            return f"执行失败: XML树中找不到 [{target_text}]。建议尝试视觉定位。"
    except Exception as e:
        return f"点击异常: {str(e)}"

def input_text(d, text_content):
    """
    【执行能力 - 原子】纯粹打字：处理输入法夺权、塞文字。不负责点击发送。
    """
    try:
        print(f"⌨️ 准备纯粹注入文字: {text_content}")
        d.set_fastinput_ime(True)
        time.sleep(0.5) 
        d.send_keys(text_content, clear=True)
        time.sleep(1) 
        d.set_fastinput_ime(False)
        return f"执行成功: 已在当前聚焦的输入框中注入文字 [{text_content}]。请调用视觉工具点击发送。"
    except Exception as e:
        d.set_fastinput_ime(False)
        return f"输入注入失败: {str(e)}"

def swipe_screen(d, direction):
    try:
        d.swipe_ext(direction)
        time.sleep(1.5)
        return f"执行成功: 已模拟向 {direction} 滑动"
    except Exception as e:
        return f"滑动失败: {str(e)}"

def open_app(d, package_name):
    try:
        d.app_start(package_name)
        time.sleep(2)
        return f"执行成功: 已拉起包名 [{package_name}]"
    except Exception as e:
        return f"拉起应用失败: {str(e)}"
    
def press_key(d, key_name):
    """
    【执行能力】按压系统物理按键：home (桌面), back (返回), enter (回车)
    """
    try:
        d.press(key_name)
        time.sleep(1)
        return f"执行成功: 已按压 [{key_name}] 键"
    except Exception as e:
        return f"按键失败: {str(e)}"
    
def wait_action(seconds_str):
    """
    【执行能力】主动休眠等待，用于躲避顶部横幅通知等临时干扰
    """
    try:
        sec = int(seconds_str)
        print(f"⏳ 正在等待 {sec} 秒，避开临时干扰...")
        time.sleep(sec)
        return f"执行成功: 已等待 {sec} 秒"
    except Exception as e:
        return f"等待异常，参数必须是整数: {str(e)}"
    
def smart_open_app(d, app_name):
    """
    【综合能力】大模型专用：直接通过应用中文名（如"淘宝"、"抖音"）打开 App
    """
    app_registry = {
        "微信": "com.tencent.mm",
        "支付宝": "com.eg.android.AlipayGphone",
        "淘宝": "com.taobao.taobao",
        "抖音": "com.ss.android.ugc.aweme",
        "美团": "com.sankuai.meituan",
        "京东": "com.jingdong.app.mall",
        "哔哩哔哩": "tv.danmaku.bili",
        "小红书": "com.xingin.xhs"
    }
    
    try:
        for key, pkg in app_registry.items():
            if key in app_name:
                d.app_start(pkg)
                time.sleep(2)
                return f"执行成功: 已通过包名拉起 [{key}]"
                
        print(f"⚠️ 未知包名，尝试回桌面通过视觉寻找 [{app_name}]...")
        d.press("home")
        time.sleep(1)
        if d(textContains=app_name).exists:
            d(textContains=app_name).click()
            time.sleep(2)
            return f"执行成功: 在桌面上找到了 [{app_name}] 并已点击打开"
        else:
            return f"执行失败: 字典中无包名，且当前桌面上未发现 [{app_name}]，请尝试滑动桌面或手动提供包名。"
    except Exception as e:
        return f"打开应用失败: {str(e)}"

def task_complete_action(reason):
    """
    【状态信号】大模型判定任务已达成，终止 ReAct 循环
    """
    msg = reason if reason else "VLM 判定当前屏幕已达到最终目标。"
    print(f"🎉 任务判定完成: {msg}")
    return f"执行成功: 任务已完成。原因: {msg}"

def task_failed_action(reason):
    """
    【状态信号】大模型判定任务无法推进（如找不到人），主动阻断幻觉
    """
    msg = reason if reason else "VLM 判定当前任务遭遇死胡同，无法继续。"
    print(f"🛑 任务判定失败/终止: {msg}")
    return f"执行失败: 任务强行终止。原因: {msg}"

# ==========================================
# 4. 命令行路由枢纽 (OpenClaw 的 API 接口)
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenClaw 智能体手机控制端")
    
    # 动作指令库扩充 (共 12 个原子动作 + 2 个状态信号)
    parser.add_argument("--action", required=True, 
                        choices=[
                            "get_info",       # 获取分辨率和状态
                            "read_xml",       # 极速读取文字
                            "vision_find",    # 调用大模型定位目标
                            "click_text",     # 传统文字点击
                            "click_xy",       # 坐标点击
                            "input",          # 输入文字
                            "swipe",          # 滑动
                            "open_app",       # 打开应用
                            "press_key",      # 按压系统按键：home (桌面), back (返回)
                            "smart_open_app", # 大模型专用：直接通过应用中文名打开 App
                            "wait",           # 主动等待
                            "analyze_plan",   # 大脑：综合感知与规划
                            "task_complete",  # 【状态】任务成功
                            "task_failed"     # 【状态】任务失败
                        ], 
                        help="执行的原子动作")
    parser.add_argument("--param", required=False, default="", help="动作参数")
    
    args = parser.parse_args()
    
    # 初始化设备并获取分辨率
    device, s_width, s_height = init_device()
    if device is None:
        print(json.dumps({"status": "error", "message": "设备连接失败或未授权"}, ensure_ascii=False))
        exit(1)

    # 动作路由执行
    result_msg = ""
    if args.action == "get_info":
        result_msg = get_device_info(device, s_width, s_height)
        
    elif args.action == "read_xml":
        result_msg = read_screen_xml(device)
        
    elif args.action == "vision_find":
        if not args.param: result_msg = "失败: vision_find 缺少 --param (目标描述)"
        else: result_msg = vision_find_element(device, args.param, s_width, s_height)
        
    elif args.action == "click_xy":
        if not args.param: result_msg = "失败: click_xy 缺少 --param (例如 500,1200)"
        else: result_msg = click_by_xy(device, args.param)
        
    elif args.action == "click_text":
        if not args.param: result_msg = "失败: click_text 缺少 --param"
        else: result_msg = click_by_text(device, args.param)
        
    elif args.action == "input":
        result_msg = input_text(device, args.param)
        
    elif args.action == "swipe":
        result_msg = swipe_screen(device, args.param)
        
    elif args.action == "open_app":
        result_msg = open_app(device, args.param)
        
    elif args.action == "press_key":
        result_msg = press_key(device, args.param)
        
    elif args.action == "smart_open_app":
        result_msg = smart_open_app(device, args.param)
        
    elif args.action == "wait":
        if not args.param: result_msg = wait_action("5") # 默认等5秒
        else: result_msg = wait_action(args.param)
        
    elif args.action == "task_complete":
        result_msg = task_complete_action(args.param)
        
    elif args.action == "task_failed":
        result_msg = task_failed_action(args.param)
        
    elif args.action == "analyze_plan":
        if not args.param: 
            result_msg = json.dumps({"status": "failed", "result": "缺少用户的总目标参数"}, ensure_ascii=False)
        else: 
            # 直接把 JSON 字符串原样返回，不走下面的普通格式化
            plan_result = vlm_analyze_and_plan(device, s_width, s_height, args.param)
            print(plan_result)
            exit(0)

    # 统一格式化输出给 OpenClaw
    output = {
        "status": "success" if ("成功" in result_msg or "状态" in result_msg or "文本" in result_msg) else "failed",
        "result": result_msg
    }
    print(json.dumps(output, ensure_ascii=False))