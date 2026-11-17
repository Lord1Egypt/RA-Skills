"""原文元素清单的数据模型。

一句话说清它要解决什么：以前程序只知道"第 7 页很复杂"，不知道那一页
到底有几个东西。于是漏一张图、压平一个表格，没有任何环节会发现。

现在每一个正文、标题、图、表、公式、脚注都是一个有稳定 ID 的元素。
后面的渲染计划、候选映射和结构对账都挂在这些 ID 上。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.enums import (
    PAGE_FURNITURE_TYPES,
    REQUIRED_ELEMENT_TYPES,
    VISUAL_ELEMENT_TYPES,
    ElementType,
)

BBox = tuple[float, float, float, float]


def normalize_bbox(value: Any) -> BBox | None:
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        return None
    try:
        x0, y0, x1, y1 = (float(item) for item in value)
    except (TypeError, ValueError):
        return None
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def union_bbox(boxes: list[BBox]) -> BBox | None:
    valid = [box for box in boxes if box is not None]
    if not valid:
        return None
    return (
        min(box[0] for box in valid),
        min(box[1] for box in valid),
        max(box[2] for box in valid),
        max(box[3] for box in valid),
    )


def bbox_area(box: BBox | None) -> float:
    if box is None:
        return 0.0
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def bbox_overlap(first: BBox | None, second: BBox | None) -> float:
    if first is None or second is None:
        return 0.0
    width = min(first[2], second[2]) - max(first[0], second[0])
    height = min(first[3], second[3]) - max(first[1], second[1])
    return max(0.0, width) * max(0.0, height)


def center_in_bbox(
    span_bbox: list[float] | tuple[float, ...], bbox: list[float]
) -> bool:
    """一个跨度的中心点在不在某个框里。

    判中心点而不判整框相交：一行文字的框常常比它所属的区域宽出一点，
    按相交算会把邻区的文字也算进来。
    """

    x0, y0, x1, y1 = span_bbox
    cx = (float(x0) + float(x1)) / 2
    cy = (float(y0) + float(y1)) / 2
    bx0, by0, bx1, by1 = map(float, bbox)
    return bx0 <= cx <= bx1 and by0 <= cy <= by1


def bbox_distance(first: BBox | None, second: BBox | None) -> float:
    """两个框之间的最短间距；相交时为 0。"""

    if first is None or second is None:
        return float("inf")
    dx = max(first[0] - second[2], second[0] - first[2], 0.0)
    dy = max(first[1] - second[3], second[1] - first[3], 0.0)
    return (dx * dx + dy * dy) ** 0.5


#: 元素关系。图片→图题、表格→表注、公式→编号等。
RELATION_CAPTION = "caption"
RELATION_CAPTIONS_FOR = "captions-for"
RELATION_TABLE_NOTE = "table-note"
RELATION_NOTE_FOR = "note-for"
RELATION_FORMULA_NUMBER = "formula-number"
RELATION_NUMBER_FOR = "number-for"
RELATION_FOOTNOTE_MARKER = "footnote-marker"
RELATION_MARKER_FOR = "marker-for"
RELATION_FOLLOWING_BODY = "following-body"
RELATION_SECTION_HEADING = "section-heading"
RELATION_EMBEDDED_LABEL = "embedded-label"
RELATION_LABEL_OF = "label-of"
RELATION_PARENT = "parent"
RELATION_CHILD = "child"


@dataclass
class ElementRisk:
    """一条风险标记。有风险不等于识别失败，但要进定向检查。"""

    code: str
    detail: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SourceElement:
    """原文里的一个东西。"""

    id: str
    page: int
    type: ElementType
    bbox: BBox | None = None
    confidence: float = 1.0
    source_block_ids: list[int] = field(default_factory=list)
    translation_unit_ids: list[str] = field(default_factory=list)
    #: 判定依据。写清楚为什么认为它是这个类型。
    signals: list[str] = field(default_factory=list)
    risk_flags: list[ElementRisk] = field(default_factory=list)
    #: 关系名 → 对方元素 ID 列表。
    relations: dict[str, list[str]] = field(default_factory=dict)
    #: 类型专属的结构信息（表格行列、图内标签、绘图对象数量等）。
    detail: dict[str, Any] = field(default_factory=dict)
    text: str = ""

    @property
    def required(self) -> bool:
        """丢了就是丢内容的元素。"""

        return self.type in REQUIRED_ELEMENT_TYPES

    @property
    def is_visual(self) -> bool:
        return self.type in VISUAL_ELEMENT_TYPES

    @property
    def is_page_furniture(self) -> bool:
        return self.type in PAGE_FURNITURE_TYPES

    def add_risk(self, code: str, detail: str = "") -> None:
        if not any(risk.code == code for risk in self.risk_flags):
            self.risk_flags.append(ElementRisk(code=code, detail=detail))

    def link(self, relation: str, other_id: str) -> None:
        targets = self.relations.setdefault(relation, [])
        if other_id not in targets:
            targets.append(other_id)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "page": self.page,
            "type": self.type.value,
            "bbox": list(self.bbox) if self.bbox else None,
            "confidence": round(float(self.confidence), 4),
            "required": self.required,
            "source_block_ids": list(self.source_block_ids),
            "translation_unit_ids": list(self.translation_unit_ids),
            "signals": list(self.signals),
            "risk_flags": [risk.as_dict() for risk in self.risk_flags],
            "relations": {
                key: list(value) for key, value in sorted(self.relations.items())
            },
            "detail": dict(self.detail),
            "text_excerpt": self.text[:200],
        }


@dataclass
class SourceElementInventory:
    """一份原文的完整元素清单。"""

    source_sha256: str
    page_count: int
    elements: list[SourceElement] = field(default_factory=list)
    unresolved_elements: list[dict[str, Any]] = field(default_factory=list)
    detector_version: str = ""
    cache_key: str = ""
    schema_version: str = "2.0"

    def by_page(self, page: int) -> list[SourceElement]:
        return [element for element in self.elements if element.page == page]

    def by_id(self, element_id: str) -> SourceElement | None:
        for element in self.elements:
            if element.id == element_id:
                return element
        return None

    def required_elements(self) -> list[SourceElement]:
        return [element for element in self.elements if element.required]

    def type_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for element in self.elements:
            counts[element.type.value] = counts.get(element.type.value, 0) + 1
        return dict(sorted(counts.items()))

    def high_risk_pages(self) -> list[int]:
        pages = {
            element.page
            for element in self.elements
            if element.risk_flags or element.type in VISUAL_ELEMENT_TYPES
            or element.type is ElementType.DISPLAY_FORMULA
            or element.type is ElementType.FOOTNOTE
        }
        return sorted(pages)

    def low_confidence_elements(self, floor: float) -> list[SourceElement]:
        return [
            element
            for element in self.elements
            if element.confidence < floor
        ]

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source_sha256": self.source_sha256,
            "page_count": self.page_count,
            "detector_version": self.detector_version,
            "cache_key": self.cache_key,
            "element_count": len(self.elements),
            "required_element_count": len(self.required_elements()),
            "type_counts": self.type_counts(),
            "high_risk_pages": self.high_risk_pages(),
            "elements": [element.as_dict() for element in self.elements],
            "unresolved_elements": list(self.unresolved_elements),
        }
