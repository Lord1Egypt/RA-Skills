#!/usr/bin/env python3
"""Finalize topic metadata after merge."""

from __future__ import annotations

import argparse
import json

from clawexpert_common import (
    count_formal_nodes,
    count_source_files,
    iso_now,
    knowledge_dir,
    load_json,
    meta_path,
    save_json,
    topic_dir,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--status")
    parser.add_argument("--missing-status", default="timeout")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    root = topic_dir(kb, args.slug)
    meta_file = meta_path(kb, args.slug)
    meta = load_json(meta_file, default=None)
    if meta is None:
        raise SystemExit(f"Missing meta.json: {meta_file}")

    flags = {}
    for sub in meta.get("subtopics", []):
        sub_id = sub.get("id")
        if not sub_id:
            continue
        flag_file = root / f"done-{sub_id}.flag"
        if flag_file.exists():
            flags[sub_id] = load_json(flag_file, default={}) or {}

    flag_statuses = [data.get("status", "done") for data in flags.values()]
    inferred_status = "complete"
    if len(flags) < len(meta.get("subtopics", [])) or any(status != "done" for status in flag_statuses):
        inferred_status = "partial"

    meta["status"] = args.status or inferred_status
    meta["last_updated"] = iso_now()
    meta["source_count"] = count_source_files(root)
    meta["node_count"] = count_formal_nodes(root)

    sessions = meta.get("learning_sessions", [])
    if sessions:
        sessions[-1]["finished"] = iso_now()
        sessions[-1]["sources_added"] = sum(int(item.get("sources_added", 0)) for item in flags.values())

    for sub in meta.get("subtopics", []):
        sub_id = sub.get("id")
        flag = flags.get(sub_id)
        if flag:
            sub["status"] = flag.get("status", "done")
            sub["sources_added"] = int(flag.get("sources_added", 0))
        else:
            sub["status"] = args.missing_status

    save_json(meta_file, meta)
    print(json.dumps({
        "slug": args.slug,
        "status": meta["status"],
        "source_count": meta["source_count"],
        "node_count": meta["node_count"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
