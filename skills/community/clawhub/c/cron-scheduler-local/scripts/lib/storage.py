#!/usr/bin/env python3
import json
import os
from datetime import datetime

CRON_DIR = os.path.expanduser("~/.openclaw/workspace/memory/cron")
JOBS_FILE = os.path.join(CRON_DIR, "jobs.json")
RUNS_FILE = os.path.join(CRON_DIR, "runs.json")
STATS_FILE = os.path.join(CRON_DIR, "stats.json")

def ensure_dir():
    os.makedirs(CRON_DIR, exist_ok=True)

def _safe_load(path, default):
    ensure_dir()
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default

def _atomic_save(path, data):
    ensure_dir()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def load_jobs():
    now = datetime.now().isoformat()
    return _safe_load(JOBS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "jobs": {}
    })

def save_jobs(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(JOBS_FILE, data)

def load_runs():
    now = datetime.now().isoformat()
    return _safe_load(RUNS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "runs": {}
    })

def save_runs(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(RUNS_FILE, data)

def load_stats():
    return _safe_load(STATS_FILE, {
        "total_jobs_created": 0,
        "total_jobs_paused": 0,
        "total_jobs_resumed": 0,
        "total_runs_completed": 0,
        "last_reviewed_at": None
    })

def save_stats(data):
    _atomic_save(STATS_FILE, data)
