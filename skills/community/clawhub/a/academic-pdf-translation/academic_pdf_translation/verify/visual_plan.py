"""高风险视觉检查：挑出真正值得用眼睛看的那几页。

前两个阶段把能数的都数了。但有一类问题数不出来——字压在图上、
表格线歪了、中文和公式挤成一团。这些只有看才知道。

看又不能全看。八页的论文全看一遍，十篇就是八十页，评审会累到不看。
所以这里做一件事：**把风险信号折成分数，按分数排页，只渲染最值得看的几页，
并且逐页写清楚要看什么。**

风险信号有两个来源。

**异常信号**来自阶段 9 的映射和阶段 10 的对账：元素缺失、几何对象数量
不够、图题跨页、没有证据、定位模糊、顺序倒置。它们回答"有没有出事"。

**基础信号**按内容类型给：表格、行间公式、密集矢量图、带嵌入标签的图、
脚注、走了安全降级的元素、跨页的表格，默认都要进视觉检查。这一类补的是
另一个洞——表格线错位、数字挤到隔壁列、公式被裁掉一角、中文压在图上、
标签遮挡，这些在结构映射全绿时照样会发生。映射说"元素在"，只是说它在，
没说它排得对。快速档最容易在这里出错，恰恰又最不会有人复看。

免检的门开得很小：只有渲染器能拿出非常强的确定性证明才免——行间公式要
同时满足「按原区域整块保留」「裁切边界检测通过（不是
``FORMULA_REGION_UNCERTAIN``）」「像素指纹证明整块内容原样在场」三条。
三条缺一条就照看不误。拿不到这些证据时默认要看，不默认放过。

被预算砍掉的页会原样记在 ``skipped`` 里——悄悄截断会让报告读起来像
"全看过了"。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.render.formula_crop import STATUS_OK
from academic_pdf_translation.verify.candidate_mapping import (
    METHOD_DRAWING_BOUND,
    METHOD_INSIDE_PRESERVED,
    METHOD_NO_EVIDENCE,
    METHOD_REGION_PIXELS,
    CandidateMapping,
)
from academic_pdf_translation.verify.structural_audit import StructuralAudit

SCHEMA_VERSION = "1.1"

SIGNAL_MISSING = "element-missing"
SIGNAL_GEOMETRY_GAP = "geometry-gap"
SIGNAL_CAPTION_SPLIT = "caption-split"
SIGNAL_AMBIGUOUS = "ambiguous-location"
SIGNAL_DRAWING_BOUND = "drawing-bound-only"
SIGNAL_NO_EVIDENCE = "required-without-evidence"
SIGNAL_ORDER = "order-inversion"

#: 基础信号：按内容类型给，映射全绿也照给。
SIGNAL_TABLE_LAYOUT = "table-layout"
SIGNAL_TABLE_PAGE_SPLIT = "table-page-split"
SIGNAL_FORMULA_INTEGRITY = "formula-integrity"
SIGNAL_DENSE_VECTOR = "dense-vector-figure"
SIGNAL_EMBEDDED_LABEL = "embedded-label-figure"
SIGNAL_FOOTNOTE_PLACEMENT = "footnote-placement"
SIGNAL_SAFE_FALLBACK = "safe-fallback-region"

#: 各信号的权重。数字本身不重要，重要的是相对次序：
#: 整块内容不见了，永远比顺序抖动更该先看。
#: 基础信号排在异常信号之下、顺序抖动之上——它们不报告已知的错，
#: 只说明这一页有一类看不出来的错，够格占一个名额。
RISK_WEIGHTS = {
    SIGNAL_MISSING: 10.0,
    SIGNAL_GEOMETRY_GAP: 9.0,
    SIGNAL_CAPTION_SPLIT: 7.0,
    SIGNAL_TABLE_PAGE_SPLIT: 6.0,
    SIGNAL_TABLE_LAYOUT: 5.0,
    SIGNAL_FORMULA_INTEGRITY: 5.0,
    SIGNAL_DENSE_VECTOR: 5.0,
    SIGNAL_NO_EVIDENCE: 4.0,
    SIGNAL_EMBEDDED_LABEL: 4.0,
    SIGNAL_DRAWING_BOUND: 3.0,
    SIGNAL_SAFE_FALLBACK: 3.0,
    SIGNAL_AMBIGUOUS: 2.0,
    SIGNAL_FOOTNOTE_PLACEMENT: 2.0,
    SIGNAL_ORDER: 1.0,
}

#: 每个信号对应的检查项。写成"看什么"，不是"哪里有风险"。
SIGNAL_CHECKLIST = {
    SIGNAL_MISSING: "这一页附近应当出现的内容是不是真的没了，还是挪到了别处",
    SIGNAL_GEOMETRY_GAP: "图里的线条和箭头在不在，还是只剩下一堆孤立的数字",
    SIGNAL_CAPTION_SPLIT: "图题和它说明的图是不是隔着页",
    SIGNAL_NO_EVIDENCE: "这一页有没有该出现却查不到的内容",
    SIGNAL_DRAWING_BOUND: "这一页上的图形是不是真是它，而不是碰巧数量够",
    SIGNAL_AMBIGUOUS: "同一段内容是不是被重复排了两处",
    SIGNAL_ORDER: "这一页的内容顺序读起来顺不顺",
    SIGNAL_TABLE_LAYOUT: "表格线有没有错位，每个数字是不是还在自己那一列",
    SIGNAL_TABLE_PAGE_SPLIT: "这张表跨了页，接缝两侧的行列有没有对齐、有没有重复",
    SIGNAL_FORMULA_INTEGRITY: "公式有没有被裁掉一角，上下标和行末编号在不在",
    SIGNAL_DENSE_VECTOR: "图形有没有糊、有没有被压扁，细线还看得清吗",
    SIGNAL_EMBEDDED_LABEL: "图里的中文标签有没有压住图形，有没有互相遮挡",
    SIGNAL_FOOTNOTE_PLACEMENT: "脚注在不在该在的位置，有没有跑到正文中间",
    SIGNAL_SAFE_FALLBACK: "保留下来的原文区域和周围的中文正文有没有重叠或错位",
}

#: 触发基础信号的元素类型 → 信号码。
BASELINE_TYPE_SIGNALS = {
    "table": SIGNAL_TABLE_LAYOUT,
    "display-formula": SIGNAL_FORMULA_INTEGRITY,
    "footnote": SIGNAL_FOOTNOTE_PLACEMENT,
}

#: 可能是"密集矢量图"的类型。
VECTOR_FIGURE_TYPES = frozenset({"vector-figure", "chart"})

#: 拿不到原文清单时的兜底门槛：这么多绘图对象就算密集矢量图。
#: 有原文清单时以它的 ``dense-vector`` 风险标记为准，不用这个数。
DENSE_VECTOR_DRAWINGS = 15

#: 走了安全降级的定位方法：内容是整块原区域搬过来的。
PRESERVED_METHODS = frozenset({METHOD_REGION_PIXELS, METHOD_INSIDE_PRESERVED})

#: 安全降级本来就是复杂内容的机制，只有这些类型自己占一块保留区域。
#: 图内标签、被区域盖住的正文都不单独发检查项——它们和宿主在同一块区域里，
#: 宿主那一条就是在看这块区域。一张图 43 个标签各发一条只会把清单淹掉。
FALLBACK_REGION_TYPES = frozenset(
    {
        "table",
        "vector-figure",
        "chart",
        "raster-figure",
        "screenshot",
        "display-formula",
    }
)

#: 计划里代表"保留原区域/原页"的策略前缀。
PRESERVE_STRATEGY_MARK = "preserve"

#: 默认最多渲染几页。评审看得完才有意义。
DEFAULT_PAGE_BUDGET = 6
#: 渲染分辨率。看排版够用，文件也不会大到打不开。
REVIEW_DPI = 150
#: 低于这个分数的页不值得占用评审的注意力。
MIN_REVIEW_SCORE = 1.0

#: 计划状态：没有风险页就是 NOT_REQUIRED——不是"看过了"，是"不用看"。
PLAN_NOT_REQUIRED = "NOT_REQUIRED"
PLAN_REQUIRED = "REQUIRED"
#: 有风险页被预算砍掉。截断的计划不许当成"全看过了"。
PLAN_TRUNCATED = "TRUNCATED"


class VisualReviewError(RuntimeError):
    """视觉检查计划构建失败。"""


@dataclass
class RiskSignal:
    """一条风险信号。"""

    code: str
    element_id: str
    detail: str

    @property
    def weight(self) -> float:
        return RISK_WEIGHTS.get(self.code, 0.0)

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["weight"] = self.weight
        return data


@dataclass
class PageRisk:
    """一页的风险汇总。"""

    candidate_page: int
    signals: list[RiskSignal] = field(default_factory=list)

    @property
    def score(self) -> float:
        return round(sum(signal.weight for signal in self.signals), 2)

    @property
    def element_ids(self) -> list[str]:
        seen: list[str] = []
        for signal in self.signals:
            if signal.element_id and signal.element_id not in seen:
                seen.append(signal.element_id)
        return seen

    @property
    def checklist(self) -> list[str]:
        seen: list[str] = []
        for signal in sorted(
            self.signals, key=lambda item: item.weight, reverse=True
        ):
            item = SIGNAL_CHECKLIST.get(signal.code)
            if item and item not in seen:
                seen.append(item)
        return seen

    @property
    def checks(self) -> list[tuple[str, str, str]]:
        """逐元素的检查项：(元素 ID, 检查码, 看什么)。

        视觉门按 (页, 元素, 检查码) 对账，所以清单也必须写到元素这一级：
        同一页两个表格触发同一个码，就是两条要分别回答的检查项。
        """

        seen: list[tuple[str, str, str]] = []
        for signal in sorted(
            self.signals, key=lambda item: item.weight, reverse=True
        ):
            entry = (
                signal.element_id,
                signal.code,
                SIGNAL_CHECKLIST.get(signal.code, signal.code),
            )
            if entry not in seen:
                seen.append(entry)
        return seen

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_page": self.candidate_page,
            "score": self.score,
            "element_ids": self.element_ids,
            "checklist": self.checklist,
            "checks": [
                {"element_id": item[0], "check_code": item[1], "look_for": item[2]}
                for item in self.checks
            ],
            "signals": [signal.as_dict() for signal in self.signals],
        }


@dataclass
class VisualReviewPlan:
    """一次视觉检查的计划。"""

    schema_version: str = SCHEMA_VERSION
    page_budget: int = DEFAULT_PAGE_BUDGET
    selected: list[PageRisk] = field(default_factory=list)
    #: 有风险但被预算砍掉的页。悄悄截断会让报告读起来像"全看过了"。
    skipped: list[PageRisk] = field(default_factory=list)
    rendered: list[str] = field(default_factory=list)

    @property
    def truncated(self) -> bool:
        return bool(self.skipped)

    @property
    def status(self) -> str:
        if self.truncated:
            return PLAN_TRUNCATED
        if self.selected:
            return PLAN_REQUIRED
        return PLAN_NOT_REQUIRED

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "page_budget": self.page_budget,
            "selected_count": len(self.selected),
            "skipped_count": len(self.skipped),
            "truncated": self.truncated,
            "selected": [item.as_dict() for item in self.selected],
            "skipped": [item.as_dict() for item in self.skipped],
            "rendered": list(self.rendered),
        }


def _source_index(
    elements: list[dict[str, Any]] | None,
) -> dict[str, dict[str, Any]]:
    if not elements:
        return {}
    return {
        str(element.get("id") or ""): element
        for element in elements
        if isinstance(element, dict) and element.get("id")
    }


def _plan_index(
    render_plan: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    if not render_plan:
        return {}
    return {
        str(entry.get("element_id") or ""): entry
        for entry in render_plan.get("elements", [])
        if isinstance(entry, dict) and entry.get("element_id")
    }


def _is_dense_vector(
    item: Any, source: dict[str, Any] | None
) -> bool:
    """这是不是一张密集矢量图。

    有原文清单就认它的 ``dense-vector`` 风险标记——那是扫描阶段按真实
    绘图对象数下的判断。没有清单才退到绘图对象数量的兜底门槛。
    """

    if item.element_type not in VECTOR_FIGURE_TYPES:
        return False
    if source is not None:
        return any(
            str(flag.get("code") or "") == "dense-vector"
            for flag in source.get("risk_flags", [])
            if isinstance(flag, dict)
        )
    return item.source_drawing_count >= DENSE_VECTOR_DRAWINGS


def _is_embedded_label(source: dict[str, Any] | None) -> bool:
    """这个元素是不是别人图里的一个标签。"""

    if source is None:
        return False
    relations = source.get("relations")
    return isinstance(relations, dict) and bool(relations.get("label-of"))


def _has_embedded_labels(source: dict[str, Any] | None) -> bool:
    if source is None:
        return False
    relations = source.get("relations")
    if not isinstance(relations, dict):
        return False
    return bool(relations.get("embedded-label"))


def _went_through_safe_fallback(
    item: Any, planned: dict[str, Any] | None
) -> bool:
    """这个元素是不是走了安全降级（整块保留原区域或原页）。

    计划说了算；拿不到计划时看映射用的定位方法——按像素指纹或落在保留
    区域内认出来的，本身就说明内容是整块搬过来的。
    """

    if item.element_type not in FALLBACK_REGION_TYPES:
        return False
    if planned is not None:
        strategy = str(planned.get("strategy") or "")
        if PRESERVE_STRATEGY_MARK in strategy:
            return True
    return item.method in PRESERVED_METHODS


def _formula_is_certainly_intact(
    item: Any,
    planned: dict[str, Any] | None,
    crop: dict[str, Any] | None,
) -> bool:
    """行间公式能不能免检。

    三条同时成立才免：按原区域整块保留、裁切边界检测通过、像素指纹
    证明整块内容原样在场。少一条、或者根本拿不到这些证据，都要看——
    默认要看，不默认放过。
    """

    if item.method != METHOD_REGION_PIXELS:
        return False
    if planned is None or PRESERVE_STRATEGY_MARK not in str(
        planned.get("strategy") or ""
    ):
        return False
    if not isinstance(crop, dict):
        return False
    return str(crop.get("status") or "") == STATUS_OK


def collect_signals(
    mapping: CandidateMapping,
    audit: StructuralAudit,
    *,
    elements: list[dict[str, Any]] | None = None,
    render_plan: dict[str, Any] | None = None,
    formula_crops: dict[str, dict[str, Any]] | None = None,
) -> dict[int, list[RiskSignal]]:
    """把阶段 9、10 的结果和内容类型折成逐页的风险信号。

    找不到的元素没有候选页码，挂到它原文所在的页上——评审要去看的，
    正是"这块内容本该出现的地方"。

    ``elements``、``render_plan``、``formula_crops`` 都是可选的补充证据。
    它们只会让判断更准，拿不到时基础信号照给：证据缺失不是免检的理由。
    """

    by_page: dict[int, list[RiskSignal]] = {}
    sources = _source_index(elements)
    plans = _plan_index(render_plan)
    crops = formula_crops or {}

    def add(page: int, signal: RiskSignal) -> None:
        if page <= 0:
            return
        by_page.setdefault(page, []).append(signal)

    def add_baseline(item: Any) -> None:
        """按内容类型给基础信号。映射说元素在，不代表它排得对。"""

        source = sources.get(item.element_id)
        planned = plans.get(item.element_id)
        if _is_embedded_label(source):
            # 图内标签不单独出检查项：它整块跟着宿主图走，宿主图的
            # embedded-label-figure 一项就是在看这些标签压没压住图形。
            # 一张图 43 个标签各发一条，只会把清单淹掉。
            return
        if item.element_type == "display-formula" and (
            _formula_is_certainly_intact(
                item, planned, crops.get(item.element_id)
            )
        ):
            return

        codes: list[tuple[str, str]] = []
        typed = BASELINE_TYPE_SIGNALS.get(item.element_type)
        if typed:
            codes.append((typed, f"{item.element_type} 默认进视觉检查"))
        if item.element_type == "table" and len(item.candidate_pages) > 1:
            codes.append(
                (
                    SIGNAL_TABLE_PAGE_SPLIT,
                    f"这张表落在候选第 {item.candidate_pages} 页",
                )
            )
        if _is_dense_vector(item, source):
            codes.append(
                (
                    SIGNAL_DENSE_VECTOR,
                    f"原文 {item.source_drawing_count} 个绘图对象",
                )
            )
        if _has_embedded_labels(source):
            codes.append(
                (
                    SIGNAL_EMBEDDED_LABEL,
                    f"图内有 {len(source['relations']['embedded-label'])} 个标签",
                )
            )
        if _went_through_safe_fallback(item, planned):
            codes.append(
                (
                    SIGNAL_SAFE_FALLBACK,
                    f"按 {planned.get('strategy') if planned else item.method} "
                    "整块保留了原区域",
                )
            )
        for code, detail in codes:
            for page in item.candidate_pages:
                add(page, RiskSignal(code, item.element_id, detail))

    for item in mapping.locations:
        if not item.located and item.required:
            # 「查不到」和「判不了」要分开：探针只剩一两个数学字体残渣字符时，
            # 我们并不知道内容丢没丢，不该按最高权重把评审引过去。
            code = (
                SIGNAL_NO_EVIDENCE
                if item.method == METHOD_NO_EVIDENCE
                else SIGNAL_MISSING
            )
            add(
                item.source_page,
                RiskSignal(code, item.element_id, item.evidence),
            )
            continue
        if item.geometry_ok is False:
            for page in item.candidate_pages:
                add(
                    page,
                    RiskSignal(
                        SIGNAL_GEOMETRY_GAP,
                        item.element_id,
                        f"原文 {item.source_drawing_count} 个绘图对象，"
                        f"候选这几页最多 {item.candidate_drawing_count} 个",
                    ),
                )
        if item.ambiguous:
            for page in item.candidate_pages:
                add(
                    page,
                    RiskSignal(
                        SIGNAL_AMBIGUOUS,
                        item.element_id,
                        f"同时疑似命中第 {item.candidate_pages} 页",
                    ),
                )
        if item.located and item.method == METHOD_DRAWING_BOUND:
            for page in item.candidate_pages:
                add(
                    page,
                    RiskSignal(
                        SIGNAL_DRAWING_BOUND, item.element_id, item.evidence
                    ),
                )
        add_baseline(item)

    for split in audit.caption_splits:
        for page in set(split.caption_pages) | set(split.target_pages):
            add(
                page,
                RiskSignal(
                    SIGNAL_CAPTION_SPLIT,
                    split.caption_id,
                    f"图题在第 {split.caption_pages} 页，"
                    f"{split.target_id} 在第 {split.target_pages} 页",
                ),
            )

    for inversion in audit.order_inversions:
        for page in (
            inversion.earlier_candidate_page,
            inversion.later_candidate_page,
        ):
            add(
                page,
                RiskSignal(
                    SIGNAL_ORDER,
                    inversion.earlier_in_source,
                    f"{inversion.earlier_in_source} 排到了 "
                    f"{inversion.later_in_source} 后面",
                ),
            )

    return by_page


def rank_pages(
    signals: dict[int, list[RiskSignal]],
    *,
    page_budget: int = DEFAULT_PAGE_BUDGET,
    min_score: float = MIN_REVIEW_SCORE,
) -> tuple[list[PageRisk], list[PageRisk]]:
    """按分数排页，返回（选中的，被预算砍掉的）。"""

    if page_budget < 1:
        raise VisualReviewError("视觉检查至少要看一页")

    ranked = [
        PageRisk(candidate_page=page, signals=list(items))
        for page, items in signals.items()
    ]
    ranked = [item for item in ranked if item.score >= min_score]
    ranked.sort(key=lambda item: (-item.score, item.candidate_page))
    return (ranked[:page_budget], ranked[page_budget:])


def build_review_plan(
    mapping: CandidateMapping,
    audit: StructuralAudit,
    *,
    page_budget: int = DEFAULT_PAGE_BUDGET,
    min_score: float = MIN_REVIEW_SCORE,
    elements: list[dict[str, Any]] | None = None,
    render_plan: dict[str, Any] | None = None,
    formula_crops: dict[str, dict[str, Any]] | None = None,
) -> VisualReviewPlan:
    """从映射、对账结果和内容类型算出该看哪几页。"""

    selected, skipped = rank_pages(
        collect_signals(
            mapping,
            audit,
            elements=elements,
            render_plan=render_plan,
            formula_crops=formula_crops,
        ),
        page_budget=page_budget,
        min_score=min_score,
    )
    return VisualReviewPlan(
        page_budget=page_budget, selected=selected, skipped=skipped
    )


def format_plan(plan: VisualReviewPlan) -> str:
    """给评审看的一页纸：看哪几页，每页看什么。"""

    if not plan.selected:
        return "没有需要人工细看的页。"
    lines = [f"需要人工细看 {len(plan.selected)} 页（预算 {plan.page_budget}）:"]
    for item in plan.selected:
        lines.append("")
        lines.append(f"候选第 {item.candidate_page} 页（风险分 {item.score}）")
        for element_id, code, look_for in item.checks:
            lines.append(f"  - [{element_id}] {code}: {look_for}")
    if plan.truncated:
        lines.append("")
        lines.append(
            f"另有 {len(plan.skipped)} 页有风险但超出预算未渲染: "
            + "、".join(
                f"第 {item.candidate_page} 页（{item.score}）"
                for item in plan.skipped
            )
        )
    return "\n".join(lines)
