import asyncio
import json
import os
import sys
import time
from pathlib import Path

# 设置 UTF-8 编码输出
sys.stdout.reconfigure(encoding='utf-8')

# DingDing Talk - 钉钉自动发送技能

import pyautogui
pyautogui.FAILSAFE = False
import pygetwindow as gw
from PIL import Image, ImageGrab
import pyperclip


def open_dingding():
    """Step 1: Ctrl+Shift+Z 打开钉钉"""
    print("正在打开钉钉...")
    pyautogui.hotkey('ctrl', 'shift', 'z')
    time.sleep(1.0)
    
    # 等待钉钉窗口出现
    for _ in range(10):
        wins = gw.getWindowsWithTitle("钉钉")
        for w in wins:
            if w.width > 500 and w.width < 2000:
                print("钉钉窗口已打开")
                return True
        time.sleep(0.5)
    
    return False


def maximize_dingding():
    """Step 2: Win+Up 最大化钉钉窗口"""
    print("最大化钉钉窗口 (Win+Up)...")
    pyautogui.hotkey('win', 'up')
    time.sleep(0.5)
    print("钉钉窗口已最大化 (Win+Up)")
    return True


def search_contact(contact_name, press_enter=True):
    """Step 3-4: Ctrl+Shift+F 搜索联系人，可选择是否回车打开聊天"""
    print(f"搜索联系人：{contact_name}")
    
    # Ctrl+Shift+F 打开搜索
    pyautogui.hotkey('ctrl', 'shift', 'f')
    time.sleep(0.3)
    
    # 清空搜索框
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.1)
    
    # 输入联系人名称
    pyperclip.copy(contact_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # 根据参数决定是否回车打开聊天
    if press_enter:
        pyautogui.press('enter')
        time.sleep(0.5)
        print(f"已打开联系人：{contact_name}")
    else:
        print(f"已输入联系人：{contact_name}（等待后续操作）")
    
    return True, None




def search_contact_simple(contact_name):
    """搜索联系人 - 不执行 Ctrl+Shift+F，直接输入（假设搜索框已激活）"""
    print(f"  输入联系人：{contact_name}")
    
    # 清空搜索框
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.1)
    
    # 输入联系人名称
    pyperclip.copy(contact_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    print(f"  已输入联系人：{contact_name}")
    
    return True, None


def get_dingding_window():
    """获取钉钉主窗口"""
    wins = gw.getWindowsWithTitle("钉钉")
    for w in wins:
        if w.width > 500 and w.width < 2000:
            return w
    return None


def send_message_to_contact(contact_name, message):
    """给指定联系人发送消息
    
    流程：
    1. Ctrl+Shift+Z 打开钉钉
    2. Win+Up 最大化钉钉窗口
    3. Ctrl+Shift+F 打开搜索
    4. 输入联系人名称，回车打开聊天
    5. 输入消息内容，回车发送
    """
    print(f"\n=== 发送消息给 {contact_name} ===")
    print(f"消息内容：{message}")
    
    # Step 1: 打开钉钉
    print("\n--- Step 1: 打开钉钉 (Ctrl+Shift+Z) ---")
    open_dingding()
    time.sleep(0.5)
    
    # Step 2: 最大化钉钉窗口
    print("\n--- Step 2: 最大化窗口 (Win+Up) ---")
    maximize_dingding()
    time.sleep(0.5)
    
    
    # Step 3: 点击坐标激活窗口
    print("\n--- Step 3: 点击坐标 (1000, 30) ---")
    pyautogui.click(1000, 30)
    time.sleep(0.3)

    # Step 4: 输入联系人名称
    print("\n--- Step 4: 输入联系人名称 ---")
    success, err = search_contact_simple(contact_name)
    if not success:
        return False, err
    
    # Step 5: 等待搜索结果加载
    print("\n--- 等待搜索结果加载 (2 秒) ---")
    time.sleep(2.0)
    
    # Step 6: 回车打开聊天窗口
    print("\n--- Step 6: 打开聊天窗口 (Enter) ---")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # Step 7: 点击坐标 1300,1150
    print("\n--- Step 7: 点击坐标 (1300, 1150) ---")
    pyautogui.click(1300, 1150)
    time.sleep(0.3)
    
    # Step 8: 复制并粘贴消息
    print("\n--- Step 5: 复制并粘贴消息 ---")
    pyperclip.copy(message)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # Step 9: 回车发送
    print("\n--- Step 9: 发送消息 (Enter) ---")
    pyautogui.press('enter')
    time.sleep(0.3)
    
    # Step 10: Win+Down 还原窗口
    print("\n--- Step 10: 还原窗口 (Win+Down) ---")
    pyautogui.hotkey('win', 'down')
    time.sleep(0.3)
    
    print("\n=== 发送完成! ===")
    return True, None




def send_message_skip_steps(contact_name, message, skip_first=True, skip_last=True):
    """给指定联系人发送消息（跳过部分步骤）
    
    参数:
        contact_name: 联系人姓名
        message: 消息内容
        skip_first: 是否跳过 Step 1-2（打开钉钉和最大化窗口）
        skip_last: 是否跳过 Step 10（还原窗口）
    
    流程:
        - skip_first=True: 从 Step 3 开始执行
        - skip_last=True: 执行到 Step 9 结束
        - skip_last=False: 执行 Step 10（最后一个人需要还原窗口）
    """
    print(f"\n=== 发送消息给 {contact_name} ===")
    print(f"消息内容：{message}")
    print(f"跳过 Step 1-2: {skip_first}, 跳过 Step 10: {skip_last}")
    
    # Step 1-2: 根据参数决定是否跳过
    if not skip_first:
        print("\n--- Step 1: 打开钉钉 (Ctrl+Shift+Z) ---")
        open_dingding()
        time.sleep(0.5)
        
        print("\n--- Step 2: 最大化窗口 (Win+Up) ---")
        maximize_dingding()
        time.sleep(0.5)
    
    # Step 3: 点击坐标激活窗口
    print("\n--- Step 3: 点击坐标 (1000, 30) ---")
    pyautogui.click(1000, 30)
    time.sleep(0.3)

    # Step 4: 输入联系人名称
    print("\n--- Step 4: 输入联系人名称 ---")
    success, err = search_contact_simple(contact_name)
    if not success:
        return False, err
    
    # Step 5: 等待搜索结果加载
    print("\n--- 等待搜索结果加载 (2 秒) ---")
    time.sleep(2.0)
    
    # Step 6: 回车打开聊天窗口
    print("\n--- Step 6: 打开聊天窗口 (Enter) ---")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # Step 7: 点击坐标激活输入框
    print("\n--- Step 7: 点击坐标 (1300, 1150) ---")
    pyautogui.click(1300, 1150)
    time.sleep(0.3)
    
    # Step 8: 复制并粘贴消息
    print("\n--- Step 8: 复制并粘贴消息 ---")
    pyperclip.copy(message)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # Step 9: 回车发送
    print("\n--- Step 9: 发送消息 (Enter) ---")
    pyautogui.press('enter')
    time.sleep(0.3)
    
    # Step 10: 根据参数决定是否还原窗口
    if not skip_last:
        print("\n--- Step 10: 还原窗口 (Win+Down) ---")
        pyautogui.hotkey('win', 'down')
        time.sleep(0.3)
    
    print("\n=== 发送完成! ===")
    return True, None


def send_message_to_current(message):
    """给当前聊天窗口发送消息"""
    print(f"\n=== 发送消息到当前窗口 ===")
    print(f"消息内容：{message}")
    
    # 复制并粘贴消息
    pyperclip.copy(message)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 回车发送
    pyautogui.press('enter')
    time.sleep(0.3)
    
    print("\n=== 发送完成! ===")
    return True, None


def get_dingding_status():
    """获取钉钉状态"""
    win = get_dingding_window()
    
    if not win:
        return {"status": "not_running", "message": "钉钉未运行"}
    
    return {
        "status": "running",
        "title": win.title,
        "position": {"x": win.left, "y": win.top},
        "size": {"width": win.width, "height": win.height}
    }


# MCP 工具定义
TOOLS = [
    {
        "name": "dingding_get_status",
        "description": "获取钉钉状态",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "dingding_send_message",
        "description": "给指定联系人发送消息（每次只发送给一个人，多人需多次调用）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "contact": {"type": "string", "description": "联系人姓名"},
                "message": {"type": "string", "description": "消息内容"}
            },
            "required": ["contact", "message"]
        }
    },
    {
        "name": "dingding_send_batch",
        "description": "批量发送消息给多人（每次调用只处理一个人，返回待发送列表）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "contacts": {"type": "array", "items": {"type": "string"}, "description": "联系人姓名列表"},
                "message": {"type": "string", "description": "消息内容"},
                "queue_file": {"type": "string", "description": "队列文件路径（可选，默认使用临时文件）"}
            },
            "required": ["contacts", "message"]
        }
    }
]


def get_queue_file(queue_file=None):
    """获取队列文件路径"""
    if queue_file:
        return queue_file
    return os.path.join(os.path.dirname(__file__), "send_queue.json")


def load_queue(queue_file=None):
    """加载发送队列"""
    path = get_queue_file(queue_file)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"contacts": [], "message": "", "current_index": 0}


def save_queue(queue_data, queue_file=None):
    """保存发送队列"""
    path = get_queue_file(queue_file)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(queue_data, f, ensure_ascii=False, indent=2)


def clear_queue(queue_file=None):
    """清空发送队列"""
    path = get_queue_file(queue_file)
    if os.path.exists(path):
        os.remove(path)


async def handle_tool(name, arguments):
    """处理工具调用"""
    if name == "dingding_get_status":
        result = get_dingding_status()
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}
    
    elif name == "dingding_send_message":
        contact = arguments.get("contact")
        message = arguments.get("message")
        
        if not contact:
            return {"content": [{"type": "text", "text": "错误：需要指定联系人"}]}
        if not message:
            return {"content": [{"type": "text", "text": "错误：需要指定消息内容"}]}
        
        success, err = send_message_to_contact(contact, message)
        
        if success:
            return {"content": [{"type": "text", "text": f"[OK] 消息已发送给 {contact}\n内容：{message}"}]}
        else:
            return {"content": [{"type": "text", "text": f"[ERROR] 错误：{err}"}]}
    
    elif name == "dingding_send_batch":
        contacts = arguments.get("contacts", [])
        message = arguments.get("message")
        queue_file = arguments.get("queue_file")
        
        if not contacts:
            return {"content": [{"type": "text", "text": "错误：需要指定联系人列表"}]}
        if not message:
            return {"content": [{"type": "text", "text": "错误：需要指定消息内容"}]}
        
        # 加载或初始化队列
        queue_data = load_queue(queue_file)
        
        # 如果是新任务，初始化队列
        if queue_data.get("current_index", 0) >= len(queue_data.get("contacts", [])):
            queue_data = {
                "contacts": contacts,
                "message": message,
                "current_index": 0
            }
        
        # 检查是否还有待发送的联系人
        if queue_data["current_index"] >= len(queue_data["contacts"]):
            clear_queue(queue_file)
            return {"content": [{"type": "text", "text": "[DONE] 所有消息已发送完成"}]}
        
        # 获取当前要发送的联系人
        current_contact = queue_data["contacts"][queue_data["current_index"]]
        
        # 发送消息
        print(f"\n>>> 正在发送给 [{queue_data['current_index'] + 1}/{len(queue_data['contacts'])}]: {current_contact}")
        success, err = send_message_to_contact(current_contact, message)
        
        if success:
            # 更新索引
            queue_data["current_index"] += 1
            save_queue(queue_data, queue_file)
            
            remaining = len(queue_data["contacts"]) - queue_data["current_index"]
            if remaining > 0:
                next_contact = queue_data["contacts"][queue_data["current_index"]]
                return {"content": [{"type": "text", "text": f"[OK] 已发送给 {current_contact}\n剩余：{remaining} 人 (下一个：{next_contact})\n请再次调用此工具继续发送"}]}
            else:
                clear_queue(queue_file)
                return {"content": [{"type": "text", "text": f"[OK] 已发送给 {current_contact}\n[DONE] 所有消息已发送完成"}]}
        else:
            return {"content": [{"type": "text", "text": f"[ERROR] 发送给 {current_contact} 失败：{err}"}]}
    
    return {"content": [{"type": "text", "text": "未知命令"}]}


async def main():
    """MCP 主循环"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line)
            
            if request.get("method") == "tools/list":
                response = {"jsonrpc": "2.0", "id": request.get("id"), "result": {"tools": TOOLS}}
                print(json.dumps(response), flush=True)
            
            elif request.get("method") == "tools/call":
                tool_name = request.get("name")
                tool_args = request.get("arguments", {})
                result = await handle_tool(tool_name, tool_args)
                response = {"jsonrpc": "2.0", "id": request.get("id"), "result": result}
                print(json.dumps(response), flush=True)
        
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": str(e)}), flush=True)


if __name__ == "__main__":
    import sys
    asyncio.run(main())
