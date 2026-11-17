from __future__ import annotations

import argparse
import re
import statistics
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import perf_trace
from _common import (
    SkillError,
    complex_payload_replaced_unit_ids,
    internal_job_path,
    load_json,
    write_json,
)
from candidate_analysis import open_candidate_analysis
from candidate_page_map import (
    candidate_pages_for_source,
    load_candidate_page_map,
)
from content_anchors import (
    acronyms as extract_acronyms,
)
from content_anchors import (
    anchors_present,
    converted_statistics,
    required_anchors,
)
from content_anchors import (
    citation_numbers as extract_citation_numbers,
)
from content_anchors import (
    present_acronyms as extract_present_acronyms,
)
from content_anchors import (
    statistics as extract_statistics,
)
from extract_source_structure import extract_source_structure
from retained_source import (
    REFERENCE_CATEGORIES,
    extract_retained_regions,
    retained_region_covers_page,
    retained_regions_by_page,
    strip_retained_blocks,
)
from translation_truthfulness import evaluate_translation

CONTENT_RE = re.compile(r"[\w\u3400-\u9fff]", re.UNICODE)
SOURCE_SENTENCE_RE = re.compile(r"(?<=[.!?])(?:[\"')\]]+)?\s+")
TARGET_SENTENCE_RE = re.compile(r"[。！？!?]+")

TRANSLATION_REPAIR_FLAGS = {
    "SEVERE_TRANSLATION_COMPRESSION",
    "POSSIBLE_SUMMARY_OR_OMISSION",
    "LOW_SENTENCE_RETENTION",
    "STATISTICAL_ANCHOR_LOSS",
    "CITATION_ANCHOR_LOSS",
    "TERM_OR_ACRONYM_LOSS",
    "SECTION_HEADING_LOSS",
}
METADATA_REPAIR_FLAGS = {"URL_LOSS", "DOI_LOSS"}


def _content_length(text: str) -> int:
    return len(CONTENT_RE.findall(text or ""))


def _sentence_count(text: str, target: bool) -> int:
    if not text.strip():
        return 0
    pieces = (
        TARGET_SENTENCE_RE.split(text)
        if target
        else SOURCE_SENTENCE_RE.split(text)
    )
    return sum(1 for piece in pieces if _content_length(piece) >= 8)


def _citation_numbers(text: str) -> set[str]:
    return extract_citation_numbers(text)


def _stats(text: str) -> set[str]:
    return extract_statistics(text)


def _remove_percent_marker_only_mismatches(
    missing: set[str],
    target_text: str,
) -> set[str]:
    target_numeric_cores = {
        value[:-1] if value.endswith("%") else value
        for value in _stats(target_text)
    }
    return {
        value
        for value in missing
        if (value[:-1] if value.endswith("%") else value)
        not in target_numeric_cores
    }


def _acronyms(text: str) -> set[str]:
    return extract_acronyms(text)


def _anchors(text: str) -> set[str]:
    anchors = {f"citation:{value}" for value in _citation_numbers(text)}
    anchors.update(f"stat:{value}" for value in _stats(text))
    anchors.update(f"acronym:{value}" for value in _acronyms(text))
    return anchors


def _normalized_presence_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text or "").casefold()
    return "".join(
        character
        for character in normalized
        if unicodedata.category(character)[0] in {"L", "N"}
    )


def _strip_page_furniture(
    text: str,
    structure_page: dict[str, Any],
) -> str:
    result = re.sub(
        r"\s+",
        " ",
        unicodedata.normalize("NFKC", text or ""),
    ).strip()
    furniture = [
        re.sub(
            r"\s+",
            " ",
            unicodedata.normalize(
                "NFKC",
                str(block.get("text") or ""),
            ),
        ).strip()
        for block in structure_page.get("blocks", [])
        if isinstance(block, dict) and block.get("page_furniture")
    ]
    for value in sorted(
        (value for value in furniture if value),
        key=len,
        reverse=True,
    ):
        result = result.replace(value, " ")
    return re.sub(r"\s+", " ", result).strip()


def _bbox_covered_by_retained_region(
    bbox: Any,
    retained_payloads: list[dict[str, Any]],
) -> bool:
    if (
        not isinstance(bbox, list)
        or len(bbox) != 4
        or not all(isinstance(value, (int, float)) for value in bbox)
    ):
        return False
    x0, y0, x1, y1 = map(float, bbox)
    if x1 <= x0 or y1 <= y0:
        return False
    area = (x1 - x0) * (y1 - y0)
    center_x = (x0 + x1) / 2
    center_y = (y0 + y1) / 2
    for payload in retained_payloads:
        if (
            payload.get("resolution") == "translated-nonreference-region"
            or not payload.get("blocks")
        ):
            continue
        region = payload.get("effective_bbox") or payload.get("bbox")
        if not isinstance(region, list) or len(region) != 4:
            continue
        rx0, ry0, rx1, ry1 = map(float, region)
        if rx0 <= center_x <= rx1 and ry0 <= center_y <= ry1:
            return True
        overlap_width = max(0.0, min(x1, rx1) - max(x0, rx0))
        overlap_height = max(0.0, min(y1, ry1) - max(y0, ry0))
        if overlap_width * overlap_height / max(area, 1.0) >= 0.5:
            return True
    return False


def _coordinate_filtered_source_text(
    structure_page: dict[str, Any],
    retained_payloads: list[dict[str, Any]],
) -> str | None:
    active_payloads = [
        payload
        for payload in retained_payloads
        if payload.get("resolution") != "translated-nonreference-region"
        and payload.get("blocks")
    ]
    blocks = [
        block
        for block in structure_page.get("blocks", [])
        if isinstance(block, dict)
    ]
    if not active_payloads or not blocks:
        return None

    by_id = {
        int(block["id"]): block
        for block in blocks
        if isinstance(block.get("id"), int)
    }
    layout = structure_page.get("layout", {})
    order_key = (
        "layout_order"
        if layout.get("selected_order") == "layout"
        else "native_order"
    )
    ordered_ids = [
        int(value)
        for value in layout.get(order_key, [])
        if isinstance(value, int) and value in by_id
    ]
    ordered_ids.extend(
        block_id for block_id in by_id if block_id not in set(ordered_ids)
    )

    paragraphs: list[str] = []
    for block_id in ordered_ids:
        block = by_id[block_id]
        if block.get("page_furniture"):
            continue
        lines = [
            line
            for line in block.get("lines", [])
            if isinstance(line, dict)
        ]
        if lines:
            kept_lines = [
                str(line.get("text") or "").strip()
                for line in lines
                if str(line.get("text") or "").strip()
                and not _bbox_covered_by_retained_region(
                    line.get("bbox"),
                    active_payloads,
                )
            ]
            if kept_lines:
                paragraphs.append("\n".join(kept_lines))
            continue
        text = str(block.get("text") or "").strip()
        if text and not _bbox_covered_by_retained_region(
            block.get("bbox"),
            active_payloads,
        ):
            paragraphs.append(text)
    return "\n\n".join(paragraphs)


def _complex_payload_text(value: Any, parent_key: str = "") -> list[str]:
    scalar_keys = {
        "title",
        "caption",
        "translation",
        "text",
        "label",
        "value",
        "name",
        "note",
        "footnote",
    }
    collection_keys = {
        "rows",
        "cells",
        "headers",
        "labels",
        "items",
        "annotations",
        "values",
        "notes",
        "footnotes",
    }
    if isinstance(value, str):
        if parent_key in scalar_keys or parent_key in collection_keys:
            return [value]
        return []
    if isinstance(value, (int, float)):
        return [str(value)] if parent_key in collection_keys else []
    if isinstance(value, list):
        return [
            text
            for item in value
            for text in _complex_payload_text(item, parent_key)
        ]
    if isinstance(value, dict):
        return [
            text
            for key, item in value.items()
            if key not in {"suppress_texts", "source_evidence", "notes"}
            for text in _complex_payload_text(item, str(key))
        ]
    return []


def _heading_expectations(
    units: list[dict[str, Any]],
    complex_items: list[dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    expectations: list[dict[str, str]] = []
    replaced_unit_ids = complex_payload_replaced_unit_ids(
        units,
        complex_items or [],
        minimum_unit_chars=4,
        minimum_group_chars=4,
    )
    for unit in units:
        if str(unit.get("kind") or "").lower() not in {
            "title",
            "subtitle",
            "heading",
        }:
            continue
        if str(unit.get("id") or "") in replaced_unit_ids:
            continue
        expected = str(
            unit.get("translation")
            or unit.get("source")
            or ""
        ).strip()
        if not expected:
            continue
        expectations.append(
            {
                "unit_id": str(unit.get("id") or ""),
                "source": str(unit.get("source") or ""),
                "expected": expected,
            }
        )
    return expectations


def _page_translation(units: list[dict[str, Any]]) -> str:
    return "\n".join(
        str(unit.get("translation") or "")
        for unit in units
        if str(unit.get("translation") or "").strip()
    )


def _is_reference_unit(unit: dict[str, Any]) -> bool:
    """只有结构化证据才算参考文献单元。

    自由文本的 keep_source_reason 不再有效：它曾经能把任意正文单元变成
    “参考文献”，从而跳过后面全部检查。
    """

    kind = str(unit.get("kind") or "").lower()
    if kind.startswith(("reference", "bibliography")):
        return True
    return (
        not str(unit.get("translation") or "").strip()
        and str(unit.get("keep_source_code") or "").strip()
        == "bibliography-entry"
    )


def _is_reference_page(
    page_number: int,
    units: list[dict[str, Any]],
    retained_payloads: list[dict[str, Any]],
    page_width: float,
    page_height: float,
) -> bool:
    if units:
        total = sum(_content_length(str(unit.get("source") or "")) for unit in units)
        reference = sum(
            _content_length(str(unit.get("source") or ""))
            for unit in units
            if _is_reference_unit(unit)
        )
        if total and reference / total >= 0.9:
            return True
    return any(
        payload.get("page") == page_number
        and payload.get("category") in REFERENCE_CATEGORIES
        and retained_region_covers_page(
            payload,
            page_width,
            page_height,
        )
        for payload in retained_payloads
    )


def _candidate_visuals(
    candidate_doc: Any | None,
    page_numbers: list[int],
) -> dict[str, int]:
    if candidate_doc is None:
        return {"drawings": 0, "images": 0, "text_blocks": 0}
    pages = [
        candidate_doc[page_number - 1]
        for page_number in page_numbers
        if 1 <= page_number <= candidate_doc.page_count
    ]
    return {
        "drawings": sum(len(page.get_drawings()) for page in pages),
        "images": sum(len(page.get_images(full=True)) for page in pages),
        "text_blocks": sum(
            len(
                [
                    block
                    for block in page.get_text("blocks")
                    if str(block[4]).strip()
                ]
            )
            for page in pages
        ),
    }


def _source_visuals(structure_page: dict[str, Any]) -> dict[str, int]:
    return {
        "drawings": int(structure_page.get("drawing_count", 0)),
        "images": len(structure_page.get("images", [])),
        "text_blocks": len(
            [
                block
                for block in structure_page.get("blocks", [])
                if not block.get("page_furniture")
            ]
        ),
    }


def _visual_rebuild_issue(
    item: dict[str, Any],
    source_visuals: dict[str, int],
    candidate_visuals: dict[str, int],
) -> str | None:
    if item.get("text_status") == "not-applicable" or item.get("status") == "not-applicable":
        return None
    method = str(item.get("method") or "")
    if method == "vector-rebuild":
        expected = max(4, min(12, round(source_visuals["drawings"] * 0.1)))
        if (
            candidate_visuals["drawings"] < expected
            and candidate_visuals["images"] == 0
        ):
            return (
                f"声明为 vector-rebuild，但候选仅有 "
                f"{candidate_visuals['drawings']} 个绘图对象；"
                f"原页有 {source_visuals['drawings']} 个"
            )
    elif method in {"structured-table-rebuild", "semantic-grid-rebuild"}:
        if (
            candidate_visuals["drawings"] < 3
            and candidate_visuals["images"] == 0
        ):
            return (
                f"声明为 {method}，但候选没有足够网格或图像结构"
            )
    elif method == "image-text-localization":
        if candidate_visuals["images"] == 0 and candidate_visuals["drawings"] < 4:
            return "声明为 image-text-localization，但候选未检测到图像或等价矢量结构"
    return None


def _ratio_floor(source_language: str, target_language: str) -> tuple[float, float]:
    if source_language in {"en", "und-Latn"} and target_language.startswith("zh"):
        return 0.2, 0.25
    if source_language in {"en", "und-Latn"} and target_language in {"ja", "ko"}:
        return 0.22, 0.27
    return 0.45, 0.6


def _candidate_stage_has_current_pdf(status: Any) -> bool:
    return status in {"candidate", "accepted", "finalized"}


def _unit_compression_flags(
    kind: str,
    source_chars: int,
    ratio: float,
    hard_floor: float,
    review_floor: float,
    *,
    validated_keep_source: bool = False,
) -> list[str]:
    # 通过真实性检查的保留原文单元本来就没有译文，拿它衡量"译文压缩"没有意义。
    # 这里只信真实性检查给出的判定：自己写个理由把译文清空的单元，
    # 在同一次审查里已经被判为 invalid，整篇照样进返修。
    if validated_keep_source:
        return []
    compression_exempt = kind.lower() in {
        "title",
        "subtitle",
        "heading",
        "section-heading",
        "author",
        "affiliation",
        "metadata",
        "figure-or-caption",
        "table-or-caption",
        "table-note",
    }
    if compression_exempt or source_chars < 30:
        return []
    if ratio < hard_floor:
        return ["SEVERE_TRANSLATION_COMPRESSION"]
    if source_chars >= 120 and ratio < review_floor:
        return ["POSSIBLE_SUMMARY_OR_OMISSION"]
    return []


def _repair_tasks(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for page in pages:
        flags = set(page.get("flags", []))
        if not flags:
            continue
        actions: list[str] = []
        layers: list[str] = []
        if flags & TRANSLATION_REPAIR_FLAGS:
            layers.append("translation")
            actions.append(
                "回到该页原文文字块，按段落或语义区域重译；不得沿用现有摘要式译文。"
            )
        if "STATISTICAL_ANCHOR_LOSS" in flags:
            actions.append("逐项补回统计值、正负号、小数位、区间和显著性标记。")
        if "CITATION_ANCHOR_LOSS" in flags:
            actions.append("补回缺失的作者年份或编号引文，并保持与论述位置对应。")
        if "TERM_OR_ACRONYM_LOSS" in flags:
            actions.append("核对并补回量表、变量、模型和正式缩写。")
        if "SECTION_HEADING_LOSS" in flags:
            actions.append("恢复缺失章节标题及其下面的完整正文。")
        if flags & METADATA_REPAIR_FLAGS:
            layers.append("metadata")
            actions.append("补回 DOI、URL 和必要出版信息，保持可复制检索。")
        if "POSSIBLE_PAGE_MAPPING_DRIFT" in flags:
            layers.append("mapping")
            actions.append(
                "重新对齐本页与相邻页的原译关系；跨页续句只保留一次并记录真实来源页。"
            )
        if "COMPLEX_VISUAL_REBUILD_NOT_PRESENT" in flags:
            layers.append("layout")
            actions.append(
                "按图表清单重新构造实际网格、节点、连线、标签和数值；不能改成文字摘要。"
            )
        if any("看图确认阅读顺序" in note for note in page.get("notes", [])):
            layers.append("reading-order")
            actions.append("对照原页图像确认栏位和阅读顺序后，再生成译文单元。")
        evidence = {
            "translation_source_ratio": page.get("translation_source_ratio"),
            "sentence_retention_ratio": page.get("sentence_retention_ratio"),
            "missing_statistics": page.get("missing_statistics", []),
            "missing_citations": page.get("missing_citations", []),
            "missing_acronyms": page.get("missing_acronyms", []),
            "missing_urls": page.get("missing_urls", []),
            "missing_dois": page.get("missing_dois", []),
            "missing_headings": page.get("missing_headings", []),
            "shifted_headings": page.get("shifted_headings", []),
            "visual_rebuild_issues": page.get("visual_rebuild_issues", []),
            "unit_issues": page.get("unit_issues", []),
        }
        tasks.append(
            {
                "task_id": f"repair-page-{int(page['page']):04d}",
                "page": int(page["page"]),
                "priority": (
                    "high"
                    if flags
                    & {
                        "SEVERE_TRANSLATION_COMPRESSION",
                        "STATISTICAL_ANCHOR_LOSS",
                        "COMPLEX_VISUAL_REBUILD_NOT_PRESENT",
                    }
                    else "normal"
                ),
                "layers": sorted(set(layers)),
                "problem_codes": sorted(flags),
                "actions": list(dict.fromkeys(actions)),
                "evidence": evidence,
                "completion_check": (
                    "完成全部动作，重新生成临时候选并再次运行 preflight_candidate.py；"
                    "只有返回 READY_TO_REGISTER 才结束返修循环。"
                ),
            }
        )
    return tasks


def _timed_build_completeness_audit(
    job_dir: Path,
    *,
    include_candidate: bool = True,
) -> dict[str, Any]:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    source_path = internal_job_path(job_dir, job["source"]["job_path"])
    translation = load_json(
        internal_job_path(job_dir, job["files"]["translation"])
    )
    retained = load_json(
        internal_job_path(job_dir, job["files"]["retained_source"])
    )
    inventory = load_json(
        internal_job_path(job_dir, job["files"]["figure_inventory"])
    )
    complex_path = internal_job_path(
        job_dir,
        job.get("files", {}).get(
            "complex_content_payload",
            "complex_content.json",
        ),
    )
    complex_content = (
        load_json(complex_path)
        if complex_path.is_file()
        else {"items": []}
    )
    structure_path = job_dir / "source_structure.json"
    if structure_path.is_file():
        structure = load_json(structure_path)
    else:
        structure = extract_source_structure(source_path)
    source_analysis = open_candidate_analysis(source_path, role="source")
    source_doc = source_analysis.document
    retained_payloads = extract_retained_regions(
        source_doc,
        retained,
        translation,
    )
    retained_by_page = retained_regions_by_page(retained_payloads)

    units_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for unit in translation.get("units", []):
        page = unit.get("page")
        if isinstance(page, int):
            units_by_page[page].append(unit)

    candidate_path = internal_job_path(job_dir, job["files"]["candidate"])
    candidate_is_current_stage = (
        include_candidate
        and _candidate_stage_has_current_pdf(job.get("status"))
    )
    candidate_handle = (
        open_candidate_analysis(candidate_path)
        if candidate_is_current_stage and candidate_path.is_file()
        else None
    )
    candidate_doc = (
        candidate_handle.document if candidate_handle is not None else None
    )
    candidate_mapping = (
        load_candidate_page_map(
            job_dir,
            job,
            required=(
                "candidate_page_map" in job.get("files", {})
            ),
            candidate_path=candidate_path,
            translation=translation,
        )
        if candidate_doc is not None
        and (
            "candidate_page_map" in job.get("files", {})
            or (job_dir / "candidate-page-map.json").is_file()
        )
        else None
    )
    source_language = str(translation.get("source_language") or "und")
    target_language = str(translation.get("target_language") or "")
    hard_floor, review_floor = _ratio_floor(source_language, target_language)

    inventory_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for item in inventory.get("items", []):
        page = item.get("page")
        if isinstance(page, int):
            inventory_by_page[page].append(item)
    complex_text_by_page: dict[int, list[str]] = defaultdict(list)
    complex_items_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    structured_complex_pages: set[int] = set()
    for item in complex_content.get("items", []):
        page = item.get("page") if isinstance(item, dict) else None
        if not isinstance(page, int):
            continue
        complex_items_by_page[page].append(item)
        complex_text_by_page[page].extend(
            _complex_payload_text(item.get("payload"))
        )
        if (
            item.get("status") == "ready"
            and item.get("method")
            in {"structured-table-rebuild", "semantic-grid-rebuild"}
        ):
            structured_complex_pages.add(page)

    translations = {
        page: _page_translation(units)
        for page, units in units_by_page.items()
    }
    candidate_page_texts = (
        {
            page_number: _normalized_presence_text(
                candidate_doc[page_number - 1].get_text("text")
            )
            for page_number in range(1, candidate_doc.page_count + 1)
        }
        if candidate_doc is not None
        else {}
    )
    anchor_map = {
        page: _anchors(text)
        for page, text in translations.items()
    }

    truthfulness = evaluate_translation(
        translation,
        retained_source=retained,
    )
    validated_keep_source_ids = {
        verdict["unit_id"]
        for verdict in truthfulness["units"]
        if verdict["state"] == "kept-source"
    }

    pages: list[dict[str, Any]] = []
    document_ratios: list[float] = []
    required_repair_flags = {
        "SEVERE_TRANSLATION_COMPRESSION",
        "STATISTICAL_ANCHOR_LOSS",
        "COMPLEX_VISUAL_REBUILD_NOT_PRESENT",
    }
    for structure_page in structure.get("pages", []):
        page_number = int(structure_page["page"])
        units = units_by_page.get(page_number, [])
        page_retained = retained_by_page.get(page_number, [])
        page_rect = source_doc[page_number - 1].rect
        reference_page = _is_reference_page(
            page_number,
            units,
            retained_payloads,
            float(page_rect.width),
            float(page_rect.height),
        )
        content_units = [unit for unit in units if not _is_reference_unit(unit)]
        coordinate_source_text = _coordinate_filtered_source_text(
            structure_page,
            page_retained,
        )
        if coordinate_source_text is not None:
            source_text = coordinate_source_text
        else:
            source_text = "\n".join(
                strip_retained_blocks(
                    str(unit.get("source") or ""),
                    page_retained,
                )
                for unit in content_units
            )
        if not source_text:
            if reference_page:
                source_text = ""
            else:
                source_text = str(
                    structure_page.get("text_layer", {}).get("native_text") or ""
                )
        source_text = _strip_page_furniture(source_text, structure_page)
        complex_target_text = "\n".join(
            complex_text_by_page.get(page_number, [])
        )
        adjacent_target_text = "\n".join(
            value
            for neighbor in (page_number - 1, page_number + 1)
            for value in (
                translations.get(neighbor, ""),
                "\n".join(complex_text_by_page.get(neighbor, [])),
            )
            if value.strip()
        )
        target_text = "\n".join(
            value
            for value in (
                _page_translation(content_units),
                complex_target_text,
            )
            if value.strip()
        )
        source_chars = _content_length(source_text)
        target_chars = _content_length(target_text)
        ratio = round(target_chars / source_chars, 3) if source_chars else None
        unit_issues: list[dict[str, Any]] = []
        for unit in content_units:
            if (
                coordinate_source_text is not None
                and len(content_units) == 1
                and not unit.get("source_bbox")
            ):
                unit_source = source_text
            else:
                unit_source = strip_retained_blocks(
                    str(unit.get("source") or ""),
                    page_retained,
                )
                unit_source = _strip_page_furniture(
                    unit_source,
                    structure_page,
                )
            unit_target = "\n".join(
                value
                for value in (
                    str(unit.get("translation") or ""),
                    complex_target_text,
                )
                if value.strip()
            )
            unit_source_chars = _content_length(unit_source)
            unit_target_chars = _content_length(unit_target)
            if unit_source_chars < 30:
                continue
            unit_kind = str(unit.get("kind") or "").lower()
            unit_ratio = round(
                unit_target_chars / unit_source_chars,
                3,
            )
            unit_missing_stats_set = _stats(unit_source) - _stats(unit_target)
            unit_missing_stats_set -= converted_statistics(
                unit_source,
                "\n".join(
                    value
                    for value in (unit_target, adjacent_target_text)
                    if value.strip()
                ),
            )
            adjacent_unit_stats = (
                unit_missing_stats_set & _stats(adjacent_target_text)
            )
            if len(adjacent_unit_stats) >= 2:
                unit_missing_stats_set -= adjacent_unit_stats
            if page_number in structured_complex_pages:
                unit_missing_stats_set = (
                    _remove_percent_marker_only_mismatches(
                        unit_missing_stats_set,
                        "\n".join(
                            value
                            for value in (
                                unit_target,
                                adjacent_target_text,
                            )
                            if value.strip()
                        ),
                    )
                )
            unit_missing_stats = sorted(unit_missing_stats_set)
            unit_flags = _unit_compression_flags(
                unit_kind,
                unit_source_chars,
                unit_ratio,
                hard_floor,
                review_floor,
                validated_keep_source=(
                    str(unit.get("id") or "") in validated_keep_source_ids
                ),
            )
            source_unit_stats = _stats(unit_source)
            if (
                len(source_unit_stats) >= 4
                and len(unit_missing_stats) / len(source_unit_stats) >= 0.25
            ):
                unit_flags.append("STATISTICAL_ANCHOR_LOSS")
            if unit_flags:
                unit_issues.append(
                    {
                        "unit_id": unit.get("id"),
                        "source_ref": unit.get("source_ref"),
                        "source_chars": unit_source_chars,
                        "translation_chars": unit_target_chars,
                        "translation_source_ratio": unit_ratio,
                        "missing_statistics": unit_missing_stats,
                        "flags": sorted(set(unit_flags)),
                    }
                )
        if (
            not reference_page
            and source_chars >= 600
            and ratio is not None
            and ratio > 0
        ):
            document_ratios.append(ratio)

        source_sentences = _sentence_count(source_text, target=False)
        target_sentences = _sentence_count(target_text, target=True)
        sentence_ratio = (
            round(target_sentences / source_sentences, 3)
            if source_sentences
            else None
        )
        source_stats = _stats(source_text)
        target_stats = _stats(target_text)
        missing_stats_set = source_stats - target_stats
        missing_stats_set -= converted_statistics(
            source_text,
            "\n".join(
                value
                for value in (target_text, adjacent_target_text)
                if value.strip()
            ),
        )
        adjacent_statistics = missing_stats_set & _stats(adjacent_target_text)
        relocated_statistics = (
            adjacent_statistics if len(adjacent_statistics) >= 2 else set()
        )
        missing_stats_set -= relocated_statistics
        if page_number in structured_complex_pages:
            missing_stats_set = _remove_percent_marker_only_mismatches(
                missing_stats_set,
                "\n".join(
                    value
                    for value in (target_text, adjacent_target_text)
                    if value.strip()
                ),
            )
        missing_stats = sorted(missing_stats_set)
        source_citations = _citation_numbers(source_text)
        target_citations = _citation_numbers(target_text)
        missing_citations = sorted(
            source_citations - target_citations,
            key=lambda value: int(value),
        )
        source_acronyms = _acronyms(source_text)
        target_acronyms = extract_present_acronyms(target_text)
        missing_acronyms = sorted(source_acronyms - target_acronyms)
        source_link_anchors = required_anchors(source_text)
        missing_link_anchors = anchors_present(
            source_link_anchors,
            target_text,
        )
        missing_urls = missing_link_anchors["urls"]
        missing_dois = missing_link_anchors["dois"]

        headings = (
            []
            if reference_page
            else _heading_expectations(
                content_units,
                complex_items_by_page.get(page_number, []),
            )
        )
        missing_headings: list[str] = []
        shifted_headings: list[dict[str, Any]] = []
        for heading in headings:
            if candidate_doc is None:
                continue
            expected = _normalized_presence_text(heading["expected"])
            mapped_pages = candidate_pages_for_source(
                candidate_mapping,
                page_number,
            )
            mapped_text = "".join(
                candidate_page_texts.get(page, "")
                for page in mapped_pages
            )
            if expected in mapped_text:
                continue
            neighbor_hits = []
            for neighbor in (page_number - 1, page_number + 1):
                if neighbor < 1:
                    continue
                neighbor_text = "".join(
                    candidate_page_texts.get(page, "")
                    for page in candidate_pages_for_source(
                        candidate_mapping,
                        neighbor,
                    )
                )
                if expected in neighbor_text:
                    neighbor_hits.append(neighbor)
            if neighbor_hits:
                shifted_headings.append(
                    {
                        "unit_id": heading["unit_id"],
                        "source": heading["source"],
                        "found_on_pages": neighbor_hits,
                    }
                )
            else:
                missing_headings.append(heading["unit_id"])

        current_anchor_score = len(_anchors(source_text) & anchor_map.get(page_number, set()))
        neighbor_scores = {
            neighbor: len(_anchors(source_text) & anchor_map.get(neighbor, set()))
            for neighbor in (page_number - 1, page_number + 1)
            if neighbor in translations
        }
        best_neighbor = (
            max(neighbor_scores, key=neighbor_scores.get)
            if neighbor_scores
            else None
        )
        mapping_drift = bool(
            best_neighbor is not None
            and neighbor_scores[best_neighbor] >= current_anchor_score + 3
            and neighbor_scores[best_neighbor] >= max(5, current_anchor_score * 1.5)
        )

        source_visuals = _source_visuals(structure_page)
        candidate_visuals = _candidate_visuals(
            candidate_doc,
            candidate_pages_for_source(
                candidate_mapping,
                page_number,
            ),
        )
        visual_issues = (
            [
                {
                    "item_id": item.get("id"),
                    "method": item.get("method"),
                    "reason": reason,
                }
                for item in (
                    inventory_by_page.get(page_number, [])
                    + complex_items_by_page.get(page_number, [])
                )
                if (
                    reason := _visual_rebuild_issue(
                        item,
                        source_visuals,
                        candidate_visuals,
                    )
                )
            ]
            if candidate_doc is not None
            else []
        )

        flags: list[str] = []
        notes: list[str] = []
        if not reference_page and source_chars >= 800 and ratio is not None:
            if ratio < hard_floor:
                flags.append("SEVERE_TRANSLATION_COMPRESSION")
            elif ratio < review_floor:
                flags.append("POSSIBLE_SUMMARY_OR_OMISSION")
        if (
            not reference_page
            and source_sentences >= 8
            and sentence_ratio is not None
            and sentence_ratio < 0.62
            and ratio is not None
            and ratio < review_floor + 0.04
        ):
            flags.append("LOW_SENTENCE_RETENTION")
        if (
            not reference_page
            and len(source_stats) >= 6
            and len(missing_stats) / len(source_stats) >= 0.25
        ):
            flags.append("STATISTICAL_ANCHOR_LOSS")
        if (
            not reference_page
            and len(source_citations) >= 8
            and len(missing_citations) / len(source_citations) >= 0.35
        ):
            flags.append("CITATION_ANCHOR_LOSS")
        if (
            not reference_page
            and len(source_acronyms) >= 5
            and len(missing_acronyms) / len(source_acronyms) >= 0.5
        ):
            flags.append("TERM_OR_ACRONYM_LOSS")
        if not reference_page and missing_urls:
            flags.append("URL_LOSS")
        if not reference_page and missing_dois:
            flags.append("DOI_LOSS")
        if missing_headings:
            flags.append("SECTION_HEADING_LOSS")
        if shifted_headings or mapping_drift:
            flags.append("POSSIBLE_PAGE_MAPPING_DRIFT")
        if relocated_statistics:
            flags.append("ADJACENT_PAGE_ANCHOR_SHIFT")
        if visual_issues:
            flags.append("COMPLEX_VISUAL_REBUILD_NOT_PRESENT")
        for issue in unit_issues:
            flags.extend(issue["flags"])
        if (
            not reference_page
            and source_chars >= 1800
            and len([unit for unit in units if unit.get("translation")]) <= 1
        ):
            notes.append("整页只绑定一个译文单元，无法自动证明逐段对应关系")
        if structure_page.get("layout", {}).get("selected_order") == "visual-confirmation-required":
            notes.append("PDF 内部顺序与坐标推断顺序冲突，需要看图确认阅读顺序")
        if relocated_statistics:
            notes.append(
                "本页部分数字出现在相邻页译文中，属于跨页续句或连续流重排。"
            )

        pages.append(
            {
                "page": page_number,
                "reference_page": reference_page,
                "source_chars": source_chars,
                "translation_chars": target_chars,
                "translation_source_ratio": ratio,
                "source_sentence_count": source_sentences,
                "translation_sentence_count": target_sentences,
                "sentence_retention_ratio": sentence_ratio,
                "missing_statistics": missing_stats,
                "adjacent_page_statistics": sorted(relocated_statistics),
                "missing_citations": missing_citations,
                "missing_acronyms": missing_acronyms,
                "missing_urls": missing_urls,
                "missing_dois": missing_dois,
                "source_headings": [
                    {
                        "unit_id": heading["unit_id"],
                        "source": heading["source"],
                    }
                    for heading in headings
                ],
                "missing_headings": missing_headings,
                "shifted_headings": shifted_headings,
                "anchor_score_current_page": current_anchor_score,
                "anchor_scores_neighbor_pages": neighbor_scores,
                "source_visuals": source_visuals,
                "candidate_visuals": candidate_visuals,
                "visual_rebuild_issues": visual_issues,
                "unit_issues": unit_issues,
                "flags": sorted(set(flags)),
                "notes": notes,
                "retained_source_chars_excluded": sum(
                    int(payload.get("source_char_count") or 0)
                    for payload in page_retained
                ),
            }
        )

    source_analysis.release()
    if candidate_handle is not None:
        candidate_handle.release()
    flag_counts = Counter(
        flag for page in pages for flag in page["flags"]
    )
    repair_pages = [
        page["page"]
        for page in pages
        if required_repair_flags.intersection(page["flags"])
    ]
    review_pages = [page["page"] for page in pages if page["flags"]]
    repair_tasks = _repair_tasks(
        [page for page in pages if page["page"] in repair_pages]
    )
    # 译文真实性不通过时，整篇直接进入返修，不看页级比例结论。
    # 这一步不读取 translation.coverage.complete：它由制作方自报，不作数。
    decision = (
        "NEEDS_REPAIR"
        if repair_pages or not truthfulness["complete"]
        else "REVIEW"
        if review_pages
        else "READY"
    )
    return {
        "schema_version": "1.0",
        "job_id": job.get("job_id"),
        "decision": decision,
        "translation_truthfulness": {
            "complete": truthfulness["complete"],
            "cross_language": truthfulness["cross_language"],
            "unit_count": truthfulness["unit_count"],
            "validated_translated_units": truthfulness[
                "validated_translated_units"
            ],
            "validated_kept_source_units": truthfulness[
                "validated_kept_source_units"
            ],
            "invalid_or_unverified_units": truthfulness[
                "invalid_or_unverified_units"
            ],
            "document_target_script_ratio": truthfulness[
                "document_target_script_ratio"
            ],
            "kept_source_content_ratio": truthfulness[
                "kept_source_content_ratio"
            ],
            "thresholds": truthfulness["thresholds"],
            "problem_counts": dict(
                sorted(
                    Counter(
                        problem["code"] for problem in truthfulness["problems"]
                    ).items()
                )
            ),
            "problems": truthfulness["problems"][:200],
        },
        "page_count": len(pages),
        "repair_pages": repair_pages,
        "review_pages": review_pages,
        "flag_counts": dict(sorted(flag_counts.items())),
        "repair_plan": {
            "schema_version": "1.0",
            "action": "repair-and-retry",
            "task_count": len(repair_tasks),
            "tasks": repair_tasks,
            "completion_condition": (
                "集中完成全部返修任务，重新生成候选并重复预检，"
                "直到状态为 READY_TO_REGISTER。"
            ),
        },
        "document_translation_source_ratio_median": (
            round(statistics.median(document_ratios), 3)
            if document_ratios
            else None
        ),
        "ratio_thresholds": {
            "severe": hard_floor,
            "review": review_floor,
            "language_pair": f"{source_language}->{target_language}",
        },
        "pages": pages,
        "interpretation": (
            "该脚本把文字提取、阅读顺序、译文完整性和图表重建分开检查。"
            "READY 仍不等于语义完全正确；NEEDS_REPAIR 是下一轮制作输入，"
            "不是任务终止状态。"
        ),
    }


def _markdown(report: dict[str, Any]) -> str:
    lines = [
        "# 翻译完整性审计",
        "",
        f"- 结论：`{report['decision']}`",
        f"- 返修页：{', '.join(map(str, report['repair_pages'])) or '无'}",
        f"- 需核对页：{', '.join(map(str, report['review_pages'])) or '无'}",
        f"- 全文译源字量比中位数：{report['document_translation_source_ratio_median']}",
        "",
        "| 页码 | 风险 | 译源字量比 | 句子保留比 | 图表声明问题 |",
        "|---:|---|---:|---:|---|",
    ]
    for page in report["pages"]:
        if not page["flags"]:
            continue
        visual = "；".join(
            issue["reason"] for issue in page["visual_rebuild_issues"]
        )
        lines.append(
            "| {page} | {flags} | {ratio} | {sentence} | {visual} |".format(
                page=page["page"],
                flags=", ".join(page["flags"]),
                ratio=page["translation_source_ratio"],
                sentence=page["sentence_retention_ratio"],
                visual=visual or "-",
            )
        )
    lines.extend(["", report["interpretation"], ""])
    return "\n".join(lines)



def build_completeness_audit(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("completeness_audit"):
        return _timed_build_completeness_audit(*args, **kwargs)

def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查正文是否摘要化、数字是否丢失、页面映射和图表重建是否真实"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()
    try:
        report = build_completeness_audit(args.job_dir)
        output_json = (
            args.output_json
            or args.job_dir.resolve() / "reviews" / "completeness-audit.json"
        )
        output_md = (
            args.output_md
            or args.job_dir.resolve() / "reviews" / "completeness-audit.md"
        )
        write_json(output_json.resolve(), report)
        output_md.resolve().parent.mkdir(parents=True, exist_ok=True)
        output_md.resolve().write_text(_markdown(report), encoding="utf-8")
        if report["decision"] == "NEEDS_REPAIR":
            write_json(
                args.job_dir.resolve() / "reviews" / "repair-plan.json",
                report["repair_plan"],
            )
        print(f"完整性审计: {report['decision']}")
        print(f"JSON: {output_json.resolve()}")
        print(f"Markdown: {output_md.resolve()}")
        if report["decision"] == "NEEDS_REPAIR":
            print(
                "返修任务: "
                f"{args.job_dir.resolve() / 'reviews' / 'repair-plan.json'}"
            )
            return 2
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
