#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs

def main():
    data = load_jobs()
    jobs = data.get("jobs", {})

    if not jobs:
        print("No jobs found.")
        return

    for job_id, job in jobs.items():
        print(f"{job_id} | {job['title']} | {job['status']} | next={job.get('next_run_at')}")

if __name__ == "__main__":
    main()
