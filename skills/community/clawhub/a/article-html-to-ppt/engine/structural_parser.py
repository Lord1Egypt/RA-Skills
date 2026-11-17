"""Deterministic structural parser: Markdown / HTML / plain text -> SourceDoc.

This is Evidence A of the dual-evidence design: everything here is derived
from document structure alone, with no model involvement. The anchors it
emits are the only valid targets for IR source_refs, and the extractive
fallback IR is built purely from its output.

Stdlib only. Markdown covers the CommonMark/GFM subset that matters for
articles: headings, paragraphs, fenced code, blockquotes, ordered/unordered
lists, pipe tables, standalone images. HTML uses html.parser and covers
h1-h6, p, ul/ol/li, table/tr/th/td, blockquote, pre, img.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

from .source_doc import SourceDoc

_MD_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_MD_ULIST = re.compile(r"^\s*[-*+]\s+(.*)$")
_MD_OLIST = re.compile(r"^\s*\d+[.)]\s+(.*)$")
_MD_IMAGE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
_MD_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
_INLINE_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_INLINE_IMG = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_INLINE_MARKS = re.compile(r"(\*\*|__|\*|_|`|~~)")


def _clean_inline(text: str) -> str:
    text = _INLINE_IMG.sub(lambda m: m.group(1), text)
    text = _INLINE_LINK.sub(lambda m: m.group(1), text)
    return _INLINE_MARKS.sub("", text)


def _split_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_markdown(text: str, source_id: str) -> SourceDoc:
    doc = SourceDoc(source_id=source_id)
    lines = text.splitlines()
    i, n = 0, len(lines)
    para_buf: list[str] = []

    def flush_para() -> None:
        if para_buf:
            doc.add("para", _clean_inline(" ".join(para_buf)))
            para_buf.clear()

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            i += 1
            continue

        if stripped.startswith("```"):
            flush_para()
            fence: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                fence.append(lines[i])
                i += 1
            i += 1  # closing fence
            doc.add("code", "\n".join(fence))
            continue

        m = _MD_HEADING.match(stripped)
        if m:
            flush_para()
            level = len(m.group(1))
            doc.add(f"h{level}", _clean_inline(m.group(2)), level=level)
            i += 1
            continue

        m = _MD_IMAGE.match(stripped)
        if m:
            flush_para()
            doc.add("img", _clean_inline(m.group(1)), src=m.group(2).strip())
            i += 1
            continue

        if stripped.startswith(">"):
            flush_para()
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            doc.add("blockquote", _clean_inline(" ".join(q for q in quote if q)))
            continue

        if "|" in stripped and i + 1 < n and _MD_TABLE_SEP.match(lines[i + 1]):
            flush_para()
            rows = [_split_table_row(stripped)]
            i += 2  # skip separator
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(_split_table_row(lines[i]))
                i += 1
            width = len(rows[0])
            doc.add("table", "", rows=[
                [_clean_inline(c) for c in (row + [""] * width)[:width]] for row in rows
            ])
            continue

        if _MD_ULIST.match(stripped) or _MD_OLIST.match(stripped):
            flush_para()
            items: list[str] = []
            while i < n:
                s = lines[i].strip()
                m = _MD_ULIST.match(s) or _MD_OLIST.match(s)
                if not m:
                    break
                items.append(_clean_inline(m.group(1)))
                i += 1
            doc.add("list", "", items=items)
            continue

        para_buf.append(stripped)
        i += 1

    flush_para()
    return doc


class _HtmlToDoc(HTMLParser):
    _HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
    _SKIP = {"script", "style", "head", "nav", "footer"}

    def __init__(self, doc: SourceDoc) -> None:
        super().__init__(convert_charrefs=True)
        self.doc = doc
        self._text: list[str] = []
        self._context: list[str] = []
        self._items: list[str] = []
        self._rows: list[list[str]] = []
        self._cells: list[str] = []
        self._skip_depth = 0

    def _in(self, tag: str) -> bool:
        return tag in self._context

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self._SKIP:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in self._HEADINGS or tag in {"p", "blockquote", "pre"}:
            self._text = []
            self._context.append(tag)
        elif tag in {"ul", "ol"} and not self._in("ul") and not self._in("ol"):
            self._items = []
            self._context.append(tag)
        elif tag == "li":
            self._text = []
            self._context.append(tag)
        elif tag == "table":
            self._rows = []
            self._context.append(tag)
        elif tag == "tr":
            self._cells = []
            self._context.append(tag)
        elif tag in {"td", "th"}:
            self._text = []
            self._context.append(tag)
        elif tag == "img":
            src = dict(attrs).get("src", "") or ""
            alt = dict(attrs).get("alt", "") or ""
            self.doc.add("img", alt, src=src)

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth or not self._context:
            return
        if self._context[-1] != tag:
            if tag in self._context:
                while self._context and self._context[-1] != tag:
                    self._context.pop()
            else:
                return
        self._context.pop()
        text = "".join(self._text).strip()
        if tag in self._HEADINGS:
            if text:
                self.doc.add(tag, text, level=int(tag[1]))
        elif tag == "p":
            if text and not self._in("li") and not self._in("td") and not self._in("th"):
                self.doc.add("para", text)
            elif text:
                self._text = [text]
                return
        elif tag == "blockquote":
            if text:
                self.doc.add("blockquote", text)
        elif tag == "pre":
            if text:
                self.doc.add("code", text)
        elif tag == "li":
            if text:
                self._items.append(text)
        elif tag in {"ul", "ol"}:
            if self._items:
                self.doc.add("list", "", items=self._items)
            self._items = []
        elif tag in {"td", "th"}:
            self._cells.append(text)
        elif tag == "tr":
            if self._cells:
                self._rows.append(self._cells)
            self._cells = []
        elif tag == "table":
            if self._rows:
                width = max(len(r) for r in self._rows)
                self.doc.add("table", "", rows=[
                    (row + [""] * width)[:width] for row in self._rows
                ])
            self._rows = []
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._context and self._context[-1] in (
            self._HEADINGS | {"p", "blockquote", "pre", "li", "td", "th"}
        ):
            self._text.append(data)


def parse_html(text: str, source_id: str) -> SourceDoc:
    doc = SourceDoc(source_id=source_id)
    parser = _HtmlToDoc(doc)
    parser.feed(text)
    parser.close()
    return doc


_PLAIN_CHAPTER_RE = re.compile(r"^(?:chapter|part)\s+(?:\d+|[ivxlcdm]+)\b", re.IGNORECASE)
_PLAIN_SECTION_RE = re.compile(r"^[A-Z][A-Z0-9 &/,:-]{2,80}$")


def _plain_heading_level(chunk: str) -> int | None:
    """Recognize only unambiguous headings from PDF-to-text output.

    PDF extractors commonly lose Markdown markers but preserve standalone
    chapter labels and all-caps section names. Keeping this intentionally
    narrow prevents body sentences from becoming invented document structure.
    """
    normalized = re.sub(r"\s+", " ", chunk).strip()
    if _PLAIN_CHAPTER_RE.match(normalized):
        return 1
    if _PLAIN_SECTION_RE.fullmatch(normalized) and any(c.isalpha() for c in normalized):
        return 2
    return None


def parse_plain_text(text: str, source_id: str) -> SourceDoc:
    doc = SourceDoc(source_id=source_id)
    for chunk in re.split(r"\n\s*\n", text.replace("\f", "\n")):
        chunk = chunk.strip()
        if not chunk:
            continue
        level = _plain_heading_level(chunk)
        if level is not None:
            doc.add(f"h{level}", chunk, level=level)
        else:
            doc.add("para", chunk)
    return doc


def parse_source(text: str, source_type: str, source_id: str) -> SourceDoc:
    """Dispatch on the IR source.type vocabulary (markdown/html/text)."""
    if source_type == "markdown":
        return parse_markdown(text, source_id)
    if source_type == "html":
        return parse_html(text, source_id)
    if source_type == "text":
        return parse_plain_text(text, source_id)
    raise ValueError(f"unsupported source type for structural parsing: {source_type}")
