#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
import re
from pathlib import Path
from textwrap import dedent

from memory_os_common import load_settings

AXIS_BY_KIND = {
    "experience": {"think", "say", "do"},
    "value": {"good", "bad"},
    "standard": {"right", "wrong"},
}

KIND_ALIASES = {
    "preference": "value",
}


def ensure_daily_file(path: Path, iso_date: str) -> None:
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if "## L1 Entries" in text:
            return
        path.write_text(text.rstrip() + "\n\n## L1 Entries\n", encoding="utf-8")
        return

    template = dedent(
        f"""
        # {iso_date} Memory Log (L1)

        ## Format
        - [YYYY-MM-DD|M-YYYYMMDD-###|kind|axis|status|confidence|topic] statement

        ## L1 Entries
        """
    ).strip() + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template, encoding="utf-8")


def next_entry_id(path: Path, iso_date: str) -> str:
    ymd = iso_date.replace("-", "")
    prefix = f"M-{ymd}-"
    if not path.exists():
        return prefix + "001"

    max_num = 0
    pattern = re.compile(re.escape(prefix) + r"(\d{3})")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if not match:
            continue
        max_num = max(max_num, int(match.group(1)))
    return prefix + f"{max_num + 1:03d}"


def sanitize(text: str) -> str:
    return " ".join(text.replace("|", "/").replace("]", ")").split())


def normalize_kind(raw_kind: str) -> str:
    kind = raw_kind.strip().lower()
    return KIND_ALIASES.get(kind, kind)


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a typed L1 memory entry.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    parser.add_argument("--kind", required=True, help="experience | value | standard (legacy preference is accepted)")
    parser.add_argument("--axis", required=True)
    parser.add_argument("--topic", required=True, help="Short topic label")
    parser.add_argument("--statement", required=True, help="Memory statement")
    parser.add_argument("--status", default="active", choices=["active", "candidate", "stale", "conflicted", "superseded"])
    parser.add_argument("--confidence", default="medium", choices=["low", "medium", "high"])
    args = parser.parse_args()

    kind = normalize_kind(args.kind)
    if kind not in AXIS_BY_KIND:
        raise SystemExit(f"Invalid kind '{args.kind}'. Allowed: {', '.join(sorted(AXIS_BY_KIND.keys()))}")

    axis = args.axis.strip().lower()
    allowed = AXIS_BY_KIND[kind]
    if axis not in allowed:
        raise SystemExit(f"Invalid axis '{axis}' for kind '{kind}'. Allowed: {', '.join(sorted(allowed))}")

    workspace = Path(args.workspace).expanduser().resolve()
    settings = load_settings(workspace)
    today = date.today().isoformat()
    daily_path = workspace / "memory" / f"{today}.md"
    ensure_daily_file(daily_path, today)

    entry_id = next_entry_id(daily_path, today)
    topic = sanitize(args.topic.strip().lower())
    statement = sanitize(args.statement.strip())

    line = f"- [{today}|{entry_id}|{kind}|{axis}|{args.status}|{args.confidence}|{topic}] {statement}"
    with daily_path.open("a", encoding="utf-8") as handle:
        if daily_path.read_text(encoding="utf-8").rstrip().endswith("## L1 Entries"):
            handle.write("\n")
        handle.write(line + "\n")

    print(f"Captured: {entry_id}")
    print(f"File: {daily_path}")
    print(line)
    entry_count = int(entry_id.rsplit("-", 1)[-1])
    if entry_count > settings["daily_entries_soft_limit"]:
        print(
            f"Warning: daily entry count {entry_count} exceeds soft limit "
            f"{settings['daily_entries_soft_limit']}. Consider running run_daily_review.py."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
