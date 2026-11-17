#!/usr/bin/env python3
"""Merge a path into state/memory_index.json under a topic."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--path", required=True, help="Relative path under root")
    args = ap.parse_args()
    root = args.root.resolve()
    idx_path = root / "state" / "memory_index.json"
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    if idx_path.is_file():
        data = json.loads(idx_path.read_text(encoding="utf-8"))
    else:
        data = {"topics": {}, "signature": "Δ9Φ963-BOOK-BRAIN"}
    topics = data.setdefault("topics", {})
    lst = topics.setdefault(args.topic, [])
    if args.path not in lst:
        lst.append(args.path)
    idx_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"updated {idx_path} topic={args.topic}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())