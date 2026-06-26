#!/usr/bin/env python3
"""Inspect done flags and heartbeat files to find stalled subtopics."""

from __future__ import annotations

import argparse
import json

from clawexpert_common import knowledge_dir, load_json, meta_path, progress_path, topic_dir, utc_now


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--stall-seconds", type=int, default=600)
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    meta = load_json(meta_path(kb, args.slug), default={}) or {}
    root = topic_dir(kb, args.slug)

    subtopics = [sub.get("id") for sub in meta.get("subtopics", []) if sub.get("id")]
    flags = {}
    stalled = []
    active = []
    now = utc_now()

    for subtopic_id in subtopics:
        flag_file = root / f"done-{subtopic_id}.flag"
        if flag_file.exists():
            flags[subtopic_id] = load_json(flag_file, default={}) or {}
            continue

        progress = load_json(progress_path(kb, args.slug, subtopic_id), default={}) or {}
        if not progress:
            continue

        updated_at = progress.get("updated_at")
        age_seconds = None
        if updated_at:
            try:
                ts = updated_at.replace("Z", "+00:00")
                age_seconds = int((now - __import__("datetime").datetime.fromisoformat(ts)).total_seconds())
            except ValueError:
                age_seconds = None

        item = {
            "subtopic_id": subtopic_id,
            "status": progress.get("status", "running"),
            "search_round": progress.get("search_round"),
            "sources_saved": progress.get("sources_saved", 0),
            "last_error": progress.get("last_error"),
            "updated_at": updated_at,
            "age_seconds": age_seconds,
        }
        if age_seconds is not None and age_seconds >= args.stall_seconds:
            stalled.append(item)
        else:
            active.append(item)

    summary = {
        "slug": args.slug,
        "expected": len(subtopics),
        "done": len(flags),
        "missing": [sub for sub in subtopics if sub not in flags],
        "flag_statuses": {sub: data.get("status", "done") for sub, data in flags.items()},
        "active": active,
        "stalled": stalled,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
