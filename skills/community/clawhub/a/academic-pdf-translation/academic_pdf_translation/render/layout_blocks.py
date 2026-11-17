"""统一排版块。

以前每个渲染分支各自往 PDF 里写，分页规则也各写一套。结果就是
图题和图分到两页、脚注插进正文、表题和表格被拆开——这些不是排版参数
调得不好，是根本没有一个地方统一管"哪些东西必须待在一起"。

现在所有元素先变成 LayoutBlock，绑定关系写在块上，分页只有一处实现。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.enums import ElementType

# --- 块种类 -----------------------------------------------------------------

KIND_TEXT = "text"
KIND_HEADING = "heading"
KIND_FIGURE = "figure"
KIND_TABLE = "table"
KIND_FORMULA = "formula"
KIND_CAPTION = "caption"
KIND_TABLE_NOTE = "table-note"
KIND_FOOTNOTE = "footnote"
KIND_REFERENCE = "reference"
KIND_PRESERVED_REGION = "preserved-region"

#: 这些块不能被分页切开。切开就意味着图只剩一半、公式断成两截。
UNSPLITTABLE_KINDS = frozenset(
    {KIND_FIGURE, KIND_TABLE, KIND_FORMULA, KIND_PRESERVED_REGION}
)

#: 脚注不进正文流，由页面合成器送到页脚区。
FOOTER_AREA_KINDS = frozenset({KIND_FOOTNOTE})

ELEMENT_KIND_MAP = {
    ElementType.DOCUMENT_TITLE: KIND_HEADING,
    ElementType.HEADING: KIND_HEADING,
    ElementType.REFERENCE_HEADING: KIND_HEADING,
    ElementType.AUTHOR_BLOCK: KIND_TEXT,
    ElementType.AFFILIATION: KIND_TEXT,
    ElementType.PUBLICATION_METADATA: KIND_TEXT,
    ElementType.BODY: KIND_TEXT,
    ElementType.CAPTION: KIND_CAPTION,
    ElementType.TABLE: KIND_TABLE,
    ElementType.TABLE_NOTE: KIND_TABLE_NOTE,
    ElementType.RASTER_FIGURE: KIND_FIGURE,
    ElementType.VECTOR_FIGURE: KIND_FIGURE,
    ElementType.CHART: KIND_FIGURE,
    ElementType.SCREENSHOT: KIND_FIGURE,
    ElementType.DISPLAY_FORMULA: KIND_FORMULA,
    ElementType.FOOTNOTE: KIND_FOOTNOTE,
    ElementType.REFERENCE_ENTRY: KIND_REFERENCE,
}


@dataclass
class LayoutBlock:
    """一个排版块。"""

    id: str
    source_element_id: str
    kind: str
    page_hint: int = 0
    preferred_width: float | None = None
    minimum_height: float | None = None
    #: 与下一块绑定：两者之间不允许分页。
    keep_with_next: bool = False
    #: 允许被分页切开。图、表、公式一律不允许。
    splittable: bool = True
    #: 同组的其他块 ID。一组必须整体落在同一页。
    group_id: str | None = None
    order: int = 0
    renderer: str = ""
    strategy: str = ""
    translation_unit_ids: list[str] = field(default_factory=list)
    renderer_payload: dict[str, Any] = field(default_factory=dict)

    @property
    def goes_to_footer(self) -> bool:
        return self.kind in FOOTER_AREA_KINDS

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def kind_for(element_type: ElementType) -> str:
    return ELEMENT_KIND_MAP.get(element_type, KIND_TEXT)


@dataclass
class BlockGroup:
    """必须整体待在同一页的一组块。

    图与图题、表与表题表注、公式主体与编号——这三组是硬绑定。
    """

    id: str
    block_ids: list[str] = field(default_factory=list)
    reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _sort_key(element: Any) -> tuple[int, float, float]:
    box = element.bbox or (0.0, 0.0, 0.0, 0.0)
    return (element.page, box[1], box[0])


def build_blocks(
    inventory: Any,
    plan: Any,
) -> tuple[list[LayoutBlock], list[BlockGroup]]:
    """把元素清单和渲染计划变成排版块与绑定组。

    这里不做翻译、不做元素识别、不做 QA，只决定"这块是什么、
    能不能拆、和谁绑在一起"。
    """

    planned = {item.element_id: item for item in plan.elements}
    ordered = sorted(
        (
            element
            for element in inventory.elements
            if planned.get(element.id) is not None
            and planned[element.id].status != "omitted"
        ),
        key=_sort_key,
    )

    blocks: list[LayoutBlock] = []
    by_element: dict[str, LayoutBlock] = {}
    for order, element in enumerate(ordered):
        item = planned[element.id]
        kind = kind_for(element.type)
        block = LayoutBlock(
            id=f"block-{element.id}",
            source_element_id=element.id,
            kind=kind,
            page_hint=element.page,
            keep_with_next=False,
            splittable=kind not in UNSPLITTABLE_KINDS,
            order=order,
            renderer=item.renderer,
            strategy=item.strategy,
            translation_unit_ids=list(element.translation_unit_ids),
            renderer_payload={
                "element_type": element.type.value,
                "bbox": list(element.bbox) if element.bbox else None,
                "fallback_levels": list(item.fallback_levels),
            },
        )
        blocks.append(block)
        by_element[element.id] = block

    groups: list[BlockGroup] = []

    def bind(anchor_id: str, member_ids: list[str], reason: str) -> None:
        anchor = by_element.get(anchor_id)
        members = [by_element[mid] for mid in member_ids if mid in by_element]
        if anchor is None or not members:
            return
        group_id = f"group-{anchor_id}"
        group = BlockGroup(
            id=group_id,
            block_ids=[anchor.id] + [member.id for member in members],
            reason=reason,
        )
        for block in [anchor, *members]:
            block.group_id = group_id
            block.splittable = False
        groups.append(group)

    for element in ordered:
        block = by_element[element.id]
        if block.kind == KIND_FIGURE:
            bind(
                element.id,
                element.relations.get("caption", []),
                "图与图题必须同页",
            )
        elif block.kind == KIND_TABLE:
            bind(
                element.id,
                element.relations.get("caption", [])
                + element.relations.get("table-note", []),
                "表格与表题、表注必须同页",
            )
        elif block.kind == KIND_FORMULA and element.detail.get(
            "formula_number"
        ):
            block.splittable = False

    # 组内按阅读顺序排：图题在图下方时排在图后面，在上方时排在前面。
    order_by_id = {block.id: block.order for block in blocks}
    for group in groups:
        group.block_ids.sort(key=lambda block_id: order_by_id.get(block_id, 0))
        for block_id in group.block_ids[:-1]:
            for block in blocks:
                if block.id == block_id:
                    block.keep_with_next = True
                    break

    return blocks, groups
