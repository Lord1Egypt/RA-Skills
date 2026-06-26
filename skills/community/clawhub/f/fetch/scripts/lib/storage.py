#!/usr/bin/env python3
import json
import os
from datetime import datetime

FETCH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/fetch")
PAGES_DIR = os.path.join(FETCH_DIR, "pages")
JOBS_FILE = os.path.join(FETCH_DIR, "jobs.json")

def ensure_dirs():
    os.makedirs(FETCH_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)

def _safe_load(path, default):
    ensure_dirs()
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default

def _atomic_save(path, data):
    ensure_dirs()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def load_jobs():
    return _safe_load(JOBS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "jobs": {}
    })

def save_jobs(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(JOBS_FILE, data)
