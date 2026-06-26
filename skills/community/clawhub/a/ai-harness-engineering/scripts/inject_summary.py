#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 错误摘要注入脚本
每次session启动时自动执行，将错误台账摘要注入到上下文
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
ERRORS_FILE = DATA_DIR / "error_ledger.jsonl"
LEARNINGS_FILE = DATA_DIR / "learnings_ledger.jsonl"


def load_errors(limit: int = 5) -> list:
    """加载最近的错误记录"""
    errors = []
    if ERRORS_FILE.exists():
        with open(ERRORS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        errors.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    
    # 按时间倒序，返回最近 N 条
    errors.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return errors[:limit]


def load_high_frequency_learnings() -> list:
    """加载高频率学习（recurrence_count >= 3）"""
    learnings = []
    if LEARNINGS_FILE.exists():
        with open(LEARNINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        learning = json.loads(line)
                        if learning.get('recurrence_count', 1) >= 3 and learning.get('status') == 'pending':
                            learnings.append(learning)
                    except json.JSONDecodeError:
                        continue
    return learnings


def load_pending_errors() -> list:
    """加载未修复的错误"""
    errors = []
    if ERRORS_FILE.exists():
        with open(ERRORS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        error = json.loads(line)
                        if error.get('fix_status') == '未修复':
                            errors.append(error)
                    except json.JSONDecodeError:
                        continue
    return errors


def generate_summary() -> str:
    """生成错误台账摘要"""
    lines = []
    lines.append("【HarnessEngineering 错误台账摘要】")
    lines.append("")
    
    # 加载数据
    recent_errors = load_errors(5)
    high_freq_learnings = load_high_frequency_learnings()
    pending_errors = load_pending_errors()
    
    # 最近错误
    lines.append("📌 最近错误：")
    if recent_errors:
        for e in recent_errors:
            recency = f" (重复{e.get('recurrence_count', 1)}次)"
            lines.append(f"  • [{e.get('error_type')}] {e.get('question', '')[:40]}...{recency}")
    else:
        lines.append("  • 暂无")
    lines.append("")
    
    # 高频错误（需提升）
    if high_freq_learnings:
        lines.append("⚠️ 高频错误（recurrence_count >= 3，亟待提升）：")
        for l in high_freq_learnings:
            lines.append(f"  • [{l.get('category')}] {l.get('summary', '')[:40]}... (出现{l.get('recurrence_count')}次)")
        lines.append("")
    
    # 未修复错误
    lines.append(f"📊 未修复错误：{len(pending_errors)} 条")
    
    # 已规避的错误模式
    avoided_patterns = []
    for e in recent_errors:
        if e.get('fix_status') in ['已修复', '已规避']:
            avoided_patterns.append(e.get('correct_answer', '')[:30])
    
    if avoided_patterns:
        lines.append("")
        lines.append("✅ 已规避的错误模式：")
        for p in avoided_patterns[:3]:
            lines.append(f"  • {p}...")
    
    return '\n'.join(lines)


def inject_to_context(format: str = "text") -> dict:
    """注入错误摘要到上下文"""
    summary = generate_summary()
    
    if format == "json":
        return {
            "status": "ok",
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
    else:
        # 输出纯文本格式，可以被 OpenClaw 读取
        print(summary)
        return {"status": "ok"}


def session_start() -> str:
    """Session 启动时的注入"""
    return generate_summary()


def main():
    # 解决 Windows 输出编码问题
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(description='错误摘要注入')
    parser.add_argument('--action', default='session_start',
                       choices=['session_start', 'inject'],
                       help='操作类型')
    parser.add_argument('--format', default='text',
                       choices=['text', 'json'],
                       help='输出格式')
    parser.add_argument('--limit', type=int, default=5,
                       help='最近错误数量')
    
    args = parser.parse_args()
    
    if args.action == 'session_start':
        result = inject_to_context(args.format)
        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == 'inject':
        result = inject_to_context(args.format)
        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()