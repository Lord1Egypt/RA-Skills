"""Source-anchored evidence outline for structured-IR planning."""

from __future__ import annotations

from .source_doc import SourceDoc


def build_evidence_outline(doc: SourceDoc) -> dict:
    """Group every extractable element under the latest recovered heading.

    This is intentionally a planning artifact, not a Presentation IR: it
    preserves all source anchors and never claims that raw report text is
    already an audience-ready narrative.
    """
    sections: list[dict] = []
    current: dict | None = None
    in_contents = False
    for element in doc.elements:
        if element.etype in {"h1", "h2", "h3"}:
            title = element.text.strip()
            in_contents = title.casefold() in {"contents", "table of contents"}
            current = {
                "id": element.anchor,
                "title": title,
                "level": element.level,
                "evidence": [],
            }
            sections.append(current)
            continue
        if element.etype not in {"para", "list", "table", "blockquote", "img"}:
            continue
        # Contents pages are navigation metadata, not source evidence.
        if in_contents:
            continue
        if current is None:
            current = {"id": "preamble", "title": "Preamble", "level": 0, "evidence": []}
            sections.append(current)
        item = {"anchor": element.anchor, "type": element.etype}
        text = element.full_text()
        if text:
            item["text"] = text
        numbers = sorted(element.numbers())
        if numbers:
            item["numbers"] = numbers
        current["evidence"].append(item)
    sections = [section for section in sections if section["evidence"]]
    return {
        "schema_version": "4.0.0",
        "source_id": doc.source_id,
        "title": doc.title(),
        "section_count": len(sections),
        "evidence_count": sum(len(section["evidence"]) for section in sections),
        "sections": sections,
    }
