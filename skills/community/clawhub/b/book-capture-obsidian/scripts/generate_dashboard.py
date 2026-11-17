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

from common_config import get_env_csv, get_env_str
from common_json import fail_and_print, make_result, print_json
from common_markdown import inert_table_cell

STAGE = "generate_dashboard"
DEFAULT_TEMPLATE = SCRIPT_DIR.parent / "assets" / "templates" / "library-dashboard-template.md"


def _shelf_groups() -> Dict[str, List[str]]:
    """Shelf names counted under each status; Goodreads names by default."""
    return {
        "to_read": [s.lower() for s in get_env_csv("BOOK_CAPTURE_SHELVES_TO_READ", ["to-read", "want-to-read", "tbr"])],
        "reading": [s.lower() for s in get_env_csv("BOOK_CAPTURE_SHELVES_READING", ["currently-reading", "reading"])],
        "finished": [s.lower() for s in get_env_csv("BOOK_CAPTURE_SHELVES_READ", ["read", "finished"])],
        "inbox": ["inbox"],
    }


def _shelf_table(counts: Dict[str, int]) -> str:
    if not counts:
        return "_No shelves yet._"
    rows = ["| Shelf | Books |", "| --- | --- |"]
    for shelf, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        rows.append(f"| {inert_table_cell(shelf)} | {count} |")
    return "\n".join(rows)


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
    vault = Path(vault_path).expanduser().resolve()
    books_root = (vault / Path(notes_dir)).resolve()
    dashboard_path = (vault / Path(dashboard_file)).resolve()
    for label, path in (("notes directory", books_root), ("dashboard file", dashboard_path)):
        if path != vault and vault not in path.parents:
            return make_result(STAGE, ok=False, error=f"{label} escapes the vault: {path}")
    if dashboard_path.suffix.lower() != ".md":
        return make_result(STAGE, ok=False, error=f"dashboard file must be a .md note: {dashboard_path}")

    if not books_root.exists():
        return make_result(STAGE, ok=False, error=f"books directory not found: {books_root}")

    template_path = Path(template_file).expanduser()
    if not template_path.exists():
        return make_result(STAGE, ok=False, error=f"dashboard template not found: {template_path}")

    groups = _shelf_groups()
    counts = {"to_read": 0, "reading": 0, "finished": 0, "inbox": 0}
    shelf_counts: Dict[str, int] = {}
    total = 0

    for note_path in sorted(books_root.rglob("*.md")):
        if note_path.resolve() == dashboard_path.resolve() or note_path.name.startswith("Series - "):
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
        shelf = str(frontmatter.get("shelf") or "inbox").strip().lower() or "inbox"
        shelf_counts[shelf] = shelf_counts.get(shelf, 0) + 1
        for group, shelves in groups.items():
            if shelf in shelves:
                counts[group] += 1
                break

    summary = {
        "total_books": total,
        "to_read_count": counts["to_read"],
        "reading_count": counts["reading"],
        "finished_count": counts["finished"],
        "inbox_count": counts["inbox"],
    }
    template = template_path.read_text(encoding="utf-8")
    rendered = _render_template(
        template,
        {
            **summary,
            "notes_dir": Path(notes_dir).as_posix().strip("/"),
            "reading_shelves": ", ".join(f'"{name}"' for name in groups["reading"]),
            "shelf_table": _shelf_table(shelf_counts),
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
        counts=summary,
        shelves=dict(sorted(shelf_counts.items())),
    )


def _self_check() -> Dict[str, Any]:
    sample = """---\nshelf: "currently-reading"\ntags:\n  - "book"\n---\n# Book\n"""
    parsed = _parse_frontmatter(sample)
    ok = parsed.get("shelf") == "currently-reading" and parsed.get("tags") == ["book"] and DEFAULT_TEMPLATE.exists()
    return make_result(STAGE, ok=ok, error=None if ok else "frontmatter parser self-check failed", checks=parsed)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault-path", default=get_env_str("BOOK_CAPTURE_VAULT_PATH", ""), help="Obsidian vault root (required)")
    parser.add_argument("--notes-dir", default=get_env_str("BOOK_CAPTURE_NOTES_DIR", "Books"), help="Notes directory inside vault")
    parser.add_argument("--dashboard-file", default=get_env_str("BOOK_CAPTURE_DASHBOARD_FILE", ""), help="Dashboard note path relative to vault (default: <notes-dir>/Library Dashboard.md)")
    parser.add_argument("--template-file", default=get_env_str("BOOK_CAPTURE_DASHBOARD_TEMPLATE", str(DEFAULT_TEMPLATE)), help="Template markdown path")
    parser.add_argument("--self-check", action="store_true", help="Run internal quick checks")
    args = parser.parse_args(argv)

    if args.self_check:
        result = _self_check()
        print_json(result)
        return 0 if result.get("ok") else 1

    if not args.vault_path.strip() or not Path(args.vault_path).expanduser().is_dir():
        return fail_and_print(STAGE, "an existing vault directory is required (--vault-path or BOOK_CAPTURE_VAULT_PATH)")

    result = generate_dashboard(
        vault_path=args.vault_path,
        notes_dir=args.notes_dir,
        dashboard_file=args.dashboard_file or str(Path(args.notes_dir) / "Library Dashboard.md"),
        template_file=args.template_file,
    )
    print_json(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
