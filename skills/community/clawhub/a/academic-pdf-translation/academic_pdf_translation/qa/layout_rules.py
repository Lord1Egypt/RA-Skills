"""版面判据：这一页的留白、行距、宽度、重叠算不算问题。

从 ``scripts/qa_pdf.py`` 原样搬来，行为不变。它们只吃页面度量与
版式声明，吐布尔值或问题清单，不打开 PDF、不读作业文件——
所以能单独测试，也能被别的检查路径复用。

判据的共同形状是"**有没有正当理由**"：留白大不一定是问题，
版式声明里写明了理由才不是问题。所以函数名都叫 ``..._justified``
而不是 ``..._ok``。
"""

from __future__ import annotations

from academic_pdf_translation.qa.geometry import page_selector_matches


def paragraph_gap_inflation_justified(
    overrides: dict, page_number: int
) -> bool:
    for item in overrides.get("page_overrides", []):
        if not isinstance(item, dict) or not page_selector_matches(
            item, page_number
        ):
            continue
        if (
            item.get("paragraph_gap_inflation_justified") is True
            and isinstance(item.get("reason"), str)
            and item["reason"].strip()
        ):
            return True
    return False

def document_typography_locked(overrides: dict) -> bool:
    typography = overrides.get("document_typography")
    if not isinstance(typography, dict):
        return False
    leading_value = typography.get(
        "leading_ratio",
        typography.get(
            "leading",
            typography.get("body_leading"),
        ),
    )
    natural_spacing = (
        typography.get("paragraph_spacing_policy") == "natural"
        or typography.get("natural_paragraph_spacing") is True
        or isinstance(typography.get("paragraph_space_em"), (int, float))
    )
    return (
        typography.get("selection_method")
        in {"densest-page-fit", "actual-render-page-budget"}
        and (
            typography.get("all_body_pages_locked") is True
            or typography.get("font_locked_across_document") is True
        )
        and isinstance(typography.get("body_font_pt"), (int, float))
        and isinstance(leading_value, (int, float))
        and natural_spacing
        and isinstance(typography.get("reason"), str)
        and typography["reason"].strip()
    )

def sparse_layout_justified(
    overrides: dict, page_number: int
) -> bool:
    for item in overrides.get("page_overrides", []):
        pages = item.get("pages", [])
        applies = item.get("page") == page_number or (
            isinstance(pages, list) and page_number in pages
        )
        if (
            applies
            and item.get("sparse_layout_justified") is True
            and isinstance(item.get("reason"), str)
            and item["reason"].strip()
        ):
            return True
    return False

def horizontal_width_change_justified(
    overrides: dict, page_number: int
) -> bool:
    for item in overrides.get("page_overrides", []):
        if not isinstance(item, dict) or not page_selector_matches(
            item, page_number
        ):
            continue
        if (
            item.get("horizontal_width_change_justified") is True
            and isinstance(item.get("reason"), str)
            and item["reason"].strip()
        ):
            return True
    return False

def body_width_collapsed(
    source_ratio: float | None,
    candidate_ratio: float | None,
    retention_min: float,
    loss_trigger: float,
) -> bool:
    if (
        source_ratio is None
        or candidate_ratio is None
        or source_ratio <= 0
    ):
        return False
    retention = candidate_ratio / source_ratio
    loss = max(0.0, source_ratio - candidate_ratio)
    return retention < retention_min and loss >= loss_trigger

def bottom_whitespace_is_unbalanced(
    excess_bottom_ratio: float,
    bottom_blank_ratio: float,
    top_blank_ratio: float,
    excess_trigger: float = 0.25,
    imbalance_trigger: float = 0.20,
) -> bool:
    return (
        excess_bottom_ratio >= excess_trigger
        and bottom_blank_ratio - top_blank_ratio >= imbalance_trigger
    )

def excessive_unused_space_unjustified(
    page: dict,
    overrides: dict,
    pre_complex_break_pages: set[int],
) -> bool:
    page_number = int(page["page"])
    return (
        page["target_chars"] >= 120
        and page.get("mapped_has_body_prose", True)
        and not page.get("mapped_has_retained_regions", False)
        and not page["whole_page_reference_exception"]
        and not page["complex_visual_page"]
        and not page.get("is_final_candidate_page", False)
        and page_number not in pre_complex_break_pages
        and not sparse_layout_justified(overrides, page_number)
        and bottom_whitespace_is_unbalanced(
            page["excess_bottom_blank_ratio"],
            page["largest_column_bottom_blank_ratio"],
            page["top_blank_ratio"],
        )
    )

def compressed_page_requires_repair(page: dict) -> bool:
    return bool(
        page.get("compressed_despite_blank_space")
        and not page.get("whole_page_reference_exception")
        and not page.get("structured_table_visual_check")
        and not page.get("complex_visual_page")
        and not page.get("is_final_candidate_page", False)
    )

def text_block_overlaps(text_dict: dict) -> list[dict]:
    blocks = []
    for block in text_dict["blocks"]:
        if block.get("type") != 0:
            continue
        text = "".join(
            span.get("text", "")
            for line in block.get("lines", [])
            for span in line.get("spans", [])
        ).strip()
        if len(text) < 12:
            continue
        bbox = [float(value) for value in block["bbox"]]
        area = max(0.0, bbox[2] - bbox[0]) * max(0.0, bbox[3] - bbox[1])
        if area <= 0:
            continue
        blocks.append({"text": text, "bbox": bbox, "area": area})

    overlaps = []
    for index, first in enumerate(blocks):
        for second in blocks[index + 1 :]:
            x0 = max(first["bbox"][0], second["bbox"][0])
            y0 = max(first["bbox"][1], second["bbox"][1])
            x1 = min(first["bbox"][2], second["bbox"][2])
            y1 = min(first["bbox"][3], second["bbox"][3])
            intersection = max(0.0, x1 - x0) * max(0.0, y1 - y0)
            if intersection / min(first["area"], second["area"]) < 0.35:
                continue
            overlaps.append(
                {
                    "first": first["text"][:100],
                    "second": second["text"][:100],
                    "intersection_ratio": round(
                        intersection / min(first["area"], second["area"]), 3
                    ),
                }
            )
    return overlaps

def text_span_overlaps(spans: list[dict]) -> list[dict]:
    prepared = []
    for span in spans:
        text = span.get("text", "").strip()
        if len(text) < 2:
            continue
        bbox = [float(value) for value in span["bbox"]]
        area = max(0.0, bbox[2] - bbox[0]) * max(0.0, bbox[3] - bbox[1])
        if area <= 0:
            continue
        prepared.append({"text": text, "bbox": bbox, "area": area})
    overlaps = []
    for index, first in enumerate(prepared):
        for second in prepared[index + 1 :]:
            x0 = max(first["bbox"][0], second["bbox"][0])
            y0 = max(first["bbox"][1], second["bbox"][1])
            x1 = min(first["bbox"][2], second["bbox"][2])
            y1 = min(first["bbox"][3], second["bbox"][3])
            intersection = max(0.0, x1 - x0) * max(0.0, y1 - y0)
            ratio = intersection / min(first["area"], second["area"])
            if ratio < 0.45:
                continue
            overlaps.append(
                {
                    "first": first["text"][:100],
                    "second": second["text"][:100],
                    "intersection_ratio": round(ratio, 3),
                }
            )
    return overlaps
