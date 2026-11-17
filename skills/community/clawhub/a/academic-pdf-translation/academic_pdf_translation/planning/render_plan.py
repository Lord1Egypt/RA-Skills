"""渲染计划：给原文里的每一个必需元素安排一个去处。

不允许出现"原文有这个元素，但计划里没有它"。这条是硬失败，
因为图 1 消失、表格压平这类问题的源头就在这里——以前根本没有这一步。

`complete` 由程序算：必需元素数 == 已安排数 + 合法省略数。
AI 不得手工填写。
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from academic_pdf_translation.contracts.enums import (
    ElementType,
    QualityMode,
)
from academic_pdf_translation.contracts.models import (
    SourceElement,
    SourceElementInventory,
)
from academic_pdf_translation.planning.fallback_policy import (
    FallbackChain,
    build_chain,
)
from academic_pdf_translation.planning.mode_policy import (
    FALLBACK_PRESERVE_ELEMENT_REGION,
    FALLBACK_PRESERVE_FULL_PAGE,
    ModePolicy,
    policy_for,
)

PLAN_FILE_NAME = "render_plan.json"
SCHEMA_VERSION = "2.0"

# --- 策略名（渲染器认这些名字）---------------------------------------------

STRATEGY_TRANSLATE_AND_REFLOW = "translate-and-reflow"
STRATEGY_TABLE_REBUILD = "structured-table-rebuild"
STRATEGY_TABLE_PRESERVE = "preserve-table-region-with-translation-key"
STRATEGY_FORMULA_PRESERVE = "preserve-formula-region"
STRATEGY_VECTOR_OVERLAY = "preserve-geometry-with-label-overlay"
STRATEGY_VECTOR_LEGEND = "preserve-geometry-with-numbered-legend"
STRATEGY_IMAGE_PRESERVE = "preserve-original-image"
STRATEGY_CAPTION_KEEP_TOGETHER = "translate-caption-and-keep-with-figure"
STRATEGY_FOOTNOTE = "translate-and-render-as-footnote"
STRATEGY_REFERENCE_NORMALIZE = "preserve-and-normalize-line-breaks"
STRATEGY_OMIT = "omit-nonsemantic"
#: 降级链上的两级。它们也必须有渲染器——否则降级链就只是写着好看，
#: 真降下来的时候没人能画。
STRATEGY_PRESERVE_ELEMENT_REGION = FALLBACK_PRESERVE_ELEMENT_REGION
STRATEGY_PRESERVE_FULL_PAGE = FALLBACK_PRESERVE_FULL_PAGE

#: 渲染器名。一个策略只归一个渲染器管。
RENDERER_TEXT = "text"
RENDERER_TABLE = "table"
RENDERER_FIGURE = "figure"
RENDERER_FORMULA = "formula"
RENDERER_FOOTNOTE = "footnote"
RENDERER_REFERENCE = "reference"
RENDERER_PRESERVED_REGION = "preserved-region"
RENDERER_NONE = "none"

STRATEGY_RENDERERS = {
    STRATEGY_TRANSLATE_AND_REFLOW: RENDERER_TEXT,
    STRATEGY_CAPTION_KEEP_TOGETHER: RENDERER_TEXT,
    STRATEGY_TABLE_REBUILD: RENDERER_TABLE,
    STRATEGY_TABLE_PRESERVE: RENDERER_PRESERVED_REGION,
    STRATEGY_FORMULA_PRESERVE: RENDERER_FORMULA,
    STRATEGY_VECTOR_OVERLAY: RENDERER_FIGURE,
    STRATEGY_VECTOR_LEGEND: RENDERER_FIGURE,
    STRATEGY_IMAGE_PRESERVE: RENDERER_FIGURE,
    STRATEGY_FOOTNOTE: RENDERER_FOOTNOTE,
    STRATEGY_REFERENCE_NORMALIZE: RENDERER_REFERENCE,
    STRATEGY_OMIT: RENDERER_NONE,
    STRATEGY_PRESERVE_ELEMENT_REGION: RENDERER_PRESERVED_REGION,
    STRATEGY_PRESERVE_FULL_PAGE: RENDERER_PRESERVED_REGION,
}


class RenderPlanError(ValueError):
    """计划本身不成立。"""


@dataclass
class PlannedElement:
    """一个元素的处理方案。"""

    element_id: str
    element_type: str
    page: int
    strategy: str
    renderer: str
    fallback: str | None
    fallback_levels: list[str]
    reason: str
    status: str = "ready"
    risk_flags: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _table_strategy(
    element: SourceElement,
    policy: ModePolicy,
) -> tuple[str, str]:
    """表格：认得准才重建，否则保留原表。绝不压平成段落。"""

    columns = int(element.detail.get("estimated_columns") or 0)
    rows = int(element.detail.get("estimated_rows") or 0)
    unresolved = any(
        risk.code == "table-columns-unresolved" for risk in element.risk_flags
    )
    reliable = (
        element.confidence >= policy.table_confidence_floor
        and columns >= 2
        and rows >= 2
        and not unresolved
    )
    if reliable:
        return (
            STRATEGY_TABLE_REBUILD,
            f"网格置信度 {element.confidence:.2f}、{rows} 行 {columns} 列已确定",
        )
    return (
        STRATEGY_TABLE_PRESERVE,
        "行列关系无法可靠确定，保留原表区域并附中文表题与列头翻译键；"
        "宁可保守，也不把表格压成段落",
    )


def _vector_strategy(
    element: SourceElement,
    policy: ModePolicy,
) -> tuple[str, str]:
    """矢量图：几何结构一律保留，只处理文字标签。"""

    labels = element.relations.get("embedded-label", [])
    mapping_confidence = float(
        element.detail.get("label_mapping_confidence", 1.0 if labels else 0.0)
    )
    if labels and mapping_confidence >= policy.label_mapping_confidence_floor:
        return (
            STRATEGY_VECTOR_OVERLAY,
            f"保留几何结构，{len(labels)} 个图内标签一对一覆盖中文",
        )
    if labels:
        return (
            STRATEGY_VECTOR_LEGEND,
            f"标签映射置信度 {mapping_confidence:.2f} 不足，改用编号图例",
        )
    return (
        STRATEGY_VECTOR_LEGEND,
        "没有可映射的图内标签，保留几何结构并附编号图例",
    )


def plan_element(
    element: SourceElement,
    policy: ModePolicy,
    *,
    forced_strategy: str | None = None,
) -> PlannedElement:
    """给一个元素定策略。

    ``forced_strategy`` 是内部返修用的：核查发现某个元素没搬过来，返修就把
    它按降级链往下压一级。它**只能往下压**——往回调等于让失败过的策略再试
    一次，那不是返修，那是重试。
    """

    element_type = element.type
    risks = [risk.code for risk in element.risk_flags]

    if element.detail.get("omitted"):
        code = str(element.detail.get("omit_code") or "")
        if not code:
            raise RenderPlanError(
                f"{element.id} 标记为省略但没有 omit_code"
            )
        return PlannedElement(
            element_id=element.id,
            element_type=element_type.value,
            page=element.page,
            strategy=STRATEGY_OMIT,
            renderer=RENDERER_NONE,
            fallback=None,
            fallback_levels=[STRATEGY_OMIT],
            reason=f"按固定代码省略: {code}",
            status="omitted",
            risk_flags=risks,
        )

    if element_type is ElementType.TABLE:
        strategy, reason = _table_strategy(element, policy)
    elif element_type in {ElementType.VECTOR_FIGURE, ElementType.CHART}:
        strategy, reason = _vector_strategy(element, policy)
    elif element_type in {
        ElementType.RASTER_FIGURE,
        ElementType.SCREENSHOT,
    }:
        strategy, reason = (
            STRATEGY_IMAGE_PRESERVE,
            "位图原样保留，不放大、不替换",
        )
    elif element_type is ElementType.DISPLAY_FORMULA:
        strategy, reason = (
            STRATEGY_FORMULA_PRESERVE,
            "保留原公式区域，只翻译公式周围说明；不重新输入数学结构",
        )
    elif element_type is ElementType.CAPTION:
        strategy, reason = (
            STRATEGY_CAPTION_KEEP_TOGETHER,
            "翻译图题并与主体绑成同页组",
        )
    elif element_type is ElementType.FOOTNOTE:
        strategy, reason = (
            STRATEGY_FOOTNOTE,
            "翻译后排进页脚区，不进正文流",
        )
    elif element_type in {
        ElementType.REFERENCE_ENTRY,
        ElementType.REFERENCE_HEADING,
    }:
        strategy, reason = (
            STRATEGY_REFERENCE_NORMALIZE,
            "题录保留原文，修复换行断词与被切碎的 URL",
        )
    elif element_type in {
        ElementType.HEADER,
        ElementType.FOOTER,
        ElementType.PAGE_NUMBER,
        ElementType.WATERMARK,
    }:
        strategy, reason = (
            STRATEGY_OMIT,
            "页面家具由排版器统一生成，不搬运原文的",
        )
    else:
        strategy, reason = (
            STRATEGY_TRANSLATE_AND_REFLOW,
            "普通文本翻译后重新流排",
        )

    if strategy in policy.forbidden_strategies:
        raise RenderPlanError(
            f"{element.id} 的策略 {strategy} 在 "
            f"{policy.quality_mode.value} 档被禁止"
        )

    chain: FallbackChain = build_chain(
        element.id, element_type, strategy, policy
    )
    if forced_strategy:
        strategy, reason = _apply_forced_strategy(
            element.id, strategy, forced_strategy, chain
        )
    return PlannedElement(
        element_id=element.id,
        element_type=element_type.value,
        page=element.page,
        strategy=strategy,
        renderer=STRATEGY_RENDERERS[strategy],
        fallback=chain.next_after(strategy),
        fallback_levels=list(chain.levels),
        reason=reason,
        status="omitted" if strategy == STRATEGY_OMIT else "ready",
        risk_flags=risks,
    )


def _apply_forced_strategy(
    element_id: str,
    strategy: str,
    forced: str,
    chain: FallbackChain,
) -> tuple[str, str]:
    """把返修指定的策略套上去，并挡住"往回调"。"""

    if forced not in chain.levels:
        raise RenderPlanError(
            f"{element_id}: 返修策略 {forced} 不在它的降级链 "
            f"{list(chain.levels)} 里"
        )
    if chain.levels.index(forced) <= chain.levels.index(strategy):
        raise RenderPlanError(
            f"{element_id}: 返修只能降级；{forced} 不比当前的 {strategy} 更保守"
        )
    return (forced, f"返修降级：{strategy} -> {forced}")


@dataclass
class RenderPlan:
    """整篇的渲染计划。"""

    quality_mode: str
    source_sha256: str
    elements: list[PlannedElement] = field(default_factory=list)
    required_elements: int = 0
    planned_elements: int = 0
    omitted_elements: int = 0
    unresolved_elements: int = 0
    problems: list[str] = field(default_factory=list)
    schema_version: str = SCHEMA_VERSION

    @property
    def complete(self) -> bool:
        """由程序计算，AI 不得填写。"""

        return (
            not self.problems
            and self.unresolved_elements == 0
            and self.required_elements
            == self.planned_elements + self.omitted_elements
        )

    def plan_hash(self) -> str:
        payload = json.dumps(
            [item.as_dict() for item in self.elements],
            ensure_ascii=False,
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "quality_mode": self.quality_mode,
            "source_sha256": self.source_sha256,
            "plan_sha256": self.plan_hash(),
            "elements": [item.as_dict() for item in self.elements],
            "completeness": {
                "required_elements": self.required_elements,
                "planned_elements": self.planned_elements,
                "omitted_elements": self.omitted_elements,
                "unresolved_elements": self.unresolved_elements,
                "complete": self.complete,
                "computed_by": "program",
            },
            "problems": list(self.problems),
        }


def build_render_plan(
    inventory: SourceElementInventory,
    quality_mode: QualityMode | str,
    *,
    forced_strategies: dict[str, str] | None = None,
) -> RenderPlan:
    """从元素清单推出渲染计划。

    ``forced_strategies`` 是内部返修的结果：元素 id 到它该降到的策略。
    没有这一项时，计划完全由清单和档位决定，和返修无关。
    """

    policy = policy_for(quality_mode)
    plan = RenderPlan(
        quality_mode=policy.quality_mode.value,
        source_sha256=inventory.source_sha256,
    )
    seen: set[str] = set()
    for element in inventory.elements:
        if element.id in seen:
            plan.problems.append(f"元素 {element.id} 出现了两次")
            continue
        seen.add(element.id)
        try:
            planned = plan_element(
                element,
                policy,
                forced_strategy=(forced_strategies or {}).get(element.id),
            )
        except RenderPlanError as exc:
            plan.problems.append(str(exc))
            continue
        plan.elements.append(planned)

    required_ids = {element.id for element in inventory.required_elements()}
    planned_ids = {
        item.element_id for item in plan.elements if item.status == "ready"
    }
    omitted_ids = {
        item.element_id for item in plan.elements if item.status == "omitted"
    }

    plan.required_elements = len(required_ids)
    plan.planned_elements = len(required_ids & planned_ids)
    plan.omitted_elements = len(required_ids & omitted_ids)
    plan.unresolved_elements = len(inventory.unresolved_elements)

    missing = sorted(required_ids - planned_ids - omitted_ids)
    if missing:
        plan.problems.append(
            "以下必需元素在渲染计划中没有去处: " + ", ".join(missing[:20])
        )
    if plan.required_elements != plan.planned_elements + plan.omitted_elements:
        plan.problems.append(
            f"必需元素 {plan.required_elements} 个，"
            f"已安排 {plan.planned_elements} 个、合法省略 "
            f"{plan.omitted_elements} 个，对不上"
        )
    if plan.unresolved_elements:
        plan.problems.append(
            f"仍有 {plan.unresolved_elements} 个未解决元素，不能进入渲染"
        )
    return plan


#: 这些策略会把译文写进图或表里：图内标签叠中文、表格重建、
#: 保留表区域再附中文翻译键。图表清单的 text_status 只对它们记 translated。
TEXT_TRANSLATING_STRATEGIES = frozenset(
    {
        STRATEGY_VECTOR_OVERLAY,
        STRATEGY_VECTOR_LEGEND,
        STRATEGY_TABLE_REBUILD,
        STRATEGY_TABLE_PRESERVE,
    }
)


def _inventory_policy(planned: PlannedElement | None) -> str:
    """一个视觉元素在图表清单里的策略。

    保留原图就是保留原图：它是**已渲染**的元素，不是被省略的元素，
    也不需要给出"省略理由"。这里让图表清单和渲染合同用同一个口径。
    """

    if planned is None:
        return "preserve-original"
    if planned.status == "omitted":
        return "omit-nonsemantic"
    if planned.strategy in TEXT_TRANSLATING_STRATEGIES:
        return "translate-embedded-text"
    return "preserve-original"


def build_figure_inventory(
    inventory: SourceElementInventory,
    plan: RenderPlan,
    *,
    renderer_version: str = "",
    candidate_sha256: str | None = None,
) -> dict[str, Any]:
    """图表清单改为程序生成。

    `inventory_complete` 不再接受手工输入：它等于
    "必需视觉元素数 == 已安排数 + 合法省略数"。
    """

    by_id = {item.element_id: item for item in plan.elements}
    items: list[dict[str, Any]] = []
    for element in inventory.elements:
        if not element.is_visual:
            continue
        planned = by_id.get(element.id)
        policy = _inventory_policy(planned)
        items.append(
            {
                "id": element.id,
                "page": element.page,
                "element_type": element.type.value,
                # 两个字段必须同口径：只有真的往图里写了译文才是
                # translated，保留原图和省略都是 not-applicable。
                "text_status": (
                    "translated"
                    if policy == "translate-embedded-text"
                    else "not-applicable"
                ),
                "translation_policy": policy,
                "translation_policy_reason": (
                    planned.reason if planned is not None else "尚未安排"
                ),
                "render_strategy": (
                    planned.strategy if planned is not None else None
                ),
            }
        )
    required_visuals = [
        element
        for element in inventory.elements
        if element.is_visual and element.required
    ]
    arranged = sum(
        1
        for element in required_visuals
        if by_id.get(element.id) is not None
        and by_id[element.id].status == "ready"
    )
    omitted = sum(
        1
        for element in required_visuals
        if by_id.get(element.id) is not None
        and by_id[element.id].status == "omitted"
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": "program",
        "inventory_complete": len(required_visuals) == arranged + omitted,
        "required_visual_elements": len(required_visuals),
        "arranged_visual_elements": arranged,
        "omitted_visual_elements": omitted,
        "source_elements_sha256": inventory.cache_key,
        "render_plan_sha256": plan.plan_hash(),
        "renderer_version": renderer_version,
        "candidate_sha256": candidate_sha256,
        "scope_note": (
            "由 source_elements.json 与 render_plan.json 程序派生，"
            "不接受手工填写的 inventory_complete。"
        ),
        "items": items,
    }


def write_plan(job_dir: Path, plan: RenderPlan) -> Path:
    path = Path(job_dir) / PLAN_FILE_NAME
    path.write_text(
        json.dumps(plan.as_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path
