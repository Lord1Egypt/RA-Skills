#!/usr/bin/env python3
"""List dream records, optionally filtered by date range or keyword."""

import json
import re
import sys
from pathlib import Path

DREAMS_DIR = Path.home() / ".openclaw" / "memory" / "dreams"


def parse_frontmatter(text: str) -> dict:
    meta = {}
    if not text.startswith("---"):
        return meta
    end = text.find("---", 3)
    if end == -1:
        return meta
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta


def list_dreams(since: str = None, keyword: str = None, limit: int = 20) -> list:
    files = sorted(DREAMS_DIR.glob("*.md"), reverse=True)
    results = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        date = meta.get("date", "")[:10]
        if since and date < since:
            continue
        if keyword and keyword not in text:
            continue
        results.append({
            "file": f.name,
            "date": date,
            "title": meta.get("title", f.stem),
            "tags": meta.get("tags", ""),
        })
        if len(results) >= limit:
            break
    return results


if __name__ == "__main__":
    args = json.loads(sys.stdin.buffer.read().decode("utf-8")) if not sys.stdin.isatty() else {}
    dreams = list_dreams(
        since=args.get("since"),
        keyword=args.get("keyword"),
        limit=args.get("limit", 20),
    )
    sys.stdout.buffer.write(json.dumps(dreams, ensure_ascii=False, indent=2).encode("utf-8"))
