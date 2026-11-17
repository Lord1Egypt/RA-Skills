"""脚注检测。

脚注混进正文会把结论段落切断，插进参考文献标题和第一条题录之间更糟。
认出来才谈得上把它排回页脚。
"""

from __future__ import annotations

import re
from typing import Any

from academic_pdf_translation.contracts.models import BBox, normalize_bbox

DETECTOR_VERSION = "footnotes-v1"

#: 脚注编号：行首的数字、上标数字或星号。
FOOTNOTE_MARKER_RE = re.compile(r"^\s*(?:[\d]{1,2}|[*†‡§]|[⁰-⁹]{1,2})\s+\S")
#: 脚注分隔线通常短，只占版心左侧一小段。
MAX_SEPARATOR_WIDTH_RATIO = 0.45
MAX_SEPARATOR_THICKNESS_PT = 2.5
#: 脚注区域必须落在页面下方这个比例之下。
FOOTNOTE_ZONE_TOP_RATIO = 0.60
#: 脚注字号相对正文中位字号的上限。
MAX_FOOTNOTE_FONT_RATIO = 0.92
#: 块的上沿可能比分隔线高出零点几个点（基线与线宽的差），给一点容差。
FOOTNOTE_TOP_TOLERANCE_PT = 4.0
#: 估正文字号时，只有这么长的块才算散文。
MIN_PROSE_BLOCK_CHARS = 80


def find_separator(page: dict[str, Any]) -> BBox | None:
    """找脚注分隔线：页面下半部、细、短、靠左。"""

    height = float(page.get("height") or 0) or 1.0
    width = float(page.get("width") or 0) or 1.0
    best: BBox | None = None
    for raw in page.get("drawing_bboxes") or []:
        box = normalize_bbox(raw)
        if box is None:
            continue
        if box[3] - box[1] > MAX_SEPARATOR_THICKNESS_PT:
            continue
        if (box[2] - box[0]) / width > MAX_SEPARATOR_WIDTH_RATIO:
            continue
        if box[1] / height < FOOTNOTE_ZONE_TOP_RATIO:
            continue
        if best is None or box[1] < best[1]:
            best = box
    return best


def _body_font_size(page: dict[str, Any], zone_top: float) -> float:
    """正文字号：只统计脚注区以外的块。

    把脚注自己算进中位数，正文字号会被拉低到和脚注一样，
    "脚注比正文小"这条判据就永远不成立。
    """

    # 按字符数加权，而且只看真正的散文块。图内标签和表格单元格数量多、
    # 字号小，用块数取中位数会把"正文字号"拉到和脚注一样。
    weights: dict[float, int] = {}
    for block in page.get("blocks") or []:
        if block.get("page_furniture"):
            continue
        box = normalize_bbox(block.get("bbox"))
        if box is None or box[3] > zone_top:
            continue
        text = str(block.get("text") or "")
        if len(text) < MIN_PROSE_BLOCK_CHARS:
            continue
        size = float(block.get("font", {}).get("median_size") or 0)
        if size > 0:
            weights[size] = weights.get(size, 0) + len(text)
    if not weights:
        return 0.0
    return max(weights.items(), key=lambda item: (item[1], item[0]))[0]


def detect_footnotes(page: dict[str, Any]) -> list[dict[str, Any]]:
    """返回这一页的脚注块。"""

    height = float(page.get("height") or 0) or 1.0
    separator = find_separator(page)
    zone_top = (
        separator[3]
        if separator is not None
        else height * FOOTNOTE_ZONE_TOP_RATIO
    )
    body_size = _body_font_size(page, zone_top)

    results: list[dict[str, Any]] = []
    for block in page.get("blocks") or []:
        if block.get("page_furniture"):
            continue
        box = normalize_bbox(block.get("bbox"))
        if box is None:
            continue
        below_separator = (
            box[3] > zone_top
            and box[1] >= zone_top - FOOTNOTE_TOP_TOLERANCE_PT
        )
        if not below_separator:
            continue
        text = str(block.get("text") or "").strip()
        if not text:
            continue
        size = float(block.get("font", {}).get("median_size") or 0)
        smaller = bool(
            body_size and size and size <= body_size * MAX_FOOTNOTE_FONT_RATIO
        )
        marked = bool(FOOTNOTE_MARKER_RE.match(text))
        # 分隔线是排版上的明确声明：线下面、又带编号的块就是脚注，
        # 不必再要求它比正文小（图表密集页的"正文字号"本来就不可靠）。
        qualifies = (
            (marked or smaller) if separator is not None else (smaller and marked)
        )
        if not qualifies:
            continue
        confidence = 0.6 + (0.2 if marked else 0.0) + (
            0.15 if separator is not None else 0.0
        )
        results.append(
            {
                "bbox": box,
                "block_id": int(block["id"]),
                "text": text,
                "marker": marked,
                "has_separator": separator is not None,
                "font_size": size,
                "body_font_size": body_size,
                "confidence": round(min(confidence, 0.95), 4),
            }
        )
    results.sort(key=lambda item: item["bbox"][1])
    return results
