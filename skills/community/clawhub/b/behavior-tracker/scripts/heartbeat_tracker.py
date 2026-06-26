#!/usr/bin/env python3
"""
轻量行为追踪器 - 供 Heartbeat 调用
- 快速检查今日是否有新对话
- 仅在有新内容时更新
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

# 配置 - 跨平台路径
OPENCLAW_DIR = Path(os.environ.get("OPENCLAW_DIR", str(Path.home() / ".openclaw")))
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", str(OPENCLAW_DIR / "workspace")))
MEMORY_DIR = WORKSPACE / "memory"
BEHAVIOR_FILE = MEMORY_DIR / "behavior-patterns.json"
LAST_CHECK_FILE = MEMORY_DIR / "behavior-last-check.json"

# 关键词库 (轻量版)
KEYWORDS = {
    "topics": ["AI Agent", "Python", "C语言", "MiroFish", "OASIS", "N8n", "Moltbook", "EvoMap", "OpenClaw", "Tool", "Memory", "Decorator", "LangChain"],
    "projects": ["N8n", "Moltbook", "EvoMap", "The Machine", "Hostinger", "rapidwebwork", "OpenClaw"]
}

def load_json(path):
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return None

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_today_memory():
    """获取今日记忆"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = MEMORY_DIR / f"{today}.md"
    
    if not memory_file.exists():
        return None
    
    with open(memory_file, 'r') as f:
        return f.read()

def extract_keywords(content):
    """提取关键词"""
    content_lower = content.lower()
    found = {"topics": [], "projects": []}
    
    for kw in KEYWORDS["topics"]:
        if kw.lower() in content_lower:
            found["topics"].append(kw)
    
    for kw in KEYWORDS["projects"]:
        if kw.lower() in content_lower:
            found["projects"].append(kw)
    
    return found

def load_behavior_data():
    """加载行为数据"""
    data = load_json(BEHAVIOR_FILE)
    if data is None:
        return {
            "topics": {}, "projects": {}, "skills": {},
            "active_hours": {}, "total_conversations": 0
        }
    return data

def save_behavior_data(data):
    """保存行为数据"""
    save_json(BEHAVIOR_FILE, data)

def quick_track():
    """轻量追踪 - 每日首次 heartbeat 时调用"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 检查今日是否已处理
    last_check = load_json(LAST_CHECK_FILE)
    if last_check and last_check.get("date") == today:
        # 今日已处理，检查是否有新内容
        memory = get_today_memory()
        if not memory:
            return False
        
        # 简单比较 - 如果内存文件大小没变，可能没新内容
        if last_check.get("memory_size") == len(memory):
            return False
        
        # 有新内容，更新
        last_check["memory_size"] = len(memory)
    else:
        # 首次今日检查
        memory = get_today_memory()
        if not memory:
            return False
        
        last_check = {"date": today, "memory_size": len(memory)}
    
    # 提取关键词
    found = extract_keywords(memory)
    if not found["topics"] and not found["projects"]:
        save_json(LAST_CHECK_FILE, last_check)
        return False
    
    # 更新行为数据
    data = load_behavior_data()
    
    for topic in found["topics"]:
        data["topics"][topic] = data["topics"].get(topic, 0) + 1
    
    for project in found["projects"]:
        data["projects"][project] = data["projects"].get(project, 0) + 1
    
    data["total_conversations"] = data.get("total_conversations", 0) + 1
    save_behavior_data(data)
    save_json(LAST_CHECK_FILE, last_check)
    
    print(f"✅ 行为追踪更新: {found['topics'][:3]}, {found['projects'][:2]}")
    return True

def main():
    """主函数"""
    result = quick_track()
    if not result:
        print(f"⏭️ 今日无需更新 (或无新内容)")

if __name__ == "__main__":
    main()
