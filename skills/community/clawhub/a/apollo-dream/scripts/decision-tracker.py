#!/usr/bin/env python3
"""
decision-tracker.py - 决策点追踪
识别并记录对话中的关键决策
"""
import os
import json
import re
from datetime import datetime

STATE_DIR = "/root/.openclaw/workspace/.dream"
DECISION_FILE = os.path.join(STATE_DIR, "decisions.json")

# 决策相关模式
DECISION_PATTERNS = [
    (r'决定：(.+)', 'decision'),
    (r'结论是：(.+)', 'conclusion'),
    (r'选([ABCD])：(.+)', 'choice'),
    (r'确认：(.+)', 'confirmation'),
    (r'同意：(.+)', 'agreement'),
    (r'用(.+)方案', 'adopted'),
    (r'不做(.+)', 'rejected'),
]

def init_state():
    """初始化状态目录"""
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(DECISION_FILE):
        with open(DECISION_FILE, 'w') as f:
            json.dump({'decisions': [], 'pending': []}, f)

def add_decision(text, source="unknown"):
    """添加决策"""
    init_state()
    
    decisions = []
    for pattern, label in DECISION_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            decisions.append({
                'type': label,
                'content': match if isinstance(match, str) else ' '.join(match),
                'source': source,
                'timestamp': datetime.now().isoformat(),
            })
    
    if decisions:
        with open(DECISION_FILE, 'r') as f:
            state = json.load(f)
        
        state['decisions'].extend(decisions)
        
        with open(DECISION_FILE, 'w') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    return decisions

def get_decisions(limit=10):
    """获取最近决策"""
    init_state()
    with open(DECISION_FILE, 'r') as f:
        state = json.load(f)
    
    return state['decisions'][-limit:]

def list_decisions():
    """列出所有决策"""
    decisions = get_decisions(limit=100)
    
    if not decisions:
        print("暂无决策记录")
        return
    
    print(f"共 {len(decisions)} 条决策:")
    for d in decisions:
        print(f"  [{d['type']}] {d['content'][:50]}")
        print(f"    {d['timestamp'][:19]} | 来源: {d['source']}")

def extract_decisions_from_text(text):
    """
    从文本中提取决策点
    
    Returns:
        list: 提取到的决策
    """
    decisions = []
    for pattern, label in DECISION_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            content = match if isinstance(match, str) else ' '.join(match)
            decisions.append({
                'type': label,
                'content': content,
                'matched_by': pattern,
            })
    return decisions

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: decision-tracker.py <add|list|extract> [args]")
        print("  add <text>")
        print("  list")
        print("  extract <text>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'add':
        if len(sys.argv) < 3:
            print("用法: decision-tracker.py add <text>")
            sys.exit(1)
        text = ' '.join(sys.argv[2:])
        decisions = add_decision(text)
        print(f"添加了 {len(decisions)} 条决策")
    
    elif cmd == 'list':
        list_decisions()
    
    elif cmd == 'extract':
        if len(sys.argv) < 3:
            print("用法: decision-tracker.py extract <text>")
            sys.exit(1)
        text = ' '.join(sys.argv[2:])
        decisions = extract_decisions_from_text(text)
        print(f"发现 {len(decisions)} 个决策点:")
        for d in decisions:
            print(f"  [{d['type']}] {d['content'][:50]}")
    
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()
