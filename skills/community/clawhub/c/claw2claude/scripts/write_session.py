#!/usr/bin/env python3
"""Safely write the session state file, avoiding shell variable interpolation risks.
Usage: write_session.py <session_file> <session_id> <mode> <project_path>
"""
import sys
import json
import os
from datetime import datetime

if len(sys.argv) < 5:
    print("Usage: write_session.py <session_file> <session_id> <mode> <project_path>", file=sys.stderr)
    sys.exit(1)

session_file = sys.argv[1]
session_id   = sys.argv[2]
mode         = sys.argv[3]
project_path = sys.argv[4]

data = {
    "session_id":   session_id,
    "mode":         mode,
    "project_path": project_path,
    "updated_at":   datetime.now().isoformat(),
}

tmp = session_file + ".tmp"
try:
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, session_file)  # Atomic replace — prevents partial write from corrupting the file
except OSError as e:
    # Clean up the temp file if the atomic replace failed
    try:
        os.unlink(tmp)
    except OSError:
        pass
    print(f"⚠️  Could not write session file: {e}", file=sys.stderr)
    sys.exit(1)
