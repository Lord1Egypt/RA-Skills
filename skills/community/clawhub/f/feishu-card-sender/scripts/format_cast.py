#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def load_items(args):
    if args.input_json:
        return json.loads(args.input_json)
    if args.input_file:
        return json.loads(Path(args.input_file).read_text(encoding="utf-8"))
    data = sys.stdin.read().strip()
    if data:
        return json.loads(data)
    raise ValueError("No input provided. Use --input-json / --input-file / stdin")


def main():
    p = argparse.ArgumentParser(description="Format cast JSON array to Feishu card markdown lines")
    p.add_argument("--input-json", help='JSON string, e.g. [{"name":"吴京","role":"刘培强"}]')
    p.add_argument("--input-file", help="Path to JSON file")
    p.add_argument("--name-key", default="name")
    p.add_argument("--role-key", default="role")
    p.add_argument("--escape-newline", action="store_true", help="Output with \\n instead of real newlines")
    args = p.parse_args()

    items = load_items(args)
    if not isinstance(items, list):
        raise ValueError("Input must be a JSON array")

    lines = []
    for i in items:
        if not isinstance(i, dict):
            continue
        name = str(i.get(args.name_key, "")).strip()
        role = str(i.get(args.role_key, "")).strip()
        if not name:
            continue
        if role:
            lines.append(f"• **{name}** 饰 {role}")
        else:
            lines.append(f"• **{name}**")

    out = "\n".join(lines)
    if args.escape_newline:
        out = out.replace("\n", "\\n")
    print(out)


if __name__ == "__main__":
    main()
