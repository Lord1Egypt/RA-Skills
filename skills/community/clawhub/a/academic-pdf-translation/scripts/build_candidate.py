from __future__ import annotations

import sys
from pathlib import Path as _Path

# 按 README 的写法直接跑时 sys.path 里没有仓库根，包就 import 不到。
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

import argparse
import hashlib
import html
import io
import math
import os
import re
import tempfile
import time
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from academic_pdf_translation.planning.mode_policy import (  # noqa: E402
    FALLBACK_PRESERVE_ELEMENT_REGION,
    FALLBACK_PRESERVE_FULL_PAGE,
)
from academic_pdf_translation.render.plan_bridge import (  # noqa: E402
    FIGURE_CAPTION_KEY,
    attach_figure_captions,
    build_preservation_items,
    merge_into_complex_content,
)
from academic_pdf_translation.render.preserved_region_renderer import (  # noqa: E402
    MIN_RASTER_DPI,
    PDF_BASE_DPI,
)
from academic_pdf_translation.render.table_autobuild import (  # noqa: E402
    build_table_payload,
)
from academic_pdf_translation.render.reference_renderer import (  # noqa: E402
    build_hyphenated_forms,
    build_vocabulary,
    normalize_reference_text,
    repair_baked_line_artifacts,
)
from academic_pdf_translation.verify.render_contract import (  # noqa: E402
    derive_complex_view,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

import perf_trace  # noqa: E402
from _common import (
    SkillError,
    _complex_item_source_pages,
    complex_payload_replaced_unit_ids,
    import_fitz,
    internal_job_path,
    is_nonsemantic_source_furniture_unit,
    load_json,
    remove_suppressed_texts,
    resolve_language_profile,
    sha256_file,
    utc_now,
    write_json,
)
from candidate_analysis import open_candidate_analysis
from cjk_markup import install_reportlab_cjk_nobr_patch, reportlab_cjk_markup
from font_preparation import (
    _resolve_fonts,
    _resolve_reference_font,
    font_evidence,
    fonts_are_current,
)
from i18n import message
from renderer_identity import renderer_build_id
from reportlab_layout import make_cjk_style
from retained_source import (
    REFERENCE_CATEGORIES,
    extract_retained_regions,
    retained_region_ids,
    retained_regions_by_page,
)
from set_complex_payload import validate_complex_payload_item
from typography_fit import (
    candidate_groups,
    search_first_acceptable,
)

# 生成器身份的唯一定义已移入
# academic_pdf_translation.render.document_output，这里再导出保持引用路径不变。
from academic_pdf_translation.render.document_output import (  # noqa: E402,F401
    RENDERER_NAME,
    RENDERER_VERSION,
)
REFERENCE_KINDS = {
    "reference",
    "references",
    "bibliography",
}
HEADING_KINDS = {"title", "subtitle", "heading", "section-heading"}
# 字体分段与行内标记已移入 academic_pdf_translation.render.font_runs。
# 它们是纯函数：给定文本与字体名产出标记字符串，不依赖排版上下文。
# 这里再导出，保持本模块内既有调用与测试的引用路径不变。
from academic_pdf_translation.render.font_runs import (  # noqa: E402,F401
    CJK_FONT_RUN_PATTERN,
    CONTROL_CHARACTER_RE,
    LIGATURE_REPLACEMENTS,
    MARKUP_TOKEN_PATTERN,
    SUPERSCRIPT_CHARACTERS,
    SUPERSCRIPT_DIGITS,
    SUPERSCRIPT_PATTERN_CLASS,
    _edge_label_lines,
    _fallback_runs,
    _font_supports,
    _markup,
    _plain_superscript,
    _unicode_superscript_characters,
)
from academic_pdf_translation.render import font_runs as _font_runs  # noqa: E402


def _register_font(name: str, path: Path) -> None:
    if name in pdfmetrics.getRegisteredFontNames():
        return
    kwargs = {"subfontIndex": 0} if path.suffix.casefold() == ".ttc" else {}
    pdfmetrics.registerFont(TTFont(name, str(path), **kwargs))


def _common_page_size(source_path: Path) -> tuple[float, float]:
    handle = open_candidate_analysis(source_path, role="source")
    counts: dict[tuple[float, float], int] = defaultdict(int)
    for page in handle.document:
        width = round(float(page.rect.width), 1)
        height = round(float(page.rect.height), 1)
        if width > height:
            width, height = height, width
        counts[(width, height)] += 1
    handle.release()
    if not counts:
        raise SkillError("原文没有页面")
    return max(counts, key=lambda value: counts[value])


# 文本分块与标题资格判定已移入 academic_pdf_translation.render.text_blocks。
# 这里按旧名再导出，本模块内的调用与既有测试引用路径不变。
from academic_pdf_translation.render.text_blocks import (  # noqa: E402,F401
    looks_like_heading as _looks_like_heading,
)
from academic_pdf_translation.render.text_blocks import (  # noqa: E402,F401
    role_may_head as _role_may_head,
)
from academic_pdf_translation.render.text_blocks import (  # noqa: E402,F401
    split_blocks as _split_blocks,
)
from academic_pdf_translation.render.text_blocks import (  # noqa: E402,F401
    unit_text_blocks as _unit_text_blocks,
)

# 候选页映射的四个类已移入 academic_pdf_translation.render.mapping，
# 这里再导出保持调用路径不变。
from academic_pdf_translation.render.mapping import (  # noqa: E402,F401
    MappingAnchor,
    MappingDocTemplate,
    MappingError,
    MappingEvent,
    MappingTracker,
)


# 矢量图 Flowable 已移入 academic_pdf_translation.render.flowables，
# 这里再导出保持调用路径不变。
from academic_pdf_translation.render.flowables import (  # noqa: E402,F401
    VectorFigureError,
    VectorPayloadFlowable,
)


# Story 构建已移入 academic_pdf_translation.render 的四个模块。
# 按"改动频率"分层：story 负责调度（哪一页先放什么，改得最勤），
# story_text / story_visual / story_complex 负责画法（相对稳定）。
# 这里按旧名再导出，保持本模块内既有调用与既有测试的引用路径不变。
from academic_pdf_translation.render import story as _story_module  # noqa: E402
from academic_pdf_translation.render import (  # noqa: E402
    story_complex as _story_complex,
)
from academic_pdf_translation.render import story_text as _story_text  # noqa: E402
from academic_pdf_translation.render import (  # noqa: E402
    story_visual as _story_visual,
)
from academic_pdf_translation.render.reference_data import (  # noqa: E402,F401
    REFERENCE_CATEGORIES,
    _is_reference_heading_unit,
    _reference_font_size,
    _reference_unit_parts,
)
from academic_pdf_translation.render.story import (  # noqa: E402,F401
    _bbox_overlap_ratio,
    _ordered_page_units,
    _reading_order_text_token,
    _reading_order_unit_roles,
    _source_block_for_unit,
)
from academic_pdf_translation.render.story_complex import (  # noqa: E402,F401
    PRESERVED_REGION_MAX_HEIGHT_RATIO,
    _complex_embedded_texts,
    _complex_render_policy,
    _overlay_chinese_labels,
    _with_figure_caption,
)
from academic_pdf_translation.render.story_text import (  # noqa: E402,F401
    StoryError,
    _is_bottom_note_unit,
    _is_cross_page_continuation,
    _join_target_fragments,
    _line_fragment_bbox,
    _line_fragment_role,
    _retained_render_policy,
    _should_join_line_fragment,
    _source_ends_paragraph,
    _starts_with_latin_upper,
    _unit_bbox,
    _unit_fully_covered_by_retained,
)
from academic_pdf_translation.render.story_visual import (  # noqa: E402,F401
    _bounded_float,
    _image_clip_bbox,
    _image_label_text,
    _localized_image_labels,
)
from academic_pdf_translation.render.table_data import (  # noqa: E402,F401
    TableDataError,
    _cell_text,
    _column_widths,
    _table_emphasis_rows,
    _table_header_spans,
    _table_matrix,
    _table_note_text,
)

#: Story 构建需要的、原本长在 scripts 层的几件东西，在这里一次装配好。
#: 包内不 import scripts，所以这些依赖只能从外面递进去。
_STORY_DEPS = _story_text.StoryDeps(
    message_fn=message,
    import_fitz_fn=import_fitz,
    make_cjk_style_fn=make_cjk_style,
    remove_suppressed_texts_fn=remove_suppressed_texts,
    is_nonsemantic_furniture_fn=is_nonsemantic_source_furniture_unit,
    complex_replaced_unit_ids_fn=complex_payload_replaced_unit_ids,
    complex_item_source_pages_fn=_complex_item_source_pages,
    retained_regions_by_page_fn=retained_regions_by_page,
)


def _with_story_deps(call, *args: Any, **kwargs: Any):
    """递上注入包调用包内函数，并把 StoryError 翻译回 SkillError。

    文案原样透传，所以对调用方来说异常类型和消息都和搬家前一样。
    """

    try:
        return call(*args, deps=_STORY_DEPS, **kwargs)
    except StoryError as exc:
        raise SkillError(str(exc)) from exc


def _styles(**kwargs: Any) -> dict[str, ParagraphStyle]:
    return _with_story_deps(_story_text._styles, **kwargs)


def _unit_flowables(*args: Any, **kwargs: Any) -> list[Flowable]:
    return _with_story_deps(_story_text._unit_flowables, *args, **kwargs)


def _joined_unit_flowables(*args: Any, **kwargs: Any) -> list[Flowable]:
    return _with_story_deps(
        _story_text._joined_unit_flowables,
        *args,
        **kwargs,
    )


def _retained_heading_label(target_language: str) -> str:
    return _story_text._retained_heading_label(_STORY_DEPS, target_language)


def _retained_flowables(*args: Any, **kwargs: Any) -> list[Flowable]:
    return _with_story_deps(_story_text._retained_flowables, *args, **kwargs)


def _retained_references_precede_visible_units(
    *args: Any,
    **kwargs: Any,
) -> bool:
    return _with_story_deps(
        _story_text._retained_references_precede_visible_units,
        *args,
        **kwargs,
    )


def _table_flowables(*args: Any, **kwargs: Any) -> list[Flowable]:
    # 表格不需要注入包，但仍要把 StoryError 翻回 SkillError。
    try:
        return _story_visual._table_flowables(*args, **kwargs)
    except StoryError as exc:
        raise SkillError(str(exc)) from exc


def _image_flowables(*args: Any, **kwargs: Any) -> list[Flowable]:
    return _with_story_deps(_story_visual._image_flowables, *args, **kwargs)


def _localized_image_label_flowables(
    *args: Any,
    **kwargs: Any,
) -> list[Flowable]:
    return _with_story_deps(
        _story_visual._localized_image_label_flowables,
        *args,
        **kwargs,
    )


def _preserved_source_region_image(*args: Any, **kwargs: Any) -> Image:
    return _with_story_deps(
        _story_complex._preserved_source_region_image,
        *args,
        **kwargs,
    )


def _preserved_region_flowables(*args: Any, **kwargs: Any) -> list[Flowable]:
    return _with_story_deps(
        _story_complex._preserved_region_flowables,
        *args,
        **kwargs,
    )


def _complex_flowables(*args: Any, **kwargs: Any) -> list[Flowable]:
    return _with_story_deps(
        _story_complex._complex_flowables,
        *args,
        **kwargs,
    )


def _cross_page_continuation_pairs(**kwargs: Any) -> dict[str, dict[str, Any]]:
    return _with_story_deps(
        _story_module._cross_page_continuation_pairs,
        **kwargs,
    )


def _story(**kwargs: Any) -> list[Flowable]:
    return _with_story_deps(_story_module._story, **kwargs)


# 排版搜索（字号、行距和页数的试排与选择）已移入
# academic_pdf_translation.render.typography_search。
# 它对外只有一个入口 search_typography，进出都是明确的数据，
# 生成器主流程不再夹着一段两百行的搜索循环。
# 这里按旧名再导出，需要注入的用薄包装绑好依赖，调用路径不变。
from academic_pdf_translation.render import (  # noqa: E402
    typography_search as _typography_search,
)
from academic_pdf_translation.render.typography_search import (  # noqa: E402,F401
    TypographySearchError,
    _adaptive_page_expansion_limit,
    _estimated_page_count,
    _title_from_translation,
)

#: 排版搜索需要的、原本长在 scripts 层的几件东西，在这里一次装配好。
_TYPOGRAPHY_DEPS = _typography_search.TypographyDeps(
    story=_STORY_DEPS,
    candidate_groups_fn=candidate_groups,
    search_first_acceptable_fn=search_first_acceptable,
    count_render_attempt_fn=lambda: perf_trace.count(
        perf_trace.COUNTER_RENDER_ATTEMPT
    ),
    open_candidate_analysis_fn=open_candidate_analysis,
)


def _with_typography_deps(call, *args: Any, **kwargs: Any):
    """递上注入包调用包内函数，并把 TypographySearchError 翻译回 SkillError。"""

    try:
        return call(*args, deps=_TYPOGRAPHY_DEPS, **kwargs)
    except TypographySearchError as exc:
        raise SkillError(str(exc)) from exc


def _render_attempt(**kwargs: Any) -> tuple[MappingTracker, int]:
    return _with_typography_deps(_typography_search._render_attempt, **kwargs)


def _typography_candidate_groups(
    job: dict[str, Any],
) -> list[list[tuple[float, float]]]:
    return _with_typography_deps(
        _typography_search._typography_candidate_groups,
        job,
    )


def _search_typography(
    **kwargs: Any,
) -> _typography_search.TypographySearchResult:
    return _with_typography_deps(
        _typography_search.search_typography,
        **kwargs,
    )


# 输出写入（书签、原子替换、渲染日志组装）已移入
# academic_pdf_translation.render.document_output。
# 这三件事都是对外承诺：写盘必须原子，渲染日志是交付判断的证据来源。
# 它们和排版怎么算无关，所以不和排版搜索挤在一起。
# 这里按旧名再导出，需要注入的用薄包装绑好依赖，调用路径不变。
from academic_pdf_translation.render import (  # noqa: E402
    document_output as _document_output,
)
from academic_pdf_translation.render.document_output import (  # noqa: E402,F401
    _bookmark_entries,
)

#: 输出写入需要的、原本长在 scripts 层的几件东西，在这里一次装配好。
_OUTPUT_DEPS = _document_output.DocumentOutputDeps(
    open_candidate_analysis_fn=open_candidate_analysis,
    sha256_file_fn=sha256_file,
    renderer_build_id_fn=renderer_build_id,
    retained_region_ids_fn=retained_region_ids,
)


def _add_outline(
    source_pdf: Path,
    destination_pdf: Path,
    mapping: dict[str, Any],
    translation: dict[str, Any],
) -> None:
    _document_output._add_outline(
        source_pdf,
        destination_pdf,
        mapping,
        translation,
        deps=_OUTPUT_DEPS,
    )


def _write_candidate_pdf(**kwargs: Any) -> None:
    _document_output.write_candidate_pdf(deps=_OUTPUT_DEPS, **kwargs)


def _build_layout_log(**kwargs: Any) -> dict[str, Any]:
    return _document_output.build_layout_log(deps=_OUTPUT_DEPS, **kwargs)


def _element_unit_texts(job_dir: Path, translation: dict[str, Any]) -> dict[str, str]:
    """元素到译文的映射，用来给保留区域取图题。

    单元归属取 unit_bindings.json——元素清单自己的 translation_unit_ids
    是空的，那是另一个阶段算出来的结果，没有回填进清单。
    """

    bindings_path = job_dir / "unit_bindings.json"
    if not bindings_path.is_file():
        return {}
    units = {
        str(unit.get("id") or ""): unit
        for unit in translation.get("units", [])
        if isinstance(unit, dict)
    }
    texts: dict[str, list[str]] = {}
    for binding in load_json(bindings_path).get("bindings", []):
        if not isinstance(binding, dict):
            continue
        element_id = str(binding.get("element_id") or "")
        unit = units.get(str(binding.get("unit_id") or ""))
        if not element_id or unit is None:
            continue
        value = str(unit.get("translation") or "").strip()
        if value:
            texts.setdefault(element_id, []).append(value)
    return {key: " ".join(value) for key, value in texts.items()}


def _merge_render_plan_preservations(
    job_dir: Path,
    complex_content: dict[str, Any],
    translation: dict[str, Any],
) -> dict[str, Any]:
    """把渲染计划里的保留级决定并进复杂内容。

    没有渲染计划就原样返回——老作业不该因为多了这一步而跑不动。
    元素清单缺失同理：翻译需要坐标，没有清单就取不到坐标。
    """

    plan_path = job_dir / "render_plan.json"
    elements_path = job_dir / "source_elements.json"
    if not plan_path.is_file() or not elements_path.is_file():
        return complex_content

    plan = load_json(plan_path)
    elements = load_json(elements_path).get("elements") or []
    unit_texts = _element_unit_texts(job_dir, translation)
    page_sizes: dict[int, tuple[float, float]] = {}
    table_items: list[dict[str, Any]] = []
    rebuilt_tables: set[str] = set()
    source_path = job_dir / "source.pdf"
    translation_units = [
        unit
        for unit in translation.get("units", [])
        if isinstance(unit, dict)
    ]
    if source_path.is_file():
        # 经计数通道打开：这次读页尺寸也计入性能基线的 PDF 打开次数。
        handle = open_candidate_analysis(source_path, role="source")
        try:
            _doc = handle.document
            page_sizes = {
                index + 1: (
                    float(_doc[index].rect.width),
                    float(_doc[index].rect.height),
                )
                for index in range(_doc.page_count)
            }
            # 计划定为"保留表格区域"的表，先试自动重建成中文结构表：
            # 网格是几何事实，数字不用翻，文字格的译文从既有单元里收割。
            # 哪一步没把握就仍走贴图保底。
            plan_strategies = {
                str(entry.get("element_id") or ""): str(
                    entry.get("strategy") or ""
                )
                for entry in plan.get("elements", [])
                if isinstance(entry, dict)
            }
            unit_texts_for_captions = _element_unit_texts(job_dir, translation)
            elements_by_id = {
                str(element.get("id") or ""): element
                for element in elements
                if isinstance(element, dict)
            }
            for element in elements:
                if not isinstance(element, dict):
                    continue
                element_id = str(element.get("id") or "")
                if (
                    plan_strategies.get(element_id)
                    != "preserve-table-region-with-translation-key"
                ):
                    continue
                page_number = int(element.get("page") or 0)
                if not 1 <= page_number <= _doc.page_count:
                    continue
                caption = ""
                for caption_id in (element.get("relations") or {}).get(
                    "caption", []
                ):
                    caption = unit_texts_for_captions.get(
                        str(caption_id), ""
                    ).strip()
                    if not caption:
                        caption_element = elements_by_id.get(str(caption_id))
                        if caption_element:
                            caption = str(
                                caption_element.get("text_excerpt") or ""
                            ).strip()
                    if caption:
                        break
                item = build_table_payload(
                    _doc[page_number - 1],
                    element,
                    translation_units,
                    caption=caption,
                )
                if item is not None:
                    table_items.append(item)
                    rebuilt_tables.add(element_id)
            # 结构化抑制标注：数学字体残渣、标题续行重复。
            # 需要查原文字形字体，趁文档开着做。清单随译文对象带给渲染日志。
            formula_boxes: dict[int, list[list[float]]] = {}
            for element in elements:
                if (
                    isinstance(element, dict)
                    and str(element.get("type") or "") == "display-formula"
                    and isinstance(element.get("bbox"), list)
                ):
                    fb = [float(v) for v in element["bbox"]]
                    # 紧框加碎片垫，与桥接层的坐标吞一致
                    fb = [fb[0] - 28.0, fb[1] - 5.0, fb[2] + 28.0, fb[3] + 5.0]
                    formula_boxes.setdefault(
                        int(element.get("page") or 0), []
                    ).append(fb)
            translation["_suppression_manifest"] = (
                _annotate_structural_suppressions(
                    _doc, translation, formula_boxes
                )
            )
            # 公式裁切三步法要做边缘墨迹检查，需要页对象在手，
            # 所以桥接在文档还开着时完成。
            source_pages = {
                index + 1: _doc[index] for index in range(_doc.page_count)
            }
            bridged = build_preservation_items(
                plan,
                elements,
                unit_texts_by_element=unit_texts,
                page_sizes=page_sizes,
                units=translation_units,
                skip_elements=rebuilt_tables,
                source_pages=source_pages,
            )
        finally:
            handle.release()
    else:
        bridged = build_preservation_items(
            plan,
            elements,
            unit_texts_by_element=unit_texts,
            page_sizes=page_sizes,
            units=translation_units,
            skip_elements=rebuilt_tables,
        )
    bridged.items.extend(table_items)
    merged = (
        merge_into_complex_content(complex_content, bridged)
        if (bridged.items or bridged.skipped)
        else complex_content
    )
    # 图级图题挂到它那个复杂条目上，让它跟着图走。
    merged, _attached = attach_figure_captions(merged, elements, unit_texts)
    return merged


MATH_FONT_RE = re.compile(
    r"CMSY|CMEX|CMMI|MSAM|MSBM|Math|Symbol", re.IGNORECASE
)

#: 数学符号字体里少数能确定解码的字形：CMSY/CMEX 的 'p' 是根号。
#: 解码不是翻译——它是按字体编码把源字形读对，√(2/N) 的根号就是这么丢的。
MATH_GLYPH_DECODE = {"p": "√"}


def _annotate_structural_suppressions(
    document: Any,
    translation: dict[str, Any],
    formula_boxes: dict[int, list[list[float]]] | None = None,
) -> list[dict[str, Any]]:
    """结构化判定哪些单元不该以文字形式渲染。

    两类，判据都是结构不是猜测：

    1. **数学字体残渣。** 源文只有一两个字符、没有译文，且原文对应
       位置的字形全部来自数学符号字体（CMSY 里的 'p' 其实是根号）。
       把它当拉丁字母排出来只会得到一个孤立的 'p'。
    2. **标题续行重复。** 原文标题折行被拆成两个单元，模型在第一个
       单元里已译出完整标题，续行单元的译文是它的子串——再排一遍
       就是"…卷积网络图像分割"这种重复。

    返回抑制清单（写进渲染日志），并在单元上打 ``_suppressed_reason``。
    """

    manifest: list[dict[str, Any]] = []
    units = [
        unit
        for unit in translation.get("units", [])
        if isinstance(unit, dict)
    ]

    for unit in units:
        source = str(unit.get("source") or "").strip()
        # keep_source 不豁免：模型标了"根号符号"保源，但源字形在数学
        # 符号字体里，按拉丁字母排出来只是个 'p'——字体检查才是判据。
        if (
            str(unit.get("translation") or "").strip()
            or not source
            or len(source) > 3
        ):
            continue
        bbox = unit.get("source_bbox")
        page_number = unit.get("page")
        if (
            not isinstance(bbox, list)
            or len(bbox) != 4
            or not isinstance(page_number, int)
            or not 1 <= page_number <= document.page_count
        ):
            continue
        import fitz

        # 邻字会蹭进精确 bbox 的 clip；只认文字与本单元源文一致、
        # 且中心落在 bbox 内的那个 span 的字体。
        clip = fitz.Rect(*bbox)
        fonts: set[str] = set()
        for block in document[page_number - 1].get_text(
            "dict", clip=clip
        ).get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    span_text = str(span.get("text") or "").strip()
                    sb = span.get("bbox") or (0, 0, 0, 0)
                    cx = (sb[0] + sb[2]) / 2
                    cy = (sb[1] + sb[3]) / 2
                    if (
                        span_text
                        and span_text == source
                        and bbox[0] <= cx <= bbox[2]
                        and bbox[1] <= cy <= bbox[3]
                    ):
                        fonts.add(str(span.get("font") or ""))
        if fonts and all(MATH_FONT_RE.search(font) for font in fonts):
            cx = (bbox[0] + bbox[2]) / 2
            cy = (bbox[1] + bbox[3]) / 2
            inside_formula = any(
                fb[0] <= cx <= fb[2] and fb[1] <= cy <= fb[3]
                for fb in (formula_boxes or {}).get(page_number, [])
            )
            decoded = MATH_GLYPH_DECODE.get(source)
            if decoded and not inside_formula:
                # 行内符号且能确定解码：按字体编码读对它，不是删掉它。
                unit["_decoded_math"] = decoded
                manifest.append(
                    {
                        "unit_id": str(unit.get("id") or ""),
                        "text": source,
                        "fonts": sorted(fonts),
                        "decoded": decoded,
                        "reason": (
                            f"数学字体字形按编码解码为 {decoded!r}，"
                            "保留在行内"
                        ),
                    }
                )
            else:
                unit["_suppressed_reason"] = "math-font-residue"
                manifest.append(
                    {
                        "unit_id": str(unit.get("id") or ""),
                        "text": source,
                        "fonts": sorted(fonts),
                        "reason": (
                            "源文只是数学符号字体里的字形，且其内容已随"
                            "公式保留区域整块保留，不按拉丁字母重复排版"
                            if inside_formula
                            else "源文只是数学符号字体里的字形，无法确定"
                            "解码，不按拉丁字母排版"
                        ),
                    }
                )

    previous: dict[str, Any] | None = None
    for unit in units:
        translation_text = str(unit.get("translation") or "").strip()
        if previous is not None and translation_text:
            previous_text = str(previous.get("translation") or "").strip()
            if (
                str(previous.get("_element_role") or "") == "document-title"
                and unit.get("page") == previous.get("page")
                and translation_text != previous_text
                and translation_text in previous_text
            ):
                unit["_suppressed_reason"] = "title-continuation-duplicate"
                manifest.append(
                    {
                        "unit_id": str(unit.get("id") or ""),
                        "text": translation_text,
                        "reason": (
                            "标题续行的译文已包含在整题译文里，再排一遍"
                            "就是重复"
                        ),
                    }
                )
        if translation_text or str(unit.get("source") or "").strip():
            previous = unit
    return manifest


def _annotate_element_roles(
    job_dir: Path,
    translation: dict[str, Any],
) -> None:
    """把单元绑定的元素角色标到单元上，供标题判定否决使用。

    "谁是标题"应当来自原文结构分析，不是字号或行长的猜测——作者单位、
    arXiv 版本戳、图内标签都可能长得像标题。没有绑定文件时不标注，
    下游维持原有启发式行为。
    """

    bindings_path = job_dir / "unit_bindings.json"
    if not bindings_path.is_file():
        return
    try:
        bindings = load_json(bindings_path).get("bindings") or []
    except (OSError, ValueError):
        return
    roles = {
        str(binding.get("unit_id") or ""): str(binding.get("element_role") or "")
        for binding in bindings
        if isinstance(binding, dict) and binding.get("unit_id")
    }
    if not roles:
        return
    element_ids = {
        str(binding.get("unit_id") or ""): str(
            binding.get("element_id") or ""
        )
        for binding in bindings
        if isinstance(binding, dict) and binding.get("unit_id")
    }
    for unit in translation.get("units", []):
        if isinstance(unit, dict):
            unit_id = str(unit.get("id") or "")
            role = roles.get(unit_id)
            if role:
                unit["_element_role"] = role
            element_id = element_ids.get(unit_id)
            if element_id:
                unit["_element_id"] = element_id


def _timed_build_candidate(
    job_dir: Path,
    output_pdf: Path,
    *,
    max_page_expansion_ratio: float | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    job_dir = job_dir.resolve()
    output_pdf = output_pdf.resolve()
    job = load_json(job_dir / "job.json")
    translation_path = internal_job_path(
        job_dir,
        job["files"]["translation"],
    )
    translation = load_json(translation_path)
    _annotate_element_roles(job_dir, translation)
    complex_path = internal_job_path(
        job_dir,
        job.get("files", {}).get(
            "complex_content_payload",
            "complex_content.json",
        ),
    )
    complex_content = (
        load_json(complex_path)
        if complex_path.is_file()
        else {
            "schema_version": "1.0",
            "classification_complete": True,
            "items": [],
        }
    )
    # 渲染计划里定到保留级的元素，翻成生成器认识的条目再并进来。
    # 阶段 15 的基准查出：不做这一步，返修算出来的降级生成器根本看不见，
    # 重建出来的候选与返修前一字不差。
    complex_content = _merge_render_plan_preservations(
        job_dir, complex_content, translation
    )
    # 复杂内容从此是**派生视图**：并完计划立刻写回磁盘并盖上计划哈希。
    # 预渲染检查对的是这份落盘文件——生成器消化了什么、文件里就是什么，
    # 旧手写条目数再也不能把一版合法的新计划错误地拦下来。
    _plan_file = job_dir / "render_plan.json"
    if _plan_file.is_file():
        complex_content = derive_complex_view(
            complex_content, sha256_file(_plan_file)
        )
        write_json(complex_path, complex_content)

    retained_path = internal_job_path(
        job_dir,
        job["files"]["retained_source"],
    )
    retained = load_json(retained_path)
    source_structure_path = internal_job_path(
        job_dir,
        job.get("files", {}).get(
            "source_structure",
            "source_structure.json",
        ),
    )
    source_structure = (
        load_json(source_structure_path)
        if source_structure_path.is_file()
        else {
            "schema_version": "legacy-no-source-structure",
            "pages": [],
        }
    )
    unit_layout_roles = _reading_order_unit_roles(
        translation,
        complex_content,
        source_structure,
    )
    unresolved_complex = [
        item.get("id") or item.get("page")
        for item in complex_content.get("items", [])
        if isinstance(item, dict) and item.get("status") != "ready"
    ]
    if unresolved_complex:
        raise SkillError(
            "以下复杂页载荷尚未 ready，统一生成器不会把它们降级成文字摘要: "
            + ", ".join(map(str, unresolved_complex[:30]))
        )
    invalid_complex: list[str] = []
    for item in complex_content.get("items", []):
        if not isinstance(item, dict):
            invalid_complex.append("复杂页载荷含非对象条目")
            continue
        invalid_complex.extend(
            f"{item.get('id') or item.get('page')}: {error}"
            for error in validate_complex_payload_item(item)
        )
    if invalid_complex:
        raise SkillError(
            "复杂页载荷不完整: " + "；".join(invalid_complex[:30])
        )
    source_path = internal_job_path(job_dir, job["source"]["job_path"])
    # 字体正常在初始化或统一入口就已冻结；这里只兜底，并保持证据同步。
    # 冻结优先：prepare_job_fonts 已经把三个角色的字体连同哈希写进
    # job.json，渲染就用它们。渲染时再解析一遍等于绕开冻结——
    # 冻结时按题录真实字符做过覆盖检查，重解析没有这份输入，会选错。
    _frozen_fonts = (job.get("quality") or {}).get("selected_fonts")
    if (
        isinstance(_frozen_fonts, list)
        and len(_frozen_fonts) >= 3
        and fonts_are_current(job)
    ):
        regular_path = Path(_frozen_fonts[0])
        bold_path = Path(_frozen_fonts[1])
        reference_path = Path(_frozen_fonts[2])
        math_path = (
            Path(_frozen_fonts[3]) if len(_frozen_fonts) >= 4 else None
        )
    else:
        regular_path, bold_path = _resolve_fonts(job)
        reference_path = _resolve_reference_font(regular_path)
        math_path = None
    resolved_font_paths = [
        str(regular_path),
        str(bold_path),
        str(reference_path),
        *([str(math_path)] if math_path else []),
    ]
    if job.get("quality", {}).get("selected_fonts") != resolved_font_paths:
        quality = job.setdefault("quality", {})
        quality["selected_fonts"] = resolved_font_paths
        quality["selected_font_evidence"] = font_evidence(
            [
                regular_path,
                bold_path,
                reference_path,
                *([math_path] if math_path else []),
            ]
        )
        write_json(job_dir / "job.json", job)
    regular_font = "AcademicUnifiedRegular"
    bold_font = "AcademicUnifiedBold"
    reference_font_name = "AcademicUnifiedReference"
    _register_font(regular_font, regular_path)
    _register_font(bold_font, bold_path)
    _register_font(reference_font_name, reference_path)
    # 数学后备字体名是 font_runs 的模块级状态：_markup 逐字符判断时要用。
    if math_path is not None and Path(math_path).is_file():
        _register_font("AcademicUnifiedMath", Path(math_path))
        _font_runs.MATH_FALLBACK_FONT_NAME = "AcademicUnifiedMath"
    else:
        _font_runs.MATH_FALLBACK_FONT_NAME = None
    install_reportlab_cjk_nobr_patch()

    page_size = _common_page_size(source_path)
    margins = (48.0, 48.0, 42.0, 38.0)
    source_page_count = int(job["source"]["page_count"])
    source_handle = open_candidate_analysis(source_path, role="source")
    source_document = source_handle.document
    retained_payloads = extract_retained_regions(
        source_document,
        retained,
        translation,
    )
    effective_page_expansion_ratio = (
        float(max_page_expansion_ratio)
        if max_page_expansion_ratio is not None
        else _adaptive_page_expansion_limit(
            source_document,
            retained_payloads,
            complex_content,
        )
    )
    empty_retained = [
        payload["id"]
        for payload in retained_payloads
        if not payload.get("blocks")
        and payload.get("already_present_in_translation") is not True
    ]
    if empty_retained:
        source_handle.release()
        raise SkillError(
            "以下保留原文区域没有提取到可排版文字: "
            + ", ".join(empty_retained[:30])
        )
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="academic-unified-render-") as tmp:
        tmp_dir = Path(tmp)
        search_result = _search_typography(
            tmp_dir=tmp_dir,
            job=job,
            translation=translation,
            complex_content=complex_content,
            retained_payloads=retained_payloads,
            source_document=source_document,
            source_structure=source_structure,
            page_size=page_size,
            margins=margins,
            regular_font=regular_font,
            bold_font=bold_font,
            reference_font_name=reference_font_name,
            label_font_path=str(regular_path),
            source_page_count=source_page_count,
            effective_page_expansion_ratio=effective_page_expansion_ratio,
        )
        attempts = search_result.attempts
        typography_search = search_result.typography_search
        (
            selected_path,
            tracker,
            candidate_page_count,
            body_font,
            leading,
            reference_font_pt,
        ) = search_result.selection
        provisional_hash = sha256_file(selected_path)
        provisional_map = tracker.build_map(
            job=job,
            translation=translation,
            retained_payloads=retained_payloads,
            unit_layout_roles=unit_layout_roles,
            page_size=page_size,
            margins=margins,
            candidate_page_count=candidate_page_count,
            candidate_sha256=provisional_hash,
            now_fn=utc_now,
        )
        _write_candidate_pdf(
            selected_path=selected_path,
            outline_path=tmp_dir / "candidate-with-outline.pdf",
            output_pdf=output_pdf,
            mapping=provisional_map,
            translation=translation,
        )
    source_handle.release()

    candidate_hash = sha256_file(output_pdf)
    mapping = tracker.build_map(
        job=job,
        translation=translation,
        retained_payloads=retained_payloads,
        unit_layout_roles=unit_layout_roles,
        page_size=page_size,
        margins=margins,
        candidate_page_count=candidate_page_count,
        candidate_sha256=candidate_hash,
        now_fn=utc_now,
    )
    mapping["translation_sha256"] = sha256_file(translation_path)
    map_path = output_pdf.with_suffix(".page-map.json")
    write_json(map_path, mapping)

    layout_log = _build_layout_log(
        translation=translation,
        complex_content=complex_content,
        retained=retained,
        retained_payloads=retained_payloads,
        retained_path=retained_path,
        mapping=mapping,
        map_path=map_path,
        page_size=page_size,
        margins=margins,
        body_font_pt=body_font,
        leading_ratio=leading,
        reference_font_pt=reference_font_pt,
        source_page_count=source_page_count,
        candidate_page_count=candidate_page_count,
        page_count_ratio_limit=effective_page_expansion_ratio,
        page_count_ratio_limit_source=(
            "explicit"
            if max_page_expansion_ratio is not None
            else "adaptive-reference-share"
        ),
        attempts=attempts,
        typography_search=typography_search,
        orphan_regions=tracker.orphan_regions,
        font_paths=[
            str(regular_path),
            str(bold_path),
            str(reference_path),
            # 数学符号后备也是真用到的字体，必须进合同——
            # 少报一把，字体一致性检查就对不上。
            *([str(math_path)] if math_path else []),
        ],
        elapsed_seconds=round(time.monotonic() - started, 3),
    )
    write_json(job_dir / "generator-layout-log.json", layout_log)
    return {
        "output_pdf": str(output_pdf),
        "candidate_page_map": str(map_path),
        "generator_layout_log": str(job_dir / "generator-layout-log.json"),
        "renderer": RENDERER_NAME,
        "renderer_version": RENDERER_VERSION,
        "renderer_build_id": layout_log["renderer_build_id"],
        "source_page_count": source_page_count,
        "candidate_page_count": candidate_page_count,
        "body_font_pt": body_font,
        "leading_ratio": leading,
        "page_count_ratio_limit": effective_page_expansion_ratio,
        "elapsed_seconds": layout_log["elapsed_seconds"],
    }



def build_candidate(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("build_candidate"):
        # 映射类在包内抛自己的异常，这里翻译回 SkillError，
        # 保证对外的错误类型和文案与搬家前完全一致。
        try:
            return _timed_build_candidate(*args, **kwargs)
        except MappingError as error:
            raise SkillError(str(error)) from error


def main() -> int:
    parser = argparse.ArgumentParser(
        description="用统一连续流排和结构化复杂页载荷生成首版候选 PDF"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument(
        "--max-page-expansion-ratio",
        type=float,
        default=None,
        help="可选的异常页数保护上限；默认按参考文献占比自动计算",
    )
    args = parser.parse_args()
    try:
        if (
            args.max_page_expansion_ratio is not None
            and not 1.0 <= args.max_page_expansion_ratio <= 3.0
        ):
            raise SkillError("--max-page-expansion-ratio 必须位于 1.0..3.0")
        result = build_candidate(
            args.job_dir,
            args.output_pdf,
            max_page_expansion_ratio=args.max_page_expansion_ratio,
        )
        print(f"首版候选: {result['output_pdf']}")
        print(
            "分页: "
            f"{result['source_page_count']} 个源页 -> "
            f"{result['candidate_page_count']} 个候选页"
        )
        print(
            "正文: "
            f"{result['body_font_pt']} pt，"
            f"{result['leading_ratio']} 倍行距"
        )
        print(f"耗时: {result['elapsed_seconds']} 秒")
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
