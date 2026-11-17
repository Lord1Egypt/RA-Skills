"""表格检测。

按可靠程度依次尝试：

1. 横竖线组成的网格（含 booktabs 那种只有横线的三线表）；
2. "Table N / 表 N" 标题信号；
3. 对齐文字组成的行列。

置信度不够就如实标风险，不假装识别成功——后面的渲染计划会据此改用
"保留原表区域"，而不是硬重建。
"""

from __future__ import annotations

import re
from typing import Any

from academic_pdf_translation.contracts.models import (
    BBox,
    normalize_bbox,
    union_bbox,
)

DETECTOR_VERSION = "tables-v1"

TABLE_CAPTION_RE = re.compile(
    r"^\s*(?:table|tab\.|表)\s*([0-9IVXivx]+)\b",
    re.IGNORECASE,
)
TABLE_NOTE_RE = re.compile(r"^\s*(?:note|notes|注)\s*[:：.]", re.IGNORECASE)

#: 线要多细才算规则线而不是填充块。
MAX_RULE_THICKNESS_PT = 2.5
#: 两条线的左右端点差在这个范围内算同一张表。
RULE_X_TOLERANCE_PT = 6.0
#: 表格规则线之间的最大垂直间距，超过就算两张表。
MAX_RULE_GAP_PT = 260.0
#: 表格标题到表体的最大距离。
MAX_CAPTION_DISTANCE_PT = 60.0


def _horizontal_rules(page: dict[str, Any]) -> list[BBox]:
    rules: list[BBox] = []
    for raw in page.get("drawing_bboxes") or []:
        box = normalize_bbox(raw)
        if box is None:
            continue
        height = box[3] - box[1]
        width = box[2] - box[0]
        if height <= MAX_RULE_THICKNESS_PT and width >= 40.0:
            rules.append(box)
    rules.sort(key=lambda box: (box[1], box[0]))
    return rules


def _group_rules(rules: list[BBox]) -> list[list[BBox]]:
    """把左右端点接近、上下相邻的横线归成一组。"""

    groups: list[list[BBox]] = []
    for rule in rules:
        placed = False
        for group in groups:
            reference = group[0]
            if (
                abs(rule[0] - reference[0]) <= RULE_X_TOLERANCE_PT
                and abs(rule[2] - reference[2]) <= RULE_X_TOLERANCE_PT
                and rule[1] - group[-1][3] <= MAX_RULE_GAP_PT
            ):
                group.append(rule)
                placed = True
                break
        if not placed:
            groups.append([rule])
    return [group for group in groups if len(group) >= 2]


def _blocks_in(page: dict[str, Any], region: BBox) -> list[dict[str, Any]]:
    inside: list[dict[str, Any]] = []
    for block in page.get("blocks") or []:
        box = normalize_bbox(block.get("bbox"))
        if box is None:
            continue
        center_y = (box[1] + box[3]) / 2
        center_x = (box[0] + box[2]) / 2
        if (
            region[1] <= center_y <= region[3]
            and region[0] - RULE_X_TOLERANCE_PT
            <= center_x
            <= region[2] + RULE_X_TOLERANCE_PT
        ):
            inside.append(block)
    inside.sort(key=lambda block: normalize_bbox(block["bbox"])[1])
    return inside


def find_table_caption(
    page: dict[str, Any],
    region: BBox,
) -> dict[str, Any] | None:
    """在表体上方找最近的 "Table N" 标题块。"""

    best = None
    best_distance = MAX_CAPTION_DISTANCE_PT
    for block in page.get("blocks") or []:
        text = str(block.get("text") or "").strip()
        if not TABLE_CAPTION_RE.match(text):
            continue
        box = normalize_bbox(block.get("bbox"))
        if box is None:
            continue
        distance = region[1] - box[3]
        if 0 <= distance <= best_distance:
            best, best_distance = block, distance
    return best


def _estimate_grid(blocks: list[dict[str, Any]]) -> tuple[int, int]:
    """从表体文字估行数和列数。

    行数取块内的行数总和；列数取各行里空白分隔出来的最多列数。
    这是估计值，所以调用方必须把它当成"待确认"。
    """

    rows = 0
    columns = 0
    for block in blocks:
        lines = block.get("lines") or []
        rows += max(len(lines), 1)
        for line in lines or [{"text": block.get("text")}]:
            text = str(line.get("text") or "").strip()
            if not text:
                continue
            columns = max(columns, len(re.split(r"\s{2,}", text)))
    return rows, columns


def detect_tables(page: dict[str, Any]) -> list[dict[str, Any]]:
    """返回这一页的表格候选。"""

    tables: list[dict[str, Any]] = []
    used_regions: list[BBox] = []
    for group in _group_rules(_horizontal_rules(page)):
        region = union_bbox(group)
        if region is None:
            continue
        body = _blocks_in(page, region)
        if not body:
            continue
        caption = find_table_caption(page, region)
        rows, columns = _estimate_grid(body)
        signals = ["horizontal-rules"]
        confidence = 0.72
        if caption is not None:
            signals.append("table-caption")
            confidence += 0.15
        if len(group) >= 3:
            signals.append("three-line-table")
            confidence += 0.08
        if columns >= 2:
            signals.append("multi-column-text")
            confidence += 0.05
        tables.append(
            {
                "bbox": region,
                "rule_count": len(group),
                "rows": rows,
                "columns": columns,
                "block_ids": [int(block["id"]) for block in body],
                "caption_block_id": (
                    int(caption["id"]) if caption is not None else None
                ),
                "signals": signals,
                "confidence": round(min(confidence, 0.97), 4),
            }
        )
        used_regions.append(region)

    # 有 "Table N" 标题但没画线的表：仍然要成为元素，只是置信度低。
    for block in page.get("blocks") or []:
        text = str(block.get("text") or "").strip()
        if not TABLE_CAPTION_RE.match(text):
            continue
        box = normalize_bbox(block.get("bbox"))
        if box is None:
            continue
        if any(
            region[1] - MAX_CAPTION_DISTANCE_PT <= box[3] <= region[3]
            for region in used_regions
        ):
            continue
        tables.append(
            {
                "bbox": box,
                "rule_count": 0,
                "rows": 0,
                "columns": 0,
                "block_ids": [int(block["id"])],
                "caption_block_id": int(block["id"]),
                "signals": ["table-caption-only"],
                "confidence": 0.45,
            }
        )
    tables.sort(key=lambda item: (item["bbox"][1], item["bbox"][0]))
    return tables


def is_table_note(text: str) -> bool:
    return bool(TABLE_NOTE_RE.match(str(text or "")))
