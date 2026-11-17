"""公式渲染器。

规则只有一条：**不重新输入数学结构**。

独立公式一旦被当成普通文字流重排，求和号会变成字母 X、根号会变成字母 p、
分式线会消失、分母会脱离分式、上标平方会退化成普通 2。这些不是排版参数
的问题，是"把图形当文字重打了一遍"的必然结果。

所以这里把公式连同它的编号一起，从原文整块搬进候选。公式周围的说明
照常翻译，公式本身一个字符都不重打。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import BBox, normalize_bbox
from academic_pdf_translation.render.preserved_region_renderer import (
    PreservedRegion,
    PreservedRegionError,
    preserve_region,
)

#: 公式区域左右各留的余量。公式编号常靠版心右边缘，留窄了会被切掉。
FORMULA_SIDE_PADDING_PT = 6.0
#: 公式主体与编号之间允许的最大水平间距，超过就不算同一行公式。
MAX_NUMBER_GAP_PT = 320.0

#: 数学结构被当成文字重打时留下的典型伪影。出现它们就说明公式散架了。
BROKEN_MATH_ARTIFACTS = (
    "X",  # 求和号 Σ 被当成字母 X
    "P",  # 连乘号 Π 被当成字母 P
    "K",  # 求和上界被拆成孤立字母
    "!",  # 右括号或分隔符退化
)


class FormulaRenderError(RuntimeError):
    """公式保留失败。"""


@dataclass
class RenderedFormula:
    """一个公式的渲染结果。"""

    element_id: str
    source_page: int
    candidate_page: int
    candidate_bbox: list[float]
    formula_number: str | None
    mode: str
    content_sha256: str
    fragment_count: int = 1
    surrounding_unit_ids: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def formula_region(
    element_bbox: Any,
    page_rect: Any,
    *,
    include_number: bool = True,
) -> BBox:
    """算出要保留的公式区域。

    公式编号在行末、靠近版心右边缘。按元素坐标直接截会把它切掉，
    所以这里把区域向右展到版心边界。
    """

    box = normalize_bbox(element_bbox)
    if box is None:
        raise FormulaRenderError("公式元素缺少有效坐标")
    left = max(float(page_rect.x0), box[0] - FORMULA_SIDE_PADDING_PT)
    right = box[2] + FORMULA_SIDE_PADDING_PT
    if include_number:
        right = min(float(page_rect.x1), max(right, float(page_rect.x1) - 1.0))
    else:
        right = min(float(page_rect.x1), right)
    return (left, box[1], right, box[3])


def fits_on_one_page(region: BBox, available_height: float) -> bool:
    """公式不得跨页拆开：放不下就整块挪下一页。"""

    return (region[3] - region[1]) <= available_height


def math_artifacts(text: str) -> list[str]:
    """文字层里孤立成行的数学伪影。

    注意：**原文 PDF 的文字层本来就有这些**。数学字体把 Σ 映射成字母 X、
    把 Π 映射成 P，抽文字时就会抽出孤立的 "X"、"P"。所以单看候选里有没有
    这些字符，说明不了任何问题。
    """

    found: list[str] = []
    for line in str(text or "").splitlines():
        stripped = line.strip()
        if stripped in BROKEN_MATH_ARTIFACTS and stripped not in found:
            found.append(stripped)
    return found


def detect_retypeset_formula(
    source_text: str,
    candidate_text: str,
) -> list[str]:
    """判断公式是不是被重新排过，而不是原样保留。

    判据是**候选比原文多出来的伪影**：区域保留的候选和原文一模一样，
    多出来的伪影只可能来自把数学结构当文字重打了一遍。

    这条区分很要紧。之前那版渲染器把公式拆成 "E ="、"X"、"x∈Ω" 几行
    重新排出来，读者看到的是一堆碎片；而区域保留出来的候选，
    视觉上和原文逐像素一致，文字层的怪字符和原文一样——那是原文自带的，
    不是我们弄坏的。
    """

    baseline = set(math_artifacts(source_text))
    return [
        artifact
        for artifact in math_artifacts(candidate_text)
        if artifact not in baseline
    ]


def render_formula(
    source_document: Any,
    candidate_page: Any,
    element: dict[str, Any],
    *,
    target_bbox: Any,
    dpi: int | None = None,
    force_raster: bool = False,
) -> RenderedFormula:
    """把一个独立公式连同编号原样搬进候选。"""

    element_id = str(element.get("id") or "")
    source_page = int(element.get("page") or 0)
    if not 1 <= source_page <= source_document.page_count:
        raise FormulaRenderError(f"{element_id}: 原文页码 {source_page} 越界")

    page = source_document[source_page - 1]
    detail = element.get("detail") or {}
    region = formula_region(element.get("bbox"), page.rect)

    try:
        preserved: PreservedRegion = preserve_region(
            source_document,
            candidate_page,
            source_page=source_page,
            source_bbox=region,
            target_bbox=target_bbox,
            element_id=element_id,
            **({"dpi": dpi} if dpi is not None else {}),
            force_raster=force_raster,
        )
    except PreservedRegionError as exc:
        raise FormulaRenderError(f"{element_id}: 公式区域保留失败: {exc}") from exc

    return RenderedFormula(
        element_id=element_id,
        source_page=source_page,
        candidate_page=preserved.candidate_page,
        candidate_bbox=list(preserved.candidate_bbox),
        formula_number=detail.get("formula_number"),
        mode=preserved.mode,
        content_sha256=preserved.content_sha256,
        fragment_count=int(detail.get("fragment_count") or 1),
    )
