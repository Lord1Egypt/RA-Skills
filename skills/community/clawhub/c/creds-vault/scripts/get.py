#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat, re
from datetime import datetime

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")
AUDIT_FILE   = os.path.expanduser("~/.openclaw/workspace/secrets.audit.log")

def _audit(action, key=None, field=None, masked=None, success=True):
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
        pass

def _mask(val):
    s = str(val)
    return (s[:6] + "..." + s[-4:]) if len(s) > 10 else s[:2] + "**"

def load():
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"categories": [], "entries": {}}

def save(data):
    with open(SECRETS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.chmod(SECRETS_FILE, stat.S_IRUSR | stat.S_IWUSR)

def get(key, field=None):
    # Sanitize
    if not re.fullmatch(r'[a-zA-Z0-9_\-]{1,64}', key):
        print(f"[错误] Invalid key format"); return None

    data = load()
    if key not in data.get("entries", {}):
        _audit("get", key, success=False)
        print(f"[错误] 未找到令牌: {key}"); return None

    entry = data["entries"][key]

    if field:
        val = entry.get("fields", {}).get(field)
        if val is None:
            _audit("get", key, field, success=False)
            print(f"[错误] {key} 中未找到字段: {field}"); return None
        # 更新读取统计
        entry["read_count"] = entry.get("read_count", 0) + 1
        entry["last_read"] = datetime.now().isoformat()
        save(data)
        _audit("get", key, field, _mask(val), True)
        print(val)
        return val
    else:
        entry["read_count"] = entry.get("read_count", 0) + 1
        entry["last_read"] = datetime.now().isoformat()
        save(data)
        _audit("get", key, success=True)
        print(f"\n[{key}] {entry.get('name', key)}")
        print(f"  分类: {entry.get('category', 'other')}")
        print(f"  过期: {entry.get('expire_at', '永不过期')}")
        print(f"  备注: {entry.get('note', '')}")
        print(f"  创建: {entry.get('created_at', '')}")
        print(f"  读取: {entry.get('read_count', 0)}次")
        print(f"  最近: {entry.get('last_read', '')}")
        print(f"  字段:")
        for k, v in entry.get("fields", {}).items():
            print(f"    {k}: {v}")
        return entry

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python get.py <key> [field]"); sys.exit(1)
    key = sys.argv[1]
    field = sys.argv[2] if len(sys.argv) > 2 else None
    get(key, field)
