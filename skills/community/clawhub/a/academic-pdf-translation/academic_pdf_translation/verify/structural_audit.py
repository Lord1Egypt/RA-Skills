"""结构对账：把原文的结构和候选的结构摆在一起数。

阶段 9 回答了"每个元素落在哪一页"。这里回答下一个问题：
**合起来看，这份候选还是原来那篇论文吗？**

四件事分开数，因为它们坏起来的样子完全不同：

1. 逐类型清点。公式少了三条、图题少了两条，单看某一条都像小事，
   按类型一列就藏不住了。
2. 阅读顺序。元素都在，顺序乱了，读者一样读不下去——arXiv 版本戳插进
   引言中间就是这种。这里数逆序对，不是"看着差不多"。
3. 图题跟不跟着图。图在第 4 页、图题在第 5 页，等于两样东西都废了。
4. 页数增长。中文比英文长，涨一点正常；涨到一倍多，说明分页失控了。

结论是**数出来的**：必需元素有缺、或者任何一项硬指标越界，就是不通过。
没有"大体上还行"这个档。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import normalize_bbox
from academic_pdf_translation.verify.candidate_mapping import (
    CandidateMapping,
    ElementLocation,
)

SCHEMA_VERSION = "1.0"

#: 页数相对原文的增长上限。中文比英文长，涨一点正常。
MAX_PAGE_GROWTH = 1.60
#: 阅读顺序逆序对占比上限。完全乱序是 0.5，这里留的余量已经很宽。
MAX_INVERSION_RATIO = 0.05


class StructuralAuditError(RuntimeError):
    """结构对账失败。"""


@dataclass
class TypeTally:
    """一个元素类型的清点结果。"""

    element_type: str
    source_count: int
    located_count: int
    required_count: int
    missing_required: int

    @property
    def coverage(self) -> float:
        if self.source_count <= 0:
            return 1.0
        return round(self.located_count / self.source_count, 4)

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["coverage"] = self.coverage
        return data


@dataclass
class OrderInversion:
    """一对顺序颠倒的元素。"""

    earlier_in_source: str
    later_in_source: str
    earlier_candidate_page: int
    later_candidate_page: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CaptionSplit:
    """图题（或表题）和它的图表被分到了两页。"""

    caption_id: str
    target_id: str
    caption_pages: list[int]
    target_pages: list[int]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StructuralAudit:
    """一次结构对账的完整结果。"""

    schema_version: str = SCHEMA_VERSION
    source_pages: int = 0
    candidate_pages: int = 0
    tallies: list[TypeTally] = field(default_factory=list)
    #: 只保留前若干条样本给人看。
    order_inversions: list[OrderInversion] = field(default_factory=list)
    #: 逆序对的全数。占比用它算，不用样本条数。
    inversion_count: int = 0
    caption_splits: list[CaptionSplit] = field(default_factory=list)
    comparable_pairs: int = 0
    problems: list[str] = field(default_factory=list)

    @property
    def page_growth(self) -> float:
        if self.source_pages <= 0:
            return 0.0
        return round(self.candidate_pages / self.source_pages, 4)

    @property
    def inversion_ratio(self) -> float:
        if self.comparable_pairs <= 0:
            return 0.0
        return round(self.inversion_count / self.comparable_pairs, 4)

    @property
    def missing_required(self) -> int:
        return sum(item.missing_required for item in self.tallies)

    @property
    def passed(self) -> bool:
        """通过与否是数出来的，没有"大体上还行"这一档。"""

        return not self.problems

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source_pages": self.source_pages,
            "candidate_pages": self.candidate_pages,
            "page_growth": self.page_growth,
            "inversion_ratio": self.inversion_ratio,
            "inversion_count": self.inversion_count,
            "comparable_pairs": self.comparable_pairs,
            "missing_required": self.missing_required,
            "passed": self.passed,
            "tallies": [item.as_dict() for item in self.tallies],
            "order_inversions": [
                item.as_dict() for item in self.order_inversions
            ],
            "caption_splits": [item.as_dict() for item in self.caption_splits],
            "problems": list(self.problems),
        }


def tally_by_type(mapping: CandidateMapping) -> list[TypeTally]:
    """逐类型清点。单看一条像小事，按类型一列就藏不住。"""

    grouped: dict[str, list[ElementLocation]] = {}
    for item in mapping.locations:
        grouped.setdefault(item.element_type, []).append(item)
    return [
        TypeTally(
            element_type=element_type,
            source_count=len(items),
            located_count=sum(1 for item in items if item.located),
            required_count=sum(1 for item in items if item.required),
            missing_required=sum(
                1 for item in items if item.required and not item.located
            ),
        )
        for element_type in sorted(grouped)
        for items in [grouped[element_type]]
    ]


def _source_key(element: dict[str, Any]) -> tuple[float, float, float]:
    box = normalize_bbox(element.get("bbox")) or (0.0, 0.0, 0.0, 0.0)
    return (float(element.get("page") or 0), box[1], box[0])


def _candidate_key(item: ElementLocation) -> tuple[float, float | None]:
    """元素在候选里的位置。量不到纵坐标时返回 None，不拿 0 顶替。

    拿 0 顶替等于宣称"它在这一页最上面"，而那是编出来的。同一页里
    只要有一个元素量不到坐标，这一对就谈不上谁先谁后。
    """

    box = normalize_bbox(item.candidate_bbox)
    return (float(item.candidate_pages[0]), box[1] if box else None)


def reading_order_inversions(
    mapping: CandidateMapping,
    elements: list[dict[str, Any]],
    *,
    limit: int = 40,
) -> tuple[list[OrderInversion], int, int]:
    """数逆序对。

    只比**定位唯一**的元素：落点说不清的两个元素之间，谈不上谁先谁后。

    同一页内两个元素，只要有一个量不到纵坐标，这一对就跳过，
    既不算逆序也不进分母——宁可少数几对，也不要拿编出来的顺序去指控排版。
    页码不同的一对，按页码比就够了，不需要坐标。
    """

    by_id = {str(element.get("id") or ""): element for element in elements}
    ordered = [
        item
        for item in mapping.locations
        if item.located and not item.ambiguous and item.element_id in by_id
    ]
    ordered.sort(key=lambda item: _source_key(by_id[item.element_id]))

    # 样本只留前 limit 条给人看，计数全数——占比要用全数算，
    # 拿截断后的条数去除总对数，得出的比例会凭空变小。
    examples: list[OrderInversion] = []
    total = 0
    comparable = 0
    for index, earlier in enumerate(ordered):
        for later in ordered[index + 1:]:
            earlier_page, earlier_y = _candidate_key(earlier)
            later_page, later_y = _candidate_key(later)
            if earlier_page == later_page:
                if earlier_y is None or later_y is None or earlier_y == later_y:
                    continue
                comparable += 1
                if earlier_y <= later_y:
                    continue
            else:
                comparable += 1
                if earlier_page <= later_page:
                    continue
            total += 1
            if len(examples) < limit:
                examples.append(
                    OrderInversion(
                        earlier_in_source=earlier.element_id,
                        later_in_source=later.element_id,
                        earlier_candidate_page=earlier.candidate_pages[0],
                        later_candidate_page=later.candidate_pages[0],
                    )
                )
    return (examples, total, comparable)


def caption_splits(
    mapping: CandidateMapping, elements: list[dict[str, Any]]
) -> list[CaptionSplit]:
    """图题、表题必须和它说明的东西在同一页。"""

    by_id = {item.element_id: item for item in mapping.locations}
    splits: list[CaptionSplit] = []
    for element in elements:
        caption_id = str(element.get("id") or "")
        targets = (element.get("relations") or {}).get("captions-for") or []
        caption = by_id.get(caption_id)
        if caption is None or not caption.located:
            continue
        for target_id in targets:
            target = by_id.get(str(target_id))
            if target is None or not target.located:
                continue
            if set(caption.candidate_pages) & set(target.candidate_pages):
                continue
            splits.append(
                CaptionSplit(
                    caption_id=caption_id,
                    target_id=str(target_id),
                    caption_pages=list(caption.candidate_pages),
                    target_pages=list(target.candidate_pages),
                )
            )
    return splits


def audit_structure(
    mapping: CandidateMapping,
    elements: list[dict[str, Any]],
    *,
    max_page_growth: float = MAX_PAGE_GROWTH,
    max_inversion_ratio: float = MAX_INVERSION_RATIO,
) -> StructuralAudit:
    """把四项对账一次做完，结论由计数给出。"""

    if not elements:
        raise StructuralAuditError("元素清单为空，无法对账")
    if len(mapping.locations) != len(elements):
        raise StructuralAuditError(
            f"映射有 {len(mapping.locations)} 条，元素清单有 {len(elements)} 条，"
            "两者必须一一对应"
        )

    inversions, inversion_count, comparable = reading_order_inversions(
        mapping, elements
    )
    audit = StructuralAudit(
        source_pages=mapping.source_pages,
        candidate_pages=mapping.candidate_pages,
        tallies=tally_by_type(mapping),
        order_inversions=inversions,
        inversion_count=inversion_count,
        caption_splits=caption_splits(mapping, elements),
        comparable_pairs=comparable,
    )

    for tally in audit.tallies:
        if tally.missing_required:
            audit.problems.append(
                f"{tally.element_type}: {tally.missing_required}/"
                f"{tally.required_count} 个必需元素在候选里找不到"
            )

    if audit.page_growth > max_page_growth:
        audit.problems.append(
            f"候选 {audit.candidate_pages} 页比原文 {audit.source_pages} 页涨了 "
            f"{audit.page_growth:.2f} 倍，超过 {max_page_growth:.2f}，分页失控"
        )

    if audit.inversion_ratio > max_inversion_ratio:
        audit.problems.append(
            f"阅读顺序逆序对占比 {audit.inversion_ratio:.4f} 超过 "
            f"{max_inversion_ratio:.4f}（{audit.inversion_count}/"
            f"{audit.comparable_pairs} 对），元素都在但顺序乱了"
        )

    for split in audit.caption_splits:
        audit.problems.append(
            f"{split.caption_id} 在候选第 {split.caption_pages} 页，"
            f"它说明的 {split.target_id} 在第 {split.target_pages} 页，必须同页"
        )

    return audit


def format_report(audit: StructuralAudit) -> str:
    """给人看的一页纸。数字全部来自对账结果，不另行加工。"""

    lines = [
        f"结论: {'通过' if audit.passed else '不通过'}",
        f"页数: 原文 {audit.source_pages} -> 候选 {audit.candidate_pages}"
        f"（{audit.page_growth:.2f} 倍）",
        f"阅读顺序: {audit.inversion_count}/{audit.comparable_pairs} 对逆序"
        f"（{audit.inversion_ratio:.4f}）",
        "",
        "逐类型清点:",
    ]
    for tally in audit.tallies:
        lines.append(
            f"  {tally.element_type:20s} 原文 {tally.source_count:3d}  "
            f"命中 {tally.located_count:3d}  覆盖 {tally.coverage:.2f}  "
            f"必需缺失 {tally.missing_required}"
        )
    if audit.problems:
        lines.append("")
        lines.append("问题:")
        lines.extend(f"  - {problem}" for problem in audit.problems)
    return "\n".join(lines)
