#!/usr/bin/env python3
"""
inspect.py - Profile a JSON / JSONL file: structure, types, depth, leaf
count, and sample values per path.

Usage:
    inspect.py INPUT [--max-depth N] [--max-samples N] [--json]

Options:
    --max-depth N       only descend N levels (default: 6)
    --max-samples N     keep up to N sample values per path (default: 3)
    --json              emit a machine-readable report on stdout
    -h, --help          show this help

Exit codes:
    0  success
    1  empty file
    2  bad arguments / missing file / unsafe path / invalid JSON
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from _common import load_json, safe_path, type_of, walk


def _summarize(data: Any, max_depth: int, max_samples: int) -> Dict[str, Any]:
    paths: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "types": defaultdict(int), "samples": [], "count": 0,
    })

    def _path_depth(p: str) -> int:
        return p.count(".") + p.count("[")

    if isinstance(data, list):
        # Top-level array: walk each item with its index prefix removed
        # so we describe the shape of items consistently.
        for i, item in enumerate(data):
            for p, v in walk(item, prefix=""):
                if _path_depth(p) > max_depth:
                    continue
                info = paths[p]
                info["count"] += 1
                info["types"][type_of(v)] += 1
                if len(info["samples"]) < max_samples:
                    if not isinstance(v, (dict, list)):
                        info["samples"].append(v)
    else:
        for p, v in walk(data):
            if _path_depth(p) > max_depth:
                continue
            info = paths[p]
            info["count"] += 1
            info["types"][type_of(v)] += 1
            if len(info["samples"]) < max_samples:
                if not isinstance(v, (dict, list)):
                    info["samples"].append(v)

    return paths


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("--max-depth", type=int, default=6)
    p.add_argument("--max-samples", type=int, default=3)
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input:
        print(__doc__)
        return 0 if args.help else 2

    try:
        in_path = safe_path(args.input)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    try:
        data, kind = load_json(in_path)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        return 2

    if data is None or (isinstance(data, list) and len(data) == 0):
        print(f"Inspect: empty file ({in_path})", file=sys.stderr)
        return 1

    top = type_of(data)
    n_items = len(data) if isinstance(data, list) else 1
    size = in_path.stat().st_size

    paths = _summarize(data, args.max_depth, args.max_samples)

    summary = {
        "input": str(in_path),
        "kind": kind,
        "top_level_type": top,
        "items": n_items,
        "size_bytes": size,
        "paths": {
            p: {
                "count": info["count"],
                "types": dict(info["types"]),
                "samples": info["samples"],
            } for p, info in paths.items()
        },
    }

    if args.as_json:
        print(json.dumps(summary, indent=2, default=str))
        return 0

    print(f"Inspect: {in_path}")
    print(f"  Kind:           {kind}")
    print(f"  Top-level:      {top}")
    print(f"  Items:          {n_items}")
    print(f"  Size:           {size:,} bytes")
    print(f"  Distinct paths: {len(paths)}")
    print()
    print(f"  {'path':<40s} {'count':>6s}  {'type(s)':<20s}  samples")
    print("  " + "-" * 90)
    for p in sorted(paths.keys()):
        info = paths[p]
        types_str = ",".join(f"{t}:{n}" for t, n in info["types"].items())
        samples = info["samples"]
        smp_str = ", ".join(repr(s)[:30] for s in samples) if samples else ""
        if len(smp_str) > 50:
            smp_str = smp_str[:50] + "..."
        print(f"  {p[:40]:<40s} {info['count']:>6d}  {types_str:<20s}  {smp_str}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
