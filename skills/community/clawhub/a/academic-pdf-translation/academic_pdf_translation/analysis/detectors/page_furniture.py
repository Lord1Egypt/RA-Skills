"""页眉、页脚、页码与水印。

它们可以合法省略，但省略必须走结构化代码，不能靠一句自由文字。
"""

from __future__ import annotations

import re
from typing import Any

from academic_pdf_translation.contracts.enums import ElementType
from academic_pdf_translation.contracts.models import normalize_bbox

DETECTOR_VERSION = "page-furniture-v1"

PAGE_NUMBER_RE = re.compile(r"^\s*[-–—\[(]?\s*\d{1,4}\s*[-–—\])]?\s*$")
#: 页眉区与页脚区各占页面上下这个比例。
HEADER_ZONE_RATIO = 0.08
FOOTER_ZONE_RATIO = 0.92
#: 判定页码时放宽一点：页码常印在版心之内、离页边一两厘米。
PAGE_NUMBER_HEADER_RATIO = 0.15
PAGE_NUMBER_FOOTER_RATIO = 0.85
#: 页码块必须很窄，否则那是正文里的一个数字。
MAX_PAGE_NUMBER_WIDTH_RATIO = 0.12


def classify_furniture(
    block: dict[str, Any],
    page: dict[str, Any],
) -> ElementType | None:
    """判断一个块是不是页面家具；不是就返回 None。"""

    box = normalize_bbox(block.get("bbox"))
    if box is None:
        return None
    height = float(page.get("height") or 0) or 1.0
    text = str(block.get("text") or "").strip()
    if not text:
        return None
    top_ratio = box[1] / height
    bottom_ratio = box[3] / height
    width = float(page.get("width") or 0) or 1.0
    narrow = (box[2] - box[0]) / width <= MAX_PAGE_NUMBER_WIDTH_RATIO
    if (
        PAGE_NUMBER_RE.match(text)
        and narrow
        and (
            top_ratio <= PAGE_NUMBER_HEADER_RATIO
            or bottom_ratio >= PAGE_NUMBER_FOOTER_RATIO
        )
    ):
        return ElementType.PAGE_NUMBER
    if block.get("page_furniture"):
        if top_ratio <= HEADER_ZONE_RATIO:
            return ElementType.HEADER
        if bottom_ratio >= FOOTER_ZONE_RATIO:
            return ElementType.FOOTER
        return ElementType.HEADER
    return None
