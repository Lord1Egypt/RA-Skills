"""Story 构建的第一层：正文单元、跨页合并、保留题录。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。这一层只处理**文字**：
段落样式、单元 Flowable、行片段合并判定、保留区域的题录排版。表格、图片、
复杂图和整篇 Story 的装配分别在 ``story_visual``、``story_complex``、
``story`` 里，按依赖方向单向叠加，不互相回指。

原来的 scripts 层依赖按包内规则改写：异常改成本模块自己的 ``StoryError``，
由调用侧翻译回 SkillError；界面文案、CJK 段落样式和几个作业数据判定函数
由调用侧用 ``StoryDeps`` 一次性注入。

本模块略超 800 行，暂时不再拆：多出来的部分几乎全是 ``_styles`` 里的
样式表和跨页合并的一组判定函数。样式表是一整张表，拆开就要在两个文件
之间对着看；合并判定的几个函数只被 ``_joined_unit_flowables`` 用，
搬走就变成没人再看的孤儿。等样式表能按用途分组之后再拆。
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable, Paragraph, Spacer
from reportlab.platypus.flowables import HRFlowable

from .font_runs import SUPERSCRIPT_PATTERN_CLASS, _markup
from .mapping import MappingAnchor
from .reference_data import REFERENCE_CATEGORIES
from .text_blocks import HEADING_KINDS, REFERENCE_KINDS
from .text_blocks import looks_like_heading as _looks_like_heading
from .text_blocks import role_may_head as _role_may_head
from .text_blocks import unit_text_blocks as _unit_text_blocks

#: 正文与脚注区之间的间距（点）。
FOOTNOTE_ZONE_GAP_PT = 8.0
#: 脚注分隔线的宽度占版心的比例。学术排版的惯例是短短一条，不是通栏。
FOOTNOTE_SEPARATOR_WIDTH = "30%"
#: 分隔线与脚注文字之间的间距（点）。
FOOTNOTE_SEPARATOR_GAP_PT = 4.0


class StoryError(RuntimeError):
    """Story 构建过程中的数据错误。

    以前抛的是 scripts 层的 SkillError；包不该依赖 scripts，所以这里
    自己定义。调用侧把它翻译回 SkillError，文案原样透传，对外行为不变。
    """


@dataclass(frozen=True)
class StoryDeps:
    """Story 构建需要的、原本长在 scripts 层的几件东西。

    都是纯函数或纯文案，一次注入，沿调用链往下传。这样包内不必 import
    scripts，同时"这段代码到底依赖外面什么"也一眼看得见。
    """

    #: 取界面文案：``message(target_language, key)``。
    message_fn: Callable[..., str]
    #: 取 PyMuPDF 模块，缺依赖时由它抛出统一提示。
    import_fitz_fn: Callable[[], Any]
    #: 建 CJK 段落样式，全项目只有一处定义。
    make_cjk_style_fn: Callable[..., ParagraphStyle]
    #: 从文本里去掉被抑制的片段。
    remove_suppressed_texts_fn: Callable[[str, Iterable[Any]], str]
    #: 判定一个单元是不是原文页眉页脚这类无语义家具。
    is_nonsemantic_furniture_fn: Callable[..., bool]
    #: 算出被复杂内容载荷顶替掉的单元 id。
    complex_replaced_unit_ids_fn: Callable[..., set[str]]
    #: 列出一条复杂内容覆盖到的原文页码。
    complex_item_source_pages_fn: Callable[[dict[str, Any]], set[int]]
    #: 把保留区域载荷按页分组并排好序。
    retained_regions_by_page_fn: Callable[
        [list[dict[str, Any]]],
        dict[int, list[dict[str, Any]]],
    ]


def _styles(
    *,
    deps: StoryDeps,
    regular_font: str,
    bold_font: str,
    reference_font: str,
    body_font_pt: float,
    leading_ratio: float,
    reference_font_pt: float,
) -> dict[str, ParagraphStyle]:
    # 正文基样式由通用流排层定义，生成器只补上自己的正文颜色。
    # 这样"CJK 段落样式"在全项目只有一处定义。
    body = deps.make_cjk_style_fn(
        "body",
        font_name=regular_font,
        font_size=body_font_pt,
        leading_ratio=leading_ratio,
        alignment=TA_LEFT,
        first_line_indent_em=2,
        space_after_em=0.62,
    )
    body.textColor = colors.HexColor("#1A2025")
    return {
        "body": body,
        "body_no_indent": ParagraphStyle(
            "body-no-indent",
            parent=body,
            firstLineIndent=0,
        ),
        "metadata": ParagraphStyle(
            "metadata",
            parent=body,
            firstLineIndent=0,
            leading=body_font_pt * 1.5,
            spaceAfter=body_font_pt * 0.35,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=body,
            fontName=bold_font,
            fontSize=body_font_pt * 1.42,
            leading=body_font_pt * leading_ratio * 1.18,
            firstLineIndent=0,
            spaceBefore=body_font_pt * 0.55,
            spaceAfter=body_font_pt * 0.72,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=body,
            fontName=bold_font,
            fontSize=body_font_pt * 1.22,
            leading=body_font_pt * leading_ratio * 1.08,
            firstLineIndent=0,
            spaceBefore=body_font_pt * 0.48,
            spaceAfter=body_font_pt * 0.58,
            keepWithNext=True,
        ),
        "title": ParagraphStyle(
            "title",
            parent=body,
            fontName=bold_font,
            fontSize=body_font_pt * 1.72,
            leading=body_font_pt * leading_ratio * 1.35,
            alignment=TA_CENTER,
            firstLineIndent=0,
            spaceBefore=body_font_pt * 0.8,
            spaceAfter=body_font_pt * 1.0,
            keepWithNext=True,
        ),
        "reference": ParagraphStyle(
            "reference",
            parent=body,
            fontName=reference_font,
            fontSize=reference_font_pt,
            leading=reference_font_pt * 1.5,
            leftIndent=reference_font_pt * 1.5,
            firstLineIndent=-reference_font_pt * 1.5,
            spaceAfter=reference_font_pt * 0.42,
        ),
        "source_anchor": ParagraphStyle(
            "source-anchor",
            fontName=regular_font,
            fontSize=7.4,
            leading=9.2,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#68737B"),
            spaceBefore=4,
            spaceAfter=5,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=body,
            fontSize=max(8.0, body_font_pt * 0.82),
            leading=max(11.5, body_font_pt * 1.18),
            firstLineIndent=0,
            alignment=TA_CENTER,
            spaceAfter=body_font_pt * 0.55,
            keepWithNext=True,
        ),
        "table": ParagraphStyle(
            "table",
            parent=body,
            fontSize=max(8.2, body_font_pt * 0.82),
            leading=max(11.0, body_font_pt * 1.1),
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceAfter=0,
        ),
        "table_header": ParagraphStyle(
            "table-header",
            parent=body,
            fontName=bold_font,
            fontSize=max(8.2, body_font_pt * 0.82),
            leading=max(11.0, body_font_pt * 1.1),
            firstLineIndent=0,
            alignment=TA_CENTER,
            spaceAfter=0,
        ),
        "table_note": ParagraphStyle(
            "table-note",
            parent=body,
            fontSize=max(8.2, body_font_pt * 0.82),
            leading=max(11.8, body_font_pt * 1.18),
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=body_font_pt * 0.35,
            spaceAfter=body_font_pt * 0.25,
        ),
    }


def _unit_flowables(
    unit: dict[str, Any],
    styles: dict[str, ParagraphStyle],
    suppress_texts: Iterable[str] = (),
    *,
    deps: StoryDeps,
    text_override: str | None = None,
    kind_override: str | None = None,
    include_start: bool = True,
    include_end: bool = True,
) -> list[Flowable]:
    source_page = int(unit["page"])
    unit_id = str(unit["id"])
    text = deps.remove_suppressed_texts_fn(
        (
            str(text_override).strip()
            if text_override is not None
            else str(
                unit.get("translation")
                or unit.get("source")
                or ""
            ).strip()
        ),
        suppress_texts,
    )
    if unit.get("_suppressed_reason"):
        # 结构化抑制：单元照常入映射（锚点还在），但不排任何文字。
        # 名单与理由记录在 generator-layout-log.json 的 suppressed_units。
        text = ""
    elif unit.get("_decoded_math") and text_override is None:
        text = str(unit["_decoded_math"])
    result: list[Flowable] = []
    keep_end_with_next = False
    if include_start:
        result.append(MappingAnchor("start", "unit", unit_id, source_page))
    blocks = _unit_text_blocks(unit, text)
    kind = str(kind_override or unit.get("kind") or "").lower()
    layout_role = str(unit.get("_layout_role") or "").lower()
    if unit.get("_footnote_zone_start") and blocks:
        result.append(Spacer(1, FOOTNOTE_ZONE_GAP_PT))
        result.append(
            HRFlowable(
                width=FOOTNOTE_SEPARATOR_WIDTH,
                thickness=0.5,
                color=colors.grey,
                spaceAfter=FOOTNOTE_SEPARATOR_GAP_PT,
                hAlign="LEFT",
            )
        )
    for index, block in enumerate(blocks):
        if unit.get("_element_role") == "footnote":
            # 脚注不是正文：字号小一档、无缩进。分隔线由页面单元的
            # 首个脚注前插入（见 _unit_flowables 调用侧）。
            style = styles["table_note"]
        elif layout_role in {
            "publication-metadata",
            "formal-citation-footer",
        }:
            style = styles["metadata"]
        elif kind in REFERENCE_KINDS or unit.get("keep_source_reason"):
            style = styles["reference"]
        elif (
            index == 0
            and (
                kind == "title"
                or unit.get("_element_role") == "document-title"
            )
            and _role_may_head(unit)
        ):
            style = styles["title"]
        elif (
            kind in HEADING_KINDS or unit.get("heading_level") == 1
        ) and _role_may_head(unit):
            style = styles["h1"]
        elif unit.get("heading_level") == 2 and _role_may_head(unit):
            style = styles["h2"]
        elif (
            kind in {"", "text", "unknown"}
            and _looks_like_heading(block)
            and unit.get("_element_role")
            in (None, "", "heading", "document-title")
        ):
            # 绑定角色已知且不是标题的，启发式没有提升权：
            # 作者单位、arXiv 版本戳、图内标签长得再像标题也不是标题。
            style = styles["h2"]
        elif block.startswith(("图", "表", "注", "DOI", "doi")):
            style = styles["body_no_indent"]
        else:
            style = styles["body"]
        result.append(
            Paragraph(
                _markup(
                    block,
                    cjk_font=(
                        styles["body"].fontName
                        if style is styles["reference"]
                        else None
                    ),
                    primary_font=(
                        style.fontName
                        if style is styles["reference"]
                        else None
                    ),
                ),
                style,
            )
        )
        keep_end_with_next = bool(
            getattr(style, "keepWithNext", False)
        )
    if include_end:
        result.append(
            MappingAnchor(
                "end",
                "unit",
                unit_id,
                source_page,
                keep_with_next=keep_end_with_next,
            )
        )
    return result


def _line_fragment_bbox(
    unit: dict[str, Any],
) -> tuple[float, float, float, float] | None:
    bbox = unit.get("source_bbox")
    if (
        not isinstance(bbox, list)
        or len(bbox) != 4
        or not all(isinstance(value, (int, float)) for value in bbox)
    ):
        return None
    x0, y0, x1, y1 = map(float, bbox)
    if x1 <= x0 or y1 <= y0 or y1 - y0 > 38.0:
        return None
    return x0, y0, x1, y1


def _line_fragment_role(unit: dict[str, Any]) -> str | None:
    if (
        not str(unit.get("translation") or "").strip()
        or str(unit.get("keep_source_reason") or "").strip()
        or "\n" in str(unit.get("source") or "").strip()
        or _line_fragment_bbox(unit) is None
    ):
        return None
    kind = str(unit.get("kind") or "").lower()
    if kind in HEADING_KINDS:
        return "heading"
    if kind == "body":
        return "body"
    return None


def _source_ends_paragraph(text: str) -> bool:
    compact = re.sub(
        rf"(?:\s*(?:\d{{1,3}}|[{SUPERSCRIPT_PATTERN_CLASS}]+))+$",
        "",
        str(text or "").rstrip(),
    )
    return bool(re.search(r'[.!?。！？][”’"\']?$', compact))


def _starts_with_latin_upper(text: str) -> bool:
    match = re.search(r"[A-Za-z]", str(text or ""))
    return bool(match and match.group(0).isupper())


def _unit_bbox(
    unit: dict[str, Any],
) -> tuple[float, float, float, float] | None:
    bbox = unit.get("source_bbox")
    if (
        not isinstance(bbox, list)
        or len(bbox) != 4
        or not all(isinstance(value, (int, float)) for value in bbox)
    ):
        return None
    x0, y0, x1, y1 = map(float, bbox)
    if x1 <= x0 or y1 <= y0:
        return None
    return x0, y0, x1, y1


def _is_bottom_note_unit(
    unit: dict[str, Any],
    *,
    page_height: float,
) -> bool:
    bbox = _unit_bbox(unit)
    if bbox is None:
        return False
    source = str(unit.get("source") or "").strip()
    return bool(
        bbox[1] >= page_height * 0.72
        and re.match(r"^(?:\d{1,3}|[*†‡])(?:\s|https?://)", source)
    )


def _is_cross_page_continuation(
    previous: dict[str, Any],
    following: dict[str, Any],
    *,
    previous_page_width: float,
    previous_page_height: float,
    following_page_width: float,
    following_page_height: float,
) -> bool:
    if (
        str(previous.get("kind") or "").lower() != "body"
        or str(following.get("kind") or "").lower() != "body"
        or int(following.get("page") or 0)
        != int(previous.get("page") or 0) + 1
    ):
        return False
    previous_bbox = _unit_bbox(previous)
    following_bbox = _unit_bbox(following)
    if previous_bbox is None or following_bbox is None:
        return False
    px0, _py0, px1, py1 = previous_bbox
    fx0, fy0, fx1, _fy1 = following_bbox
    if (
        py1 < previous_page_height * 0.68
        or fy0 > following_page_height * 0.25
    ):
        return False
    overlap = min(px1, fx1) - max(px0, fx0)
    minimum_width = min(px1 - px0, fx1 - fx0)
    same_column = (
        overlap >= minimum_width * 0.45
        and abs(px0 - fx0) <= max(
            28.0,
            min(previous_page_width, following_page_width) * 0.06,
        )
    )
    column_wrap = (
        px0 >= previous_page_width * 0.45
        and fx0 <= following_page_width * 0.25
        and abs((px1 - px0) - (fx1 - fx0))
        <= max(
            28.0,
            min(px1 - px0, fx1 - fx0) * 0.18,
        )
    )
    if not same_column and not column_wrap:
        return False
    if not column_wrap and abs(px0 - fx0) > max(
        28.0,
        min(previous_page_width, following_page_width) * 0.06,
    ):
        return False
    previous_source = str(previous.get("source") or "").strip()
    following_source = str(following.get("source") or "").strip()
    previous_target = str(previous.get("translation") or "").strip()
    following_target = str(following.get("translation") or "").strip()
    return not (
        len(previous_source) < 12
        or len(following_source) < 4
        or len(previous_target) < 4
        or len(following_target) < 2
        or _source_ends_paragraph(previous_source)
        or _source_ends_paragraph(previous_target)
    )


def _should_join_line_fragment(
    run: list[dict[str, Any]],
    next_unit: dict[str, Any],
    *,
    page_width: float,
) -> bool:
    if not run or len(run) >= 24:
        return False
    current = run[-1]
    if current.get("page") != next_unit.get("page"):
        return False
    role = _line_fragment_role(current)
    if role is None or role != _line_fragment_role(next_unit):
        return False
    current_bbox = _line_fragment_bbox(current)
    next_bbox = _line_fragment_bbox(next_unit)
    if current_bbox is None or next_bbox is None:
        return False
    cx0, cy0, cx1, cy1 = current_bbox
    nx0, ny0, nx1, ny1 = next_bbox
    current_height = cy1 - cy0
    next_height = ny1 - ny0
    line_step = ny0 - cy0
    if (
        line_step <= max(current_height, next_height) * 0.55
        or line_step
        > max(34.0, max(current_height, next_height) * 2.25)
    ):
        return False
    horizontal_overlap = min(cx1, nx1) - max(cx0, nx0)
    if horizontal_overlap < min(cx1 - cx0, nx1 - nx0) * 0.2:
        return False
    current_source = str(current.get("source") or "").strip()
    next_source = str(next_unit.get("source") or "").strip()
    if role == "heading":
        return bool(
            len(run) < 3
            and current.get("heading_level")
            == next_unit.get("heading_level")
            and not _source_ends_paragraph(current_source)
        )

    current_width = cx1 - cx0
    next_width = nx1 - nx0
    if current_width < max(120.0, page_width * 0.42):
        return False
    group_left = min(
        float(_line_fragment_bbox(unit)[0])
        for unit in run
        if _line_fragment_bbox(unit) is not None
    )
    if (
        _source_ends_paragraph(current_source)
        and nx0 - group_left > max(16.0, page_width * 0.03)
    ):
        return False
    if (
        _source_ends_paragraph(current_source)
        and next_source.startswith(("(", "[", "（", "【"))
    ):
        return False
    return not (
        _source_ends_paragraph(current_source)
        and next_width < page_width * 0.3
        and _starts_with_latin_upper(next_source)
    )


def _join_target_fragments(
    values: Iterable[str],
    *,
    target_language: str,
) -> str:
    fragments = [str(value).strip() for value in values if str(value).strip()]
    if not fragments:
        return ""
    cjk_target = target_language.startswith(("zh", "ja", "ko"))
    result = fragments[0]
    for fragment in fragments[1:]:
        separator = ""
        if not cjk_target or (
            re.search(r"[A-Za-z0-9&,;:]$", result)
            and re.match(r"[A-Za-z0-9]", fragment)
        ):
            separator = " "
        result += separator + fragment
    return result


def _joined_unit_flowables(
    units: list[dict[str, Any]],
    styles: dict[str, ParagraphStyle],
    suppress_texts: Iterable[str],
    *,
    deps: StoryDeps,
    target_language: str,
) -> list[Flowable]:
    if not units:
        return []
    result: list[Flowable] = [
        MappingAnchor(
            "start",
            "unit",
            str(unit["id"]),
            int(unit["page"]),
        )
        for unit in units
    ]
    combined_text = _join_target_fragments(
        (
            deps.remove_suppressed_texts_fn(
                str(unit.get("translation") or unit.get("source") or ""),
                suppress_texts,
            )
            # 结构化抑制的单元（数学字体残渣、标题续行重复）不进合并文本；
            # 解码过的数学字形用解码结果。锚点都发过，映射不受影响。
            if not unit.get("_suppressed_reason")
            and not unit.get("_decoded_math")
            else str(unit.get("_decoded_math") or "")
            for unit in units
        ),
        target_language=target_language,
    )
    content_flowables = _unit_flowables(
        units[0],
        styles,
        deps=deps,
        text_override=combined_text,
        include_start=False,
        include_end=False,
    )
    result.extend(content_flowables)
    keep_end_with_next = bool(
        content_flowables
        and callable(
            getattr(content_flowables[-1], "getKeepWithNext", None)
        )
        and content_flowables[-1].getKeepWithNext()
    )
    result.extend(
        MappingAnchor(
            "end",
            "unit",
            str(unit["id"]),
            int(unit["page"]),
            keep_with_next=keep_end_with_next,
        )
        for unit in units
    )
    return result


def _unit_fully_covered_by_retained(
    unit: dict[str, Any],
    retained_payloads: Iterable[dict[str, Any]],
    *,
    tolerance: float = 2.0,
) -> bool:
    if not str(unit.get("keep_source_reason") or "").strip():
        return False
    source_bbox = unit.get("source_bbox")
    if (
        not isinstance(source_bbox, list)
        or len(source_bbox) != 4
        or not all(isinstance(value, (int, float)) for value in source_bbox)
    ):
        return False
    x0, y0, x1, y1 = map(float, source_bbox)
    for payload in retained_payloads:
        if (
            not isinstance(payload, dict)
            or payload.get("already_present_in_translation") is True
            or not payload.get("blocks")
        ):
            continue
        bbox = payload.get("effective_bbox") or payload.get("bbox")
        if (
            not isinstance(bbox, list)
            or len(bbox) != 4
            or not all(isinstance(value, (int, float)) for value in bbox)
        ):
            continue
        rx0, ry0, rx1, ry1 = map(float, bbox)
        if (
            x0 >= rx0 - tolerance
            and y0 >= ry0 - tolerance
            and x1 <= rx1 + tolerance
            and y1 <= ry1 + tolerance
        ):
            return True
    return False


def _retained_heading_label(deps: StoryDeps, target_language: str) -> str:
    return deps.message_fn(target_language, "retained_references")


def _retained_flowables(
    payload: dict[str, Any],
    *,
    deps: StoryDeps,
    styles: dict[str, ParagraphStyle],
    target_language: str,
    include_reference_heading: bool,
    reference_text_transform: Any = None,
) -> list[Flowable]:
    if payload.get("already_present_in_translation") is True:
        return []
    result: list[Flowable] = []
    category = str(payload.get("category") or "")
    has_source_heading = any(
        isinstance(block, dict) and block.get("role") == "heading"
        for block in payload.get("blocks", [])
    )
    if (
        category in REFERENCE_CATEGORIES
        and include_reference_heading
        and not has_source_heading
    ):
        result.append(
            Paragraph(
                _markup(_retained_heading_label(deps, target_language)),
                styles["h2"],
            )
        )
    for block in payload.get("blocks", []):
        if not isinstance(block, dict):
            continue
        text = str(block.get("text") or "").strip()
        if not text:
            continue
        if (
            reference_text_transform is not None
            and category in REFERENCE_CATEGORIES
        ):
            # 参考文献保留的是原文，但行末软断词（net-\nworks）和被折行
            # 切断的 URL 是排版伪影，不是内容——按文档词表拼回去。
            # 必须从 raw_text（带换行）判，清理后的文本已把伪影固化。
            text = reference_text_transform(
                str(block.get("raw_text") or "") or text
            )
            if not text:
                continue
        if block.get("role") == "heading" and category in REFERENCE_CATEGORIES:
            if include_reference_heading:
                result.append(
                    Paragraph(
                        _markup(_retained_heading_label(deps, target_language)),
                        styles["h2"],
                    )
                )
        else:
            result.append(
                Paragraph(
                    _markup(
                        text,
                        cjk_font=(
                            styles["body"].fontName
                            if category in REFERENCE_CATEGORIES
                            else None
                        ),
                        primary_font=(
                            styles["reference"].fontName
                            if category in REFERENCE_CATEGORIES
                            else None
                        ),
                    ),
                    (
                        styles["reference"]
                        if category in REFERENCE_CATEGORIES
                        else styles["body_no_indent"]
                    ),
                )
            )
    return result


def _retained_render_policy(
    payload: dict[str, Any],
    page_height: float,
) -> str:
    explicit = payload.get("render_policy")
    if explicit in {"insert-before", "insert-after"}:
        return str(explicit)
    if str(payload.get("category") or "") in REFERENCE_CATEGORIES:
        return "insert-after"
    bbox = payload.get("effective_bbox") or payload.get("bbox") or [0, 0, 0, 0]
    return "insert-before" if float(bbox[1]) < page_height * 0.35 else "insert-after"


def _retained_references_precede_visible_units(
    page_units: list[dict[str, Any]],
    page_retained: list[dict[str, Any]],
    page_complex: list[dict[str, Any]],
    *,
    deps: StoryDeps,
    page_width: float | None = None,
    page_height: float | None = None,
    tolerance: float = 2.0,
) -> bool:
    references = [
        payload
        for payload in page_retained
        if (
            isinstance(payload, dict)
            and str(payload.get("category") or "") in REFERENCE_CATEGORIES
            and payload.get("blocks")
        )
    ]
    if not references:
        return False

    complex_replaced_unit_ids = deps.complex_replaced_unit_ids_fn(
        page_units,
        page_complex,
    )
    visible_units: list[dict[str, Any]] = []
    for unit in page_units:
        if (
            not isinstance(unit, dict)
            or not str(unit.get("translation") or "").strip()
            or _unit_fully_covered_by_retained(unit, page_retained)
            or deps.is_nonsemantic_furniture_fn(
                unit,
                page_width=page_width,
                page_height=page_height,
            )
            or str(unit.get("id") or "") in complex_replaced_unit_ids
        ):
            continue
        bbox = unit.get("source_bbox")
        if (
            not isinstance(bbox, list)
            or len(bbox) != 4
            or not all(isinstance(value, (int, float)) for value in bbox)
        ):
            return False
        visible_units.append(unit)
    if not visible_units:
        return False

    for unit in visible_units:
        ux0, uy0, ux1, _ = map(float, unit["source_bbox"])
        overlapping_references = []
        for payload in references:
            bbox = payload.get("bbox")
            if (
                not isinstance(bbox, list)
                or len(bbox) != 4
                or not all(isinstance(value, (int, float)) for value in bbox)
            ):
                continue
            rx0, _, rx1, _ = map(float, bbox)
            if min(ux1, rx1) - max(ux0, rx0) > tolerance:
                overlapping_references.append(payload)
        if not overlapping_references:
            return False
        if not any(
            uy0 >= float(payload["bbox"][3]) - tolerance
            for payload in overlapping_references
        ):
            return False
    return True
