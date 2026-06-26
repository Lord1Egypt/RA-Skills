#!/usr/bin/env python3
import json
import os
from datetime import datetime

CRON_DIR = os.path.expanduser("~/.openclaw/workspace/memory/cron")
JOBS_FILE = os.path.join(CRON_DIR, "jobs.json")
RUNS_FILE = os.path.join(CRON_DIR, "runs.json")
STATS_FILE = os.path.join(CRON_DIR, "stats.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(CRON_DIR, exist_ok=True)
    now = datetime.now().isoformat()

    write_json_if_missing(JOBS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "jobs": {}
    })

    write_json_if_missing(RUNS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "runs": {}
    })

    write_json_if_missing(STATS_FILE, {
        "total_jobs_created": 0,
        "total_jobs_paused": 0,
        "total_jobs_resumed": 0,
        "total_runs_completed": 0,
        "last_reviewed_at": None
    })

    print("✓ Cron storage initialized")
    print(f"  {JOBS_FILE}")
    print(f"  {RUNS_FILE}")
    print(f"  {STATS_FILE}")

if __name__ == "__main__":
    main()
