#!/usr/bin/env python3
"""
prefs.py — Persist and recall user export preferences for export-reply skill.

Preferences are stored in ~/.export_reply_prefs.json

Usage:
    # Read last preferences (returns JSON to stdout)
    python3 prefs.py --action get

    # Save new preferences
    python3 prefs.py --action set \
        --scope full --mode summary --format pdf --path ~/Desktop/

    # Clear preferences
    python3 prefs.py --action clear
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

PREFS_FILE = Path.home() / ".export_reply_prefs.json"


def get_prefs():  # -> Optional[dict]
    if not PREFS_FILE.exists():
        return None
    try:
        data = json.loads(PREFS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def set_prefs(scope: str, mode: str, fmt: str, path: str) -> dict:
    prefs = {
        "scope": scope,
        "mode": mode,
        "format": fmt,
        "path": path,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    PREFS_FILE.write_text(json.dumps(prefs, ensure_ascii=False, indent=2), encoding="utf-8")
    return prefs


def clear_prefs():
    if PREFS_FILE.exists():
        PREFS_FILE.unlink()


def describe_prefs(prefs: dict) -> str:
    """Return human-readable one-line summary of prefs."""
    scope_label = "完整对话" if prefs.get("scope") == "full" else "仅当前回答"
    mode_label  = "精简摘要" if prefs.get("mode")  == "summary" else "原文保留"
    fmt         = prefs.get("format", "?").upper()
    path        = prefs.get("path", "~/Desktop/")
    saved_at    = prefs.get("saved_at", "")
    return f"{scope_label} · {mode_label} · {fmt} → {path}（上次：{saved_at}）"


def main():
    parser = argparse.ArgumentParser(description="Manage export-reply preferences")
    parser.add_argument("--action", choices=["get", "set", "clear"], required=True)
    parser.add_argument("--scope",  help="full | reply")
    parser.add_argument("--mode",   help="raw | summary")
    parser.add_argument("--format", help="md | txt | html | pdf | docx | all")
    parser.add_argument("--path",   help="Output directory or file path")
    args = parser.parse_args()

    if args.action == "get":
        prefs = get_prefs()
        if prefs:
            print(json.dumps(prefs, ensure_ascii=False))
        else:
            print("null")

    elif args.action == "set":
        missing = [f for f in ("scope", "mode", "format", "path") if not getattr(args, f)]
        if missing:
            print(f"ERROR: missing --{missing[0]}", file=sys.stderr)
            sys.exit(1)
        prefs = set_prefs(args.scope, args.mode, args.format, args.path)
        print(f"✅ 偏好已保存：{describe_prefs(prefs)}")

    elif args.action == "clear":
        clear_prefs()
        print("✅ 偏好已清除")


if __name__ == "__main__":
    main()
