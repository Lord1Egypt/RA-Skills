#!/usr/bin/env python3
"""Write or remove subtopic heartbeat files."""

from __future__ import annotations

import argparse
import json

from clawexpert_common import iso_now, knowledge_dir, load_json, progress_path, save_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--subtopic-id", required=True)
    parser.add_argument("--status")
    parser.add_argument("--search-round", type=int)
    parser.add_argument("--sources-found", type=int)
    parser.add_argument("--sources-saved", type=int)
    parser.add_argument("--last-url")
    parser.add_argument("--last-error")
    parser.add_argument("--node-file", action="append", default=[])
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    path = progress_path(kb, args.slug, args.subtopic_id)

    if args.remove:
        removed = False
        if path.exists():
            path.unlink()
            removed = True
        print(json.dumps({"removed": removed, "path": str(path)}))
        return 0

    data = load_json(path, default={}) or {}
    data.setdefault("subtopic_id", args.subtopic_id)
    data.setdefault("started_at", iso_now())
    if args.status:
        data["status"] = args.status
    if args.search_round is not None:
        data["search_round"] = args.search_round
    if args.sources_found is not None:
        data["sources_found"] = args.sources_found
    if args.sources_saved is not None:
        data["sources_saved"] = args.sources_saved
    if args.last_url:
        data["last_url"] = args.last_url
    if args.last_error:
        data["last_error"] = args.last_error
    if args.node_file:
        existing = list(data.get("node_files", []))
        for item in args.node_file:
            if item not in existing:
                existing.append(item)
        data["node_files"] = existing
    data["updated_at"] = iso_now()

    save_json(path, data)
    print(json.dumps({"path": str(path), "status": data.get("status"), "updated_at": data["updated_at"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
