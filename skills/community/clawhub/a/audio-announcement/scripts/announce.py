#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一播报入口脚本
避免硬编码路径，集中管理语音播报调用
"""

import sys
from pathlib import Path

# 计算 skill 根目录（相对于本脚本位置）
# 脚本位置：workspace/scripts/announce.py
# skill 位置：~/.openclaw-autoclaw/skills/audio-announcement/
SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = Path.home() / ".openclaw-autoclaw" / "skills"
ANNOUNCE_SCRIPT = SKILLS_DIR / "audio-announcement" / "audio_announcement" / "scripts" / "announce_pygame.py"

# 可选的备用路径（相对路径）
if not ANNOUNCE_SCRIPT.exists():
    # 尝试从当前工作目录向上查找
    cwd = Path.cwd()
    if "audio-announcement" in str(cwd):
        # 可能在 skill 目录中
        ANNOUNCE_SCRIPT = cwd / "audio_announcement" / "scripts" / "announce_pygame.py"

def usage():
    print("用法: announce <type> <message> [lang]")
    print("类型: receive, task, complete, error")
    print("语言: zh (中文), en (英文) 等")
    print("示例: announce receive '收到指令' zh")

def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    ann_type = sys.argv[1]
    message = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else "zh"

    if ann_type not in ("receive", "task", "complete", "error"):
        print(f"错误: 未知类型 '{ann_type}'")
        usage()
        sys.exit(1)

    # 调用技能脚本
    import subprocess
    cmd = [sys.executable, str(ANNOUNCE_SCRIPT), ann_type, message, lang]
    result = subprocess.run(cmd)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
