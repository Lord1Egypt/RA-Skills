#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "music_skill.py"

def run(*args: str):
    result = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def main():
    scan = run("scan")
    assert "apps" in scan and isinstance(scan["apps"], list)

    rec = run("recommend", "适合写代码的音乐", "--top-k", "2")
    assert len(rec["suggestions"]) == 2

    search = run("search", "周杰伦 稻香")
    assert "query" in search and search["query"] == "周杰伦 稻香"

    if scan.get("os") != "macos":
        ctrl = run("control", "--app", "spotify", "--action", "status")
        assert ctrl["ok"] is False

    print(json.dumps({
        "scan_apps": len(scan["apps"]),
        "recommendation_count": len(rec["suggestions"]),
        "search_method": search.get("method"),
        "has_osascript": scan.get("has_osascript"),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
