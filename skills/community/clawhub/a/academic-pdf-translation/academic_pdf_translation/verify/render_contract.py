"""渲染合同：三份清单按元素 ID 对账，谁也别数条目。

唯一事实来源从此定死：

- ``source_elements.json`` —— 原文里有什么；
- ``render_plan.json`` —— 每个元素怎么处理；
- ``candidate_elements.json`` —— 每个元素最后去了哪里（由候选映射派生）。

通过条件是三条集合关系，缺谁、多谁都不行：

- 必需元素 ⊆ 计划元素（少一个就是漏排）；
- 计划元素 ⊆ 原文元素（多一个就是凭空捏造的假元素）；
- 必需元素 == 已渲染元素 ∪ 合法省略元素。

第二条必须单独查。只查"少了谁"的话，一个只存在于计划、原文里根本
没有的 ID 会一路混进候选清单，还因为"计划里有"而白得一个"有原文来源"
的身份——从此再没有任何一关能认出它是假的。所以"元素有没有来源"
只认原文清单，计划说了不算。

不再用"复杂页载荷数量"做核心判断——同一页可以同时有图、表、公式、
图题、脚注，按页数或旧条目数比对必然错位。``complex_content.json``
降级为自动派生的兼容视图，手写的 ``complete`` 一律不信。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from academic_pdf_translation.verify.candidate_mapping import CandidateMapping

SCHEMA_VERSION = "1.0"

#: 允许的省略理由。目前只有一种：抽取残渣——正文单元的可用文字只剩
#: 单个字体残渣字符，内容已随所在区域整块保留，判不了也不必判。
OMIT_EXTRACTION_RESIDUE = "extraction-residue"
LEGAL_OMISSION_CODES = frozenset({OMIT_EXTRACTION_RESIDUE})

#: 映射层给残渣元素写的证据前缀（见 candidate_mapping 的降级判定）。
_RESIDUE_EVIDENCE_MARK = "抽取残渣"


@dataclass
class RenderContract:
    """一次按元素 ID 的对账结果。"""

    schema_version: str = SCHEMA_VERSION
    #: 原文清单里的**全部**元素，含非必需的。判断"有没有来源"只看它。
    all_source_element_ids: set[str] = field(default_factory=set)
    required_element_ids: set[str] = field(default_factory=set)
    planned_element_ids: set[str] = field(default_factory=set)
    rendered_element_ids: set[str] = field(default_factory=set)
    legal_omitted_element_ids: set[str] = field(default_factory=set)
    problems: list[str] = field(default_factory=list)

    @property
    def unknown_planned_element_ids(self) -> set[str]:
        """计划里有、原文里没有的元素。凭空多出来的处理对象。"""

        return self.planned_element_ids - self.all_source_element_ids

    @property
    def omitted_element_ids(self) -> set[str]:
        return self.required_element_ids - self.rendered_element_ids

    @property
    def illegal_omitted_element_ids(self) -> set[str]:
        return self.omitted_element_ids - self.legal_omitted_element_ids

    @property
    def passed(self) -> bool:
        return not self.problems

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source_count": len(self.all_source_element_ids),
            "required_count": len(self.required_element_ids),
            "planned_count": len(self.planned_element_ids),
            "rendered_count": len(self.rendered_element_ids),
            "omitted_count": len(self.omitted_element_ids),
            "legal_omitted_count": len(self.legal_omitted_element_ids),
            "unknown_planned_count": len(self.unknown_planned_element_ids),
            "all_source_element_ids": sorted(self.all_source_element_ids),
            "required_element_ids": sorted(self.required_element_ids),
            "planned_element_ids": sorted(self.planned_element_ids),
            "rendered_element_ids": sorted(self.rendered_element_ids),
            "omitted_element_ids": sorted(self.omitted_element_ids),
            "legal_omitted_element_ids": sorted(
                self.legal_omitted_element_ids
            ),
            "unknown_planned_element_ids": sorted(
                self.unknown_planned_element_ids
            ),
            "passed": self.passed,
            "problems": list(self.problems),
        }


def _ids_with_duplicates(
    records: list[Any], key: str
) -> tuple[set[str], list[str]]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        value = str(record.get(key) or "")
        if not value:
            continue
        if value in seen:
            duplicates.append(value)
        seen.add(value)
    return seen, duplicates


def _source_ids(
    source_elements: dict[str, Any],
) -> tuple[set[str], set[str], list[str]]:
    """原文清单拆成三份：全部 ID、必需 ID、重复的 ID。

    「全部」和「必需」必须分开。必需 ID 回答"谁一定要有计划"，
    全部 ID 回答"谁在原文里真的存在"——后者才是元素身份的来源。
    """

    records = [
        element
        for element in source_elements.get("elements", [])
        if isinstance(element, dict)
    ]
    all_ids, duplicates = _ids_with_duplicates(records, "id")
    required, _ = _ids_with_duplicates(
        [record for record in records if record.get("required", True)], "id"
    )
    return all_ids, required, duplicates


def planning_issues(
    source_elements: dict[str, Any], render_plan: dict[str, Any]
) -> list[dict[str, Any]]:
    """构建前就能查的部分：必需元素每个都要有计划，计划里也不许有假元素。"""

    issues: list[dict[str, Any]] = []
    all_source, required, source_dups = _source_ids(source_elements)
    planned, plan_dups = _ids_with_duplicates(
        render_plan.get("elements", []), "element_id"
    )
    for duplicate in sorted(set(source_dups)):
        issues.append(
            {
                "code": "ELEMENT_ID_DUPLICATED_IN_SOURCE",
                "element_id": duplicate,
            }
        )
    for duplicate in sorted(set(plan_dups)):
        issues.append(
            {
                "code": "ELEMENT_ID_DUPLICATED_IN_PLAN",
                "element_id": duplicate,
            }
        )
    unplanned = required - planned
    if unplanned:
        issues.append(
            {
                "code": "REQUIRED_ELEMENTS_WITHOUT_PLAN",
                "element_ids": sorted(unplanned),
                "message": "这些必需元素没有任何处理计划，禁止渲染",
            }
        )
    unknown = planned - all_source
    if unknown:
        issues.append(
            {
                "code": "PLAN_ELEMENTS_WITHOUT_SOURCE",
                "element_ids": sorted(unknown),
                "message": "这些元素只存在于渲染计划，原文里查无此人，禁止渲染",
            }
        )
    return issues


def derive_candidate_elements(mapping: CandidateMapping) -> dict[str, Any]:
    """从候选映射派生"每个元素最后去了哪里"的视图。

    这是**派生视图**：它的每一行都能在映射证据里找到出处，
    没有任何字段接受手写。
    """

    elements: list[dict[str, Any]] = []
    for item in mapping.locations:
        record: dict[str, Any] = {
            "id": item.element_id,
            "type": item.element_type,
            "located": item.located,
            "required": item.required,
            "pages": list(item.candidate_pages),
            "method": item.method,
        }
        if not item.located and _RESIDUE_EVIDENCE_MARK in item.evidence:
            record["omit_reason"] = OMIT_EXTRACTION_RESIDUE
        elements.append(record)
    return {
        "schema_version": SCHEMA_VERSION,
        "derived_from": "candidate-mapping",
        "elements": elements,
    }


def contract_from_documents(
    source_elements: dict[str, Any],
    render_plan: dict[str, Any],
    candidate_elements: dict[str, Any] | None = None,
) -> RenderContract:
    """三份清单 → 一份合同。``candidate_elements`` 缺席时只查计划侧。"""

    contract = RenderContract()
    all_source, required, source_dups = _source_ids(source_elements)
    planned, plan_dups = _ids_with_duplicates(
        render_plan.get("elements", []), "element_id"
    )
    contract.all_source_element_ids = all_source
    contract.required_element_ids = required
    contract.planned_element_ids = planned

    for duplicate in sorted(set(source_dups)):
        contract.problems.append(f"元素 {duplicate} 在原文清单里出现了两次")
    for duplicate in sorted(set(plan_dups)):
        contract.problems.append(f"元素 {duplicate} 在渲染计划里出现了两次")
    unplanned = required - planned
    if unplanned:
        contract.problems.append(
            "必需元素没有处理计划: " + "、".join(sorted(unplanned)[:8])
            + (f" 等 {len(unplanned)} 个" if len(unplanned) > 8 else "")
        )
    unknown_planned = contract.unknown_planned_element_ids
    if unknown_planned:
        contract.problems.append(
            "渲染计划里有原文清单查无此人的元素: "
            + "、".join(sorted(unknown_planned)[:8])
            + (
                f" 等 {len(unknown_planned)} 个"
                if len(unknown_planned) > 8
                else ""
            )
        )

    if candidate_elements is None:
        return contract

    records = [
        record
        for record in candidate_elements.get("elements", [])
        if isinstance(record, dict)
    ]
    rendered, candidate_dups = _ids_with_duplicates(
        [record for record in records if record.get("located")], "id"
    )
    contract.rendered_element_ids = rendered
    for duplicate in sorted(set(candidate_dups)):
        contract.problems.append(
            f"元素 {duplicate} 在候选清单里被计了两次——同一个元素不能既算这里又算那里"
        )
    # 「有没有原文来源」只认原文清单。出现在计划里不算来源——
    # 否则一个假元素只要混进计划，就能永远逃过这一关。
    unsourced = {
        str(record.get("id") or "") for record in records
    } - all_source - {""}
    if unsourced:
        contract.problems.append(
            "候选清单里有原文清单查无此人的元素: "
            + "、".join(sorted(unsourced)[:8])
        )
    contract.legal_omitted_element_ids = {
        str(record.get("id") or "")
        for record in records
        if not record.get("located")
        and str(record.get("omit_reason") or "") in LEGAL_OMISSION_CODES
    } & required
    illegal = contract.illegal_omitted_element_ids
    if illegal:
        contract.problems.append(
            "必需元素既没渲染也没有合法省略理由: "
            + "、".join(sorted(illegal)[:8])
            + (f" 等 {len(illegal)} 个" if len(illegal) > 8 else "")
        )
    return contract


def derive_complex_view(
    complex_content: dict[str, Any], render_plan_sha256: str
) -> dict[str, Any]:
    """给复杂内容盖上"派生视图"的戳。

    从此 ``complex_content.json`` 由渲染计划自动生成，戳里的计划哈希
    说明它派生自哪一版计划；哈希对不上就是旧视图，不作数。
    """

    view = dict(complex_content)
    view["derived_from"] = {
        "source": "render_plan",
        "render_plan_sha256": render_plan_sha256,
    }
    return view


def complex_view_is_current(
    complex_content: dict[str, Any], render_plan_sha256: str
) -> bool:
    marker = complex_content.get("derived_from")
    return (
        isinstance(marker, dict)
        and marker.get("source") == "render_plan"
        and marker.get("render_plan_sha256") == render_plan_sha256
    )
