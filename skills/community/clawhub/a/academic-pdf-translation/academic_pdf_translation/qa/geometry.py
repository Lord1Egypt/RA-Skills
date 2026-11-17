"""QA 的区域几何：页面、区域、覆盖率。

这一族回答的都是同一类问题——**这块东西落在页面的哪里，占多大**。
它们原本挤在 qa_pdf.py 里，和排版度量、文本白名单、字体检查混在一起，
读的人得先分辨这个函数属于哪一层。搬出来之后每个文件只回答一类问题。

函数体与搬出来之前逐字一致，只去掉了私有前缀。
"""

from __future__ import annotations

from typing import Any

from academic_pdf_translation.contracts.models import center_in_bbox


def page_selector_matches(item: dict, page_number: int) -> bool:
    if item.get("page") == page_number:
        return True
    pages = item.get("pages")
    return isinstance(pages, list) and page_number in pages


def regions_for_page(items: list[dict], page_number: int) -> list[dict]:
    return [
        item
        for item in items
        if isinstance(item, dict) and page_selector_matches(item, page_number)
    ]


def region_covers_page(page: Any, region: dict) -> bool:
    bbox = region.get("bbox")
    if not isinstance(bbox, list) or len(bbox) != 4:
        return False
    x0, y0, x1, y1 = map(float, bbox)
    area = max(0.0, x1 - x0) * max(0.0, y1 - y0)
    for page_rect in (page.rect, page.cropbox):
        page_area = max(float(page_rect.width * page_rect.height), 1.0)
        if area / page_area >= 0.8:
            return True
    return False


def structured_table_page(
    page_number: int,
    page_overrides: list[dict],
    non_body_regions: list[dict],
) -> bool:
    if any(
        "table" in str(region.get("category", "")).lower()
        for region in non_body_regions
    ):
        return True
    for item in page_overrides:
        if not isinstance(item, dict) or not page_selector_matches(
            item, page_number
        ):
            continue
        layout = str(item.get("layout", "")).lower()
        if (
            item.get("preserve_column_structure") is True
            or item.get("structured_table") is True
            or "table" in layout
        ):
            return True
    return False


def structured_complex_candidate_pages(
    complex_content: dict,
    candidate_mapping: dict[str, Any] | None,
) -> set[int]:
    if not isinstance(candidate_mapping, dict):
        return set()
    structured_ids = {
        str(item.get("id") or "")
        for item in complex_content.get("items", [])
        if isinstance(item, dict)
        and item.get("status") == "ready"
        and item.get("method")
        in {"structured-table-rebuild", "semantic-grid-rebuild"}
        and str(item.get("id") or "")
    }
    pages: set[int] = set()
    for entry in candidate_mapping.get("complex_items", []):
        if (
            not isinstance(entry, dict)
            or str(entry.get("complex_item_id") or "") not in structured_ids
        ):
            continue
        pages.update(
            int(page)
            for page in entry.get("candidate_pages", [])
            if isinstance(page, int)
        )
    return pages


def all_complex_candidate_pages(
    complex_content: dict[str, Any],
    candidate_mapping: dict[str, Any] | None,
) -> set[int]:
    if not isinstance(candidate_mapping, dict):
        return set()
    ready_ids = {
        str(item.get("id") or "")
        for item in complex_content.get("items", [])
        if isinstance(item, dict)
        and item.get("status") == "ready"
        and str(item.get("id") or "")
    }
    pages: set[int] = set()
    for entry in candidate_mapping.get("complex_items", []):
        if (
            not isinstance(entry, dict)
            or str(entry.get("complex_item_id") or "") not in ready_ids
        ):
            continue
        pages.update(
            int(page)
            for page in entry.get("candidate_pages", [])
            if isinstance(page, int)
        )
    return pages


def pre_complex_break_pages(
    candidate_mapping: dict[str, Any] | None,
    structured_pages: set[int],
) -> set[int]:
    if not isinstance(candidate_mapping, dict):
        return set()
    source_pages_by_candidate = {
        int(entry["candidate_page"]): {
            int(page)
            for page in entry.get("source_pages", [])
            if isinstance(page, int)
        }
        for entry in candidate_mapping.get("candidate_pages", [])
        if isinstance(entry, dict)
        and isinstance(entry.get("candidate_page"), int)
    }
    result: set[int] = set()
    for page in structured_pages:
        if page <= 1:
            continue
        previous_sources = source_pages_by_candidate.get(page - 1, set())
        current_sources = source_pages_by_candidate.get(page, set())
        if previous_sources & current_sources:
            result.add(page - 1)
            continue
        if (
            previous_sources
            and current_sources
            and max(previous_sources) + 1 == min(current_sources)
        ):
            result.add(page - 1)
    return result


def in_any_region(span_bbox: Any, regions: list[dict]) -> bool:
    return any(
        isinstance(region.get("bbox"), list)
        and len(region["bbox"]) == 4
        and center_in_bbox(span_bbox, region["bbox"])
        for region in regions
    )


def region_union_area(regions: list[dict]) -> float:
    rectangles = []
    for region in regions:
        bbox = region.get("bbox")
        if not isinstance(bbox, list) or len(bbox) != 4:
            continue
        x0, y0, x1, y1 = map(float, bbox)
        if x1 > x0 and y1 > y0:
            rectangles.append((x0, y0, x1, y1))
    if not rectangles:
        return 0.0
    x_values = sorted({value for rect in rectangles for value in (rect[0], rect[2])})
    area = 0.0
    # strict=False 与搬出来之前的默认行为一致，只是把它写明。
    for left, right in zip(x_values, x_values[1:], strict=False):
        if right <= left:
            continue
        intervals = sorted(
            (y0, y1)
            for x0, y0, x1, y1 in rectangles
            if x0 < right and x1 > left
        )
        if not intervals:
            continue
        covered = 0.0
        start, end = intervals[0]
        for current_start, current_end in intervals[1:]:
            if current_start <= end:
                end = max(end, current_end)
            else:
                covered += end - start
                start, end = current_start, current_end
        covered += end - start
        area += (right - left) * covered
    return area


def reference_area_ratio(page: Any, regions: list[dict]) -> float:
    reference_regions = [
        region
        for region in regions
        if region.get("category") in {"references", "bibliography"}
    ]
    page_area = max(float(page.rect.width * page.rect.height), 1.0)
    return min(1.0, region_union_area(reference_regions) / page_area)


def whole_page_reference(page: Any, regions: list[dict]) -> bool:
    return reference_area_ratio(page, regions) >= 0.72
