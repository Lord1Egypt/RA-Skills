#!/usr/bin/env python3
"""
Self-Improving Agent - 用户纠正记录工具
记录用户的纠正，支持去重（原地更新计数而非追加重复）
"""

import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_utils import upsert_entry, update_index, load_entries

FILENAME = "corrections.jsonl"


def log_correction(topic, wrong, correct, context=None):
    # 先检查是否有相同主题+错误做法的旧记录，计算count
    existing_entries = load_entries(FILENAME)
    count = 1
    for old in existing_entries:
        if old.get("topic") == topic and old.get("wrong") == wrong:
            count = old.get("count", 1) + 1
            break

    entry = {
        "type": "correction",
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "wrong": wrong,
        "correct": correct,
        "context": context,
        "count": count,
    }

    is_new, saved = upsert_entry(FILENAME, entry, match_fields=["topic", "wrong"])

    if is_new:
        print(f"[新纠正] 已记录 [{topic}]:")
    else:
        print(f"[重复纠正] 已更新 [{topic}] (第{count}次纠正):")

    print(f"   错误做法: {wrong}")
    print(f"   正确做法: {correct}")
    if context:
        print(f"   上下文: {context}")

    if count > 2:
        print(f"\n   !! 此项已被纠正{count}次，请特别注意！")

    # 更新索引
    keywords = [topic] + wrong.split()[:3] + correct.split()[:3]
    update_index("correction", keywords)


def main():
    parser = argparse.ArgumentParser(description="记录用户纠正")
    parser.add_argument("--topic", required=True, help="纠正主题")
    parser.add_argument("--wrong", required=True, help="错误做法")
    parser.add_argument("--correct", required=True, help="正确做法")
    parser.add_argument("--context", default=None, help="上下文/位置")
    args = parser.parse_args()

    log_correction(args.topic, args.wrong, args.correct, args.context)


if __name__ == "__main__":
    main()
