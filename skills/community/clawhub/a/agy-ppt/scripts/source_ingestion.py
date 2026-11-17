#!/usr/bin/env python3
"""Deterministic source ingestion & locator extraction (Phase 13.1 + 13.2).

This module turns a **local** source file into normalized, deterministically
identified extraction *blocks* with source-format-native *locators*. It is the
upstream producer for the Phase 12 grounding system:

    local source
      -> format detection
      -> deterministic extractor
      -> normalized extracted blocks + locators   <-- this module
      -> AGY semantic segmentation
      -> Phase 12 source_inventory.json
      -> Phase 12 grounding workflow

Hard boundary, and the reason this lives outside ``source_grounding.py``:

    extraction != semantic understanding

This module decides only what a document mechanically contains: which page a
run of text sits on, which Markdown heading encloses it, which line range a
paragraph spans. It never decides what is important, what a claim means,
whether a source supports a claim, what belongs on a slide, or how the source
should be semantically segmented. Those are AGY decisions, and an extracted
block is therefore **not** a Phase 12 semantic source unit.

Scope of Phase 13.2-13.4: PDF with an extractable text layer, Markdown, plain
text, DOCX, and local static HTML, all read from the local filesystem. There is
no OCR, no network acquisition, no browser and no JavaScript execution -- each
unsupported case fails deterministically rather than silently degrading.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
import sys  # noqa: E402

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# The one canonical source-fingerprint definition lives in Phase 12; Phase 13
# delegates to it instead of inventing a second, incompatible digest meaning.
from source_grounding import compute_source_digest  # noqa: E402

# ---------------------------------------------------------------------------
# Versions
# ---------------------------------------------------------------------------
#: Shape of the extraction result document.
SCHEMA_VERSION = "1"

#: Version of the *extraction behaviour*. Deliberately independent of the
#: release version and of Git tags: if extraction rules ever change, persisted
#: results stay identifiable. Bump this when block/locator output changes.
EXTRACTOR_VERSION = "1"

# ---------------------------------------------------------------------------
# Formats
# ---------------------------------------------------------------------------
FORMAT_PDF = "pdf"
FORMAT_MARKDOWN = "markdown"
FORMAT_TEXT = "text"
FORMAT_DOCX = "docx"
FORMAT_HTML = "html"
FORMAT_UNSUPPORTED = "unsupported"

SUPPORTED_FORMATS = (
    FORMAT_PDF,
    FORMAT_MARKDOWN,
    FORMAT_TEXT,
    FORMAT_DOCX,
    FORMAT_HTML,
)

MARKDOWN_SUFFIXES = (".md", ".markdown", ".mdown")
TEXT_SUFFIXES = (".txt", ".text")
PDF_SUFFIXES = (".pdf",)
DOCX_SUFFIXES = (".docx",)
HTML_SUFFIXES = (".html", ".htm")

#: Every PDF must start with this signature; extension alone is never trusted.
PDF_SIGNATURE = b"%PDF-"

#: A DOCX is an OOXML ZIP package, so it starts with the local-file-header magic.
ZIP_SIGNATURE = b"PK\x03\x04"

#: The part that distinguishes a word-processing package from any other ZIP or
#: from a spreadsheet/presentation OOXML package.
DOCX_BODY_PART = "word/document.xml"

#: Markers that identify an HTML document by content rather than by extension.
#: Deliberately conservative: a stray ``<div>`` inside a text file is not enough.
HTML_MARKERS = (b"<!doctype html", b"<html", b"<head", b"<body")

#: How many leading bytes are inspected when sniffing for HTML markers.
HTML_SNIFF_BYTES = 4096

# ---------------------------------------------------------------------------
# Block types
# ---------------------------------------------------------------------------
BLOCK_PAGE = "page"
BLOCK_MARKDOWN_SECTION = "markdown_section"
BLOCK_PARAGRAPH = "paragraph"
BLOCK_DOCX_SECTION = "docx_section"
BLOCK_DOCX_TABLE = "docx_table"
BLOCK_HTML_SECTION = "html_section"
BLOCK_HTML_LIST = "html_list"
BLOCK_HTML_TABLE = "html_table"

# ---------------------------------------------------------------------------
# Error taxonomy
# ---------------------------------------------------------------------------
# Deliberately disjoint from the Phase 12 grounding codes and the image-worker
# codes: an ingestion problem must never be recorded as a traceability,
# coverage or image-generation failure.
ERROR_SOURCE_FORMAT_UNSUPPORTED = "SOURCE_FORMAT_UNSUPPORTED"
ERROR_SOURCE_FILE_NOT_FOUND = "SOURCE_FILE_NOT_FOUND"
ERROR_SOURCE_READ_FAILED = "SOURCE_READ_FAILED"
ERROR_SOURCE_ENCODING_UNSUPPORTED = "SOURCE_ENCODING_UNSUPPORTED"
ERROR_SOURCE_TEXT_UNAVAILABLE = "SOURCE_TEXT_UNAVAILABLE"
ERROR_SOURCE_EXTRACTION_FAILED = "SOURCE_EXTRACTION_FAILED"

_SOURCE_ID_RE = re.compile(r"^src_[A-Za-z0-9._-]+$")


class SourceIngestionError(Exception):
    """Base error carrying a stable error_code, matching project_state.py."""

    error_code = ERROR_SOURCE_EXTRACTION_FAILED

    def __init__(self, message: str, error_code: str | None = None) -> None:
        super().__init__(message)
        if error_code is not None:
            self.error_code = error_code


class SourceFormatUnsupported(SourceIngestionError):
    error_code = ERROR_SOURCE_FORMAT_UNSUPPORTED


class SourceFileNotFound(SourceIngestionError):
    error_code = ERROR_SOURCE_FILE_NOT_FOUND


class SourceReadFailed(SourceIngestionError):
    error_code = ERROR_SOURCE_READ_FAILED


class SourceEncodingUnsupported(SourceIngestionError):
    error_code = ERROR_SOURCE_ENCODING_UNSUPPORTED


class SourceTextUnavailable(SourceIngestionError):
    error_code = ERROR_SOURCE_TEXT_UNAVAILABLE


class SourceExtractionFailed(SourceIngestionError):
    error_code = ERROR_SOURCE_EXTRACTION_FAILED


# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------
def compute_block_id(source_id: str, locator: dict[str, Any], ordinal: int) -> str:
    """Deterministic, resume-safe, source-local block id.

    Derived from ``(source_id, canonical locator, ordinal)`` only. It never
    depends on an absolute filesystem path, a temporary directory, a process
    id, a timestamp, or a bare random UUID, so re-ingesting identical bytes
    with the same extractor version always reproduces the same id.
    """
    if not _SOURCE_ID_RE.match(source_id or ""):
        raise SourceIngestionError(
            f"invalid source_id: {source_id!r} (expected ^src_[A-Za-z0-9._-]+$)"
        )
    canonical = json.dumps(locator, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(
        f"{source_id}\n{canonical}\n{ordinal}".encode("utf-8")
    ).hexdigest()[:12]
    return f"blk:{source_id}:{digest}"


# ---------------------------------------------------------------------------
# Result contract
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ExtractedBlock:
    """One mechanically extracted run of text plus where it came from."""

    block_id: str
    block_type: str
    text: str
    locator: dict[str, Any]
    ordinal: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "block_id": self.block_id,
            "block_type": self.block_type,
            "text": self.text,
            "locator": dict(self.locator),
            "ordinal": self.ordinal,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ExtractionResult:
    """Normalized extraction result handed to AGY for semantic segmentation."""

    schema_version: str
    extractor_version: str
    source_id: str
    source_format: str
    source_digest: str
    blocks: tuple[ExtractedBlock, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "extractor_version": self.extractor_version,
            "source_id": self.source_id,
            "source_format": self.source_format,
            "source_digest": self.source_digest,
            "blocks": [b.to_dict() for b in self.blocks],
        }

    @property
    def block_count(self) -> int:
        return len(self.blocks)


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------
def _zip_package_format(path: Path) -> str:
    """Classify a ZIP-signature file without doing any semantic analysis.

    Enough structure is inspected to tell a word-processing OOXML package apart
    from an ordinary ZIP, a corrupted ZIP, and a non-word Office package
    (spreadsheet/presentation), which is all detection needs to decide routing.
    """
    import zipfile

    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
    except (zipfile.BadZipFile, OSError):
        # A broken container. Only claim DOCX when the extension says so, so
        # that extraction can report a DOCX-specific deterministic failure.
        return FORMAT_DOCX if path.suffix.lower() in DOCX_SUFFIXES else FORMAT_UNSUPPORTED

    if DOCX_BODY_PART in names:
        return FORMAT_DOCX
    return FORMAT_UNSUPPORTED


def detect_source_format(path: str | Path) -> str:
    """The single deterministic format authority for Phase 13.

    Resolution order:

    1. If the file begins with the ``%PDF-`` signature it is treated as PDF,
       whatever the extension says. The signature wins so that a mislabelled
       or extension-less PDF is still routed to the PDF extractor.
    2. If the file begins with the ZIP signature it is inspected as an OOXML
       package: it is ``docx`` only when it actually contains
       ``word/document.xml``. An ordinary ZIP, a spreadsheet package, or a
       presentation package is therefore *not* misclassified as DOCX.
    3. Otherwise the extension selects Markdown or plain text, since a text
       file has no signature to validate against.
    4. A ``.docx`` extension with no ZIP signature -- which is how a
       password-protected DOCX appears, since it is wrapped in an OLE/CFB
       container -- is still routed to DOCX so that extraction can fail with a
       DOCX-specific diagnostic rather than a vague unsupported-format error.
    5. Anything else -- including a file merely *named* ``.pdf`` without a PDF
       signature -- is ``unsupported``.
    """
    p = Path(os.path.expanduser(str(path)))
    if not p.is_file():
        raise SourceFileNotFound(f"source file not found: {p.name}")
    try:
        with p.open("rb") as fh:
            head = fh.read(HTML_SNIFF_BYTES)
    except OSError as exc:
        raise SourceReadFailed(f"could not read source file: {exc}")

    if head.startswith(PDF_SIGNATURE):
        return FORMAT_PDF
    if head.startswith(ZIP_SIGNATURE):
        return _zip_package_format(p)

    suffix = p.suffix.lower()
    if suffix in MARKDOWN_SUFFIXES:
        return FORMAT_MARKDOWN
    if suffix in TEXT_SUFFIXES:
        return FORMAT_TEXT
    if suffix in DOCX_SUFFIXES:
        return FORMAT_DOCX

    lowered = head.lower()
    if suffix in HTML_SUFFIXES:
        # Trust the extension only when the content does not contradict it:
        # a file named .html with no element markup at all is not HTML.
        return FORMAT_HTML if _HTML_TAG_RE.search(head) else FORMAT_UNSUPPORTED
    if any(marker in lowered for marker in HTML_MARKERS):
        # Extension-less or oddly named HTML is still routed to HTML, but only
        # on an html-specific marker -- never on the presence of any tag, so
        # generic XML is not misclassified.
        return FORMAT_HTML
    return FORMAT_UNSUPPORTED


# ---------------------------------------------------------------------------
# Text decoding
# ---------------------------------------------------------------------------
def _decode_text(raw: bytes) -> str:
    """Decode UTF-8 (with or without BOM) and normalize line endings.

    ``utf-8-sig`` transparently strips a leading BOM and is otherwise plain
    UTF-8. CRLF and lone CR are normalized to LF so that line numbering is
    identical across platforms. This normalization applies only to the
    *extracted text*: the Phase 12 source digest is always computed over the
    raw, unnormalized bytes.
    """
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise SourceEncodingUnsupported(
            f"source is not valid UTF-8 (or UTF-8 with BOM): {exc.reason}"
        )
    return text.replace("\r\n", "\n").replace("\r", "\n")


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------
def extract_pdf(raw: bytes, source_id: str) -> list[ExtractedBlock]:
    """Page-level extraction from a PDF that has a real text layer.

    Granularity is deliberately page-level: it is the one division a PDF
    reliably exposes without guessing at layout. Page numbers in the locator
    are 1-based, matching what a reader sees, never a library's 0-based index.

    A structurally broken PDF raises :class:`SourceExtractionFailed`. A
    structurally valid PDF with no extractable text -- the scanned/image-only
    case -- raises :class:`SourceTextUnavailable`. There is no OCR fallback,
    so neither case can silently return an empty success.
    """
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise SourceExtractionFailed(f"pypdf is required for PDF ingestion: {exc}")

    import io
    import logging

    # pypdf logs recovery warnings for damaged files; keep ordinary
    # unsupported-source handling quiet rather than noisy.
    pypdf_log = logging.getLogger("pypdf")
    previous_level = pypdf_log.level
    pypdf_log.setLevel(logging.ERROR)
    try:
        try:
            reader = PdfReader(io.BytesIO(raw))
            pages = list(reader.pages)
        except Exception as exc:
            raise SourceExtractionFailed(f"PDF structure could not be parsed: {exc}")

        blocks: list[ExtractedBlock] = []
        ordinal = 0
        for page_number, page in enumerate(pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:
                raise SourceExtractionFailed(
                    f"text extraction failed on page {page_number}: {exc}"
                )
            text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
            if not text:
                # An empty page is not an error on its own; only a document
                # with no extractable text at all is.
                continue
            ordinal += 1
            locator = {"kind": "page", "start": page_number, "end": page_number}
            blocks.append(
                ExtractedBlock(
                    block_id=compute_block_id(source_id, locator, ordinal),
                    block_type=BLOCK_PAGE,
                    text=text,
                    locator=locator,
                    ordinal=ordinal,
                    metadata={"page": page_number, "page_count": len(pages)},
                )
            )
    finally:
        pypdf_log.setLevel(previous_level)

    if not blocks:
        raise SourceTextUnavailable(
            "PDF has no extractable text layer (scanned or image-only PDF); "
            "OCR is not supported"
        )
    return blocks


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
_ATX_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def _markdown_outline(lines: list[str]) -> list[tuple[int, int, str]]:
    """Return ``(line_number, level, heading_text)`` for real ATX headings.

    Lines inside fenced code blocks are skipped, so a ``# Fake Heading``
    written inside a fence never becomes a section.
    """
    outline: list[tuple[int, int, str]] = []
    fence: str | None = None
    for index, line in enumerate(lines, start=1):
        fence_match = _FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)[0] * 3
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is not None:
            continue
        heading = _ATX_HEADING_RE.match(line)
        if heading:
            outline.append((index, len(heading.group(1)), heading.group(2).strip()))
    return outline


def extract_markdown(raw: bytes, source_id: str) -> list[ExtractedBlock]:
    """Heading-scoped extraction from Markdown.

    A section runs from its heading line to the line before the next heading
    of any level. ``heading_path`` records the enclosing hierarchy, which is
    what keeps two identically-named headings (for example ``Overview`` under
    ``Architecture`` and ``Overview`` under ``Testing``) distinct: their
    heading paths differ, their line ranges differ, and therefore their block
    ids differ.

    This is a deterministic outline walk, not a Markdown renderer, and the
    resulting sections carry no claim of semantic importance.
    """
    text = _decode_text(raw)
    lines = text.split("\n")
    outline = _markdown_outline(lines)

    blocks: list[ExtractedBlock] = []
    ordinal = 0

    def _slice(start_line: int, end_line: int) -> str:
        return "\n".join(lines[start_line - 1 : end_line]).strip()

    # Content before the first heading is preserved rather than dropped.
    if outline:
        first_heading_line = outline[0][0]
        if first_heading_line > 1:
            preamble = _slice(1, first_heading_line - 1)
            if preamble:
                ordinal += 1
                locator = {
                    "kind": "section",
                    "label": "(preamble)",
                    "heading_path": [],
                    "start_line": 1,
                    "end_line": first_heading_line - 1,
                }
                blocks.append(
                    ExtractedBlock(
                        block_id=compute_block_id(source_id, locator, ordinal),
                        block_type=BLOCK_MARKDOWN_SECTION,
                        text=preamble,
                        locator=locator,
                        ordinal=ordinal,
                        metadata={"heading_level": 0, "heading_text": None},
                    )
                )
    else:
        # No headings at all: fall back to a single whole-document section so
        # that valid Markdown never silently yields zero blocks.
        body = text.strip()
        if not body:
            raise SourceTextUnavailable("Markdown source contains no text")
        locator = {
            "kind": "section",
            "label": "(document)",
            "heading_path": [],
            "start_line": 1,
            "end_line": len(lines),
        }
        return [
            ExtractedBlock(
                block_id=compute_block_id(source_id, locator, 1),
                block_type=BLOCK_MARKDOWN_SECTION,
                text=body,
                locator=locator,
                ordinal=1,
                metadata={"heading_level": 0, "heading_text": None},
            )
        ]

    path_stack: list[tuple[int, str]] = []
    for position, (line_number, level, heading_text) in enumerate(outline):
        while path_stack and path_stack[-1][0] >= level:
            path_stack.pop()
        path_stack.append((level, heading_text))
        heading_path = [name for _lvl, name in path_stack]

        end_line = (
            outline[position + 1][0] - 1 if position + 1 < len(outline) else len(lines)
        )
        ordinal += 1
        locator = {
            "kind": "section",
            "label": " > ".join(heading_path),
            "heading_path": list(heading_path),
            "start_line": line_number,
            "end_line": end_line,
        }
        blocks.append(
            ExtractedBlock(
                block_id=compute_block_id(source_id, locator, ordinal),
                block_type=BLOCK_MARKDOWN_SECTION,
                text=_slice(line_number, end_line),
                locator=locator,
                ordinal=ordinal,
                metadata={"heading_level": level, "heading_text": heading_text},
            )
        )
    return blocks


# ---------------------------------------------------------------------------
# Plain text
# ---------------------------------------------------------------------------
def extract_text(raw: bytes, source_id: str) -> list[ExtractedBlock]:
    """Paragraph extraction from plain text, split on blank lines.

    Deliberately simple and purely mechanical: blank-line separation only. No
    semantic chunking, no sentence splitting, no topic detection. Line numbers
    are 1-based and refer to the first and last non-blank line of the
    paragraph.
    """
    text = _decode_text(raw)
    lines = text.split("\n")

    blocks: list[ExtractedBlock] = []
    ordinal = 0
    start: int | None = None
    for index, line in enumerate(lines, start=1):
        if line.strip():
            if start is None:
                start = index
            continue
        if start is not None:
            ordinal += 1
            blocks.append(_text_block(source_id, lines, start, index - 1, ordinal))
            start = None
    if start is not None:
        ordinal += 1
        blocks.append(_text_block(source_id, lines, start, len(lines), ordinal))

    if not blocks:
        raise SourceTextUnavailable("plain-text source contains no text")
    return blocks


def _text_block(
    source_id: str, lines: list[str], start: int, end: int, ordinal: int
) -> ExtractedBlock:
    while end > start and not lines[end - 1].strip():
        end -= 1
    locator = {"kind": "line_range", "start": start, "end": end}
    return ExtractedBlock(
        block_id=compute_block_id(source_id, locator, ordinal),
        block_type=BLOCK_PARAGRAPH,
        text="\n".join(lines[start - 1 : end]).strip(),
        locator=locator,
        ordinal=ordinal,
        metadata={"start_line": start, "end_line": end},
    )


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------
#: Only an explicit built-in Word heading style makes a paragraph a heading.
_HEADING_STYLE_RE = re.compile(r"^Heading\s+([1-9])$", re.IGNORECASE)


def _normalize_docx_text(text: str) -> str:
    """Normalize DOCX run text without altering meaning.

    Word encodes a soft line break as a vertical tab, and non-breaking spaces
    are whitespace for reading purposes, so both are folded to their ordinary
    equivalents. Tabs are preserved because they can carry real structure in a
    document's content.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\v", "\n").replace("\x0b", "\n")
    text = text.replace("\xa0", " ")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def _heading_level(paragraph: Any) -> int | None:
    """The heading level from an explicit heading style, else ``None``.

    Heading identity comes from the paragraph's style only. Font size, weight,
    colour and visual position are deliberately ignored: inferring a heading
    from formatting would be heuristic layout interpretation, which belongs to
    semantic review, not deterministic extraction. Unstyled bold text therefore
    stays ordinary paragraph content.
    """
    try:
        style_name = paragraph.style.name or ""
    except Exception:
        return None
    match = _HEADING_STYLE_RE.match(style_name.strip())
    return int(match.group(1)) if match else None


def _table_text(table: Any) -> tuple[str, int, int]:
    """Flatten a table in deterministic row-major reading order.

    Rows top to bottom, cells left to right within each row, one row per output
    line with cells joined by ``" | "``. A line break *inside* a cell is folded
    to a space so that one output line always corresponds to exactly one table
    row; otherwise row boundaries would be ambiguous.

    A cell spanning multiple columns is reported by python-docx once per grid
    position it covers, so a merged cell's text repeats across the positions it
    spans rather than being dropped. That is the parser's actual behaviour and
    is tested as such; no stronger layout fidelity is claimed.
    """
    rows: list[str] = []
    row_count = 0
    column_count = 0
    for row in table.rows:
        row_count += 1
        cells = [
            _normalize_docx_text(cell.text).replace("\n", " ").strip()
            for cell in row.cells
        ]
        column_count = max(column_count, len(cells))
        rows.append(" | ".join(cells))
    return "\n".join(rows).strip(), row_count, column_count


def extract_docx(raw: bytes, source_id: str) -> list[ExtractedBlock]:
    """Structural extraction from a Word (OOXML) document.

    DOCX is flow-based: it carries no reliable rendered page boundaries without
    running Word's layout engine. Locators are therefore **structural** and no
    page number is ever synthesised.

    Body-level elements are walked in true document order, so interleaved
    paragraphs and tables keep their original sequence. Headings scope the
    following paragraphs into a section; each table becomes its own block,
    tagged with the heading path in force where it appears, so tables are never
    silently discarded.

    Body content only: headers, footers, footnotes, endnotes, comments,
    tracked-change metadata, and text inside embedded images are not ingested,
    and there is no OCR.
    """
    try:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise SourceExtractionFailed(f"python-docx is required for DOCX ingestion: {exc}")

    import io

    try:
        document = Document(io.BytesIO(raw))
        body = document.element.body
        children = list(body.iterchildren())
    except Exception as exc:
        raise SourceExtractionFailed(
            "DOCX package could not be parsed (it may be corrupted, or "
            f"password-protected/encrypted, which is not supported): {exc}"
        )

    blocks: list[ExtractedBlock] = []
    ordinal = 0
    path_stack: list[tuple[int, str]] = []
    heading_path: list[str] = []
    # Accumulating section: (heading_path, heading_level, texts, start, end)
    pending: dict[str, Any] | None = None

    def flush() -> None:
        nonlocal pending, ordinal
        if pending is None:
            return
        text = "\n\n".join(t for t in pending["texts"] if t).strip()
        if text:
            ordinal += 1
            locator = {
                "kind": "section",
                "label": " > ".join(pending["heading_path"]) or "(preamble)",
                "heading_path": list(pending["heading_path"]),
                "start_element": pending["start"],
                "end_element": pending["end"],
            }
            blocks.append(
                ExtractedBlock(
                    block_id=compute_block_id(source_id, locator, ordinal),
                    block_type=BLOCK_DOCX_SECTION,
                    text=text,
                    locator=locator,
                    ordinal=ordinal,
                    metadata={
                        "heading_level": pending["heading_level"],
                        "heading_text": pending["heading_text"],
                    },
                )
            )
        pending = None

    element_index = 0
    table_index = 0
    for child in children:
        tag = child.tag.rsplit("}", 1)[-1]
        if tag not in ("p", "tbl"):
            # sectPr and similar layout-only elements carry no source text.
            continue
        element_index += 1

        if tag == "p":
            paragraph = Paragraph(child, document)
            text = _normalize_docx_text(paragraph.text)
            level = _heading_level(paragraph)
            if level is not None:
                flush()
                while path_stack and path_stack[-1][0] >= level:
                    path_stack.pop()
                path_stack.append((level, text))
                heading_path = [name for _lvl, name in path_stack]
                pending = {
                    "heading_path": list(heading_path),
                    "heading_level": level,
                    "heading_text": text,
                    "texts": [text] if text else [],
                    "start": element_index,
                    "end": element_index,
                }
                continue
            if not text:
                # Layout-only empty paragraph: whitespace or empty runs only.
                continue
            if pending is None:
                pending = {
                    "heading_path": list(heading_path),
                    "heading_level": 0 if not heading_path else path_stack[-1][0],
                    "heading_text": path_stack[-1][1] if path_stack else None,
                    "texts": [],
                    "start": element_index,
                    "end": element_index,
                }
            pending["texts"].append(text)
            pending["end"] = element_index
            continue

        # tag == "tbl": emit in place so document order is preserved.
        flush()
        table_index += 1
        table = Table(child, document)
        text, row_count, column_count = _table_text(table)
        if not text:
            continue
        ordinal += 1
        locator = {
            "kind": "section",
            "label": f"Table {table_index}",
            "heading_path": list(heading_path),
            "table_index": table_index,
            "start_row": 1,
            "end_row": row_count,
        }
        blocks.append(
            ExtractedBlock(
                block_id=compute_block_id(source_id, locator, ordinal),
                block_type=BLOCK_DOCX_TABLE,
                text=text,
                locator=locator,
                ordinal=ordinal,
                metadata={
                    "table_index": table_index,
                    "row_count": row_count,
                    "column_count": column_count,
                    "element_index": element_index,
                },
            )
        )

    flush()

    if not blocks:
        raise SourceTextUnavailable(
            "DOCX has no extractable body or table text; text inside embedded "
            "images is not ingested and OCR is not supported"
        )
    return blocks


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
#: Matches the start of any element tag, used only to confirm that a file named
#: ``.html`` actually contains markup.
_HTML_TAG_RE = re.compile(rb"<[A-Za-z]")

#: Elements whose contents are code, styling, or browser-execution state rather
#: than document text. Their entire subtree is skipped.
HTML_EXCLUDED_TAGS = frozenset(
    {"script", "style", "template", "noscript", "head", "svg", "math"}
)

#: Elements that become their own extraction block, in document order.
_HTML_HEADINGS = ("h1", "h2", "h3", "h4", "h5", "h6")
_HTML_BLOCK_TAGS = frozenset(_HTML_HEADINGS) | {"p", "ul", "ol", "table"}


def _html_excluded(element: Any) -> bool:
    """True when an element sits inside excluded, tabular, or nested-list content."""
    for ancestor in element.iterancestors():
        tag = ancestor.tag
        if not isinstance(tag, str):
            continue
        if tag in HTML_EXCLUDED_TAGS:
            return True
        if tag == "table":
            # Text inside a table belongs to that table's block.
            return True
        if tag in ("ul", "ol"):
            # Nested list content is rendered inside its outermost list block.
            return True
    return False


def _html_inline_text(element: Any) -> str:
    """Visible text of an element, excluding excluded subtrees and nested lists.

    Inline markup such as ``strong``, ``em``, ``span``, ``code`` and ``a``
    contributes its text here rather than becoming a separate block, so a bold
    phrase never fragments a paragraph.
    """
    parts: list[str] = []

    def walk(node: Any, is_root: bool) -> None:
        tag = node.tag
        if isinstance(tag, str):
            if tag in HTML_EXCLUDED_TAGS:
                return
            if not is_root and tag in ("ul", "ol"):
                return
        if node.text:
            parts.append(node.text)
        for child in node:
            walk(child, False)
            if child.tail:
                parts.append(child.tail)

    walk(element, True)
    return _normalize_html_text("".join(parts))


def _normalize_html_text(text: str) -> str:
    """Collapse HTML whitespace deterministically without rewriting content."""
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def _html_list_lines(element: Any, depth: int = 0) -> list[str]:
    """Render a list, and any nested lists, as deterministic indented lines.

    Nested items appear once, indented under their parent item, so an outer list
    block never duplicates the text of a list nested inside it. List depth
    carries no priority meaning.
    """
    lines: list[str] = []
    ordered = element.tag == "ol"
    counter = 0
    for item in element:
        if not isinstance(item.tag, str) or item.tag != "li":
            continue
        counter += 1
        marker = f"{counter}." if ordered else "-"
        own = _html_inline_text(item)
        lines.append(f"{'  ' * depth}{marker} {own}".rstrip())
        for child in item:
            if isinstance(child.tag, str) and child.tag in ("ul", "ol"):
                lines.extend(_html_list_lines(child, depth + 1))
    return lines


def _html_table_text(element: Any) -> tuple[str, int, int]:
    """Flatten an HTML table in DOM row-major order.

    One output line per ``tr``, cells joined with ``" | "``. Cells are taken in
    the order they actually appear in the DOM.

    ``rowspan`` and ``colspan`` attributes are **not** expanded into a visual
    grid: no spreadsheet model is reconstructed, so a spanned cell appears once,
    on the row where it is declared, and later rows show only the cells they
    actually contain. This is the real DOM cell order and is tested as such.
    """
    rows: list[str] = []
    row_count = 0
    column_count = 0
    for row in element.iter("tr"):
        cells = [c for c in row if isinstance(c.tag, str) and c.tag in ("td", "th")]
        if not cells:
            continue
        row_count += 1
        texts = [_html_inline_text(c).replace("\n", " ").strip() for c in cells]
        column_count = max(column_count, len(texts))
        rows.append(" | ".join(texts))
    return "\n".join(rows).strip(), row_count, column_count


def extract_html(raw: bytes, source_id: str) -> list[ExtractedBlock]:
    """Static structural extraction from a local HTML file.

    This is **not** browser rendering. No JavaScript is executed, no CSS is
    applied, no browser or headless engine is involved, and nothing is fetched:
    ``img``/``script``/``link`` sources, stylesheets, iframes and hyperlinks are
    never resolved or downloaded. Content that only exists after JavaScript runs
    is therefore not ingested.

    Because CSS is not evaluated, this is described as static structural text
    extraction with non-content elements excluded -- not as "only
    browser-visible text". An element hidden purely by CSS is not detected as
    hidden.

    ``script``, ``style``, ``template``, ``noscript``, ``svg`` and ``math``
    subtrees are skipped, as are HTML comments and processing instructions, so
    embedded JSON-LD never reaches ordinary source text. Headings, paragraphs,
    lists and tables become blocks in DOM document order.
    """
    try:
        import lxml.html as lxml_html
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise SourceExtractionFailed(f"lxml is required for HTML ingestion: {exc}")

    text = _decode_text(raw)
    if not text.strip():
        raise SourceTextUnavailable("HTML source is empty")

    # no_network hard-disables any external access the parser could attempt;
    # comments and processing instructions are dropped before the tree is built.
    parser = lxml_html.HTMLParser(
        no_network=True,
        remove_comments=True,
        remove_pis=True,
        huge_tree=False,
    )
    try:
        document = lxml_html.document_fromstring(text, parser=parser)
    except Exception as exc:
        raise SourceExtractionFailed(f"HTML could not be parsed: {exc}")

    blocks: list[ExtractedBlock] = []
    ordinal = 0
    element_index = 0
    table_index = 0
    list_index = 0
    path_stack: list[tuple[int, str]] = []
    heading_path: list[str] = []
    pending: dict[str, Any] | None = None

    def flush() -> None:
        nonlocal pending, ordinal
        if pending is None:
            return
        body = "\n\n".join(t for t in pending["texts"] if t).strip()
        if body:
            ordinal += 1
            locator = {
                "kind": "section",
                "label": " > ".join(pending["heading_path"]) or "(preamble)",
                "heading_path": list(pending["heading_path"]),
                "start_element": pending["start"],
                "end_element": pending["end"],
            }
            blocks.append(
                ExtractedBlock(
                    block_id=compute_block_id(source_id, locator, ordinal),
                    block_type=BLOCK_HTML_SECTION,
                    text=body,
                    locator=locator,
                    ordinal=ordinal,
                    metadata={
                        "heading_level": pending["heading_level"],
                        "heading_text": pending["heading_text"],
                    },
                )
            )
        pending = None

    for element in document.iter():
        tag = element.tag
        if not isinstance(tag, str) or tag not in _HTML_BLOCK_TAGS:
            continue
        if _html_excluded(element):
            continue
        element_index += 1

        if tag in _HTML_HEADINGS:
            level = int(tag[1])
            content = _html_inline_text(element)
            flush()
            # A jumped level (h1 -> h3) simply nests one deeper; no missing
            # intermediate heading is ever invented.
            while path_stack and path_stack[-1][0] >= level:
                path_stack.pop()
            path_stack.append((level, content))
            heading_path = [name for _lvl, name in path_stack]
            pending = {
                "heading_path": list(heading_path),
                "heading_level": level,
                "heading_text": content,
                "texts": [content] if content else [],
                "start": element_index,
                "end": element_index,
            }
            continue

        if tag == "p":
            content = _html_inline_text(element)
            if not content:
                continue
            if pending is None:
                pending = {
                    "heading_path": list(heading_path),
                    "heading_level": path_stack[-1][0] if path_stack else 0,
                    "heading_text": path_stack[-1][1] if path_stack else None,
                    "texts": [],
                    "start": element_index,
                    "end": element_index,
                }
            pending["texts"].append(content)
            pending["end"] = element_index
            continue

        if tag in ("ul", "ol"):
            flush()
            lines = _html_list_lines(element)
            body = "\n".join(line for line in lines if line.strip("- ").strip())
            if not body.strip():
                continue
            list_index += 1
            ordinal += 1
            locator = {
                "kind": "section",
                "label": f"List {list_index}",
                "heading_path": list(heading_path),
                "list_index": list_index,
                "start_element": element_index,
                "end_element": element_index,
            }
            blocks.append(
                ExtractedBlock(
                    block_id=compute_block_id(source_id, locator, ordinal),
                    block_type=BLOCK_HTML_LIST,
                    text=body,
                    locator=locator,
                    ordinal=ordinal,
                    metadata={
                        "list_index": list_index,
                        "list_type": "ordered" if tag == "ol" else "unordered",
                        "item_count": len(lines),
                        "element_index": element_index,
                    },
                )
            )
            continue

        # tag == "table"
        flush()
        body, row_count, column_count = _html_table_text(element)
        if not body:
            continue
        table_index += 1
        ordinal += 1
        locator = {
            "kind": "section",
            "label": f"Table {table_index}",
            "heading_path": list(heading_path),
            "table_index": table_index,
            "start_row": 1,
            "end_row": row_count,
            "start_element": element_index,
            "end_element": element_index,
        }
        blocks.append(
            ExtractedBlock(
                block_id=compute_block_id(source_id, locator, ordinal),
                block_type=BLOCK_HTML_TABLE,
                text=body,
                locator=locator,
                ordinal=ordinal,
                metadata={
                    "table_index": table_index,
                    "row_count": row_count,
                    "column_count": column_count,
                    "element_index": element_index,
                },
            )
        )

    flush()

    if not blocks:
        raise SourceTextUnavailable(
            "HTML has no extractable static text; JavaScript is not executed and "
            "no browser rendering, remote resource loading or OCR is performed"
        )
    return blocks


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
_EXTRACTORS = {
    FORMAT_PDF: extract_pdf,
    FORMAT_MARKDOWN: extract_markdown,
    FORMAT_TEXT: extract_text,
    FORMAT_DOCX: extract_docx,
    FORMAT_HTML: extract_html,
}


def ingest_source(path: str | Path, source_id: str) -> ExtractionResult:
    """The single orchestration-facing ingestion entry point.

    Reads a local file, detects its format, extracts normalized blocks with
    format-native locators, and fingerprints the source using the Phase 12
    digest definition. The returned result is input for AGY's semantic
    segmentation; it is not a Phase 12 source inventory and no block is
    promoted to a semantic source unit here.
    """
    if not _SOURCE_ID_RE.match(source_id or ""):
        raise SourceIngestionError(
            f"invalid source_id: {source_id!r} (expected ^src_[A-Za-z0-9._-]+$)"
        )

    p = Path(os.path.expanduser(str(path)))
    source_format = detect_source_format(p)
    if source_format not in _EXTRACTORS:
        raise SourceFormatUnsupported(
            f"unsupported source format for {p.name!r}; Phase 13 supports "
            f"{', '.join(SUPPORTED_FORMATS)} (local files only; no remote URL "
            "ingestion and no OCR)"
        )

    try:
        raw = p.read_bytes()
    except OSError as exc:
        raise SourceReadFailed(f"could not read source file: {exc}")

    blocks = _EXTRACTORS[source_format](raw, source_id)
    return ExtractionResult(
        schema_version=SCHEMA_VERSION,
        extractor_version=EXTRACTOR_VERSION,
        source_id=source_id,
        source_format=source_format,
        # Always over the raw bytes, so it matches whatever Phase 12 recorded.
        source_digest=compute_source_digest(raw),
        blocks=tuple(blocks),
    )


# ---------------------------------------------------------------------------
# Phase 12 handoff
# ---------------------------------------------------------------------------
def phase12_locator(block: ExtractedBlock) -> dict[str, Any]:
    """The Phase 12 locator for an extracted block.

    Phase 13 locators are authored using the frozen Phase 12 locator kinds
    (``page``, ``section``, ``line_range``), so handoff needs no translation
    and no change to Phase 12: PDF pages use ``page``, Markdown sections use
    ``section`` with an additional ``heading_path``/line range, plain-text
    paragraphs use ``line_range``, and DOCX and HTML sections, lists and tables
    use ``section`` with structural element/row ranges. Nothing here contains a
    filesystem path -- a locator describes a position *within* a source, and the
    source itself is identified by ``source_id``.

    Handing the result to :meth:`SourceInventory.add_unit` remains an AGY
    decision: this returns the locator for a block AGY has *chosen* to promote,
    and never promotes blocks on its own.
    """
    return dict(block.locator)
