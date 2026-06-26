#!/usr/bin/env python3
"""CLI for reading and writing dyk-prefs.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from write_tags import load_vocabulary
from helpers import PREFS_PATH

TAGS_CSV = Path(__file__).parent.parent / "references" / "tags.csv"

VALUE_MAP = {"like": 1, "neutral": 0, "dislike": -1}
VALUE_MAP_INV = {v: k for k, v in VALUE_MAP.items()}


def _load_vocab() -> dict[str, set[str]]:
    try:
        return load_vocabulary(TAGS_CSV)
    except OSError as exc:
        print(f"Cannot load vocabulary: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.rename(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def cmd_init(args: argparse.Namespace) -> int:
    if PREFS_PATH.exists():
        print(f"dyk-prefs.json already exists at {PREFS_PATH}", file=sys.stderr)
        return 1
    vocab = _load_vocab()
    data = {dim: {tag: 0 for tag in sorted(tags)} for dim, tags in sorted(vocab.items())}
    _atomic_write(PREFS_PATH, data)
    print(f"Created {PREFS_PATH}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    if not PREFS_PATH.exists():
        print(f"No prefs file found. Run: prefs.py init", file=sys.stderr)
        return 1
    try:
        data = json.loads(PREFS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Cannot read prefs: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print(f"Prefs file is malformed (expected a JSON object)", file=sys.stderr)
        return 1
    for dim, tags in sorted(data.items()):
        print(f"{dim}:")
        if not isinstance(tags, dict):
            print(f"Warning: expected object for {dim!r}, got {type(tags).__name__!r} — skipping", file=sys.stderr)
            continue
        for tag, val in sorted(tags.items()):
            word = VALUE_MAP_INV.get(val, str(val))
            if val not in VALUE_MAP_INV:
                print(f"Warning: unexpected value {val!r} for {dim}.{tag} — expected -1, 0, or 1", file=sys.stderr)
            print(f"  {tag}: {word}")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    if not PREFS_PATH.exists():
        print(f"No prefs file found. Run: prefs.py init", file=sys.stderr)
        return 1
    vocab = _load_vocab()
    if args.dimension not in vocab:
        print(f"Unknown dimension: {args.dimension!r}. Valid: {sorted(vocab)}", file=sys.stderr)
        return 1
    if args.tag not in vocab[args.dimension]:
        print(f"Unknown tag: {args.tag!r}. Valid for {args.dimension!r}: {sorted(vocab[args.dimension])}", file=sys.stderr)
        return 1
    try:
        data = json.loads(PREFS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Cannot read prefs: {exc}", file=sys.stderr)
        return 1
    dim_data = data.get(args.dimension)
    if not isinstance(dim_data, dict):
        print(f"Prefs file is malformed: expected object for {args.dimension!r}", file=sys.stderr)
        return 1
    val = dim_data.get(args.tag, 0)
    if val not in VALUE_MAP_INV:
        print(f"Warning: unexpected value {val!r} for {args.dimension}.{args.tag} — expected -1, 0, or 1", file=sys.stderr)
    print(VALUE_MAP_INV.get(val, str(val)))
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    if not PREFS_PATH.exists():
        print(f"No prefs file found. Run: prefs.py init", file=sys.stderr)
        return 1
    vocab = _load_vocab()
    if args.dimension not in vocab:
        print(f"Unknown dimension: {args.dimension!r}. Valid: {sorted(vocab)}", file=sys.stderr)
        return 1
    if args.tag not in vocab[args.dimension]:
        print(f"Unknown tag: {args.tag!r}. Valid for {args.dimension!r}: {sorted(vocab[args.dimension])}", file=sys.stderr)
        return 1
    try:
        data = json.loads(PREFS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Cannot read prefs: {exc}", file=sys.stderr)
        return 1
    data.setdefault(args.dimension, {})[args.tag] = VALUE_MAP[args.value]
    _atomic_write(PREFS_PATH, data)
    print(f"Set {args.dimension}.{args.tag} = {args.value}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage DYK preferences.")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("init", help="Create prefs file (fails if already exists)")
    sub.add_parser("list", help="Show all current preferences")
    get_p = sub.add_parser("get", help="Get preference for a tag")
    get_p.add_argument("dimension")
    get_p.add_argument("tag")
    set_p = sub.add_parser("set", help="Set preference for a tag")
    set_p.add_argument("dimension")
    set_p.add_argument("tag")
    set_p.add_argument("value", choices=list(VALUE_MAP))
    # Catch argparse's SystemExit(2) on invalid args and normalise to return code 1.
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code if exc.code is not None else 1
        return 1 if code != 0 else 0
    if args.command is None:
        parser.print_help()
        return 1
    if args.command == "init":
        return cmd_init(args)
    if args.command == "list":
        return cmd_list(args)
    if args.command == "get":
        return cmd_get(args)
    if args.command == "set":
        return cmd_set(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
