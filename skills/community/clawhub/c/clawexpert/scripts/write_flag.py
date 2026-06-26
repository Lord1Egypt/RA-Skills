#!/usr/bin/env python3
"""Write a subtopic completion flag and optionally remove the heartbeat file."""

from __future__ import annotations

import argparse
import json

from clawexpert_common import flag_path, iso_now, knowledge_dir, progress_path, save_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--subtopic-id", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--sources-added", type=int, default=0)
    parser.add_argument("--node-file", action="append", default=[])
    parser.add_argument("--cleanup-progress", action="store_true")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    path = flag_path(kb, args.slug, args.subtopic_id)
    data = {
        "status": args.status,
        "subtopic_id": args.subtopic_id,
        "sources_added": args.sources_added,
        "node_files": args.node_file,
        "completed_at": iso_now(),
    }
    save_json(path, data)

    progress_removed = False
    if args.cleanup_progress:
        progress = progress_path(kb, args.slug, args.subtopic_id)
        if progress.exists():
            progress.unlink()
            progress_removed = True

    print(json.dumps({"path": str(path), "status": args.status, "progress_removed": progress_removed}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
