#!/usr/bin/env python3
"""
随想记录脚本 - 确保真实写入文件

用法：
  cat content.txt | python3 record_thought.py <workspace_path> [--tag <tag>]
  echo "短内容" | python3 record_thought.py <workspace_path>
  python3 record_thought.py <workspace_path> < content.txt

从 stdin 读取内容，追加到 daily-thoughts/raw/YYYY-MM-DD.md，
输出 JSON 格式的确认信息。
"""

import sys
import os
import json
from datetime import datetime


def record_thought(content: str, workspace_path: str, tag: str = "") -> dict:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    raw_dir = os.path.join(workspace_path, "daily-thoughts", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    file_path = os.path.join(raw_dir, f"{date_str}.md")

    is_new_file = not os.path.exists(file_path)

    # Build entry block
    timestamp = f"## {date_str} {time_str}"
    if tag:
        timestamp += f" — {tag}"
    entry = f"\n\n{timestamp}\n\n{content.strip()}\n"

    with open(file_path, "a", encoding="utf-8") as f:
        if is_new_file:
            f.write(f"# {date_str} 随想记录\n")
        f.write(entry)

    # Stats
    with open(file_path, "r", encoding="utf-8") as f:
        full = f.read()

    bytes_size = os.path.getsize(file_path)
    lines = full.count("\n")

    prefix = full[:100]
    suffix = full[-100:] if len(full) > 100 else full

    return {
        "success": True,
        "file_path": os.path.relpath(file_path, workspace_path),
        "is_new_file": is_new_file,
        "bytes": bytes_size,
        "lines": lines,
        "prefix": prefix,
        "suffix": suffix,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: cat content | record_thought.py <workspace_path> [--tag <tag>]", file=sys.stderr)
        sys.exit(1)

    workspace_path = sys.argv[1]
    tag = ""
    if "--tag" in sys.argv:
        idx = sys.argv.index("--tag")
        if idx + 1 < len(sys.argv):
            tag = sys.argv[idx + 1]

    content = sys.stdin.read()
    if not content.strip():
        print("错误: stdin 为空，没有内容可记录", file=sys.stderr)
        sys.exit(1)

    result = record_thought(content, workspace_path, tag=tag)
    print(json.dumps(result, ensure_ascii=False, indent=2))
