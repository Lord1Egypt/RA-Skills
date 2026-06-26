#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat
from datetime import datetime, timedelta

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")
AUDIT_FILE   = os.path.expanduser("~/.openclaw/workspace/secrets.audit.log")

def load():
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"categories": [], "entries": {}}

def mask(val):
    s = str(val)
    return (s[:6] + "..." + s[-4:]) if len(s) > 10 else s[:2] + "**"

CATEGORY_LABELS = {
    "social": "社交媒体", "cloud": "云服务",
    "dev": "开发工具", "marketing": "营销平台", "other": "其他"
}

def formatExpire(expire_at):
    if not expire_at:
        return "永不过期"
    try:
        expire = datetime.strptime(expire_at, "%Y-%m-%d")
        delta = (expire.date() - datetime.now().date()).days
        if delta < 0:   return f"已于 {expire_at} 过期"
        elif delta == 0: return "今天过期 ⚠️"
        elif delta <= 7: return f"{expire_at} ({delta}天) ⚠️"
        elif delta <= 30: return f"{expire_at} ({delta}天)"
        return expire_at
    except:
        return expire_at

def list_all(raw=False, category=None, expire=False, days=7):
    data = load()
    entries = data.get("entries", {})

    if category:
        entries = {k: v for k, v in entries.items() if v.get("category") == category}
    if expire:
        threshold = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        entries = {k: v for k, v in entries.items()
                   if v.get("expire_at") and v["expire_at"] <= threshold}

    if not entries:
        print("暂无令牌，或筛选结果为空")
        return

    print(f"\n{'='*52}")
    print(f"  令牌管理中心 (共 {len(entries)} 个)")
    print(f"{'='*52}")

    for key, info in entries.items():
        name = info.get("name", key)
        cat  = CATEGORY_LABELS.get(info.get("category", "other"), info.get("category"))
        read = info.get("read_count", 0)
        print(f"\n[{key}] {name}")
        print(f"    分类: {cat} | 过期: {formatExpire(info.get('expire_at'))} | 读取: {read}次")
        note = info.get("note", "")
        if note:
            print(f"    备注: {note}")
        if raw:
            for k, v in info.get("fields", {}).items():
                print(f"    {k}: {v}")
        else:
            for k, v in info.get("fields", {}).items():
                print(f"    {k}: {mask(v)}")

if __name__ == "__main__":
    args = sys.argv[1:]
    raw      = "--raw" in args
    expire   = "--expire" in args
    category = None
    days     = 7

    i = 0
    while i < len(args):
        if args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]; i += 2
        elif args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1]); i += 2
        else:
            i += 1

    list_all(raw=raw, expire=expire, category=category, days=days)
