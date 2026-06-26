#!/usr/bin/env python3
"""write_file — 写入文件"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

def main():
    params = parse_input()
    path = get_param(params, "path", required=True)
    content = get_param(params, "content", required=True)
    encoding = get_param(params, "encoding", "utf-8")
    mkdirs = get_param(params, "mkdirs", True)
    append = get_param(params, "append", False)
    newline = get_param(params, "newline", None)

    p = resolve_path(str(path))

    try:
        if mkdirs:
            p.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        kwargs = {"encoding": encoding}
        if newline is not None:
            kwargs["newline"] = newline
        p.write_text(content, **kwargs)
        size = p.stat().st_size
    except Exception as e:
        output_error(f"写入失败: {e}", EXIT_EXEC_ERROR)

    output_ok({
        "path": str(p),
        "bytes": size,
        "mode": "append" if append else "overwrite",
    })

if __name__ == "__main__":
    main()
