from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def recompute_counts(job: dict) -> None:
    results = job.get("file_results", [])
    job["processed_documents"] = len([r for r in results if r.get("status") == "success"])
    job["failed_documents"] = len([r for r in results if r.get("status") == "failed"])
    job["skipped_documents"] = len([r for r in results if r.get("status") == "skipped"]) + len(job.get("skipped_files", []))
    job["completed_document_results"] = len(results)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", required=True)
    parser.add_argument("--source_path", required=True)
    parser.add_argument("--status", required=True, choices=["success", "failed", "skipped"])
    parser.add_argument("--page_url", default="")
    parser.add_argument("--message", default="")
    args = parser.parse_args()
    jobs = sc.jobs()
    job = jobs.get(args.job_id)
    if not job:
        out(json_fail("job_not_found", "找不到批量任务。"))
        return

    valid_paths = {item.get("path") or item.get("source_path") for item in job.get("document_files", [])}
    valid_paths.discard(None)
    if valid_paths and args.source_path not in valid_paths:
        out(json_fail("source_path_not_in_job", "该源文件不属于这个 job 的 document_files。"))
        return

    result = {
        "source_path": args.source_path,
        "status": args.status,
        "page_url": args.page_url,
        "message": args.message,
        "time": now_str(),
    }
    results = [r for r in job.get("file_results", []) if r.get("source_path") != args.source_path]
    results.append(result)
    job["file_results"] = results
    claims = job.setdefault("claimed_files", {})
    claims.pop(args.source_path, None)
    recompute_counts(job)
    job["next_cursor"] = len(results) + len(claims)
    job["updated_at"] = now_str()
    sc.update_json("jobs.json", lambda current: {**current, args.job_id: job}, default={})
    out({"success": True, "job": job})


if __name__ == "__main__":
    main()
