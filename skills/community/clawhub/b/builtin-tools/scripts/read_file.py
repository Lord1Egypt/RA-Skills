#!/usr/bin/env python3
"""read_file — 读取文件"""
import sys, os
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *

def main():
    params = parse_input()
    path = get_param(params, "path", required=True)
    offset = get_param(params, "offset", 0)
    limit = get_param(params, "limit")
    encoding = get_param(params, "encoding", "utf-8")

    p = resolve_path(str(path), must_exist=True)
    if not p.is_file():
        output_error(f"不是文件: {p}", EXIT_EXEC_ERROR)

    # 图片等二进制文件
    img_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico"}
    if p.suffix.lower() in img_exts:
        stat = p.stat()
        output_ok({
            "path": str(p),
            "type": "image",
            "size": stat.st_size,
            "suffix": p.suffix.lower(),
            "message": "二进制文件，请用图片查看器打开",
        })

    try:
        content = p.read_text(encoding=encoding, errors="replace")
    except Exception as e:
        output_error(f"读取失败: {e}", EXIT_EXEC_ERROR)

    lines = content.splitlines()
    total_lines = len(lines)

    if offset:
        lines = lines[offset:]
    if limit:
        lines = lines[:limit]

    stat = p.stat()
    output_ok({
        "path": str(p),
        "type": "text",
        "content": content if limit is None and not offset else "\n".join(lines),
        "lines": lines if (limit or offset) else None,
        "total_lines": total_lines,
        "shown_lines": len(lines),
        "size": stat.st_size,
        "encoding": encoding,
    })

if __name__ == "__main__":
    main()
