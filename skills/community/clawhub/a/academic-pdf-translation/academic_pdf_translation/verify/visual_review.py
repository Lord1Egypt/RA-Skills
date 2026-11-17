"""兼容入口：视觉检查已拆成计划、渲染、结果、门槛四个模块。

- :mod:`visual_plan`：收集风险、算分、选页、生成逐页清单。
- :mod:`visual_render`：把选中的页渲染成图片。
- :mod:`visual_result`：真正的检查结果（绑定候选哈希，逐页逐项）。
- :mod:`visual_gate`：计划和结果对得上才算看过。

旧导入路径继续可用，新代码请直接从上面四个模块导入。
"""

from __future__ import annotations

from academic_pdf_translation.verify.visual_plan import (  # noqa: F401
    DEFAULT_PAGE_BUDGET,
    MIN_REVIEW_SCORE,
    PLAN_NOT_REQUIRED,
    PLAN_REQUIRED,
    PLAN_TRUNCATED,
    REVIEW_DPI,
    RISK_WEIGHTS,
    SIGNAL_AMBIGUOUS,
    SIGNAL_CAPTION_SPLIT,
    SIGNAL_CHECKLIST,
    SIGNAL_DENSE_VECTOR,
    SIGNAL_DRAWING_BOUND,
    SIGNAL_EMBEDDED_LABEL,
    SIGNAL_FOOTNOTE_PLACEMENT,
    SIGNAL_FORMULA_INTEGRITY,
    SIGNAL_GEOMETRY_GAP,
    SIGNAL_MISSING,
    SIGNAL_NO_EVIDENCE,
    SIGNAL_ORDER,
    SIGNAL_SAFE_FALLBACK,
    SIGNAL_TABLE_LAYOUT,
    SIGNAL_TABLE_PAGE_SPLIT,
    PageRisk,
    RiskSignal,
    VisualReviewError,
    VisualReviewPlan,
    build_review_plan,
    collect_signals,
    format_plan,
    rank_pages,
)
from academic_pdf_translation.verify.visual_render import (  # noqa: F401
    render_review_pages,
    rendered_image_hashes,
)
