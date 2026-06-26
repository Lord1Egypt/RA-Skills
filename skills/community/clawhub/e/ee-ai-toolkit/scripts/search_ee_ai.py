#!/usr/bin/env python3
import argparse
from pathlib import Path


def iter_files(base):
    for rel_root in ("references", "assets/python-scripts"):
        root = base / rel_root
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in {".md", ".py", ".txt"}:
                yield path


def make_snippet(text, pos, width):
    start = max(0, pos - width)
    end = min(len(text), pos + width)
    snippet = text[start:end].replace("\n", " ")
    return " ".join(snippet.split())


def main():
    parser = argparse.ArgumentParser(description="Search EE AI Toolkit references and script assets.")
    parser.add_argument("--query", required=True, help="Keyword or phrase to search.")
    parser.add_argument("--limit", type=int, default=12, help="Maximum matches to print.")
    parser.add_argument("--width", type=int, default=220, help="Snippet characters around each match.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    query = args.query.lower()
    matches = []

    for path in iter_files(base):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lower = text.lower()
        pos = lower.find(query)
        while pos != -1:
            matches.append((path.relative_to(base), pos, make_snippet(text, pos, args.width)))
            if len(matches) >= args.limit:
                break
            pos = lower.find(query, pos + len(query))
        if len(matches) >= args.limit:
            break

    if not matches:
        print(f"No matches for: {args.query}")
        return 1

    for idx, (path, pos, snippet) in enumerate(matches, 1):
        print(f"{idx}. {path} @ char {pos}")
        print(f"   {snippet}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
