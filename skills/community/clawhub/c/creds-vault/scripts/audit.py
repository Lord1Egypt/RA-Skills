#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit.py — 操作审计日志
所有对 secrets.json 的操作都会记录，不可篡改（append-only）
"""
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, stat
from datetime import datetime

AUDIT_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.audit.log")

def log(action: str, key: str = None, field: str = None, masked_value: str = None, success: bool = True):
    """
    追加一条审计日志。
    action: add / get / remove / update / backup / restore
    """
    ts = datetime.now().isoformat()
    entry = {
        "ts": ts,
        "action": action,
        "key": key,
        "field": field,
        "value_masked": masked_value,
        "success": success
    }
    line = json.dumps(entry, ensure_ascii=False)
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    os.chmod(AUDIT_FILE, stat.S_IRUSR | stat.S_IWUSR)

def get_audit(limit: int = 50):
    """读取最近 limit 条审计日志"""
    if not os.path.exists(AUDIT_FILE):
        print("暂无审计记录")
        return
    with open(AUDIT_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    recent = lines[-limit:]
    print(f"\n{'='*60}")
    print(f"  审计日志 (共 {len(lines)} 条，显示最近 {limit} 条)")
    print(f"{'='*60}\n")
    for line in recent:
        try:
            import json
            entry = json.loads(line.strip())
            status = "✓" if entry["success"] else "✗"
            val = f" [{entry.get('field','')}={entry.get('value_masked','')}]" if entry.get("value_masked") else ""
            print(f"{status} {entry['ts'][11:19]} [{entry['action']}] {entry.get('key','')}{val}")
        except:
            print(line.strip())

import json  # top-level for log()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="审计日志查看器")
    parser.add_argument("--limit", type=int, default=50, help="显示条数")
    parser.add_argument("--export", action="store_true", help="导出所有日志")
    args = parser.parse_args()

    if args.export:
        if os.path.exists(AUDIT_FILE):
            with open(AUDIT_FILE, encoding="utf-8") as f:
                print(f.read())
        else:
            print("")
    else:
        get_audit(limit=args.limit)
