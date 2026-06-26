"""
PDF → outline importer (uses PyMuPDF).

Extracts per-page text and classifies each page into a DeckCraft page type
using heuristics. Output is an outline dict that can be passed to
`scripts/generate_ppt.py` or `DeckEngine` directly.

Limitations (v5.3 first cut):
- Text-only extraction (no images, no tables with complex layouts)
- Page-type classification is heuristic — manual review of output recommended
- CJK text is supported via PyMuPDF's default extraction
"""
from typing import Dict, Any, List
import fitz  # PyMuPDF

from .base import (
    looks_like_cover, looks_like_toc, looks_like_section_divider,
    looks_like_table, looks_like_stats,
    extract_bullets, extract_table, extract_stats, extract_heading,
    make_outline_page,
)


def pdf_to_outline(
    pdf_path: str,
    page_types: List[str] = None,
    theme: str = "business",
    canvas: str = "16:9",
    max_pages: int = 200,
) -> Dict[str, Any]:
    """Convert a PDF file to a DeckCraft outline dict.

    Args:
        pdf_path: Path to the PDF file.
        page_types: Optional list of explicit page types, one per PDF page
                    (e.g. ["cover", "content", "table"]). Overrides heuristic.
        theme: Theme name to embed in outline (default: "business").
        canvas: Canvas preset (default: "16:9").
        max_pages: Max number of pages to process (safety limit, default: 200).

    Returns:
        Outline dict with 'pages' list. Each page has 'type' and required fields.
    """
    doc = fitz.open(pdf_path)
    total = min(len(doc), max_pages)
    pages: List[Dict[str, Any]] = []

    for page_idx in range(total):
        page = doc[page_idx]
        text = page.get_text("text").strip()
        if not text:
            continue  # skip blank pages

        # 1. Use explicit override if provided
        if page_types and page_idx < len(page_types):
            explicit = page_types[page_idx]
            pages.append(_build_page(explicit, text, page_idx == 0))
            continue

        # 2. Heuristic classification
        ptype = _classify_page(text, is_first_page=(page_idx == 0))
        pages.append(_build_page(ptype, text, page_idx == 0))

    doc.close()

    if not pages:
        # Edge case: empty or all-blank PDF
        pages.append(make_outline_page("cover", title="Imported from PDF"))

    return {
        "theme": theme,
        "canvas": canvas,
        "pages": pages,
    }


def _classify_page(text: str, is_first_page: bool) -> str:
    """Heuristic page-type classifier."""
    if looks_like_cover(text, is_first_page=is_first_page):
        return "cover"
    if looks_like_toc(text):
        return "toc"
    if looks_like_section_divider(text):
        return "section"
    if looks_like_table(text):
        return "table"
    if looks_like_stats(text):
        return "stat_cards"
    return "content"


def _build_page(ptype: str, text: str, is_first_page: bool) -> Dict[str, Any]:
    """Build a page dict from classified type and raw text."""
    if ptype == "cover":
        title = extract_heading(text) or "Imported Document"
        # Try to extract author/date from the first 5 lines
        lines = [l.strip() for l in text.split("\n") if l.strip()][:5]
        subtitle = lines[1] if len(lines) > 1 else ""
        author = lines[2] if len(lines) > 2 else ""
        date = lines[3] if len(lines) > 3 else ""
        return make_outline_page("cover", title=title, subtitle=subtitle,
                                 author=author, date=date)

    if ptype == "toc":
        # Extract numbered items
        import re
        items = []
        for line in text.split("\n"):
            m = re.match(r"^\s*(\d+|[IVX]+)[\.\)、\s]+(.+?)\s*[.…\-]{2,}\s*(\d+|[IVX]+)?\s*$", line)
            if m:
                num = m.group(1)
                title = m.group(2).strip()
                items.append([num, title, ""])
            else:
                # Try simpler pattern: "01  Title"
                m2 = re.match(r"^\s*(\d+)\s+(.{3,80})$", line.strip())
                if m2 and not m2.group(2).startswith(tuple("0123456789")):
                    items.append([m2.group(1), m2.group(2).strip(), ""])
        if not items:
            # Fallback: split by lines that look like items
            for line in text.split("\n"):
                line = line.strip()
                if 5 < len(line) < 80 and not line.endswith(":"):
                    items.append([str(len(items) + 1), line, ""])
        return make_outline_page("toc", items=items[:8])

    if ptype == "section":
        title = extract_heading(text) or text.strip().split("\n")[0]
        return make_outline_page("section", title=title)

    if ptype == "table":
        parsed = extract_table(text)
        if parsed:
            return make_outline_page("table", title=extract_heading(text) or "Data",
                                    headers=parsed["headers"], rows=parsed["rows"])
        # Fallback if no table structure detected
        bullets = extract_bullets(text)
        return make_outline_page("content", title=extract_heading(text) or "Content",
                                 bullets=bullets or [text[:100]])

    if ptype == "stat_cards":
        title = extract_heading(text) or "Key Stats"
        stats = extract_stats(text)
        if stats:
            return make_outline_page("stat_cards", title=title, stats=stats)
        # Fallback
        return make_outline_page("content", title=title, bullets=extract_bullets(text) or [text[:100]])

    # Default: content
    title = extract_heading(text) or "Slide"
    bullets = extract_bullets(text)
    if not bullets:
        # Last resort: use non-empty lines as bullets
        bullets = [l.strip() for l in text.split("\n") if 5 < len(l.strip()) < 200][:5]
    return make_outline_page("content", title=title, bullets=bullets,
                             key_point="")


__all__ = ["pdf_to_outline"]
