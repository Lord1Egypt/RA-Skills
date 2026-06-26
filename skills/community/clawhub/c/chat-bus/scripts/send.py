#!/usr/bin/env python3
"""send.py — 发送消息（单聊/群聊）"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def main():
    params = parse_input()
    chat_root = get_chat_root(params)
    init_chat_root(chat_root)

    sender = get_current_user(params)
    msg_type = get_param(params, "type", "direct").lower()  # "direct" | "room"

    # 验证发送者已注册
    sender_profile = load_user_profile(chat_root, sender)
    if not sender_profile:
        output_error(f"发送者 '{sender}' 未注册，请先 register", EXIT_EXEC_ERROR)

    content = get_param(params, "content", required=True)
    msg_id = gen_message_id()
    ts = timestamp_str()
    ts_iso = timestamp_iso()

    message = {
        "id": msg_id,
        "sender": sender,
        "sender_display": sender_profile.get("display_name", sender),
        "content": content,
        "timestamp": ts_iso,
        "type": msg_type,
    }

    if msg_type == "direct":
        # 单聊
        recipient = get_param(params, "to") or get_param(params, "recipient", required=True)
        # 验证收件人已注册
        recipient_profile = load_user_profile(chat_root, recipient)
        if not recipient_profile:
            output_error(f"收件人 '{recipient}' 未注册", EXIT_EXEC_ERROR)

        message["recipient"] = recipient
        message["recipient_display"] = recipient_profile.get("display_name", recipient)

        filename = format_message_filename(sender, msg_id, ts)
        msg_path = chat_root / "inbox" / recipient / filename
        save_message(msg_path, message)

        output_ok({
            "action": "sent",
            "type": "direct",
            "to": recipient,
            "message_id": msg_id,
            "file": filename,
        })

    elif msg_type == "room":
        # 群聊
        room = get_param(params, "room", required=True)
        room_path = chat_root / "rooms" / room
        if not room_path.exists():
            output_error(f"房间 '{room}' 不存在", EXIT_EXEC_ERROR)

        message["room"] = room
        filename = format_message_filename(sender, msg_id, ts)
        msg_path = room_path / filename
        save_message(msg_path, message)

        output_ok({
            "action": "sent",
            "type": "room",
            "room": room,
            "message_id": msg_id,
            "file": filename,
        })

    elif msg_type == "broadcast":
        # 广播给所有注册用户
        users_dir = chat_root / "users"
        count = 0
        if users_dir.exists():
            for f in users_dir.glob("*.json"):
                recipient = f.stem
                if recipient == sender:
                    continue
                filename = format_message_filename(sender, msg_id, ts)
                msg_path = chat_root / "inbox" / recipient / filename
                msg_copy = dict(message)
                msg_copy["recipient"] = recipient
                msg_copy["type"] = "broadcast"
                save_message(msg_path, msg_copy)
                count += 1

        output_ok({
            "action": "broadcast",
            "message_id": msg_id,
            "recipients": count,
        })

    else:
        output_error(
            f"未知消息类型: {msg_type}（支持: direct, room, broadcast）",
            EXIT_PARAM_ERROR,
        )


if __name__ == "__main__":
    main()
