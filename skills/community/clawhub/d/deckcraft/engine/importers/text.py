"""
Plain text / Markdown → outline importer.

Lightweight importer for .txt and .md files. Each non-empty paragraph becomes
a bullet, and headings (# Title) become section dividers.
"""
from typing import Dict, Any, List
import os
import re

from .base import extract_bullets, extract_heading, make_outline_page


HEADING_PATTERN = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)


def text_to_outline(
    text_path: str,
    theme: str = "business",
    canvas: str = "16:9",
    max_pages: int = 100,
) -> Dict[str, Any]:
    """Convert a .txt or .md file to outline dict.

    Headings (#, ##, ###) split the file into sections. Each section
    becomes one slide with the heading as title and body lines as bullets.

    Args:
        text_path: Path to .txt or .md file.
        theme: Theme name (default: "business").
        canvas: Canvas preset (default: "16:9").
        max_pages: Max slides to generate.

    Returns:
        Outline dict with 'pages' list.
    """
    with open(text_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    # Split by heading
    sections = []
    current = {"title": "", "body": []}
    pos = 0
    for m in HEADING_PATTERN.finditer(text):
        if m.start() > pos:
            chunk = text[pos:m.start()].strip()
            if chunk:
                current["body"].append(chunk)
        if current["title"] or current["body"]:
            sections.append(current)
        current = {"title": m.group(2).strip(), "body": []}
        pos = m.end()
    if pos < len(text):
        chunk = text[pos:].strip()
        if chunk:
            current["body"].append(chunk)
    if current["title"] or current["body"]:
        sections.append(current)

    if not sections:
        return {
            "theme": theme,
            "canvas": canvas,
            "pages": [make_outline_page("cover", title=os.path.basename(text_path))],
        }

    pages: List[Dict[str, Any]] = []

    for i, section in enumerate(sections):
        if len(pages) >= max_pages:
            break

        body_text = "\n".join(section["body"])
        bullets = extract_bullets(body_text)

        if i == 0:
            # First section = cover
            pages.append(make_outline_page(
                "cover",
                title=section["title"] or os.path.basename(text_path),
                subtitle=bullets[0] if bullets else "",
            ))
        else:
            pages.append(make_outline_page(
                "content",
                title=section["title"] or "Section",
                bullets=bullets or [body_text[:200]],
            ))

    # Append closing
    if pages and pages[-1].get("type") != "closing":
        pages.append(make_outline_page("closing", title="Thank You"))

    return {
        "theme": theme,
        "canvas": canvas,
        "pages": pages,
    }


__all__ = ["text_to_outline"]
