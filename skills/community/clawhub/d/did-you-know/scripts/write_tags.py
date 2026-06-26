#!/usr/bin/env python3
"""Merge LLM-assigned tags into the DYK cache."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from helpers import load_store, save_store

TAGS_CSV = Path(__file__).parent.parent / "references" / "tags.csv"


def load_vocabulary(path: Path) -> dict[str, set[str]]:
    """Return allowed tag IDs grouped by dimension."""
    vocab: dict[str, set[str]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            vocab.setdefault(row["dimension"], set()).add(row["tag_id"])
    return vocab


def apply_tags(store: dict, entries: list[dict], vocab: dict[str, set[str]]) -> None:
    """Validate all entries then merge tags into matching hooks.

    Hooks with no 'tags' key (legacy) are skipped.
    Hooks where tags is not None (already tagged) are skipped.
    Unrecognised URLs are silently skipped.
    Raises ValueError on any unknown tag before any merging occurs.
    """
    if not isinstance(entries, list):
        raise ValueError("entries must be a list")

    allowed_domains = vocab.get("domain", set())
    allowed_tones = vocab.get("tone", set())

    # Validate all before touching the store.
    for entry in entries:
        if not isinstance(entry.get("url"), str):
            raise ValueError("each entry must have a 'url' string field")
        domain = entry.get("domain", [])
        if not isinstance(domain, list):
            raise ValueError(f"'domain' must be a list, got {type(domain).__name__!r}")
        tone = entry.get("tone")
        if not isinstance(tone, str):
            raise ValueError(f"'tone' must be a string, got {type(tone).__name__!r}")
        for d in domain:
            if d not in allowed_domains:
                raise ValueError(f"Unknown domain tag: {d!r}")
        if tone not in allowed_tones:
            raise ValueError(f"Unknown tone tag: {tone!r}")

    url_to_entry = {e["url"]: e for e in entries}

    for coll in store.get("collections", []):
        for hook in coll.get("hooks", []):
            if "tags" not in hook:
                continue  # legacy hook — skip
            if hook["tags"] is not None:
                continue  # already tagged — skip
            primary_url = (hook.get("urls") or [None])[0]
            if primary_url not in url_to_entry:
                continue
            entry = url_to_entry[primary_url]
            hook["tags"] = {
                "domain": entry["domain"],
                "tone": entry["tone"],
                "low_confidence": entry.get("low_confidence", False),
            }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge tags into DYK cache.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--json", dest="json_input",
                        help="JSON array of tagged entries (inline)")
    source.add_argument("--json-file", dest="json_file",
                        help="Path to JSON file containing tagged entries array")
    parser.add_argument("--vocabulary", default=str(TAGS_CSV),
                        help="Path to tags.csv vocabulary file")
    args = parser.parse_args(argv)

    if args.json_file is not None:
        try:
            raw = Path(args.json_file).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"Cannot read JSON file: {exc}", file=sys.stderr)
            return 1
    else:
        raw = args.json_input

    try:
        entries = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1

    try:
        vocab = load_vocabulary(Path(args.vocabulary))
    except OSError as exc:
        print(f"Cannot load vocabulary: {exc}", file=sys.stderr)
        return 1

    store = load_store()
    try:
        apply_tags(store, entries, vocab)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    save_store(store)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
