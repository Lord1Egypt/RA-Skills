#!/usr/bin/env python3
"""replace_in_file — 精确字符串替换"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

def main():
    params = parse_input()
    path = get_param(params, "path", required=True)
    old = get_param(params, "old", required=True)
    new = get_param(params, "new", "")
    encoding = get_param(params, "encoding", "utf-8")
    count_max = get_param(params, "count", 1)

    p = resolve_path(str(path), must_exist=True)
    if not p.is_file():
        output_error(f"不是文件: {p}", EXIT_EXEC_ERROR)

    try:
        content = p.read_text(encoding=encoding, errors="replace")
    except Exception as e:
        output_error(f"读取失败: {e}", EXIT_EXEC_ERROR)

    occurrences = content.count(old)
    if occurrences == 0:
        output_error(f"未找到匹配文本 (长度={len(old)})", EXIT_EXEC_ERROR)

    if occurrences > count_max:
        output_error(
            f"找到 {occurrences} 处匹配，超过 count={count_max}。请提供更多上下文或增大 count。",
            EXIT_PARAM_ERROR,
        )

    new_content = content.replace(old, new, count_max)

    try:
        p.write_text(new_content, encoding=encoding)
    except Exception as e:
        output_error(f"写入失败: {e}", EXIT_EXEC_ERROR)

    output_ok({
        "path": str(p),
        "replaced": occurrences,
        "old_length": len(old),
        "new_length": len(new),
    })

if __name__ == "__main__":
    main()
