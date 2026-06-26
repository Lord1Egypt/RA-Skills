#!/usr/bin/env python3
"""
flatten.py - Flatten nested JSON into single-level objects with dot-notation
keys, or unflatten back into nested structure.

Two modes:
    --flatten   (default)  nested object/array -> {dot.path: value}
    --unflatten            {dot.path: value}    -> nested object/array

Usage:
    flatten.py INPUT OUTPUT [--separator .] [--unflatten] [--index-style dot|bracket]

Options:
    --separator CHAR        path separator (default: '.')
    --index-style dot|bracket
                            for arrays: dot -> 'items.0.name'; bracket ->
                            'items[0].name' (default: dot)
    --unflatten             reverse the flattening (read {path: value} dict
                            and rebuild a nested structure)
    --output-format json|jsonl
                            for flatten on a JSONL input, choose how to emit
                            (default: jsonl)
    --json                  emit a machine-readable summary on stderr
    --quiet                 suppress the summary
    -h, --help              show this help

Exit codes:
    0  success
    1  input is empty / nothing to flatten
    2  bad arguments / unsafe path / missing file / invalid JSON /
       unsupported output extension
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

from _common import load_json, safe_path, dump_json, dump_jsonl


ALLOWED_EXTS = {".json", ".jsonl"}


def flatten_obj(obj: Any, sep: str = ".", index_style: str = "dot",
                prefix: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if isinstance(obj, dict):
        if not obj:
            if prefix:
                out[prefix] = {}
            return out
        for k, v in obj.items():
            key = str(k)
            new = f"{prefix}{sep}{key}" if prefix else key
            out.update(flatten_obj(v, sep, index_style, new))
    elif isinstance(obj, list):
        if not obj:
            if prefix:
                out[prefix] = []
            return out
        for i, v in enumerate(obj):
            if index_style == "bracket":
                new = f"{prefix}[{i}]" if prefix else f"[{i}]"
            else:
                new = f"{prefix}{sep}{i}" if prefix else str(i)
            out.update(flatten_obj(v, sep, index_style, new))
    else:
        out[prefix] = obj
    return out


_BRACKET_INDEX_RE = re.compile(r"\[(\d+)\]")


def unflatten_obj(flat: Dict[str, Any], sep: str = ".",
                  index_style: str = "dot") -> Any:
    root: Any = None

    def _set(path_parts: List[Any], value: Any) -> None:
        nonlocal root
        if not path_parts:
            root = value
            return
        # Decide if root should be a list or dict based on first part
        if root is None:
            root = [] if isinstance(path_parts[0], int) else {}
        cur = root
        for i, part in enumerate(path_parts[:-1]):
            nxt_part = path_parts[i + 1]
            if isinstance(part, int):
                # cur must be a list
                while len(cur) <= part:
                    cur.append({} if not isinstance(nxt_part, int) else [])
                if cur[part] is None or (
                    isinstance(cur[part], dict) and isinstance(nxt_part, int)
                ) or (isinstance(cur[part], list) and not isinstance(nxt_part, int)):
                    cur[part] = [] if isinstance(nxt_part, int) else {}
                cur = cur[part]
            else:
                if part not in cur or cur[part] is None:
                    cur[part] = [] if isinstance(nxt_part, int) else {}
                cur = cur[part]
        last = path_parts[-1]
        if isinstance(last, int):
            while len(cur) <= last:
                cur.append(None)
            cur[last] = value
        else:
            cur[last] = value

    for path, value in flat.items():
        parts: List[Any] = []
        if index_style == "bracket":
            # Split on sep, then parse [N] inside each piece
            for piece in path.split(sep):
                m = _BRACKET_INDEX_RE.search(piece)
                if m:
                    pre = piece[: m.start()]
                    if pre:
                        parts.append(pre)
                    parts.append(int(m.group(1)))
                    # there might be more [n] in the same piece
                    rest = piece[m.end():]
                    while rest:
                        m2 = _BRACKET_INDEX_RE.match(rest)
                        if m2:
                            parts.append(int(m2.group(1)))
                            rest = rest[m2.end():]
                        else:
                            break
                else:
                    parts.append(piece)
        else:
            for piece in path.split(sep):
                if piece.isdigit():
                    parts.append(int(piece))
                else:
                    parts.append(piece)
        _set(parts, value)

    return root if root is not None else {}


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--separator", default=".")
    p.add_argument("--index-style", dest="index_style",
                   choices=("dot", "bracket"), default="dot")
    p.add_argument("--unflatten", action="store_true")
    p.add_argument("--output-format", dest="out_fmt",
                   choices=("json", "jsonl"), default=None)
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2
    if out_path.suffix.lower() not in ALLOWED_EXTS:
        print(f"Error: unsupported output extension '{out_path.suffix}'. "
              f"Allowed: .json, .jsonl", file=sys.stderr)
        return 2

    try:
        data, kind = load_json(in_path)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        return 2

    if data is None:
        print(f"Empty input: {in_path}", file=sys.stderr)
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.unflatten:
        # Input must be a dict (or JSONL of dicts)
        if kind == "jsonl":
            results = [unflatten_obj(item, args.separator, args.index_style)
                       for item in data if isinstance(item, dict)]
            ext = out_path.suffix.lower()
            if ext == ".jsonl":
                out_path.write_text(dump_jsonl(results), encoding="utf-8")
            else:
                out_path.write_text(dump_json(results), encoding="utf-8")
            n = len(results)
        else:
            if not isinstance(data, dict):
                print("Error: --unflatten requires a top-level object",
                      file=sys.stderr)
                return 2
            result = unflatten_obj(data, args.separator, args.index_style)
            out_path.write_text(dump_json(result), encoding="utf-8")
            n = 1
    else:
        if kind == "jsonl":
            results = [flatten_obj(item, args.separator, args.index_style)
                       for item in data]
            ext = out_path.suffix.lower()
            fmt = args.out_fmt or ("jsonl" if ext == ".jsonl" else "json")
            if fmt == "jsonl":
                out_path.write_text(dump_jsonl(results), encoding="utf-8")
            else:
                out_path.write_text(dump_json(results), encoding="utf-8")
            n = len(results)
        else:
            result = flatten_obj(data, args.separator, args.index_style)
            ext = out_path.suffix.lower()
            if ext == ".jsonl":
                # One key=value per line, each as a {key: value} JSONL row
                lines = [json.dumps({k: v}, ensure_ascii=False)
                         for k, v in result.items()]
                out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            else:
                out_path.write_text(dump_json(result), encoding="utf-8")
            n = len(result)

    summary = {
        "input": str(in_path),
        "output": str(out_path),
        "mode": "unflatten" if args.unflatten else "flatten",
        "separator": args.separator,
        "index_style": args.index_style,
        "items": n,
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            mode = "unflatten" if args.unflatten else "flatten"
            print(f"{mode}: {n} item(s)/key(s) -> {out_path}", file=sys.stderr)
    return 0 if n > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
