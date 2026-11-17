#!/usr/bin/env python3
"""Export AgentScope conversation logs to multiple formats."""

import argparse
import csv
import html
import json
from pathlib import Path


def read_conversation(input_path: Path) -> dict:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data
    raise ValueError("Unsupported conversation file format")


def as_markdown(conversation: dict) -> str:
    lines = ["# Conversation Export", ""]
    for turn in conversation.get("turns", []):
        role = turn.get("role", "unknown")
        content = turn.get("content", "")
        lines.append(f"## {role}")
        lines.append("")
        lines.append(content)
        lines.append("")
    return "\n".join(lines)


def as_csv(conversation: dict, output_path: Path) -> None:
    rows = []
    for turn in conversation.get("turns", []):
        rows.append(
            {
                "role": turn.get("role", ""),
                "content": turn.get("content", ""),
                "timestamp": turn.get("timestamp", ""),
            }
        )
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["role", "content", "timestamp"])
        writer.writeheader()
        writer.writerows(rows)


def as_html(conversation: dict) -> str:
    body = []
    for turn in conversation.get("turns", []):
        role = html.escape(turn.get("role", "unknown"))
        content = html.escape(turn.get("content", ""))
        body.append(f"<article><h2>{role}</h2><p>{content}</p></article>")
    return "\n".join(
        [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            '<meta charset="utf-8">',
            "<title>Conversation Export</title>",
            "</head>",
            "<body>",
            "<h1>Conversation Export</h1>",
            *body,
            "</body>",
            "</html>",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Export AgentScope conversation logs")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--format", required=True, choices=["json", "markdown", "csv", "html"])
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    conversation = read_conversation(args.input)

    if args.format == "json":
        args.output.write_text(json.dumps(conversation, indent=2, ensure_ascii=False), encoding="utf-8")
    elif args.format == "markdown":
        args.output.write_text(as_markdown(conversation), encoding="utf-8")
    elif args.format == "csv":
        as_csv(conversation, args.output)
    elif args.format == "html":
        args.output.write_text(as_html(conversation), encoding="utf-8")

    print(f"Exported conversation to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
