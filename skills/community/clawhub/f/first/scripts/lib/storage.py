#!/usr/bin/env python3
import json
import os
import uuid
from datetime import datetime

STORAGE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/firstprinciples")
CASES_PATH = os.path.join(STORAGE_DIR, "cases.json")
EXPORT_DIR = os.path.join(STORAGE_DIR, "exports")
PATTERNS_PATH = os.path.join(STORAGE_DIR, "patterns.md")
CASE_INDEX_PATH = os.path.join(STORAGE_DIR, "case_index.md")

def now_iso():
    return datetime.utcnow().isoformat()

def ensure_storage():
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(EXPORT_DIR, exist_ok=True)

    if not os.path.exists(CASES_PATH):
        data = {
            "metadata": {
                "version": "1.1.0",
                "created_at": now_iso(),
                "last_updated": now_iso()
            },
            "cases": {}
        }
        save_cases(data)

    if not os.path.exists(PATTERNS_PATH):
        with open(PATTERNS_PATH, "w", encoding="utf-8") as f:
            f.write("# Promoted Reasoning Patterns\n\n")

    if not os.path.exists(CASE_INDEX_PATH):
        with open(CASE_INDEX_PATH, "w", encoding="utf-8") as f:
            f.write("# Case Index\n\n")

    return CASES_PATH

def load_cases():
    ensure_storage()
    with open(CASES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cases(data):
    os.makedirs(STORAGE_DIR, exist_ok=True)
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = now_iso()
    with open(CASES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_case_id():
    return "FP-" + uuid.uuid4().hex[:6].upper()

def append_case_index(case):
    ensure_storage()
    line = f"- {case['id']} | {case['title']} | score={case.get('score', {}).get('overall')} | promotion={case.get('promotion_status', 'none')} | created={case.get('created_at')}\n"
    with open(CASE_INDEX_PATH, "a", encoding="utf-8") as f:
        f.write(line)

def append_promoted_pattern(case):
    ensure_storage()
    candidate = (case.get("reusable_pattern_candidate") or "").strip()
    if not candidate:
        return False
    entry = []
    entry.append(f"## {case['id']} — {case['title']}")
    entry.append(f"- Pattern: {candidate}")
    entry.append(f"- Source score: {case.get('score', {}).get('overall')}")
    entry.append(f"- Created: {case.get('created_at')}")
    entry.append("")
    with open(PATTERNS_PATH, "a", encoding="utf-8") as f:
        f.write("\n".join(entry) + "\n")
    return True
