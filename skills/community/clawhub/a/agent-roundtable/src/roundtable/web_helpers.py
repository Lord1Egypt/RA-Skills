from __future__ import annotations

from typing import Any


def get_display_name_for_participant(participant: str, participants: list[dict[str, Any]]) -> str:
    for item in participants:
        if item.get("profile") == participant or item.get("participant") == participant:
            return str(item.get("display_name") or item.get("profile") or participant)
    return participant


def get_role_for_participant(participant: str, participants: list[dict[str, Any]]) -> str:
    for item in participants:
        if item.get("profile") == participant or item.get("participant") == participant:
            return str(item.get("role") or "")
    return ""


def get_avatar_for_participant(participant: str, participants: list[dict[str, Any]]) -> str:
    # 1. Check for explicit avatar in participant data
    for item in participants:
        if item.get("profile") == participant or item.get("participant") == participant:
            explicit = item.get("avatar", "")
            if explicit:
                return str(explicit)
    if participant == "coordinator":
        return "📋"
    role = get_role_for_participant(participant, participants).lower()
    if "design" in role or "设计" in role:
        return "🎨"
    if "product" in role or "产品" in role:
        return "📦"
    if "engineer" in role or "tech" in role or "技术" in role or "开发" in role:
        return "⚡"
    return "🤖"
