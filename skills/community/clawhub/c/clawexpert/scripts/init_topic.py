#!/usr/bin/env python3
"""Initialize a topic directory and write the initial meta.json."""

from __future__ import annotations

import argparse
import json
import sys

from clawexpert_common import ensure_dir, iso_now, knowledge_dir, meta_path, save_json, slugify, topic_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--kb")
    parser.add_argument("--max-hours", type=int, default=2)
    parser.add_argument("--status", default="learning")
    parser.add_argument("--session-id", default="main")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    slug = args.slug or slugify(args.topic)
    root = topic_dir(kb, slug)
    meta_file = meta_path(kb, slug)

    if meta_file.exists() and not args.force:
        print(f"Refusing to overwrite existing meta.json: {meta_file}", file=sys.stderr)
        return 1

    ensure_dir(root / "raw" / "web")
    ensure_dir(root / "raw" / "pdf")
    ensure_dir(root / "nodes")

    now = iso_now()
    meta = {
        "topic": args.topic,
        "slug": slug,
        "created": now,
        "last_updated": now,
        "status": args.status,
        "source_count": 0,
        "node_count": 0,
        "max_hours": args.max_hours,
        "subtopics": [],
        "learning_sessions": [
            {
                "session_id": args.session_id,
                "started": now,
                "finished": None,
                "sources_added": 0,
            }
        ],
    }
    save_json(meta_file, meta)
    print(json.dumps({"topic": args.topic, "slug": slug, "meta_path": str(meta_file)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
