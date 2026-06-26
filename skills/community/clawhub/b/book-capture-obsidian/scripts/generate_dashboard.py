#!/usr/bin/env python3
"""Generate a Library Dashboard note from existing book note frontmatter."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_config import get_env_str
from common_json import fail_and_print, make_result, print_json

STAGE = "generate_dashboard"


def _parse_frontmatter(content: str) -> Dict[str, Any]:
    lines = content.splitlines()
    if not lines:
        return {}

    start = None
    for idx, line in enumerate(lines[:20]):
        if line.strip() == "---":
            start = idx
            break
    if start is None:
        return {}

    data: Dict[str, Any] = {}
    i = start + 1
    current_key = None
    current_list: List[str] = []

    while i < len(lines):
        line = lines[i]
        i += 1
        if line.strip() == "---":
            break

        if current_key and line.startswith("  - "):
            current_list.append(line[4:].strip().strip('"'))
            continue

        if current_key and current_list:
            data[current_key] = current_list
            current_key = None
            current_list = []

        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if value == "":
            current_key = key
            current_list = []
            continue

        if value in {"null", "None"}:
            data[key] = None
        elif value in {"true", "false"}:
            data[key] = value == "true"
        elif re.fullmatch(r"-?\d+", value):
            data[key] = int(value)
        elif re.fullmatch(r"-?\d+\.\d+", value):
            data[key] = float(value)
        else:
            data[key] = value.strip('"')

    if current_key and current_list:
        data[current_key] = current_list

    return data


def _render_template(template: str, values: Dict[str, Any]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def generate_dashboard(vault_path: str, notes_dir: str, dashboard_file: str, template_file: str) -> Dict[str, Any]:
    vault = Path(vault_path).expanduser()
    books_root = vault / Path(notes_dir)
    dashboard_path = vault / Path(dashboard_file)

    if not books_root.exists():
        return make_result(STAGE, ok=False, error=f"books directory not found: {books_root}")

    template_path = Path(template_file).expanduser()
    if not template_path.exists():
        return make_result(STAGE, ok=False, error=f"dashboard template not found: {template_path}")

    total = 0
    to_read = 0
    reading = 0
    finished = 0
    needs_review = 0

    for note_path in books_root.rglob("*.md"):
        if note_path.name == "Library Dashboard.md" or note_path.name.startswith("Series - "):
            continue

        content = note_path.read_text(encoding="utf-8")
        frontmatter = _parse_frontmatter(content)
        if not frontmatter:
            continue

        # Count only book notes
        tags = frontmatter.get("tags")
        is_book = False
        if isinstance(tags, list):
            is_book = "book" in [str(t).strip().lower() for t in tags]
        if not is_book and not frontmatter.get("shelf"):
            continue

        total += 1
        status = str(frontmatter.get("status") or "").strip().lower()
        if status == "to-read":
            to_read += 1
        elif status == "reading":
            reading += 1
        elif status == "finished":
            finished += 1

        if bool(frontmatter.get("needs_review", False)):
            needs_review += 1

    template = template_path.read_text(encoding="utf-8")
    rendered = _render_template(
        template,
        {
            "total_books": total,
            "to_read_count": to_read,
            "reading_count": reading,
            "finished_count": finished,
            "needs_review_count": needs_review,
        },
    )

    dashboard_path.parent.mkdir(parents=True, exist_ok=True)
    previous = dashboard_path.read_text(encoding="utf-8") if dashboard_path.exists() else None
    updated = previous != rendered
    if updated:
        dashboard_path.write_text(rendered, encoding="utf-8")

    return make_result(
        STAGE,
        ok=True,
        error=None,
        dashboard_path=str(dashboard_path),
        updated=updated,
        counts={
            "total_books": total,
            "to_read_count": to_read,
            "reading_count": reading,
            "finished_count": finished,
            "needs_review_count": needs_review,
        },
    )


def _self_check() -> Dict[str, Any]:
    sample = """---\nstatus: reading\nneeds_review: true\n---\n# Book\n"""
    parsed = _parse_frontmatter(sample)
    ok = parsed.get("status") == "reading" and parsed.get("needs_review") is True
    return make_result(STAGE, ok=ok, error=None if ok else "frontmatter parser self-check failed", checks=parsed)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault-path", default=get_env_str("BOOK_CAPTURE_VAULT_PATH", "."), help="Obsidian vault root")
    parser.add_argument("--notes-dir", default=get_env_str("BOOK_CAPTURE_NOTES_DIR", "Books"), help="Notes directory inside vault")
    parser.add_argument("--dashboard-file", default=get_env_str("BOOK_CAPTURE_DASHBOARD_FILE", "Books/Library Dashboard.md"), help="Dashboard note path relative to vault")
    parser.add_argument("--template-file", default=get_env_str("BOOK_CAPTURE_DASHBOARD_TEMPLATE", "skill/book-capture-obsidian/assets/templates/library-dashboard-template.md"), help="Template markdown path")
    parser.add_argument("--self-check", action="store_true", help="Run internal quick checks")
    args = parser.parse_args(argv)

    if args.self_check:
        result = _self_check()
        print_json(result)
        return 0 if result.get("ok") else 1

    result = generate_dashboard(
        vault_path=args.vault_path,
        notes_dir=args.notes_dir,
        dashboard_file=args.dashboard_file,
        template_file=args.template_file,
    )
    print_json(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
