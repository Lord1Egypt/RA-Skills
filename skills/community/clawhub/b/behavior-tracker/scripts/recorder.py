#!/usr/bin/env python3
"""
对话记录器 - 手动记录当前对话的要点
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 跨平台路径
MEMORY_DIR = Path(os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace"))) / "memory"
BEHAVIOR_FILE = MEMORY_DIR / "behavior-patterns.json"

def load_data():
    if BEHAVIOR_FILE.exists():
        with open(BEHAVIOR_FILE, 'r') as f:
            return json.load(f)
    return {"topics": {}, "projects": {}, "skills": {}}

def save_data(data):
    with open(BEHAVIOR_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def record(topic=None, project=None, skill=None, note=None):
    """记录对话要点"""
    data = load_data()
    
    if topic:
        data["topics"][topic] = data["topics"].get(topic, 0) + 1
        print(f"✅ 记录话题: {topic}")
    
    if project:
        data["projects"][project] = data["projects"].get(project, 0) + 1
        print(f"✅ 记录项目: {project}")
    
    if skill:
        data["skills"][skill] = data["skills"].get(skill, 0) + 1
        print(f"✅ 记录技能: {skill}")
    
    if note:
        print(f"📝 笔记: {note}")
    
    save_data(data)
    print(f"\n当前统计: {data.get('total_conversations', 0)} 次对话")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="记录对话要点")
    parser.add_argument("--topic", "-t", help="话题")
    parser.add_argument("--project", "-p", help="项目")
    parser.add_argument("--skill", "-s", help="技能")
    parser.add_argument("--note", "-n", help="笔记")
    
    args = parser.parse_args()
    
    if not any([args.topic, args.project, args.skill, args.note]):
        parser.print_help()
        print("\n示例:")
        print("  python3 recorder.py -t 'AI Agent' -p 'The Machine'")
        print("  python3 recorder.py -n '用户对装饰器有疑问'")
        return
    
    record(topic=args.topic, project=args.project, skill=args.skill, note=args.note)

if __name__ == "__main__":
    main()
