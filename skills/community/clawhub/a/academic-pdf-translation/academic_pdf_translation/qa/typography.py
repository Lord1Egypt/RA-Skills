"""QA 的排版度量：字号、行距、留白、行宽。

这一族回答的是**这一页排得像不像正经排版**：正文字号是多少、行距有没有
被撑开、左右留白是不是塌了、有没有一行只剩一个汉字吊在那里。

它们只量，不判。阈值和豁免留在调用方——同一个数字在不同档位下的含义
不一样，把判断塞进度量里，以后改档位就得改度量。

函数体与搬出来之前逐字一致，只去掉了私有前缀。
"""

from __future__ import annotations

import statistics
from collections import Counter
from typing import Any

from academic_pdf_translation.qa.geometry import (
    in_any_region,
    region_covers_page,
    regions_for_page,
)
from academic_pdf_translation.qa.text_signals import (
    HAN_CHARACTER_PATTERN,
    ORPHAN_TRAILING_PUNCTUATION,
    SOURCE_MAPPING_LABEL_PATTERN,
)


def body_spans(
    page: Any,
    page_number: int,
    spans: list[dict],
    overrides: dict,
    retained_regions: list[dict],
) -> tuple[list[dict], str]:
    spans = [
        span
        for span in spans
        if not SOURCE_MAPPING_LABEL_PATTERN.fullmatch(
            str(span.get("text") or "").strip()
        )
    ]
    body_regions = regions_for_page(
        overrides.get("body_regions", []), page_number
    )
    non_body_regions = regions_for_page(
        overrides.get("non_body_regions", []), page_number
    )
    reference_regions = [
        region
        for region in retained_regions
        if region.get("category") in {"references", "bibliography"}
    ]
    if any(region_covers_page(page, region) for region in non_body_regions):
        return [], "explicit-non-body"
    if body_regions:
        return [
            span for span in spans if in_any_region(span["bbox"], body_regions)
        ], "explicit"

    top = float(page.rect.height) * 0.06
    bottom = float(page.rect.height) * 0.93
    result = []
    for span in spans:
        bbox = span["bbox"]
        if float(bbox[1]) < top or float(bbox[3]) > bottom:
            continue
        if in_any_region(bbox, non_body_regions):
            continue
        if in_any_region(bbox, reference_regions):
            continue
        result.append(span)
    return result, "heuristic"


def weighted_font_mode(spans: list[dict]) -> float | None:
    weights: Counter[float] = Counter()
    for span in spans:
        text = span.get("text", "").strip()
        if not text:
            continue
        weights[round(float(span["size"]), 1)] += max(len(text), 1)
    if not weights:
        return None
    return float(weights.most_common(1)[0][0])


def low_table_spans(
    spans: list[dict],
    table_regions: list[dict],
    minimum_font_pt: float,
) -> list[dict]:
    hits: list[dict] = []
    for span in spans:
        text = span.get("text", "").strip()
        size = float(span.get("size", 0))
        if (
            len(text) >= 2
            and size < minimum_font_pt
            and not int(span.get("flags", 0)) & 1
            and in_any_region(span["bbox"], table_regions)
        ):
            hits.append(
                {
                    "text": text[:120],
                    "size": round(size, 3),
                    "bbox": [
                        round(float(value), 2) for value in span["bbox"]
                    ],
                }
            )
    return hits


def leading_ratios(
    text_dict: dict,
    body_mode: float | None,
    page_number: int,
    overrides: dict,
    retained_regions: list[dict],
) -> list[float]:
    if body_mode is None:
        return []
    non_body_regions = regions_for_page(
        overrides.get("non_body_regions", []), page_number
    )
    reference_regions = [
        region
        for region in retained_regions
        if region.get("category") in {"references", "bibliography"}
    ]
    ratios: list[float] = []
    for block in text_dict["blocks"]:
        if block.get("type") != 0:
            continue
        lines = block.get("lines", [])
        for previous, current in zip(lines, lines[1:], strict=False):
            if in_any_region(current["bbox"], non_body_regions):
                continue
            if in_any_region(current["bbox"], reference_regions):
                continue
            previous_spans = [
                span for span in previous.get("spans", []) if span.get("text", "").strip()
            ]
            current_spans = [
                span for span in current.get("spans", []) if span.get("text", "").strip()
            ]
            if not previous_spans or not current_spans:
                continue
            size = statistics.median(
                [float(span["size"]) for span in previous_spans + current_spans]
            )
            if abs(size - body_mode) > 1.2 or size <= 0:
                continue
            baseline_gap = float(current["bbox"][3]) - float(previous["bbox"][3])
            ratio = baseline_gap / size
            if 0.8 <= ratio <= 3.0:
                ratios.append(ratio)
    return ratios


def column_blank_ratio(page: Any, body_spans: list[dict]) -> float:
    page_rect = page.rect
    page_width = float(page_rect.width)
    page_center = float(page_rect.x0) + page_width / 2
    center_margin = page_width * 0.06
    text_total = sum(len(span.get("text", "").strip()) for span in body_spans)
    center_crossing = [
        span
        for span in body_spans
        if (
            len(span.get("text", "").strip()) >= 12
            and float(span["bbox"][0]) <= page_center - center_margin
            and float(span["bbox"][2]) >= page_center + center_margin
        )
    ]
    center_crossing_chars = sum(
        len(span.get("text", "").strip()) for span in center_crossing
    )
    single_column = (
        len(center_crossing) >= 5
        and text_total > 0
        and center_crossing_chars / text_total >= 0.25
    )
    usable_bottom = float(page_rect.height) * 0.9
    usable_height = float(page_rect.height) * 0.84
    if single_column:
        content_bottom = max(
            (float(span["bbox"][3]) for span in body_spans),
            default=usable_bottom,
        )
        return round(
            max(0.0, usable_bottom - content_bottom) / usable_height,
            3,
        )

    ratios: list[float] = []
    for left, right in (
        (float(page_rect.x0), float(page_rect.x0 + page_rect.width / 2)),
        (float(page_rect.x0 + page_rect.width / 2), float(page_rect.x1)),
    ):
        column = [
            span
            for span in body_spans
            if left
            <= (float(span["bbox"][0]) + float(span["bbox"][2])) / 2
            < right
        ]
        if sum(len(span["text"].strip()) for span in column) < 80:
            continue
        content_bottom = max(float(span["bbox"][3]) for span in column)
        ratios.append(max(0.0, usable_bottom - content_bottom) / usable_height)
    return round(max(ratios, default=0.0), 3)


def top_blank_ratio(page: Any, body_spans: list[dict]) -> float:
    if sum(len(span["text"].strip()) for span in body_spans) < 80:
        return 0.0
    page_height = float(page.rect.height)
    usable_top = page_height * 0.06
    usable_height = page_height * 0.84
    content_top = min(float(span["bbox"][1]) for span in body_spans)
    return round(max(0.0, content_top - usable_top) / usable_height, 3)


def body_line_width_ratio(
    page: Any,
    text_dict: dict,
    body_spans: list[dict],
) -> tuple[float | None, int]:
    if not body_spans:
        return None, 0
    body_keys = {
        (
            tuple(round(float(value), 3) for value in span["bbox"]),
            str(span.get("text", "")),
        )
        for span in body_spans
    }
    ratios: list[float] = []
    page_width = max(float(page.rect.width), 1.0)
    for block in text_dict["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            selected = [
                span
                for span in line.get("spans", [])
                if (
                    tuple(round(float(value), 3) for value in span["bbox"]),
                    str(span.get("text", "")),
                )
                in body_keys
            ]
            text = "".join(span.get("text", "") for span in selected).strip()
            if len(text) < 12:
                continue
            x0 = min(float(span["bbox"][0]) for span in selected)
            x1 = max(float(span["bbox"][2]) for span in selected)
            ratio = max(0.0, x1 - x0) / page_width
            if ratio >= 0.08:
                ratios.append(ratio)
    if not ratios:
        return None, 0
    return round(statistics.median(ratios), 3), len(ratios)


def orphan_single_han_lines(
    text_dict: dict,
    body_spans: list[dict],
) -> list[dict]:
    if not body_spans:
        return []
    body_keys = {
        (
            tuple(round(float(value), 3) for value in span["bbox"]),
            str(span.get("text", "")),
        )
        for span in body_spans
    }
    lines: list[dict] = []
    for block in text_dict["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            selected = [
                span
                for span in line.get("spans", [])
                if (
                    tuple(round(float(value), 3) for value in span["bbox"]),
                    str(span.get("text", "")),
                )
                in body_keys
            ]
            text = "".join(span.get("text", "") for span in selected).strip()
            if not text:
                continue
            lines.append(
                {
                    "text": text,
                    "bbox": [
                        min(float(span["bbox"][0]) for span in selected),
                        min(float(span["bbox"][1]) for span in selected),
                        max(float(span["bbox"][2]) for span in selected),
                        max(float(span["bbox"][3]) for span in selected),
                    ],
                    "size": statistics.median(
                        float(span["size"]) for span in selected
                    ),
                }
            )
    lines.sort(key=lambda item: (item["bbox"][1], item["bbox"][0]))
    hits: list[dict] = []
    for previous, current in zip(lines, lines[1:], strict=False):
        orphan_core = current["text"].rstrip(
            ORPHAN_TRAILING_PUNCTUATION
        )
        if (
            not HAN_CHARACTER_PATTERN.fullmatch(orphan_core)
            or len(previous["text"]) < 8
            or abs(float(previous["size"]) - float(current["size"])) > 0.4
        ):
            continue
        vertical_gap = float(current["bbox"][1]) - float(previous["bbox"][3])
        if -0.5 <= vertical_gap <= float(current["size"]) * 1.5:
            hits.append(
                {
                    "text": current["text"],
                    "previous_text": previous["text"][-80:],
                    "bbox": [round(value, 2) for value in current["bbox"]],
                }
            )
    return hits


def interline_gap_outliers(
    text_dict: dict,
    body_spans: list[dict],
    body_mode: float | None,
    minimum_ratio: float = 4.0,
) -> list[dict]:
    if not body_spans or body_mode is None or body_mode <= 0:
        return []
    body_keys = {
        (
            tuple(round(float(value), 3) for value in span["bbox"]),
            str(span.get("text", "")),
        )
        for span in body_spans
    }
    all_lines: list[dict] = []
    for block in text_dict["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            spans = [
                span
                for span in line.get("spans", [])
                if str(span.get("text") or "").strip()
            ]
            if not spans:
                continue
            all_lines.append(
                {
                    "text": "".join(
                        str(span.get("text") or "") for span in spans
                    ).strip(),
                    "bbox": [
                        min(float(span["bbox"][0]) for span in spans),
                        min(float(span["bbox"][1]) for span in spans),
                        max(float(span["bbox"][2]) for span in spans),
                        max(float(span["bbox"][3]) for span in spans),
                    ],
                }
            )
    lines: list[dict] = []
    for block in text_dict["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            selected = [
                span
                for span in line.get("spans", [])
                if (
                    tuple(round(float(value), 3) for value in span["bbox"]),
                    str(span.get("text", "")),
                )
                in body_keys
            ]
            text = "".join(span.get("text", "") for span in selected).strip()
            if not text:
                continue
            lines.append(
                {
                    "text": text,
                    "bbox": [
                        min(float(span["bbox"][0]) for span in selected),
                        min(float(span["bbox"][1]) for span in selected),
                        max(float(span["bbox"][2]) for span in selected),
                        max(float(span["bbox"][3]) for span in selected),
                    ],
                    "size": statistics.median(
                        float(span["size"]) for span in selected
                    ),
                }
            )
    lines.sort(key=lambda item: (item["bbox"][1], item["bbox"][0]))
    hits: list[dict] = []
    for previous, current in zip(lines, lines[1:], strict=False):
        gap = float(current["bbox"][1]) - float(previous["bbox"][3])
        size = statistics.median(
            [float(previous["size"]), float(current["size"])]
        )
        if gap <= 0 or size <= 0:
            continue
        ratio = gap / size
        if ratio >= minimum_ratio:
            gap_left = min(
                float(previous["bbox"][0]),
                float(current["bbox"][0]),
            )
            gap_right = max(
                float(previous["bbox"][2]),
                float(current["bbox"][2]),
            )
            occupied = False
            for line in all_lines:
                center_y = (
                    float(line["bbox"][1]) + float(line["bbox"][3])
                ) / 2
                if not (
                    float(previous["bbox"][3]) < center_y
                    < float(current["bbox"][1])
                ):
                    continue
                horizontal_overlap = max(
                    0.0,
                    min(gap_right, float(line["bbox"][2]))
                    - max(gap_left, float(line["bbox"][0])),
                )
                if horizontal_overlap >= 4.0:
                    occupied = True
                    break
            if occupied:
                continue
            hits.append(
                {
                    "gap_pt": round(gap, 2),
                    "gap_to_font_ratio": round(ratio, 2),
                    "previous_text": previous["text"][-80:],
                    "next_text": current["text"][:80],
                }
            )
    return hits
