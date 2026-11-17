from __future__ import annotations

import sys
from pathlib import Path as _Path

# 按 README 的写法 `python3 scripts/qa_pdf.py` 运行时 sys.path 里没有仓库根。
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
import re  # noqa: E402
import statistics  # noqa: E402
from collections import Counter, defaultdict  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Any  # noqa: E402

from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    allowed_latin_corpus as _allowed_latin_corpus,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    complex_localized_source_labels as _complex_localized_source_labels,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    expected_literal_placeholder_tokens as _expected_literal_placeholder_tokens,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    font_embedding_issues as _font_embedding_issues,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    font_name_token as _font_name_token,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    inventory_accounts_for_missing_image as _inventory_accounts_for_missing_image,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    looks_like_proper_name as _looks_like_proper_name,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    mapped_entry_has_visible_retained_content as _mapped_entry_has_visible_retained_content,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    meaningful_image_bbox as _meaningful_image_bbox,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    meaningful_page_image_count as _meaningful_page_image_count,
)

# 内容判据已移入 academic_pdf_translation.qa.content_rules：占位符、
# 拉丁语料、原文残留、图像与字体嵌入。这里按旧名再导出，调用路径不变。
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    placeholder_token as _placeholder_token,
)
from academic_pdf_translation.qa.content_rules import (  # noqa: E402,F401
    unit_is_substantive_body_prose as _unit_is_substantive_body_prose,
)
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    all_complex_candidate_pages as _all_complex_candidate_pages,
)
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    in_any_region as _in_any_region,
)

# 下面三块已经搬进 academic_pdf_translation.qa，这里按原名再导入。
# self_test.py 直接从 qa_pdf 取这些名字，所以即使本文件不再用到某一个，
# 也不能删——F401 的 noqa 就是为这件事写的。
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    page_selector_matches as _page_selector_matches,
)
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    pre_complex_break_pages as _pre_complex_break_pages,
)
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    reference_area_ratio as _reference_area_ratio,
)
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    regions_for_page as _regions_for_page,
)
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    structured_complex_candidate_pages as _structured_complex_candidate_pages,
)
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    structured_table_page as _structured_table_page,
)
from academic_pdf_translation.qa.geometry import (  # noqa: E402,F401
    whole_page_reference as _whole_page_reference,
)

# 版面判据已移入 academic_pdf_translation.qa.layout_rules：它们只吃页面
# 度量与版式声明，不打开 PDF。这里按旧名再导出，调用路径保持不变。
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    body_width_collapsed as _body_width_collapsed,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    bottom_whitespace_is_unbalanced as _bottom_whitespace_is_unbalanced,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    compressed_page_requires_repair as _compressed_page_requires_repair,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    document_typography_locked as _document_typography_locked,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    excessive_unused_space_unjustified as _excessive_unused_space_unjustified,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    horizontal_width_change_justified as _horizontal_width_change_justified,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    paragraph_gap_inflation_justified as _paragraph_gap_inflation_justified,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    sparse_layout_justified as _sparse_layout_justified,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    text_block_overlaps as _text_block_overlaps,
)
from academic_pdf_translation.qa.layout_rules import (  # noqa: E402,F401
    text_span_overlaps as _text_span_overlaps,
)

# 逐页度量已移入 academic_pdf_translation.qa.page_metrics：它只量不判。
# target_character_count 是脚本层的语言配置，按注入传进去。
from academic_pdf_translation.qa.page_metrics import (  # noqa: E402,F401
    page_metrics as _page_metrics_impl,
)
from academic_pdf_translation.qa.page_metrics import (  # noqa: E402,F401
    residual_source_prose as _residual_source_prose,
)
from academic_pdf_translation.qa.text_signals import (  # noqa: E402,F401
    COMPATIBILITY_IDEOGRAPH_PATTERN,
    HAN_CHARACTER_PATTERN,
    LATIN_PROSE_PATTERN,
    ORPHAN_TRAILING_PUNCTUATION,
    PLACEHOLDER_PATTERN,
    REFERENCE_KINDS,
    SOURCE_MAPPING_LABEL_PATTERN,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    body_line_width_ratio as _body_line_width_ratio,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    body_spans as _body_spans,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    column_blank_ratio as _column_blank_ratio,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    interline_gap_outliers as _interline_gap_outliers,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    leading_ratios as _leading_ratios,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    low_table_spans as _low_table_spans,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    orphan_single_han_lines as _orphan_single_han_lines,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    top_blank_ratio as _top_blank_ratio,
)
from academic_pdf_translation.qa.typography import (  # noqa: E402,F401
    weighted_font_mode as _weighted_font_mode,
)


def _page_metrics(*args: Any, **kwargs: Any) -> dict:
    """把脚本层的字符计数注入包内度量函数，调用签名保持不变。"""

    return _page_metrics_impl(
        *args, count_target_characters=target_character_count, **kwargs
    )


import perf_trace  # noqa: E402
from _common import (  # noqa: E402
    SkillError,
    character_counts,
    internal_job_path,
    load_json,
    resolve_language_profile,
    sha256_file,
    target_character_count,
    utc_now,
    write_json,
)
from candidate_analysis import open_candidate_analysis  # noqa: E402
from i18n import all_messages  # noqa: E402


def visible_source_page_marker_pages(document: Any) -> list[int]:
    """候选文字层里出现源页调试标记的页码（任何语言模板都算）。"""

    patterns = [
        re.compile(
            re.escape(template).replace(
                re.escape("{page}"), r"\s*\d+\s*"
            )
        )
        for template in all_messages("source_page")
    ]
    pages: list[int] = []
    for index in range(document.page_count):
        text = document[index].get_text("text")
        if any(pattern.search(text) for pattern in patterns):
            pages.append(index + 1)
    return pages

from candidate_page_map import (  # noqa: E402
    candidate_pages_for_source,
    candidate_pages_for_unit,
    load_candidate_page_map,
    source_pages_for_candidate,
)
from retained_source import extract_retained_regions  # noqa: E402


def _registered_generator_typography(
    job_dir: Path,
    job: dict,
    candidate_path: Path,
    candidate_mapping: dict[str, Any] | None,
) -> dict[str, float] | None:
    files = job.get("files", {})
    provenance_path = internal_job_path(
        job_dir,
        files.get("candidate_provenance", "candidate_provenance.json"),
    )
    layout_log_path = job_dir / "generator-layout-log.json"
    if not provenance_path.is_file() or not layout_log_path.is_file():
        return None
    provenance = load_json(provenance_path)
    layout_log = load_json(layout_log_path)
    candidate_hash = sha256_file(candidate_path)
    if provenance.get("candidate_sha256") != candidate_hash:
        return None
    if (
        isinstance(candidate_mapping, dict)
        and candidate_mapping.get("candidate_sha256") != candidate_hash
    ):
        return None
    if (
        provenance.get("renderer") != layout_log.get("renderer")
        or str(provenance.get("renderer_version") or "")
        != str(layout_log.get("renderer_version") or "")
        or str(provenance.get("renderer_build_id") or "")
        != str(layout_log.get("renderer_build_id") or "")
    ):
        return None
    body_font = layout_log.get("body_font_pt")
    reference_font = layout_log.get("reference_font_pt")
    if not isinstance(body_font, (int, float)) or not 5 <= body_font <= 30:
        return None
    result = {"body_font_pt": float(body_font)}
    if (
        isinstance(reference_font, (int, float))
        and 5 <= reference_font <= 30
    ):
        result["reference_font_pt"] = float(reference_font)
    return result


def _candidate_retained_source(
    retained: dict,
    candidate_mapping: dict[str, Any] | None,
) -> dict:
    if candidate_mapping is None:
        return retained
    candidate_regions: list[dict] = []
    for entry in candidate_mapping.get("retained_regions", []):
        if not isinstance(entry, dict):
            continue
        for region in entry.get("candidate_regions", []):
            if not isinstance(region, dict):
                continue
            candidate_page = region.get("candidate_page")
            bbox = region.get("bbox")
            if (
                not isinstance(candidate_page, int)
                or not isinstance(bbox, list)
                or len(bbox) != 4
            ):
                continue
            candidate_regions.append(
                {
                    "page": candidate_page,
                    "bbox": bbox,
                    "category": entry.get("category"),
                    "retained_region_id": entry.get("retained_region_id"),
                    "reason": "由候选页映射生成的保留原文区域。",
                }
            )
    candidate_items: list[dict] = []
    for item in retained.get("items", []):
        if not isinstance(item, dict):
            continue
        source_page = item.get("page")
        if not isinstance(source_page, int):
            candidate_items.append(dict(item))
            continue
        for candidate_page in candidate_pages_for_source(
            candidate_mapping,
            source_page,
        ):
            candidate_items.append({**item, "page": candidate_page})
    return {
        "schema_version": retained.get("schema_version", "1.0"),
        "items": candidate_items,
        "regions": candidate_regions,
    }


















def _allowed_patterns(retained: dict) -> list[tuple[int | None, re.Pattern[str]]]:
    patterns: list[tuple[int | None, re.Pattern[str]]] = []
    for item in retained.get("items", []):
        value = item.get("pattern") or item.get("text")
        if not value:
            continue
        try:
            patterns.append(
                (
                    int(item["page"]) if item.get("page") is not None else None,
                    re.compile(value if item.get("is_regex") else re.escape(value)),
                )
            )
        except re.error as exc:
            raise SkillError(f"retained_source.json 中正则无效: {value}: {exc}") from exc
    return patterns




















def _timed_run_qa(job_dir: Path) -> dict:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    files = job["files"]
    source_path = internal_job_path(job_dir, job["source"]["job_path"])
    candidate_path = internal_job_path(job_dir, files["candidate"])
    if not source_path.is_file():
        raise SkillError(f"缺少原文: {source_path}")
    if not candidate_path.is_file():
        raise SkillError(f"缺少候选 PDF: {candidate_path}")

    _, profile = resolve_language_profile(job["translation"]["target_language"])
    quality = job["quality"]
    overrides = load_json(internal_job_path(job_dir, files["layout_overrides"]))
    retained = load_json(internal_job_path(job_dir, files["retained_source"]))
    figure_inventory = load_json(
        internal_job_path(job_dir, files["figure_inventory"])
    )
    translation = load_json(
        internal_job_path(job_dir, files["translation"])
    )
    complex_path = internal_job_path(
        job_dir,
        files.get("complex_content_payload", "complex_content.json"),
    )
    complex_content = (
        load_json(complex_path)
        if complex_path.is_file()
        else {"items": []}
    )
    source_analysis = open_candidate_analysis(source_path, role="source")
    candidate_analysis_handle = open_candidate_analysis(
        candidate_path,
        role="candidate",
    )
    source = source_analysis.document
    candidate = candidate_analysis_handle.document
    candidate_mapping = (
        load_candidate_page_map(
            job_dir,
            job,
            required=("candidate_page_map" in files),
            candidate_path=candidate_path,
            translation=translation,
        )
        if (
            "candidate_page_map" in files
            or (job_dir / "candidate-page-map.json").is_file()
        )
        else None
    )
    generator_typography = _registered_generator_typography(
        job_dir,
        job,
        candidate_path,
        candidate_mapping,
    )
    structured_candidate_pages = _structured_complex_candidate_pages(
        complex_content,
        candidate_mapping,
    )
    pre_complex_break_pages = _pre_complex_break_pages(
        candidate_mapping,
        _all_complex_candidate_pages(
            complex_content,
            candidate_mapping,
        ),
    )
    candidate_retained = _candidate_retained_source(
        retained,
        candidate_mapping,
    )
    allowed_patterns = _allowed_patterns(candidate_retained)
    allowed_corpus_by_candidate: dict[int, str] = defaultdict(str)
    retained_payloads = extract_retained_regions(
        source,
        retained,
        translation,
    )
    retained_payload_by_id = {
        str(payload["id"]): payload
        for payload in retained_payloads
        if isinstance(payload, dict) and str(payload.get("id") or "")
    }
    if candidate_mapping is not None:
        for entry in candidate_mapping.get("retained_regions", []):
            if not isinstance(entry, dict):
                continue
            payload = retained_payload_by_id.get(
                str(entry.get("retained_region_id") or "")
            )
            if not payload:
                continue
            retained_key = _allowed_latin_corpus(
                str(payload.get("text") or "")
            )
            mapped_pages = {
                page
                for page in entry.get("candidate_pages", [])
                if isinstance(page, int)
            }
            if isinstance(payload.get("page"), int):
                mapped_pages.update(
                    candidate_pages_for_source(
                        candidate_mapping,
                        int(payload["page"]),
                    )
                )
            for candidate_page in mapped_pages:
                allowed_corpus_by_candidate[candidate_page] += (
                    retained_key + "\n"
                )
        complex_by_id = {
            str(item.get("id") or ""): item
            for item in complex_content.get("items", [])
            if isinstance(item, dict) and str(item.get("id") or "")
        }
        for entry in candidate_mapping.get("complex_items", []):
            if not isinstance(entry, dict):
                continue
            item = complex_by_id.get(
                str(entry.get("complex_item_id") or "")
            )
            if not item:
                continue
            source_labels = _complex_localized_source_labels(item)
            if not source_labels:
                continue
            localized_key = _allowed_latin_corpus(
                "\n".join(source_labels)
            )
            for candidate_page in entry.get("candidate_pages", []):
                if isinstance(candidate_page, int):
                    allowed_corpus_by_candidate[candidate_page] += (
                        localized_key + "\n"
                    )
    for unit in translation.get("units", []):
        if not isinstance(unit, dict) or not isinstance(unit.get("page"), int):
            continue
        text = str(unit.get("translation") or unit.get("source") or "")
        mapped_candidate_pages = candidate_pages_for_unit(
            candidate_mapping,
            str(unit.get("id") or ""),
            int(unit["page"]),
        )
        if (
            profile["writing_system"] != "latin"
            and target_character_count(text, profile["writing_system"]) >= 12
        ):
            translated_key = _allowed_latin_corpus(text)
            for candidate_page in mapped_candidate_pages:
                allowed_corpus_by_candidate[candidate_page] += (
                    translated_key + "\n"
                )
        kind = str(unit.get("kind") or "").lower()
        markers = (
            "参考文献题录（保留原文）",
            "参考文献（题录保留原文）",
            "參考文獻（題錄保留原文）",
        )
        marker = next((value for value in markers if value in text), None)
        if marker:
            retained_text = text.split(marker, 1)[1]
        elif unit.get("keep_source_reason") or kind in REFERENCE_KINDS:
            retained_text = text
        else:
            continue
        retained_key = _allowed_latin_corpus(retained_text)
        for candidate_page in mapped_candidate_pages:
            allowed_corpus_by_candidate[candidate_page] += (
                retained_key + "\n"
            )

    source_pages = []
    for index, page in enumerate(source, 1):
        text_dict = page.get_text("dict")
        spans = [
            span
            for block in text_dict["blocks"]
            if block.get("type") == 0
            for line in block.get("lines", [])
            for span in line.get("spans", [])
            if span.get("text", "").strip()
        ]
        retained_regions = _regions_for_page(
            retained.get("regions", []), index
        )
        body_spans, _ = _body_spans(
            page,
            index,
            spans,
            {
                "body_regions": [],
                "non_body_regions": overrides.get("non_body_regions", []),
            },
            retained_regions,
        )
        median_body_line_width, body_line_width_sample_count = (
            _body_line_width_ratio(page, text_dict, body_spans)
        )
        source_pages.append(
            {
                "page": index,
                "width": round(float(page.rect.width), 3),
                "height": round(float(page.rect.height), 3),
                "images": _meaningful_page_image_count(page),
                "median_body_line_width_ratio": median_body_line_width,
                "body_line_width_sample_count": body_line_width_sample_count,
                "largest_column_bottom_blank_ratio": _column_blank_ratio(
                    page, body_spans
                ),
            }
        )
    candidate_overrides = overrides
    if candidate_mapping is not None:
        remapped_page_overrides = []
        remapped_non_body_regions = []
        for item in overrides.get("page_overrides", []):
            if not isinstance(item, dict):
                continue
            source_numbers = []
            if isinstance(item.get("page"), int):
                source_numbers.append(int(item["page"]))
            if isinstance(item.get("pages"), list):
                source_numbers.extend(
                    int(page)
                    for page in item["pages"]
                    if isinstance(page, int)
                )
            candidate_numbers = sorted(
                {
                    candidate_page
                    for source_page in source_numbers
                    for candidate_page in candidate_pages_for_source(
                        candidate_mapping,
                        source_page,
                    )
                }
            )
            if not candidate_numbers:
                continue
            remapped = {
                key: value
                for key, value in item.items()
                if key not in {"page", "pages"}
            }
            remapped["pages"] = candidate_numbers
            remapped_page_overrides.append(remapped)
        for candidate_page in sorted(structured_candidate_pages):
            remapped_page_overrides.append(
                {
                    "page": candidate_page,
                    "layout": "structured-table",
                    "structured_table": True,
                    "reason": "就绪的复杂页载荷以结构化表格方式进入候选。",
                }
            )
            page_rect = candidate[candidate_page - 1].rect
            remapped_non_body_regions.append(
                {
                    "page": candidate_page,
                    "bbox": [
                        float(page_rect.x0),
                        float(page_rect.y0),
                        float(page_rect.x1),
                        float(page_rect.y1),
                    ],
                    "category": "structured-table",
                }
            )
        candidate_overrides = {
            **overrides,
            "body_regions": [],
            "non_body_regions": remapped_non_body_regions,
            "page_overrides": remapped_page_overrides,
        }
    candidate_pages = [
        _page_metrics(
            page,
            index,
            profile,
            quality,
            candidate_overrides,
            candidate_retained,
            allowed_patterns,
            allowed_corpus_by_candidate.get(index, ""),
        )
        for index, page in enumerate(candidate, 1)
    ]
    if candidate_pages:
        candidate_pages[-1]["is_final_candidate_page"] = True
    candidate_text = "\n".join(page.get_text("text") for page in candidate)
    expected_literal_placeholder_tokens = (
        _expected_literal_placeholder_tokens(translation)
    )
    unit_by_id = {
        str(unit.get("id") or ""): unit
        for unit in translation.get("units", [])
        if isinstance(unit, dict)
    }

    hard_failures: list[dict] = []
    review_flags: list[dict] = []

    # 参考文献不许整页排成粗体：某页字符量的六成以上来自名字带
    # Bold/Black/Heavy 的字体，就是题录体选错了（例如 Arial Black）。
    bold_dominated_pages: list[int] = []
    bold_name_re = re.compile(r"black|heavy|bold", re.IGNORECASE)
    for index in range(candidate.page_count):
        by_weight = {"bold": 0, "other": 0}
        for block in candidate[index].get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    chars = len(str(span.get("text") or "").strip())
                    if not chars:
                        continue
                    if bold_name_re.search(str(span.get("font") or "")):
                        by_weight["bold"] += chars
                    else:
                        by_weight["other"] += chars
        total = by_weight["bold"] + by_weight["other"]
        if total >= 200 and by_weight["bold"] / total > 0.6:
            bold_dominated_pages.append(index + 1)
    if bold_dominated_pages:
        hard_failures.append(
            {
                "code": "REFERENCE_FONT_TOO_BOLD",
                "pages": bold_dominated_pages,
                "message": (
                    "整页文字六成以上来自粗体家族字体，"
                    "题录体或正文字体选错了字重"
                ),
            }
        )

    # 正式 PDF 的文字层里不许出现"原文第 X 页"这类调试标记——
    # 任何语言版本的模板命中都算，映射锚点应当是不可见的。
    marker_pages = visible_source_page_marker_pages(candidate)
    if marker_pages:
        hard_failures.append(
            {
                "code": "VISIBLE_SOURCE_PAGE_MARKER",
                "pages": marker_pages,
                "message": "正文文字层出现源页调试标记，禁止交付",
            }
        )

    if pre_complex_break_pages:
        review_flags.append(
            {
                "code": "NATURAL_BREAK_BEFORE_COMPLEX_CONTENT",
                "pages": sorted(pre_complex_break_pages),
                "message": (
                    "下一候选页承载同一或紧邻原文页的大型结构化内容，"
                    "本页页底留白按自然分页处理并保留目视复核。"
                ),
            }
        )
    if candidate_mapping is None and source.page_count != candidate.page_count:
        hard_failures.append(
            {
                "code": "PAGE_COUNT_MISMATCH",
                "source": source.page_count,
                "candidate": candidate.page_count,
            }
        )
    elif candidate_mapping is not None and source.page_count != candidate.page_count:
        review_flags.append(
            {
                "code": "PAGINATION_REFLOWED_WITH_SOURCE_MAP",
                "source_pages": source.page_count,
                "candidate_pages": candidate.page_count,
                "message": "正文按连续阅读重新分页，逐页核对使用候选页映射。",
            }
        )
    size_mismatches = []
    for candidate_page in candidate_pages:
        mapped_source_numbers = source_pages_for_candidate(
            candidate_mapping,
            int(candidate_page["page"]),
        )
        mapped_source_metrics = [
            source_pages[source_page - 1]
            for source_page in mapped_source_numbers
            if 1 <= source_page <= len(source_pages)
        ]
        if not mapped_source_metrics:
            continue
        source_blank_values = [
            float(item["largest_column_bottom_blank_ratio"])
            for item in mapped_source_metrics
        ]
        source_blank = statistics.median(source_blank_values)
        candidate_page["mapped_source_pages"] = mapped_source_numbers
        mapped_complex_ids = []
        mapped_unit_ids: list[str] = []
        mapped_entry: dict[str, Any] = {}
        if candidate_mapping is not None:
            mapped_entry = next(
                (
                    entry
                    for entry in candidate_mapping.get(
                        "candidate_pages",
                        [],
                    )
                    if isinstance(entry, dict)
                    and entry.get("candidate_page")
                    == candidate_page["page"]
                ),
                {},
            )
            mapped_complex_ids = [
                str(value)
                for value in mapped_entry.get("complex_item_ids", [])
            ]
            mapped_unit_ids = [
                str(value)
                for value in mapped_entry.get("unit_ids", [])
            ]
        candidate_page["mapped_complex_item_ids"] = mapped_complex_ids
        candidate_page["mapped_has_retained_regions"] = (
            _mapped_entry_has_visible_retained_content(mapped_entry)
        )
        candidate_page["mapped_has_body_prose"] = (
            any(
                (
                    _unit_is_substantive_body_prose(
                        unit_by_id.get(unit_id)
                    )
                    and str(
                        mapped_entry.get(
                            "unit_layout_roles",
                            {},
                        ).get(unit_id)
                        or ""
                    ).lower()
                    not in {
                        "publication-metadata",
                        "formal-citation-footer",
                        "footnote",
                    }
                )
                for unit_id in mapped_unit_ids
            )
            if candidate_mapping is not None
            else True
        )
        candidate_page["complex_visual_page"] = bool(mapped_complex_ids)
        candidate_page["source_bottom_blank_ratio"] = round(source_blank, 3)
        candidate_page["excess_bottom_blank_ratio"] = round(
            max(
                0.0,
                candidate_page["largest_column_bottom_blank_ratio"]
                - source_blank,
            ),
            3,
        )
        source_width_values = [
            float(item["median_body_line_width_ratio"])
            for item in mapped_source_metrics
            if item["median_body_line_width_ratio"] is not None
        ]
        source_width_ratio = (
            statistics.median(source_width_values)
            if source_width_values
            else None
        )
        candidate_width_ratio = candidate_page[
            "median_body_line_width_ratio"
        ]
        candidate_page["source_body_line_width_ratio"] = source_width_ratio
        candidate_page["body_width_retention_ratio"] = (
            round(candidate_width_ratio / source_width_ratio, 3)
            if source_width_ratio
            and candidate_width_ratio is not None
            else None
        )
        candidate_page["body_width_loss_ratio"] = (
            round(max(0.0, source_width_ratio - candidate_width_ratio), 3)
            if source_width_ratio is not None
            and candidate_width_ratio is not None
            else None
        )
        if candidate_mapping is None and not any(
            abs(source_page["width"] - candidate_page["width"]) <= 0.1
            and abs(source_page["height"] - candidate_page["height"]) <= 0.1
            for source_page in mapped_source_metrics
        ):
            size_mismatches.append(candidate_page["page"])
    if size_mismatches:
        hard_failures.append(
            {"code": "PAGE_SIZE_MISMATCH", "pages": size_mismatches}
        )

    empty_pages = [
        page["page"]
        for page in candidate_pages
        if page["text_chars"] == 0 and page["images"] == 0
    ]
    if empty_pages:
        hard_failures.append({"code": "BLANK_PAGES", "pages": empty_pages})

    target_text_missing = [
        page["page"]
        for page in candidate_pages
        if not page["whole_page_reference_exception"]
        and page["target_chars"]
        < int(profile["minimum_target_chars_per_nonreference_page"])
    ]
    if target_text_missing:
        hard_failures.append(
            {"code": "TARGET_TEXT_MISSING", "pages": target_text_missing}
        )

    font_floor_pages = [
        page["page"]
        for page in candidate_pages
        if not page["whole_page_reference_exception"]
        and not page.get("complex_visual_page")
        and (
            (
                page["body_font_mode_pt"] is not None
                and page["body_font_mode_pt"] < float(quality["body_font_min_pt"])
            )
            or page["low_body_spans"]
        )
    ]
    if font_floor_pages:
        hard_failures.append(
            {"code": "BODY_FONT_BELOW_MINIMUM", "pages": font_floor_pages}
        )

    low_table_pages = []
    for page in candidate_pages:
        hits = page["low_table_spans"]
        low_character_count = sum(len(hit["text"]) for hit in hits)
        if hits and (
            low_character_count >= 24
            or any(len(hit["text"]) >= 12 for hit in hits)
        ):
            low_table_pages.append(
                {
                    "page": page["page"],
                    "minimum_font_pt": page["table_font_min_pt"],
                    "low_character_count": low_character_count,
                    "samples": hits[:12],
                }
            )
    if low_table_pages:
        hard_failures.append(
            {
                "code": "TABLE_FONT_BELOW_MINIMUM",
                "pages": low_table_pages,
                "message": (
                    "结构化表格使用独立字号层级，但仍须原尺寸可读；"
                    "不得把表格标成非正文后用极小字号绕过正文门槛。"
                ),
            }
        )

    leading_exception_pages = {
        int(item["page"])
        for item in overrides.get("leading_exceptions", [])
        if item.get("page") is not None and item.get("reason")
    }
    leading_fail_pages = []
    undocumented_tight_pages = []
    missing_leading_samples = []
    for page in candidate_pages:
        ratio = page["median_leading_ratio"]
        if ratio is None:
            if (
                page["text_chars"] >= 300
                and not page["whole_page_reference_exception"]
                and not page["structured_table_visual_check"]
            ):
                missing_leading_samples.append(page["page"])
            continue
        if (
            ratio < float(quality["leading_exception_min"])
            and not page["whole_page_reference_exception"]
            and not page["structured_table_visual_check"]
            and not page.get("complex_visual_page")
        ):
            leading_fail_pages.append(page["page"])
        elif (
            ratio < float(quality["leading_target"][0])
            and page["page"] not in leading_exception_pages
            and not page["whole_page_reference_exception"]
            and not page["structured_table_visual_check"]
            and not page.get("complex_visual_page")
        ):
            undocumented_tight_pages.append(page["page"])
    if leading_fail_pages:
        hard_failures.append(
            {"code": "LEADING_BELOW_HARD_MINIMUM", "pages": leading_fail_pages}
        )
    if undocumented_tight_pages:
        hard_failures.append(
            {
                "code": "LEADING_EXCEPTION_NOT_DOCUMENTED",
                "pages": undocumented_tight_pages,
            }
        )
    if missing_leading_samples:
        review_flags.append(
            {
                "code": "LEADING_REQUIRES_VISUAL_CHECK",
                "pages": missing_leading_samples,
            }
        )

    ordinary_body_pages = [
        page
        for page in candidate_pages
        if (
            page["body_font_mode_pt"] is not None
            and page["target_chars"] >= 120
            and page.get("mapped_has_body_prose", True)
            and not page["whole_page_reference_exception"]
            and not page["structured_table_visual_check"]
            and not page.get("complex_visual_page")
        )
    ]
    if ordinary_body_pages:
        if generator_typography is not None:
            document_body_mode = generator_typography["body_font_pt"]
            reference_font_mode = generator_typography.get(
                "reference_font_pt"
            )
            mode_source = "registered-generator"
        else:
            document_weights: Counter[float] = Counter()
            for page in ordinary_body_pages:
                for size, weight in page[
                    "body_font_size_weights"
                ].items():
                    document_weights[float(size)] += int(weight)
            document_body_mode = float(
                document_weights.most_common(1)[0][0]
            )
            reference_font_mode = None
            mode_source = "document-character-mode"

        inconsistent_body_fonts = []
        for page in ordinary_body_pages:
            weights = {
                float(size): int(weight)
                for size, weight in page[
                    "body_font_size_weights"
                ].items()
            }
            evaluated_weights = weights
            if (
                reference_font_mode is not None
                and abs(reference_font_mode - document_body_mode) > 0.25
            ):
                without_reference = {
                    size: weight
                    for size, weight in weights.items()
                    if abs(size - reference_font_mode) > 0.25
                }
                if without_reference:
                    evaluated_weights = without_reference
            expected_weight = sum(
                weight
                for size, weight in evaluated_weights.items()
                if abs(size - document_body_mode) <= 0.25
            )
            required_weight = max(
                24,
                int(sum(evaluated_weights.values()) * 0.20),
            )
            if expected_weight >= required_weight:
                continue
            inconsistent_body_fonts.append(
                {
                    "page": page["page"],
                    "body_font_mode_pt": page["body_font_mode_pt"],
                    "document_body_mode_pt": round(
                        document_body_mode,
                        2,
                    ),
                    "document_mode_character_weight": expected_weight,
                    "minimum_character_weight": required_weight,
                    "mode_source": mode_source,
                }
            )
        if inconsistent_body_fonts:
            hard_failures.append(
                {
                    "code": "BODY_FONT_INCONSISTENT_ACROSS_DOCUMENT",
                    "pages": inconsistent_body_fonts,
                    "message": (
                        "普通正文应先按全篇最密页计算统一字号，再冻结到全篇；"
                        "不得逐页缩放正文。"
                    ),
                }
            )

    inflated_paragraph_gaps = []
    for page in candidate_pages:
        gaps = page["interline_gap_outliers"]
        if (
            not gaps
            or page["whole_page_reference_exception"]
            or page["structured_table_visual_check"]
            or page.get("complex_visual_page")
            or _paragraph_gap_inflation_justified(overrides, page["page"])
        ):
            continue
        if (
            len(gaps) >= 2
            or max(gap["gap_to_font_ratio"] for gap in gaps) >= 8.0
        ):
            inflated_paragraph_gaps.append(
                {
                    "page": page["page"],
                    "gaps": gaps[:8],
                }
            )
    if inflated_paragraph_gaps:
        hard_failures.append(
            {
                "code": "PARAGRAPH_GAP_INFLATION",
                "pages": inflated_paragraph_gaps,
                "message": (
                    "检测到以超大段间距追赶页面高度。应保持自然段落流，"
                    "优先按全篇统一字号放大正文；不得用机械分块和极端段距填页。"
                ),
            }
        )

    compressed_pages = [
        page["page"]
        for page in candidate_pages
        if _compressed_page_requires_repair(page)
    ]
    if compressed_pages:
        hard_failures.append(
            {"code": "COMPRESSED_WITH_UNUSED_SPACE", "pages": compressed_pages}
        )
    sparse_pages = [
        {
            "page": page["page"],
            "largest_column_bottom_blank_ratio": page[
                "largest_column_bottom_blank_ratio"
            ],
            "top_blank_ratio": page["top_blank_ratio"],
            "vertical_blank_imbalance_ratio": page[
                "vertical_blank_imbalance_ratio"
            ],
        }
        for page in candidate_pages
        if (
            page["sparse_layout_unjustified"]
            and not page.get("mapped_has_retained_regions", False)
            and page["page"] not in pre_complex_break_pages
        )
    ]
    if sparse_pages:
        review_flags.append(
            {
                "code": "SPARSE_PAGE_REQUIRES_JUSTIFICATION",
                "pages": sparse_pages,
                "message": (
                    "页面仍有较大可用空间。优先增加字号、行距、题项间距或"
                    "重平衡版心；确需保留时在 page_overrides 中记录理由。"
                ),
            }
        )
    excessive_unused_space = [
        {
            "page": page["page"],
            "source_bottom_blank_ratio": page["source_bottom_blank_ratio"],
            "candidate_bottom_blank_ratio": page[
                "largest_column_bottom_blank_ratio"
            ],
            "excess_bottom_blank_ratio": page[
                "excess_bottom_blank_ratio"
            ],
        }
        for page in candidate_pages
        if _excessive_unused_space_unjustified(
            page,
            overrides,
            pre_complex_break_pages,
        )
    ]
    if excessive_unused_space:
        if _document_typography_locked(overrides):
            review_flags.append(
                {
                    "code": "NATURAL_SHORT_PAGE_AFTER_DOCUMENT_TYPOGRAPHY",
                    "pages": excessive_unused_space,
                    "message": (
                        "全篇普通正文已按最密页试排锁定统一字号与行距，且段距膨胀、"
                        "正文缩字和版心坍缩均由其他门禁独立检查。剩余短页留白必须"
                        "逐页原尺寸人工复核，不能由自动QA直接判定PASS。"
                    ),
                }
            )
        else:
            hard_failures.append(
                {
                    "code": "EXCESSIVE_UNUSED_SPACE_VS_SOURCE",
                    "pages": excessive_unused_space,
                }
            )

    width_retention_min = float(
        quality.get("body_width_retention_min", 0.72)
    )
    width_loss_trigger = float(
        quality.get("body_width_loss_trigger", 0.12)
    )
    collapsed_body_width_pages = [
        {
            "page": page["page"],
            "source_body_line_width_ratio": page[
                "source_body_line_width_ratio"
            ],
            "candidate_body_line_width_ratio": page[
                "median_body_line_width_ratio"
            ],
            "body_width_retention_ratio": page[
                "body_width_retention_ratio"
            ],
            "body_width_loss_ratio": page["body_width_loss_ratio"],
        }
        for page in candidate_pages
        if (
            page["target_chars"] >= 120
            and page.get("mapped_has_body_prose", True)
            and not page["whole_page_reference_exception"]
            and not page["structured_table_visual_check"]
            and not page.get("complex_visual_page")
            and _body_width_collapsed(
                page["source_body_line_width_ratio"],
                page["median_body_line_width_ratio"],
                width_retention_min,
                width_loss_trigger,
            )
            and not _horizontal_width_change_justified(
                overrides, page["page"]
            )
        )
    ]
    if collapsed_body_width_pages:
        hard_failures.append(
            {
                "code": "BODY_WIDTH_COLLAPSE_VS_SOURCE",
                "pages": collapsed_body_width_pages,
                "message": (
                    "普通正文的横向版心相对原文被显著压窄。"
                    "应优先保持原文正文宽度，并通过自然段流排、字号、"
                    "行距和段距处理纵向空间；只有任务明确批准新版式时，"
                    "才可记录 horizontal_width_change_justified。"
                ),
            }
        )
    complex_visual_pages = [
        page["page"]
        for page in candidate_pages
        if page.get("complex_visual_page")
    ]
    if complex_visual_pages:
        review_flags.append(
            {
                "code": "COMPLEX_VISUAL_LAYOUT_REQUIRES_VISUAL_CHECK",
                "pages": complex_visual_pages,
                "message": (
                    "图片、图表或矢量模型页不使用普通正文段距和行宽门槛，"
                    "必须按原尺寸核对结构与可读性。"
                ),
            }
        )

    orphan_han_pages = [
        {
            "page": page["page"],
            "hits": page["orphan_single_han_lines"],
        }
        for page in candidate_pages
        if (
            page["orphan_single_han_lines"]
            and not page["whole_page_reference_exception"]
            and not page["structured_table_visual_check"]
        )
    ]
    if orphan_han_pages:
        hard_failures.append(
            {
                "code": "ORPHAN_SINGLE_HAN_LINE",
                "pages": orphan_han_pages,
                "message": (
                    "检测到紧跟长行的单个汉字续行。"
                    "应通过平衡断行、调整标题字号或改写合法换行修复；"
                    "不得把单字孤行作为正常排版交付。"
                ),
            }
        )

    out_of_bounds_pages = [
        page["page"] for page in candidate_pages if page["out_of_bounds_spans"]
    ]
    if out_of_bounds_pages:
        hard_failures.append(
            {"code": "TEXT_OUT_OF_BOUNDS", "pages": out_of_bounds_pages}
        )
    overlap_pages = [
        page["page"]
        for page in candidate_pages
        if page["text_block_overlaps"] or page["text_span_overlaps"]
    ]
    if overlap_pages:
        hard_failures.append(
            {"code": "TEXT_BLOCK_OVERLAP", "pages": overlap_pages}
        )
    structured_table_pages = [
        page["page"]
        for page in candidate_pages
        if page["structured_table_visual_check"]
    ]
    if structured_table_pages:
        review_flags.append(
            {
                "code": "STRUCTURED_TABLE_REQUIRES_VISUAL_CHECK",
                "pages": structured_table_pages,
                "message": (
                    "结构化表页已跳过易误报的整块文本框相交检查；"
                    "仍执行字符 span 重叠检查，并必须逐页原尺寸目视复核。"
                ),
            }
        )

    replacement_count = sum(page["replacement_chars"] for page in candidate_pages)
    if replacement_count:
        hard_failures.append(
            {"code": "REPLACEMENT_CHARACTERS", "count": replacement_count}
        )
    null_character_count = sum(
        page["null_characters"] for page in candidate_pages
    )
    if null_character_count:
        hard_failures.append(
            {"code": "NULL_CHARACTERS", "count": null_character_count}
        )
    compatibility_count = sum(
        len(page["compatibility_ideographs"]) for page in candidate_pages
    )
    if profile["disallow_compatibility_ideographs"] and compatibility_count:
        hard_failures.append(
            {"code": "COMPATIBILITY_IDEOGRAPHS", "count": compatibility_count}
        )
    placeholder_hits = [
        hit
        for page in candidate_pages
        for hit in page["placeholder_hits"]
        if (
            not hit.startswith("{{")
            or _placeholder_token(hit)
            not in expected_literal_placeholder_tokens
        )
    ]
    if placeholder_hits:
        hard_failures.append(
            {"code": "PLACEHOLDER_TEXT", "samples": placeholder_hits[:20]}
        )
    source_residuals = [
        hit for page in candidate_pages for hit in page["source_residuals"]
    ]
    if source_residuals:
        hard_failures.append(
            {
                "code": "UNACCOUNTED_SOURCE_PROSE",
                "count": len(source_residuals),
                "samples": source_residuals[:30],
            }
        )

    script_counts = character_counts(candidate_text)
    primary_script = profile.get("primary_script")
    primary_count = int(script_counts.get(primary_script, 0))
    primary_minimum = int(
        profile.get("minimum_primary_script_chars_per_document", 1)
    )
    if primary_count < primary_minimum:
        hard_failures.append(
            {
                "code": "TARGET_PRIMARY_SCRIPT_MISSING",
                "target_language": job["translation"]["target_language"],
                "primary_script": primary_script,
                "count": primary_count,
                "minimum": primary_minimum,
            }
        )
    if profile["writing_system"] == "han" and script_counts["han"] >= 100:
        target_markers = set(profile.get("variant_marker_chars", ""))
        opposite_markers = set(profile.get("opposite_variant_marker_chars", ""))
        target_variant_hits = sum(
            1 for character in candidate_text if character in target_markers
        )
        opposite_variant_hits = sum(
            1 for character in candidate_text if character in opposite_markers
        )
        minimum_variant_hits = max(3, round(script_counts["han"] * 0.002))
        if (
            target_variant_hits < minimum_variant_hits
            and opposite_variant_hits > target_variant_hits
        ):
            hard_failures.append(
                {
                    "code": "TARGET_HAN_VARIANT_MISMATCH",
                    "target_language": job["translation"]["target_language"],
                    "target_marker_hits": target_variant_hits,
                    "opposite_marker_hits": opposite_variant_hits,
                    "minimum_target_hits": minimum_variant_hits,
                }
            )

    if profile["writing_system"] == "latin":
        words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", candidate_text.lower())
        markers = set(profile.get("language_marker_words", []))
        marker_hits = sum(1 for word in words if word in markers)
        minimum_hits = max(3, round(len(words) * 0.02))
        exception_reason = quality.get("language_marker_exception_reason")
        if (
            len(words) >= 25
            and marker_hits < minimum_hits
            and not (
                isinstance(exception_reason, str) and exception_reason.strip()
            )
        ):
            hard_failures.append(
                {
                    "code": "TARGET_LANGUAGE_MARKERS_MISSING",
                    "target_language": job["translation"]["target_language"],
                    "word_count": len(words),
                    "marker_hits": marker_hits,
                    "minimum_hits": minimum_hits,
                }
            )

    font_embedding_issues = _font_embedding_issues(candidate)
    if font_embedding_issues:
        hard_failures.append(
            {"code": "FONT_NOT_EMBEDDED", "fonts": font_embedding_issues}
        )

    image_count_risk = []
    for source_page in source_pages:
        mapped_candidate_pages = candidate_pages_for_source(
            candidate_mapping,
            int(source_page["page"]),
        )
        mapped_metrics = [
            candidate_pages[candidate_page - 1]
            for candidate_page in mapped_candidate_pages
            if 1 <= candidate_page <= len(candidate_pages)
        ]
        if (
            source_page["images"] >= 1
            and sum(item["images"] for item in mapped_metrics) == 0
        ):
            image_count_risk.append(source_page["page"])
    image_rebuild_pages: set[int] = set()
    for page_number in range(1, source.page_count + 1):
        for item in overrides.get("page_overrides", []):
            if (
                isinstance(item, dict)
                and _page_selector_matches(item, page_number)
                and (
                    item.get("image_preserved_without_pdf_image") is True
                    or item.get("vector_rebuild") is True
                )
                and isinstance(item.get("reason"), str)
                and item["reason"].strip()
            ):
                image_rebuild_pages.add(page_number)
    for item in figure_inventory.get("items", []):
        if not isinstance(item, dict):
            continue
        if not _inventory_accounts_for_missing_image(item):
            continue
        page = item.get("page")
        if isinstance(page, int):
            image_rebuild_pages.add(page)
        pages = item.get("pages")
        if isinstance(pages, list):
            image_rebuild_pages.update(
                value for value in pages if isinstance(value, int)
            )
    unexplained_image_loss = [
        page for page in image_count_risk if page not in image_rebuild_pages
    ]
    if unexplained_image_loss:
        hard_failures.append(
            {"code": "SOURCE_IMAGE_MISSING", "pages": unexplained_image_loss}
        )
    if any(page["images"] for page in source_pages) or figure_inventory.get(
        "items"
    ):
        review_flags.append(
            {
                "code": "IMAGE_TEXT_REQUIRES_INVENTORY_AND_VISUAL_REVIEW",
                "message": "PDF 文本层无法证明位图内部文字已完成翻译。",
            }
        )

    decision = "BLOCKED" if hard_failures else "READY_FOR_HUMAN_REVIEW"
    report = {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "automatic_decision": decision,
        "source": str(source_path),
        "source_sha256": sha256_file(source_path),
        "candidate": str(candidate_path),
        "candidate_sha256": sha256_file(candidate_path),
        "target_language": job["translation"]["target_language"],
        "quality": quality,
        "generator_typography": generator_typography,
        "hard_failures": hard_failures,
        "review_flags": review_flags,
        "source_pages": source_pages,
        "candidate_pages": candidate_pages,
    }
    output = internal_job_path(job_dir, files["qa"])
    write_json(output, report)
    source_analysis.release()
    candidate_analysis_handle.release()
    return report



def run_qa(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("qa_candidate"):
        return _timed_run_qa(*args, **kwargs)

def main() -> int:
    parser = argparse.ArgumentParser(description="对学术 PDF 译制候选执行确定性 QA")
    parser.add_argument("job_dir", type=Path)
    args = parser.parse_args()
    try:
        report = run_qa(args.job_dir)
        print(f"自动结论: {report['automatic_decision']}")
        print(f"硬失败: {len(report['hard_failures'])}")
        print(f"人工风险: {len(report['review_flags'])}")
        return 0 if report["automatic_decision"] != "BLOCKED" else 2
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
