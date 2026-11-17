"""公式裁切三步法：内容并集 → 方向边距 → 边缘墨迹检查。

固定边距的老办法（左右 28pt、上下 5pt）对复杂公式不够：求和号上界、
根号顶端、分式的分子分母都可能贴出框外，截出来缺一角还留半行英文。

这里按三步算：

1. **合并真实内容边界。** 收集公式附近的文字 span、绘图对象和行末
   编号，取并集框。完整的句子（中文，或像散文的英文行）不并进来——
   它们是公式的邻居，不是公式的一部分，反而充当扩展的挡板。
2. **加方向不同的安全边距。** 上下 8pt、左右 6pt，只是起点。
3. **做边缘占用检查。** 把区域渲成图，看最外几行像素还有没有墨迹；
   贴边就朝那个方向扩 4pt，最多扩三次。扩到头仍贴边，如实报
   ``FORMULA_REGION_UNCERTAIN``，调用方退到保留更大的整行区域。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

MARGIN_X = 6.0
MARGIN_TOP = 8.0
MARGIN_BOTTOM = 8.0
EDGE_EXPAND_STEP = 4.0
MAX_EDGE_EXPANSIONS = 3
#: 边缘检查看最外几个像素行/列。
EDGE_PIXELS = 2
#: 渲染检查用的缩放（≈150dpi）。
INK_CHECK_SCALE = 150.0 / 72.0
#: 像素灰度低于它算"有墨迹"。
INK_THRESHOLD = 160

STATUS_OK = "OK"
STATUS_UNCERTAIN = "FORMULA_REGION_UNCERTAIN"

CJK_RE = re.compile(r"[㐀-鿿]")
#: 行末公式编号，如 (1) / (12)。
FORMULA_NUMBER_RE = re.compile(r"^\(?\d{1,2}\)?$")
WORD_RE = re.compile(r"[A-Za-z]{2,}")


@dataclass
class FormulaCrop:
    """一次公式裁切的结果与依据。"""

    box: list[float]
    status: str = STATUS_OK
    expansions: list[str] = field(default_factory=list)
    reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "box": list(self.box),
            "status": self.status,
            "expansions": list(self.expansions),
            "reason": self.reason,
        }


def span_is_prose(text: str) -> bool:
    """这一行是句子还是公式碎片。

    句子不并进公式区域：有中文的是译文；四个以上英文单词、
    像散文的英文行是原文说明（例如公式后的 where 从句要是完整句，
    也应当留在正文，不该被公式截图吞掉）。
    """

    stripped = text.strip()
    if not stripped:
        return False
    if CJK_RE.search(stripped):
        return True
    words = WORD_RE.findall(stripped)
    if len(words) >= 4:
        letters = sum(len(word) for word in words)
        # 公式行也可能有 log、exp 这类记号，但散文的字母占比远高于符号。
        return letters >= max(12, 0.55 * len(stripped))
    return False


def _rects_overlap_vertically(a: tuple, b: tuple, slack: float = 2.0) -> bool:
    return a[1] - slack <= b[3] and b[1] - slack <= a[3]


def _union(box: list[float], other: tuple) -> None:
    box[0] = min(box[0], other[0])
    box[1] = min(box[1], other[1])
    box[2] = max(box[2], other[2])
    box[3] = max(box[3], other[3])


def collect_content_box(
    page: Any, seed_box: tuple
) -> tuple[list[float], list[str], tuple[float, float]]:
    """第一步：公式真实内容的并集框。

    返回（并集框，并入内容的说明，上下方的散文挡板 y 坐标）。
    """

    union = [
        float(seed_box[0]),
        float(seed_box[1]),
        float(seed_box[2]),
        float(seed_box[3]),
    ]
    notes: list[str] = []
    page_rect = page.rect
    prose_above = 0.0
    prose_below = float(page_rect.height)

    text = page.get_text("dict")
    for block in text.get("blocks", []):
        for line in block.get("lines", []):
            bbox = line.get("bbox")
            if not bbox:
                continue
            line_text = "".join(
                span.get("text", "") for span in line.get("spans", [])
            ).strip()
            if not line_text:
                continue
            if _rects_overlap_vertically(tuple(seed_box), tuple(bbox)):
                if span_is_prose(line_text):
                    continue
                _union(union, tuple(bbox))
                if FORMULA_NUMBER_RE.match(line_text):
                    notes.append(f"并入行末编号 {line_text!r}")
                else:
                    notes.append(f"并入碎片行 {line_text!r}")
            elif span_is_prose(line_text):
                # 完整句子是挡板：公式区域不越过它们。
                if bbox[3] <= seed_box[1] and bbox[3] > prose_above:
                    prose_above = float(bbox[3])
                elif bbox[1] >= seed_box[3] and bbox[1] < prose_below:
                    prose_below = float(bbox[1])

    for drawing in page.get_drawings():
        rect = drawing.get("rect")
        if rect is None:
            continue
        db = (rect.x0, rect.y0, rect.x1, rect.y1)
        if _rects_overlap_vertically(tuple(seed_box), db) and (
            db[0] <= union[2] + MARGIN_X * 4
            and db[2] >= union[0] - MARGIN_X * 4
        ):
            _union(union, db)
            notes.append("并入绘图对象（根号/分数线等）")

    # 挡板收口：内容并集不越过上下散文
    union[1] = max(union[1], prose_above)
    union[3] = min(union[3], prose_below)
    return union, notes, (prose_above, prose_below)


def _edge_has_ink(samples: Any, width: int, height: int, side: str) -> bool:
    stride = samples if isinstance(samples, bytes) else bytes(samples)
    edge = EDGE_PIXELS

    def dark(x: int, y: int) -> bool:
        return stride[y * width + x] < INK_THRESHOLD

    if side == "top":
        return any(
            dark(x, y) for y in range(min(edge, height)) for x in range(width)
        )
    if side == "bottom":
        return any(
            dark(x, y)
            for y in range(max(0, height - edge), height)
            for x in range(width)
        )
    if side == "left":
        return any(
            dark(x, y) for x in range(min(edge, width)) for y in range(height)
        )
    return any(
        dark(x, y)
        for x in range(max(0, width - edge), width)
        for y in range(height)
    )


def _ink_sides(page: Any, box: list[float]) -> list[str]:
    import fitz

    clip = fitz.Rect(*box) & page.rect
    if clip.is_empty:
        return []
    pix = page.get_pixmap(
        matrix=fitz.Matrix(INK_CHECK_SCALE, INK_CHECK_SCALE),
        clip=clip,
        colorspace=fitz.csGRAY,
    )
    if pix.width < 4 or pix.height < 4:
        return []
    return [
        side
        for side in ("top", "bottom", "left", "right")
        if _edge_has_ink(pix.samples, pix.width, pix.height, side)
    ]


def compute_formula_crop(page: Any, seed_box: tuple) -> FormulaCrop:
    """三步算出公式的最终源区域。"""

    content, notes, (prose_above, prose_below) = collect_content_box(
        page, seed_box
    )
    page_rect = page.rect
    box = [
        max(0.0, content[0] - MARGIN_X),
        max(prose_above, content[1] - MARGIN_TOP),
        min(float(page_rect.width), content[2] + MARGIN_X),
        min(prose_below, content[3] + MARGIN_BOTTOM),
    ]

    expansions: list[str] = []
    limits = {
        "top": prose_above,
        "bottom": prose_below,
        "left": 0.0,
        "right": float(page_rect.width),
    }
    for _round in range(MAX_EDGE_EXPANSIONS):
        inked = _ink_sides(page, box)
        if not inked:
            return FormulaCrop(
                box=box,
                status=STATUS_OK,
                expansions=expansions,
                reason="；".join(notes) or "按检出框加边距即干净",
            )
        grew = False
        for side in inked:
            side_grew = False
            if side == "top" and box[1] > limits["top"]:
                box[1] = max(limits["top"], box[1] - EDGE_EXPAND_STEP)
                side_grew = True
            elif side == "bottom" and box[3] < limits["bottom"]:
                box[3] = min(limits["bottom"], box[3] + EDGE_EXPAND_STEP)
                side_grew = True
            elif side == "left" and box[0] > limits["left"]:
                box[0] = max(limits["left"], box[0] - EDGE_EXPAND_STEP)
                side_grew = True
            elif side == "right" and box[2] < limits["right"]:
                box[2] = min(limits["right"], box[2] + EDGE_EXPAND_STEP)
                side_grew = True
            if side_grew:
                grew = True
                expansions.append(f"{side}+{EDGE_EXPAND_STEP}pt")
        if not grew:
            break

    inked = _ink_sides(page, box)
    if inked:
        return FormulaCrop(
            box=box,
            status=STATUS_UNCERTAIN,
            expansions=expansions,
            reason=(
                f"扩到上限后 {'、'.join(inked)} 边仍有墨迹，"
                "无法确认公式完整；调用方应退到保留整行区域"
            ),
        )
    return FormulaCrop(
        box=box,
        status=STATUS_OK,
        expansions=expansions,
        reason="；".join(notes) or "边缘扩展后干净",
    )


def full_line_fallback_box(page: Any, seed_box: tuple) -> list[float]:
    """不确定时的保底：同一竖向带的整行区域（版心整宽）。

    带子碰到哪一行，就把那一行**整行**并进来，迭代到稳定——
    宁可多保几行完整的原文，也不能出现被水平切成半截的字迹。
    """

    page_rect = page.rect
    y0 = max(0.0, float(seed_box[1]) - MARGIN_TOP)
    y1 = min(float(page_rect.height), float(seed_box[3]) + MARGIN_BOTTOM)

    lines: list[tuple[float, float]] = []
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            bbox = line.get("bbox")
            if bbox and "".join(
                span.get("text", "") for span in line.get("spans", [])
            ).strip():
                lines.append((float(bbox[1]), float(bbox[3])))

    changed = True
    while changed:
        changed = False
        for top, bottom in lines:
            if top < y1 and bottom > y0 and (top < y0 or bottom > y1):
                y0 = min(y0, top)
                y1 = max(y1, bottom)
                changed = True
    return [
        0.0,
        max(0.0, y0 - 2.0),
        float(page_rect.width),
        min(float(page_rect.height), y1 + 2.0),
    ]


def formula_render_box(page: Any, seed_box: tuple) -> list[float]:
    """生成器与核查层共用的最终渲染框。

    两边必须调同一个函数：渲染按什么框画，核查就按什么框比，
    否则指纹必然失配。不确定时统一退到整行保底框。
    """

    crop = compute_formula_crop(page, seed_box)
    if crop.status == STATUS_UNCERTAIN:
        return full_line_fallback_box(page, seed_box)
    return crop.box
