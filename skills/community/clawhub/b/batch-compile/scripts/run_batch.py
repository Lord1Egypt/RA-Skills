from __future__ import annotations

import argparse
import json
from pathlib import Path

import cards
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", required=True)
    parser.add_argument("--confirmed_by", default="", help="OpenClaw SenderId of the user who confirmed the card.")
    parser.add_argument("--batch_size", type=int, default=100)
    args = parser.parse_args()

    tasks = sc.active_tasks()
    task = tasks.get(args.task_id)
    if not task:
        out(json_fail("task_not_found", "找不到待确认的批量编译任务。"))
        return
    if args.confirmed_by and task.get("created_by") != args.confirmed_by:
        out(json_fail("permission_denied", "只有发起该批量编译的人可以确认开始。"))
        return
    scan_file = Path(task["scan_file"])
    if not scan_file.exists():
        out(json_fail("scan_file_not_found", "找不到该任务对应的扫描结果。"))
        return
    scan = json.loads(scan_file.read_text(encoding="utf-8"))
    source_meta = scan.get("source", {})
    source_record = sc.sources().get(task["source_id"], {})
    files = scan.get("files", [])
    document_files = [f for f in files if f.get("action") == "document"]
    code_files = [f for f in files if f.get("action") in {"code_context", "dependency_context"}]
    skipped_files = [f for f in files if f.get("action") == "skip"]

    job_id = sc.new_record_id("job")
    job_record = {
        "type": "batch_compile",
        "status": "running",
        "source_id": task["source_id"],
        "source_type": source_record.get("source_type") or source_meta.get("type", ""),
        "source_label": source_record.get("source_label") or source_meta.get("label") or source_meta.get("repo", ""),
        "source_url": source_record.get("source_url") or source_meta.get("url", ""),
        "source_ref": source_record.get("source_ref") or source_meta.get("ref", ""),
        "source_owner": source_record.get("source_owner") or source_meta.get("owner", ""),
        "source_repo": source_record.get("source_repo") or source_meta.get("repo", ""),
        "latest_commit": source_record.get("last_commit") or source_meta.get("latest_commit", ""),
        "created_by": task["created_by"],
        "chat_type": task.get("chat_type", "direct"),
        "chat_id": task.get("chat_id", ""),
        "source_message_sid": task.get("message_sid", ""),
        "message_thread_id": task.get("message_thread_id", ""),
        "account_id": task.get("account_id", "default"),
        "deliver_to": task.get("deliver_to", {}),
        "target_scope": task["target_scope"],
        "target_team_id": task.get("target_team_id", ""),
        "target_project_id": task.get("target_project_id", ""),
        "target_kb_owner": task["target_kb_owner"],
        "target_kb_repo": task["target_kb_repo"],
        "total_documents": len(document_files),
        "processed_documents": 0,
        "failed_documents": 0,
        "skipped_documents": len(skipped_files),
        "batch_size": args.batch_size,
        "next_cursor": 0,
        "auto_continue": True,
        "execution_mode": "background_worker",
        "worker_required": True,
        "worker_spawn": {},
        "notified": False,
        "notify_status": "not_ready",
        "notify_attempts": 0,
        "notify_last_error": "",
        "document_files": document_files,
        "code_files": code_files,
        "skipped_files": skipped_files,
        "scan_file": str(scan_file),
        "created_at": now_str(),
        "updated_at": now_str(),
    }
    sc.update_json("jobs.json", lambda current: {**current, job_id: job_record}, default={})

    def remove_task(current: dict) -> dict:
        current.pop(args.task_id, None)
        return current

    sc.update_json("active_tasks.json", remove_task, default={})
    out({
        "success": True,
        "job_id": job_id,
        "total_documents": len(document_files),
        "code_context_files": len(code_files),
        "skipped_files": len(skipped_files),
        "execution_mode": "background_worker",
        "worker_required": True,
        "notify_status": "not_ready",
        "message": "批量编译 job 已创建；后续必须派后台 worker 分批生成摘要并保存。",
        "interactive_card": cards.worker_started(job_id, len(document_files), len(code_files)),
    })


if __name__ == "__main__":
    main()
