#!/usr/bin/env python3
"""rooms.py — 群聊房间管理"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def load_room_config(chat_root, room):
    """加载房间配置"""
    config_path = chat_root / "rooms" / room / "_room.json"
    if config_path.exists():
        try:
            return json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def save_room_config(chat_root, room, config):
    """保存房间配置"""
    room_path = chat_root / "rooms" / room
    room_path.mkdir(parents=True, exist_ok=True)
    config_path = room_path / "_room.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    return config_path


def main():
    params = parse_input()
    chat_root = get_chat_root(params)
    init_chat_root(chat_root)

    action = get_param(params, "action", "list").lower()

    if action == "create":
        username = get_current_user(params)
        room = get_param(params, "room", required=True)
        topic = get_param(params, "topic", "")
        description = get_param(params, "description", "")

        # 验证创建者已注册
        creator = load_user_profile(chat_root, username)
        if not creator:
            output_error(f"用户 '{username}' 未注册", EXIT_EXEC_ERROR)

        room_path = chat_root / "rooms" / room
        if room_path.exists():
            output_error(f"房间 '{room}' 已存在", EXIT_EXEC_ERROR)

        config = {
            "room": room,
            "topic": topic,
            "description": description,
            "created_by": username,
            "created_at": timestamp_iso(),
            "members": [username],
        }
        save_room_config(chat_root, room, config)

        # 发送系统消息
        sys_msg = {
            "id": gen_message_id(),
            "sender": "system",
            "sender_display": "System",
            "content": f"{username} 创建了房间 '{room}'",
            "timestamp": timestamp_iso(),
            "type": "room",
            "room": room,
            "_system": True,
        }
        msg_path = room_path / format_message_filename("system", sys_msg["id"])
        save_message(msg_path, sys_msg)

        output_ok({
            "action": "created",
            "room": room,
            "topic": topic,
            "created_by": username,
        })

    elif action == "join":
        username = get_current_user(params)
        room = get_param(params, "room", required=True)

        config = load_room_config(chat_root, room)
        if not config:
            output_error(f"房间 '{room}' 不存在", EXIT_EXEC_ERROR)

        members = config.get("members", [])
        if username in members:
            output_ok({"action": "already_joined", "room": room, "members": len(members)})
            return

        members.append(username)
        config["members"] = members
        config["updated_at"] = timestamp_iso()
        save_room_config(chat_root, room, config)

        # 系统消息
        room_path = chat_root / "rooms" / room
        sys_msg = {
            "id": gen_message_id(),
            "sender": "system",
            "sender_display": "System",
            "content": f"{username} 加入了房间",
            "timestamp": timestamp_iso(),
            "type": "room",
            "room": room,
            "_system": True,
        }
        msg_path = room_path / format_message_filename("system", sys_msg["id"])
        save_message(msg_path, sys_msg)

        output_ok({"action": "joined", "room": room, "members": len(members)})

    elif action == "leave":
        username = get_current_user(params)
        room = get_param(params, "room", required=True)

        config = load_room_config(chat_root, room)
        if not config:
            output_error(f"房间 '{room}' 不存在", EXIT_EXEC_ERROR)

        members = config.get("members", [])
        if username not in members:
            output_ok({"action": "not_in_room", "room": room})
            return

        members.remove(username)
        config["members"] = members
        save_room_config(chat_root, room, config)

        # 系统消息
        room_path = chat_root / "rooms" / room
        sys_msg = {
            "id": gen_message_id(),
            "sender": "system",
            "sender_display": "System",
            "content": f"{username} 离开了房间",
            "timestamp": timestamp_iso(),
            "type": "room",
            "room": room,
            "_system": True,
        }
        msg_path = room_path / format_message_filename("system", sys_msg["id"])
        save_message(msg_path, sys_msg)

        output_ok({"action": "left", "room": room, "members": len(members)})

    elif action == "info":
        room = get_param(params, "room", required=True)
        config = load_room_config(chat_root, room)
        if not config:
            output_error(f"房间 '{room}' 不存在", EXIT_EXEC_ERROR)

        # 统计消息数
        room_path = chat_root / "rooms" / room
        msg_count = len(list(room_path.glob("*.json")))

        output_ok({
            "room": room,
            "topic": config.get("topic", ""),
            "description": config.get("description", ""),
            "created_by": config.get("created_by"),
            "created_at": config.get("created_at"),
            "members": config.get("members", []),
            "member_count": len(config.get("members", [])),
            "message_count": msg_count,
        })

    elif action == "list":
        rooms_dir = chat_root / "rooms"
        rooms = []
        if rooms_dir.exists():
            for d in sorted(rooms_dir.iterdir()):
                if d.is_dir():
                    config = load_room_config(chat_root, d.name)
                    if config:
                        msg_count = len(list(d.glob("*.json")))
                        rooms.append({
                            "room": d.name,
                            "topic": config.get("topic", ""),
                            "members": len(config.get("members", [])),
                            "message_count": msg_count,
                            "created_at": config.get("created_at"),
                        })
        output_ok({"total": len(rooms), "rooms": rooms})

    elif action == "delete":
        username = get_current_user(params)
        room = get_param(params, "room", required=True)

        config = load_room_config(chat_root, room)
        if not config:
            output_error(f"房间 '{room}' 不存在", EXIT_EXEC_ERROR)

        # 只有创建者可以删除
        if config.get("created_by") != username:
            output_error("只有房间创建者可以删除房间", EXIT_PARAM_ERROR)

        import shutil
        room_path = chat_root / "rooms" / room
        shutil.rmtree(str(room_path), ignore_errors=True)

        output_ok({"action": "deleted", "room": room})

    else:
        output_error(
            f"未知操作: {action}（支持: create, join, leave, info, list, delete）",
            EXIT_PARAM_ERROR,
        )


if __name__ == "__main__":
    main()
