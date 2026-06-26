#!/usr/bin/env python3
"""
Version check for chat-visualizer-ymind.
Uses __file__ to locate the skill directory — no hardcoded paths.

Output (stdout):
  UPDATE|<local>|<remote>|<skill_dir>|<release_notes_first_3_lines>
  (empty if already up to date or on any error)
"""
import os, sys, urllib.request, json

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
version_file = os.path.join(skill_dir, "VERSION")

if not os.path.exists(version_file):
    sys.exit(0)

local = open(version_file).read().strip()

try:
    resp = urllib.request.urlopen(
        "https://api.github.com/repos/yslenjoy/chat-visualizer-ymind/releases/latest",
        timeout=3,
    )
    data = json.loads(resp.read())
    remote = data["tag_name"].lstrip("v")
    if remote == local:
        sys.exit(0)
    notes = "\n".join((data.get("body") or "").strip().splitlines()[:3])
    print(f"UPDATE|{local}|{remote}|{skill_dir}|{notes}")
except Exception:
    pass
