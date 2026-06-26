#!/usr/bin/env python3
"""
Self-Improving Agent - 知识盲区记录工具
记录过时知识、API变更、废弃方法等
"""

import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_utils import upsert_entry, update_index

FILENAME = "knowledge_gaps.jsonl"


def log_knowledge_gap(topic, outdated, current, source=None):
    entry = {
        "type": "knowledge_gap",
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "outdated": outdated,
        "current": current,
        "source": source,
        "status": "active",
    }

    is_new, saved = upsert_entry(FILENAME, entry, match_fields=["topic", "outdated"])

    if is_new:
        print(f"[新盲区] 已记录 [{topic}]:")
    else:
        print(f"[更新盲区] 已更新 [{topic}]:")

    print(f"   过时信息: {outdated}")
    print(f"   当前正确: {current}")
    if source:
        print(f"   信息来源: {source}")

    keywords = [topic] + outdated.split()[:3] + current.split()[:3]
    update_index("knowledge_gap", keywords)


def main():
    parser = argparse.ArgumentParser(description="记录知识盲区/过时知识")
    parser.add_argument("--topic", required=True, help="主题")
    parser.add_argument("--outdated", required=True, help="过时的知识/做法")
    parser.add_argument("--current", required=True, help="当前正确信息")
    parser.add_argument("--source", default=None, help="信息来源（文档链接、版本号等）")
    args = parser.parse_args()

    log_knowledge_gap(args.topic, args.outdated, args.current, args.source)


if __name__ == "__main__":
    main()
