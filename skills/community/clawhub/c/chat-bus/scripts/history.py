#!/usr/bin/env python3
"""history.py — 消息历史查询"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def main():
    params = parse_input()
    chat_root = get_chat_root(params)

    source = get_param(params, "source", "inbox").lower()  # "inbox" | "room"
    user = get_param(params, "user") or get_param(params, "username")
    room = get_param(params, "room")
    limit = get_param(params, "limit", 100)
    offset = get_param(params, "offset", 0)
    search = get_param(params, "search")  # 内容搜索
    sender_filter = get_param(params, "sender")  # 按发送者过滤
    date_filter = get_param(params, "date")  # 按日期过滤 YYYY-MM-DD

    messages = []
    base_path = None

    if source == "inbox":
        if not user:
            output_error("inbox 模式需要 user 参数", EXIT_PARAM_ERROR)
        base_path = chat_root / "inbox" / user
    elif source == "room":
        if not room:
            output_error("room 模式需要 room 参数", EXIT_PARAM_ERROR)
        base_path = chat_root / "rooms" / room
    else:
        output_error(f"未知来源: {source}（支持: inbox, room）", EXIT_PARAM_ERROR)

    if not base_path.exists():
        output_ok({"source": source, "messages": [], "total": 0})

    all_files = list(base_path.glob("*.json")) + list(base_path.glob("*.json.read"))
    all_files.sort(reverse=True)  # 最新在前

    collected = 0
    skipped = 0

    for f in all_files:
        msg = load_message(f)
        if not msg:
            continue

        # 搜索过滤
        if search:
            if search.lower() not in msg.get("content", "").lower():
                continue

        # 发送者过滤
        if sender_filter and msg.get("sender") != sender_filter:
            continue

        # 日期过滤
        if date_filter:
            ts = msg.get("timestamp", "")
            if not ts.startswith(date_filter):
                continue

        # 分页
        if collected < offset:
            skipped += 1
            continue

        # 已读状态
        msg["_read"] = f.suffix == ".read"
        messages.append(msg)
        collected += 1
        if collected >= limit:
            break

    # 按时间正序返回
    messages.sort(key=lambda m: m.get("timestamp", ""))

    total_available = len(all_files)

    output_ok({
        "source": source,
        "user": user,
        "room": room,
        "messages": messages,
        "returned": len(messages),
        "offset": offset,
        "total_available": total_available,
        "filters": {
            "search": search,
            "sender": sender_filter,
            "date": date_filter,
        },
    })


if __name__ == "__main__":
    main()
