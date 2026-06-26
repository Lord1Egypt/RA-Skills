#!/usr/bin/env python3
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs

def main():
    jobs = list(load_jobs().get("jobs", {}).values())
    active_jobs = [j for j in jobs if j.get("status") == "active" and j.get("next_run_at")]

    if not active_jobs:
        print("No active upcoming jobs.")
        return

    active_jobs.sort(key=lambda x: x["next_run_at"])
    job = active_jobs[0]

    print("Next scheduled job:")
    print(f"  ID: {job['id']}")
    print(f"  Title: {job['title']}")
    print(f"  Next run: {job['next_run_at']}")

if __name__ == "__main__":
    main()
