from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


TERMINAL_STATUSES = {"completed", "partial", "failed", "cancelled", "timed_out"}


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def source_label(job: dict) -> str:
    return job.get("source_label") or job.get("source_repo") or job.get("source_url") or job.get("source_id", "")


def result_summary(job: dict) -> str:
    total = int(job.get("total_documents", 0) or 0)
    success_count = int(job.get("processed_documents", 0) or 0)
    failed_count = int(job.get("failed_documents", 0) or 0)
    skipped_count = int(job.get("skipped_documents", 0) or 0)
    status = job.get("status", "")
    failed = [r.get("source_path", "") for r in job.get("file_results", []) if r.get("status") == "failed"]
    lines = [
        "batch_compile 已完成" if status in {"completed", "partial"} else f"batch_compile 状态：{status}",
        "",
        f"资料源：{source_label(job)}",
        f"Job：{job.get('job_id', '')}",
        f"状态：{status}",
        f"成功：{success_count}/{total}",
        f"失败：{failed_count}",
        f"跳过：{skipped_count}",
    ]
    if failed:
        preview = "、".join(path for path in failed[:8] if path)
        if len(failed) > 8:
            preview += f" 等 {len(failed)} 个文件"
        lines.append(f"失败文件：{preview}")
    if job.get("target_kb_owner") and job.get("target_kb_repo"):
        lines.append(f"目标知识库：{job.get('target_kb_owner')}/{job.get('target_kb_repo')}")
    return "\n".join(lines)


def pending_notifications(jobs: dict) -> list[dict]:
    items = []
    for job_id, job in jobs.items():
        if job.get("type") not in {"batch_compile", "incremental_compile"}:
            continue
        if job.get("status") not in TERMINAL_STATUSES:
            continue
        if job.get("notified"):
            continue
        deliver_to = job.get("deliver_to") or {}
        targets = deliver_to.get("targets") or []
        target = deliver_to.get("target")
        if target and target not in targets:
            targets.insert(0, target)
        targets = [item for item in targets if item]
        if not targets:
            continue
        items.append({
            "job_id": job_id,
            "target": targets[0],
            "targets": targets,
            "channel": deliver_to.get("channel", "feishu"),
            "chat_type": deliver_to.get("chat_type", ""),
            "thread_id": deliver_to.get("thread_id", ""),
            "account_id": deliver_to.get("account_id", "default"),
            "message": result_summary({**job, "job_id": job_id}),
        })
    return items


def mark_sent(job_id: str) -> None:
    def mutate(current: dict) -> dict:
        job = current.get(job_id)
        if not job:
            raise KeyError(job_id)
        job["notified"] = True
        job["notify_status"] = "sent"
        job["notified_at"] = now_str()
        job["updated_at"] = now_str()
        current[job_id] = job
        return current

    sc.update_json("jobs.json", mutate, default={})


def mark_failed(job_id: str, error: str) -> None:
    def mutate(current: dict) -> dict:
        job = current.get(job_id)
        if not job:
            raise KeyError(job_id)
        job["notify_status"] = "failed"
        job["notify_attempts"] = int(job.get("notify_attempts", 0) or 0) + 1
        job["notify_last_error"] = error
        job["updated_at"] = now_str()
        current[job_id] = job
        return current

    sc.update_json("jobs.json", mutate, default={})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mark_sent", action="store_true")
    parser.add_argument("--mark_failed", action="store_true")
    parser.add_argument("--job_id", default="")
    parser.add_argument("--error", default="")
    args = parser.parse_args()

    if args.mark_sent:
        if not args.job_id:
            out(json_fail("missing_job_id", "标记通知成功必须提供 --job_id。"))
            return
        try:
            mark_sent(args.job_id)
        except KeyError:
            out(json_fail("job_not_found", "找不到 job。"))
            return
        out({"success": True, "job_id": args.job_id, "notified": True})
        return

    if args.mark_failed:
        if not args.job_id:
            out(json_fail("missing_job_id", "标记通知失败必须提供 --job_id。"))
            return
        try:
            mark_failed(args.job_id, args.error)
        except KeyError:
            out(json_fail("job_not_found", "找不到 job。"))
            return
        out({"success": True, "job_id": args.job_id, "notify_status": "failed"})
        return

    items = pending_notifications(sc.jobs())
    out({"success": True, "pending_count": len(items), "notifications": items})


if __name__ == "__main__":
    main()
