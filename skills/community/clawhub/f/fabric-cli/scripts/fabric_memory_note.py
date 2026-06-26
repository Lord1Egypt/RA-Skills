#!/usr/bin/env python3
"""Generate a structured, redacted Fabric memory note.

The script prints Markdown by default, or JSON with --json. It does not call the
Fabric CLI. Agents can inspect the output, then pipe it to `fabric note` or
`fabric save` when the user has opted into persistence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|pwd)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"(?i)bearer\s+[a-z0-9._~+/=-]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
    re.compile(r"\b[a-f0-9]{32,}\b", re.IGNORECASE),
]


def redact(text: str) -> str:
    value = text or ""
    for pattern in SECRET_PATTERNS:
        value = pattern.sub("[REDACTED_SECRET]", value)
    return value


def read_text(value: str | None, file_value: str | None, stdin: bool) -> str:
    if file_value:
        return Path(file_value).read_text(encoding="utf-8")
    if stdin:
        return sys.stdin.read()
    return value or ""


def normalise_items(values: list[str] | None) -> list[str]:
    items: list[str] = []
    for value in values or []:
        for line in str(value).splitlines():
            cleaned = redact(line.strip())
            if cleaned:
                items.append(cleaned)
    return items


def normalise_tag(tag: str) -> str:
    tag = redact(tag.strip().lower().replace(" ", "-"))
    tag = re.sub(r"[^a-z0-9._-]+", "-", tag)
    return re.sub(r"-+", "-", tag).strip("-")


def normalise_tags(values: list[str] | None, project: str) -> list[str]:
    tags = ["agent-memory"]
    if project:
        tags.append(normalise_tag(project))
    for value in values or []:
        for part in str(value).split(","):
            tag = normalise_tag(part)
            if tag:
                tags.append(tag)
    deduped: list[str] = []
    for tag in tags:
        if tag and tag not in deduped:
            deduped.append(tag)
    return deduped


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None recorded."


def clamp(text: str, max_chars: int) -> tuple[str, bool]:
    if max_chars <= 0 or len(text) <= max_chars:
        return text, False
    return text[:max_chars].rstrip() + f"\n\n[Truncated to {max_chars} characters before saving.]", True


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    title = redact(args.title.strip())
    project = redact(args.project.strip()) if args.project else "Not specified"
    raw_summary = read_text(args.summary, args.summary_file, args.stdin_summary).strip()
    summary, truncated = clamp(redact(raw_summary), args.max_summary_chars)
    tags = normalise_tags(args.tag, args.project)
    date = args.date or dt.date.today().isoformat()
    note = "\n".join([
        f"# {title}", "",
        f"Date: {date}",
        f"Project: {project}",
        f"Tags: {', '.join(tags)}", "",
        "## Summary", summary or "No summary provided.", "",
        "## Decisions", bullets(normalise_items(args.decision)), "",
        "## Evidence or context", bullets(normalise_items(args.evidence)), "",
        "## Open questions", bullets(normalise_items(args.open_question)), "",
        "## Next steps", bullets(normalise_items(args.next_step)), "",
        "## Safety notes",
        "- Secrets and token-like strings were redacted automatically, but review before saving to Fabric.",
        "- The summary was truncated before output." if truncated else "",
    ]).rstrip() + "\n"
    return {"title": title, "project": project, "tags": tags, "note": note, "summary_truncated": truncated}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a structured, redacted Fabric memory note without calling Fabric.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--title", default="Fabric agent memory", help="Markdown note title.")
    parser.add_argument("--project", default="", help="Project/topic identifier, e.g. project-atlas.")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Date to include in the note.")
    parser.add_argument("--summary", help="Summary text. Use --summary-file or --stdin-summary for longer content.")
    parser.add_argument("--summary-file", help="Read UTF-8 summary text from this file.")
    parser.add_argument("--stdin-summary", action="store_true", help="Read summary text from stdin.")
    parser.add_argument("--decision", action="append", help="Decision bullet. May be repeated.")
    parser.add_argument("--evidence", action="append", help="Evidence/context bullet. May be repeated.")
    parser.add_argument("--open-question", action="append", help="Open question bullet. May be repeated.")
    parser.add_argument("--next-step", action="append", help="Next-step bullet. May be repeated.")
    parser.add_argument("--tag", action="append", help="Additional tag. May be repeated or comma-separated.")
    parser.add_argument("--max-summary-chars", type=int, default=6000, help="Maximum summary characters before truncation. Use 0 for no limit.")
    parser.add_argument("--output", help="Write output to this file instead of stdout.")
    parser.add_argument("--json", action="store_true", help="Print JSON containing title, project, tags, note, and truncation status.")
    return parser.parse_args(argv)


def main(argv: list[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    payload = build_payload(args)
    output = json.dumps(payload, indent=2, sort_keys=True) + "\n" if args.json else str(payload["note"])
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
