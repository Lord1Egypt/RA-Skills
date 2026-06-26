"""
Poll running jobs and print status updates.

Usage:
    python poll_jobs.py                    # poll all running jobs
    python poll_jobs.py --project_id 154   # filter by project
    python poll_jobs.py --interval 30      # check every 30 seconds
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime


def get_jobs(status_flag: str | None = None) -> list[dict]:
    """Get job list as JSON."""
    cmd = ["bohr", "job", "list", "-n", "20", "--json"]
    if status_flag:
        cmd.append(status_flag)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []


def format_status(status: str) -> str:
    icons = {
        "Running": "RUN",
        "Finished": "OK ",
        "Failed": "ERR",
        "Pending": "...",
        "Scheduling": "...",
    }
    return icons.get(status, status)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Poll Bohrium job status")
    parser.add_argument("--interval", type=int, default=60, help="Poll interval in seconds")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    while True:
        now = datetime.now().strftime("%H:%M:%S")
        jobs = get_jobs("-r")  # running only
        pending = get_jobs("-p")  # pending
        all_active = jobs + pending

        if not all_active:
            print(f"[{now}] No active jobs.")
            if args.once:
                break
            time.sleep(args.interval)
            continue

        print(f"\n[{now}] Active jobs: {len(all_active)}")
        print(f"  {'ID':<12} {'Status':<6} {'Name':<30}")
        print(f"  {'-'*12} {'-'*6} {'-'*30}")
        for job in all_active:
            job_id = job.get("jobId", job.get("id", "?"))
            status = format_status(job.get("status", "?"))
            name = job.get("jobName", job.get("name", "?"))[:30]
            print(f"  {job_id:<12} {status:<6} {name}")

        if args.once:
            break

        print(f"  Next check in {args.interval}s... (Ctrl+C to stop)")
        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped.")
            break


if __name__ == "__main__":
    main()
