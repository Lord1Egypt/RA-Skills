#!/usr/bin/env python3
"""
Parse CSV/Excel rows and output structured task objects
in Jira, Markdown, or JSON format.
"""
import csv, sys, json, argparse
from pathlib import Path

TEMPLATE_MARKDOWN = """| # | Summary | Description | Status | Priority |
|---|---------|------------|--------|----------|
{rows}"""

TEMPLATE_JSON = {
    "tasks": []
}

def parse_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            rows.append((i, row))
    return rows

def to_markdown(rows):
    lines = []
    for i, row in rows:
        lines.append(f"| {i} | {row.get('summary', row.get('title', ''))} | {row.get('description', '')} | {row.get('status', 'todo')} | {row.get('priority', 'medium')} |")
    return TEMPLATE_MARKDOWN.format(rows="\n".join(lines))

def to_json(rows):
    tasks = []
    for i, row in rows:
        tasks.append({
            "id": i,
            "summary": row.get("summary", row.get("title", "")),
            "description": row.get("description", ""),
            "status": row.get("status", "todo"),
            "priority": row.get("priority", "medium"),
        })
    return json.dumps({"tasks": tasks}, indent=2, ensure_ascii=False)

def to_jira(rows):
    lines = []
    for i, row in rows:
        lines.append(f"* [{row.get('status', 'todo').upper()}] {row.get('summary', row.get('title', ''))}")
        desc = row.get("description", "")
        if desc:
            lines.append(f"  #description {desc}")
        pri = row.get("priority", "medium")
        lines.append(f"  #priority {pri}")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("file", help="CSV or Excel file path")
    p.add_argument("-f", "--format", default="markdown", choices=["markdown", "json", "jira"])
    p.add_argument("-o", "--output", help="Output file path")
    args = p.parse_args()

    rows = parse_rows(args.file)
    out = {"markdown": to_markdown, "json": to_json, "jira": to_jira}[args.format](rows)

    if args.output:
        Path(args.output).write_text(out)
        print(f"✅ Written to {args.output}")
    else:
        print(out)