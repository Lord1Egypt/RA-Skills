#!/usr/bin/env python3
"""Collect merge inputs: subtopic nodes, flags, and heartbeat status."""

from __future__ import annotations

import argparse
import json

from clawexpert_common import knowledge_dir, list_subtopic_nodes, load_json, meta_path, topic_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--stall-seconds", type=int, default=600)
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    root = topic_dir(kb, args.slug)
    meta = load_json(meta_path(kb, args.slug), default={}) or {}
    node_files = [str(path) for path in list_subtopic_nodes(root)]

    # Reuse monitor_subtopics without an extra subprocess.
    subtopics = [sub.get("id") for sub in meta.get("subtopics", []) if sub.get("id")]
    flags = {}
    missing_flags = []
    for subtopic_id in subtopics:
        path = root / f"done-{subtopic_id}.flag"
        if path.exists():
            flags[subtopic_id] = load_json(path, default={}) or {}
        else:
            missing_flags.append(subtopic_id)

    summary = {
        "slug": args.slug,
        "subtopic_count": len(subtopics),
        "node_file_count": len(node_files),
        "node_files": node_files,
        "flags": flags,
        "missing_flags": missing_flags,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
