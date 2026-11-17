from __future__ import annotations

import sys
from pathlib import Path as _Path

# 按 README 的写法直接跑时 sys.path 里没有仓库根，包就 import 不到。
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

import perf_trace
from _common import SkillError, import_fitz
from candidate_analysis import open_candidate_analysis

# 文献类目名的唯一定义已移入 academic_pdf_translation.render.reference_data，
# 这里再导出保持调用路径不变。
from academic_pdf_translation.render.reference_data import (  # noqa: F401
    REFERENCE_CATEGORIES,
)
REFERENCE_HEADING_RE = re.compile(
    r"^\s*(?:references|bibliography|literature\s+cited|works\s+cited)\s*$",
    re.IGNORECASE,
)
REFERENCE_HEADING_PREFIX_RE = re.compile(
    r"^\s*(references|bibliography|literature\s+cited|works\s+cited)"
    r"\s+(?=(?:\[\d+\]|\d+[.)]))",
    re.IGNORECASE,
)
REFERENCE_TAIL_LABEL_PATTERN = (
    r"(?:"
    r"conflict(?:s)?\s+of\s+interest|"
    r"author\s+contributions?|"
    r"acknowledg(?:e)?ments?|"
    r"funding|"
    r"data\s+availability|"
    r"ethics\s+statement|"
    r"publisher(?:[’']s)?\s+note|"
    r"supplementary\s+material|"
    r"copyright\b|"
    r"about\s+the\s+authors?"
    r")"
)
REFERENCE_TAIL_RE = re.compile(
    rf"^\s*{REFERENCE_TAIL_LABEL_PATTERN}",
    re.IGNORECASE,
)
REFERENCE_TAIL_INLINE_RE = re.compile(
    rf"(?<=[.\]\)])\s+(?={REFERENCE_TAIL_LABEL_PATTERN})",
    re.IGNORECASE,
)
YEAR_CITATION_RE = re.compile(r"\((?:19|20)\d{2}[a-z]?\)")
REFERENCE_START_RE = re.compile(
    r"^\s*(?:\d+\.\s*)?"
    r"(?:[A-ZÀ-ÖØ-Þ][^()]{0,220}|[A-Z][A-Za-z&.' -]{2,120})"
    r"\((?:19|20)\d{2}[a-z]?\)\.?",
)
NUMBERED_REFERENCE_RE = re.compile(
    r"^\s*(?!(?:19|20)\d{2}\.)(\d{1,4})\.\s+\S+"
)
NUMBERED_MARKER_RE = re.compile(
    r"(?:^|\s)(?!(?:19|20)\d{2}\.)(\d{1,4})\.\s+\S+"
)
AUTHOR_LEAD_RE = re.compile(
    r"^\s*[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]+,\s*[A-Z]\."
)
AUTHOR_INLINE_RE = re.compile(
    r"(?:^|\s)(?:\d+\.\s*)?"
    r"(?:(?:de|De|den|Den|van|Van|von|Von|der|Der|la|La|le|Le)\s+)?"
    r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]+,\s*[A-Z]\."
)
ORGANIZATION_INLINE_RE = re.compile(
    r"(?:^|\s)"
    r"(?:[A-Z][A-Za-z&.'-]+\s+){1,6}"
    r"[A-Z][A-Za-z&.'-]+\s+\((?:19|20)\d{2}[a-z]?\)"
)
NUMBERED_INLINE_RE = re.compile(
    r"(?<=[.?!\]])\s+"
    r"(?=(?!(?:19|20)\d{2}\.)\d{1,4}\.\s+\S)"
)
PERSON_ENTRY_BOUNDARY_RE = re.compile(
    r"(?<=[.\]\)])\s+"
    r"(?="
    r"(?:(?:de|De|den|Den|van|Van|von|Von|der|Der|la|La|le|Le|ter|Ter)\s+)?"
    r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]+"
    r"(?:\s+[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]+){0,2},\s*"
    r"(?:[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ’'`-]{1,}|[A-Z]\.)"
    r"(?:[^.:]|[A-Z]\.){0,180}\.\s+"
    r"(?:19|20)\d{2}[a-z]?\."
    r")"
)
PAREN_PERSON_ENTRY_BOUNDARY_RE = re.compile(
    r"(?<=[.\]\)])\s+"
    r"(?="
    r"(?:(?:de|De|den|Den|van|Van|von|Von|der|Der|la|La|le|Le|ter|Ter)\s+)?"
    r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]+"
    r"(?:\s+[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]+){0,2},\s*"
    r"[A-ZÀ-ÖØ-Þ]\."
    r"[^()]{0,220}\((?:19|20)\d{2}[a-z]?\)\."
    r")"
)
ORGANIZATION_ENTRY_BOUNDARY_RE = re.compile(
    r"(?<=[.\]\)])\s+"
    r"(?="
    r"[A-Z][A-Za-z&.'’-]+"
    r"(?:\s+(?:[A-Z][A-Za-z&.'’-]+|for|of|and|the)){1,10}"
    r"\.\s+(?:19|20)\d{2}[a-z]?\."
    r")"
)


def retained_region_id(region: dict[str, Any], index: int) -> str:
    explicit = str(region.get("id") or "").strip()
    if explicit:
        return explicit
    page = int(region.get("page") or 0)
    return f"p{page:04d}-retained-{index + 1:03d}"


def retained_region_ids(retained: dict[str, Any]) -> list[str]:
    return [
        retained_region_id(region, index)
        for index, region in enumerate(retained.get("regions", []))
        if isinstance(region, dict)
    ]


def _normalized(text: str) -> str:
    value = unicodedata.normalize("NFKC", text or "")
    return re.sub(r"\s+", " ", value).strip()


def _presence_token(text: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFKC", text or "").casefold()
        if unicodedata.category(character)[0] in {"L", "N"}
    )


def _clean_block_text(text: str) -> str:
    value = unicodedata.normalize("NFKC", text or "")
    value = re.sub(r"\u00ad\s*", "", value)
    value = value.translate(
        str.maketrans(
            {
                "\u2010": "-",
                "\u2011": "-",
                "\u2012": "-",
            }
        )
    )
    value = (
        value.replace("\u200b", "")
        .replace("\u2060", "")
    )
    value = re.sub(r"(?m)^\s*\d\s+\d\s*$", "", value)
    value = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"(https?://)\s+", r"\1", value, flags=re.I)
    value = re.sub(r"(?<=\bdoi\.)\s+(?=org/)", "", value, flags=re.I)
    value = re.sub(r"(?<=\bwww\.)\s+(?=[A-Za-z0-9])", "", value, flags=re.I)
    value = re.sub(r"(?<=\b10\.)\s+(?=\d{4,9}/)", "", value)
    value = re.sub(r"(?<=doi\.org/)\s+(?=10\.)", "", value, flags=re.I)
    return value


def _ends_with_reference_number_prefix(text: str) -> bool:
    return bool(
        re.search(
            r"(?<!\d)(?!(?:19|20)\d{2}\.)\d{1,4}\.\s*$",
            _clean_block_text(text),
        )
    )


def _boundary_follows_author_initial(
    text: str,
    boundary_start: int,
) -> bool:
    previous = text[:boundary_start].rstrip()
    return bool(re.search(r"(?:^|[\s,])[A-Z]\.$", previous))


def _ends_with_wrapped_surname_prefix(text: str) -> bool:
    cleaned = _clean_block_text(text)
    word = r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]+"
    particle = (
        r"(?:de|De|den|Den|van|Van|von|Von|der|Der|"
        r"la|La|le|Le|ter|Ter)\s+"
    )
    return bool(
        re.search(
            rf"(?:[.\]])\s+(?:{particle})?{word}"
            rf"(?:\s+{word})?\s*$",
            cleaned,
        )
        or re.search(
            rf"(?:\band\b|&)\s+(?:{particle})?{word}"
            rf"(?:\s+{word})?\s*$",
            cleaned,
        )
    )


def _valid_bbox(value: Any) -> tuple[float, float, float, float]:
    if (
        not isinstance(value, list)
        or len(value) != 4
        or not all(isinstance(item, (int, float)) for item in value)
    ):
        raise SkillError("retained_source.regions 中存在无效 bbox")
    x0, y0, x1, y1 = map(float, value)
    if x1 <= x0 or y1 <= y0:
        raise SkillError("retained_source.regions 中存在空 bbox")
    return x0, y0, x1, y1


def _is_page_furniture(
    record: dict[str, Any],
    page_height: float,
) -> bool:
    x0, y0, x1, y1 = record["bbox"]
    text = record["text"]
    if (
        y1 <= page_height * 0.10
        and re.fullmatch(r"\s*\d{1,4}\s*", text)
    ):
        return True
    if y1 <= page_height * 0.065:
        return (
            len(text) <= 180
            and not YEAR_CITATION_RE.search(text)
            and not REFERENCE_HEADING_RE.match(text)
        )
    if (
        y0 <= page_height * 0.04
        and y1 <= page_height * 0.10
        and len(text) <= 240
    ):
        return bool(
            re.search(
                r"(?:©|copyright|journal|volume|vol\.|"
                r"\bpp?\.\s*\d|doi\b|www\.)",
                text,
                re.IGNORECASE,
            )
        )
    if y0 >= page_height * 0.955 and len(text) <= 240:
        return bool(
            re.search(
                r"(?:www\.|volume|vol\.|article|journal|frontiers|"
                r"\b(?:19|20)\d{2}\b|\bpage\s+\d+\b)",
                text,
                re.IGNORECASE,
            )
        )
    return False


def _records_for_clip(page: Any, bbox: tuple[float, float, float, float]) -> list[dict[str, Any]]:
    fitz = import_fitz()
    clip = fitz.Rect(*bbox) & page.rect
    if clip.is_empty:
        return []
    records: list[dict[str, Any]] = []
    for block in page.get_text("blocks", clip=clip, sort=False):
        raw_text = str(block[4] or "")
        text = _clean_block_text(raw_text)
        if not text:
            continue
        records.append(
            {
                "bbox": [round(float(value), 3) for value in block[:4]],
                "raw_text": raw_text,
                "text": text,
                "role": "body",
            }
        )
    return records


def _reference_heading_record(
    page: Any,
    region_bbox: tuple[float, float, float, float],
) -> dict[str, Any] | None:
    region_x0, region_y0, region_x1, region_y1 = region_bbox
    candidates: list[dict[str, Any]] = []
    for block in page.get_text("blocks", sort=False):
        text = _clean_block_text(str(block[4] or ""))
        if not REFERENCE_HEADING_RE.match(text):
            continue
        if float(block[1]) + 90 < region_y0:
            continue
        if float(block[1]) > region_y1 + 1:
            continue
        heading_x0 = float(block[0])
        heading_x1 = float(block[2])
        horizontal_overlap = max(
            0.0,
            min(region_x1, heading_x1) - max(region_x0, heading_x0),
        )
        if horizontal_overlap <= 0:
            continue
        candidates.append(
            {
                "bbox": [round(float(value), 3) for value in block[:4]],
                "raw_text": str(block[4] or ""),
                "text": text,
                "role": "heading",
            }
        )
    if not candidates:
        return None
    return min(candidates, key=lambda item: abs(float(item["bbox"][1]) - region_y0))


def _column_order(records: list[dict[str, Any]], page_width: float) -> list[dict[str, Any]]:
    if len(records) < 3:
        return sorted(records, key=lambda item: (item["bbox"][1], item["bbox"][0]))

    x_positions = sorted(float(item["bbox"][0]) for item in records)
    clusters: list[list[float]] = []
    tolerance = page_width * 0.11
    for x0 in x_positions:
        if not clusters or x0 - sum(clusters[-1]) / len(clusters[-1]) > tolerance:
            clusters.append([x0])
        else:
            clusters[-1].append(x0)
    centers = [sum(cluster) / len(cluster) for cluster in clusters]
    if (
        len(centers) < 2
        or max(
            right - left
            for left, right in zip(centers, centers[1:])
        )
        < page_width * 0.18
    ):
        return sorted(records, key=lambda item: (item["bbox"][1], item["bbox"][0]))

    def order_key(item: dict[str, Any]) -> tuple[int, float, float]:
        x0 = float(item["bbox"][0])
        column = min(
            range(len(centers)),
            key=lambda index: abs(centers[index] - x0),
        )
        return column, float(item["bbox"][1]), x0

    return sorted(records, key=order_key)


def _reference_entries(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    current_lines: list[str] = []
    current_raw: list[str] = []
    current_bbox: list[float] | None = None
    numbered_markers = [
        int(match.group(1))
        for record in records
        for match in NUMBERED_MARKER_RE.finditer(
            str(record.get("raw_text") or record.get("text") or "")
        )
    ]
    numbered_mode = any(
        current == previous + 1
        for previous, current in zip(
            numbered_markers,
            numbered_markers[1:],
        )
    )

    def split_blob(text: str) -> list[str]:
        positions = {0}
        for boundary_pattern in (
            NUMBERED_INLINE_RE,
            PAREN_PERSON_ENTRY_BOUNDARY_RE,
            PERSON_ENTRY_BOUNDARY_RE,
            ORGANIZATION_ENTRY_BOUNDARY_RE,
        ):
            for match in boundary_pattern.finditer(text):
                if (
                    boundary_pattern is PERSON_ENTRY_BOUNDARY_RE
                    and _boundary_follows_author_initial(
                        text,
                        match.start(),
                    )
                ):
                    continue
                positions.add(match.end())
        for pattern in (AUTHOR_INLINE_RE, ORGANIZATION_INLINE_RE):
            for match in pattern.finditer(text):
                start = match.start()
                while start < len(text) and text[start].isspace():
                    start += 1
                if not numbered_mode:
                    numeric_prefix = re.match(
                        r"\d{1,4}\.\s+",
                        text[start:],
                    )
                    if numeric_prefix:
                        start += numeric_prefix.end()
                if start <= 0:
                    continue
                previous = text[:start].rstrip()
                if not previous or previous[-1] in {",", ";"}:
                    continue
                previous_word = re.search(r"([A-Za-z]+)\s*$", previous)
                if (
                    previous_word
                    and previous_word.group(1).casefold()
                    in {"de", "den", "van", "von", "der", "la", "le"}
                ):
                    continue
                if re.search(r"(?:\band\b|&|et\s+al\.?)\s*$", previous, re.I):
                    continue
                if re.search(
                    r"(?:\band\b|&)\s+"
                    r"(?:de|den|van|von|der|la|le|ter)\s+"
                    r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]+\s*$",
                    previous,
                    re.IGNORECASE,
                ):
                    continue
                if any(
                    0 < start - position <= 60
                    and not re.search(r"[.;)\]]", text[position:start])
                    for position in positions
                ):
                    continue
                lookahead = text[start : start + 260]
                if not YEAR_CITATION_RE.search(lookahead):
                    continue
                if not YEAR_CITATION_RE.search(previous):
                    continue
                positions.add(start)
        ordered = sorted(positions)
        return [
            text[start:end].strip()
            for start, end in zip(ordered, ordered[1:] + [len(text)])
            if text[start:end].strip()
        ]

    def flush() -> None:
        nonlocal current_lines, current_raw, current_bbox
        text = _clean_block_text("\n".join(current_lines))
        if text:
            for part in split_blob(text):
                entries.append(
                    {
                        "bbox": current_bbox or [0.0, 0.0, 0.0, 0.0],
                        "raw_text": part,
                        "text": part,
                        "role": "body",
                    }
                )
        current_lines = []
        current_raw = []
        current_bbox = None

    for record in records:
        if record.get("role") == "heading":
            flush()
            entries.append(record)
            continue
        raw_lines = [
            line.strip()
            for line in str(record.get("raw_text") or "").splitlines()
            if line.strip()
        ]
        if not raw_lines:
            raw_lines = [str(record.get("text") or "").strip()]
        first_clean = _clean_block_text(raw_lines[0])
        heading_prefix = REFERENCE_HEADING_PREFIX_RE.match(first_clean)
        if heading_prefix:
            flush()
            entries.append(
                {
                    "bbox": list(record["bbox"]),
                    "raw_text": heading_prefix.group(1),
                    "text": heading_prefix.group(1),
                    "role": "heading",
                }
            )
            remainder = first_clean[heading_prefix.end() :].strip()
            raw_lines = ([remainder] if remainder else []) + raw_lines[1:]
        elif REFERENCE_HEADING_RE.match(first_clean):
            flush()
            entries.append(
                {
                    "bbox": list(record["bbox"]),
                    "raw_text": first_clean,
                    "text": first_clean,
                    "role": "heading",
                }
            )
            raw_lines = raw_lines[1:]
        if not raw_lines:
            continue
        first_line = _clean_block_text(raw_lines[0])
        if (
            current_lines
            and AUTHOR_LEAD_RE.match(first_line)
            and not _ends_with_reference_number_prefix(current_lines[-1])
            and not _ends_with_wrapped_surname_prefix(current_lines[-1])
            and not _clean_block_text(current_lines[-1]).endswith(
                (",", ";", "&")
            )
        ):
            flush()
        for line in raw_lines:
            clean_line = _clean_block_text(line)
            numbered_start = NUMBERED_REFERENCE_RE.match(clean_line)
            author_year_start = (
                REFERENCE_START_RE.match(clean_line)
                if not numbered_start
                else None
            )
            if (
                current_lines
                and (
                    (numbered_mode and numbered_start)
                    or author_year_start
                )
                and not _ends_with_reference_number_prefix(
                    current_lines[-1]
                )
                and not _ends_with_wrapped_surname_prefix(
                    current_lines[-1]
                )
                and not _clean_block_text(current_lines[-1]).endswith(
                    (",", ";", "&")
                )
            ):
                flush()
            if current_bbox is None:
                current_bbox = list(record["bbox"])
            else:
                current_bbox = [
                    min(current_bbox[0], float(record["bbox"][0])),
                    min(current_bbox[1], float(record["bbox"][1])),
                    max(current_bbox[2], float(record["bbox"][2])),
                    max(current_bbox[3], float(record["bbox"][3])),
                ]
            current_lines.append(line)
            current_raw.append(line)
    flush()
    return entries


def _trim_reference_tail(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    trimmed: list[dict[str, Any]] = []
    for record in records:
        text = str(record.get("text") or "")
        if REFERENCE_TAIL_RE.match(text):
            break
        tail = REFERENCE_TAIL_INLINE_RE.search(text)
        if tail is None:
            trimmed.append(record)
            continue
        prefix = text[: tail.start()].strip()
        if prefix:
            trimmed.append(
                {
                    **record,
                    "raw_text": prefix,
                    "text": prefix,
                }
            )
        break
    return trimmed


def _translation_by_page(translation: dict[str, Any] | None) -> dict[int, str]:
    values: dict[int, list[str]] = defaultdict(list)
    if not isinstance(translation, dict):
        return {}
    for unit in translation.get("units", []):
        if not isinstance(unit, dict) or not isinstance(unit.get("page"), int):
            continue
        text = str(unit.get("translation") or "")
        if text.strip():
            values[int(unit["page"])].append(text)
    return {page: "\n".join(texts) for page, texts in values.items()}


def _translated_source_by_page(
    translation: dict[str, Any] | None,
) -> dict[int, str]:
    values: dict[int, list[str]] = defaultdict(list)
    if not isinstance(translation, dict):
        return {}
    for unit in translation.get("units", []):
        if (
            not isinstance(unit, dict)
            or not isinstance(unit.get("page"), int)
            or not str(unit.get("translation") or "").strip()
        ):
            continue
        source = str(unit.get("source") or "")
        if source.strip():
            values[int(unit["page"])].append(source)
    return {page: "\n".join(texts) for page, texts in values.items()}


def _records_have_reference_signal(records: list[dict[str, Any]]) -> bool:
    for record in records:
        text = str(record.get("text") or "")
        if (
            REFERENCE_HEADING_RE.match(text)
            or REFERENCE_START_RE.match(text)
            or NUMBERED_REFERENCE_RE.match(text)
            or YEAR_CITATION_RE.search(text)
            or (
                AUTHOR_LEAD_RE.match(text)
                and re.search(r"\b(?:19|20)\d{2}[a-z]?\b", text)
            )
        ):
            return True
    return False


def _records_covered_by_source(
    records: list[dict[str, Any]],
    source_text: str,
) -> bool:
    source_token = _presence_token(source_text)
    if not source_token:
        return False
    weighted_total = 0
    weighted_present = 0
    for record in records:
        token = _presence_token(str(record.get("text") or ""))
        if not token:
            continue
        weighted_total += len(token)
        if token in source_token:
            weighted_present += len(token)
    return bool(
        weighted_total
        and weighted_present / weighted_total >= 0.85
    )


def _timed_extract_retained_regions(
    source: Path | Any,
    retained: dict[str, Any],
    translation: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    close_document = isinstance(source, Path)
    handle = (
        open_candidate_analysis(source, role="source")
        if close_document
        else None
    )
    document = handle.document if handle is not None else source
    translated_pages = _translation_by_page(translation)
    translated_source_pages = _translated_source_by_page(translation)
    payloads: list[dict[str, Any]] = []
    try:
        for index, region in enumerate(retained.get("regions", [])):
            if not isinstance(region, dict):
                continue
            page_number = region.get("page")
            if (
                not isinstance(page_number, int)
                or not 1 <= page_number <= document.page_count
            ):
                raise SkillError("retained_source.regions 中存在无效页码")
            page = document[page_number - 1]
            bbox = _valid_bbox(region.get("bbox"))
            category = str(region.get("category") or "")
            records = _records_for_clip(page, bbox)
            raw_records = list(records)
            effective_bbox = list(bbox)
            resolution = "retained-source"

            if category in REFERENCE_CATEGORIES:
                effective_bbox[3] = min(
                    float(page.rect.y1),
                    effective_bbox[3] + 14.0,
                )
                heading = _reference_heading_record(
                    page,
                    bbox,
                )
                if heading is not None:
                    heading_y = float(heading["bbox"][1])
                    effective_bbox[1] = max(float(page.rect.y0), heading_y - 1.0)
                records = _records_for_clip(
                    page,
                    tuple(map(float, effective_bbox)),
                )
                records = [
                    record
                    for record in records
                    if not _is_page_furniture(record, float(page.rect.height))
                ]
                for record in records:
                    if REFERENCE_HEADING_RE.match(record["text"]):
                        record["role"] = "heading"
                records = _column_order(records, float(page.rect.width))
                records = _reference_entries(
                    _trim_reference_tail(records)
                )
                if (
                    not _records_have_reference_signal(records)
                    and _records_covered_by_source(
                        raw_records,
                        translated_source_pages.get(page_number, ""),
                    )
                ):
                    records = []
                    resolution = "translated-nonreference-region"
            else:
                records = sorted(
                    records,
                    key=lambda item: (item["bbox"][1], item["bbox"][0]),
                )

            region_text = "\n\n".join(record["text"] for record in records)
            target_token = _presence_token(
                translated_pages.get(page_number, "")
            )
            weighted_total = 0
            weighted_present = 0
            for record in records:
                token = _presence_token(record["text"])
                if not token:
                    continue
                weighted_total += len(token)
                if token in target_token:
                    weighted_present += len(token)
            already_present = bool(
                weighted_total
                and weighted_present / weighted_total >= 0.85
            )
            if resolution == "translated-nonreference-region":
                already_present = True
            payloads.append(
                {
                    "id": retained_region_id(region, index),
                    "page": page_number,
                    "category": category,
                    "reason": str(region.get("reason") or ""),
                    "render_policy": region.get("render_policy"),
                    "bbox": list(bbox),
                    "effective_bbox": [
                        round(float(value), 3) for value in effective_bbox
                    ],
                    "page_width": round(float(page.rect.width), 3),
                    "blocks": records,
                    "text": region_text,
                    "source_char_count": len(_presence_token(region_text)),
                    "already_present_in_translation": already_present,
                    "resolution": resolution,
                }
            )
    finally:
        if handle is not None:
            handle.release()
    return payloads


def retained_regions_by_page(
    payloads: list[dict[str, Any]],
) -> dict[int, list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for payload in payloads:
        if isinstance(payload.get("page"), int):
            grouped[int(payload["page"])].append(payload)
    for page in grouped:
        ordinary = [
            item
            for item in grouped[page]
            if str(item.get("category") or "") not in REFERENCE_CATEGORIES
        ]
        references = [
            item
            for item in grouped[page]
            if str(item.get("category") or "") in REFERENCE_CATEGORIES
        ]
        ordinary.sort(
            key=lambda item: (
                float(item.get("effective_bbox", item["bbox"])[1]),
                float(item.get("effective_bbox", item["bbox"])[0]),
            )
        )

        reference_columns: list[list[dict[str, Any]]] = []
        for item in sorted(
            references,
            key=lambda value: (
                float(value.get("effective_bbox", value["bbox"])[0]),
                float(value.get("effective_bbox", value["bbox"])[1]),
            ),
        ):
            bbox = item.get("effective_bbox", item["bbox"])
            x0 = float(bbox[0])
            page_width = max(
                float(value.get("page_width") or 0.0)
                for value in references
            )
            if page_width <= 0:
                page_width = max(
                    float(
                        value.get("effective_bbox", value["bbox"])[2]
                    )
                    for value in references
                )
            tolerance = max(page_width * 0.10, 12.0)
            if (
                not reference_columns
                or x0
                - sum(
                    float(
                        value.get(
                            "effective_bbox",
                            value["bbox"],
                        )[0]
                    )
                    for value in reference_columns[-1]
                )
                / len(reference_columns[-1])
                > tolerance
            ):
                reference_columns.append([item])
            else:
                reference_columns[-1].append(item)
        ordered_references = [
            item
            for column in reference_columns
            for item in sorted(
                column,
                key=lambda value: (
                    float(
                        value.get("effective_bbox", value["bbox"])[1]
                    ),
                    float(
                        value.get("effective_bbox", value["bbox"])[0]
                    ),
                ),
            )
        ]
        grouped[page] = ordinary + ordered_references
    return dict(grouped)


def strip_retained_blocks(
    text: str,
    payloads: list[dict[str, Any]],
) -> str:
    result = _normalized(text)
    block_texts = [
        _normalized(str(block.get("raw_text") or block.get("text") or ""))
        for payload in payloads
        for block in payload.get("blocks", [])
        if isinstance(block, dict)
    ]
    for block_text in sorted(
        (value for value in block_texts if value),
        key=len,
        reverse=True,
    ):
        result = result.replace(block_text, " ")
    return re.sub(r"\s+", " ", result).strip()


def retained_region_covers_page(
    payload: dict[str, Any],
    page_width: float,
    page_height: float,
) -> bool:
    x0, y0, x1, y1 = map(
        float,
        payload.get("effective_bbox") or payload.get("bbox") or [0, 0, 0, 0],
    )
    width_ratio = max(0.0, x1 - x0) / max(page_width, 1.0)
    height_ratio = max(0.0, y1 - y0) / max(page_height, 1.0)
    return width_ratio >= 0.82 and height_ratio >= 0.78


def extract_retained_regions(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("retained_region_extract"):
        return _timed_extract_retained_regions(*args, **kwargs)
