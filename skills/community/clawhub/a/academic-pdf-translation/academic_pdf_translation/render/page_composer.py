"""页面合成器：唯一负责分页的地方。

它只管六件事：块顺序、分页、版心、同页绑定、页眉页脚、输出映射。

它不翻译，不识别元素，不做 QA。这三件事各有各的模块——分页逻辑散落到
每个渲染分支里，正是图题跨页和脚注混进正文的成因。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.render.layout_blocks import (
    BlockGroup,
    LayoutBlock,
)

#: 版心之外留给页脚区的高度下限，脚注放不下时会向上要空间。
MIN_FOOTER_RESERVE_PT = 0.0


@dataclass
class PageArea:
    """版心。"""

    width: float
    height: float
    top_margin: float = 48.0
    bottom_margin: float = 48.0
    left_margin: float = 56.0
    right_margin: float = 56.0

    @property
    def content_width(self) -> float:
        return self.width - self.left_margin - self.right_margin

    @property
    def content_height(self) -> float:
        return self.height - self.top_margin - self.bottom_margin


@dataclass
class PlacedBlock:
    """一个块最终落在哪一页。"""

    block_id: str
    source_element_id: str
    kind: str
    page: int
    area: str = "body"
    height: float = 0.0
    split_part: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ComposedDocument:
    """合成结果。"""

    pages: int = 0
    placements: list[PlacedBlock] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    def page_of(self, block_id: str) -> int | None:
        for placed in self.placements:
            if placed.block_id == block_id:
                return placed.page
        return None

    def pages_of_element(self, element_id: str) -> list[int]:
        return sorted(
            {
                placed.page
                for placed in self.placements
                if placed.source_element_id == element_id
            }
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "2.0",
            "pages": self.pages,
            "placements": [item.as_dict() for item in self.placements],
            "problems": list(self.problems),
        }


HeightFn = Callable[[LayoutBlock, float], float]


def _default_height(block: LayoutBlock, width: float) -> float:
    """没有真实测量时的占位高度。真实排版由渲染器提供测量函数。"""

    if block.minimum_height:
        return float(block.minimum_height)
    return 40.0


def compose(
    blocks: list[LayoutBlock],
    groups: list[BlockGroup],
    area: PageArea,
    *,
    measure: HeightFn | None = None,
) -> ComposedDocument:
    """把块排进页面。

    规则：
    - 同一组的块必须整体落在同一页，放不下就整组挪到下一页；
    - 不可拆分的块放不下就整块挪到下一页；
    - 脚注不进正文流，直接进它所在页的页脚区。
    """

    measure_fn = measure or _default_height
    document = ComposedDocument()
    ordered = sorted(blocks, key=lambda block: block.order)
    group_members: dict[str, list[LayoutBlock]] = {}
    for group in groups:
        group_members[group.id] = [
            block for block in ordered if block.id in set(group.block_ids)
        ]

    page = 1
    remaining = area.content_height
    consumed_groups: set[str] = set()

    def start_new_page() -> None:
        nonlocal page, remaining
        page += 1
        remaining = area.content_height

    for block in ordered:
        if block.goes_to_footer:
            # 脚注不占正文流的高度，它属于页脚区。
            document.placements.append(
                PlacedBlock(
                    block_id=block.id,
                    source_element_id=block.source_element_id,
                    kind=block.kind,
                    page=page,
                    area="footer",
                    height=measure_fn(block, area.content_width),
                )
            )
            continue

        if block.group_id:
            if block.group_id in consumed_groups:
                continue
            members = group_members.get(block.group_id, [block])
            total = sum(
                measure_fn(member, area.content_width) for member in members
            )
            if total > remaining and total <= area.content_height:
                start_new_page()
            elif total > area.content_height:
                document.problems.append(
                    f"绑定组 {block.group_id} 高度 {total:.0f}pt "
                    f"超过整页版心 {area.content_height:.0f}pt，无法保持同页"
                )
            for member in members:
                height = measure_fn(member, area.content_width)
                document.placements.append(
                    PlacedBlock(
                        block_id=member.id,
                        source_element_id=member.source_element_id,
                        kind=member.kind,
                        page=page,
                        height=height,
                    )
                )
                remaining -= height
            consumed_groups.add(block.group_id)
            continue

        height = measure_fn(block, area.content_width)
        if height > remaining:
            if not block.splittable:
                if height <= area.content_height:
                    start_new_page()
                else:
                    document.problems.append(
                        f"不可拆分块 {block.id} 高度 {height:.0f}pt "
                        f"超过整页版心，无法完整放下"
                    )
            else:
                start_new_page()
        document.placements.append(
            PlacedBlock(
                block_id=block.id,
                source_element_id=block.source_element_id,
                kind=block.kind,
                page=page,
                height=height,
            )
        )
        remaining -= height

    document.pages = page
    _verify_groups(document, groups)
    return document


def _verify_groups(
    document: ComposedDocument,
    groups: list[BlockGroup],
) -> None:
    """合成之后再核一遍：绑定组真的落在同一页了吗。"""

    for group in groups:
        pages = {
            placed.page
            for placed in document.placements
            if placed.block_id in set(group.block_ids)
        }
        if len(pages) > 1:
            document.problems.append(
                f"绑定组 {group.id} 被拆到了第 {sorted(pages)} 页: {group.reason}"
            )


def candidate_page_map(document: ComposedDocument) -> dict[str, list[int]]:
    """输出映射：每个源元素落在候选的哪些页。"""

    mapping: dict[str, list[int]] = {}
    for placed in document.placements:
        mapping.setdefault(placed.source_element_id, [])
        if placed.page not in mapping[placed.source_element_id]:
            mapping[placed.source_element_id].append(placed.page)
    return {key: sorted(value) for key, value in mapping.items()}
