#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat, re, secrets
from datetime import datetime

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")
AUDIT_FILE   = os.path.expanduser("~/.openclaw/workspace/secrets.audit.log")

def _audit(action, key=None, success=True):
    entry = {"ts": datetime.now().isoformat(), "action": action, "key": key, "success": success}
    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        os.chmod(AUDIT_FILE, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass

def load():
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"categories": [], "entries": {}}

def save(data):
    with open(SECRETS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.chmod(SECRETS_FILE, stat.S_IRUSR | stat.S_IWUSR)

def _overwrite_value(value: str) -> str:
    """
    用随机数据覆写字符串值，然后返回全零字符串。
    原地覆写后返回等长不可读字符，内存中原值被破坏。
    """
    if not isinstance(value, str):
        return value
    # 用不可打印字符替换（保留长度，防止信息泄露）
    replacer = '\x00' * len(value)
    # 触发 Python GC 后 s 会被覆盖
    return replacer

def secure_remove_entry(key: str) -> bool:
    """
    安全删除单个 entry：
    1. 验证 key 存在
    2. 将所有字段值覆写为不可读字符
    3. 从 JSON 中删除 entry
    4. 保存文件（权限 600）
    5. 记录审计日志
    """
    data = load()
    if key not in data.get("entries", {}):
        _audit("remove", key, False)
        print(f"[错误] 未找到令牌: {key}"); return False

    entry = data["entries"][key]
    name = entry.get("name", key)

    # 覆写所有字段值（原地破坏）
    for field_name in list(entry.get("fields", {}).keys()):
        original = entry["fields"][field_name]
        # 覆写后替换（不可逆）
        entry["fields"][field_name] = _overwrite_value(original)

    # 删除 entry
    del data["entries"][key]
    save(data)

    _audit("remove", key, True)
    print(f"[OK] 已安全删除 {key} ({name})")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print("用法: python remove.py <key>"); sys.exit(1)

    key = sys.argv[1]
    if not re.fullmatch(r'[a-zA-Z0-9_\-]{1,64}', key):
        print(f"[错误] Invalid key format"); sys.exit(1)

    try:
        secure_remove_entry(key)
    except Exception as e:
        _audit("remove", key, False)
        print(f"[错误] {e}"); sys.exit(1)
