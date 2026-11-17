"""SourceDoc: the deterministic parse result every anchor points into.

Anchor grammar (frozen in schemas/v4/presentation-ir.schema.json):
``<element>_<index>`` with optional ``#start-end`` character span, e.g.
``para_12``, ``h2_3``, ``table_1``, ``list_4#0-20``. Indexes are 1-based
per element type in document order, so an anchor is stable for a given
source text regardless of who produced the IR.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

ANCHOR_RE = re.compile(r"^([a-z][a-z0-9]*)_([0-9]+)(?:#([0-9]+)-([0-9]+))?$")

# Element types the parser may emit. Heading anchors use h1..h6.
ELEMENT_TYPES = {
    "h1", "h2", "h3", "h4", "h5", "h6",
    "para", "list", "table", "img", "blockquote", "code",
}

_NUMBER_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?%?")


def normalize_text(text: str) -> str:
    """NFKC-normalize and collapse whitespace.

    NFKC folds full-width digits/percent signs common in Chinese sources
    into ASCII, so provenance matching behaves the same for 36% and ３６％.
    """
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def extract_numbers(text: str) -> set[str]:
    """Return canonical numeric tokens found in text (commas stripped)."""
    return {m.group(0).replace(",", "") for m in _NUMBER_RE.finditer(normalize_text(text))}


@dataclass
class SourceElement:
    anchor: str
    etype: str
    text: str
    level: int = 0
    items: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    src: str = ""

    def numbers(self) -> set[str]:
        parts = [self.text, *self.items]
        for row in self.rows:
            parts.extend(row)
        found: set[str] = set()
        for part in parts:
            found |= extract_numbers(part)
        return found

    def full_text(self) -> str:
        parts = [self.text, *self.items]
        for row in self.rows:
            parts.extend(row)
        return normalize_text(" ".join(p for p in parts if p))


@dataclass
class SourceDoc:
    source_id: str
    elements: list[SourceElement] = field(default_factory=list)
    _by_anchor: dict[str, SourceElement] = field(default_factory=dict)
    _counters: dict[str, int] = field(default_factory=dict)

    def add(self, etype: str, text: str, *, level: int = 0,
            items: list[str] | None = None, rows: list[list[str]] | None = None,
            src: str = "") -> SourceElement:
        if etype not in ELEMENT_TYPES:
            raise ValueError(f"unknown element type: {etype}")
        self._counters[etype] = self._counters.get(etype, 0) + 1
        element = SourceElement(
            anchor=f"{etype}_{self._counters[etype]}",
            etype=etype,
            text=normalize_text(text),
            level=level,
            items=[normalize_text(i) for i in (items or []) if normalize_text(i)],
            rows=[[normalize_text(c) for c in row] for row in (rows or [])],
            src=src,
        )
        self.elements.append(element)
        self._by_anchor[element.anchor] = element
        return element

    def get(self, anchor: str) -> SourceElement | None:
        return self._by_anchor.get(anchor)

    def headings(self, level: int | None = None) -> list[SourceElement]:
        return [e for e in self.elements
                if e.etype.startswith("h") and e.etype in ELEMENT_TYPES
                and (level is None or e.etype == f"h{level}")]

    def tables(self) -> list[SourceElement]:
        return [e for e in self.elements if e.etype == "table"]

    def title(self) -> str:
        h1 = self.headings(1)
        return h1[0].text if h1 else ""

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "element_count": len(self.elements),
            "elements": [
                {
                    "anchor": e.anchor,
                    "type": e.etype,
                    "text": e.text,
                    **({"items": e.items} if e.items else {}),
                    **({"rows": e.rows} if e.rows else {}),
                    **({"src": e.src} if e.src else {}),
                }
                for e in self.elements
            ],
        }


def parse_anchor(loc: str) -> tuple[str, int, tuple[int, int] | None] | None:
    """Split an anchor into (etype, index, optional span); None if malformed."""
    m = ANCHOR_RE.match(loc)
    if not m:
        return None
    etype, index = m.group(1), int(m.group(2))
    span = (int(m.group(3)), int(m.group(4))) if m.group(3) is not None else None
    return etype, index, span
