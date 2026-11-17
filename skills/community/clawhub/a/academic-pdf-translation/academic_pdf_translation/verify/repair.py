"""内部返修：只修一次，只往安全的方向修。

核查查出问题之后，最容易走上的两条歪路是：

1. **反复重试。** 每轮都改一点，每轮都重跑核查，直到报告变绿。跑够多轮，
   任何检查都能被磨过去，而产出未必变好。所以这里硬性只修一轮：
   第二次调用直接拒绝，把剩下的问题交给人。
2. **改判据而不是改产出。** 阈值降一点、白名单宽一点、这个检查先跳过——
   报告立刻好看了，读者拿到的 PDF 一个字没变。所以这里有一张明令禁止的
   动作表，出现即抛错。

允许的动作只有一类：**降级**。重建不了就保留原文区域，区域也保不住就保留
整张原文页。降级不好看，但它不会让读者拿到一份消失了图的 PDF。

还有一类问题根本不该自动修——译文重复、定位不唯一、证据不足。它们需要
判断，不是需要重试。这些走 ``manual``，写清楚为什么机器不碰。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.planning.mode_policy import (
    FALLBACK_PRESERVE_ELEMENT_REGION,
    FALLBACK_PRESERVE_FULL_PAGE,
)
from academic_pdf_translation.verify.candidate_mapping import (
    METHOD_DRAWING_BOUND,
    METHOD_NO_EVIDENCE,
    CandidateMapping,
)
from academic_pdf_translation.verify.structural_audit import StructuralAudit

SCHEMA_VERSION = "1.0"

#: 内部自动返修最多几轮。跑够多轮，任何检查都能被磨过去。
MAX_REPAIR_ROUNDS = 1

ACTION_PRESERVE_REGION = FALLBACK_PRESERVE_ELEMENT_REGION
ACTION_PRESERVE_FULL_PAGE = FALLBACK_PRESERVE_FULL_PAGE
ACTION_KEEP_CAPTION_WITH_TARGET = "keep-caption-with-target"
ACTION_RECOMPOSE_ORDER = "recompose-reading-order"

#: 允许的返修动作。全是"降级"或"重排"，没有一个动的是判据。
ALLOWED_ACTIONS = frozenset(
    {
        ACTION_PRESERVE_REGION,
        ACTION_PRESERVE_FULL_PAGE,
        ACTION_KEEP_CAPTION_WITH_TARGET,
        ACTION_RECOMPOSE_ORDER,
    }
)

#: 明令禁止的"修法"。它们让报告变好看，不让产出变好。
FORBIDDEN_ACTIONS = frozenset(
    {
        "lower-threshold",
        "widen-whitelist",
        "skip-check",
        "drop-element",
        "relax-qa",
        "mark-complete",
    }
)

REASON_ALREADY_REPAIRED = "内部返修已经用掉唯一一轮，剩下的问题交给人"

#: 这些元素类型丢了，可以直接退到"保留原文区域"。
REGION_REPAIRABLE_TYPES = frozenset(
    {
        "vector-figure",
        "raster-figure",
        "chart",
        "screenshot",
        "table",
        "display-formula",
    }
)


class RepairError(RuntimeError):
    """返修计划非法。"""


@dataclass
class RepairAction:
    """一条返修动作。"""

    element_id: str
    action: str
    signal: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ManualItem:
    """机器不碰、交给人的一条。"""

    element_id: str
    signal: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RepairPlan:
    """一轮返修的计划。"""

    schema_version: str = SCHEMA_VERSION
    round_index: int = 0
    actions: list[RepairAction] = field(default_factory=list)
    manual: list[ManualItem] = field(default_factory=list)
    refused: str = ""

    @property
    def allowed(self) -> bool:
        return not self.refused

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "round_index": self.round_index,
            "allowed": self.allowed,
            "refused": self.refused,
            "action_count": len(self.actions),
            "manual_count": len(self.manual),
            "actions": [item.as_dict() for item in self.actions],
            "manual": [item.as_dict() for item in self.manual],
        }


@dataclass
class RepairOutcome:
    """返修前后的对比。"""

    fixed: list[str] = field(default_factory=list)
    still_broken: list[str] = field(default_factory=list)
    regressions: list[str] = field(default_factory=list)
    before_missing: int = 0
    after_missing: int = 0

    @property
    def improved(self) -> bool:
        """修好了东西，而且没修坏别的。"""

        return bool(self.fixed) and not self.regressions

    @property
    def verdict(self) -> str:
        if self.regressions:
            return "返修引入了新问题"
        if not self.fixed:
            return "返修没有修好任何一条"
        if self.still_broken:
            return "部分修好，剩下的交给人"
        return "全部修好"

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["improved"] = self.improved
        data["verdict"] = self.verdict
        return data


def validate_action(action: str) -> None:
    """挡住"改判据"那一类动作。出现即抛错，没有开关可以放行。"""

    if action in FORBIDDEN_ACTIONS:
        raise RepairError(
            f"返修动作 {action!r} 改的是判据不是产出，禁止使用"
        )
    if action not in ALLOWED_ACTIONS:
        raise RepairError(f"返修动作 {action!r} 不在允许清单里")


def fallback_levels_by_element(
    render_plan: dict[str, Any] | None,
) -> dict[str, list[str]]:
    """从渲染计划取出每个元素的降级链。"""

    levels: dict[str, list[str]] = {}
    for entry in (render_plan or {}).get("elements", []):
        if not isinstance(entry, dict):
            continue
        element_id = str(entry.get("element_id") or "")
        chain = entry.get("fallback_levels")
        if element_id and isinstance(chain, list):
            levels[element_id] = [str(value) for value in chain]
    return levels


def plan_repair(
    mapping: CandidateMapping,
    audit: StructuralAudit,
    *,
    round_index: int = 0,
    max_rounds: int = MAX_REPAIR_ROUNDS,
    fallback_levels: dict[str, list[str]] | None = None,
) -> RepairPlan:
    """从核查结果算出这一轮该修什么。

    ``round_index`` 是**已经修过的轮数**。它达到上限就直接拒绝——
    不是少修几条，是一条都不修，把问题原样交给人。

    ``fallback_levels`` 是每个元素的降级链。发一个链上没有的动作，
    重算渲染计划时必然被拒，整轮返修白跑一遍还把候选卡在 BLOCKED。
    落不进计划的动作一律改成交给人。
    """

    if round_index >= max_rounds:
        return RepairPlan(
            round_index=round_index, refused=REASON_ALREADY_REPAIRED
        )

    actions: list[RepairAction] = []
    manual: list[ManualItem] = []
    seen: set[tuple[str, str]] = set()

    def add_action(element_id: str, action: str, signal: str, reason: str) -> None:
        validate_action(action)
        key = (element_id, action)
        if key in seen:
            return
        seen.add(key)
        # 只有降级类动作要落进渲染计划；图题绑定和重排不走降级链。
        chain = (fallback_levels or {}).get(element_id)
        if (
            action in {ACTION_PRESERVE_REGION, ACTION_PRESERVE_FULL_PAGE}
            and chain is not None
            and action not in chain
        ):
            manual.append(
                ManualItem(
                    element_id=element_id,
                    signal=signal,
                    reason=(
                        f"{reason}；但 {action} 不在它的降级链 {chain} 里，"
                        "机器落不进渲染计划，交给人"
                    ),
                )
            )
            return
        actions.append(
            RepairAction(
                element_id=element_id,
                action=action,
                signal=signal,
                reason=reason,
            )
        )

    for item in mapping.locations:
        if item.method == METHOD_NO_EVIDENCE and item.required:
            manual.append(
                ManualItem(
                    element_id=item.element_id,
                    signal="required-without-evidence",
                    reason=(
                        "定位不了不等于内容丢了，需要人看一眼原文和候选，"
                        "机器重试多少次都得不出新信息"
                    ),
                )
            )
            continue

        if not item.located and item.required:
            if item.element_type in REGION_REPAIRABLE_TYPES:
                add_action(
                    item.element_id,
                    ACTION_PRESERVE_REGION,
                    "element-missing",
                    f"{item.element_type} 整块没搬过来，退到保留原文区域",
                )
            else:
                add_action(
                    item.element_id,
                    ACTION_PRESERVE_REGION,
                    "element-missing",
                    "文字内容没有出现在候选里，退到保留原文区域，"
                    "宁可留英文也不丢内容",
                )
            continue

        if item.geometry_ok is False:
            # 文字锚点在、几何不在，说明"按主策略重建"这条路已经走过并失败了。
            # 区域保留是下一级，不是重试同一级。
            add_action(
                item.element_id,
                ACTION_PRESERVE_REGION,
                "geometry-gap",
                f"原文 {item.source_drawing_count} 个绘图对象只搬过来 "
                f"{item.candidate_drawing_count} 个，退到保留原文区域",
            )
            continue

        if item.located and item.method == METHOD_DRAWING_BOUND:
            add_action(
                item.element_id,
                ACTION_PRESERVE_REGION,
                "drawing-bound-only",
                "只有绘图对象数量下界，证明不了它在，退到保留原文区域",
            )
            continue

        if item.ambiguous:
            manual.append(
                ManualItem(
                    element_id=item.element_id,
                    signal="ambiguous-location",
                    reason=(
                        f"同时疑似命中第 {item.candidate_pages} 页，"
                        "到底是重复排了还是探针太短，需要人判断"
                    ),
                )
            )

    for split in audit.caption_splits:
        add_action(
            split.caption_id,
            ACTION_KEEP_CAPTION_WITH_TARGET,
            "caption-split",
            f"与 {split.target_id} 绑成一组，整组同页；放不下就整组换页",
        )

    if audit.inversion_ratio > 0 and any(
        "顺序乱了" in problem for problem in audit.problems
    ):
        # 重排目前没有自动执行路径。发出一个执行不了的动作，
        # 流程会空转一轮重建再报"毫无变化"——不如直接交给人。
        manual.append(
            ManualItem(
                element_id="",
                signal="order-inversion",
                reason=(
                    f"逆序对占比 {audit.inversion_ratio:.4f}，"
                    "自动重排暂无执行路径，需人工确认阅读顺序"
                ),
            )
        )

    return RepairPlan(round_index=round_index, actions=actions, manual=manual)


def escalate(action: str) -> str | None:
    """一条返修动作失败之后还能往哪退。

    保留区域之后是保留整张原文页；再往后没有了——那是最后一级，
    退无可退时应当如实报失败，不是绕回去重试。
    """

    if action == ACTION_PRESERVE_REGION:
        return ACTION_PRESERVE_FULL_PAGE
    return None


def compare_rounds(
    before: CandidateMapping, after: CandidateMapping
) -> RepairOutcome:
    """返修前后对比。修好了什么、还剩什么、有没有修坏别的。"""

    before_broken = {item.element_id for item in before.missing_required}
    after_broken = {item.element_id for item in after.missing_required}
    return RepairOutcome(
        fixed=sorted(before_broken - after_broken),
        still_broken=sorted(before_broken & after_broken),
        regressions=sorted(after_broken - before_broken),
        before_missing=len(before_broken),
        after_missing=len(after_broken),
    )


def format_plan(plan: RepairPlan) -> str:
    """给人看的一页纸。"""

    if not plan.allowed:
        return f"不再返修: {plan.refused}"
    if not plan.actions and not plan.manual:
        return "没有需要返修的地方。"
    lines = [f"返修第 {plan.round_index + 1} 轮（上限 {MAX_REPAIR_ROUNDS} 轮）:"]
    for item in plan.actions:
        target = item.element_id or "（全文）"
        lines.append(f"  {target} -> {item.action}: {item.reason}")
    if plan.manual:
        lines.append("")
        lines.append(f"交给人处理 {len(plan.manual)} 条:")
        for item in plan.manual:
            lines.append(f"  {item.element_id}（{item.signal}）: {item.reason}")
    return "\n".join(lines)
