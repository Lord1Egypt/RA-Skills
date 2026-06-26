#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def normalize_tags(tags):
    if isinstance(tags, str):
        items = [part.strip() for part in tags.replace("，", ",").split(",")]
    elif isinstance(tags, list):
        items = [str(part).strip() for part in tags]
    else:
        items = []
    return [item for item in items if item]


def load_payload(path_arg):
    if path_arg:
        return json.loads(Path(path_arg).read_text(encoding="utf-8"))
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise SystemExit("Provide --input <json-file> or pipe JSON via stdin.")


def render_markdown(payload):
    tags = normalize_tags(payload.get("tags", []))
    tag_line = " ".join(tag if tag.startswith("#") else f"#{tag}" for tag in tags)
    lines = [
        "# Xiaohongshu Publish Package",
        "",
        f"- Title: {payload.get('title', '').strip()}",
        f"- Suggested Window: {payload.get('suggested_posting_window', '').strip()}",
        f"- Cover Idea: {payload.get('cover_idea', '').strip()}",
        "",
        "## Body",
        "",
        payload.get("body", "").strip(),
        "",
        "## Tags",
        "",
        tag_line,
        "",
        "## First Comment",
        "",
        payload.get("first_comment", "").strip(),
        "",
        "## Notes",
        "",
        payload.get("notes", "待人工确认后发布。").strip(),
    ]
    return "\n".join(lines).strip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()

    payload = load_payload(args.input)
    markdown = render_markdown(payload)
    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
