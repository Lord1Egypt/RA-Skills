#!/usr/bin/env python3
"""
logger.py — Log pipeline events to project research log
Usage: python3 logger.py "<project>" "<message>"
"""

import sys
import os
import datetime

def log(project, message, base_dir=None):
    if base_dir is None:
        base_dir = os.path.expanduser("~/.openclaw/workspace/research-supervisor-pro")

    log_dir = os.path.join(base_dir, "research", project)
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "auto_log.md")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a") as f:
        f.write(f"- [{timestamp}] {message}\n")

    print(f"📝 Logged: {message}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 logger.py \"<project>\" \"<message>\"")
        sys.exit(1)
    log(sys.argv[1], sys.argv[2])
