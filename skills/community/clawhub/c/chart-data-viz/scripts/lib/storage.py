#!/usr/bin/env python3
import json
import os
from datetime import datetime

CHART_DIR = os.path.expanduser("~/.openclaw/workspace/memory/chart")
OUTPUT_DIR = os.path.join(CHART_DIR, "output")
CHARTS_FILE = os.path.join(CHART_DIR, "charts.json")

def ensure_dir():
    os.makedirs(CHART_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

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

def load_charts():
    return _safe_load(CHARTS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "charts": {}
    })

def save_charts(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(CHARTS_FILE, data)
