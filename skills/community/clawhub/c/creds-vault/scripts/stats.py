#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat
from datetime import datetime

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")
AUDIT_FILE   = os.path.expanduser("~/.openclaw/workspace/secrets.audit.log")

def load():
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"categories": [], "entries": {}}

CATEGORY_LABELS = {
    "social": "社交媒体", "cloud": "云服务",
    "dev": "开发工具", "marketing": "营销平台", "other": "其他"
}

def show_stats(top=None, key=None):
    data = load()
    entries = data.get("entries", {})

    if key:
        if key not in entries:
            print(f"[错误] 未找到令牌: {key}"); return
        v = entries[key]
        print(f"\n[{key}] {v.get('name', key)}")
        print(f"  分类: {CATEGORY_LABELS.get(v.get('category','other'), v.get('category'))}")
        print(f"  创建: {v.get('created_at', '')}")
        print(f"  读取次数: {v.get('read_count', 0)}")
        print(f"  最近读取: {v.get('last_read', '从未')}")
        print(f"  过期时间: {v.get('expire_at', '永不过期')}")
        return

    if not entries:
        print("暂无令牌统计数据"); return

    sorted_e = sorted(entries.items(), key=lambda x: x[1].get("read_count", 0), reverse=True)
    if top:
        sorted_e = sorted_e[:int(top)]

    print(f"\n{'='*52}")
    print(f"  令牌使用统计 (共 {len(entries)} 个)")
    print(f"{'='*52}")

    for k, v in sorted_e:
        name = v.get("name", k)
        count = v.get("read_count", 0)
        last  = v.get("last_read", "从未")
        cat   = CATEGORY_LABELS.get(v.get("category", "other"), v.get("category"))
        bar   = "█" * min(count, 30)
        print(f"\n[{k}] {name}")
        print(f"  分类: {cat} | 读取: {count}次 | 最近: {last}")
        if count > 0:
            print(f"  {bar}")

if __name__ == "__main__":
    args = sys.argv[1:]
    top = None
    key = None

    if "--top" in args:
        idx = args.index("--top")
        v = args[idx + 1] if idx + 1 < len(args) else None
        if v: top = v.lstrip("=")

    for a in args:
        if not a.startswith("--") and not a.startswith("-"):
            key = a; break

    show_stats(top=top, key=key)
