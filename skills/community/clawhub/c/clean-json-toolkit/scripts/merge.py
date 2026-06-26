#!/usr/bin/env python3
"""
merge.py - Merge multiple JSON files into one. Common agent need: combine a
default config + user overrides + env-specific overrides into a final
config, or fold many small JSON files into one big object/array.

Usage:
    merge.py OUTPUT INPUT1 INPUT2 [INPUT3 ...] [options]

Strategies (--strategy):
    deep            (default) recursively merge objects; for arrays, later
                    inputs replace earlier ones (array-replace). Objects
                    inside arrays are NOT merged by position.
    shallow         top-level keys only; later inputs replace earlier ones
                    wholesale (no recursive descent).
    array-concat    same as 'deep' but arrays are concatenated end-to-end
                    instead of replaced.
    array-uniq      same as 'array-concat' but duplicate elements are dropped
                    (only works for hashable scalars; dicts/lists kept as-is).
    array-extend    if the top-level is an array on every input, concatenate
                    them into one big array. Errors if any input is not an
                    array.

Options:
    --strategy NAME     pick a merge strategy (default: deep)
    --pretty / --compact   indent=2 (default) vs single-line output
    --json              emit a machine-readable summary on stderr
    --quiet             suppress the text summary
    -h, --help          show this help

Examples:
    # Deep merge: defaults + user overrides
    merge.py final.json defaults.json user.json

    # Combine many event files into one big array
    merge.py all.json events/*.json --strategy array-extend

    # Merge package.json with override patches, concatenating arrays
    merge.py merged.json package.json overrides.json --strategy array-concat

Exit codes:
    0   success (output written)
    1   nothing to merge (all inputs were empty or null)
    2   bad arguments / unsafe path / missing file / invalid JSON /
        strategy mismatch (e.g. array-extend with non-array input)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List

from _common import load_json, safe_path


def deep_merge(a: Any, b: Any, array_mode: str = "replace") -> Any:
    """Merge b into a (b wins on conflict). array_mode: replace|concat|uniq."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k, v in b.items():
            if k in out:
                out[k] = deep_merge(out[k], v, array_mode)
            else:
                out[k] = v
        return out
    if isinstance(a, list) and isinstance(b, list):
        if array_mode == "concat":
            return a + b
        if array_mode == "uniq":
            combined = a + b
            seen = set()
            out_list = []
            for item in combined:
                try:
                    key = json.dumps(item, sort_keys=True)
                except TypeError:
                    key = id(item)
                if key in seen:
                    continue
                seen.add(key)
                out_list.append(item)
            return out_list
        return b  # replace
    return b


def shallow_merge(a: Any, b: Any) -> Any:
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        out.update(b)
        return out
    return b


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("output", nargs="?")
    p.add_argument("inputs", nargs="*")
    p.add_argument("--strategy", default="deep",
                   choices=("deep", "shallow", "array-concat", "array-uniq",
                            "array-extend"))
    p.add_argument("--pretty", action="store_true", default=True)
    p.add_argument("--compact", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.output or len(args.inputs) < 1:
        print(__doc__)
        return 0 if args.help else 2

    try:
        out_path = safe_path(args.output)
        in_paths = [safe_path(p) for p in args.inputs]
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if out_path.suffix.lower() not in (".json", ".jsonl"):
        print(f"Error: unsupported output extension '{out_path.suffix}'. "
              f"Allowed: .json, .jsonl", file=sys.stderr)
        return 2

    for p_ in in_paths:
        if not p_.is_file():
            print(f"Error: not a file: {p_}", file=sys.stderr)
            return 2

    # Load all inputs
    loaded: List[Any] = []
    for p_ in in_paths:
        try:
            data, _kind = load_json(p_)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON in {p_}: {e}", file=sys.stderr)
            return 2
        loaded.append(data)

    # Apply strategy
    if args.strategy == "array-extend":
        combined: List[Any] = []
        for i, data in enumerate(loaded):
            if not isinstance(data, list):
                print(f"Error: --strategy array-extend requires every input "
                      f"to be a top-level array; {in_paths[i]} is a "
                      f"{type(data).__name__}", file=sys.stderr)
                return 2
            combined.extend(data)
        result = combined
    elif args.strategy == "shallow":
        result = loaded[0]
        for nxt in loaded[1:]:
            result = shallow_merge(result, nxt)
    else:
        mode = {"deep": "replace", "array-concat": "concat",
                "array-uniq": "uniq"}[args.strategy]
        result = loaded[0]
        for nxt in loaded[1:]:
            result = deep_merge(result, nxt, mode)

    if result is None or (isinstance(result, (list, dict)) and len(result) == 0):
        if not args.quiet:
            print(f"merge: result is empty", file=sys.stderr)
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    indent = None if args.compact else 2
    if out_path.suffix.lower() == ".jsonl":
        if not isinstance(result, list):
            print(f"Error: cannot write non-array result to .jsonl",
                  file=sys.stderr)
            return 2
        with out_path.open("w", encoding="utf-8") as f:
            for item in result:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
    else:
        out_path.write_text(
            json.dumps(result, indent=indent, ensure_ascii=False),
            encoding="utf-8"
        )

    summary = {
        "output": str(out_path),
        "inputs": [str(p) for p in in_paths],
        "strategy": args.strategy,
        "top_level_type": type(result).__name__,
        "items": (len(result) if isinstance(result, (list, dict)) else 1),
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            n = summary["items"]
            print(f"merge: {len(in_paths)} input(s) -> {out_path} "
                  f"({args.strategy}, {summary['top_level_type']}, {n} item(s))",
                  file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
