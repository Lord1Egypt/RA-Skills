#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs

def main():
    jobs = load_jobs().get("jobs", {})
    if not jobs:
        print("No fetch jobs yet.")
        return

    for job in sorted(jobs.values(), key=lambda x: x["created_at"], reverse=True):
        print(f"{job['id']} | {job['title']} | {job['url']}")

if __name__ == "__main__":
    main()
