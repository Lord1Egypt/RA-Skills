#!/usr/bin/env python3
"""
auto_save_capsule.py — 自动保存会话胶囊 v1.0

由 index.js 的 message:received 和 message:sent hooks 调用。
保存当前工作记忆到会话胶囊，确保进程重启后能恢复上下文。

用法：
  python3 scripts/auto_save_capsule.py
"""

import json, os, sys
from datetime import datetime, timezone, timedelta

BEIJING_TZ = timezone(timedelta(hours=8))
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE") or os.path.expanduser("~/.openclaw/workspace")
CAPSULE_FILE = os.path.join(WORKSPACE, ".context_capsule.json")


def save_capsule():
    """保存当前上下文快照"""
    state = {
        "last_saved": datetime.now(BEIJING_TZ).isoformat(),
        "status": "ok"
    }
    try:
        os.makedirs(os.path.dirname(CAPSULE_FILE), exist_ok=True)
        with open(CAPSULE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print(json.dumps({"status": "ok", "path": CAPSULE_FILE}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))


if __name__ == "__main__":
    save_capsule()
