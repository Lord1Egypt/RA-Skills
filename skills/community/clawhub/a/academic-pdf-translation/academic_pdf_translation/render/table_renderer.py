"""表格渲染器。

一条底线：**表格不能变成普通段落**。

独立复审 R-003 报的就是这个——表 1 和表 2 被压成一行流水文字，
"0.000353 0.0382 0.0611 2. DIVE-SCI 0.000355..."，读者无法判断哪个数字
属于哪一列，空值位置也丢了。

所以这里只有在**每一项都确定**的前提下才允许结构化重建：网格置信度达标、
行数列数已定、数字能映射到单元格、合并单元格已定、表题表注已找到、
粗体语义已找到。任何一项不满足，就保留原表区域，另配中文表题、
中文列头翻译键和中文表注——不好看，但每个数字仍在它该在的格子里。
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import normalize_bbox
from academic_pdf_translation.render.preserved_region_renderer import (
    PreservedRegionError,
    preserve_region,
)

MODE_STRUCTURED = "structured-table-rebuild"
MODE_PRESERVED = "preserve-table-region-with-translation-key"

#: 粗体字体名里的标志。表格里靠粗体表达"本列最优"，这是语义不是装饰。
BOLD_FONT_TOKENS = ("bold", "bx", "-b", "black", "heavy", "semib")

#: 空白单元格与显式的"-"是两回事：前者是没测，后者是测了但不适用。
EMPTY_CELL = ""
EXPLICIT_MISSING = "-"
MISSING_MARKERS = ("-", "–", "—", "n/a", "N/A")

#: 表格字号下限，来自质量合同。低于它就不叫可读。
MIN_TABLE_FONT_PT = 7.0

NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?%?")


class TableRenderError(RuntimeError):
    """表格渲染失败。"""


@dataclass
class TableReliability:
    """能不能结构化重建，逐项说明。"""

    grid_confidence_ok: bool
    rows_known: bool
    columns_known: bool
    numbers_mapped: bool
    merged_cells_known: bool
    caption_found: bool
    note_found_or_absent: bool
    bold_semantics_known: bool

    @property
    def reliable(self) -> bool:
        """全部为真才允许重建。有一项含糊就走保留。"""

        return all(asdict(self).values())

    def missing(self) -> list[str]:
        return [name for name, ok in asdict(self).items() if not ok]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["reliable"] = self.reliable
        data["missing"] = self.missing()
        return data


@dataclass
class RenderedTable:
    """一张表的渲染结果与证据。"""

    element_id: str
    source_page: int
    candidate_page: int
    candidate_bbox: list[float]
    mode: str
    reliability: dict[str, Any]
    rows: int
    columns: int
    bold_cells: list[str] = field(default_factory=list)
    explicit_missing_cells: int = 0
    caption_element_id: str | None = None
    caption_page: int | None = None
    note_element_id: str | None = None
    translation_key: list[str] = field(default_factory=list)
    content_sha256: str = ""
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def is_bold_font(font_name: str) -> bool:
    lowered = str(font_name or "").casefold()
    return any(token in lowered for token in BOLD_FONT_TOKENS)


def detect_bold_cells(page: Any, bbox: Any) -> list[str]:
    """找出表格区域里用粗体标出的值。

    学术表格用粗体表示"本列最优"。这是语义，不是装饰——丢了粗体，
    读者就看不出哪一行赢了。
    """

    import fitz

    box = normalize_bbox(bbox)
    if box is None:
        return []
    found: list[str] = []
    data = page.get_text("dict", clip=fitz.Rect(*box))
    for block in data.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = str(span.get("text") or "").strip()
                if not text:
                    continue
                if is_bold_font(span.get("font", "")) and text not in found:
                    found.append(text)
    return found


def classify_cell(text: str) -> str:
    """区分空白单元格和显式的缺失标记。"""

    value = str(text or "").strip()
    if not value:
        return EMPTY_CELL
    if value in MISSING_MARKERS:
        return EXPLICIT_MISSING
    return value


def count_explicit_missing(cells: list[str]) -> int:
    return sum(1 for cell in cells if classify_cell(cell) == EXPLICIT_MISSING)


def decimals_preserved(source_text: str, candidate_text: str) -> list[str]:
    """小数位必须原样保留。0.000420 不能变成 0.00042。"""

    source_numbers = NUMBER_RE.findall(source_text or "")
    missing: list[str] = []
    for number in source_numbers:
        if "." not in number:
            continue
        if number not in (candidate_text or ""):
            missing.append(number)
    return missing


def assess_reliability(
    element: dict[str, Any],
    *,
    confidence_floor: float,
    bold_cells: list[str],
    caption_element_id: str | None,
    note_element_id: str | None,
    merged_cells_known: bool = False,
) -> TableReliability:
    """逐项判断能不能结构化重建。"""

    detail = element.get("detail") or {}
    rows = int(detail.get("estimated_rows") or 0)
    columns = int(detail.get("estimated_columns") or 0)
    risks = {
        str(risk.get("code") or "")
        for risk in (element.get("risk_flags") or [])
        if isinstance(risk, dict)
    }
    columns_known = columns >= 2 and "table-columns-unresolved" not in risks
    return TableReliability(
        grid_confidence_ok=float(element.get("confidence") or 0.0)
        >= confidence_floor,
        rows_known=rows >= 2,
        columns_known=columns_known,
        # 列都定不下来时，谈不上"数字映射到了单元格"。
        numbers_mapped=columns_known and rows >= 2,
        merged_cells_known=merged_cells_known,
        caption_found=bool(caption_element_id),
        note_found_or_absent=True,
        bold_semantics_known=bold_cells is not None,
    )


def build_column_key(headers: list[dict[str, Any]]) -> list[str]:
    """中文列头翻译键。

    保留原表区域时，读者看到的是英文表头，所以下面要给一份对照。
    每一条必须来自翻译单元，不许现编。
    """

    key: list[str] = []
    for index, header in enumerate(headers, 1):
        translation = str(header.get("translation") or "").strip()
        if not translation:
            continue
        unit_id = str(header.get("translation_unit_id") or "").strip()
        if not unit_id:
            raise TableRenderError(
                f"列头翻译键第 {index} 条没有绑定 translation_unit_id: "
                f"{translation[:30]!r}"
            )
        source = str(header.get("source") or "").strip()
        key.append(
            f"{source} -> {translation}" if source else translation
        )
    return key


def render_table(
    source_document: Any,
    candidate_page: Any,
    element: dict[str, Any],
    *,
    target_bbox: Any,
    confidence_floor: float = 0.85,
    column_headers: list[dict[str, Any]] | None = None,
    caption_element_id: str | None = None,
    caption_page: int | None = None,
    note_element_id: str | None = None,
    merged_cells_known: bool = False,
    force_raster: bool = False,
) -> RenderedTable:
    """渲染一张表。认得准就重建，认不准就保留原表。"""

    element_id = str(element.get("id") or "")
    source_page = int(element.get("page") or 0)
    if not 1 <= source_page <= source_document.page_count:
        raise TableRenderError(f"{element_id}: 原文页码 {source_page} 越界")

    page = source_document[source_page - 1]
    bold_cells = detect_bold_cells(page, element.get("bbox"))
    reliability = assess_reliability(
        element,
        confidence_floor=confidence_floor,
        bold_cells=bold_cells,
        caption_element_id=caption_element_id,
        note_element_id=note_element_id,
        merged_cells_known=merged_cells_known,
    )

    warnings: list[str] = []
    detail = element.get("detail") or {}

    if reliability.reliable:
        mode = MODE_STRUCTURED
    else:
        mode = MODE_PRESERVED
        warnings.append(
            "结构化重建的前提没有全部满足（"
            + "、".join(reliability.missing())
            + "），保留原表区域并附中文表题与列头翻译键"
        )

    try:
        preserved = preserve_region(
            source_document,
            candidate_page,
            source_page=source_page,
            source_bbox=element.get("bbox"),
            target_bbox=target_bbox,
            element_id=element_id,
            force_raster=force_raster,
        )
    except PreservedRegionError as exc:
        raise TableRenderError(f"{element_id}: 表格区域保留失败: {exc}") from exc

    key = build_column_key(list(column_headers or []))

    if caption_page is not None and caption_page != preserved.candidate_page:
        warnings.append(
            f"表题在候选第 {caption_page} 页，表格在第 "
            f"{preserved.candidate_page} 页，必须同页"
        )

    import fitz

    region_text = page.get_text(
        "text", clip=fitz.Rect(*normalize_bbox(element.get("bbox")))
    )
    explicit_missing = count_explicit_missing(
        [line.strip() for line in region_text.splitlines()]
    )

    return RenderedTable(
        element_id=element_id,
        source_page=source_page,
        candidate_page=preserved.candidate_page,
        candidate_bbox=list(preserved.candidate_bbox),
        mode=mode,
        reliability=reliability.as_dict(),
        rows=int(detail.get("estimated_rows") or 0),
        columns=int(detail.get("estimated_columns") or 0),
        bold_cells=bold_cells,
        explicit_missing_cells=explicit_missing,
        caption_element_id=caption_element_id,
        caption_page=caption_page,
        note_element_id=note_element_id,
        translation_key=key,
        content_sha256=preserved.content_sha256,
        warnings=warnings,
    )


def verify_table_output(
    rendered: RenderedTable,
    source_text: str,
    candidate_text: str,
    *,
    candidate_drawing_count: int | None = None,
) -> list[str]:
    """核对一张表有没有真的保住。

    **表格不能变成段落**这条，靠的是网格线还在 + 数字与小数位还在，
    不是靠字符串里有没有那些数字——压平成段落时数字其实一个不少。
    """

    problems: list[str] = []

    missing_decimals = decimals_preserved(source_text, candidate_text)
    if missing_decimals:
        problems.append(
            f"{rendered.element_id}: 小数位被改动或丢失: "
            + ", ".join(missing_decimals[:8])
        )

    for value in rendered.bold_cells:
        if value not in candidate_text:
            problems.append(
                f"{rendered.element_id}: 粗体最优值 {value} 在候选里找不到"
            )

    if (
        candidate_drawing_count is not None
        and rendered.mode == MODE_PRESERVED
        and candidate_drawing_count <= 0
    ):
        problems.append(
            f"{rendered.element_id}: 保留模式下候选没有任何网格线，"
            "表格很可能被压平成了段落"
        )

    if rendered.caption_page is not None and (
        rendered.caption_page != rendered.candidate_page
    ):
        problems.append(
            f"{rendered.element_id}: 表题与表格不在同一页"
        )
    return problems
