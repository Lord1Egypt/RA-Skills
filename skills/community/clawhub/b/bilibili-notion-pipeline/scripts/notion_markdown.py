from __future__ import annotations

import re
from typing import List, Dict


def _rt(text: str) -> list[dict]:
    return [{"type": "text", "text": {"content": text[:2000]}}]


def _block(kind: str, text: str = "") -> dict:
    if kind == "divider":
        return {"object": "block", "type": "divider", "divider": {}}
    return {"object": "block", "type": kind, kind: {"rich_text": _rt(text)}}


def markdown_to_blocks(markdown: str) -> List[Dict]:
    blocks: List[Dict] = []
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        text = " ".join([x.strip() for x in paragraph_lines]).strip()
        if text:
            blocks.append(_block("paragraph", text))
        paragraph_lines = []

    for raw in markdown.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            continue

        if stripped == "---":
            flush_paragraph()
            blocks.append(_block("divider"))
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            blocks.append(_block("heading_3", stripped[4:]))
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            blocks.append(_block("heading_2", stripped[3:]))
            continue
        if stripped.startswith("# "):
            flush_paragraph()
            blocks.append(_block("heading_1", stripped[2:]))
            continue
        if stripped.startswith("> "):
            flush_paragraph()
            blocks.append(_block("quote", stripped[2:]))
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            blocks.append(_block("bulleted_list_item", stripped[2:]))
            continue
        if re.match(r"^\d+\.\s+", stripped):
            flush_paragraph()
            text = re.sub(r"^\d+\.\s+", "", stripped)
            blocks.append(_block("numbered_list_item", text))
            continue

        paragraph_lines.append(stripped)

    flush_paragraph()
    return blocks
