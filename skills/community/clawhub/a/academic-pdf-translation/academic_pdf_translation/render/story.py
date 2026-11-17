"""Story 构建的最外层：把一页的东西按阅读顺序排成一串 Flowable。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。这一层只做调度：
按原文结构定阅读顺序、判定跨页续段、决定每一页先放保留区域还是先放正文，
然后调下面三层去生成具体的 Flowable。

之所以单独成模块：调度规则改得最频繁，而 ``story_text``、``story_visual``、
``story_complex`` 三层是稳定的画法。分开之后改顺序不会碰到画法。

本模块超过 800 行，暂时不再拆：``_story`` 本身就是一个四百多行的
单遍扫描，它对每一页依次决定放什么，中间靠十几个循环内变量互相牵制。
把它切成几个函数，只会把这些变量变成一长串参数，读起来更难，
而且每切一刀都有改变顺序的风险。等这段扫描本身被简化之后再拆。

原来 scripts 层的 SkillError 在这里换成 ``StoryError``，
由 ``scripts/build_candidate.py`` 在调用处翻译回去，文案原样透传。
"""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from typing import Any

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable, PageBreak

from .mapping import MappingAnchor
from .reference_data import REFERENCE_CATEGORIES, _is_reference_heading_unit
from .reference_renderer import (
    build_hyphenated_forms,
    build_vocabulary,
    normalize_reference_text,
    repair_baked_line_artifacts,
)
from .story_complex import (
    _complex_embedded_texts,
    _complex_flowables,
    _complex_render_policy,
)
from .story_text import (
    StoryDeps,
    StoryError,
    _is_bottom_note_unit,
    _is_cross_page_continuation,
    _joined_unit_flowables,
    _retained_flowables,
    _retained_references_precede_visible_units,
    _retained_render_policy,
    _should_join_line_fragment,
    _unit_bbox,
    _unit_flowables,
    _unit_fully_covered_by_retained,
)
from .text_blocks import REFERENCE_KINDS


def _reading_order_text_token(value: Any) -> str:
    return re.sub(
        r"[\W_]+",
        "",
        unicodedata.normalize("NFKC", str(value or "")).casefold(),
        flags=re.UNICODE,
    )


def _bbox_overlap_ratio(
    inner: tuple[float, float, float, float],
    outer: tuple[float, float, float, float],
) -> float:
    x0 = max(inner[0], outer[0])
    y0 = max(inner[1], outer[1])
    x1 = min(inner[2], outer[2])
    y1 = min(inner[3], outer[3])
    if x1 <= x0 or y1 <= y0:
        return 0.0
    inner_area = (inner[2] - inner[0]) * (inner[3] - inner[1])
    if inner_area <= 0:
        return 0.0
    return ((x1 - x0) * (y1 - y0)) / inner_area


def _source_block_for_unit(
    unit: dict[str, Any],
    blocks: list[dict[str, Any]],
) -> int | None:
    unit_bbox = _unit_bbox(unit)
    unit_text = _reading_order_text_token(unit.get("source"))
    best: tuple[float, int] | None = None
    for block in blocks:
        block_id = block.get("id")
        block_bbox_raw = block.get("bbox")
        if (
            not isinstance(block_id, int)
            or not isinstance(block_bbox_raw, list)
            or len(block_bbox_raw) != 4
            or not all(
                isinstance(value, (int, float))
                for value in block_bbox_raw
            )
        ):
            continue
        block_bbox = tuple(map(float, block_bbox_raw))
        overlap = (
            _bbox_overlap_ratio(unit_bbox, block_bbox)
            if unit_bbox is not None
            else 0.0
        )
        block_text = _reading_order_text_token(block.get("text"))
        text_match = bool(
            unit_text
            and block_text
            and (
                unit_text == block_text
                or (
                    min(len(unit_text), len(block_text)) >= 5
                    and (
                        unit_text in block_text
                        or block_text in unit_text
                    )
                )
            )
        )
        if overlap < 0.55 and not text_match:
            continue
        score = overlap * 2.0 + (1.0 if text_match else 0.0)
        if best is None or score > best[0]:
            best = (score, block_id)
    return best[1] if best is not None else None


#: 首页署名区：题名、作者、单位、出版元数据。它们排在一起，题名领头。
FRONT_MATTER_ROLES = (
    "document-title",
    "author",
    "affiliation",
    "publication-metadata",
)


def _unit_role(unit: dict[str, Any]) -> str:
    return str(unit.get("_element_role") or "").lower()


def _front_matter_ordered(
    page_units: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """题名排在署名区最前面。

    期刊排版把版权栏和顶端的生产代码条印在题名之上，按坐标读出来的顺序
    就是"一串出版代码，然后才是题名"。读者要的是先看见题名，出版元数据
    紧随其后。这里只动题名之前的出版元数据，正文一条不碰。
    """

    roles = [_unit_role(unit) for unit in page_units]
    if "document-title" not in roles:
        return page_units
    title_index = roles.index("document-title")
    moved = [
        index
        for index in range(title_index)
        if roles[index] == "publication-metadata"
    ]
    if not moved:
        return page_units
    end = title_index + 1
    while end < len(page_units) and roles[end] in FRONT_MATTER_ROLES:
        end += 1
    moved_set = set(moved)
    head = [
        unit
        for index, unit in enumerate(page_units[:end])
        if index not in moved_set
    ]
    return (
        head
        + [page_units[index] for index in moved]
        + page_units[end:]
    )


def _footnotes_last(
    page_units: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """脚注排到本页正文之后。

    脚注在原文里印在页底，按坐标读出来却常夹在两段正文中间——通讯作者
    地址插在两个论点之间，读者的句子就被劈成两半。译本重新分页，"页底"
    这个位置没法照搬，但"正文读完再读注"这个次序照搬得了。
    """

    footnotes = [
        unit for unit in page_units if _unit_role(unit) == "footnote"
    ]
    if not footnotes or len(footnotes) == len(page_units):
        return page_units
    body = [unit for unit in page_units if _unit_role(unit) != "footnote"]
    # 第一条脚注前画一条短分隔线：读者据此知道下面不再是正文。
    footnotes = [{**footnotes[0], "_footnote_zone_start": True}] + footnotes[1:]
    return body + footnotes


def _ordered_page_units(
    page_units: list[dict[str, Any]],
    page_complex: list[dict[str, Any]],
    source_structure_page: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    page_units = _footnotes_last(_front_matter_ordered(page_units))
    if not page_units or not isinstance(source_structure_page, dict):
        return page_units
    ordered_block_ids: list[int] = []
    block_roles: dict[int, str] = {}
    for item in page_complex:
        if (
            not isinstance(item, dict)
            or str(item.get("method") or "")
            not in {
                "manual-reading-order-rebuild",
                "custom-page-reflow",
            }
        ):
            continue
        payload = item.get("payload")
        if not isinstance(payload, dict):
            continue
        for block_id in payload.get("ordered_block_ids", []):
            if (
                isinstance(block_id, int)
                and block_id not in ordered_block_ids
            ):
                ordered_block_ids.append(block_id)
        for group in payload.get("layout_groups", []):
            if not isinstance(group, dict):
                continue
            role = str(group.get("role") or "").strip()
            if not role:
                continue
            for block_id in group.get("block_ids", []):
                if isinstance(block_id, int):
                    block_roles.setdefault(block_id, role)
    if not ordered_block_ids:
        return page_units
    blocks = [
        block
        for block in source_structure_page.get("blocks", [])
        if isinstance(block, dict)
    ]
    if not blocks:
        return page_units
    rank = {
        block_id: index
        for index, block_id in enumerate(ordered_block_ids)
    }
    decorated: list[
        tuple[tuple[int, int, int], dict[str, Any]]
    ] = []
    for original_index, unit in enumerate(page_units):
        block_id = _source_block_for_unit(unit, blocks)
        rendered_unit = (
            {
                **unit,
                "_layout_role": block_roles[block_id],
            }
            if block_id in block_roles
            else unit
        )
        if block_id in rank:
            key = (0, rank[block_id], original_index)
        else:
            key = (1, original_index, original_index)
        decorated.append((key, rendered_unit))
    return [unit for _, unit in sorted(decorated, key=lambda item: item[0])]


def _reading_order_unit_roles(
    translation: dict[str, Any],
    complex_content: dict[str, Any],
    source_structure: dict[str, Any],
) -> dict[str, str]:
    units_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for unit in translation.get("units", []):
        if isinstance(unit, dict) and isinstance(unit.get("page"), int):
            units_by_page[int(unit["page"])].append(unit)
    complex_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for item in complex_content.get("items", []):
        if (
            isinstance(item, dict)
            and isinstance(item.get("page"), int)
            and item.get("status") == "ready"
        ):
            complex_by_page[int(item["page"])].append(item)
    structure_by_page = {
        int(page["page"]): page
        for page in source_structure.get("pages", [])
        if isinstance(page, dict) and isinstance(page.get("page"), int)
    }
    result: dict[str, str] = {}
    for page_number, page_units in units_by_page.items():
        for unit in page_units:
            reason = str(unit.get("keep_source_reason") or "").casefold()
            unit_id = str(unit.get("id") or "")
            if unit_id and (
                "脚注" in reason
                or "footnote" in reason
                or "注释" in reason
            ):
                result[unit_id] = "footnote"
        for unit in _ordered_page_units(
            page_units,
            complex_by_page.get(page_number, []),
            structure_by_page.get(page_number),
        ):
            role = str(unit.get("_layout_role") or "").strip()
            unit_id = str(unit.get("id") or "")
            if role and unit_id:
                result[unit_id] = role
    return result


def _cross_page_continuation_pairs(
    *,
    deps: StoryDeps,
    units_by_page: dict[int, list[dict[str, Any]]],
    complex_by_page: dict[int, list[dict[str, Any]]],
    retained_by_page: dict[int, list[dict[str, Any]]],
    source_document: Any,
    source_page_count: int,
) -> dict[str, dict[str, Any]]:
    visible_by_page: dict[int, list[dict[str, Any]]] = {}
    dimensions: dict[int, tuple[float, float]] = {}
    for page_number in range(1, source_page_count + 1):
        page = source_document[page_number - 1]
        page_width = float(page.rect.width)
        page_height = float(page.rect.height)
        dimensions[page_number] = (page_width, page_height)
        page_units = units_by_page.get(page_number, [])
        page_complex = complex_by_page.get(page_number, [])
        replaced_ids = deps.complex_replaced_unit_ids_fn(
            page_units,
            page_complex,
        )
        anchored_ids = {
            str(
                item.get("payload", {}).get("insert_before_unit_id")
                or item.get("payload", {}).get("insert_after_unit_id")
                or ""
            )
            for item in page_complex
            if isinstance(item, dict)
            and isinstance(item.get("payload"), dict)
        }
        visible_by_page[page_number] = [
            unit
            for unit in page_units
            if (
                str(unit.get("id") or "") not in replaced_ids
                and str(unit.get("id") or "") not in anchored_ids
                and not _unit_fully_covered_by_retained(
                    unit,
                    retained_by_page.get(page_number, []),
                )
                and not deps.is_nonsemantic_furniture_fn(
                    unit,
                    page_width=page_width,
                    page_height=page_height,
                )
            )
        ]

    pairs: dict[str, dict[str, Any]] = {}
    for page_number in range(1, source_page_count):
        if (
            complex_by_page.get(page_number)
            or complex_by_page.get(page_number + 1)
        ):
            continue
        page_width, page_height = dimensions[page_number]
        next_width, next_height = dimensions[page_number + 1]
        current_units = visible_by_page.get(page_number, [])
        following_units = visible_by_page.get(page_number + 1, [])
        main_units = [
            unit
            for unit in current_units
            if (
                str(unit.get("kind") or "").lower() == "body"
                and not _is_bottom_note_unit(
                    unit,
                    page_height=page_height,
                )
            )
        ]
        if not main_units or not following_units:
            continue
        previous = main_units[-1]
        previous_index = current_units.index(previous)
        if any(
            not _is_bottom_note_unit(unit, page_height=page_height)
            for unit in current_units[previous_index + 1 :]
        ):
            continue
        following = following_units[0]
        if _is_cross_page_continuation(
            previous,
            following,
            previous_page_width=page_width,
            previous_page_height=page_height,
            following_page_width=next_width,
            following_page_height=next_height,
        ):
            pairs[str(previous["id"])] = following
    return pairs


def _story(
    *,
    deps: StoryDeps,
    job: dict[str, Any],
    translation: dict[str, Any],
    complex_content: dict[str, Any],
    retained_payloads: list[dict[str, Any]],
    styles: dict[str, ParagraphStyle],
    source_document: Any,
    source_structure: dict[str, Any],
    available_width: float,
    available_height: float,
    regular_font: str,
    bold_font: str,
    body_font_pt: float,
    target_language: str,
    label_font_path: str | None = None,
) -> list[Flowable]:
    reference_state: dict[str, Any] = {}

    def reference_text_transform(text: str) -> str:
        """参考文献断词与折行 URL 的整理，词表按需建一次。

        必须吃**原始文本**（带换行）：断词判定靠的就是行尾的 "-\n"，
        换行一旦被上游折掉，net-works 是软断词还是真连字符就再也分不出来。
        """

        if "vocabulary" not in reference_state:
            document_text = unicodedata.normalize(
                "NFKC",
                "\n".join(
                    source_document[index].get_text("text")
                    for index in range(source_document.page_count)
                ),
            )
            reference_state["vocabulary"] = build_vocabulary(document_text)
            reference_state["forms"] = build_hyphenated_forms(document_text)
        value = unicodedata.normalize("NFKC", text or "")
        value = re.sub(r"\u00ad\s*", "", value)
        normalized, _decisions = normalize_reference_text(
            value,
            reference_state["vocabulary"],
            reference_state["forms"],
        )
        # 上游有的管线在更早处就把换行折掉了，伪影已经拼死在文本里，
        # 再补一遍按词表的固化修复。
        return repair_baked_line_artifacts(
            normalized,
            reference_state["vocabulary"],
            reference_state["forms"],
        )

    units_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for unit in translation.get("units", []):
        if isinstance(unit, dict) and isinstance(unit.get("page"), int):
            units_by_page[int(unit["page"])].append(unit)
    complex_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for item in complex_content.get("items", []):
        if (
            isinstance(item, dict)
            and isinstance(item.get("page"), int)
            and item.get("status") == "ready"
        ):
            complex_by_page[int(item["page"])].append(item)
    complex_coverage_by_page: dict[
        int,
        list[dict[str, Any]],
    ] = defaultdict(list)
    for items in complex_by_page.values():
        for item in items:
            for covered_page in deps.complex_item_source_pages_fn(item):
                complex_coverage_by_page[covered_page].append(item)
    structure_by_page = {
        int(page["page"]): page
        for page in source_structure.get("pages", [])
        if isinstance(page, dict) and isinstance(page.get("page"), int)
    }
    for page_number, page_units in tuple(units_by_page.items()):
        units_by_page[page_number] = _ordered_page_units(
            page_units,
            complex_by_page.get(page_number, []),
            structure_by_page.get(page_number),
        )
    retained_by_page = deps.retained_regions_by_page_fn(retained_payloads)
    source_page_count = int(job["source"]["page_count"])
    cross_page_pairs = _cross_page_continuation_pairs(
        deps=deps,
        units_by_page=units_by_page,
        complex_by_page=complex_coverage_by_page,
        retained_by_page=retained_by_page,
        source_document=source_document,
        source_page_count=source_page_count,
    )
    cross_page_consumed_ids = {
        str(unit["id"]) for unit in cross_page_pairs.values()
    }

    result: list[Flowable] = []
    reference_section_started = False
    started_source_pages: set[int] = set()
    for source_page in range(1, source_page_count + 1):
        source_page_width = float(
            source_document[source_page - 1].rect.width
        )
        source_page_height = float(
            source_document[source_page - 1].rect.height
        )
        page_units = units_by_page.get(source_page, [])
        page_complex = complex_by_page.get(source_page, [])
        page_complex_coverage = complex_coverage_by_page.get(
            source_page,
            [],
        )
        page_retained = retained_by_page.get(source_page, [])
        if (
            result
            and any(
                isinstance(item.get("payload"), dict)
                and item["payload"].get("page_break_before_source_page")
                is True
                for item in page_complex
            )
        ):
            result.append(PageBreak())
        source_id = f"source-page-{source_page:04d}"
        if source_page not in started_source_pages:
            result.append(
                MappingAnchor(
                    "start",
                    "source-page",
                    source_id,
                    source_page,
                )
            )
            started_source_pages.add(source_page)
        # 源页映射只靠上面的 MappingAnchor（零尺寸、不可见）。
        # 不再插入"原文第 X 页"可见段落——那是调试标记，读者不需要，
        # 它还会劈开跨源页的句子。映射结果照常写进 candidate-page-map.json。
        replace_items = [
            item
            for item in page_complex
            if _complex_render_policy(item) == "replace-page-units"
        ]
        anchored_items = [
            item
            for item in page_complex
            if isinstance(item.get("payload"), dict)
            and (
                item["payload"].get("insert_before_unit_id")
                or item["payload"].get("insert_after_unit_id")
            )
        ]
        before_items = [
            item
            for item in page_complex
            if _complex_render_policy(item) == "insert-before"
            and item not in anchored_items
        ]
        after_items = [
            item
            for item in page_complex
            if _complex_render_policy(item) == "insert-after"
            and item not in anchored_items
        ]
        page_unit_ids = {
            str(unit.get("id") or "")
            for unit in page_units
            if isinstance(unit, dict)
        }
        for item in anchored_items:
            payload = item["payload"]
            anchor_id = str(
                payload.get("insert_before_unit_id")
                or payload.get("insert_after_unit_id")
                or ""
            )
            if anchor_id not in page_unit_ids:
                raise StoryError(
                    f"复杂内容 {item.get('id')} 的插入锚点不存在于"
                    f"原文第 {source_page} 页: {anchor_id}"
                )
        if anchored_items and replace_items:
            raise StoryError(
                f"原文第 {source_page} 页不能同时使用整页替换与单元锚点"
            )
        retained_before = [
            payload
            for payload in page_retained
            if _retained_render_policy(
                payload,
                float(source_document[source_page - 1].rect.height),
            )
            == "insert-before"
        ]
        retained_after = [
            payload
            for payload in page_retained
            if payload not in retained_before
        ]
        if _retained_references_precede_visible_units(
            page_units,
            page_retained,
            page_complex_coverage,
            deps=deps,
            page_width=source_page_width,
            page_height=source_page_height,
        ):
            inferred_before = [
                payload
                for payload in retained_after
                if (
                    str(payload.get("category") or "")
                    in REFERENCE_CATEGORIES
                )
            ]
            retained_before.extend(inferred_before)
            retained_after = [
                payload
                for payload in retained_after
                if payload not in inferred_before
            ]

        def add_complex(
            item: dict[str, Any],
            *,
            # source_page 是循环内变量。用默认值在定义时当场绑定，
            # 取值和原来的闭包写法一致，只是不再依赖晚绑定。
            source_page: int = source_page,
        ) -> None:
            item_id = str(item.get("id") or f"p{source_page:04d}-complex")
            result.append(
                MappingAnchor("start", "complex", item_id, source_page)
            )
            result.extend(
                _complex_flowables(
                    item,
                    deps=deps,
                    styles=styles,
                    source_document=source_document,
                    available_width=available_width,
                    available_height=available_height,
                    regular_font=regular_font,
                    bold_font=bold_font,
                    body_font_pt=body_font_pt,
                    target_language=target_language,
                    label_font_path=label_font_path,
                )
            )
            result.append(
                MappingAnchor("end", "complex", item_id, source_page)
            )

        def add_retained(
            payload: dict[str, Any],
            *,
            force_render: bool = False,
            # source_page 是循环内变量。用默认值在定义时当场绑定，
            # 取值和原来的闭包写法一致，只是不再依赖晚绑定。
            source_page: int = source_page,
        ) -> None:
            nonlocal reference_section_started
            retained_id = str(payload["id"])
            is_reference = (
                str(payload.get("category") or "") in REFERENCE_CATEGORIES
            )
            result.append(
                MappingAnchor("start", "retained", retained_id, source_page)
            )
            result.extend(
                _retained_flowables(
                    (
                        {
                            **payload,
                            "already_present_in_translation": False,
                        }
                        if force_render
                        else payload
                    ),
                    deps=deps,
                    styles=styles,
                    target_language=target_language,
                    include_reference_heading=(
                        is_reference and not reference_section_started
                    ),
                    reference_text_transform=reference_text_transform,
                )
            )
            result.append(
                MappingAnchor("end", "retained", retained_id, source_page)
            )
            if is_reference and payload.get("blocks"):
                reference_section_started = True

        for item in before_items:
            add_complex(item)
        for payload in retained_before:
            add_retained(payload)
        reference_regions = [
            payload
            for payload in retained_after
            if str(payload.get("category") or "") in REFERENCE_CATEGORIES
        ]
        reference_only_page = bool(
            page_units
            and reference_regions
            and all(
                (
                    str(unit.get("kind") or "").lower()
                    in REFERENCE_KINDS
                    or _is_reference_heading_unit(unit)
                )
                for unit in page_units
            )
            and not replace_items
        )
        if reference_only_page:
            for unit in page_units:
                result.append(
                    MappingAnchor(
                        "start",
                        "unit",
                        str(unit["id"]),
                        source_page,
                    )
                )
            for payload in retained_after:
                add_retained(payload, force_render=True)
            for unit in page_units:
                result.append(
                    MappingAnchor(
                        "end",
                        "unit",
                        str(unit["id"]),
                        source_page,
                    )
                )
        elif replace_items:
            for unit in page_units:
                unit_id = str(unit["id"])
                result.append(
                    MappingAnchor("start", "unit", unit_id, source_page)
                )
            for item in replace_items:
                add_complex(item)
            for unit in page_units:
                unit_id = str(unit["id"])
                result.append(
                    MappingAnchor("end", "unit", unit_id, source_page)
                )
        else:
            suppressed_texts = [
                text
                for item in page_complex_coverage
                for text in _complex_embedded_texts(item)
            ]
            complex_replaced_unit_ids = deps.complex_replaced_unit_ids_fn(
                page_units,
                page_complex_coverage,
            )
            anchored_unit_ids = {
                str(
                    item["payload"].get("insert_before_unit_id")
                    or item["payload"].get("insert_after_unit_id")
                    or ""
                )
                for item in anchored_items
            }

            def unit_is_hidden(
                unit: dict[str, Any],
                *,
                # 下面几个都是循环内变量，用默认值当场绑定，取值不变。
                page_retained: list[dict[str, Any]] = page_retained,
                source_page_width: float | None = source_page_width,
                source_page_height: float | None = source_page_height,
                complex_replaced_unit_ids: set[str] = (
                    complex_replaced_unit_ids
                ),
            ) -> bool:
                unit_id = str(unit.get("id") or "")
                return bool(
                    _unit_fully_covered_by_retained(
                        unit,
                        page_retained,
                    )
                    or deps.is_nonsemantic_furniture_fn(
                        unit,
                        page_width=source_page_width,
                        page_height=source_page_height,
                    )
                    or unit_id in complex_replaced_unit_ids
                )

            unit_index = 0
            while unit_index < len(page_units):
                unit = page_units[unit_index]
                unit_id = str(unit.get("id") or "")
                if unit_id in cross_page_consumed_ids:
                    unit_index += 1
                    continue
                for item in anchored_items:
                    if (
                        str(
                            item["payload"].get(
                                "insert_before_unit_id"
                            )
                            or ""
                        )
                        == unit_id
                    ):
                        add_complex(item)
                if unit_is_hidden(unit):
                    result.append(
                        MappingAnchor(
                            "start",
                            "unit",
                            unit_id,
                            source_page,
                        )
                    )
                    result.append(
                        MappingAnchor(
                            "end",
                            "unit",
                            unit_id,
                            source_page,
                        )
                    )
                    rendered_units = [unit]
                else:
                    rendered_units = [unit]
                    same_page_unit_count = 1
                    if unit_id not in anchored_unit_ids:
                        next_index = unit_index + 1
                        while next_index < len(page_units):
                            next_unit = page_units[next_index]
                            next_id = str(next_unit.get("id") or "")
                            if (
                                next_id in anchored_unit_ids
                                or unit_is_hidden(next_unit)
                                or not _should_join_line_fragment(
                                    rendered_units,
                                    next_unit,
                                    page_width=source_page_width,
                                )
                            ):
                                break
                            rendered_units.append(next_unit)
                            next_index += 1
                        same_page_unit_count = len(rendered_units)
                    continuation = cross_page_pairs.get(
                        str(rendered_units[-1].get("id") or "")
                    )
                    if continuation is not None:
                        continuation_page = int(continuation["page"])
                        if continuation_page not in started_source_pages:
                            result.append(
                                MappingAnchor(
                                    "start",
                                    "source-page",
                                    (
                                        f"source-page-"
                                        f"{continuation_page:04d}"
                                    ),
                                    continuation_page,
                                )
                            )
                            started_source_pages.add(continuation_page)
                        rendered_units.append(continuation)
                    if len(rendered_units) > 1:
                        result.extend(
                            _joined_unit_flowables(
                                rendered_units,
                                styles,
                                suppressed_texts,
                                deps=deps,
                                target_language=target_language,
                            )
                        )
                    else:
                        result.extend(
                            _unit_flowables(
                                unit,
                                styles,
                                suppress_texts=suppressed_texts,
                                deps=deps,
                            )
                        )
                if any(
                    _is_reference_heading_unit(rendered_unit)
                    for rendered_unit in rendered_units
                ):
                    reference_section_started = True
                for item in anchored_items:
                    if (
                        str(
                            item["payload"].get(
                                "insert_after_unit_id"
                            )
                            or ""
                        )
                        == unit_id
                    ):
                        add_complex(item)
                unit_index += (
                    same_page_unit_count
                    if not unit_is_hidden(unit)
                    else 1
                )
        if not reference_only_page:
            for payload in retained_after:
                add_retained(payload)
        for item in after_items:
            add_complex(item)
        result.append(
            MappingAnchor("end", "source-page", source_id, source_page)
        )
    return result
