from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", required=True)
    parser.add_argument("--processed", type=int, default=0)
    parser.add_argument("--failed", type=int, default=0)
    parser.add_argument("--skipped", type=int, default=0)
    parser.add_argument("--status", default="", choices=["", "running", "completed", "failed", "cancel_requested"])
    args = parser.parse_args()
    jobs = sc.jobs()
    job = jobs.get(args.job_id)
    if not job:
        out(json_fail("job_not_found", "找不到该批量任务。"))
        return
    job["processed_documents"] = job.get("processed_documents", 0) + args.processed
    job["failed_documents"] = job.get("failed_documents", 0) + args.failed
    job["skipped_documents"] = job.get("skipped_documents", 0) + args.skipped
    if args.status:
        job["status"] = args.status
    total = job.get("total_documents", 0)
    if total and job["processed_documents"] >= total and job.get("status") == "running":
        job["status"] = "completed"
    job["updated_at"] = now_str()
    sc.update_json("jobs.json", lambda current: {**current, args.job_id: job}, default={})
    out({"success": True, "job": job})


if __name__ == "__main__":
    main()
