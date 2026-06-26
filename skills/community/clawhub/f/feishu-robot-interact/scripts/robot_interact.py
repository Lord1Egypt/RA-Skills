#!/usr/bin/env python3
"""
飞书群机器人通信处理脚本
功能：解析@消息，提取任务，与开发者交互，执行任务并回复
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ============== 配置项 ==============
ROBOT_ID = os.getenv("FEISHU_ROBOT_ID", "")
ROBOT_NAME = os.getenv("FEISHU_ROBOT_NAME", "机器人A")
DEVELOPER_ID = os.getenv("FEISHU_DEVELOPER_ID", "")
MEMORY_FILE = Path(os.getenv("MEMORY_PATH", "~/.openclaw/workspace/memory/robot_confirm.json"))

# ============== 记忆管理 ==============
def load_memory():
    """加载开发者偏好记忆"""
    path = MEMORY_FILE.expanduser()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(data):
    """保存开发者偏好记忆"""
    path = MEMORY_FILE.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_task记忆(task_type):
    """获取任务类型的记忆"""
    memory = load_memory()
    return memory.get(task_type)

def save_task记忆(task_type, status, ask_again=False):
    """保存任务执行后的记忆"""
    memory = load_memory()
    memory[task_type] = {
        "status": status,  # "confirmed" or "rejected"
        "confirmed_at": datetime.now().isoformat(),
        "ask_again": ask_again
    }
    save_memory(memory)

# ============== 消息解析 ==============
def parse_mentioned_message(message_data):
    """
    解析飞书消息事件，提取@信息
    
    Args:
        message_data: 飞书消息事件 payload
        
    Returns:
        dict: {
            "mentioned_robots": ["open_id_1", ...],
            "task_text": "纯文本任务内容",
            "from_robot": "发送消息的机器人open_id"
        }
    """
    # 消息结构示例：
    # {
    #   "msg_type": "text",
    #   "event": {
    #     "message": {
    #       "chat_id": "oc_xxx",
    #       "message_id": "om_xxx",
    #       "sender": {"sender_id": {"open_id": "ou_xxx"}},
    #       "elements": [...]
    #     }
    #   }
    # }
    
    event = message_data.get("event", {})
    message = event.get("message", {})
    elements = message.get("elements", [])
    
    mentioned_robots = []
    task_text_parts = []
    from_robot = None
    
    for elem in elements:
        # 解析 @ 机器人的元素
        if elem.get("type") == "at":
            mentioned_robot_id = elem.get("value", {}).get("open_id")
            if mentioned_robot_id:
                mentioned_robots.append(mentioned_robot_id)
        
        # 解析文本内容
        elif elem.get("type") == "text":
            text = elem.get("text", "")
            task_text_parts.append(text)
    
    # 判断发送者是否为机器人
    sender_id = message.get("sender", {}).get("sender_id", {})
    sender_open_id = sender_id.get("open_id", "")
    
    # 这里需要根据实际飞书消息判断发送者是否为机器人
    # 可以通过 sender_id 类型判断，或者维护一个机器人ID列表
    
    # 获取消息文本（去掉 @ 机器人部分）
    task_text = "".join(task_text_parts).strip()
    
    return {
        "mentioned_robots": mentioned_robots,
        "task_text": task_text,
        "from_robot": sender_open_id,
        "chat_id": message.get("chat_id"),
        "message_id": message.get("message_id")
    }

def extract_task_type(task_text):
    """
    从任务文本中提取任务类型
    用于记忆匹配
    """
    # 简单实现：取任务文本的前N个字符作为类型标识
    # 实际使用可根据业务需求自定义
    return task_text[:50] if task_text else "unknown"

# ============== 开发者确认流程 ==============
def need_confirmation(task_type):
    """判断是否需要开发者确认"""
    task记忆 = get_task记忆(task_type)
    
    if task记忆 is None:
        # 从未处理过，需要确认
        return True
    
    if task记忆.get("ask_again", True):
        # 开发者说下次还要确认
        return True
    
    return False

def build_confirm_message(task_content):
    """构建确认请求消息"""
    return f"""🤖 收到新任务请求
📋 任务内容：{task_content}

请回复：
- "确认" 执行任务
- "确认+不再询问" 执行任务并记住偏好
- "拒绝" 不执行
"""

def build_result_message(task_content, success, result_detail=""):
    """构建结果回复消息"""
    if success:
        return f"""✅ 任务已完成
📋 任务内容：{task_content}
🔧 执行结果：{result_detail}"""
    else:
        return f"""❌ 任务执行失败
📋 任务内容：{task_content}
📝 原因：{result_detail}"""

# ============== 主处理逻辑 ==============
def process_message(message_data):
    """
    处理接收到的消息
    
    Args:
        message_data: 飞书消息事件 payload
        
    Returns:
        dict: {
            "need_confirm": bool,  # 是否需要开发者确认
            "confirm_message": str, # 确认请求消息
            "execute": bool,        # 是否直接执行
            "response_message": str # 回复消息
        }
    """
    # 1. 解析消息
    parsed = parse_mentioned_message(message_data)
    
    # 2. 检查是否@了本机器人
    if ROBOT_ID not in parsed["mentioned_robots"]:
        return {"handled": False, "reason": "not_mentioned"}
    
    # 3. 检查发送者是否为机器人（可选，根据需求）
    # from_robot = parsed["from_robot"]
    # if not from_robot:  # 人类发送的消息，不处理
    #     return {"handled": False, "reason": "from_human"}
    
    task_content = parsed["task_text"]
    task_type = extract_task_type(task_content)
    
    # 4. 判断是否需要确认
    if need_confirmation(task_type):
        return {
            "handled": True,
            "need_confirm": True,
            "confirm_message": build_confirm_message(task_content),
            "task_content": task_content,
            "task_type": task_type
        }
    else:
        # 5. 直接执行（已获信任）
        return {
            "handled": True,
            "need_confirm": False,
            "execute": True,
            "task_content": task_content,
            "task_type": task_type
        }

def handle_developer_response(task_type, response_text, task_content):
    """
    处理开发者的回复
    
    Args:
        task_type: 任务类型
        response_text: 开发者回复内容
        task_content: 原始任务内容
        
    Returns:
        dict: {
            "action": "execute" | "reject" | "invalid",
            "remember": bool,  # 是否记住偏好
            "response_message": str  # 群回复消息
        }
    """
    response = response_text.strip()
    
    if response in ["确认", "同意", "ok", "yes", "执行"]:
        # 确认执行
        return {
            "action": "execute",
            "remember": False,
            "save_memory": (task_type, "confirmed", False)
        }
    elif response in ["确认+不再询问", "确认不再问", "记住", "下次不用问"]:
        # 确认执行并记住
        return {
            "action": "execute",
            "remember": True,
            "save_memory": (task_type, "confirmed", True)
        }
    elif response in ["拒绝", "取消", "no", "不执行"]:
        # 拒绝执行
        return {
            "action": "reject",
            "remember": False,
            "save_memory": (task_type, "rejected", False)
        }
    else:
        # 无效回复
        return {"action": "invalid"}

# ============== 示例用法 ==============
if __name__ == "__main__":
    # 测试用例
    test_message = {
        "msg_type": "text",
        "event": {
            "message": {
                "chat_id": "oc_xxx",
                "message_id": "om_xxx",
                "sender": {"sender_id": {"open_id": "ou_robot_b"}},
                "elements": [
                    {
                        "type": "at",
                        "value": {"open_id": ROBOT_ID or "ou_test"}
                    },
                    {
                        "type": "text",
                        "text": "请执行数据同步任务"
                    }
                ]
            }
        }
    }
    
    result = process_message(test_message)
    print(json.dumps(result, ensure_ascii=False, indent=2))