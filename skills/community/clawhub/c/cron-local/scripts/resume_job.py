#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs, save_jobs, load_stats, save_stats
from lib.schedule import compute_next_run

def main():
    parser = argparse.ArgumentParser(description="Resume one job")
    parser.add_argument("--id", required=True)
    args = parser.parse_args()

    data = load_jobs()
    jobs = data.get("jobs", {})

    if args.id not in jobs:
        print(f"Job not found: {args.id}")
        sys.exit(1)

    job = jobs[args.id]
    job["status"] = "active"
    job["next_run_at"] = compute_next_run(
        schedule_type=job["schedule_type"],
        time_of_day=job.get("time_of_day"),
        days_of_week=job.get("days_of_week"),
        day_of_month=job.get("day_of_month"),
        interval=job.get("interval")
    ).isoformat()
    job["updated_at"] = datetime.now().isoformat()
    save_jobs(data)

    stats = load_stats()
    stats["total_jobs_resumed"] += 1
    save_stats(stats)

    print(f"✓ Resumed {args.id}")
    print(f"  Next run: {job['next_run_at']}")

if __name__ == "__main__":
    main()
