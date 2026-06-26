#!/usr/bin/env python3
"""JSON工具箱 - 格式化/比对/提取/压缩/验证"""
import sys
import os
import json
import argparse

def cmd_format(text):
    """格式化JSON"""
    try:
        data = json.loads(text)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}", file=sys.stderr)
        return False

def cmd_diff(file1, file2):
    """比对两个JSON文件"""
    try:
        with open(file1) as f:
            d1 = json.load(f)
        with open(file2) as f:
            d2 = json.load(f)
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}", file=sys.stderr)
        return False

    # 简单diff：检查键差异
    only1 = set(get_keys(d1)) - set(get_keys(d2))
    only2 = set(get_keys(d2)) - set(get_keys(d1))
    all_keys = set(get_keys(d1)) & set(get_keys(d2))
    changed = {k for k in all_keys
                if d1.get(k) != d2.get(k)}

    print("文件1独有:", only1 or "无")
    print("文件2独有:", only2 or "无")
    print("值不同:", changed or "无")
    return True

def get_keys(obj, prefix=""):
    """递归获取所有键路径"""
    if isinstance(obj, dict):
        result = []
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            result.append(path)
            result.extend(get_keys(v, path))
        return result
    elif isinstance(obj, list):
        return [f"{prefix}[i]" for i in range(len(obj))]
    return []

def cmd_extract(text, path):
    """从JSON提取指定路径"""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}", file=sys.stderr)
        return False

    parts = path.split(".")
    for part in parts:
        if isinstance(data, dict):
            data = data.get(part, {})
        else:
            data = None
            break

    if data is None:
        print(f"❌ 路径 '{path}' 不存在", file=sys.stderr)
        return False

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return True

def cmd_minify(text):
    """压缩JSON"""
    try:
        data = json.loads(text)
        print(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}", file=sys.stderr)
        return False

def cmd_validate(text):
    """验证JSON"""
    try:
        json.loads(text)
        print("✅ 有效的JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python json_tool.py format <json>")
        print("  python json_tool.py validate <json>")
        print("  python json_tool.py minify <json>")
        print("  python json_tool.py extract <json> <path>")
        print("  python json_tool.py diff <file1.json> <file2.json>")
        print("  echo '<json>' | python json_tool.py format")
        sys.exit(1)

    cmd = sys.argv[1]

    # diff 需要两个文件路径
    if cmd == "diff":
        if len(sys.argv) < 4:
            print("用法: python json_tool.py diff <file1.json> <file2.json>", file=sys.stderr)
            sys.exit(1)
        sys.exit(0 if cmd_diff(sys.argv[2], sys.argv[3]) else 1)

    # extract 需要路径参数
    if cmd == "extract":
        if len(sys.argv) < 4:
            print("用法: python json_tool.py extract <json> <path>", file=sys.stderr)
            sys.exit(1)
        json_text = sys.argv[2]
        path = sys.argv[3]
    else:
        json_text = sys.argv[2] if len(sys.argv) > 2 else ""

    # 从stdin读取
    if not json_text and not sys.stdin.isatty():
        json_text = sys.stdin.read().strip()

    if not json_text:
        print(f"用法: python json_tool.py {cmd} '<JSON字符串或文件路径>'", file=sys.stderr)
        sys.exit(1)

    # 如果是文件路径，读取文件
    if os.path.isfile(json_text):
        with open(json_text) as f:
            json_text = f.read().strip()

    if cmd == "format":
        sys.exit(0 if cmd_format(json_text) else 1)
    elif cmd == "minify":
        sys.exit(0 if cmd_minify(json_text) else 1)
    elif cmd == "validate":
        sys.exit(0 if cmd_validate(json_text) else 1)
    elif cmd == "extract":
        sys.exit(0 if cmd_extract(json_text, path) else 1)
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
