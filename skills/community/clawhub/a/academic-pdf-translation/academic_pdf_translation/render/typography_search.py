"""排版搜索：字号、行距和页数的试排与选择。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。这一段回答的是
"用多大字号排"：按候选网格逐个完整试排，第一个页数没超上限的就选它。

之所以单独成模块：搜索策略、页数扩张保护和试排本身是三件容易一起改坏的事，
放在生成器主流程里，改上限会顺手碰到试排，改试排会顺手碰到搜索。
分出来之后，它对外只有一个入口 ``search_typography``，进出都是明确的数据。

估算函数刻意不参与选择。它只写进报告当"当时怎么想的"，
真正决定字号的永远是完整试排的页数。

原来的 scripts 层依赖按包内规则改写：异常改成本模块自己的
``TypographySearchError``，由调用侧翻译回 SkillError，文案原样透传；
候选网格、搜索算法、试排计数和候选 PDF 打开都由 ``TypographyDeps`` 注入。
"""

from __future__ import annotations

import math
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from reportlab.pdfgen.canvas import Canvas

from .flowables import VectorFigureError
from .mapping import MappingDocTemplate, MappingTracker
from .reference_data import REFERENCE_CATEGORIES, _reference_font_size
from .story import _story
from .story_text import StoryDeps, StoryError, _styles
from .story_visual import _localized_image_labels
from .text_blocks import HEADING_KINDS


class TypographySearchError(RuntimeError):
    """排版搜索没能给出可交付的试排。

    以前抛的是 scripts 层的 SkillError；包不该依赖 scripts，所以这里
    自己定义。调用侧把它翻译回 SkillError，文案原样透传，对外行为不变。
    """


@dataclass(frozen=True)
class TypographyDeps:
    """排版搜索需要的、原本长在 scripts 层的几件东西。"""

    #: Story 构建的注入包，原样往下传。
    story: StoryDeps
    #: 生成候选网格：``typography_fit.candidate_groups``。
    candidate_groups_fn: Callable[..., list[list[tuple[float, float]]]]
    #: 搜索第一个可接受候选：``typography_fit.search_first_acceptable``。
    search_first_acceptable_fn: Callable[..., tuple[Any, str, str]]
    #: 记一次试排，用于性能基线计数。
    count_render_attempt_fn: Callable[[], None]
    #: 打开候选 PDF 读页数，返回带 ``page_count`` 与 ``release`` 的句柄。
    open_candidate_analysis_fn: Callable[..., Any]


@dataclass(frozen=True)
class TypographySearchResult:
    """一次排版搜索的全部产出。

    ``selection`` 是被选中的那次试排：路径、映射跟踪器、页数、字号、
    行距、题录字号。搜索失败不会返回这个对象，而是直接抛异常。
    """

    selection: tuple[Path, MappingTracker, int, float, float, float]
    attempts: list[dict[str, Any]]
    typography_search: dict[str, Any]


def _title_from_translation(translation: dict[str, Any], fallback: str) -> str:
    for unit in translation.get("units", []):
        if not isinstance(unit, dict):
            continue
        if str(unit.get("kind") or "").lower() not in HEADING_KINDS:
            continue
        value = str(unit.get("translation") or "").strip()
        if value:
            return value.splitlines()[0][:180]
    for unit in translation.get("units", []):
        if isinstance(unit, dict):
            value = str(unit.get("translation") or "").strip()
            if value:
                return value.splitlines()[0][:180]
    return fallback


def _render_attempt(
    *,
    deps: TypographyDeps,
    path: Path,
    job: dict[str, Any],
    translation: dict[str, Any],
    complex_content: dict[str, Any],
    retained_payloads: list[dict[str, Any]],
    source_document: Any,
    source_structure: dict[str, Any],
    page_size: tuple[float, float],
    margins: tuple[float, float, float, float],
    regular_font: str,
    bold_font: str,
    reference_font: str,
    body_font_pt: float,
    leading_ratio: float,
    reference_font_pt: float,
    label_font_path: str | None = None,
) -> tuple[MappingTracker, int]:
    """完整试排一次，结果写入给定路径。

    这里刻意保留落盘：实测在写时复制文件系统上，写临时文件再内存映射打开，
    比把整份 PDF 复制成 bytes 再从内存流解析更快，也不会把每次试排的完整
    PDF 都留在内存里。选中的候选直接复用它自己的临时文件，不重排。
    """

    tracker = MappingTracker()
    styles = _styles(
        deps=deps.story,
        regular_font=regular_font,
        bold_font=bold_font,
        reference_font=reference_font,
        body_font_pt=body_font_pt,
        leading_ratio=leading_ratio,
        reference_font_pt=reference_font_pt,
    )
    available_width = page_size[0] - margins[0] - margins[1]
    available_height = page_size[1] - margins[2] - margins[3]
    story = _story(
        deps=deps.story,
        job=job,
        translation=translation,
        complex_content=complex_content,
        retained_payloads=retained_payloads,
        styles=styles,
        source_document=source_document,
        source_structure=source_structure,
        available_width=available_width,
        available_height=available_height,
        regular_font=regular_font,
        bold_font=bold_font,
        body_font_pt=body_font_pt,
        target_language=str(job["translation"]["target_language"]),
        label_font_path=label_font_path,
    )
    document = MappingDocTemplate(
        str(path),
        tracker=tracker,
        page_size=page_size,
        margins=margins,
        regular_font=regular_font,
        title=_title_from_translation(translation, str(job["job_id"])),
        target_language=str(job["translation"]["target_language"]),
        message_fn=deps.story.message_fn,
    )
    def canvas_maker(filename: str, **kwargs):
        kwargs["initialFontName"] = regular_font
        kwargs["initialFontSize"] = body_font_pt
        kwargs["initialLeading"] = body_font_pt * leading_ratio
        return Canvas(filename, **kwargs)

    # 矢量图和 Story 在各自模块里抛自己的异常，这里统一成本模块的异常，
    # 再由调用侧翻译回 SkillError，文案原样透传。
    try:
        document.build(story, canvasmaker=canvas_maker)
    except (VectorFigureError, StoryError) as error:
        raise TypographySearchError(str(error)) from error
    tracker.finalize_heading_check()
    deps.count_render_attempt_fn()
    output = deps.open_candidate_analysis_fn(path)
    page_count = output.page_count
    output.release()
    return tracker, page_count


def _typography_candidate_groups(
    job: dict[str, Any],
    *,
    deps: TypographyDeps,
) -> list[list[tuple[float, float]]]:
    """把作业里的质量配置翻译成候选搜索空间。

    这里只做作业数据到参数的适配；网格本身由 `typography_fit.candidate_groups`
    唯一定义，排版器不再自带一套。
    """

    quality = job.get("quality", {})
    search = quality.get("typography_search") or {}
    font_range = search.get("body_font_range_pt") or quality.get(
        "body_font_target_pt",
        [9.5, 11.5],
    )
    leading_range = search.get("leading_range") or quality.get(
        "leading_target",
        [1.5, 1.65],
    )
    lower_font, upper_font = map(float, font_range)
    lower_leading, upper_leading = map(float, leading_range)
    return deps.candidate_groups_fn(
        body_font_range_pt=(lower_font, upper_font),
        body_font_step_pt=max(
            float(search.get("body_font_step_pt") or 0.5),
            0.5,
        ),
        leading_range=(lower_leading, upper_leading),
        leading_step=max(float(search.get("leading_step") or 0.05), 0.05),
        preferred_body_font_pt=float(
            quality.get("body_font_preferred_pt")
            or (lower_font + upper_font) / 2
        ),
        preferred_leading=float(
            quality.get("leading_preferred")
            or (lower_leading + upper_leading) / 2
        ),
    )


def _estimated_page_count(
    *,
    translated_chars: int,
    paragraph_count: int,
    heading_count: int,
    available_width_pt: float,
    available_height_pt: float,
    body_font_pt: float,
    leading_ratio: float,
) -> int:
    """不做完整试排的轻量页数估算。

    只用字量、段落数、标题数和可用版心，用来记录搜索依据；它不参与选择，
    因此估算偏差不会改变最终字号。
    """

    line_height = max(body_font_pt * leading_ratio, 1.0)
    chars_per_line = max(available_width_pt / max(body_font_pt, 1.0), 1.0)
    lines_per_page = max(available_height_pt / line_height, 1.0)
    text_lines = translated_chars / chars_per_line
    spacing_lines = paragraph_count * 0.9 + heading_count * 1.6
    return max(1, math.ceil((text_lines + spacing_lines) / lines_per_page))



def _adaptive_page_expansion_limit(
    source_document: Any,
    retained_payloads: list[dict[str, Any]],
    complex_content: dict[str, Any] | None = None,
) -> float:
    page_count = max(int(source_document.page_count), 1)
    reference_page_equivalents = 0.0
    for payload in retained_payloads:
        if (
            str(payload.get("category") or "") not in REFERENCE_CATEGORIES
            or payload.get("resolution")
            == "translated-nonreference-region"
        ):
            continue
        page_number = payload.get("page")
        bbox = payload.get("effective_bbox") or payload.get("bbox")
        if (
            not isinstance(page_number, int)
            or not 1 <= page_number <= page_count
            or not isinstance(bbox, list)
            or len(bbox) != 4
        ):
            continue
        page = source_document[page_number - 1]
        page_area = max(float(page.rect.width * page.rect.height), 1.0)
        x0, y0, x1, y1 = map(float, bbox)
        region_area = max(0.0, x1 - x0) * max(0.0, y1 - y0)
        reference_page_equivalents += min(region_area / page_area, 1.0)
    reference_share = min(reference_page_equivalents / page_count, 1.0)
    complex_page_equivalents = 0.0
    for item in (complex_content or {}).get("items", []):
        if not isinstance(item, dict) or item.get("status") != "ready":
            continue
        payload = item.get("payload")
        if not isinstance(payload, dict):
            continue
        method = str(item.get("method") or "")
        if method in {"structured-table-rebuild", "semantic-grid-rebuild"}:
            for table in payload.get("tables", []):
                if not isinstance(table, dict):
                    continue
                rows = table.get("rows")
                row_count = (
                    len(rows)
                    if isinstance(rows, list)
                    else int(table.get("row_count") or 0)
                )
                complex_page_equivalents += max(0.15, row_count / 30.0)
        elif method in {"image-text-localization", "ocr-region-rebuild"}:
            for region in payload.get("regions", []):
                if not isinstance(region, dict):
                    continue
                label_count = len(_localized_image_labels(region))
                complex_page_equivalents += 0.35 + label_count / 30.0
        elif method == "vector-rebuild":
            figures = payload.get("figures")
            if isinstance(figures, list):
                complex_page_equivalents += max(0.4, len(figures) * 0.4)
    complex_share = min(complex_page_equivalents / page_count, 1.0)
    return round(
        min(
            2.4,
            1.6
            + reference_share * 1.5
            + min(complex_share * 0.9, 0.8),
        ),
        3,
    )



def search_typography(
    *,
    deps: TypographyDeps,
    tmp_dir: Path,
    job: dict[str, Any],
    translation: dict[str, Any],
    complex_content: dict[str, Any],
    retained_payloads: list[dict[str, Any]],
    source_document: Any,
    source_structure: dict[str, Any],
    page_size: tuple[float, float],
    margins: tuple[float, float, float, float],
    regular_font: str,
    bold_font: str,
    reference_font_name: str,
    label_font_path: str | None,
    source_page_count: int,
    effective_page_expansion_ratio: float,
) -> TypographySearchResult:
    """按候选网格试排，返回第一个页数没超上限的结果。

    ``tmp_dir`` 由调用侧给，因为每次试排的 PDF 都落在那里，选中的那份
    还要被继续用；目录的生命周期必须由调用侧控制。
    """

    attempts: list[dict[str, Any]] = []
    selected: tuple[Path, MappingTracker, int, float, float, float] | None = None
    typography_groups = _typography_candidate_groups(job, deps=deps)
    translated_chars = sum(
        len(str(unit.get("translation") or unit.get("source") or ""))
        for unit in translation.get("units", [])
        if isinstance(unit, dict)
    )
    heading_count = sum(
        1
        for unit in translation.get("units", [])
        if isinstance(unit, dict)
        and str(unit.get("kind") or "").lower() == "heading"
    )
    paragraph_count = len(
        [unit for unit in translation.get("units", []) if isinstance(unit, dict)]
    )
    typography_estimate = {
        "translated_chars": translated_chars,
        "paragraph_count": paragraph_count,
        "heading_count": heading_count,
        "available_width_pt": round(page_size[0] - margins[0] - margins[1], 2),
        "available_height_pt": round(page_size[1] - margins[2] - margins[3], 2),
        "candidates": [
            {
                "body_font_pt": body_font,
                "leading_ratio": leading,
                "estimated_page_count": _estimated_page_count(
                    translated_chars=translated_chars,
                    paragraph_count=paragraph_count,
                    heading_count=heading_count,
                    available_width_pt=page_size[0] - margins[0] - margins[1],
                    available_height_pt=page_size[1] - margins[2] - margins[3],
                    body_font_pt=body_font,
                    leading_ratio=leading,
                ),
            }
            for group in typography_groups
            for body_font, leading in group[-1:]
        ],
        "note": (
            "估算只用于记录搜索依据，不参与选择；实际字号仍由完整试排决定。"
        ),
    }

    probe_cache: dict[tuple[int, int], dict[str, Any] | None] = {}

    def _evaluate_candidate(
        group_index: int,
        item_index: int,
    ) -> dict[str, Any] | None:
        key = (group_index, item_index)
        if key in probe_cache:
            return probe_cache[key]
        body_font, leading = typography_groups[group_index][item_index]
        reference_font_pt = _reference_font_size(job, body_font)
        attempt_started = time.monotonic()
        attempt_path = (
            tmp_dir / f"attempt-{group_index:02d}-{item_index:02d}.pdf"
        )
        try:
            tracker, page_count = _render_attempt(
                deps=deps,
                path=attempt_path,
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
                reference_font=reference_font_name,
                body_font_pt=body_font,
                leading_ratio=leading,
                reference_font_pt=reference_font_pt,
                label_font_path=label_font_path,
            )
        except Exception as exc:
            attempts.append(
                {
                    "body_font_pt": body_font,
                    "leading_ratio": leading,
                    "status": "render-failed",
                    "message": str(exc)[:2000],
                    "seconds": round(time.monotonic() - attempt_started, 3),
                }
            )
            probe_cache[key] = None
            return None
        expansion = page_count / max(source_page_count, 1)
        fits = expansion <= effective_page_expansion_ratio
        record = {
            "body_font_pt": body_font,
            "leading_ratio": leading,
            "reference_font_pt": round(reference_font_pt, 2),
            "candidate_page_count": page_count,
            "page_count_ratio": round(expansion, 3),
            "status": "fits" if fits else "too-many-pages",
            "seconds": round(time.monotonic() - attempt_started, 3),
        }
        attempts.append(record)
        probe_cache[key] = {
            "record": record,
            # 不达标的候选不可能被选中；它的映射跟踪器立刻释放，
            # 否则完整扫描会把每一次试排的逐单元映射都留在内存里。
            "tracker": tracker if fits else None,
            "page_count": page_count,
            "path": attempt_path,
            "body_font_pt": body_font,
            "leading_ratio": leading,
            "reference_font_pt": reference_font_pt,
            "fits": fits,
        }
        return probe_cache[key]

    position, search_method, search_note = deps.search_first_acceptable_fn(
        groups=typography_groups,
        evaluate=_evaluate_candidate,
    )
    if search_method == "linear-fallback":
        for group_index, group in enumerate(typography_groups):
            for item_index in range(len(group)):
                result = _evaluate_candidate(group_index, item_index)
                if result is not None and result["fits"]:
                    position = (group_index, item_index)
                    break
            if position is not None:
                break

    if position is not None:
        chosen = probe_cache[position]
        chosen["record"]["status"] = "selected"
        selected = (
            chosen["path"],
            chosen["tracker"],
            chosen["page_count"],
            chosen["body_font_pt"],
            chosen["leading_ratio"],
            chosen["reference_font_pt"],
        )
    typography_search = {
        "method": search_method,
        "note": search_note,
        "candidate_count": sum(
            len(group) for group in typography_groups
        ),
        "leading_group_count": len(typography_groups),
        "render_attempts": len(attempts),
        "estimate": typography_estimate,
    }
    if selected is None:
        rendered_attempts = [
            attempt
            for attempt in attempts
            if attempt.get("candidate_page_count")
        ]
        best = min(
            rendered_attempts,
            key=lambda attempt: float(
                attempt.get("page_count_ratio") or math.inf
            ),
            default=None,
        )
        if best is None:
            failure_messages = list(
                dict.fromkeys(
                    str(attempt.get("message") or "").strip()
                    for attempt in attempts
                    if attempt.get("status") == "render-failed"
                    and str(attempt.get("message") or "").strip()
                )
            )
            detail = (
                "没有成功试排。"
                + (
                    "首个渲染错误：" + " | ".join(failure_messages[:3])
                    if failure_messages
                    else ""
                )
            )
        else:
            detail = (
                f"最紧凑的可读试排为 "
                f"{best['candidate_page_count']} 页，"
                f"扩张比 {best['page_count_ratio']}；"
                f"当前异常保护上限为 "
                f"{effective_page_expansion_ratio}。"
            )
        raise TypographySearchError(
            "统一生成器无法在可读字号和页数扩张上限内完成首版。"
            f"{detail}"
            "请优先检查重复内容、错误保留区域或异常复杂页载荷。"
        )
    return TypographySearchResult(
        selection=selected,
        attempts=attempts,
        typography_search=typography_search,
    )
