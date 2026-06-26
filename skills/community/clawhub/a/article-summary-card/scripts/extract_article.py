#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from summarize_article import read_input


def main():
    parser = argparse.ArgumentParser(
        description="Extract article title, source, and main text for session-driven summarization."
    )
    parser.add_argument("--url", help="Article URL")
    parser.add_argument("--file", help="Local text/markdown file")
    parser.add_argument("--out", required=True, help="Path to output extracted article JSON")
    args = parser.parse_args()

    title, source, article_text = read_input(args.url, args.file)
    payload = {
        "title": title,
        "source": source,
        "article_text": article_text,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
