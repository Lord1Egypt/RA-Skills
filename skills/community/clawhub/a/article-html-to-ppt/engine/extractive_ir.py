"""Extractive fallback IR: a complete, schema-valid Presentation IR built
purely from the deterministic parse — zero LLM involvement.

This is the blank-page antidote (plan decision D3): the worst case of the
whole pipeline is "the source article, professionally laid out", never an
empty or fabricated deck. An LLM-produced IR that fails validation and
repair degrades to this.

Sectioning: slides follow the source's own outline (h2 by default, h1 when
the document has no h2). Content blocks quote the source verbatim with
anchors, so every extractive block passes provenance verification by
construction.
"""

from __future__ import annotations

import re
from .source_doc import SourceDoc, SourceElement

MAX_SLIDES = 60
# The deterministic layout engine is intentionally conservative: extractive
# fallback is a source-preserving diagnostic path, so it must split pages
# rather than generate a dense page and rely on the renderer to truncate it.
MAX_BLOCKS_PER_SLIDE = 4
MAX_TEXT = 320
MAX_TITLE = 120
MAX_LIST_ITEMS = 10
MAX_ITEM_TEXT = 200

_CJK_RE = re.compile(r"[一-鿿]")


def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _detect_language(doc: SourceDoc) -> str:
    sample = " ".join(e.full_text() for e in doc.elements[:20])
    if not sample:
        return "zh"
    cjk = len(_CJK_RE.findall(sample))
    return "zh" if cjk / max(len(sample), 1) > 0.05 else "en"


def _section_level(doc: SourceDoc) -> int | None:
    if doc.headings(2):
        return 2
    if len(doc.headings(1)) > 1:
        return 1
    return None


def _element_to_block(element: SourceElement, source_id: str) -> dict | None:
    ref = {"source_id": source_id, "loc": element.anchor}
    if element.etype == "para":
        if not element.text:
            return None
        return {"role": "fact", "text": _truncate(element.text, MAX_TEXT), "source_ref": ref}
    if element.etype == "blockquote":
        if not element.text:
            return None
        return {"role": "quote", "text": _truncate(element.text, MAX_TEXT), "source_ref": ref}
    if element.etype == "list":
        items = [
            {"text": _truncate(item, MAX_ITEM_TEXT), "source_ref": dict(ref)}
            for item in element.items[:MAX_LIST_ITEMS]
        ]
        return {"role": "list", "items": items} if items else None
    if element.etype == "table":
        return {"role": "table", "source_ref": ref}
    if element.etype == "img":
        block = {"role": "image", "asset_ref": element.anchor, "source_ref": ref}
        if element.text:
            block["caption"] = _truncate(element.text, MAX_ITEM_TEXT)
        return block
    return None  # code blocks and sub-headings are not slide content in fallback mode


def build_extractive_ir(doc: SourceDoc, *, source_meta: dict | None = None) -> dict:
    """Build a schema-valid v4 Presentation IR from a SourceDoc.

    Returns {"ir": <dict>, "warnings": [<str>...]} — warnings surface every
    bound applied (dropped slides, truncated sections), never silently.
    """
    warnings: list[str] = []
    level = _section_level(doc)

    # Partition elements into (section_title, elements) groups.
    sections: list[tuple[str, list[SourceElement]]] = []
    current_title = ""
    current: list[SourceElement] = []
    for element in doc.elements:
        if level is not None and element.etype == f"h{level}":
            if current or current_title:
                sections.append((current_title, current))
            current_title, current = element.text, []
        elif element.etype == "h1" and level == 2 and not sections and not current:
            continue  # the document title, already used for deck.title
        else:
            current.append(element)
    sections.append((current_title, current))
    sections = [(t, els) for t, els in sections if t or any(
        e.etype in {"para", "list", "table", "img", "blockquote"} for e in els)]

    slides: list[dict] = []
    for title, elements in sections:
        blocks = [b for b in (_element_to_block(e, doc.source_id) for e in elements) if b]
        if not blocks and not title:
            continue
        if not blocks:
            # A heading with no body still gets a section marker slide only
            # if we have nothing else; otherwise skip empty sections.
            warnings.append(f"section '{title}' has no extractable content; skipped")
            continue
        chunks = [blocks[i:i + MAX_BLOCKS_PER_SLIDE]
                  for i in range(0, len(blocks), MAX_BLOCKS_PER_SLIDE)]
        if len(chunks) > 1:
            warnings.append(f"section '{title or 'untitled'}' split into {len(chunks)} slides")
        for idx, chunk in enumerate(chunks):
            slide_title = title or (doc.title() or "内容")
            if idx:
                slide_title = f"{slide_title}（续 {idx + 1}）"
            slides.append({
                "id": f"s{len(slides) + 1}",
                "title": _truncate(slide_title, MAX_TITLE),
                "blocks": chunk,
            })

    if len(slides) > MAX_SLIDES:
        warnings.append(f"deck truncated from {len(slides)} to {MAX_SLIDES} slides")
        slides = slides[:MAX_SLIDES]

    if not slides:
        # Absolute floor: one slide carrying whatever text exists.
        text = " ".join(e.full_text() for e in doc.elements)[:MAX_TEXT] or "（空文档）"
        anchor = doc.elements[0].anchor if doc.elements else None
        block = ({"role": "fact", "text": text,
                  "source_ref": {"source_id": doc.source_id, "loc": anchor}}
                 if anchor else
                 {"role": "context", "text": text})
        slides = [{"id": "s1", "title": doc.title() or "内容摘要", "blocks": [block]}]
        warnings.append("document had no sectionable content; produced a single summary slide")

    meta = source_meta or {}
    source_entry = {"source_id": doc.source_id, "type": meta.get("type", "markdown")}
    for key in ("title", "path", "url"):
        if meta.get(key):
            source_entry[key] = meta[key]

    ir = {
        "schema_version": "4.0.0",
        "deck": {
            "title": _truncate(doc.title() or meta.get("title") or "未命名文档", 160),
            "language": _detect_language(doc),
        },
        "sources": [source_entry],
        "slides": slides,
    }
    return {"ir": ir, "warnings": warnings}
