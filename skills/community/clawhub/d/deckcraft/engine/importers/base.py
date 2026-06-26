"""
Shared helpers for source importers.
"""
import re
import os
from typing import List, Dict, Any, Optional


# ── Heuristics: classify text content into page types ────────────────────

AGENDAS = re.compile(
    r"^\s*(agenda|contents?|table\s+of\s+contents|目录|大纲|议程)\s*$"
    r"|^\s*(agenda|contents?)\s*[\.\:—\-]",
    re.IGNORECASE | re.MULTILINE,
)

# Numbered-list pattern: "01  Title", "1. Title", "I. Title" — at least 3 such lines
NUMBERED_LIST = re.compile(r"^\s*\d+[\.\s\)]\s+\S", re.MULTILINE)
SECTION_DIVIDERS = re.compile(r"^\s*(part|chapter|section|模块|章节)\s*\d", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"^(#{1,3}\s+.+|[A-Z][A-Za-z0-9 ,\-—&:/]{4,80})$")
BULLET_PATTERN = re.compile(r"^\s*[•●○\-*→▪]\s+(.+)")
NUMBER_BULLET_PATTERN = re.compile(r"^\s*(\d+)[\.\)、]\s+(.+)")
LARGE_NUMBER_PATTERN = re.compile(r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?%?)\b")
STAT_PATTERN = re.compile(r"^([\d$€¥£]+(?:\.\d+)?[%KMBkmb]?)\s+(.{3,40})$")


def looks_like_cover(text: str, is_first_page: bool = False) -> bool:
    """Cover slide: short text, large title, often centered. First page is often a cover."""
    if not text:
        return False
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    # Heuristic: a cover is short and on the first page
    if is_first_page and len(lines) <= 5 and len(text) < 300:
        return True
    return False


def looks_like_toc(text: str) -> bool:
    """TOC: 'Agenda' / '目录' / numbered list of chapters."""
    if AGENDAS.search(text[:200]):
        return True
    # Heuristic: 3+ numbered lines at start of lines = numbered list (could be TOC)
    numbered_lines = NUMBERED_LIST.findall(text)
    if len(numbered_lines) >= 3:
        # And those lines should be short (titles, not paragraphs)
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        numbered_line_texts = [l for l in lines if NUMBERED_LIST.match(l)]
        if numbered_line_texts and all(len(l) <= 80 for l in numbered_line_texts):
            return True
    return False


def looks_like_section_divider(text: str) -> bool:
    """Section divider: single short line, all caps, or 'Part N' / 'Section N'."""
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    if len(lines) == 1 and len(lines[0]) < 60:
        return SECTION_DIVIDERS.match(lines[0]) or lines[0].isupper()
    return False


def looks_like_table(text: str) -> bool:
    """Table: multiple rows of | col1 | col2 | ... or aligned columns."""
    lines = [l for l in text.split("\n") if l.strip()]
    pipe_lines = [l for l in lines if "|" in l and l.count("|") >= 2]
    if len(pipe_lines) >= 3:
        return True
    # Heuristic: 3+ short lines with similar structure
    if len(lines) >= 3 and all(20 < len(l) < 80 for l in lines[:5]):
        return True
    return False


def looks_like_stats(text: str) -> bool:
    """Stats: lines like '99%  Uptime' or '$2M  Revenue'."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    stat_lines = [l for l in lines if STAT_PATTERN.match(l)]
    return len(stat_lines) >= 2


def extract_bullets(text: str) -> List[str]:
    """Extract bullet items from text, returning a list of strings."""
    bullets = []
    for line in text.split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        m = BULLET_PATTERN.match(line)
        if m:
            bullets.append(m.group(1).strip())
            continue
        m = NUMBER_BULLET_PATTERN.match(line)
        if m:
            bullets.append(m.group(2).strip())
            continue
        # Plain line — only include if short
        if line.startswith("  ") or line.startswith("\t"):
            continue  # indented = sub-bullet, skip
        if 10 < len(line) < 200:
            bullets.append(line.strip())
    return bullets[:15]  # cap at 15


def extract_table(text: str) -> Optional[Dict[str, Any]]:
    """Parse a markdown-style or pipe-delimited table."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    pipe_lines = [l for l in lines if "|" in l and l.count("|") >= 2]
    if len(pipe_lines) < 2:
        return None

    def parse_row(line: str) -> List[str]:
        return [c.strip() for c in line.strip("|").split("|")]

    headers = parse_row(pipe_lines[0])
    # Skip separator row if present (|---|---|)
    rows = []
    for line in pipe_lines[1:]:
        if re.match(r"^\|?[\s\-:|]+\|?$", line):
            continue
        rows.append(parse_row(line))
    if not rows:
        return None
    return {"headers": headers, "rows": rows}


def extract_stats(text: str) -> List[tuple]:
    """Extract stat cards (number, label) pairs from text."""
    stats = []
    for line in text.split("\n"):
        line = line.strip()
        m = STAT_PATTERN.match(line)
        if m:
            stats.append((m.group(1), m.group(2)))
    return stats[:6]  # cap at 6


def extract_heading(text: str) -> Optional[str]:
    """Extract the first non-empty line as a heading (likely the page title)."""
    for line in text.split("\n"):
        line = line.strip()
        if line and 3 < len(line) < 120:
            # Skip pure bullet lines
            if not BULLET_PATTERN.match(line) and not NUMBER_BULLET_PATTERN.match(line):
                return line
    return None


def make_outline_page(page_type: str, **kwargs) -> Dict[str, Any]:
    """Helper to construct a page dict with type and other fields."""
    page = {"type": page_type}
    page.update(kwargs)
    return page


# ── Entry: detect and import any supported format ──────────────────────

def detect_and_import(file_path: str, **kwargs) -> Dict[str, Any]:
    """Auto-detect file type by extension and import to outline dict.

    Args:
        file_path: Path to PDF, DOCX, or .txt file.
        **kwargs: Forwarded to the specific importer.

    Returns:
        Outline dict with 'pages' list (and optional 'theme'/'canvas').

    Raises:
        ValueError: If file format is unsupported.
        FileNotFoundError: If file doesn't exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Source file not found: {file_path!r}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        from .pdf import pdf_to_outline
        return pdf_to_outline(file_path, **kwargs)
    elif ext == ".docx":
        from .docx import docx_to_outline
        # docx_to_outline doesn't accept page_types — drop it
        kwargs.pop("page_types", None)
        return docx_to_outline(file_path, **kwargs)
    elif ext in (".txt", ".md"):
        from .text import text_to_outline
        # text_to_outline doesn't accept page_types either
        kwargs.pop("page_types", None)
        return text_to_outline(file_path, **kwargs)
    else:
        raise ValueError(
            f"Unsupported file format: {ext!r}. Supported: .pdf, .docx, .txt, .md"
        )
