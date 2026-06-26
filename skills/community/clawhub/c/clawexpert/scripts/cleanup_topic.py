#!/usr/bin/env python3
"""Clean temporary subtopic directories, flags, and heartbeat files."""

from __future__ import annotations

import argparse
import json
import shutil

from clawexpert_common import knowledge_dir, list_flags, list_progress_files, topic_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--keep-flags", action="store_true")
    parser.add_argument("--keep-progress", action="store_true")
    parser.add_argument("--keep-subtopic-nodes", action="store_true")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    root = topic_dir(kb, args.slug)
    removed = {"subtopic_nodes": 0, "flags": 0, "progress": 0}

    if not args.keep_subtopic_nodes:
        for path in sorted((root / "nodes").glob("sub-*")):
            shutil.rmtree(path, ignore_errors=True)
            removed["subtopic_nodes"] += 1

    if not args.keep_flags:
        for path in list_flags(root):
            path.unlink(missing_ok=True)
            removed["flags"] += 1

    if not args.keep_progress:
        for path in list_progress_files(root):
            path.unlink(missing_ok=True)
            removed["progress"] += 1

    print(json.dumps(removed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
