#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A2A 消息通信
通过 Redis 消息队列与其他 OpenClaw 实例通信
支持 AI 理解并自动执行命令
"""
import redis
import json
import sys
import os
import subprocess
import argparse
import re
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 配置 - 从环境变量读取
# 设置方式（添加到 ~/.openclaw/.env 或系统环境变量）：
#   A2A_REDIS_HOST=Redis服务器地址
#   A2A_REDIS_PORT=6379
#   A2A_REDIS_PASSWORD=密码
#   A2A_MY_ID=你的ID
#   A2A_PEER_ID=对方ID
CONFIG = {
    "host": os.getenv("A2A_REDIS_HOST", "localhost"),
    "port": int(os.getenv("A2A_REDIS_PORT", "6379")),
    "password": os.getenv("A2A_REDIS_PASSWORD", ""),
    "my_id": os.getenv("A2A_MY_ID", "daodao"),
    "peer_id": os.getenv("A2A_PEER_ID", "bibi")
}

# 技能目录
SKILLS_DIR = r"C:\Users\zhengzhicheng\.openclaw\workspace\skills"

def get_redis():
    """创建Redis连接"""
    return redis.Redis(
        host=CONFIG["host"],
        port=CONFIG["port"],
        password=CONFIG["password"],
        decode_responses=True
    )

def send_message(target_id: str, content: str) -> str:
    """发送消息给另一个Agent（放入消息队列）"""
    r = get_redis()
    queue_key = f"msgs_{target_id}"
    
    message = {
        "from": CONFIG["my_id"],
        "content": content
    }
    
    # 使用 LPUSH 放入队列头部
    r.lpush(queue_key, json.dumps(message, ensure_ascii=False))
    
    # 设置过期时间（7天）
    r.expire(queue_key, 7 * 24 * 3600)
    
    return f"[OK] 消息已发送给 {target_id}: {content}"

def receive_messages() -> list:
    """接收消息（从消息队列拉取）"""
    r = get_redis()
    queue_key = f"msgs_{CONFIG['my_id']}"
    messages = []
    
    # 使用 RPOP 从队列尾部获取（先进先出）
    while True:
        msg = r.rpop(queue_key)
        if not msg:
            break
        try:
            data = json.loads(msg)
            messages.append(data)
        except:
            pass
    
    return messages

def peek_messages() -> list:
    """查看消息（不删除）"""
    r = get_redis()
    queue_key = f"msgs_{CONFIG['my_id']}"
    
    # 查看所有消息但不删除
    messages = r.lrange(queue_key, 0, -1)
    
    result = []
    for msg in messages:
        try:
            data = json.loads(msg)
            result.append(data)
        except:
            pass
    
    return result

def queue_length() -> int:
    """查看队列长度"""
    r = get_redis()
    queue_key = f"msgs_{CONFIG['my_id']}"
    return r.llen(queue_key)

def test_connection() -> bool:
    """测试Redis连接"""
    try:
        r = get_redis()
        r.ping()
        return True
    except Exception as e:
        print(f"连接失败: {e}")
        return False

# ========== AI 理解与命令执行 ==========

# 命令模式匹配规则
COMMAND_PATTERNS = {
    # 列出技能
    "list_skills": [
        r"列出?(.*?)技能",
        r"看看?(.*?)技能",
        r"有哪些?技能",
        r"show.*skill",
        r"list.*skill"
    ],
    # 查天气
    "weather": [
        r"天气",
        r"weather",
        r"查.*天"
    ],
    # 搜索
    "search": [
        r"搜索?(.*)",
        r"查一下?(.*)",
        r"search",
        r"找一下?(.*)"
    ],
    # 发送消息
    "send_msg": [
        r"告诉(\w+)\s+(.*)",
        r"发给(\w+)\s+(.*)",
        r"send.*to\s+(\w+)\s+(.*)"
    ],
    # 查看队列
    "check_queue": [
        r"队列",
        r"queue",
        r"有多少?消息"
    ]
}

def match_command(text: str) -> tuple:
    """匹配命令类型和参数"""
    text = text.strip()
    
    # 列出技能
    for pattern in COMMAND_PATTERNS["list_skills"]:
        if re.search(pattern, text, re.IGNORECASE):
            return "list_skills", None
    
    # 查天气
    for pattern in COMMAND_PATTERNS["weather"]:
        if re.search(pattern, text, re.IGNORECASE):
            return "weather", None
    
    # 搜索
    for pattern in COMMAND_PATTERNS["search"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            query = match.group(1) if match.lastindex else text
            return "search", query.strip()
    
    # 发送消息
    for pattern in COMMAND_PATTERNS["send_msg"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            target = match.group(1)
            content = match.group(2)
            return "send_msg", {"to": target, "content": content}
    
    # 查看队列
    for pattern in COMMAND_PATTERNS["check_queue"]:
        if re.search(pattern, text, re.IGNORECASE):
            return "check_queue", None
    
    return None, None

def execute_list_skills() -> str:
    """执行列出技能"""
    try:
        skills = os.listdir(SKILLS_DIR)
        skill_list = "\n".join([f"- {s}" for s in skills])
        return f"我目前的技能列表：\n{skill_list}"
    except Exception as e:
        return f"获取技能列表失败: {e}"

def execute_weather() -> str:
    """执行查天气"""
    try:
        # 调用天气skill
        result = subprocess.run(
            ["python", "-c", "import urllib.request; print('请使用天气skill查询')"],
            capture_output=True, text=True, timeout=5
        )
        return "要查天气可以用：告诉 <对方ID> '北京天气怎么样'"
    except Exception as e:
        return f"天气查询: {e}"

def execute_search(query: str) -> str:
    """执行搜索"""
    return f"要搜索 '{query}' 可以用 Tavily 或 Baidu 搜索skill"

def execute_send_msg(to: str, content: str) -> str:
    """发送消息"""
    result = send_message(to, content)
    return f"已发送消息给 {to}: {content}"

def execute_check_queue() -> str:
    """查看队列"""
    length = queue_length()
    return f"当前队列有 {length} 条消息"

def process_message_with_ai(text: str) -> str:
    """AI理解并处理消息"""
    # 先匹配命令
    cmd_type, cmd_arg = match_command(text)
    
    if cmd_type == "list_skills":
        return execute_list_skills()
    elif cmd_type == "weather":
        return execute_weather()
    elif cmd_type == "search":
        return execute_search(cmd_arg)
    elif cmd_type == "send_msg":
        return execute_send_msg(cmd_arg["to"], cmd_arg["content"])
    elif cmd_type == "check_queue":
        return execute_check_queue()
    else:
        # 未知命令，返回帮助
        return """我理解不了这个命令，但我支持：
- 列出技能 / show skills
- 查天气 / weather  
- 搜索xxx / search xxx
- 告诉xxx xxx / send to xxx xxx
- 队列状态 / queue status"""

def auto_process() -> str:
    """自动处理队列中的消息"""
    messages = receive_messages()
    
    if not messages:
        return "没有新消息需要处理"
    
    results = []
    for msg in messages:
        sender = msg.get("from", "unknown")
        content = msg.get("content", "")
        
        print(f"处理来自 {sender} 的消息: {content}")
        
        # AI 理解并处理
        result = process_message_with_ai(content)
        
        results.append(f"来自 {sender}: {content}\n→ {result}")
        
        # 如果不是自己发的，发回结果
        if sender != CONFIG["my_id"]:
            send_message(sender, result)
    
    return "\n\n".join(results) if results else "处理完成"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A2A 消息通信")
    parser.add_argument("action", choices=["send", "poll", "peek", "queue", "test", "auto"], help="操作类型")
    parser.add_argument("--to", help="目标Agent ID")
    parser.add_argument("--content", help="消息内容")
    args = parser.parse_args()
    
    if args.action == "test":
        if test_connection():
            print("[OK] Redis连接成功！")
        else:
            print("[X] Redis连接失败")
            sys.exit(1)
    
    elif args.action == "send":
        if not args.to or not args.content:
            print("用法: python a2a.py send --to bibi --content '你好'")
            sys.exit(1)
        result = send_message(args.to, args.content)
        print(result)
    
    elif args.action == "poll":
        messages = receive_messages()
        if messages:
            for msg in messages:
                print(f"\n[收到] 来自 {msg['from']}: {msg['content']}")
        else:
            print("没有新消息")
    
    elif args.action == "peek":
        messages = peek_messages()
        count = len(messages)
        if messages:
            print(f"队列中有 {count} 条消息:")
            for msg in messages:
                print(f"  - {msg['from']}: {msg['content']}")
        else:
            print("队列为空")
    
    elif args.action == "queue":
        length = queue_length()
        print(f"队列长度: {length}")
    
    elif args.action == "auto":
        # 自动处理模式：收到消息 -> AI理解 -> 执行 -> 发回结果
        result = auto_process()
        print(result)
