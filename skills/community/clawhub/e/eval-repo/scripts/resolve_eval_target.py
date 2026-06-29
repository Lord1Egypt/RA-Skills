from __future__ import annotations

import argparse
import json

import chat_context
import system_config as sc
from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", default="", help="Backward-compatible alias for SenderId.")
    parser.add_argument("--sender_id", default="", help="OpenClaw SenderId: the message sender open_id.")
    parser.add_argument("--chat_type", default="", help="OpenClaw ChatType: direct/group.")
    parser.add_argument("--chat_id", default="", help="OpenClaw GroupSubject in group chats.")
    parser.add_argument("--message_sid", default="", help="OpenClaw MessageSid for audit.")
    parser.add_argument("--explicit_target", default="", choices=["", "personal", "team", "both"])
    parser.add_argument("--project_id", default="")
    args = parser.parse_args()

    sender_id = chat_context.actor_id(args.open_id, args.sender_id)
    if not sender_id:
        out(json_fail("missing_sender_id", "缺少 SenderId，不能识别用户。"))
        return
    chat_type = chat_context.normalize_chat_type(args.chat_type)

    if chat_type == "group":
        if args.explicit_target in {"personal", "both"}:
            out(json_fail("personal_scope_not_allowed_in_group", "群聊中不能把 GitHub 评估保存到个人知识库。请私聊我处理个人评估。"))
            return
        group, error = chat_context.resolve_group_context(sender_id, args.chat_id)
        if error:
            out(error)
            return
        team = group["team"]
        out({
            "success": True,
            "chat_type": "group",
            "chat_id": args.chat_id,
            "message_sid": args.message_sid,
            "target": "team",
            "created_by": sender_id,
            "personal_kb": None,
            "team_kb": {
                "owner": team.get("team_kb_owner"),
                "repo": team.get("team_kb_repo"),
                "team_id": group["team_id"],
                "project_id": args.project_id or "general",
            },
            "binding": group["binding"],
        })
        return

    user = sc.users().get(sender_id)
    if not user:
        out(json_fail("user_not_registered", "请先完成个人知识库初始化。"))
        return
    team = sc.teams().get(user.get("team_id", ""))
    target = args.explicit_target or "personal"
    if target in {"team", "both"} and not team:
        out(json_fail("no_team", "你还没有加入团队，不能保存到团队知识库。"))
        return
    out({
        "success": True,
        "chat_type": chat_type or "direct",
        "chat_id": args.chat_id,
        "message_sid": args.message_sid,
        "target": target,
        "created_by": sender_id,
        "personal_kb": {
            "owner": user.get("personal_kb_owner") or user.get("gitea_username"),
            "repo": user.get("personal_kb_repo"),
        },
        "team_kb": ({
            "owner": team.get("team_kb_owner"),
            "repo": team.get("team_kb_repo"),
            "team_id": user.get("team_id"),
            "project_id": args.project_id or "general",
        } if team else None),
    })


if __name__ == "__main__":
    main()
