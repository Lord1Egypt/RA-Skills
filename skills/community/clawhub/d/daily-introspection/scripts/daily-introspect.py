#!/usr/bin/env python3
"""
daily-introspection: Daily self-introspection script for OpenClaw agent
Reads daily conversation log, identifies mistakes, extracts improvements
Includes daily log + .learnings records + proactive mechanism check
"""

import os
import sys
import argparse
from datetime import datetime

def get_daily_log_path(date_str):
    """Get path to daily log file"""
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    return os.path.join(workspace, f"memory/{date_str}.md")

def get_learning_files():
    """Get all .learnings files"""
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    learnings_dir = os.path.join(workspace, ".learnings")
    files = ["LEARNINGS.md", "ERRORS.md", "FEATURE_REQUESTS.md"]
    result = {}
    for f in files:
        path = os.path.join(learnings_dir, f)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fobj:
                result[f] = fobj.read()
        else:
            result[f] = None
    return result

def get_proactive_checks():
    """Check proactive mechanism files status"""
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    checks = {}
    # Check key proactive files
    files_to_check = [
        "SESSION-STATE.md",
        "HEARTBEAT.md",
        "memory/working-buffer.md"
    ]
    for f in files_to_check:
        path = os.path.join(workspace, f)
        checks[f] = os.path.exists(path)
    return checks

def get_private_data_dir():
    """Get private data directory (create if missing)"""
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    private_dir = os.path.join(workspace, ".daily-introspection")
    if not os.path.exists(private_dir):
        os.makedirs(private_dir)
    return private_dir

def read_daily_log(date_str):
    """Read daily conversation log"""
    path = get_daily_log_path(date_str)
    if not os.path.exists(path):
        print(f"[WARN] Daily log not found: {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description='Daily self-introspection')
    parser.add_argument('--date', help='Date for introspection (YYYY-MM-DD)')
    args = parser.parse_args()

    # Use today if no date specified
    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    print(f"[INFO] Starting daily introspection for {date_str}")

    # Ensure private dir exists
    private_dir = get_private_data_dir()
    print(f"[INFO] Private data directory: {private_dir}")

    # Read daily log
    log_content = read_daily_log(date_str)
    if log_content is None:
        print("[ERROR] No daily log available, exiting")
        sys.exit(1)

    # Read learning files
    learning_content = get_learning_files()
    for name, content in learning_content.items():
        if content:
            print(f"[INFO] Read {len(content)} bytes from .learnings/{name}")
        else:
            print(f"[WARN] .learnings/{name} not found or empty")

    # Check proactive mechanism
    proactive_checks = get_proactive_checks()
    for name, exists in proactive_checks.items():
        print(f"[INFO] Proactive file {name}: {'EXISTS' if exists else 'MISSING'}")

    # The actual LLM analysis happens via OpenClaw tool calling
    # This script collects all sources, LLM will generate introspection content

    print(f"[INFO] Read {len(log_content)} bytes from daily log")
    print("[INFO] All sources collected, ready for LLM introspection analysis")

if __name__ == "__main__":
    main()
