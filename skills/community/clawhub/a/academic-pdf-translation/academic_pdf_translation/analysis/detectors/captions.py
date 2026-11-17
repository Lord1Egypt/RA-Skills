"""图题、表题与表注检测，以及它们与主体的绑定。

图题和图分到两页，是这次真实论文里出现过的问题。绑定必须有依据：
距离最近，而且在阅读顺序上挨着。
"""

from __future__ import annotations

import re

from academic_pdf_translation.contracts.models import BBox, bbox_distance

DETECTOR_VERSION = "captions-v1"

FIGURE_CAPTION_RE = re.compile(
    r"^\s*(?:fig(?:ure)?\.?|图)\s*([0-9IVXivx]+)\b",
    re.IGNORECASE,
)
TABLE_CAPTION_RE = re.compile(
    r"^\s*(?:table|tab\.|表)\s*([0-9IVXivx]+)\b",
    re.IGNORECASE,
)

#: 图题与图之间的最大距离（点）。超过它就不算同一组。
MAX_CAPTION_BIND_DISTANCE_PT = 90.0


def caption_kind(text: str) -> str | None:
    value = str(text or "")
    if FIGURE_CAPTION_RE.match(value):
        return "figure"
    if TABLE_CAPTION_RE.match(value):
        return "table"
    return None


def caption_label(text: str) -> str | None:
    for pattern in (FIGURE_CAPTION_RE, TABLE_CAPTION_RE):
        match = pattern.match(str(text or ""))
        if match:
            return match.group(1)
    return None


def bind_caption(
    caption_bbox: BBox,
    candidates: list[tuple[str, BBox]],
    *,
    max_distance: float = MAX_CAPTION_BIND_DISTANCE_PT,
) -> tuple[str | None, float]:
    """把一个图题绑到最近的视觉元素上。

    返回 (元素 ID, 距离)。找不到足够近的就返回 (None, inf)。
    """

    best_id: str | None = None
    best_distance = float("inf")
    for element_id, box in candidates:
        distance = bbox_distance(caption_bbox, box)
        if distance < best_distance:
            best_id, best_distance = element_id, distance
    if best_distance > max_distance:
        return None, best_distance
    return best_id, best_distance
