#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


MEMORY_DIR = Path("memory")


def load_payload(path_arg):
    if path_arg:
        return json.loads(Path(path_arg).read_text(encoding="utf-8"))
    import sys
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise SystemExit("Provide --input <json-file> or pipe JSON via stdin.")


def normalize_list(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--date")
    args = parser.parse_args()

    payload = load_payload(args.input)
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    path = MEMORY_DIR / f"{date_str}.md"

    titles = normalize_list(payload.get("titles"))
    reasons = normalize_list(payload.get("reasons"))
    preferences = normalize_list(payload.get("preferences"))
    notes = normalize_list(payload.get("notes"))

    lines = []
    if not path.exists():
        lines.extend([f"# {date_str}", ""])

    lines.extend([f"## {datetime.now().strftime('%H:%M')}", ""])
    for heading, items in [("Titles", titles), ("Why", reasons), ("Preferences", preferences), ("Notes", notes)]:
        if items:
            lines.append(f"### {heading}")
            lines.extend(f"- {item}" for item in items)
            lines.append("")

    if len(lines) <= 2:
        raise SystemExit("Nothing to write.")

    with path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n\n")
    print(path)


if __name__ == "__main__":
    main()
