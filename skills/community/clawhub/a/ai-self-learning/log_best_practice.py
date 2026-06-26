#!/usr/bin/env python3
"""
Self-Improving Agent - 最佳实践记录工具
记录发现的最佳做法，支持去重和替代旧实践
"""

import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_utils import upsert_entry, update_index

FILENAME = "best_practices.jsonl"


def log_best_practice(category, practice, reason=None, supersedes=None):
    entry = {
        "type": "best_practice",
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "practice": practice,
        "reason": reason,
        "supersedes": supersedes,
        "usage_count": 0,
    }

    is_new, saved = upsert_entry(FILENAME, entry, match_fields=["category", "practice"])

    if is_new:
        print(f"[新实践] 已记录 [{category}]:")
    else:
        print(f"[更新实践] 已更新 [{category}]:")

    print(f"   实践: {practice}")
    if reason:
        print(f"   原因: {reason}")
    if supersedes:
        print(f"   替代: {supersedes}")

    keywords = [category] + practice.split()[:5]
    update_index("best_practice", keywords)


def main():
    parser = argparse.ArgumentParser(description="记录最佳实践")
    parser.add_argument("--category", required=True,
                        help="类别: security, performance, style, workflow, debugging, architecture, tooling")
    parser.add_argument("--practice", required=True, help="最佳实践内容")
    parser.add_argument("--reason", default=None, help="原因/好处")
    parser.add_argument("--supersedes", default=None, help="替代的旧做法")
    args = parser.parse_args()

    log_best_practice(args.category, args.practice, args.reason, args.supersedes)


if __name__ == "__main__":
    main()
