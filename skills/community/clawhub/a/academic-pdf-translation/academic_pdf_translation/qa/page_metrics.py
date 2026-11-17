"""逐页度量：把一页 PDF 折成一组可判定的数字。

从 ``scripts/qa_pdf.py`` 原样搬来，行为不变。这是 QA 的取数层——
它只**量**，不**判**：字号众数、行距、留白比例、越界、重叠、原文残留
都在这里数出来，够不够格由调用方按档位的阈值决定。

排版与几何工具沿用原文件里带下划线的别名导入。那不是笔误：函数体里
有同名的局部变量（``body_spans``、``low_table_spans``），别名正是用来
避开遮蔽的，改成正名会让代码在自己的局部变量上崩掉。

``target_character_count`` 依赖书写系统的语言配置，属于脚本层，按
``count_target_characters`` 注入；包内不反向依赖 scripts。
"""

from __future__ import annotations

import re
import statistics
from collections import Counter
from collections.abc import Callable
from typing import Any

from academic_pdf_translation.qa.content_rules import (
    looks_like_proper_name,
    meaningful_page_image_count,
)
from academic_pdf_translation.qa.geometry import (
    in_any_region as _in_any_region,
)
from academic_pdf_translation.qa.geometry import (
    reference_area_ratio as _reference_area_ratio,
)
from academic_pdf_translation.qa.geometry import (
    regions_for_page as _regions_for_page,
)
from academic_pdf_translation.qa.geometry import (
    structured_table_page as _structured_table_page,
)
from academic_pdf_translation.qa.geometry import (
    whole_page_reference as _whole_page_reference,
)
from academic_pdf_translation.qa.layout_rules import (
    sparse_layout_justified,
    text_block_overlaps,
    text_span_overlaps,
)
from academic_pdf_translation.qa.text_signals import (
    COMPATIBILITY_IDEOGRAPH_PATTERN,
    LATIN_PROSE_PATTERN,
    PLACEHOLDER_PATTERN,
)
from academic_pdf_translation.qa.typography import (
    body_line_width_ratio as _body_line_width_ratio,
)
from academic_pdf_translation.qa.typography import (
    body_spans as _body_spans,
)
from academic_pdf_translation.qa.typography import (
    column_blank_ratio as _column_blank_ratio,
)
from academic_pdf_translation.qa.typography import (
    interline_gap_outliers as _interline_gap_outliers,
)
from academic_pdf_translation.qa.typography import (
    leading_ratios as _leading_ratios,
)
from academic_pdf_translation.qa.typography import (
    low_table_spans as _low_table_spans,
)
from academic_pdf_translation.qa.typography import (
    orphan_single_han_lines as _orphan_single_han_lines,
)
from academic_pdf_translation.qa.typography import (
    top_blank_ratio as _top_blank_ratio,
)
from academic_pdf_translation.qa.typography import (
    weighted_font_mode as _weighted_font_mode,
)


def residual_source_prose(
    spans: list[dict],
    page_number: int,
    retained: dict,
    allowed_patterns: list[tuple[int | None, re.Pattern[str]]],
    allowed_corpus: str = "",
) -> list[dict]:
    regions = _regions_for_page(retained.get("regions", []), page_number)
    hits: list[dict] = []
    for span in spans:
        if _in_any_region(span["bbox"], regions):
            continue
        text = span["text"]
        text = re.sub(r"https?://\S+|doi:\s*\S+|10\.\d{4,9}/\S+", "", text, flags=re.I)
        for pattern_page, pattern in allowed_patterns:
            if pattern_page is None or pattern_page == page_number:
                text = pattern.sub("", text)
        for match in LATIN_PROSE_PATTERN.finditer(text):
            sample = match.group(0).strip()
            if len(sample) < 18:
                continue
            if looks_like_proper_name(sample):
                continue
            sample_key = re.sub(r"[^a-z0-9]+", "", sample.casefold())
            if sample_key and sample_key in allowed_corpus:
                continue
            hits.append(
                {
                    "page": page_number,
                    "text": sample[:220],
                    "bbox": [round(float(value), 2) for value in span["bbox"]],
                }
            )
    return hits

def page_metrics(
    page: Any,
    page_number: int,
    profile: dict,
    quality: dict,
    overrides: dict,
    retained: dict,
    allowed_patterns: list[tuple[int | None, re.Pattern[str]]],
    allowed_retained_corpus: str = "",
    *,
    count_target_characters: Callable[[str, str], int],
) -> dict:
    text_dict = page.get_text("dict")
    spans = [
        span
        for block in text_dict["blocks"]
        if block.get("type") == 0
        for line in block.get("lines", [])
        for span in line.get("spans", [])
        if span.get("text", "").strip()
    ]
    text = "\n".join(span["text"] for span in spans)
    retained_regions = _regions_for_page(retained.get("regions", []), page_number)
    non_body_regions = _regions_for_page(
        overrides.get("non_body_regions", []), page_number
    )
    table_regions = [
        region
        for region in non_body_regions
        if "table" in str(region.get("category", "")).lower()
    ]
    body_spans, body_detection = _body_spans(
        page, page_number, spans, overrides, retained_regions
    )
    body_mode = _weighted_font_mode(body_spans)
    table_font_min_pt = float(quality.get("table_font_min_pt", 7.0))
    low_table_spans = _low_table_spans(
        spans, table_regions, table_font_min_pt
    )
    body_font_size_weights: Counter[float] = Counter()
    for span in body_spans:
        span_text = span.get("text", "").strip()
        if span_text:
            body_font_size_weights[round(float(span["size"]), 1)] += len(
                span_text
            )
    leading = _leading_ratios(
        text_dict, body_mode, page_number, overrides, retained_regions
    )
    median_leading = round(statistics.median(leading), 3) if leading else None
    median_body_line_width, body_line_width_sample_count = (
        _body_line_width_ratio(page, text_dict, body_spans)
    )
    orphan_single_han_lines = _orphan_single_han_lines(
        text_dict, spans
    )
    interline_gap_outliers = _interline_gap_outliers(
        text_dict, body_spans, body_mode
    )
    low_body_spans = []
    if body_mode is not None:
        for span in body_spans:
            text_value = span["text"].strip()
            size = float(span["size"])
            if (
                len(text_value) >= 24
                and size < float(quality["body_font_min_pt"])
                and abs(size - body_mode) <= 1.2
            ):
                low_body_spans.append(
                    {
                        "text": text_value[:120],
                        "size": round(size, 3),
                        "bbox": [round(float(value), 2) for value in span["bbox"]],
                    }
                )

    out_of_bounds = []
    coordinate_rect = (
        page.cropbox
        if int(getattr(page, "rotation", 0)) in {90, 270}
        else page.rect
    )
    bounds_tolerance = (
        3.0 if int(getattr(page, "rotation", 0)) in {90, 270} else 0.5
    )
    for span in spans:
        rect = span["bbox"]
        if (
            float(rect[0]) < float(coordinate_rect.x0) - bounds_tolerance
            or float(rect[1]) < float(coordinate_rect.y0) - bounds_tolerance
            or float(rect[2]) > float(coordinate_rect.x1) + bounds_tolerance
            or float(rect[3]) > float(coordinate_rect.y1) + bounds_tolerance
        ):
            out_of_bounds.append(
                {
                    "text": span["text"][:120],
                    "bbox": [round(float(value), 2) for value in rect],
                }
            )

    target_chars = count_target_characters(text, profile["writing_system"])
    blank_ratio = _column_blank_ratio(page, body_spans)
    top_blank_ratio = _top_blank_ratio(page, body_spans)
    compressed = (
        (
            body_mode is not None
            and body_mode < float(
                quality.get(
                    "body_font_preferred_pt",
                    quality["body_font_target_pt"][0],
                )
            )
            - 0.3
        )
        or (
            median_leading is not None
            and median_leading < float(
                quality.get(
                    "leading_preferred",
                    quality["leading_target"][0],
                )
            )
        )
    )
    sparse_unjustified = (
        target_chars >= 120
        and blank_ratio >= 0.25
        and not sparse_layout_justified(overrides, page_number)
    )
    source_residuals = []
    if profile["residual_source_scan"] == "latin-prose":
        source_residuals = residual_source_prose(
            spans,
            page_number,
            retained,
            allowed_patterns,
            allowed_retained_corpus,
        )
    structured_table = _structured_table_page(
        page_number,
        overrides.get("page_overrides", []),
        non_body_regions,
    )

    return {
        "page": page_number,
        "width": round(float(page.rect.width), 3),
        "height": round(float(page.rect.height), 3),
        "text_chars": len(text),
        "target_chars": target_chars,
        "images": meaningful_page_image_count(page),
        "drawings": len(page.get_drawings()),
        "body_detection": body_detection,
        "body_font_mode_pt": body_mode,
        "body_font_size_weights": {
            str(size): weight
            for size, weight in sorted(body_font_size_weights.items())
        },
        "low_body_spans": low_body_spans,
        "table_font_min_pt": table_font_min_pt,
        "low_table_spans": low_table_spans,
        "median_leading_ratio": median_leading,
        "leading_sample_count": len(leading),
        "median_body_line_width_ratio": median_body_line_width,
        "body_line_width_sample_count": body_line_width_sample_count,
        "orphan_single_han_lines": orphan_single_han_lines,
        "interline_gap_outliers": interline_gap_outliers,
        "largest_column_bottom_blank_ratio": blank_ratio,
        "top_blank_ratio": top_blank_ratio,
        "vertical_blank_imbalance_ratio": round(
            blank_ratio - top_blank_ratio, 3
        ),
        "compressed_despite_blank_space": compressed and blank_ratio >= 0.18,
        "sparse_layout_unjustified": sparse_unjustified,
        "out_of_bounds_spans": out_of_bounds,
        "replacement_chars": text.count("\ufffd"),
        "compatibility_ideographs": COMPATIBILITY_IDEOGRAPH_PATTERN.findall(text),
        "placeholder_hits": PLACEHOLDER_PATTERN.findall(text),
        "source_residuals": source_residuals,
        "text_block_overlaps": (
            [] if structured_table else text_block_overlaps(text_dict)
        ),
        "text_span_overlaps": text_span_overlaps(spans),
        "structured_table_visual_check": structured_table,
        "whole_page_reference_exception": _whole_page_reference(
            page, retained_regions
        ),
        "reference_region_area_ratio": round(
            _reference_area_ratio(page, retained_regions),
            3,
        ),
        "null_characters": text.count("\x00"),
    }
