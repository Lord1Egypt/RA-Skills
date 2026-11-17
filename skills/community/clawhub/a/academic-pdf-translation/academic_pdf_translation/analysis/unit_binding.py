"""把翻译单元绑到原文元素上。

译文不能只是一堆不知道放哪儿的文字。程序必须能说出：这段属于正文、
这个词属于表格里的某一格、这个标签属于图里的某个箭头、这段属于脚注。

绑不上会有两个直接后果：表格没法逐格重建；图内标签只能靠猜，
最后就变成凭空编出来的中文说明。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from academic_pdf_translation.contracts.enums import ElementType
from academic_pdf_translation.contracts.models import (
    SourceElement,
    SourceElementInventory,
    bbox_area,
    bbox_overlap,
    normalize_bbox,
)

# --- 单元在元素里的角色 -----------------------------------------------------

ROLE_BODY = "body"
ROLE_HEADING = "heading"
ROLE_DOCUMENT_TITLE = "document-title"
ROLE_AUTHOR = "author"
ROLE_AFFILIATION = "affiliation"
ROLE_PUBLICATION_METADATA = "publication-metadata"
ROLE_FIGURE_CAPTION = "figure-caption"
ROLE_TABLE_TITLE = "table-title"
ROLE_TABLE_HEADER = "table-header"
ROLE_TABLE_CELL = "table-cell"
ROLE_TABLE_NOTE = "table-note"
ROLE_FIGURE_LABEL = "figure-label"
ROLE_FOOTNOTE = "footnote"
ROLE_FORMULA_LABEL = "formula-label"
ROLE_REFERENCE_ENTRY = "reference-entry"
ROLE_PAGE_FURNITURE = "page-furniture"
ROLE_UNKNOWN = "unknown"

ELEMENT_TYPE_ROLES = {
    ElementType.DOCUMENT_TITLE: ROLE_DOCUMENT_TITLE,
    ElementType.AUTHOR_BLOCK: ROLE_AUTHOR,
    ElementType.AFFILIATION: ROLE_AFFILIATION,
    ElementType.PUBLICATION_METADATA: ROLE_PUBLICATION_METADATA,
    ElementType.HEADING: ROLE_HEADING,
    ElementType.BODY: ROLE_BODY,
    ElementType.TABLE_NOTE: ROLE_TABLE_NOTE,
    ElementType.FOOTNOTE: ROLE_FOOTNOTE,
    ElementType.REFERENCE_ENTRY: ROLE_REFERENCE_ENTRY,
    ElementType.REFERENCE_HEADING: ROLE_HEADING,
    ElementType.HEADER: ROLE_PAGE_FURNITURE,
    ElementType.FOOTER: ROLE_PAGE_FURNITURE,
    ElementType.PAGE_NUMBER: ROLE_PAGE_FURNITURE,
    ElementType.WATERMARK: ROLE_PAGE_FURNITURE,
    ElementType.DISPLAY_FORMULA: ROLE_FORMULA_LABEL,
    ElementType.TABLE: ROLE_TABLE_CELL,
    ElementType.VECTOR_FIGURE: ROLE_FIGURE_LABEL,
    ElementType.RASTER_FIGURE: ROLE_FIGURE_LABEL,
    ElementType.CHART: ROLE_FIGURE_LABEL,
    ElementType.SCREENSHOT: ROLE_FIGURE_LABEL,
}

#: 这些角色的文字不进正文流。
NON_BODY_FLOW_ROLES = frozenset(
    {
        ROLE_FOOTNOTE,
        ROLE_TABLE_CELL,
        ROLE_TABLE_HEADER,
        ROLE_TABLE_NOTE,
        ROLE_FIGURE_LABEL,
        ROLE_PAGE_FURNITURE,
    }
)

#: 单元落进元素区域所需的最小重叠比例。
MIN_BBOX_OVERLAP_RATIO = 0.55


def _caption_role(element: SourceElement) -> str:
    kind = str(element.detail.get("caption_kind") or "")
    return ROLE_TABLE_TITLE if kind == "table" else ROLE_FIGURE_CAPTION


def role_for(element: SourceElement) -> str:
    if element.type is ElementType.CAPTION:
        return _caption_role(element)
    if element.detail.get("role") == "embedded-label":
        return ROLE_FIGURE_LABEL
    return ELEMENT_TYPE_ROLES.get(element.type, ROLE_UNKNOWN)


@dataclass
class UnitBinding:
    """一个翻译单元的归属。"""

    unit_id: str
    element_id: str
    element_type: str
    element_role: str
    match: str
    #: 表格单元格用：行列位置。定不下来时留 None，不猜。
    row: int | None = None
    column: int | None = None

    def as_dict(self) -> dict[str, Any]:
        data = {
            "unit_id": self.unit_id,
            "element_id": self.element_id,
            "element_type": self.element_type,
            "element_role": self.element_role,
            "match": self.match,
        }
        if self.row is not None:
            data["row"] = self.row
        if self.column is not None:
            data["column"] = self.column
        return data


@dataclass
class BindingReport:
    """绑定结果与完整性检查。"""

    bindings: list[UnitBinding] = field(default_factory=list)
    orphan_units: list[str] = field(default_factory=list)
    elements_without_units: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        return not self.orphan_units and not self.problems

    def by_unit(self) -> dict[str, UnitBinding]:
        return {binding.unit_id: binding for binding in self.bindings}

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "2.0",
            "bound_units": len(self.bindings),
            "orphan_units": list(self.orphan_units),
            "elements_without_units": list(self.elements_without_units),
            "complete": self.complete,
            "problems": list(self.problems),
            "bindings": [binding.as_dict() for binding in self.bindings],
        }


def _block_index(
    inventory: SourceElementInventory,
) -> dict[tuple[int, int], SourceElement]:
    """(页码, 块 ID) → 元素。块 ID 是精确的连接键。"""

    index: dict[tuple[int, int], SourceElement] = {}
    for element in inventory.elements:
        for block_id in element.source_block_ids:
            index.setdefault((element.page, int(block_id)), element)
    return index


def _best_region_match(
    unit: dict[str, Any],
    inventory: SourceElementInventory,
) -> SourceElement | None:
    """按坐标重叠找归属，用于没有块 ID 的区域型元素（图、表）。"""

    box = normalize_bbox(unit.get("source_bbox"))
    if box is None:
        return None
    area = bbox_area(box)
    if area <= 0:
        return None
    best: SourceElement | None = None
    best_ratio = MIN_BBOX_OVERLAP_RATIO
    for element in inventory.by_page(int(unit.get("page") or 0)):
        if element.bbox is None:
            continue
        ratio = bbox_overlap(box, element.bbox) / area
        if ratio >= best_ratio:
            best, best_ratio = element, ratio
    return best


def bind_units(
    units: list[dict[str, Any]],
    inventory: SourceElementInventory,
) -> BindingReport:
    """把翻译单元绑到元素上。

    先按块 ID 精确匹配，匹配不上再按坐标重叠。两条都落空就是孤立译文，
    如实报出来，不硬塞给某个元素。
    """

    report = BindingReport()
    block_index = _block_index(inventory)
    claimed: set[str] = set()

    for unit in units:
        unit_id = str(unit.get("id") or "")
        if not unit_id:
            report.problems.append("存在没有 ID 的翻译单元")
            continue
        page = int(unit.get("page") or 0)
        element: SourceElement | None = None
        match = ""
        for block_id in unit.get("source_block_ids") or []:
            element = block_index.get((page, int(block_id)))
            if element is not None:
                match = "source-block-id"
                break
        if element is None:
            element = _best_region_match(unit, inventory)
            match = "bbox-overlap" if element is not None else ""
        if element is None:
            report.orphan_units.append(unit_id)
            continue

        element.translation_unit_ids.append(unit_id)
        claimed.add(element.id)
        report.bindings.append(
            UnitBinding(
                unit_id=unit_id,
                element_id=element.id,
                element_type=element.type.value,
                element_role=role_for(element),
                match=match,
            )
        )

    for element in inventory.elements:
        if element.id in claimed:
            continue
        if element.type in {
            ElementType.VECTOR_FIGURE,
            ElementType.RASTER_FIGURE,
            ElementType.CHART,
            ElementType.SCREENSHOT,
        }:
            # 图形本身没有文字，没有单元是正常的。
            continue
        report.elements_without_units.append(element.id)

    if report.orphan_units:
        report.problems.append(
            "以下译文单元找不到归属元素: "
            + ", ".join(report.orphan_units[:20])
        )
    return report


def validate_payload_sources(
    payload_texts: list[dict[str, Any]],
    bound_unit_ids: set[str],
) -> list[str]:
    """复杂载荷里的每段中文都必须来自某个翻译单元。

    这一条直接对着"凭空编出来的图内说明"：没有 unit_id 的文字一律报错。
    """

    problems: list[str] = []
    for index, entry in enumerate(payload_texts):
        text = str(entry.get("translation") or entry.get("text") or "").strip()
        if not text:
            continue
        unit_id = str(entry.get("translation_unit_id") or "").strip()
        if not unit_id:
            problems.append(
                f"载荷文字[{index}] 没有绑定 translation_unit_id: {text[:40]!r}"
            )
            continue
        if unit_id not in bound_unit_ids:
            problems.append(
                f"载荷文字[{index}] 绑定了不存在的单元 {unit_id}"
            )
    return problems
