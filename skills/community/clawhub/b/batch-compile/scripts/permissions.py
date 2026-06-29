from __future__ import annotations

import system_config as sc


def check_batch_permission(
    open_id: str,
    target_scope: str,
    target_kb_owner: str,
    target_kb_repo: str,
    target_team_id: str,
    target_project_id: str,
    source_type: str,
) -> tuple[bool, str]:
    user = sc.users().get(open_id)
    if not user:
        return False, "user_not_registered"

    if target_scope == "personal":
        if user.get("personal_kb_owner") != target_kb_owner or user.get("personal_kb_repo") != target_kb_repo:
            return False, "personal_kb_mismatch"
        return True, ""

    if target_scope != "team":
        return False, "bad_target_scope"

    team_id = target_team_id or user.get("team_id", "")
    teams = sc.teams()
    team = teams.get(team_id)
    if not team:
        return False, "team_not_found"
    if user.get("team_id") != team_id or open_id not in team.get("members", []):
        return False, "not_team_member"
    if team.get("team_kb_owner") != target_kb_owner or team.get("team_kb_repo") != target_kb_repo:
        return False, "team_kb_mismatch"
    project_id = target_project_id or "general"
    if project_id and project_id not in team.get("projects", {}):
        return False, "project_not_found"
    if source_type in {"gitea_repo", "obsidian_git_repo"} and open_id not in team.get("admins", []):
        return False, "team_source_requires_admin"
    return True, ""
