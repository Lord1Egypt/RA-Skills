#!/usr/bin/env python3
"""
cornell.py — A CLI tool for managing Cornell Method notes as Markdown files.
Notes are stored in ~/cornell-notes/, one .md file per note.
"""

import os
import re
import sys
import shutil
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
NOTES_DIR = Path.home() / "cornell-notes"
DATE_FMT  = "%Y-%m-%d %H:%M"

# ── ANSI colours (degrade gracefully on Windows) ──────────────────────────────
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
RESET  = "\033[0m"

def c(text, *codes):
    if not sys.stdout.isatty():
        return text
    return "".join(codes) + str(text) + RESET

# ── Helpers ───────────────────────────────────────────────────────────────────
def ensure_dir():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

def slug(title: str) -> str:
    """Turn a title into a safe filename stem."""
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:80]

def note_path(title_or_slug: str) -> Path:
    return NOTES_DIR / f"{slug(title_or_slug)}.md"

def all_notes() -> list[Path]:
    return sorted(NOTES_DIR.glob("*.md"))

def template(title: str) -> str:
    now = datetime.now().strftime(DATE_FMT)
    return f"""\
---
title: {title}
date: {now}
tags: []
---

## Notes
<!-- Write your raw lecture / reading notes here -->


## Cues
<!-- After studying: keywords, questions, main ideas that summarise the notes -->
- 

## Summary
<!-- In 2-3 sentences, summarise this note in your own words -->

"""

def parse_sections(text: str) -> dict:
    """Return a dict with keys: meta, notes, cues, summary."""
    sections = {"meta": "", "notes": "", "cues": "", "summary": ""}
    current = "meta"
    for line in text.splitlines(keepends=True):
        low = line.strip().lower()
        if low == "## notes":
            current = "notes"
        elif low == "## cues":
            current = "cues"
        elif low == "## summary":
            current = "summary"
        else:
            sections[current] += line
    return sections

def prompt(label: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    try:
        val = input(f"{c(label, CYAN, BOLD)}{hint}: ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)
    return val or default

def confirm(msg: str) -> bool:
    try:
        ans = input(f"{c(msg, YELLOW)} [y/N] ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return False
    return ans in ("y", "yes")

def render_note(path: Path):
    """Pretty-print a Cornell note in the terminal."""
    text   = path.read_text()
    secs   = parse_sections(text)
    width  = min(shutil.get_terminal_size().columns, 90)
    ruler  = c("─" * width, DIM)

    # --- header
    title_match = re.search(r"^title:\s*(.+)$", secs["meta"], re.M)
    date_match  = re.search(r"^date:\s*(.+)$",  secs["meta"], re.M)
    title = title_match.group(1).strip() if title_match else path.stem
    date  = date_match.group(1).strip()  if date_match  else ""

    print()
    print(ruler)
    print(c(f"  {title}", BOLD, CYAN))
    if date:
        print(c(f"  {date}", DIM))
    print(ruler)

    # --- two-column layout: cues | notes
    cue_lines  = [l for l in secs["cues"].splitlines()  if l.strip() and not l.strip().startswith("<!--")]
    note_lines = [l for l in secs["notes"].splitlines() if l.strip() and not l.strip().startswith("<!--")]

    col_w   = (width - 4) // 3          # cues  ~1/3
    note_w  = (width - 4) - col_w       # notes ~2/3
    rows    = max(len(cue_lines), len(note_lines), 1)

    print(c(f"{'  CUES':<{col_w+2}}  {'NOTES'}", BOLD))
    print(c("─" * (col_w + 2) + "  " + "─" * note_w, DIM))
    for i in range(rows):
        cue  = cue_lines[i]  if i < len(cue_lines)  else ""
        note = note_lines[i] if i < len(note_lines) else ""
        print(f"  {cue:<{col_w}}  {note}")

    # --- summary
    summary = "\n".join(
        l for l in secs["summary"].splitlines()
        if l.strip() and not l.strip().startswith("<!--")
    ).strip()
    print(ruler)
    print(c("  SUMMARY", BOLD))
    if summary:
        for line in summary.splitlines():
            print(f"  {line}")
    else:
        print(c("  (no summary yet)", DIM))
    print(ruler)
    print()

# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_new(args):
    ensure_dir()
    title = " ".join(args.title) if args.title else prompt("Note title")
    if not title:
        print(c("Title cannot be empty.", RED)); return

    path = note_path(title)
    if path.exists():
        print(c(f"Note already exists: {path.name}", YELLOW))
        if not confirm("Overwrite?"):
            return

    path.write_text(template(title))
    print(c(f"✓ Created: {path}", GREEN))
    _open_in_editor(path)


def cmd_list(args):
    ensure_dir()
    notes = all_notes()
    if not notes:
        print(c("No notes yet. Run:  cornell new", DIM)); return

    print()
    for i, p in enumerate(notes, 1):
        text        = p.read_text()
        title_match = re.search(r"^title:\s*(.+)$", text, re.M)
        date_match  = re.search(r"^date:\s*(.+)$",  text, re.M)
        title = title_match.group(1).strip() if title_match else p.stem
        date  = date_match.group(1).strip()  if date_match  else ""
        print(f"  {c(str(i).rjust(3), DIM)}  {c(title, BOLD)}  {c(date, DIM)}")
    print()


def cmd_view(args):
    ensure_dir()
    notes = all_notes()
    if not notes:
        print(c("No notes found.", DIM)); return

    query = " ".join(args.note) if args.note else ""
    path  = _resolve_note(query, notes)
    if path:
        render_note(path)


def cmd_search(args):
    ensure_dir()
    query = " ".join(args.query)
    if not query:
        query = prompt("Search keyword")
    if not query:
        return

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    hits    = []
    for p in all_notes():
        text = p.read_text()
        if pattern.search(text):
            lines = [l.strip() for l in text.splitlines() if pattern.search(l)]
            hits.append((p, lines))

    if not hits:
        print(c(f'No notes match "{query}".', YELLOW)); return

    print()
    for path, lines in hits:
        title_match = re.search(r"^title:\s*(.+)$", path.read_text(), re.M)
        title = title_match.group(1).strip() if title_match else path.stem
        print(c(f"  ▸ {title}", BOLD, CYAN))
        for l in lines[:3]:
            highlighted = pattern.sub(lambda m: c(m.group(), YELLOW, BOLD), l)
            print(f"    {highlighted}")
        print()


def cmd_edit(args):
    ensure_dir()
    notes = all_notes()
    if not notes:
        print(c("No notes found.", DIM)); return

    query = " ".join(args.note) if args.note else ""
    path  = _resolve_note(query, notes)
    if path:
        _open_in_editor(path)


def cmd_delete(args):
    ensure_dir()
    notes = all_notes()
    if not notes:
        print(c("No notes found.", DIM)); return

    query = " ".join(args.note) if args.note else ""
    path  = _resolve_note(query, notes)
    if not path:
        return

    title_match = re.search(r"^title:\s*(.+)$", path.read_text(), re.M)
    title = title_match.group(1).strip() if title_match else path.stem
    print(c(f'About to delete "{title}"', RED))
    if confirm("Are you sure?"):
        path.unlink()
        print(c(f"✓ Deleted: {path.name}", GREEN))
    else:
        print("Cancelled.")


# ── Internal helpers ──────────────────────────────────────────────────────────

def _resolve_note(query: str, notes: list[Path]) -> Path | None:
    """
    If query matches a title/slug exactly → return it.
    If query is a number → pick by index.
    Otherwise → show fuzzy picker.
    """
    if query:
        # exact slug match
        candidate = note_path(query)
        if candidate.exists():
            return candidate
        # number
        if query.isdigit():
            idx = int(query) - 1
            if 0 <= idx < len(notes):
                return notes[idx]
        # fuzzy: title contains query
        q = query.lower()
        matches = [p for p in notes if q in p.stem or q in p.read_text().lower()[:200]]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            notes = matches   # narrow picker

    # interactive picker
    print()
    for i, p in enumerate(notes, 1):
        title_match = re.search(r"^title:\s*(.+)$", p.read_text(), re.M)
        title = title_match.group(1).strip() if title_match else p.stem
        print(f"  {c(str(i), CYAN, BOLD)}  {title}")
    print()
    choice = prompt("Pick a number (or q to cancel)", "")
    if choice.lower() in ("q", ""):
        return None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(notes):
            return notes[idx]
    print(c("Invalid choice.", RED))
    return None


def _open_in_editor(path: Path):
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "micro"
    try:
        subprocess.run([editor, str(path)])
    except FileNotFoundError:
        print(c(f"Editor '{editor}' not found. Set $EDITOR env var.", YELLOW))
        print(f"File saved at: {path}")


# ── CLI wiring ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="cornell",
        description="Cornell Method note manager — one Markdown file per note.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  cornell new "Lecture 3 – Photosynthesis"
  cornell list
  cornell view 2
  cornell search mitochondria
  cornell edit "lecture-3"
  cornell delete 5
        """,
    )
    sub = parser.add_subparsers(dest="cmd", metavar="command")

    # new
    p_new = sub.add_parser("new",    help="Create a new Cornell note")
    p_new.add_argument("title", nargs="*", help="Note title")

    # list
    sub.add_parser("list",   help="List all notes")
    sub.add_parser("ls",     help="Alias for list")

    # view
    p_view = sub.add_parser("view",  help="View a note (pretty-printed)")
    p_view.add_argument("note", nargs="*", help="Title, slug, or number")

    # search
    p_srch = sub.add_parser("search", help="Search notes by keyword")
    p_srch.add_argument("query", nargs="*", help="Search term")

    # edit
    p_edit = sub.add_parser("edit",  help="Open a note in $EDITOR")
    p_edit.add_argument("note", nargs="*", help="Title, slug, or number")

    # delete
    p_del  = sub.add_parser("delete", help="Delete a note")
    p_del.add_argument("note", nargs="*", help="Title, slug, or number")
    sub.add_parser("rm", help="Alias for delete").add_argument("note", nargs="*")

    args = parser.parse_args()

    dispatch = {
        "new":    cmd_new,
        "list":   cmd_list,
        "ls":     cmd_list,
        "view":   cmd_view,
        "search": cmd_search,
        "edit":   cmd_edit,
        "delete": cmd_delete,
        "rm":     cmd_delete,
    }

    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
