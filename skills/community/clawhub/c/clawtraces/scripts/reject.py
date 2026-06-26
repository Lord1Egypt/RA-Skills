#!/usr/bin/env python3
# FILE_META
# INPUT:  session_id + reason pairs
# OUTPUT: manifest.json updates + trajectory file deletions
# POS:    skill scripts — utility, depends on lib/paths.py
# MISSION: Mark sessions as rejected and clean up trajectory files.
"""Reject sessions and record them in manifest to avoid re-processing.

Usage:
    python reject.py --output-dir PATH --session SESSION_ID --reason "reason"
    python reject.py --output-dir PATH --sessions 'id1:reason1' 'id2:reason2'
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

from lib.paths import get_default_output_dir

DEFAULT_OUTPUT_DIR = get_default_output_dir()
MANIFEST_FILENAME = "manifest.json"


def load_manifest(output_dir: str) -> dict:
    manifest_path = os.path.join(output_dir, MANIFEST_FILENAME)
    if os.path.isfile(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"submitted": {}, "rejected": {}}


def save_manifest(output_dir: str, manifest: dict):
    """Save manifest (atomic write via tmp+rename)."""
    manifest_path = os.path.join(output_dir, MANIFEST_FILENAME)
    tmp_path = manifest_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, manifest_path)


def reject_sessions(output_dir: str, rejections: list[tuple[str, str]]) -> int:
    """Reject sessions: record in manifest and delete trajectory files.

    Args:
        output_dir: Path to output directory containing manifest and trajectories
        rejections: List of (session_id, reason) tuples

    Returns:
        Number of sessions rejected
    """
    manifest = load_manifest(output_dir)
    manifest.setdefault("rejected", {})
    count = 0

    for session_id, reason in rejections:
        # Record in manifest
        manifest["rejected"][session_id] = {
            "rejected_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
        }

        # Delete trajectory and stats files if they exist
        for suffix in (".trajectory.json", ".stats.json"):
            path = os.path.join(output_dir, f"{session_id}{suffix}")
            if os.path.isfile(path):
                os.remove(path)

        count += 1

    save_manifest(output_dir, manifest)
    return count


def main():
    parser = argparse.ArgumentParser(description="Reject sessions and record in manifest")
    parser.add_argument("--output-dir", "-o", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--session", "-s", help="Single session ID to reject")
    parser.add_argument("--reason", "-r", default="", help="Rejection reason (used with --session)")
    parser.add_argument("--sessions", nargs="+", metavar="ID:REASON",
                        help="Multiple rejections as 'session_id:reason' pairs")
    args = parser.parse_args()

    rejections: list[tuple[str, str]] = []

    if args.session:
        rejections.append((args.session, args.reason))

    if args.sessions:
        for item in args.sessions:
            if ":" in item:
                sid, reason = item.split(":", 1)
                rejections.append((sid.strip(), reason.strip()))
            else:
                rejections.append((item.strip(), ""))

    if not rejections:
        print("No sessions to reject. Use --session or --sessions.", file=sys.stderr)
        sys.exit(1)

    count = reject_sessions(args.output_dir, rejections)
    print(json.dumps({"rejected_count": count}, indent=2))


if __name__ == "__main__":
    main()
