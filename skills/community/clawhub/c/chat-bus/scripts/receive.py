#!/usr/bin/env python3
"""receive.py — 接收新消息"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def main():
    params = parse_input()
    chat_root = get_chat_root(params)
    username = get_current_user(params)

    source = get_param(params, "source", "inbox").lower()  # "inbox" | "room"
    since = get_param(params, "since")  # 时间戳，只取此时间之后的消息
    limit = get_param(params, "limit", 50)
    mark_read = get_param(params, "mark_read", True)
    unread_only = get_param(params, "unread_only", False)

    messages = []

    if source == "inbox":
        inbox = chat_root / "inbox" / username
        if not inbox.exists():
            output_ok({"user": username, "messages": [], "total": 0})

        for f in sorted(inbox.glob("*.json")):
            msg = load_message(f)
            if not msg:
                continue
            # 时间过滤
            if since and msg.get("timestamp", "") <= since:
                continue
            # 未读过滤
            is_read = f.suffix == ".read"
            if unread_only and is_read:
                continue
            messages.append(msg)
            if len(messages) >= limit:
                break

        # 标记已读：重命名为 .json.read
        if mark_read and messages:
            for f in sorted(inbox.glob("*.json")):
                if f.suffix == ".json":
                    msg = load_message(f)
                    if msg and since and msg.get("timestamp", "") <= since:
                        continue
                    # 只标记本次返回的消息为已读
                    msg_id = msg.get("id", "")
                    if any(m.get("id") == msg_id for m in messages):
                        try:
                            f.rename(str(f) + ".read")
                        except Exception:
                            pass

    elif source == "room":
        room = get_param(params, "room", required=True)
        room_path = chat_root / "rooms" / room
        if not room_path.exists():
            output_ok({"room": room, "messages": [], "total": 0})

        for f in sorted(room_path.glob("*.json")):
            msg = load_message(f)
            if not msg:
                continue
            # 房间消息中过滤掉自己发的（可选）
            # if msg.get("sender") == username:
            #     continue
            if since and msg.get("timestamp", "") <= since:
                continue
            messages.append(msg)
            if len(messages) >= limit:
                break

    else:
        output_error(f"未知来源: {source}（支持: inbox, room）", EXIT_PARAM_ERROR)

    # 按时间正序
    messages.sort(key=lambda m: m.get("timestamp", ""))

    unread_count = sum(1 for m in messages if not m.get("_read", True))

    output_ok({
        "user": username,
        "source": source,
        "room": get_param(params, "room"),
        "messages": messages,
        "returned": len(messages),
        "unread": unread_count,
        "since": since,
    })


if __name__ == "__main__":
    main()
