#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs, save_jobs, load_stats, save_stats

def main():
    parser = argparse.ArgumentParser(description="Pause one job")
    parser.add_argument("--id", required=True)
    args = parser.parse_args()

    data = load_jobs()
    jobs = data.get("jobs", {})

    if args.id not in jobs:
        print(f"Job not found: {args.id}")
        sys.exit(1)

    jobs[args.id]["status"] = "paused"
    jobs[args.id]["updated_at"] = datetime.now().isoformat()
    save_jobs(data)

    stats = load_stats()
    stats["total_jobs_paused"] += 1
    save_stats(stats)

    print(f"✓ Paused {args.id}")
    print(f"  {jobs[args.id]['title']}")

if __name__ == "__main__":
    main()
