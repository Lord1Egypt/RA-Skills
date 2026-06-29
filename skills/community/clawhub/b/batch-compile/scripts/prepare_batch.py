from __future__ import annotations

import argparse
import json
from pathlib import Path

import cards
import chat_context
import source_registry
import system_config as sc
import permissions
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def find_existing_source(record: dict) -> tuple[str, dict]:
    for source_id, old in sc.sources().items():
        same = (
            old.get("source_url") == record.get("source_url")
            and old.get("target_kb_owner") == record.get("target_kb_owner")
            and old.get("target_kb_repo") == record.get("target_kb_repo")
            and old.get("target_project_id", "") == record.get("target_project_id", "")
        )
        if same:
            return source_id, dict(old)
    return "", {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", default="", help="Backward-compatible alias for SenderId.")
    parser.add_argument("--sender_id", default="", help="OpenClaw SenderId: the message sender open_id.")
    parser.add_argument("--chat_type", default="", help="OpenClaw ChatType: direct/group.")
    parser.add_argument("--chat_id", default="", help="OpenClaw GroupSubject in group chats.")
    parser.add_argument("--message_sid", default="", help="OpenClaw MessageSid for audit.")
    parser.add_argument("--message_thread_id", default="", help="OpenClaw MessageThreadId, if any.")
    parser.add_argument("--account_id", default="default", help="OpenClaw AccountId.")
    parser.add_argument("--scan_file", required=True, help="scan_source.py 输出 JSON 文件")
    parser.add_argument("--target_scope", default="", choices=["", "personal", "team"])
    parser.add_argument("--target_kb_owner", default="")
    parser.add_argument("--target_kb_repo", default="")
    parser.add_argument("--target_team_id", default="")
    parser.add_argument("--target_project_id", default="")
    parser.add_argument("--source_type", default="")
    parser.add_argument("--auto_update", default="")
    args = parser.parse_args()

    sender_id = chat_context.actor_id(args.open_id, args.sender_id)
    if not sender_id:
        out(json_fail("missing_sender_id", "缺少 SenderId，不能识别操作者。"))
        return

    scan_path = Path(args.scan_file)
    if not scan_path.exists():
        out(json_fail("scan_file_not_found", f"找不到扫描结果：{scan_path}"))
        return
    scan = json.loads(scan_path.read_text(encoding="utf-8"))
    if not scan.get("success"):
        out(json_fail("bad_scan_result", "扫描结果不是成功状态。"))
        return

    source = scan["source"]
    source_type = args.source_type or source.get("type") or "gitea_repo"
    chat_type = chat_context.normalize_chat_type(args.chat_type)
    binding = None
    if chat_type == "group":
        if args.target_scope and args.target_scope != "team":
            out(json_fail("personal_scope_not_allowed_in_group", "群聊中不能把批量资料源导入个人知识库。请私聊我处理个人资料。"))
            return
        group, error = chat_context.resolve_group_context(sender_id, args.chat_id)
        if error:
            out(error)
            return
        team = group["team"]
        binding = group["binding"]
        target_scope = "team"
        target_team_id = group["team_id"]
        target_project_id = args.target_project_id
        target_kb_owner = team.get("team_kb_owner", "")
        target_kb_repo = team.get("team_kb_repo", "")
        if args.target_team_id and args.target_team_id != target_team_id:
            out(json_fail("group_target_mismatch", "目标团队必须是本群绑定的团队。"))
            return
        if args.target_kb_owner and args.target_kb_owner != target_kb_owner:
            out(json_fail("group_target_mismatch", "目标知识库 owner 必须是本群绑定团队的知识库 owner。"))
            return
        if args.target_kb_repo and args.target_kb_repo != target_kb_repo:
            out(json_fail("group_target_mismatch", "目标知识库 repo 必须是本群绑定团队的知识库 repo。"))
            return
    else:
        user = sc.users().get(sender_id, {})
        if not user:
            out(json_fail("user_not_registered", "请先完成个人知识库初始化。"))
            return
        target_scope = args.target_scope
        target_team_id = args.target_team_id
        target_project_id = args.target_project_id
        target_kb_owner = args.target_kb_owner
        target_kb_repo = args.target_kb_repo
        if not target_scope:
            team = sc.teams().get(user.get("team_id", ""))
            data = json_fail("missing_target_scope", "私聊批量编译必须先确认导入个人知识库还是团队知识库。")
            data["interactive_card"] = cards.target_choice(team.get("team_name", "") if team else "")
            out(data)
            return
        if target_scope == "personal":
            target_kb_owner = target_kb_owner or user.get("personal_kb_owner") or user.get("gitea_username", "")
            target_kb_repo = target_kb_repo or user.get("personal_kb_repo", "")
        elif target_scope == "team":
            team = sc.teams().get(target_team_id or user.get("team_id", ""), {})
            target_team_id = target_team_id or user.get("team_id", "")
            target_kb_owner = target_kb_owner or team.get("team_kb_owner", "")
            target_kb_repo = target_kb_repo or team.get("team_kb_repo", "")
        if not target_kb_owner or not target_kb_repo:
            out(json_fail("missing_target_kb", "缺少目标知识库 owner/repo。"))
            return

    if target_scope == "team" and not target_project_id:
        team = sc.teams().get(target_team_id or sc.users().get(sender_id, {}).get("team_id", ""), {})
        project_items = []
        for project_id, project in (team.get("projects") or {}).items():
            project_items.append({
                "project_id": project_id,
                "name": project.get("name", project_id),
                "brief": project.get("description", ""),
            })
        data = json_fail("missing_target_project", "团队批量编译必须先确认资料所属项目。")
        data["interactive_card"] = cards.project_choice(project_items, sender_id in team.get("admins", []))
        out(data)
        return

    allowed, reason = permissions.check_batch_permission(
        sender_id,
        target_scope,
        target_kb_owner,
        target_kb_repo,
        target_team_id,
        target_project_id,
        source_type,
    )
    if not allowed:
        out(json_fail("permission_denied", reason))
        return
    user = sc.users().get(sender_id, {})
    resolved_team_id = target_team_id or (user.get("team_id", "") if target_scope == "team" else "")
    resolved_project_id = target_project_id or ("general" if target_scope == "team" else "")
    if args.auto_update:
        auto_update = args.auto_update.lower() == "true"
    else:
        auto_update = source_type in {"gitea_repo", "obsidian_git_repo"}
    record = {
        "source_type": source_type,
        "source_label": source.get("label") or source.get("repo") or source.get("url"),
        "source_url": source.get("url"),
        "source_owner": source.get("owner"),
        "source_repo": source.get("repo"),
        "source_ref": source.get("ref", ""),
        "last_commit": source.get("latest_commit", ""),
        "target_scope": target_scope,
        "target_team_id": resolved_team_id,
        "target_project_id": resolved_project_id,
        "target_kb_owner": target_kb_owner,
        "target_kb_repo": target_kb_repo,
        "created_by": sender_id,
        "source_chat_id": args.chat_id if chat_type == "group" else "",
        "source_message_sid": args.message_sid,
        "enabled": True,
        "auto_update": auto_update,
        "scan_mode": "schedule_and_manual",
        "webhook_enabled": False,
        "last_status": "pending_initial_compile",
        "created_at": now_str(),
        "last_scan_result": {"stats": scan.get("stats", {})},
    }
    existing_source_id, previous_source_record = find_existing_source(record)
    source_id = source_registry.add_source(record)

    task_id = sc.new_record_id("task")
    task_record = {
        "type": "batch_compile_confirm",
        "source_id": source_id,
        "source_was_existing": bool(existing_source_id),
        "previous_source_record": previous_source_record,
        "created_by": sender_id,
        "chat_type": chat_type or "direct",
        "chat_id": args.chat_id if chat_type == "group" else "",
        "message_sid": args.message_sid,
        "message_thread_id": args.message_thread_id,
        "account_id": args.account_id or "default",
        "deliver_to": {
            "channel": "feishu",
            "target": args.chat_id if chat_type == "group" else sender_id,
            "targets": [args.chat_id if chat_type == "group" else sender_id],
            "chat_type": chat_type or "direct",
            "thread_id": args.message_thread_id,
            "account_id": args.account_id or "default",
        },
        "target_scope": target_scope,
        "target_team_id": resolved_team_id,
        "target_project_id": resolved_project_id,
        "target_kb_owner": target_kb_owner,
        "target_kb_repo": target_kb_repo,
        "scan_file": str(scan_path),
        "created_at": now_str(),
    }
    sc.update_json("active_tasks.json", lambda current: {**current, task_id: task_record}, default={})
    out({
        "success": True,
        "source_id": source_id,
        "task_id": task_id,
        "stats": scan.get("stats", {}),
        "chat_type": chat_type or "direct",
        "binding": binding,
        "target_scope": target_scope,
        "target_team_id": resolved_team_id,
        "target_project_id": resolved_project_id,
        "target_kb_owner": target_kb_owner,
        "target_kb_repo": target_kb_repo,
        "interactive_card": cards.preview_confirm(
            task_id,
            record["source_label"] or source_id,
            scan.get("stats", {}),
            target_kb_owner,
            target_kb_repo,
            auto_update,
        ),
    })


if __name__ == "__main__":
    main()
