#!/usr/bin/env python3
"""Convert one PDF, scanned PDF, DOCX, or TXT book into canonical JSON.

The command always writes a traceable JSON draft when extraction and TOC
reconstruction succeed. It exits 0 only when the resulting bundle passes every
requested final gate; reviewable uncertainty exits 3 and remains clearly marked.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from build_derivatives import build_one
from validate_bundle import LIKELY_OCR_PATTERNS


PAGE_MARKER_RE = re.compile(r"^===== 第 (\d+) 页 =====$", re.M)
TOC_WORD_RE = re.compile(r"目\s*录")
PAGE_ONLY_RE = re.compile(r"^[（(]?\s*([0-9０-９]{1,4})\s*[）)]?$")
TITLE_PAGE_RE = re.compile(
    r"^(.*?)(?:[.．·•…⋯_—\-\s]{2,}|\s+)[（(]?\s*([0-9０-９]{1,4})\s*[）)]?$"
)
TITLE_START_RE = re.compile(
    r"^(?:第[一二三四五六七八九十百千万0-9]+[卷编篇部章节]|"
    r"[一二三四五六七八九十百]+、|[（(][一二三四五六七八九十百0-9]+[）)]|"
    r"[0-9]+[.、]|出版说明|前言|序言|绪论|导论|附录|后记|结语)"
)
TERMINAL_RE = re.compile(r"^(?:图书在版编目|责任编辑|责任校对|版权所有|ISBN|定价[:：]|封底)")
CJK_RE = re.compile(r"[\u3400-\u9fff]")
PUNCT_END = set("。！？；：.!?;:）)]】》”’」』")


@dataclass
class Page:
    number: int
    text: str


@dataclass
class HeadingMatch:
    start: int
    end: int
    source_page: int
    score: float
    matched_text: str


def run(command: list[str], *, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False, timeout=timeout)


def require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise ValueError(f"required command is unavailable: {name}")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n")
    value = value.replace("\x00", "")
    return value


def normalize_heading(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).lower()
    return "".join(char for char in value if char.isalnum() or CJK_RE.match(char))


def split_page_marked_text(text: str) -> list[Page]:
    matches = list(PAGE_MARKER_RE.finditer(text))
    if not matches:
        return [Page(1, normalize_text(text).strip())]
    pages: list[Page] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        pages.append(Page(int(match.group(1)), normalize_text(text[start:end]).strip("\n")))
    return pages


def extract_txt(path: Path) -> list[Page]:
    raw = path.read_text(encoding="utf-8-sig", errors="strict")
    return split_page_marked_text(raw)


def extract_docx(path: Path) -> list[Page]:
    namespace = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    word = f"{{{namespace}}}"
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError) as exc:
        raise ValueError(f"{path}: invalid DOCX package") from exc
    root = ET.fromstring(xml)
    pages: list[list[str]] = [[]]
    for paragraph in root.iter(f"{word}p"):
        text = normalize_text("".join(item.text or "" for item in paragraph.iter(f"{word}t"))).strip()
        if text:
            pages[-1].append(text)
        has_page_break = any(
            item.get(f"{word}type") == "page" for item in paragraph.iter(f"{word}br")
        ) or any(True for _ in paragraph.iter(f"{word}lastRenderedPageBreak"))
        if has_page_break and pages[-1]:
            pages.append([])
    if not any(pages):
        raise ValueError(f"{path}: DOCX contains no readable paragraphs")
    return [Page(index, "\n".join(lines)) for index, lines in enumerate(pages, start=1) if lines]


def pdf_text_pages(path: Path) -> list[Page]:
    pdftotext = require_command("pdftotext")
    with tempfile.TemporaryDirectory(prefix="book-pdf-text-") as temporary:
        target = Path(temporary) / "book.txt"
        result = run([pdftotext, "-layout", "-enc", "UTF-8", str(path), str(target)], timeout=600)
        if result.returncode != 0 or not target.exists():
            raise ValueError(f"pdftotext failed: {result.stderr.strip()}")
        text = normalize_text(target.read_text(encoding="utf-8", errors="replace"))
    chunks = text.split("\f")
    if chunks and not chunks[-1].strip():
        chunks.pop()
    return [Page(index, chunk.strip("\n")) for index, chunk in enumerate(chunks, start=1)]


def text_layer_is_weak(pages: list[Page]) -> bool:
    counts = [len(re.sub(r"\s+", "", page.text)) for page in pages]
    if not counts:
        return True
    useful = counts[min(3, len(counts)) :]
    useful = useful or counts
    empty_ratio = sum(count < 20 for count in useful) / len(useful)
    return statistics.median(useful) < 40 or empty_ratio > 0.45


def available_tesseract_languages() -> set[str]:
    result = run([require_command("tesseract"), "--list-langs"], timeout=60)
    if result.returncode != 0:
        return set()
    return {line.strip() for line in result.stdout.splitlines()[1:] if line.strip()}


def ocr_pdf(path: Path, language: str, dpi: int) -> list[Page]:
    pdftoppm = require_command("pdftoppm")
    tesseract = require_command("tesseract")
    requested = [item for item in language.split("+") if item]
    available = available_tesseract_languages()
    missing = [item for item in requested if item not in available]
    if missing:
        raise ValueError(f"missing Tesseract language data: {', '.join(missing)}")
    with tempfile.TemporaryDirectory(prefix="book-pdf-ocr-") as temporary:
        prefix = Path(temporary) / "page"
        render = run([pdftoppm, "-r", str(dpi), "-png", str(path), str(prefix)], timeout=1800)
        if render.returncode != 0:
            raise ValueError(f"pdftoppm failed: {render.stderr.strip()}")
        images = sorted(Path(temporary).glob("page-*.png"))
        if not images:
            raise ValueError("PDF rendering produced no pages")
        pages: list[Page] = []
        for number, image in enumerate(images, start=1):
            result = run([tesseract, str(image), "stdout", "-l", language, "--psm", "6"], timeout=300)
            if result.returncode != 0:
                raise ValueError(f"Tesseract failed on page {number}: {result.stderr.strip()}")
            pages.append(Page(number, normalize_text(result.stdout).strip()))
        return pages


def extract_pdf(path: Path, force_ocr: bool, language: str, dpi: int) -> tuple[list[Page], str]:
    pages = pdf_text_pages(path)
    if force_ocr or text_layer_is_weak(pages):
        return ocr_pdf(path, language, dpi), "ocr"
    return pages, "text_layer"


def extract_source(path: Path, force_ocr: bool, language: str, dpi: int) -> tuple[list[Page], str]:
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return extract_txt(path), "txt"
    if suffix == ".docx":
        return extract_docx(path), "docx"
    if suffix == ".pdf":
        return extract_pdf(path, force_ocr, language, dpi)
    raise ValueError(f"unsupported source type: {suffix}")


def parse_page_spec(value: str, page_count: int) -> list[int]:
    result: set[int] = set()
    for piece in value.split(","):
        piece = piece.strip()
        if not piece:
            continue
        if "-" in piece:
            left, right = piece.split("-", 1)
            result.update(range(int(left), int(right) + 1))
        else:
            result.add(int(piece))
    invalid = [number for number in result if number < 1 or number > page_count]
    if invalid:
        raise ValueError(f"TOC page numbers outside source range: {invalid}")
    return sorted(result)


def detect_toc_pages(pages: list[Page]) -> list[int]:
    starts = [page.number for page in pages if TOC_WORD_RE.search(page.text[:500])]
    if not starts:
        raise ValueError("printed TOC pages were not detected; provide --toc-pages or --toc-json")
    start = starts[0]
    selected = [start]
    for number in range(start + 1, min(len(pages), start + 7) + 1):
        text = pages[number - 1].text
        if sum(bool(PAGE_ONLY_RE.match(line.strip()) or TITLE_PAGE_RE.match(line.strip())) for line in text.splitlines()) == 0:
            break
        selected.append(number)
    return selected


def to_int(value: str) -> int:
    return int(unicodedata.normalize("NFKC", value))


def looks_like_title(value: str) -> bool:
    compact = re.sub(r"\s+", "", value)
    return bool(TITLE_START_RE.match(compact)) and 2 <= len(compact) <= 100


def infer_kind_and_level(title: str) -> tuple[str, int]:
    compact = re.sub(r"\s+", "", title)
    if re.match(r"^第.+[卷编篇部]", compact):
        return "part", 1
    if re.match(r"^第.+章", compact):
        return "chapter", 1
    if re.match(r"^第.+节", compact):
        return "section", 2
    if re.match(r"^[一二三四五六七八九十百]+、", compact):
        return "section", 1
    if re.match(r"^[（(][一二三四五六七八九十百0-9]+[）)]", compact):
        return "subsection", 2
    if re.match(r"^[0-9]+[.、]", compact):
        return "topic", 2
    if re.match(r"^(出版说明|前言|序言|绪论|导论)", compact):
        return "front_matter", 1
    if re.match(r"^(附录|后记|结语)", compact):
        return "end_matter", 1
    return "section", 1


def parse_toc(pages: list[Page], toc_page_numbers: list[int]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    buffer: list[str] = []
    for number in toc_page_numbers:
        lines = [line.strip() for line in pages[number - 1].text.splitlines()]
        for raw in lines:
            line = re.sub(r"\s+", " ", raw).strip(" .·•…⋯")
            if not line or TOC_WORD_RE.fullmatch(re.sub(r"\s+", "", line)):
                continue
            title_page = TITLE_PAGE_RE.match(line)
            page_only = PAGE_ONLY_RE.match(line)
            if title_page and title_page.group(1).strip():
                title = ("".join(buffer) + title_page.group(1).strip()).strip()
                entries.append({"title": title, "logical_page": to_int(title_page.group(2))})
                buffer = []
            elif page_only and buffer:
                entries.append({"title": "".join(buffer).strip(), "logical_page": to_int(page_only.group(1))})
                buffer = []
            elif looks_like_title(line):
                if buffer:
                    buffered = "".join(buffer).strip()
                    if looks_like_title(buffered):
                        entries.append({"title": buffered, "logical_page": None})
                buffer = [line]
            elif buffer and len("".join(buffer)) < 120:
                buffer.append(line)
    if buffer:
        buffered = "".join(buffer).strip()
        if looks_like_title(buffered):
            entries.append({"title": buffered, "logical_page": None})

    cleaned: list[dict[str, Any]] = []
    for entry in entries:
        title = re.sub(r"[.·•…⋯_—\-\s]+$", "", entry["title"]).strip()
        if not looks_like_title(title):
            continue
        if cleaned and normalize_heading(cleaned[-1]["title"]) == normalize_heading(title):
            if cleaned[-1]["logical_page"] is None:
                cleaned[-1]["logical_page"] = entry["logical_page"]
            continue
        kind, level = infer_kind_and_level(title)
        cleaned.append({"title": title, "logical_page": entry["logical_page"], "kind": kind, "level": level})
    if not cleaned:
        raise ValueError("no TOC entries could be parsed; provide a reviewed --toc-json")
    return assign_tree_keys(cleaned)


def assign_tree_keys(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stack: dict[int, str] = {}
    results: list[dict[str, Any]] = []
    for index, entry in enumerate(entries, start=1):
        level = max(1, int(entry.get("level", 1)))
        key = str(entry.get("key") or f"toc-{index:03d}")
        logical_page = entry.get("logical_page")
        if isinstance(logical_page, str) and logical_page.strip().isdigit():
            logical_page = int(logical_page.strip())
        if logical_page is not None and not isinstance(logical_page, int):
            raise ValueError(
                f"TOC entry {index} logical_page must be an integer or null, got {logical_page!r}"
            )
        parent = entry.get("parent_key")
        if "parent_key" not in entry:
            parent = stack.get(level - 1) if level > 1 else None
        results.append(
            {
                "key": key,
                "title": str(entry["title"]).strip(),
                "level": level,
                "parent_key": parent,
                "sort": index,
                "logical_page": logical_page,
                "kind": str(entry.get("kind") or infer_kind_and_level(str(entry["title"]))[0]),
            }
        )
        stack[level] = key
        for deeper in [item for item in stack if item > level]:
            del stack[deeper]
    return results


def load_toc_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("nodes", data.get("toc", data.get("entries")))
    if not isinstance(data, list) or not data:
        raise ValueError(f"{path}: TOC JSON must be a nonempty list or contain nodes/toc/entries")
    for index, entry in enumerate(data, start=1):
        if not isinstance(entry, dict) or not str(entry.get("title", "")).strip():
            raise ValueError(f"{path}: TOC entry {index} lacks a title")
    return assign_tree_keys(data)


def combined_source(pages: list[Page]) -> tuple[str, list[tuple[int, int, int]]]:
    chunks: list[str] = []
    ranges: list[tuple[int, int, int]] = []
    cursor = 0
    for page in pages:
        chunk = f"===== 第 {page.number} 页 =====\n{page.text.strip()}\n"
        chunks.append(chunk)
        ranges.append((cursor, cursor + len(chunk), page.number))
        cursor += len(chunk)
    return "\n".join(chunks), ranges


def source_page_for(offset: int, ranges: list[tuple[int, int, int]]) -> int:
    for start, end, number in ranges:
        if start <= offset < end:
            return number
    return ranges[-1][2]


def line_candidates(source: str, ranges: list[tuple[int, int, int]], body_start_page: int) -> list[tuple[int, int, int, str]]:
    candidates: list[tuple[int, int, int, str]] = []
    offset = 0
    lines = source.splitlines(keepends=True)
    for index, line in enumerate(lines):
        start = offset
        offset += len(line)
        if PAGE_MARKER_RE.match(line.strip()):
            continue
        page = source_page_for(start, ranges)
        if page < body_start_page:
            continue
        parts = [line.strip()]
        end = offset
        if parts[0]:
            candidates.append((start, end, page, parts[0]))
        for width in range(1, 3):
            if index + width >= len(lines) or PAGE_MARKER_RE.match(lines[index + width].strip()):
                break
            parts.append(lines[index + width].strip())
            end += len(lines[index + width])
            text = "".join(parts).strip()
            if text:
                candidates.append((start, end, page, text))
    return candidates


def heading_similarity(title: str, candidate: str) -> float:
    left = normalize_heading(title)
    right = normalize_heading(candidate)
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    if left in right and len(right) <= len(left) + 8:
        return 0.98
    if right in left and len(left) <= len(right) + 8:
        return 0.96
    if len(right) > max(20, len(left) * 2.2):
        return 0.0
    return difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()


def locate_headings(
    source: str,
    ranges: list[tuple[int, int, int]],
    toc: list[dict[str, Any]],
    toc_end_page: int,
) -> list[HeadingMatch]:
    candidates = line_candidates(source, ranges, 1)
    located: list[HeadingMatch] = []
    previous_end = 0
    page_offsets: list[int] = []
    for entry in toc:
        predicted: int | None = None
        if entry.get("logical_page") is not None and page_offsets:
            predicted = int(entry["logical_page"]) + round(statistics.median(page_offsets))
        best: tuple[float, int, int, int, str] | None = None
        for start, end, page, text in candidates:
            if start < previous_end:
                continue
            if toc_end_page:
                if entry.get("kind") == "front_matter" and page > toc_end_page:
                    continue
                if entry.get("kind") != "front_matter" and page <= toc_end_page:
                    continue
            score = heading_similarity(entry["title"], text)
            if predicted is not None:
                distance = abs(page - predicted)
                if distance > 12:
                    continue
                score -= min(0.12, distance * 0.01)
            if best is None or score > best[0]:
                best = (score, start, end, page, text)
        if best is None:
            located.append(HeadingMatch(previous_end, previous_end, max(1, toc_end_page + 1), 0.0, ""))
            continue
        score, start, end, page, text = best
        located.append(HeadingMatch(start, end, page, max(0.0, min(1.0, score)), text))
        previous_end = end
        if entry.get("logical_page") is not None and score >= 0.8:
            page_offsets.append(page - int(entry["logical_page"]))
    return located


def repeated_margin_lines(pages: list[Page]) -> set[str]:
    counter: Counter[str] = Counter()
    for page in pages:
        lines = [line.strip() for line in page.text.splitlines() if line.strip()]
        for line in [*lines[:2], *lines[-2:]]:
            compact = re.sub(r"\s+", "", line)
            if 2 <= len(compact) <= 50 and not compact.isdigit():
                counter[compact] += 1
    threshold = max(3, round(len(pages) * 0.2))
    return {line for line, count in counter.items() if count >= threshold}


def clean_content(value: str, repeated_margins: set[str]) -> str:
    value = PAGE_MARKER_RE.sub("", normalize_text(value))
    lines = []
    for raw in value.splitlines():
        line = raw.strip()
        compact = re.sub(r"\s+", "", line)
        if not line:
            lines.append("")
            continue
        if compact in repeated_margins or re.fullmatch(r"[-—–]?\s*\d{1,4}\s*[-—–]?", line):
            continue
        lines.append(line)

    paragraphs: list[str] = []
    current = ""
    for line in lines:
        if not line:
            if current:
                paragraphs.append(current)
                current = ""
            continue
        if not current:
            current = line
        elif current[-1] in PUNCT_END:
            paragraphs.append(current)
            current = line
        elif CJK_RE.search(current[-1:]) and CJK_RE.match(line[:1]):
            current += line
        else:
            current += " " + line
    if current:
        paragraphs.append(current)
    return "\n\n".join(paragraph.strip() for paragraph in paragraphs if paragraph.strip()).strip()


def terminal_boundary(source: str, last_content_start: int) -> int:
    tail = source[last_content_start:]
    offset = last_content_start
    for line in tail.splitlines(keepends=True):
        if TERMINAL_RE.match(line.strip()):
            return offset
        offset += len(line)
    return len(source)


def build_tree(
    source_path: Path,
    book_id: str,
    title: str,
    pages: list[Page],
    toc: list[dict[str, Any]],
    toc_pages: list[int],
    extraction_method: str,
    review_status: str,
    reviewer: str | None,
) -> dict[str, Any]:
    source, ranges = combined_source(pages)
    toc_end_page = max(toc_pages) if toc_pages else 0
    matches = locate_headings(source, ranges, toc, toc_end_page)
    margins = repeated_margin_lines(pages)
    nodes: list[dict[str, Any]] = []
    child_parents = {entry.get("parent_key") for entry in toc if entry.get("parent_key")}
    for index, (entry, match) in enumerate(zip(toc, matches)):
        next_start = matches[index + 1].start if index + 1 < len(matches) else terminal_boundary(source, match.end)
        raw = source[match.end:next_start] if match.end <= next_start else ""
        content = clean_content(raw, margins)
        structural_only = not content and entry["key"] in child_parents
        nodes.append(
            {
                "key": entry["key"],
                "title": entry["title"],
                "level": entry["level"],
                "parent_key": entry["parent_key"],
                "sort": entry["sort"],
                "logical_page": entry.get("logical_page"),
                "source_page": match.source_page,
                "heading_start": match.start,
                "content_start": match.end,
                "content_end": next_start,
                "heading_score": round(match.score, 4),
                "structural_only": structural_only,
                "content": content,
                "content_chars": len(content),
                "source_file": source_path.name,
                "kind": entry.get("kind", "section"),
                "matched_heading": match.matched_text,
            }
        )
    return {
        "book_id": book_id,
        "title": title,
        "authority": "printed_toc",
        "node_count": len(nodes),
        "source_file": source_path.name,
        "source_sha256": sha256(source_path),
        "source_format": source_path.suffix.lower().lstrip("."),
        "extraction_method": extraction_method,
        "review_status": review_status,
        "reviewer": reviewer,
        "nodes": nodes,
    }


def context_window(text: str, start: int, end: int, radius: int = 24) -> str:
    return text[max(0, start - radius) : min(len(text), end + radius)].replace("\n", " ")


def detected_candidates(tree: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    total_cjk = sum(len(CJK_RE.findall(str(node.get("content", "")))) for node in tree["nodes"])
    frequencies = Counter(char for node in tree["nodes"] for char in str(node.get("content", "")) if CJK_RE.match(char))
    for node in tree["nodes"]:
        content = str(node.get("content", ""))
        for name, pattern in LIKELY_OCR_PATTERNS:
            for occurrence, match in enumerate(pattern.finditer(content), start=1):
                rows.append(
                    {
                        "candidate_id": f"{tree['book_id']}:{node['key']}:{name}:{occurrence}",
                        "book_id": tree["book_id"],
                        "node_key": node["key"],
                        "original": match.group(0),
                        "suggestion": "",
                        "context": context_window(content, match.start(), match.end()),
                        "decision": "",
                        "reviewer": "",
                    }
                )
        if total_cjk >= 500:
            seen: Counter[str] = Counter()
            for position, char in enumerate(content):
                if CJK_RE.match(char) and frequencies[char] <= 1 and seen[char] == 0:
                    seen[char] += 1
                    rows.append(
                        {
                            "candidate_id": f"{tree['book_id']}:{node['key']}:rare-U+{ord(char):04X}",
                            "book_id": tree["book_id"],
                            "node_key": node["key"],
                            "original": char,
                            "suggestion": "",
                            "context": context_window(content, position, position + 1),
                            "decision": "",
                            "reviewer": "",
                        }
                    )
    unique: dict[str, dict[str, str]] = {}
    for row in rows:
        unique[row["candidate_id"]] = row
    return list(unique.values())


def read_ledger(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [dict(row) for row in reader]


def write_ledger(path: Path, rows: Iterable[dict[str, str]]) -> None:
    fields = ["candidate_id", "book_id", "node_key", "original", "suggestion", "context", "decision", "reviewer"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def apply_ledger(tree: dict[str, Any], rows: list[dict[str, str]]) -> None:
    nodes = {node["key"]: node for node in tree["nodes"]}
    for row in rows:
        if row.get("book_id") != tree["book_id"] or row.get("decision") != "corrected":
            continue
        node = nodes.get(row.get("node_key", ""))
        if node is None:
            raise ValueError(f"review ledger references unknown node: {row.get('node_key')}")
        old = row.get("original", "")
        new = row.get("suggestion", "")
        if not old or not new:
            raise ValueError(f"corrected candidate lacks original/suggestion: {row.get('candidate_id')}")
        if old not in node["content"]:
            raise ValueError(f"reviewed original not found in node: {row.get('candidate_id')}")
        node["content"] = node["content"].replace(old, new, 1)
        node["content_chars"] = len(node["content"])


def write_pages(work_dir: Path, pages: list[Page]) -> None:
    page_dir = work_dir / "pages"
    if page_dir.exists():
        shutil.rmtree(page_dir)
    page_dir.mkdir(parents=True, exist_ok=True)
    for page in pages:
        (page_dir / f"page-{page.number:04d}.txt").write_text(page.text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--book-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--toc-json", type=Path, help="reviewed printed-TOC manifest")
    parser.add_argument("--toc-pages", help="source page numbers, e.g. 7-9,12")
    parser.add_argument("--accept-auto-toc", action="store_true")
    parser.add_argument("--reviewer")
    parser.add_argument("--review-ledger", type=Path, help="reviewed OCR TSV to apply")
    parser.add_argument("--min-heading-score", type=float, default=0.80)
    parser.add_argument("--force-ocr", action="store_true")
    parser.add_argument("--accept-ocr", action="store_true", help="confirm rendered OCR pages were reviewed")
    parser.add_argument("--ocr-language", default="chi_sim+eng")
    parser.add_argument("--ocr-dpi", type=int, default=300)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    try:
        source = args.source.resolve()
        if not source.is_file():
            raise ValueError(f"source does not exist: {source}")
        if args.output_dir.exists() and any(args.output_dir.iterdir()) and not args.replace:
            raise ValueError("output directory is not empty; use a new version directory or --replace")
        if args.output_dir.exists() and args.replace:
            expected_tree = f"{args.book_id}_tree.json"
            conflicting = [
                path.name for path in args.output_dir.glob("*_tree.json") if path.name != expected_tree
            ]
            if conflicting:
                raise ValueError(
                    "output directory contains canonical trees for another book: " + ", ".join(conflicting)
                )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        work_dir = args.output_dir / "_work"
        work_dir.mkdir(parents=True, exist_ok=True)

        pages, extraction_method = extract_source(source, args.force_ocr, args.ocr_language, args.ocr_dpi)
        if not pages:
            raise ValueError("source extraction produced no pages")
        write_pages(work_dir, pages)

        if args.toc_json:
            toc = load_toc_json(args.toc_json)
            if args.toc_pages:
                toc_pages = parse_page_spec(args.toc_pages, len(pages))
            else:
                try:
                    toc_pages = detect_toc_pages(pages)
                except ValueError:
                    toc_pages = []
            review_status = "approved"
        else:
            toc_pages = parse_page_spec(args.toc_pages, len(pages)) if args.toc_pages else detect_toc_pages(pages)
            toc = parse_toc(pages, toc_pages)
            review_status = "approved" if args.accept_auto_toc and args.reviewer else "pending_toc_review"
        (work_dir / "toc-detected.json").write_text(
            json.dumps(toc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        tree = build_tree(
            source,
            args.book_id,
            args.title,
            pages,
            toc,
            toc_pages,
            extraction_method,
            review_status,
            args.reviewer,
        )
        reviewed_rows = read_ledger(args.review_ledger) if args.review_ledger else []
        if reviewed_rows:
            apply_ledger(tree, reviewed_rows)

        current_candidates = detected_candidates(tree)
        reviewed_by_id = {row.get("candidate_id", ""): row for row in reviewed_rows}
        unresolved: list[dict[str, str]] = []
        final_rows: list[dict[str, str]] = []
        for candidate in current_candidates:
            reviewed = reviewed_by_id.get(candidate["candidate_id"])
            if reviewed and reviewed.get("decision") in {"accepted", "false_positive"} and reviewed.get("reviewer"):
                final_rows.append(reviewed)
            else:
                unresolved.append(candidate)
                final_rows.append(candidate)
        final_rows.extend(row for row in reviewed_rows if row not in final_rows)
        ledger_path = args.output_dir / f"{args.book_id}_ocr-review.tsv"
        write_ledger(ledger_path, final_rows)

        if unresolved or (extraction_method == "ocr" and not (args.accept_ocr and args.reviewer)):
            tree["review_status"] = "pending_ocr_review"
        canonical = args.output_dir / f"{args.book_id}_tree.json"
        canonical.write_text(json.dumps(tree, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        manifest = {
            "book_id": args.book_id,
            "title": args.title,
            "source": str(source),
            "source_sha256": sha256(source),
            "source_format": source.suffix.lower().lstrip("."),
            "extraction_method": extraction_method,
            "page_count": len(pages),
            "toc_pages": toc_pages,
            "toc_entries": len(toc),
            "unresolved_ocr_candidates": len(unresolved),
        }
        (work_dir / "source-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        build_one(canonical, args.output_dir, replace=True)
        validator = Path(__file__).with_name("validate_bundle.py")
        command = [
            sys.executable,
            str(validator),
            str(canonical),
            "--artifact-dir",
            str(args.output_dir),
            "--ocr-review",
            str(ledger_path),
            "--require-ocr-review",
            "--min-heading-score",
            str(args.min_heading_score),
            "--fail-on-warnings",
        ]
        validation = subprocess.run(command, text=True, capture_output=True, check=False)
        (work_dir / "validation.log").write_text(validation.stdout + validation.stderr, encoding="utf-8")
        if validation.stdout:
            print(validation.stdout, end="")
        if validation.stderr:
            print(validation.stderr, end="", file=sys.stderr)

        if tree["review_status"] != "approved" or validation.returncode != 0:
            print(
                f"DRAFT\t{canonical}\t{len(toc)} nodes\t{len(unresolved)} unresolved OCR candidates",
                file=sys.stderr,
            )
            return 3
        print(f"PASS\t{canonical}\t{len(toc)} nodes")
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR\t{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
