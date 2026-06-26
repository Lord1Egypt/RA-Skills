#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一播报入口脚本
通过包 API 调用（不再 subprocess 绕过），保证所有新功能生效
"""

import sys
from pathlib import Path

# 确保包可导入
try:
    from audio_announcement import announce, __version__
except ImportError:
    # 回退：尝试从 skill 目录导入
    skill_dir = Path.home() / ".openclaw-autoclaw" / "skills" / "beep-skills"
    if str(skill_dir) not in sys.path:
        sys.path.insert(0, str(skill_dir))
    from audio_announcement import announce, __version__

def usage():
    print(f"Beep - Small speaker v{__version__}")
    print("")
    print("[Rules] Enforced Announcement (every interaction):")
    print("   Types: receive, task, complete, error")
    print("   Principles: <=20 chars | conversational | no names | informative")
    print("   Examples: announce receive 'msg received'")
    print("            announce task 'publishing to GitHub'")
    print("            announce complete 'upload done'")
    print("            announce error 'network timeout'")
    print("")
    print("Usage: announce <type> <message> [lang]")
    print("Types: receive, task, complete, error")
    print("Languages: zh (Chinese), en (English)")
    print("Example: announce receive 'got message' zh")

def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    ann_type = sys.argv[1]
    message = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else "zh"

    if ann_type not in ("receive", "task", "complete", "error"):
        print(f"Error: unknown type '{ann_type}'")
        usage()
        sys.exit(1)

    # 直接调用包 API（不再 subprocess）
    success = announce(ann_type, message, lang=lang)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
