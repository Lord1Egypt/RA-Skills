#!/usr/bin/env python3
"""
Behavior Persona - Phase 1: Data Collector

从 OpenClaw 会话记录中提取用户行为数据。
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 配置
SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
DATA_DIR = Path.home() / ".openclaw" / "skills" / "behavior-persona" / "data"
OUTPUT_FILE = DATA_DIR / "collected_data.json"

# 事件检测规则
EVENT_PATTERNS = {
    "task_created": [
        r"帮我[做创建个]",
        r"做个[\w]+",
        r"写个[\w]+",
        r"创建一个",
        r"帮我实现",
        r"帮我写",
        r"帮我创建",
    ],
    "task_completed": [
        r"完成了",
        r"搞定了",
        r"好了",
        r"已经[做好完成]",
        r"Perfect",
        r"Perfect!",
        r"👍",
    ],
    "task_abandoned": [
        r"算了",
        r"算了不做了",
        r"先这样",
        r"先不做",
        r"不需要了",
        r"不用了",
    ],
    "feedback_given": [
        r"不对",
        r"错了",
        r"不是这样",
        r"重新来",
        r"重做",
        r"这不是我要的",
        r"需要修改",
    ],
}

QUESTION_PATTERNS = [
    r"\?$",
    r"吗[？?]",
    r"怎么",
    r"为什么",
    r"什么[\?]",
    r"如何",
    r"能否",
    r"可以[\?]",
    r"是不是",
]


def collect_sessions(days: int = 30) -> dict:
    """
    收集最近N天的会话数据。
    
    Args:
        days: 收集最近多少天的数据
        
    Returns:
        包含消息和事件的字典
    """
    all_messages = []
    all_events = []
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 读取 session 文件
    if SESSIONS_DIR.exists():
        for session_file in sorted(SESSIONS_DIR.glob("*.jsonl")):
            # 跳过 deleted 和 reset 文件
            if ".deleted" in session_file.name or ".reset" in session_file.name:
                continue
            
            # 检查文件修改时间
            mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
            if mtime < start_date:
                continue
            
            messages = extract_messages(str(session_file), days)
            all_messages.extend(messages)
    
    # 读取 memory 文件
    for i in range(days):
        date = end_date - timedelta(days=i)
        memory_file = MEMORY_DIR / f"{date.strftime('%Y-%m-%d')}.md"
        if memory_file.exists():
            events = extract_memory_events(str(memory_file))
            all_events.extend(events)
    
    # 检测事件
    events = detect_events(all_messages)
    all_events.extend(events)
    
    # 去重并按时间排序
    all_messages.sort(key=lambda x: x["timestamp"], reverse=True)
    all_events.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "messages": all_messages,
        "events": all_events,
        "collected_at": datetime.now().isoformat(),
        "days": days,
    }


def extract_messages(session_file: str, days: int) -> list:
    """
    从单个session文件提取消息。
    
    Args:
        session_file: session 文件路径
        days: 只提取最近多少天的消息
        
    Returns:
        消息列表
    """
    messages = []
    session_key = Path(session_file).stem
    
    # 计算截止时间
    cutoff = datetime.now() - timedelta(days=days)
    
    try:
        with open(session_file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f):
                try:
                    entry = json.loads(line.strip())
                    
                    # 只处理 message 类型
                    if entry.get("type") != "message":
                        continue
                    
                    # 消息内容
                    content_list = entry.get("message", {}).get("content", [])
                    if not content_list:
                        continue
                    
                    # 对于用户消息，role 是 user；assistant 消息是 AI 的回复
                    role = entry.get("message", {}).get("role", "")
                    
                    if role == "user":
                        sender = "Roger"
                    elif role == "assistant":
                        sender = "Me"
                    else:
                        sender = "Unknown"
                    
                    # 组合所有 text parts
                    text_parts = []
                    channel = "unknown"
                    
                    for c in content_list:
                        if c.get("type") == "text":
                            text = c.get("text", "")
                            # 检测渠道
                            if sender == "Unknown" or channel == "unknown":
                                channel = detect_channel(text)
                            
                            # 跳过 metadata 块的标签
                            if "Sender (untrusted metadata)" in text:
                                sender = "Roger"
                            elif "Conversation info" in text:
                                sender = "Me"
                            
                            text_parts.append(text)
                    
                    text = "\n".join(text_parts)
                    if not text:
                        continue
                    
                    # 时间戳
                    ts = entry.get("timestamp") or entry.get("message", {}).get("timestamp")
                    if ts:
                        try:
                            msg_time = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                            if msg_time.replace(tzinfo=None) < cutoff:
                                continue
                        except:
                            pass
                    
                    # 截取前200字符 (存储原始消息内容，但有限制)
                    text = text[:200]
                    
                    messages.append({
                        "timestamp": ts,
                        "sender": sender,
                        "content": text,
                        "channel": channel,
                        "session_key": session_key,
                    })
                    
                except (json.JSONDecodeError, KeyError):
                    continue
                    
    except Exception as e:
        print(f"Error reading {session_file}: {e}")
    
    return messages


def extract_memory_events(memory_file: str) -> list:
    """
    从 memory 文件提取事件。
    
    Args:
        memory_file: memory 文件路径
        
    Returns:
        事件列表
    """
    events = []
    
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 简单提取时间（从文件名）
        date = Path(memory_file).stem
        timestamp = f"{date}T00:00:00"
        
        # 检测 TODO 完成
        if "- [x]" in content:
            events.append({
                "type": "task_completed",
                "timestamp": timestamp,
                "content": "从 memory 文件检测到完成的任务",
            })
            
        # 检测新任务
        if "- [ ]" in content:
            events.append({
                "type": "task_created",
                "timestamp": timestamp,
                "content": "从 memory 文件检测到新任务",
            })
            
    except Exception as e:
        print(f"Error reading {memory_file}: {e}")
    
    return events


def detect_events(messages: list) -> list:
    """
    从消息中检测事件。
    
    Args:
        messages: 消息列表
        
    Returns:
        事件列表
    """
    events = []
    
    for msg in messages:
        content = msg.get("content", "")
        sender = msg.get("sender", "")
        timestamp = msg.get("timestamp", "")
        
        # 检测任务创建
        for pattern in EVENT_PATTERNS["task_created"]:
            if re.search(pattern, content) and sender == "Roger":
                events.append({
                    "type": "task_created",
                    "timestamp": timestamp,
                    "task": content[:100],
                })
                break
        
        # 检测任务完成
        for pattern in EVENT_PATTERNS["task_completed"]:
            if re.search(pattern, content) and sender == "Roger":
                events.append({
                    "type": "task_completed",
                    "timestamp": timestamp,
                    "task": content[:100],
                })
                break
        
        # 检测任务放弃
        for pattern in EVENT_PATTERNS["task_abandoned"]:
            if re.search(pattern, content) and sender == "Roger":
                events.append({
                    "type": "task_abandoned",
                    "timestamp": timestamp,
                    "task": content[:100],
                })
                break
        
        # 检测问题
        for pattern in QUESTION_PATTERNS:
            if re.search(pattern, content) and sender == "Roger":
                events.append({
                    "type": "question_asked",
                    "timestamp": timestamp,
                    "topic": content[:100],
                })
                break
        
        # 检测反馈
        for pattern in EVENT_PATTERNS["feedback_given"]:
            if re.search(pattern, content) and sender == "Roger":
                events.append({
                    "type": "feedback_given",
                    "timestamp": timestamp,
                    "content": content[:100],
                })
                break
    
    return events


def detect_channel(text: str) -> str:
    """
    从消息元数据检测渠道。
    
    Args:
        text: 消息文本
        
    Returns:
        渠道名称
    """
    if "feishu" in text.lower():
        return "feishu"
    elif "imessage" in text.lower():
        return "imessage"
    elif "telegram" in text.lower():
        return "telegram"
    elif "discord" in text.lower():
        return "discord"
    else:
        return "unknown"


def save_collected_data(data: dict, output_file: Optional[Path] = None):
    """
    保存收集的数据。
    
    Args:
        data: 要保存的数据
        output_file: 输出文件路径
    """
    if output_file is None:
        output_file = OUTPUT_FILE
    
    # 确保目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to {output_file}")
    print(f"  - Messages: {len(data.get('messages', []))}")
    print(f"  - Events: {len(data.get('events', []))}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Behavior Persona - Data Collector")
    parser.add_argument("--days", type=int, default=30, help="Collect data for last N days")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (don't save)")
    
    args = parser.parse_args()
    
    print(f"Collecting session data for last {args.days} days...")
    
    data = collect_sessions(days=args.days)
    
    if args.dry_run:
        print("\n--- Dry run, skipping save ---")
        print(f"Messages: {len(data['messages'])}")
        print(f"Events: {len(data['events'])}")
        
        # 显示示例
        if data["messages"]:
            print("\n--- Sample messages ---")
            for msg in data["messages"][:3]:
                print(f"  [{msg['timestamp']}] {msg['sender']}: {msg['content'][:50]}...")
        
        if data["events"]:
            print("\n--- Sample events ---")
            for evt in data["events"][:5]:
                print(f"  [{evt['timestamp']}] {evt['type']}: {evt.get('task', evt.get('topic', ''))[:50]}")
    else:
        output = Path(args.output) if args.output else OUTPUT_FILE
        save_collected_data(data, output)


if __name__ == "__main__":
    main()