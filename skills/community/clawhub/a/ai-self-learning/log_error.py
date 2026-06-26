#!/usr/bin/env python3
"""
Self-Improving Agent - 错误记录工具
自动捕获并记录命令失败，支持去重和索引更新
"""

import sys
import os
import argparse
from datetime import datetime

# 确保能导入同目录的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_utils import upsert_entry, update_index

FILENAME = "errors.jsonl"


def log_error(command, error_msg, fix=None, priority="medium"):
    entry = {
        "type": "error",
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "error": error_msg,
        "fix": fix,
        "priority": priority,
        "status": "pending" if not fix else "resolved",
    }

    is_new, saved = upsert_entry(FILENAME, entry, match_fields=["command", "error"])

    if is_new:
        print(f"[新错误] 已记录: {command[:60]}")
    else:
        print(f"[重复错误] 已更新: {command[:60]}")

    if fix:
        print(f"   修复方案: {fix}")
    else:
        print(f"   状态: 待分析")

    # 更新索引
    keywords = command.split() + error_msg.split()[:5]
    update_index("error", keywords)


def main():
    parser = argparse.ArgumentParser(description="记录命令执行错误")
    parser.add_argument("--command", required=True, help="失败的命令")
    parser.add_argument("--error", required=True, help="错误信息")
    parser.add_argument("--fix", default=None, help="修复方法")
    parser.add_argument("--priority", default="medium", choices=["high", "medium", "low"])
    args = parser.parse_args()

    log_error(args.command, args.error, args.fix, args.priority)


if __name__ == "__main__":
    main()
