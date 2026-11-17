"""三个质量档位的行为写成程序，而不是只写在 README 里。

一句话说清三档的差别：

- 快速档：宁可保守，也不能丢内容。不做完整独立复审，但要做元素清单、
  渲染计划、结构对账、高风险页定向检查，以及**最多一次**内部返修。
- 平衡档：快速档的全部，再加一次完整独立复审和一次集中返修。
- 精细档：平衡档的全部，再加统计、定义、公式、表格逐格等深度核对。

所有阈值集中放在这里，不许散落到各个渲染器里。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.enums import (
    QUALITY_MODE_TO_REVIEW_MODE,
    QualityMode,
)

# --- 复杂元素策略 -----------------------------------------------------------

#: 表格
TABLE_STRUCTURED_REBUILD = "structured-table-rebuild"
TABLE_PRESERVE_REGION = "preserve-table-region-with-translation-key"
#: 明确禁止：把表格压成普通段落。
TABLE_FLATTEN_FORBIDDEN = "flatten-table-to-paragraph"

#: 公式
FORMULA_PRESERVE_REGION = "preserve-formula-region"
FORMULA_FULL_REBUILD = "full-formula-rebuild"

#: 矢量图
VECTOR_PRESERVE_WITH_OVERLAY = "preserve-geometry-with-label-overlay"
VECTOR_PRESERVE_WITH_LEGEND = "preserve-geometry-with-numbered-legend"
VECTOR_FULL_REBUILD = "fast-full-vector-rebuild"

#: 图内文字
LABELS_OVERLAY = "overlay-translated-labels"
LABELS_NUMBERED_LEGEND = "numbered-legend"

#: 安全降级三级
FALLBACK_PRESERVE_ELEMENT_REGION = "preserve-element-region"
FALLBACK_PRESERVE_FULL_PAGE = "preserve-full-source-page"


@dataclass(frozen=True)
class ModePolicy:
    """一个质量档位的完整行为约定。"""

    quality_mode: QualityMode
    #: 是否对高风险页做定向视觉检查。三档都做。
    targeted_visual_review: bool
    #: 是否做完整独立复审。只有平衡档和精细档做。
    full_independent_review: bool
    #: 是否做深度核对（统计、定义、公式、表格逐格）。只有精细档做。
    deep_content_checks: bool
    #: 内部自动返修上限。三档都是 1，绝不允许无限返修。
    max_internal_repairs: int
    #: 独立复审后的集中返修上限。
    max_independent_repairs: int
    #: 独立复审轮数上限。
    max_review_rounds: int
    table_strategy: str
    table_low_confidence_strategy: str
    formula_strategy: str
    vector_figure_strategy: str
    vector_figure_low_confidence_strategy: str
    figure_label_strategy: str
    figure_label_low_confidence_strategy: str
    #: 表格网格置信度低于它就不做结构化重建，改为保留原表。
    table_confidence_floor: float
    #: 图内标签映射置信度低于它就改用编号图例。
    label_mapping_confidence_floor: float
    #: 元素识别置信度低于它就标风险，进定向检查。
    element_confidence_floor: float
    #: 保留原区域栅格化时的最低 DPI。
    preserved_region_min_dpi: int
    #: 明确禁止的策略。计划里出现它们就直接失败。
    forbidden_strategies: tuple[str, ...] = field(default=())

    @property
    def review_mode(self) -> str:
        """旧的 job.review.mode，由质量档位派生，不再单独填写。"""

        return QUALITY_MODE_TO_REVIEW_MODE[self.quality_mode]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["quality_mode"] = self.quality_mode.value
        data["review_mode"] = self.review_mode
        return data


_COMMON = {
    "targeted_visual_review": True,
    "max_internal_repairs": 1,
    "table_strategy": TABLE_STRUCTURED_REBUILD,
    "table_low_confidence_strategy": TABLE_PRESERVE_REGION,
    "figure_label_strategy": LABELS_OVERLAY,
    "figure_label_low_confidence_strategy": LABELS_NUMBERED_LEGEND,
    "preserved_region_min_dpi": 300,
}

MODE_POLICIES: dict[QualityMode, ModePolicy] = {
    QualityMode.FAST: ModePolicy(
        quality_mode=QualityMode.FAST,
        full_independent_review=False,
        deep_content_checks=False,
        max_independent_repairs=0,
        max_review_rounds=0,
        # 快速档减的是重绘野心，不是内容完整性：
        # 复杂公式和复杂矢量图一律保留原区域，不重画。
        formula_strategy=FORMULA_PRESERVE_REGION,
        vector_figure_strategy=VECTOR_PRESERVE_WITH_OVERLAY,
        vector_figure_low_confidence_strategy=VECTOR_PRESERVE_WITH_LEGEND,
        table_confidence_floor=0.85,
        label_mapping_confidence_floor=0.80,
        element_confidence_floor=0.70,
        forbidden_strategies=(
            TABLE_FLATTEN_FORBIDDEN,
            FORMULA_FULL_REBUILD,
            VECTOR_FULL_REBUILD,
        ),
        **_COMMON,
    ),
    QualityMode.BALANCED: ModePolicy(
        quality_mode=QualityMode.BALANCED,
        full_independent_review=True,
        deep_content_checks=False,
        max_independent_repairs=1,
        max_review_rounds=1,
        formula_strategy=FORMULA_PRESERVE_REGION,
        vector_figure_strategy=VECTOR_PRESERVE_WITH_OVERLAY,
        vector_figure_low_confidence_strategy=VECTOR_PRESERVE_WITH_LEGEND,
        table_confidence_floor=0.85,
        label_mapping_confidence_floor=0.80,
        element_confidence_floor=0.70,
        forbidden_strategies=(TABLE_FLATTEN_FORBIDDEN,),
        **_COMMON,
    ),
    QualityMode.PRECISE: ModePolicy(
        quality_mode=QualityMode.PRECISE,
        full_independent_review=True,
        deep_content_checks=True,
        max_independent_repairs=1,
        max_review_rounds=1,
        formula_strategy=FORMULA_PRESERVE_REGION,
        vector_figure_strategy=VECTOR_PRESERVE_WITH_OVERLAY,
        vector_figure_low_confidence_strategy=VECTOR_PRESERVE_WITH_LEGEND,
        # 精细档对识别要求更高：够不到就走保留，不硬重建。
        table_confidence_floor=0.92,
        label_mapping_confidence_floor=0.88,
        element_confidence_floor=0.80,
        forbidden_strategies=(TABLE_FLATTEN_FORBIDDEN,),
        **_COMMON,
    ),
}


def policy_for(mode: QualityMode | str) -> ModePolicy:
    """取某个档位的策略。"""

    return MODE_POLICIES[
        mode if isinstance(mode, QualityMode) else QualityMode.parse(mode)
    ]


def policy_for_job(job: dict[str, Any]) -> ModePolicy:
    """从作业数据里取档位策略。

    优先用 ``quality_mode``；旧作业没有这个字段时，从 ``review.mode`` 推。
    """

    explicit = job.get("quality_mode")
    if explicit:
        return policy_for(QualityMode.parse(explicit))
    legacy = str(job.get("review", {}).get("mode") or "")
    if not legacy:
        raise ValueError(
            "作业既没有 quality_mode，也没有 review.mode，无法确定质量档位"
        )
    return policy_for(QualityMode.parse(legacy))
