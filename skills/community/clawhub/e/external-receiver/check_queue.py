#!/usr/bin/env python3
"""
检查 External Receiver 消息队列
供 OpenClaw Agent 在 heartbeat 时调用

用法（在 Agent 中）：
    from skills.external_receiver.check_queue import drain_queue
    new_messages = drain_queue()
    for msg in new_messages:
        print(msg["text"])
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

QUEUE_FILE = Path.home() / ".openclaw" / "workspace" / "received" / "message_queue.jsonl"
MARKER_FILE = Path.home() / ".openclaw" / "workspace" / "received" / ".last_read"


def drain_queue(max_age_minutes: int = 0) -> list[dict]:
    """
    读取并清空消息队列中的新消息。

    Args:
        max_age_minutes: 如果 > 0，只返回最近 N 分钟内的消息

    Returns:
        新消息列表，每条包含 {"time": "...", "text": "..."}
    """
    if not QUEUE_FILE.exists():
        return []

    try:
        lines = QUEUE_FILE.read_text().strip().split("\n")
    except Exception:
        return []

    if not lines:
        return []

    cutoff = None
    if max_age_minutes > 0:
        cutoff = datetime.now() - timedelta(minutes=max_age_minutes)

    new_entries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            if cutoff:
                entry_time = datetime.fromisoformat(entry.get("time", ""))
                if entry_time < cutoff:
                    continue
            new_entries.append(entry)
        except Exception:
            continue

    # 清空队列（保留文件）
    QUEUE_FILE.write_text("")

    return new_entries


def peek_queue(count: int = 10) -> list[dict]:
    """查看队列中的消息（不删除）"""
    if not QUEUE_FILE.exists():
        return []

    try:
        lines = QUEUE_FILE.read_text().strip().split("\n")
    except Exception:
        return []

    entries = []
    for line in lines[-count:]:
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except Exception:
            continue
    return entries


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--peek":
        msgs = peek_queue()
    else:
        msgs = drain_queue()

    if not msgs:
        print("没有新消息")
    else:
        for m in msgs:
            print(f"[{m['time']}]")
            print(m["text"])
            print("---")
