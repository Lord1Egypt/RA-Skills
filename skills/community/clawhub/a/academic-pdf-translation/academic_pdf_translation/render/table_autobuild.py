"""表格自动重建：程序抽网格、锚点收割译文，模型只出过字符串的力。

慢路径的好效果来自人工填写的结构化表格载荷；快路径的贴图保底把表格
保住了却留着英文。这两者之间缺的是一段纯程序的活：

1. **网格是几何事实，不需要模型。** 学术 PDF 的表格里，PyMuPDF 的
   行对象往往一格一个：按 y 聚成行、按 x 中心聚成列，网格就出来了。
2. **数字和拉丁专名不用翻。** 排名、误差值、方法名（u-net、DIVE-SCI）
   原样进中文表。
3. **要翻的那几个词，译文常常早就有了。** 翻译单元里存着整行的译文，
   数字和专名在原文译文里逐字相同，正好当锚点：锚点之间的中文片段，
   就是对应文字单元格的译文。

哪一步没把握就退回贴图保底，绝不硬拼一张错表。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import normalize_bbox

#: 同一行的 y 中心差不超过这个值（点）。
ROW_TOLERANCE_PT = 4.0
#: 列间空白带的最小宽度（点）。窄于它的空白当作格内间隔。
MIN_COLUMN_GAP_PT = 7
#: 至少要有这么多行、这么多列才谈得上是表。
MIN_ROWS = 2
MIN_COLUMNS = 2
#: 网格里允许的"格数不齐"行占比上限（省略号行、跨列注释行）。
MAX_RAGGED_ROW_RATIO = 0.34

#: 逐字可复制、无须翻译的单元格：数字、百分比、区间、专名式拉丁串。
VERBATIM_RE = re.compile(
    r"^[\s*]*(?:[-–—]|\.{2,}|…|[-+]?\d[\d.,%]*|"
    r"[A-Za-z][\w-]*(?:[\s/][\w()\[\].-]+)*)[\s*]*$"
)
CJK_RE = re.compile(r"[㐀-鿿]")
#: 纯数字/符号格：不收割也不翻译，原样复制。
NUMERIC_ONLY_RE = re.compile(r"^[\s*.%–—-]*[-+]?[\d.,%]+[\s*.%–—-]*$|^[.…\s]+$|^[-–—]$")
BOLD_FONT_RE = re.compile(r"bold|bx|black|heavy|semib", re.IGNORECASE)


@dataclass
class Cell:
    text: str
    x0: float
    x1: float
    bold: bool = False
    column: int = -1

    @property
    def x_center(self) -> float:
        return (self.x0 + self.x1) / 2


@dataclass
class TableGrid:
    rows: list[list[Cell]] = field(default_factory=list)
    column_count: int = 0
    issues: list[str] = field(default_factory=list)

    @property
    def confident(self) -> bool:
        return not self.issues


def extract_grid(page: Any, bbox: Any) -> TableGrid:
    """从表格区域抽网格。抽不出规整网格就如实报，不硬凑。"""

    import fitz

    box = normalize_bbox(bbox)
    grid = TableGrid()
    if box is None:
        grid.issues.append("表格元素没有有效坐标")
        return grid

    raw_lines: list[tuple[float, Cell]] = []
    data = page.get_text("dict", clip=fitz.Rect(*box))
    for block in data.get("blocks", []):
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            # 空格 span 也要保留在拼接里，否则 "IMCB-SG (2014)" 会拼成
            # "IMCB-SG(2014)"，拿去和译文单元的原文对不上。
            text = re.sub(
                r"\s+",
                " ",
                "".join(str(span.get("text") or "") for span in spans),
            ).strip()
            if not text:
                continue
            lb = line["bbox"]
            raw_lines.append(
                (
                    (lb[1] + lb[3]) / 2,
                    Cell(
                        text=text,
                        x0=float(lb[0]),
                        x1=float(lb[2]),
                        bold=any(
                            BOLD_FONT_RE.search(str(span.get("font") or ""))
                            for span in spans
                            if str(span.get("text") or "").strip()
                        ),
                    ),
                )
            )
    if not raw_lines:
        grid.issues.append("表格区域里没有文字")
        return grid

    # 按 y 聚行
    raw_lines.sort(key=lambda item: item[0])
    rows: list[list[Cell]] = []
    current_y = None
    for y, cell in raw_lines:
        if current_y is None or abs(y - current_y) > ROW_TOLERANCE_PT:
            rows.append([])
            current_y = y
        rows[-1].append(cell)
    for row in rows:
        row.sort(key=lambda cell: cell.x_center)

    # 按列间空白带分列：把每格的横向区间投影到 x 轴，
    # 从未被任何格覆盖的竖向空白带就是列分隔。学术表格列间必有空白，
    # 这比对 x 中心做链式聚类稳得多——渐变的中心值会把相邻列串成一列。
    left = min(cell.x0 for row in rows for cell in row)
    right = max(cell.x1 for row in rows for cell in row)
    span_pt = max(int(right - left) + 1, 1)
    covered = [False] * span_pt
    for row in rows:
        for cell in row:
            for x in range(int(cell.x0 - left), int(cell.x1 - left) + 1):
                if 0 <= x < span_pt:
                    covered[x] = True
    separators: list[float] = []
    gap_start = None
    for x, hit in enumerate(covered):
        if not hit and gap_start is None:
            gap_start = x
        elif hit and gap_start is not None:
            if x - gap_start >= MIN_COLUMN_GAP_PT:
                separators.append(left + (gap_start + x) / 2)
            gap_start = None
    boundaries = [left - 1.0, *separators, right + 1.0]
    column_centers = [
        (boundaries[index] + boundaries[index + 1]) / 2
        for index in range(len(boundaries) - 1)
    ]
    grid.column_count = len(column_centers)

    def column_of(cell: Cell) -> int:
        for index in range(len(boundaries) - 1):
            if boundaries[index] <= cell.x_center < boundaries[index + 1]:
                return index
        return len(boundaries) - 2

    if len(rows) < MIN_ROWS:
        grid.issues.append(f"只有 {len(rows)} 行，不足 {MIN_ROWS}")
    if grid.column_count < MIN_COLUMNS:
        grid.issues.append(
            f"只聚出 {grid.column_count} 列，不足 {MIN_COLUMNS}"
        )
    if grid.issues:
        return grid

    ragged = 0
    for row in rows:
        for cell in row:
            cell.column = column_of(cell)
        used = [cell.column for cell in row]
        if len(set(used)) != len(used):
            grid.issues.append("同一行里两格落进了同一列，列聚类不可信")
            return grid
        if len(row) != grid.column_count:
            ragged += 1
    if ragged / len(rows) > MAX_RAGGED_ROW_RATIO:
        grid.issues.append(
            f"{ragged}/{len(rows)} 行的格数与列数不符，网格不可信"
        )
        return grid

    grid.rows = rows
    return grid


def _anchor_tokens(text: str) -> list[str]:
    """原文译文里逐字相同的锚点：数字、拉丁词、破折号。"""

    return re.findall(r"[-+]?\d[\d.,%]*|[A-Za-z][\w()\[\].-]*|[-–—]", text)


def harvest_translations(
    grid: TableGrid,
    units: list[dict[str, Any]],
    claimed: set[str] | None = None,
) -> dict[str, str]:
    """用锚点从既有译文里收割文字单元格的中文。

    收不到就不填——那格保英文，宁缺毋滥。
    """

    harvested: dict[str, str] = {}
    claimed = claimed or set()
    # 纯数字格原样复制，不参与收割——短数字串在文本里到处都能撞上。
    # 其余格都试：'second-best 2015' 长得像专名，其实有译文
    # 「2015 年第二名」；收到了就用，收不到再看它像不像不用翻的。
    text_cells = [
        cell.text
        for row in grid.rows
        for cell in row
        if not NUMERIC_ONLY_RE.match(cell.text)
    ]
    if not text_cells:
        return harvested

    pairs = [
        (
            str(unit.get("source") or ""),
            str(unit.get("translation") or ""),
        )
        for unit in units
        if isinstance(unit, dict)
        and CJK_RE.search(str(unit.get("translation") or ""))
    ]

    for cell_text in text_cells:
        if cell_text in harvested or cell_text in claimed:
            continue
        for source, translation in pairs:
            position = source.find(cell_text)
            if position < 0:
                continue
            # 单元格前后最近的、在译文里也逐字出现的锚点
            before = _anchor_tokens(source[:position])
            after = _anchor_tokens(source[position + len(cell_text):])
            start = 0
            for token in reversed(before):
                hit = translation.rfind(token)
                if hit >= 0:
                    start = hit + len(token)
                    break
            end = len(translation)
            for token in after:
                hit = translation.find(token, start)
                if hit >= 0:
                    end = hit
                    break
            segment = translation[start:end].strip(" ，,。;；:：*")
            if not _segment_is_sane(segment, cell_text):
                continue
            # 片段里包着格子原文本身、又不止它一个——割到邻居了。
            if cell_text in segment and segment != cell_text:
                continue
            harvested[cell_text] = segment
            break
    return harvested


def _segment_is_sane(segment: str, cell_text: str) -> bool:
    """收割到的片段要过卫生检查，脏的宁可不要。

    从错误的单元里割出来的片段有明显特征：带着格里没有的数字、
    带着句读（说明割到了整句散文）、或长得离谱。
    """

    if not segment or not CJK_RE.search(segment):
        return False
    if "。" in segment or "，" in segment:
        return False
    if len(segment) > 2 * len(cell_text) + 10:
        return False
    cell_digits = set(re.findall(r"\d", cell_text))
    return all(
        digit in cell_digits for digit in re.findall(r"\d", segment)
    )


def _split_segment_over_cells(
    segment: str, cell_texts: list[str]
) -> dict[str, str] | None:
    """一个译文片段对应连续几格时，按空格切开一一对应。数量不齐就放弃。"""

    tokens = segment.split()
    if len(tokens) == len(cell_texts):
        return dict(zip(cell_texts, tokens, strict=True))
    return None


def refine_header_translations(
    grid: TableGrid,
    units: list[dict[str, Any]],
    harvested: dict[str, str],
) -> set[str]:
    """表头整行按词元锚点对齐拆格，返回已认领的表头格文本。

    表头没有数字锚点，但常有在译文里逐字保留的词元（Rand、PhC-U373）。
    以它们为切分点：切分点之间的中文按空格拆开，与该区间的格数一一对应；
    切分点所在的格取锚点词元加上它份内的中文（「Rand」+「误差」）。
    对不齐就整行放弃——表头保英文，好过张冠李戴。
    """

    if not grid.rows:
        return set()
    header_texts = [cell.text for cell in grid.rows[0]]
    claimed = set(header_texts)
    if all(text in harvested for text in header_texts):
        return claimed

    source_line = re.sub(r"\s+", " ", " ".join(header_texts))
    for unit in units:
        if not isinstance(unit, dict):
            continue
        source = re.sub(r"\s+", " ", str(unit.get("source") or ""))
        translation = str(unit.get("translation") or "")
        if source_line not in source or not CJK_RE.search(translation):
            continue

        # 锚点 = 在译文里逐字出现的词元，逐格找
        anchor_of: dict[int, str] = {}
        for index, text in enumerate(header_texts):
            for token in _anchor_tokens(text):
                if token in translation:
                    anchor_of[index] = token
                    break

        cursor = 0
        segments: list[str] = []
        groups: list[list[int]] = [[]]
        anchored: list[int] = []
        ok = True
        for index in range(len(header_texts)):
            if index in anchor_of:
                hit = translation.find(anchor_of[index], cursor)
                if hit < 0:
                    ok = False
                    break
                segments.append(translation[cursor:hit].strip())
                cursor = hit + len(anchor_of[index])
                anchored.append(index)
                groups.append([])
            else:
                groups[-1].append(index)
        if not ok:
            continue
        tail = translation[cursor:].strip()

        result: dict[int, str] = {}
        for group, segment in zip(groups, segments, strict=False):
            tokens = segment.split()
            if len(tokens) != len(group):
                result = {}
                break
            for index, token in zip(group, tokens, strict=True):
                result[index] = token
        if not result and any(groups[:-1]):
            continue

        # 尾段：先给最后一个锚点格补份内中文，再分给锚点后的格
        last_group = groups[-1] if groups else []
        tail_tokens = tail.split()
        if anchored:
            last_anchor = anchored[-1]
            need = len(last_group)
            if len(tail_tokens) == need + 1:
                result[last_anchor] = (
                    f"{anchor_of[last_anchor]} {tail_tokens[0]}"
                )
                tail_tokens = tail_tokens[1:]
            elif len(tail_tokens) != need:
                continue
            for index, token in zip(last_group, tail_tokens, strict=False):
                result[index] = token
            for index in anchored:
                result.setdefault(index, anchor_of[index])
        elif tail_tokens and len(tail_tokens) == len(last_group):
            for index, token in zip(last_group, tail_tokens, strict=True):
                result[index] = token
        elif last_group:
            continue

        if len(result) == len(header_texts):
            for index, text in enumerate(header_texts):
                harvested[text] = result[index]
        return claimed
    return claimed


def build_table_payload(
    page: Any,
    element: dict[str, Any],
    units: list[dict[str, Any]],
    *,
    caption: str = "",
) -> dict[str, Any] | None:
    """把一张表自动重建成生成器认识的结构化载荷。

    网格没把握、或文字格的译文收不齐一半以上，就返回 None 走贴图保底。
    """

    box = normalize_bbox(element.get("bbox"))
    grid = extract_grid(page, element.get("bbox"))
    if not grid.confident or box is None:
        return None

    page_units = [
        unit
        for unit in units
        if isinstance(unit, dict)
        and unit.get("page") == element.get("page")
    ]
    # 收割只用表格自己的单元：短格子拿到整页语料里配，
    # '1.' 会撞上正文里的"表 1."，表头会撞上图题。
    table_units = []
    for unit in page_units:
        ubox = unit.get("source_bbox")
        if not isinstance(ubox, list) or len(ubox) != 4:
            continue
        cx = (ubox[0] + ubox[2]) / 2
        cy = (ubox[1] + ubox[3]) / 2
        if (
            box[0] - 2 <= cx <= box[2] + 2
            and box[1] - 2 <= cy <= box[3] + 2
        ):
            table_units.append(unit)
    harvested: dict[str, str] = {}
    claimed = refine_header_translations(grid, table_units, harvested)
    harvested.update(
        harvest_translations(grid, table_units, claimed=claimed)
    )

    text_cells = {
        cell.text
        for row in grid.rows
        for cell in row
        if not VERBATIM_RE.match(cell.text)
        and not NUMERIC_ONLY_RE.match(cell.text)
    }
    unresolved = sorted(text for text in text_cells if text not in harvested)
    if text_cells and len(unresolved) > len(text_cells) / 2:
        return None

    matrix: list[list[str]] = []
    bold_cells: list[list[bool]] = []
    for row in grid.rows:
        row_texts = [""] * grid.column_count
        row_bold = [False] * grid.column_count
        for cell in row:
            translated = harvested.get(cell.text, cell.text)
            row_texts[cell.column] = translated
            row_bold[cell.column] = cell.bold
        matrix.append(row_texts)
        bold_cells.append(row_bold)

    suppress = sorted(
        {
            str(unit.get("translation") or unit.get("source") or "").strip()
            for unit in page_units
            if isinstance(unit.get("source_bbox"), list)
            and len(unit["source_bbox"]) == 4
            and box[0] <= (unit["source_bbox"][0] + unit["source_bbox"][2]) / 2
            <= box[2]
            and box[1] <= (unit["source_bbox"][1] + unit["source_bbox"][3]) / 2
            <= box[3]
        }
    )
    if caption:
        suppress.append(caption)

    return {
        "id": f"plan-{element.get('id')}-table",
        "page": int(element.get("page") or 0),
        "kind": "structured-table",
        "method": "structured-table-rebuild",
        "status": "ready",
        "source_element_id": str(element.get("id") or ""),
        "source_evidence": [
            f"原文第 {element.get('page')} 页表格元素 {element.get('id')}",
            f"程序抽出 {len(grid.rows)}×{grid.column_count} 网格，"
            f"文字格 {len(text_cells)} 个、锚点收割译文 "
            f"{len(text_cells) - len(unresolved)} 个",
        ],
        "payload": {
            "render_policy": "insert-before",
            "suppress_texts": [text for text in suppress if text],
            "tables": [
                {
                    "title": caption,
                    "rows": matrix,
                    "bold_cells": bold_cells,
                    "header_rows": 1,
                    "page": int(element.get("page") or 0),
                    "source_bbox": list(box),
                    "untranslated_cells": unresolved,
                }
            ],
        },
    }
