from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def source_path(item: dict) -> str:
    return item.get("source_path") or item.get("path") or ""


def source_context(job: dict) -> dict:
    return {
        "source_id": job.get("source_id", ""),
        "source_type": job.get("source_type", ""),
        "source_url": job.get("source_url", ""),
        "source_ref": job.get("source_ref", ""),
        "source_owner": job.get("source_owner", ""),
        "source_repo": job.get("source_repo", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", required=True)
    parser.add_argument("--no_claim", action="store_true", help="preview next batch without claiming it")
    args = parser.parse_args()
    jobs = sc.jobs()
    job = jobs.get(args.job_id)
    if not job:
        out(json_fail("job_not_found", "找不到批量任务。"))
        return
    if job.get("status") not in {"running", "pending"}:
        out(json_fail("job_not_running", f"任务状态不是 running/pending：{job.get('status')}"))
        return

    done = {r.get("source_path", "") for r in job.get("file_results", []) if r.get("source_path")}
    claimed = set((job.get("claimed_files") or {}).keys())
    files = job.get("document_files", [])
    pending = [item for item in files if source_path(item) not in done and source_path(item) not in claimed]
    size = int(job.get("batch_size", 100))
    batch = pending[:size]
    claim_id = ""
    if batch and not args.no_claim:
        claim_id = sc.new_record_id("claim")
        claims = job.setdefault("claimed_files", {})
        stamp = now_str()
        for item in batch:
            path = source_path(item)
            if path:
                claims[path] = {"claim_id": claim_id, "claimed_at": stamp}
        job["next_cursor"] = len(done) + len(claims)
        job["updated_at"] = stamp
        sc.update_json("jobs.json", lambda current: {**current, args.job_id: job}, default={})

    out({
        "success": True,
        "job_id": args.job_id,
        "batch": batch,
        "batch_count": len(batch),
        "claim_id": claim_id,
        "pending_after_claim": max(len(pending) - len(batch), 0),
        "claimed_count": len(job.get("claimed_files") or {}),
        "has_more": len(pending) > len(batch),
        **source_context(job),
    })


if __name__ == "__main__":
    main()
