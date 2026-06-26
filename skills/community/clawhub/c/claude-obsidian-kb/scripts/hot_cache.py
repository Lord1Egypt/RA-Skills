#!/usr/bin/env python3
"""
hot_cache.py — Claude-Obsidian 热缓存管理器
在 vault/.cache/ 中维持跨 session 的状态记忆
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

CACHE_DIR = ".cache"
CACHE_FILE = "hot_cache.json"

def get_cache_path(vault_path):
    vault = Path(vault_path)
    cache_dir = vault / CACHE_DIR
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / CACHE_FILE

def load_cache(cache_path):
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return {}
    return {}

def save_cache(cache_path, data):
    cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def cmd_get(cache_path, key):
    data = load_cache(cache_path)
    if key in data:
        print(data[key])
    else:
        print(f"[{key}] 未设置")

def cmd_set(cache_path, key, *value_parts):
    value = " ".join(value_parts)
    data = load_cache(cache_path)
    data[key] = value
    data[key + "_updated"] = datetime.now().isoformat()
    save_cache(cache_path, data)
    print(f"✅ [{key}] = {value}")

def cmd_list(cache_path):
    data = load_cache(cache_path)
    if not data:
        print("缓存为空")
        return
    print(f"{'Key':<30} {'Value':<40} {'更新时间'}")
    print("-" * 80)
    for k, v in data.items():
        updated = data.get(k + "_updated", "—")
        if not k.endswith("_updated"):
            print(f"{k:<30} {str(v):<40} {updated}")

def cmd_clear(cache_path):
    data = {}
    save_cache(cache_path, data)
    print("✅ 缓存已清空")

def cmd_touch(cache_path):
    """更新最后访问时间"""
    data = load_cache(cache_path)
    data["last_access"] = datetime.now().isoformat()
    data["last_access_readable"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_cache(cache_path, data)
    print(f"✅ 上次访问: {data['last_access_readable']}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Claude-Obsidian 热缓存管理")
    parser.add_argument("vault_path", help="Vault 目录路径")
    subparsers = parser.add_subparsers(dest="cmd", help="子命令")

    subparsers.add_parser("list", help="列出所有缓存")
    subparsers.add_parser("clear", help="清空缓存")
    subparsers.add_parser("touch", help="更新最后访问时间")

    p_get = subparsers.add_parser("get", help="读取缓存")
    p_get.add_argument("key", help="缓存键")

    p_set = subparsers.add_parser("set", help="设置缓存")
    p_set.add_argument("key", help="缓存键")
    p_set.add_argument("value", nargs="+", help="缓存值")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    cache_path = get_cache_path(args.vault_path)

    if args.cmd == "get":
        cmd_get(cache_path, args.key)
    elif args.cmd == "set":
        cmd_set(cache_path, args.key, *args.value)
    elif args.cmd == "list":
        cmd_list(cache_path)
    elif args.cmd == "clear":
        cmd_clear(cache_path)
    elif args.cmd == "touch":
        cmd_touch(cache_path)
