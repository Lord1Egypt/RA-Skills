from __future__ import annotations

import argparse
import json
from pathlib import Path

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def source_path(item: dict) -> str:
    return item.get("source_path") or item.get("path") or ""


def validate_finished(job: dict, requested_status: str) -> tuple[bool, dict, str]:
    if requested_status in {"cancelled", "failed", "timed_out"}:
        return True, {}, requested_status

    doc_paths = [source_path(item) for item in job.get("document_files", []) if source_path(item)]
    result_by_path = {r.get("source_path", ""): r for r in job.get("file_results", []) if r.get("source_path")}
    missing = [path for path in doc_paths if path not in result_by_path]
    claimed = sorted((job.get("claimed_files") or {}).keys())
    if missing or claimed:
        return False, {
            "missing_results": missing,
            "claimed_files": claimed,
            "missing_count": len(missing),
            "claimed_count": len(claimed),
        }, requested_status

    if job.get("code_files") and not job.get("codebase_result"):
        return False, {"codebase_pending": True, "code_files": len(job.get("code_files", []))}, requested_status

    failed = [r for r in result_by_path.values() if r.get("status") == "failed"]
    if failed and requested_status == "completed":
        return True, {"auto_status": "partial", "failed_count": len(failed)}, "partial"
    return True, {}, requested_status


def load_scan_metadata(job: dict, scan_file_arg: str) -> tuple[dict, str]:
    scan_file = scan_file_arg or job.get("scan_file", "")
    fingerprints = {}
    latest_commit = job.get("latest_commit", "") or job.get("current_commit", "")
    if scan_file and Path(scan_file).exists():
        try:
            scan = json.loads(Path(scan_file).read_text(encoding="utf-8"))
            fingerprints = scan.get("current_fingerprints", {})
            latest_commit = (scan.get("source") or {}).get("latest_commit", "") or latest_commit
        except json.JSONDecodeError:
            fingerprints = {}
    if not fingerprints:
        fingerprints = job.get("current_fingerprints", {})
    return fingerprints, latest_commit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", required=True)
    parser.add_argument("--scan_file", default="")
    parser.add_argument("--status", default="completed", choices=["completed", "partial", "failed", "cancelled", "timed_out"])
    args = parser.parse_args()

    jobs = sc.jobs()
    job = jobs.get(args.job_id)
    if not job:
        out(json_fail("job_not_found", "找不到批量任务。"))
        return

    ok, detail, final_status = validate_finished(job, args.status)
    if not ok:
        data = json_fail("job_not_finished", "任务还有未完成的文件或代码总览，不能收尾。")
        data.update(detail)
        out(data)
        return

    source_id = job.get("source_id", "")
    fingerprints, latest_commit = load_scan_metadata(job, args.scan_file)
    now = now_str()
    should_write_fingerprints = final_status in {"completed", "partial"}

    def mutate_sources(current: dict) -> dict:
        if source_id and source_id in current:
            src = current[source_id]
            if should_write_fingerprints and fingerprints:
                src["file_fingerprints"] = fingerprints
            if should_write_fingerprints and latest_commit:
                src["last_commit"] = latest_commit
            src["last_status"] = final_status
            src["last_scan_time"] = now
            if final_status in {"completed", "partial"}:
                src["last_success_time"] = now
            current[source_id] = src
        return current

    def mutate_jobs(current: dict) -> dict:
        job["status"] = final_status
        job["updated_at"] = now
        if final_status in {"completed", "partial", "failed", "cancelled", "timed_out"}:
            job.setdefault("notified", False)
            if not job.get("notified"):
                deliver_to = job.get("deliver_to", {}) or {}
                job["notify_status"] = "pending" if deliver_to.get("target") or deliver_to.get("targets") else "no_target"
        if detail:
            job["finalize_note"] = detail
        current[args.job_id] = job
        return current

    sc.update_json("sources.json", mutate_sources, default={})
    sc.update_json("jobs.json", mutate_jobs, default={})
    out({
        "success": True,
        "job": job,
        "status": final_status,
        "fingerprints_written": bool(should_write_fingerprints and fingerprints),
        **detail,
    })


if __name__ == "__main__":
    main()
