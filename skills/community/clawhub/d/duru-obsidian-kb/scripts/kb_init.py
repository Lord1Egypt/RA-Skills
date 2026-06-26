#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DIRS = [
    "raw/articles",
    "raw/papers",
    "raw/repos",
    "raw/files",
    "assets",
    "wiki/concepts",
    "wiki/sources",
    "wiki/indexes",
    "wiki/_meta",
    "outputs",
    "logs",
]

TOPIC_TEMPLATE = """---
title: {title}
slug: {slug}
kind: concept
source_count: 0
---

# {title}

## Topic summary

_TBD._

## Core sources

_None yet._

## Key points

- TBD

## Open questions

- TBD

## Structured artifacts

_None yet._

## Backlinks

_None yet._
"""


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json_if_missing(path: Path, data):
    if not path.exists():
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_if_missing(path: Path, content: str):
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Initialize an Obsidian KB root")
    parser.add_argument("--root", required=True, help="Knowledge base root directory")
    parser.add_argument("--name", default=None, help="KB display name")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    for rel in DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)

    name = args.name or root.name
    timestamp = now_iso()

    write_json_if_missing(root / "config.json", {
        "name": name,
        "default_output_format": "md",
        "obsidian_compatible": True,
    })
    write_json_if_missing(root / "manifest.json", {
        "version": 1,
        "created_at": timestamp,
        "updated_at": timestamp,
        "entries": [],
    })

    write_text_if_missing(root / "wiki/indexes/index.md", f"# {name}\n\n- [[sources]]\n- [[tags]]\n- [[concepts]]\n- [[timeline]]\n- [[topic-map]]\n")
    write_text_if_missing(root / "wiki/indexes/sources.md", "# Sources\n\n_No sources yet._\n")
    write_text_if_missing(root / "wiki/indexes/tags.md", "# Tags\n\n_No tags yet._\n")
    write_text_if_missing(root / "wiki/indexes/timeline.md", "# Timeline\n\n_No entries yet._\n")
    write_text_if_missing(root / "wiki/indexes/concepts.md", "# Concepts\n\n_No concepts yet._\n")
    write_text_if_missing(root / "wiki/indexes/topic-map.md", "# Topic Map\n\n_No topic memos yet._\n")
    write_text_if_missing(root / "wiki/concepts/_template.md", TOPIC_TEMPLATE.format(title="topic", slug="topic"))

    print(json.dumps({"ok": True, "root": str(root), "name": name}, ensure_ascii=False))


if __name__ == "__main__":
    main()
