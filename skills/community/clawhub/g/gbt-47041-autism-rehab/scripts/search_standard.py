#!/usr/bin/env python3
"""Search or inspect the bundled GB/T 47041-2026 standard (Markdown or PDF)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "assets" / "GBT-47041-2026.md"
PDF_PATH = ROOT / "assets" / "GBT-47041-2026.pdf"


# ---------------------------------------------------------------------------
# Source loading
# ---------------------------------------------------------------------------

def load_md_pages() -> list[tuple[int, str]]:
    """Load the Markdown source and split into pseudo-pages by '---' separators."""
    text = MD_PATH.read_text(encoding="utf-8")
    # Split on horizontal rules used as page-like separators.
    # Treat the whole file as page 1 since MD has no physical pages.
    # We chunk by top-level headings (## ) to give useful "page" references.
    chunks: list[tuple[int, str]] = []
    current: list[str] = []
    page = 1
    for line in text.splitlines():
        if line.startswith("## ") and current:
            chunks.append((page, "\n".join(current)))
            current = []
            page += 1
        current.append(line)
    if current:
        chunks.append((page, "\n".join(current)))
    return chunks


def load_pdf_pages() -> list[tuple[int, str]]:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError:
        print(
            "Missing dependency: pypdf. Run this script with a Python environment that has pypdf. "
            "In Codex Desktop, call load_workspace_dependencies and use the bundled Python path.",
            file=sys.stderr,
        )
        sys.exit(2)

    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH}", file=sys.stderr)
        sys.exit(2)

    reader = PdfReader(str(PDF_PATH))
    pages: list[tuple[int, str]] = []
    for index, page in enumerate(reader.pages, start=1):
        pages.append((index, page.extract_text() or ""))
    return pages


def load_pages() -> tuple[list[tuple[int, str]], str]:
    """Return (pages, source_label). Prefer Markdown; fall back to PDF."""
    if MD_PATH.exists():
        return load_md_pages(), "md"
    return load_pdf_pages(), "pdf"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def iter_lines(pages: list[tuple[int, str]]) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for page_number, text in pages:
        for line in text.splitlines():
            cleaned = line.strip()
            if cleaned:
                rows.append((page_number, cleaned))
    return rows


def heading_level(number: str) -> int:
    if re.fullmatch(r"\d+(?:\.\d+)*", number):
        return number.count(".") + 1
    return 1


def is_heading(line: str) -> re.Match[str] | None:
    # Match both plain text headings and Markdown headings (with optional leading #'s)
    return re.match(
        r"^\s*(?:#{1,6}\s+)*((?:\d+)(?:\.\d+)*|附录\s*[A-Z]|参考文献)\s+(.+?)\s*$",
        line,
    )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def list_sections(pages: list[tuple[int, str]], label: str) -> None:
    seen: set[tuple[str, str]] = set()
    for page_number, line in iter_lines(pages):
        match = is_heading(line)
        if not match:
            continue
        number, title = match.group(1), compact(match.group(2))
        if len(title) > 90:
            title = title[:87] + "..."
        key = (number, title)
        if key in seen:
            continue
        seen.add(key)
        tag = f"s{page_number:02d}" if label == "md" else f"p{page_number:02d}"
        print(f"{tag}  {number}  {title}")


def search_query(pages: list[tuple[int, str]], query: str, context: int, limit: int, label: str) -> None:
    needle = query.lower()
    matches = 0
    tag_prefix = "section" if label == "md" else "pdf page"
    for page_number, text in pages:
        page_text = compact(text)
        haystack = page_text.lower()
        start = 0
        while True:
            index = haystack.find(needle, start)
            if index == -1:
                break
            left = max(0, index - context)
            right = min(len(page_text), index + len(query) + context)
            snippet = page_text[left:right]
            print(f"\n[{tag_prefix} {page_number}]")
            print(snippet)
            matches += 1
            if matches >= limit:
                return
            start = index + max(1, len(query))
    if matches == 0:
        print(f"No matches for: {query}")


def dump_page(pages: list[tuple[int, str]], page_number: int, label: str) -> None:
    for number, text in pages:
        if number == page_number:
            print(text.strip())
            return
    tag = "Section" if label == "md" else "Page"
    print(f"{tag} out of range: {page_number}", file=sys.stderr)
    sys.exit(2)


def print_section(pages: list[tuple[int, str]], section: str, label: str) -> None:
    rows = iter_lines(pages)
    candidates: list[int] = []
    section_pattern = re.compile(rf"^\s*(?:#{{1,6}}\s+)*{re.escape(section)}(?:\s|$)")
    for index, (_, line) in enumerate(rows):
        if section_pattern.match(line):
            candidates.append(index)

    if not candidates:
        print(f"Section not found: {section}", file=sys.stderr)
        sys.exit(1)

    if re.fullmatch(r"\d+(?:\.\d+)*", section):
        start_index = candidates[0]
    else:
        start_index = candidates[0]

    target_level = heading_level(section)
    output: list[tuple[int, str]] = []
    for page_number, line in rows[start_index:]:
        match = is_heading(line)
        if output and match:
            number = match.group(1)
            if re.fullmatch(r"\d+(?:\.\d+)*", number) and heading_level(number) <= target_level:
                break
            if not re.fullmatch(r"\d+(?:\.\d+)*", number) and target_level == 1:
                break
        output.append((page_number, line))

    tag_prefix = "section" if label == "md" else "pdf page"
    current_page = None
    for page_number, line in output:
        if page_number != current_page:
            current_page = page_number
            print(f"\n[{tag_prefix} {page_number}]")
        print(line)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", help="Search text in the standard.")
    group.add_argument("--section", help="Print a numbered section, e.g. 5.1.2 or 6.2.")
    group.add_argument("--page", type=int, help="Print extracted text for a page/section number.")
    group.add_argument("--list-sections", action="store_true", help="List detected numbered sections.")
    parser.add_argument("--context", type=int, default=80, help="Characters around each query match.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum query matches to print.")
    args = parser.parse_args()

    pages, label = load_pages()
    if args.list_sections:
        list_sections(pages, label)
    elif args.query:
        search_query(pages, args.query, args.context, args.limit, label)
    elif args.section:
        print_section(pages, args.section, label)
    elif args.page:
        dump_page(pages, args.page, label)


if __name__ == "__main__":
    main()
