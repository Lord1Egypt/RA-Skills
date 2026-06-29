from __future__ import annotations

import system_config as sc
from utils import json_fail


def normalize_chat_type(value: str) -> str:
    if value in {"group", "direct"}:
        return value
    if value == "p2p":
        return "direct"
    return value or ""


def actor_id(open_id: str = "", sender_id: str = "") -> str:
    return sender_id or open_id


def resolve_group_context(sender_id: str, chat_id: str) -> tuple[dict | None, dict | None]:
    if not chat_id:
        return None, json_fail("missing_chat_id", "OpenClaw 没有传入群聊 chat_id，不能确定团队知识库。")
    binding = sc.chat_bindings().get(chat_id)
    if not binding or not binding.get("enabled", True):
        return None, json_fail("chat_not_bound", "本群还没有绑定团队。请团队管理员先在群里 @我 绑定本群。")
    team_id = binding.get("team_id", "")
    team = sc.teams().get(team_id)
    if not team:
        return None, json_fail("bound_team_not_found", "本群绑定的团队在 system-config 中不存在，请管理员检查绑定。")
    user = sc.users().get(sender_id)
    if not user:
        return None, json_fail("user_not_registered", "请先私聊我完成个人知识库初始化，再在团队群中使用。")
    if user.get("team_id") != team_id or sender_id not in team.get("members", []):
        return None, json_fail("not_team_member", "你不是本群绑定团队的成员，不能操作该团队知识库。")
    return {
        "binding": binding,
        "team_id": team_id,
        "team": team,
        "user": user,
    }, None


def is_team_admin(sender_id: str, team: dict) -> bool:
    return sender_id in team.get("admins", [])
