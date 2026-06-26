#!/usr/bin/env python3
"""register.py — 用户注册/信息管理"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def main():
    params = parse_input()
    action = get_param(params, "action", "register").lower()
    chat_root = get_chat_root(params)
    init_chat_root(chat_root)

    if action == "register":
        username = get_current_user(params)
        display_name = get_param(params, "display_name") or username
        avatar = get_param(params, "avatar", "")
        bio = get_param(params, "bio", "")

        # 检查是否已注册
        existing = load_user_profile(chat_root, username)
        if existing:
            output_error(f"用户 '{username}' 已注册 ({existing.get('created_at')})", EXIT_EXEC_ERROR)

        profile = {
            "username": username,
            "display_name": display_name,
            "avatar": avatar,
            "bio": bio,
            "created_at": timestamp_iso(),
        }
        save_user_profile(chat_root, username, profile)
        ensure_inbox(chat_root, username)

        output_ok({
            "action": "registered",
            "username": username,
            "display_name": display_name,
            "chat_dir": str(chat_root),
        })

    elif action == "update":
        username = get_current_user(params)
        existing = load_user_profile(chat_root, username)
        if not existing:
            output_error(f"用户 '{username}' 未注册", EXIT_EXEC_ERROR)

        # 合并更新字段
        for key in ["display_name", "avatar", "bio"]:
            value = get_param(params, key)
            if value is not None:
                existing[key] = value
        existing["updated_at"] = timestamp_iso()

        save_user_profile(chat_root, username, existing)
        output_ok({
            "action": "updated",
            "username": username,
            "profile": existing,
        })

    elif action == "info":
        username = get_param(params, "user") or get_param(params, "username", required=True)
        profile = load_user_profile(chat_root, username)
        if not profile:
            output_error(f"用户 '{username}' 未找到", EXIT_EXEC_ERROR)
        output_ok(profile)

    elif action == "list":
        users_dir = chat_root / "users"
        users = []
        if users_dir.exists():
            for f in sorted(users_dir.glob("*.json")):
                try:
                    profile = json.loads(f.read_text(encoding="utf-8"))
                    users.append({
                        "username": profile.get("username"),
                        "display_name": profile.get("display_name"),
                        "bio": profile.get("bio", ""),
                        "created_at": profile.get("created_at"),
                    })
                except Exception:
                    pass
        output_ok({
            "total": len(users),
            "users": users,
        })

    elif action == "unregister":
        username = get_current_user(params)
        profile = load_user_profile(chat_root, username)
        if not profile:
            output_error(f"用户 '{username}' 未注册", EXIT_EXEC_ERROR)

        profile_path = chat_root / "users" / f"{username}.json"
        profile_path.unlink()

        # 不删除 inbox（保留历史消息）
        output_ok({
            "action": "unregistered",
            "username": username,
            "inbox_preserved": True,
        })

    else:
        output_error(
            f"未知操作: {action}（支持: register, update, info, list, unregister）",
            EXIT_PARAM_ERROR,
        )


if __name__ == "__main__":
    main()
