#!/usr/bin/env python3
"""Extract structured standup summary from raw chat log or notes."""

import argparse
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def parse_input(text: str) -> list[dict]:
    """Parse raw text into a list of {author, content, timestamp} dicts."""
    entries = []
    pattern = re.compile(
        r"^(?:\[?([^\]\s][^\]]*?)\]?\s+)?"
        r"([A-Za-z][A-Za-z0-9_.-]*)"
        r"\s*[:>]\s+"
        r"(.+)$"
    )
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if m:
            ts, author, content = m.group(1), m.group(2), m.group(3)
            entries.append({"author": author, "content": content, "timestamp": ts or ""})
        else:
            entries.append({"author": "unknown", "content": line, "timestamp": ""})
    return entries


def classify(content: str) -> str:
    lower = content.lower()
    blocker_pat = [r"\bblock", r"\bstuck\b", r"\bwaiting\b", r"\bneed help\b",
                   r"\bimpediment\b", r"\bcan't proceed\b", r"\bdependency\b",
                   r"\bno progress\b", r"\bstalled\b", r"\bblocked\b"]
    planned_pat = [r"\bwill\b", r"\bgoing to\b", r"\bplan to\b", r"\btomorrow\b",
                   r"\bnext\b", r"\bintend to\b", r"\babout to\b", r"\bupcoming\b",
                   r"\bwill be working\b", r"\bstarting work\b"]
    completed_pat = [r"\bcompleted\b", r"\bfinished\b", r"\bdone\b", r"\bsubmitted\b",
                     r"\bmerged\b", r"\bshipped\b", r"\bfixed\b", r"\bpushed\b",
                     r"\breviewed\b", r"\bdeployed\b", r"\blaunched\b", r"\bresolved\b"]

    for p in blocker_pat:
        if re.search(p, lower):
            return "blockers"
    for p in completed_pat:
        if re.search(p, lower):
            return "completed"
    for p in planned_pat:
        if re.search(p, lower):
            return "planned"
    return "completed"


def build_summary(entries: list[dict]) -> dict:
    summary = {"completed": [], "planned": [], "blockers": []}
    for entry in entries:
        bucket = classify(entry["content"])
        summary[bucket].append({"author": entry["author"], "content": entry["content"]})
    return summary


def to_markdown(summary: dict, title: str = "Daily Standup Summary") -> str:
    lines = [f"# {title}\n"]
    labels = [("completed", "Completed"), ("planned", "Planned"), ("blockers", "Blockers")]
    for key, label in labels:
        lines.append(f"## {label}\n")
        items = summary.get(key, [])
        if not items:
            lines.append("_None to report_\n")
        else:
            for item in items:
                lines.append(f"- **{item['author']}**: {item['content']}")
            lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract standup summary from raw text")
    parser.add_argument("input", help="Path to input file (chat log or notes)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--title", default="Daily Standup Summary")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    entries = parse_input(text)
    if not entries:
        print("Error: no content parsed from input.", file=sys.stderr)
        sys.exit(1)

    summary = build_summary(entries)

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(summary, args.title))


if __name__ == "__main__":
    main()
