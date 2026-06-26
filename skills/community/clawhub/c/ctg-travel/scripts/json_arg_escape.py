#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把标准 JSON 转成适合命令行 --arg 使用的单行、已转义字符串。
用于处理大 JSON（如 flight.createOrder 的 goExtData 等）的转义问题，无需每次手写 JSON 文件。

用法:
  从文件读取:
    python3 scripts/json_arg_escape.py path/to/payload.json

  从文件读取并在输出后删除该文件（用完后不保留）:
    python3 scripts/json_arg_escape.py --rm path/to/order_arg.json

  从 stdin 读取（可粘贴或管道）:
    python3 scripts/json_arg_escape.py < payload.json
    echo '{"a":1}' | python3 scripts/json_arg_escape.py

输出: 一行单引号包裹的字符串，可直接作为 apiexe.py --arg 的参数。
"""

import sys
import json
import argparse
from pathlib import Path

# 脚本所在目录的父目录为 skill 根目录
SCRIPT_DIR = Path(__file__).resolve().parent


def load_json(file_path=None, stdin_fallback=True):
    if file_path is not None:
        path = Path(file_path)
        if not path.is_absolute() and not path.exists():
            path = SCRIPT_DIR.parent / file_path
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), path
    if stdin_fallback and not sys.stdin.isatty():
        text = sys.stdin.read()
        if text.strip():
            return json.loads(text), None
    return None, None


def shell_single_quoted(s: str) -> str:
    """转成适合单引号包裹的 shell 字符串：' 变成 '\'' """
    return "'" + s.replace("'", "'\"'\"'") + "'"


def main():
    parser = argparse.ArgumentParser(description="将 JSON 转成适合 shell --arg 的单行转义字符串")
    parser.add_argument("--rm", action="store_true", help="从文件读取时，输出后删除该文件（用完后不保留）")
    parser.add_argument("json_file", nargs="?", default=None, help="JSON 文件路径；不传则从 stdin 读取")
    args = parser.parse_args()

    try:
        data, path = load_json(args.json_file)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if data is None:
        print("Usage: json_arg_escape.py [--rm] [json_file]  or  stdin", file=sys.stderr)
        sys.exit(1)

    s = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    print(shell_single_quoted(s))

    if args.rm and path is not None and path.exists():
        path.unlink()


if __name__ == "__main__":
    main()
