"""脚注渲染器。

脚注有一件事最容易做错：把它当成一段普通文字。一旦当成普通文字，
它就会插进正文中间把句子劈成两半，或者被一股脑堆到全文末尾——两种做法
都让"正文里那个小小的 1"失去意义，读者顺着编号找不回来。

所以脚注在这里是**页底的一块独立区域**：正文下方、有分隔线、字号比正文小
但不低于可读门槛、编号与本页正文里的上标一一对应，并且绝不与参考文献
列表混在一起。
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import BBox, normalize_bbox

MODE_FOOTNOTE_ZONE = "page-bottom-footnote-zone"

#: 脚注字号下限。再小就不叫可读了。
MIN_FOOTNOTE_FONT_PT = 7.5
#: 脚注字号相对正文的上限。脚注必须**看起来就是**脚注。
MAX_BODY_RATIO = 0.90
#: 分隔线宽度占版心的比例。学术排版的惯例是短短一条，不是通栏。
SEPARATOR_WIDTH_RATIO = 0.30
#: 分隔线与脚注文字之间的间距（点）。
SEPARATOR_GAP_PT = 4.0
#: 正文底部与分隔线之间的间距（点）。
BODY_GAP_PT = 8.0
#: 脚注行距系数。
LINE_LEADING = 1.30

#: 脚注开头的编号：1、(1)、1. 都算。
MARKER_RE = re.compile(r"^\s*\(?(\d{1,3})\)?[.)]?\s+")
#: 正文里的上标编号必须比正文小这么多，才算上标而不是普通数字。
SUPERSCRIPT_SIZE_RATIO = 0.85


class FootnoteRenderError(RuntimeError):
    """脚注渲染失败。"""


@dataclass
class FootnoteEntry:
    """一条脚注。"""

    element_id: str
    marker: str
    translation: str
    translation_unit_id: str
    #: 正文里那个上标所在的页。脚注必须跟着它走，不能堆到别处。
    marker_page: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RenderedFootnotes:
    """一页脚注的渲染结果与证据。"""

    candidate_page: int
    area_bbox: list[float]
    separator_bbox: list[float]
    font_size: float
    body_font_size: float
    entries: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    mode: str = MODE_FOOTNOTE_ZONE

    @property
    def markers(self) -> list[str]:
        return [str(entry["marker"]) for entry in self.entries]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["markers"] = self.markers
        return data


def split_footnote_entries(text: str) -> list[tuple[str, str]]:
    """把一块脚注文字拆成一条一条。

    抽取出来的脚注区常常是"1 …\\n2 …\\n3 …"连在一起的一整块。
    不拆开就没法逐条核对编号，也没法保证每条都跟得上正文。
    """

    entries: list[tuple[str, str]] = []
    marker: str | None = None
    buffer: list[str] = []
    for raw_line in str(text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = MARKER_RE.match(line)
        if match:
            if marker is not None:
                entries.append((marker, " ".join(buffer).strip()))
            marker = match.group(1)
            buffer = [line[match.end():].strip()]
        elif marker is not None:
            buffer.append(line)
    if marker is not None:
        entries.append((marker, " ".join(buffer).strip()))
    return entries


def footnote_font_size(
    body_font_size: float,
    *,
    source_font_size: float | None = None,
    min_pt: float = MIN_FOOTNOTE_FONT_PT,
) -> float:
    """脚注字号：比正文小，但不低于可读门槛。

    两条约束会打架——正文本来就小的时候，"比正文小"会把脚注压到看不清。
    这时以可读门槛为准，字号相等由调用方按警告处理，不偷偷缩下去。
    """

    if body_font_size <= 0:
        raise FootnoteRenderError("正文字号必须为正数")
    target = body_font_size * MAX_BODY_RATIO
    if source_font_size and source_font_size > 0:
        target = min(target, float(source_font_size))
    return round(max(target, min_pt), 2)


def body_marker_numbers(
    page: Any,
    *,
    body_bbox: Any = None,
    body_font_size: float,
) -> list[str]:
    """找出正文里的上标编号。

    判据是**字号明显小于正文的纯数字**。页码、公式编号不在正文区域里，
    所以配合 ``body_bbox`` 一起用。
    """

    import fitz

    box = normalize_bbox(body_bbox)
    clip = fitz.Rect(*box) if box else None
    found: list[str] = []
    data = page.get_text("dict", clip=clip)
    ceiling = body_font_size * SUPERSCRIPT_SIZE_RATIO
    for block in data.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = str(span.get("text") or "").strip()
                if not text.isdigit():
                    continue
                if float(span.get("size") or 0.0) > ceiling:
                    continue
                if text not in found:
                    found.append(text)
    return found


def check_marker_consistency(
    footnote_markers: list[str], body_markers: list[str]
) -> list[str]:
    """脚注编号必须与正文里的上标对得上，一个不多一个不少。"""

    problems: list[str] = []
    missing = [m for m in footnote_markers if m not in body_markers]
    if missing:
        problems.append(
            "脚注编号 " + "、".join(missing) + " 在本页正文里找不到对应的上标"
        )
    orphan = [m for m in body_markers if m not in footnote_markers]
    if orphan:
        problems.append(
            "正文上标 " + "、".join(orphan) + " 在本页脚注区里没有对应的脚注"
        )
    return problems


def _wrap(font: Any, text: str, font_size: float, width: float) -> list[str]:
    """按实际字宽折行。中文没有空格，所以逐字累加，不按词切。"""

    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if font.text_length(candidate, fontsize=font_size) > width and current:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [""]


def render_footnotes(
    candidate_page: Any,
    entries: list[FootnoteEntry],
    *,
    body_bottom: float,
    font_path: str,
    body_font_size: float = 10.0,
    source_font_size: float | None = None,
    left_margin: float = 60.0,
    right_margin: float = 60.0,
    bottom_margin: float = 50.0,
) -> RenderedFootnotes:
    """把一页的脚注画在页底独立区域里。

    ``body_bottom`` 是正文最后一行的下边缘。脚注区从这里往下排，
    与正文之间隔一条分隔线——这是"不打断正文句子"的实现方式：
    脚注根本不进入正文的行流。
    """

    import fitz

    if not entries:
        raise FootnoteRenderError("没有脚注可渲染")

    page_rect = candidate_page.rect
    font_size = footnote_font_size(
        body_font_size, source_font_size=source_font_size
    )
    warnings: list[str] = []
    if font_size >= body_font_size:
        warnings.append(
            f"正文字号 {body_font_size:.1f} 太小，脚注为保住可读门槛 "
            f"{MIN_FOOTNOTE_FONT_PT:.1f} 只能取 {font_size:.1f}，未能小于正文"
        )

    try:
        font = fitz.Font(fontfile=font_path)
    except Exception as exc:  # noqa: BLE001 - 字体加载失败必须显式报出
        raise FootnoteRenderError(f"脚注字体加载失败: {font_path}: {exc}") from exc

    content_width = page_rect.width - left_margin - right_margin
    laid_out: list[tuple[FootnoteEntry, list[str]]] = []
    for entry in entries:
        if not str(entry.translation_unit_id or "").strip():
            raise FootnoteRenderError(
                f"{entry.element_id}: 脚注第 {entry.marker} 条没有绑定 "
                "translation_unit_id"
            )
        text = f"{entry.marker} {entry.translation}".strip()
        laid_out.append((entry, _wrap(font, text, font_size, content_width)))

    total_lines = sum(len(lines) for _, lines in laid_out)
    text_height = total_lines * font_size * LINE_LEADING
    area_top = page_rect.height - bottom_margin - text_height - SEPARATOR_GAP_PT
    separator_y = area_top

    if separator_y < body_bottom + BODY_GAP_PT:
        raise FootnoteRenderError(
            f"脚注区顶边 {separator_y:.1f} 会压到正文底边 {body_bottom:.1f}，"
            "脚注不得打断正文；应由页面合成器把正文行流上移或换页"
        )

    separator_bbox = [
        left_margin,
        separator_y,
        left_margin + content_width * SEPARATOR_WIDTH_RATIO,
        separator_y,
    ]
    candidate_page.draw_line(
        fitz.Point(separator_bbox[0], separator_y),
        fitz.Point(separator_bbox[2], separator_y),
        width=0.5,
    )

    writer = fitz.TextWriter(page_rect)
    cursor = separator_y + SEPARATOR_GAP_PT
    rendered_entries: list[dict[str, Any]] = []
    for entry, lines in laid_out:
        entry_top = cursor
        for line in lines:
            cursor += font_size * LINE_LEADING
            writer.append(
                fitz.Point(left_margin, cursor), line, font=font, fontsize=font_size
            )
        rendered_entries.append(
            {
                **entry.as_dict(),
                "lines": len(lines),
                "bbox": [
                    left_margin,
                    entry_top,
                    left_margin + content_width,
                    cursor,
                ],
            }
        )
    writer.write_text(candidate_page)

    return RenderedFootnotes(
        candidate_page=candidate_page.number + 1,
        area_bbox=[
            left_margin,
            separator_y,
            left_margin + content_width,
            cursor,
        ],
        separator_bbox=separator_bbox,
        font_size=font_size,
        body_font_size=float(body_font_size),
        entries=rendered_entries,
        warnings=warnings,
    )


def verify_footnote_output(
    rendered: RenderedFootnotes,
    candidate_page: Any,
    *,
    body_bbox: Any = None,
    reference_bbox: Any = None,
) -> list[str]:
    """核对脚注有没有真的落在它该在的地方。

    逐条读候选页面，不看渲染器自己的记录。
    """

    import fitz

    problems: list[str] = []

    if rendered.font_size < MIN_FOOTNOTE_FONT_PT:
        problems.append(
            f"脚注字号 {rendered.font_size:.1f} 低于可读门槛 "
            f"{MIN_FOOTNOTE_FONT_PT:.1f}"
        )
    if rendered.font_size >= rendered.body_font_size:
        problems.append(
            f"脚注字号 {rendered.font_size:.1f} 不小于正文字号 "
            f"{rendered.body_font_size:.1f}"
        )

    horizontal = [
        drawing
        for drawing in candidate_page.get_drawings()
        if drawing.get("rect") is not None
        and abs(fitz.Rect(drawing["rect"]).height) < 1.0
        and abs(fitz.Rect(drawing["rect"]).y0 - rendered.separator_bbox[1]) < 2.0
    ]
    if not horizontal:
        problems.append("脚注区上方没有分隔线，脚注与正文分不开")

    body = normalize_bbox(body_bbox)
    if body is not None and rendered.area_bbox[1] < body[3]:
        problems.append(
            f"脚注区顶边 {rendered.area_bbox[1]:.1f} 侵入正文区域 "
            f"（正文底边 {body[3]:.1f}），会打断正文"
        )

    reference = normalize_bbox(reference_bbox)
    if reference is not None and _overlaps(rendered.area_bbox, reference):
        problems.append("脚注区与参考文献列表重叠，脚注不得混进参考文献")

    for entry in rendered.entries:
        if int(entry.get("marker_page") or 0) != rendered.candidate_page:
            problems.append(
                f"脚注 {entry['marker']} 在候选第 {rendered.candidate_page} 页，"
                f"正文标记在第 {entry.get('marker_page')} 页，"
                "脚注必须与它的标记同页，不得堆到全文末尾"
            )
        found = candidate_page.get_text(
            "text", clip=fitz.Rect(*entry["bbox"])
        ).strip()
        if entry["marker"] not in found:
            problems.append(
                f"脚注编号 {entry['marker']} 没有出现在它自己的区域里"
            )
    return problems


def _overlaps(box: list[float], other: BBox) -> bool:
    return not (
        box[2] <= other[0]
        or box[0] >= other[2]
        or box[3] <= other[1]
        or box[1] >= other[3]
    )
