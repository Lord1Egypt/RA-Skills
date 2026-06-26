#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat, re
from datetime import datetime

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")
AUDIT_FILE   = os.path.expanduser("~/.openclaw/workspace/secrets.audit.log")
LOCK_FILE     = os.path.expanduser("~/.openclaw/workspace/secrets.lock")

CATEGORIES = ["social", "cloud", "dev", "marketing", "other"]

def _audit(action, key=None, field=None, masked=None, success=True):
    """Append-only audit log"""
    entry = {
        "ts": datetime.now().isoformat(),
        "action": action,
        "key": key,
        "field": field,
        "value_masked": masked,
        "success": success
    }
    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        os.chmod(AUDIT_FILE, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass  # never fail the main operation

def _mask(val):
    s = str(val)
    return (s[:6] + "..." + s[-4:]) if len(s) > 10 else s[:2] + "**"

def load():
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"categories": CATEGORIES, "entries": {}}

def save(data):
    with open(SECRETS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.chmod(SECRETS_FILE, stat.S_IRUSR | stat.S_IWUSR)

def sanitize_key(key: str) -> str:
    if not re.fullmatch(r'[a-zA-Z0-9_\-]{1,64}', key):
        raise ValueError(f"Invalid key format: {key!r}")
    return key

def sanitize_value(val: str) -> str:
    if not isinstance(val, str) or len(val.strip()) == 0:
        raise ValueError("Empty value not allowed")
    return val[:2048]

def add(key, name, fields, category="other", expire_at=None, note=""):
    key = sanitize_key(key)
    name = str(name)[:128]
    note = str(note)[:256]
    fields = {sanitize_key(k): sanitize_value(v) for k, v in fields.items()}

    data = load()
    now = datetime.now().isoformat()
    entry = {
        "name": name,
        "category": category,
        "fields": fields,
        "expire_at": expire_at,
        "note": note,
        "created_at": now[:10],
        "read_count": 0,
        "last_read": None
    }
    data["entries"][key] = entry
    save(data)

    for f, v in fields.items():
        _audit("add", key, f, _mask(v), True)
    print(f"[OK] {key} ({name}) 已保存")
    print(f"     分类: {category}")
    print(f"     过期: {expire_at or '无期限'}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "--help" in args or "-h" in args:
        print("用法: python add.py <key> <name> <field=value>... [--category ...] [--expire ...] [--note ...]")
        sys.exit(0)

    key = args[0]
    name = args[1] if len(args) > 1 else key
    fields = {}
    category = "other"
    expire_at = None
    note = ""

    i = 2
    while i < len(args):
        if args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]; i += 2
        elif args[i] == "--expire" and i + 1 < len(args):
            expire_at = args[i + 1]; i += 2
        elif args[i] == "--note" and i + 1 < len(args):
            note = args[i + 1]; i += 2
        elif "=" in args[i]:
            k, v = args[i].split("=", 1)
            fields[k.strip()] = v.strip(); i += 1
        else:
            i += 1

    if not fields:
        print("[错误] 至少需要一个 field=value 参数"); sys.exit(1)
    if category not in CATEGORIES:
        print(f"[错误] 无效分类: {category}"); sys.exit(1)

    try:
        add(key, name, fields, category, expire_at, note)
    except ValueError as e:
        _audit("add", key, success=False)
        print(f"[错误] {e}"); sys.exit(1)
