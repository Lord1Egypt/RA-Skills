#!/usr/bin/env python3
"""
uiautomator2 MCP Server
将 uiautomator2 的所有能力封装成 MCP Tools
供 MiniMax (或其他 MCP Client) 通过 stdio 调用

用法:
  python3 u2_mcp_server.py

MCP Protocol: JSON-RPC 2.0 over stdio
"""

import sys
import json
import uiautomator2 as u2
import time
import os
import re

# 全局设备连接
device = None
DEVICE_IP = os.environ.get("ANDROID_DEVICE", "auto")

def connect_device(ip=None):
    global device
    ip = ip or DEVICE_IP
    if ip == "auto":
        device = u2.connect()
    else:
        device = u2.connect(ip)
    return {"status": "connected", "device": device.info}

# ============ MCP Tools ============

TOOLS = []

def tool(name, description, input_schema):
    """装饰器注册 MCP Tool"""
    def decorator(func):
        TOOLS.append({
            "name": name,
            "description": description,
            "inputSchema": input_schema,
            "fn": func
        })
        return func
    return decorator

# -------- 设备连接 --------

@tool("device_connect", "连接 Android 设备（USB或无线ADB）", {
    "type": "object",
    "properties": {
        "ip": {"type": "string", "description": "设备IP:端口，如 192.168.1.100:5555，留空则自动发现"}
    },
    "required": []
})
def device_connect(ip=None):
    result = connect_device(ip)
    return json.dumps(result)

@tool("device_info", "获取已连接设备的基本信息", {
    "type": "object",
    "properties": {},
    "required": []
})
def device_info():
    return json.dumps(device.info)

# -------- 屏幕操作 --------

@tool("screenshot", "截取当前屏幕并保存到文件", {
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "保存路径，默认 /sdcard/screen.png"}
    },
    "required": []
})
def screenshot(path="/sdcard/screen.png"):
    result = device.screenshot(path)
    size = os.path.getsize(path)
    return json.dumps({"status": "ok", "path": path, "size_bytes": size})

@tool("screenshot_base64", "截取当前屏幕，返回 base64 编码的图片数据（用于AI视觉识别）", {
    "type": "object",
    "properties": {},
    "required": []
})
def screenshot_base64():
    import base64
    path = "/sdcard/screen_temp.png"
    device.screenshot(path)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return json.dumps({"status": "ok", "image_base64": b64, "format": "png"})

@tool("screen_text", "获取当前屏幕的 XML 结构化文本（可用于元素定位分析）", {
    "type": "object",
    "properties": {},
    "required": []
})
def screen_text():
    xml = device.dump_hierarchy()
    return json.dumps({"status": "ok", "xml": xml})

# -------- 点击 & 滑动 --------

@tool("click", "点击屏幕指定坐标或元素", {
    "type": "object",
    "properties": {
        "x": {"type": "number", "description": "X坐标（可选，和text二选一）"},
        "y": {"type": "number", "description": "Y坐标（可选）"},
        "text": {"type": "string", "description": "屏幕上可见的文字元素（点击匹配此文字的元素）"},
        "description": {"type": "string", "description": "元素content-desc属性"},
        "timeout": {"type": "number", "description": "等待元素出现的超时秒数，默认10"}
    },
    "required": []
})
def click(x=None, y=None, text=None, description=None, timeout=10):
    if text:
        elem = device(text=text, timeout=timeout)
        if elem.exists:
            elem.click()
            return json.dumps({"status": "ok", "action": "click", "target": f"text={text}"})
        return json.dumps({"status": "error", "reason": f"元素未找到: {text}"})
    elif description:
        elem = device(description=description, timeout=timeout)
        if elem.exists:
            elem.click()
            return json.dumps({"status": "ok", "action": "click", "target": f"description={description}"})
        return json.dumps({"status": "error", "reason": f"元素未找到: {description}"})
    elif x is not None and y is not None:
        device.click(x, y)
        return json.dumps({"status": "ok", "action": "click", "target": f"坐标({x},{y})"})
    return json.dumps({"status": "error", "reason": "缺少定位参数: x/y 或 text 或 description"})

@tool("long_press", "长按屏幕指定坐标或元素", {
    "type": "object",
    "properties": {
        "x": {"type": "number"},
        "y": {"type": "number"},
        "text": {"type": "string"},
        "duration": {"type": "number", "description": "长按时长（秒），默认0.5"}
    },
    "required": []
})
def long_press(x=None, y=None, text=None, duration=0.5):
    if text:
        device(text=text).long_click(duration=duration)
        return json.dumps({"status": "ok", "action": "long_press", "target": f"text={text}"})
    elif x is not None and y is not None:
        device.long_click(x, y, duration)
        return json.dumps({"status": "ok", "action": "long_press", "target": f"坐标({x},{y})"})
    return json.dumps({"status": "error", "reason": "缺少定位参数"})

@tool("swipe", "滑动屏幕", {
    "type": "object",
    "properties": {
        "direction": {"type": "string", "enum": ["up", "down", "left", "right"], "description": "滑动方向"},
        "scale": {"type": "number", "description": "滑动距离比例，默认0.9"}
    },
    "required": ["direction"]
})
def swipe(direction, scale=0.9):
    device.swipe_ext(direction, scale=scale)
    return json.dumps({"status": "ok", "action": "swipe", "direction": direction})

@tool("swipe_coords", "从起点坐标滑动到终点坐标", {
    "type": "object",
    "properties": {
        "sx": {"type": "number", "description": "起始X"},
        "sy": {"type": "number", "description": "起始Y"},
        "ex": {"type": "number", "description": "终点X"},
        "ey": {"type": "number", "description": "终点Y"},
        "duration": {"type": "number", "description": "滑动持续秒数，默认0.5"}
    },
    "required": ["sx", "sy", "ex", "ey"]
})
def swipe_coords(sx, sy, ex, ey, duration=0.5):
    device.swipe(sx, sy, ex, ey, duration)
    return json.dumps({"status": "ok", "action": "swipe_coords", "from": (sx, sy), "to": (ex, ey)})

# -------- 输入文字 --------

@tool("input_text", "在输入框中输入文字", {
    "type": "object",
    "properties": {
        "text": {"type": "string", "description": "要输入的文字"},
        "clear": {"type": "boolean", "description": "是否先清空输入框，默认False"}
    },
    "required": ["text"]
})
def input_text(text, clear=False):
    if clear:
        device.set_fastinput_ime(True)
        device.clear_text()
        time.sleep(0.3)
    device.set_fastinput_ime(True)
    device.send_keys(text)
    device.set_fastinput_ime(False)
    return json.dumps({"status": "ok", "action": "input", "text": text})

@tool("press_key", "按手机按键", {
    "type": "object",
    "properties": {
        "key": {"type": "string", "enum": ["home", "back", "enter", "search", "recent", "volume_up", "volume_down", "power"], "description": "按键名称"}
    },
    "required": ["key"]
})
def press_key(key):
    device.press(key)
    return json.dumps({"status": "ok", "action": "press", "key": key})

# -------- APP 管理 --------

@tool("app_start", "启动指定APP", {
    "type": "object",
    "properties": {
        "package": {"type": "string", "description": "APP包名，如 com.taobao.taobao"},
        "stop_first": {"type": "boolean", "description": "是否先停止APP再启动，默认True"}
    },
    "required": ["package"]
})
def app_start(package, stop_first=True):
    device.app_start(package, stop=stop_first)
    time.sleep(3)
    return json.dumps({"status": "ok", "action": "app_start", "package": package})

@tool("app_stop", "停止指定APP（强制退出）", {
    "type": "object",
    "properties": {
        "package": {"type": "string"}
    },
    "required": ["package"]
})
def app_stop(package):
    device.app_stop(package)
    return json.dumps({"status": "ok", "action": "app_stop", "package": package})

@tool("app_current", "获取当前前台运行的APP包名和Activity", {
    "type": "object",
    "properties": {},
    "required": []
})
def app_current():
    info = device.app_current()
    return json.dumps({"status": "ok", "app": info})

# -------- 元素定位 & 读取 --------

@tool("find_element", "查找屏幕上匹配的元素，返回其坐标和文字", {
    "type": "object",
    "properties": {
        "text": {"type": "string", "description": "按文字精确匹配"},
        "text_contains": {"type": "string", "description": "按文字模糊匹配"},
        "description": {"type": "string", "description": "按content-desc匹配"},
        "class_name": {"type": "string", "description": "按className匹配"},
        "xpath": {"type": "string", "description": "XPath定位，如 //android.widget.TextView[@text='搜索']"}
    },
    "required": []
})
def find_element(text=None, text_contains=None, description=None, class_name=None, xpath=None):
    try:
        if text:
            elem = device(text=text)
        elif text_contains:
            elem = device(textContains=text_contains)
        elif description:
            elem = device(description=description)
        elif class_name:
            elem = device(className=class_name)
        elif xpath:
            elem = device.xpath(xpath)
        else:
            return json.dumps({"status": "error", "reason": "缺少定位参数"})
        
        if elem.exists:
            info = elem.info
            return json.dumps({
                "status": "ok",
                "found": True,
                "text": info.get("text"),
                "bounds": info.get("bounds"),
                "enabled": info.get("enabled"),
                "clickable": info.get("clickable")
            })
        return json.dumps({"status": "ok", "found": False})
    except Exception as e:
        return json.dumps({"status": "error", "reason": str(e)})

@tool("get_text", "获取指定元素的文字内容", {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "xpath": {"type": "string"}
    },
    "required": []
})
def get_text(text=None, xpath=None):
    try:
        if text:
            elem = device(text=text)
        elif xpath:
            elem = device.xpath(xpath)
        else:
            return json.dumps({"status": "error", "reason": "缺少参数"})
        if elem.exists:
            return json.dumps({"status": "ok", "text": elem.get_text()})
        return json.dumps({"status": "ok", "found": False})
    except Exception as e:
        return json.dumps({"status": "error", "reason": str(e)})

# -------- 等待 --------

@tool("wait_exists", "等待指定元素出现", {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "timeout": {"type": "number", "description": "超时秒数，默认15"}
    },
    "required": ["text"]
})
def wait_exists(text, timeout=15):
    elem = device(text=text, timeout=timeout)
    if elem.exists:
        return json.dumps({"status": "ok", "found": True})
    return json.dumps({"status": "ok", "found": False, "timeout": timeout})

@tool("sleep", "等待指定秒数", {
    "type": "object",
    "properties": {
        "seconds": {"type": "number", "description": "等待秒数"}
    },
    "required": ["seconds"]
})
def sleep(seconds):
    time.sleep(seconds)
    return json.dumps({"status": "ok", "slept": seconds})

# -------- 搜索 & 比价专用 --------

APP_PACKAGES = {
    "taobao":    "com.taobao.taobao",
    "jd":        "com.jingdong.app.mall",
    "pinduoduo": "com.xunmeng.pinduoduo",
    "xiaohongshu": "com.xingin.xhs",
    "douyin":    "com.ss.android.ugc.aweme",
    "wechat":    "com.tencent.mm",
    "meituan":   "com.sankuai.meituan",
    "weibo":     "com.sina.weibo",
    "bilibili":  "tv.danmaku.bili",
}

@tool("open_app", "打开指定APP（支持名称或包名）", {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": f"APP名称，支持: {', '.join(APP_PACKAGES.keys())}"}
    },
    "required": ["name"]
})
def open_app(name):
    package = APP_PACKAGES.get(name, name)
    device.app_stop(package)
    device.app_start(package)
    time.sleep(3)
    return json.dumps({"status": "ok", "app": name, "package": package})

@tool("search_product", "在已打开的购物APP中搜索商品", {
    "type": "object",
    "properties": {
        "keyword": {"type": "string", "description": "搜索关键词"},
        "platform": {"type": "string", "description": "平台名称（可选，自动检测当前APP）"}
    },
    "required": ["keyword"]
})
def search_product(keyword, platform=None):
    pkg = device.info.get("currentPackageName", "") if device.info else ""
    
    # 找搜索框并点击
    searched = False
    for _ in range(3):
        if device(text="搜索").exists:
            device(text="搜索").click()
            time.sleep(1)
            searched = True
            break
        time.sleep(1)
    
    if not searched:
        return json.dumps({"status": "error", "reason": "未找到搜索框"})
    
    # 输入文字
    device.set_fastinput_ime(True)
    device.send_keys(keyword)
    device.set_fastinput_ime(False)
    time.sleep(0.5)
    
    # 触发搜索
    if device(text="搜索", className="android.widget.Button").exists:
        device(text="搜索", className="android.widget.Button").click()
    else:
        device.press("enter")
    
    time.sleep(3)
    return json.dumps({"status": "ok", "action": "search", "keyword": keyword})

@tool("read_price", "读取屏幕上商品的价格（自动识别¥符号后的数字）", {
    "type": "object",
    "properties": {},
    "required": []
})
def read_price():
    try:
        xml = device.dump_hierarchy()
        # 匹配 ¥数字 或 ¥ 数字 格式
        matches = re.findall(r'¥([\d.]+)', xml)
        prices = [float(m) for m in matches]
        return json.dumps({
            "status": "ok",
            "prices": prices[:10],  # 最多返回10个
            "lowest": min(prices) if prices else None
        })
    except Exception as e:
        return json.dumps({"status": "error", "reason": str(e)})

# ============ MCP Protocol Handler ============

def handle_request(req):
    """处理 MCP JSON-RPC 请求"""
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    # MCP 协议：list_tools
    if method == "tools/list":
        tool_list = []
        for t in TOOLS:
            tool_list.append({
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t["inputSchema"]
            })
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tool_list}}

    # MCP 协议：call_tool
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        for t in TOOLS:
            if t["name"] == tool_name:
                try:
                    result = t["fn"](**arguments)
                    return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": result}]}}
                except Exception as e:
                    return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"status": "error", "reason": str(e)})}]}}

        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}}

    # 初始化
    elif method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "uiautomator2-mcp", "version": "1.0.0"}
        }}

    elif method == "notifications/initialized":
        return None  # 握手确认，无需回复

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}

def main():
    # 自动连接设备
    try:
        connect_device()
        print("# uiautomator2 MCP Server 已启动，已自动连接设备", file=sys.stderr)
    except Exception as e:
        print(f"# 警告: 设备未连接: {e}，将在首次调用时连接", file=sys.stderr)

    # 读取 stdin，逐行处理 JSON-RPC
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            if resp is not None:
                print(json.dumps(resp), flush=True)
        except json.JSONDecodeError:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}}), flush=True)

if __name__ == "__main__":
    main()
