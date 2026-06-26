#!/usr/bin/env python3
"""
Conversation Archive - Session Archiver
归档 OpenClaw session 对话，生成结构化 JSON 存档
"""

import json
import os
import sys
import re
from datetime import datetime, timedelta

ARCHIVE_DIR = os.path.expanduser("~/.openclaw/workspace/conversation_archive")
INDEX_FILE = os.path.join(ARCHIVE_DIR, "index.json")

def load_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE) as f:
            return json.load(f)
    return []

def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def extract_topics(messages):
    """从对话中提取主题关键词"""
    topics = set()
    keywords = ["升级", "记忆", "skill", "安装", "删除", "配置", "飞书", "视频", "音频", "session", "清理", "搜索"]
    
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    content = c.get("text", "")
                    break
        if isinstance(content, str):
            for kw in keywords:
                if kw.lower() in content.lower():
                    topics.add(kw)
    return list(topics)

def extract_decisions(messages):
    """提取决策类语句"""
    decisions = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    content = c.get("text", "")
                    break
        if isinstance(content, str):
            if any(kw in content for kw in ["好的", "同意", "开始", "就这个", "没问题"]):
                if len(content) < 200:
                    decisions.append({"text": content[:100], "source": "user" if msg.get("role") == "user" else "assistant"})
    return decisions[:5]  # 最多5条

def extract_feedback(messages):
    """提取反馈/纠正类语句"""
    feedback = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    content = c.get("text", "")
                    break
        if isinstance(content, str):
            if any(kw in content for kw in ["不对", "错了", "不是这样", "不要", "应该", "改成"]):
                feedback.append({"user": content[:150], "from": "user" if msg.get("role") == "user" else "assistant"})
    return feedback[:5]

def generate_summary(messages):
    """生成对话摘要"""
    user_msgs = []
    assistant_msgs = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    content = c.get("text", "")
                    break
        if isinstance(content, str) and content.strip():
            if msg.get("role") == "user":
                user_msgs.append(content)
            else:
                assistant_msgs.append(content)
    
    # 简单摘要：取前3条用户消息的核心词
    summary_parts = []
    for msg in user_msgs[:3]:
        # 取前50字
        excerpt = msg[:50].strip()
        if excerpt:
            summary_parts.append(excerpt)
    
    return " | ".join(summary_parts) if summary_parts else "常规对话"

def archive_session(session_id, messages, channel="webchat", date=None):
    """归档一个 session"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    year_month = date[:7]  # YYYY-MM
    
    # 确保目录存在
    session_dir = os.path.join(ARCHIVE_DIR, "sessions", year_month)
    os.makedirs(session_dir, exist_ok=True)
    
    archive_file = os.path.join(session_dir, f"{session_id}.json")
    
    # 提取结构化信息
    topics = extract_topics(messages)
    decisions = extract_decisions(messages)
    feedback = extract_feedback(messages)
    summary = generate_summary(messages)
    
    archive = {
        "sessionId": session_id,
        "date": date,
        "channel": channel,
        "topics": topics,
        "decisions": decisions,
        "feedback": feedback,
        "summary": summary,
        "messageCount": len(messages),
        "archivedAt": datetime.now().isoformat()
    }
    
    # 写入归档
    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump(archive, f, ensure_ascii=False, indent=2)
    
    # 更新索引
    index = load_index()
    index.insert(0, {
        "sessionId": session_id,
        "date": date,
        "topics": topics,
        "summary": summary,
        "file": f"sessions/{year_month}/{session_id}.json"
    })
    
    # 保留最近1000条索引
    if len(index) > 1000:
        index = index[:1000]
    
    save_index(index)
    
    print(f"Archived: {session_id}")
    print(f"  Date: {date}")
    print(f"  Topics: {topics}")
    print(f"  Decisions: {len(decisions)}")
    print(f"  Feedback: {len(feedback)}")
    print(f"  Summary: {summary[:80]}...")
    
    return archive

if __name__ == "__main__":
    # 测试：打印当前索引状态
    index = load_index()
    print(f"Current archive index: {len(index)} entries")
    print(f"Archive directory: {ARCHIVE_DIR}")
