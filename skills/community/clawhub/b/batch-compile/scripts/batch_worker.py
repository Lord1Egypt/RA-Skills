from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def source_path(item: dict) -> str:
    return item.get("source_path") or item.get("path") or ""


def result_paths(job: dict) -> set[str]:
    return {r.get("source_path", "") for r in job.get("file_results", []) if r.get("source_path")}


def pending_documents(job: dict) -> list[dict]:
    done = result_paths(job)
    claimed = set((job.get("claimed_files") or {}).keys())
    return [item for item in job.get("document_files", []) if source_path(item) not in done and source_path(item) not in claimed]


def source_context(job: dict) -> dict:
    return {
        "source_id": job.get("source_id", ""),
        "source_type": job.get("source_type", ""),
        "source_url": job.get("source_url", ""),
        "source_ref": job.get("source_ref", ""),
        "source_owner": job.get("source_owner", ""),
        "source_repo": job.get("source_repo", ""),
        "target_kb_owner": job.get("target_kb_owner", ""),
        "target_kb_repo": job.get("target_kb_repo", ""),
        "target_project_id": job.get("target_project_id", ""),
    }


def claim_batch(job_id: str, job: dict, batch: list[dict]) -> str:
    claim_id = sc.new_record_id("claim")
    claims = job.setdefault("claimed_files", {})
    stamp = now_str()
    for item in batch:
        path = source_path(item)
        if path:
            claims[path] = {"claim_id": claim_id, "claimed_at": stamp}
    job["updated_at"] = stamp
    return claim_id


def next_action(job_id: str, job: dict, claim: bool) -> tuple[dict, dict]:
    if job.get("type") == "incremental_compile" and job.get("status") == "pending":
        return {
            "job_id": job_id,
            "action": "execute_incremental_job",
            "skill": "scan_updates",
            "script": "execute_incremental_job.py",
        }, job

    if job.get("status") not in {"running", "pending"}:
        return {"job_id": job_id, "action": "none", "reason": f"status={job.get('status')}"}, job

    batch_size = int(job.get("batch_size", 100))
    pending = pending_documents(job)
    if pending:
        batch = pending[:batch_size]
        claim_id = claim_batch(job_id, job, batch) if claim else ""
        job["next_cursor"] = len(result_paths(job)) + len(job.get("claimed_files", {}))
        return {
            "job_id": job_id,
            "action": "process_document_batch",
            "batch": batch,
            "batch_count": len(batch),
            "claim_id": claim_id,
            "pending_after_claim": max(len(pending) - len(batch), 0),
            **source_context(job),
        }, job

    claimed_count = len(job.get("claimed_files") or {})
    if claimed_count:
        return {
            "job_id": job_id,
            "action": "awaiting_claimed_results",
            "claimed_count": claimed_count,
            "message": "已有文件被领取但尚未写入处理结果，暂不收尾。",
        }, job

    code_files = job.get("code_files", [])
    if code_files and not job.get("codebase_result"):
        return {
            "job_id": job_id,
            "action": "compile_codebase_overview",
            "code_files": len(code_files),
            **source_context(job),
        }, job

    return {
        "job_id": job_id,
        "action": "finalize_job",
        "command": f"python3 scripts/finalize_batch.py --job_id {job_id}",
    }, job


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", default="")
    parser.add_argument("--claim", action="store_true", help="mark returned documents as claimed")
    args = parser.parse_args()

    jobs = sc.jobs()
    candidates = {args.job_id: jobs.get(args.job_id)} if args.job_id else {
        jid: job for jid, job in jobs.items()
        if job.get("type") in {"batch_compile", "incremental_compile"} and job.get("status") in {"pending", "running"}
    }
    for job_id, job in candidates.items():
        if not job:
            continue
        action, updated_job = next_action(job_id, job, args.claim)
        if action.get("action") != "none":
            if args.claim:
                sc.update_json("jobs.json", lambda current: {**current, job_id: updated_job}, default={})
            out({"success": True, **action})
            return
    if args.job_id:
        out(json_fail("job_not_actionable", "该 job 当前没有可执行的下一步。"))
        return
    out({"success": True, "action": "idle"})


if __name__ == "__main__":
    main()
