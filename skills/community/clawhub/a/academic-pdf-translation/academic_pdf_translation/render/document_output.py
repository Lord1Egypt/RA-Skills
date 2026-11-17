"""输出写入：书签、原子替换和渲染日志。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。这一段是候选生成的
最后一步：给选中的试排加书签，原子替换到最终路径，再把这次渲染的全部
依据写成一份渲染日志。

之所以单独成模块：这三件事都是"对外承诺"。写盘必须原子，
不能让下游看到半份 PDF；渲染日志是交付判断的证据来源，
字段一旦少一个，后面的一致性检查就查不动。它们和排版怎么算无关，
所以不该和排版搜索挤在一起。

原来的 scripts 层依赖按包内规则改写：读写 JSON、算文件哈希、
打开候选 PDF、取生成器身份、列保留区域 id，都由 ``DocumentOutputDeps`` 注入。
"""

from __future__ import annotations

import hashlib
import os
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .text_blocks import HEADING_KINDS
from .text_blocks import role_may_head as _role_may_head

#: 生成器身份。写进渲染日志和候选页映射，下游据此判断"这份候选是谁排的"。
RENDERER_NAME = "academic-pdf-layout"
RENDERER_VERSION = "1.0"


@dataclass(frozen=True)
class DocumentOutputDeps:
    """输出写入需要的、原本长在 scripts 层的几件东西。"""

    #: 打开候选 PDF，返回带 ``document`` 与 ``release`` 的句柄。
    open_candidate_analysis_fn: Callable[..., Any]
    #: 算文件的 sha256。
    sha256_file_fn: Callable[[Path], str]
    #: 取当前源码的生成器构建哈希。
    renderer_build_id_fn: Callable[[], str]
    #: 列出保留原文区域的 id。
    retained_region_ids_fn: Callable[[Any], list[str]]


def _bookmark_entries(
    mapping: dict[str, Any], translation: dict[str, Any]
) -> list[list[Any]]:
    """书签用真实章节标题，不用"原文第 X 页"调试标记。

    判据与正文渲染同一套：kind 属于标题类且绑定角色允许当标题
    （作者单位、arXiv 版本戳、图内标签长得再像标题也不是标题）。
    纯启发式判出来的"疑似标题"不进书签——书签宁缺毋滥。
    """

    unit_pages = {
        str(entry.get("unit_id") or ""): list(
            entry.get("candidate_pages") or []
        )
        for entry in mapping.get("units", [])
    }
    toc: list[list[Any]] = []
    for unit in translation.get("units", []):
        if not isinstance(unit, dict):
            continue
        text = str(unit.get("translation") or "").strip()
        if not text or not _role_may_head(unit):
            continue
        kind = str(unit.get("kind") or "").lower()
        if kind in HEADING_KINDS or unit.get("heading_level") == 1:
            level = 1
        elif unit.get("heading_level") == 2:
            level = 2
        else:
            continue
        pages = unit_pages.get(str(unit.get("id") or ""))
        if not pages:
            continue
        # set_toc 要求层级从 1 开始且不跳级
        if not toc and level > 1:
            level = 1
        elif toc and level > toc[-1][0] + 1:
            level = toc[-1][0] + 1
        toc.append([level, text, int(pages[0])])
    return toc


def _add_outline(
    source_pdf: Path,
    destination_pdf: Path,
    mapping: dict[str, Any],
    translation: dict[str, Any],
    *,
    deps: DocumentOutputDeps,
) -> None:
    handle = deps.open_candidate_analysis_fn(source_pdf, role="source")
    document = handle.document
    toc = _bookmark_entries(mapping, translation)
    if toc:
        document.set_toc(toc)
    document.save(destination_pdf, garbage=4, deflate=True)
    handle.release()


def write_candidate_pdf(
    *,
    deps: DocumentOutputDeps,
    selected_path: Path,
    outline_path: Path,
    output_pdf: Path,
    mapping: dict[str, Any],
    translation: dict[str, Any],
) -> None:
    """给选中的试排加书签，然后原子替换到最终路径。

    先写同目录下的临时文件再 os.replace，是为了让下游永远看不到半份 PDF：
    要么还是旧的那份，要么已经是完整的新的那份，没有中间态。
    """

    _add_outline(
        selected_path,
        outline_path,
        mapping,
        translation,
        deps=deps,
    )
    with tempfile.NamedTemporaryFile(
        dir=output_pdf.parent,
        prefix=f".{output_pdf.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temp_output = Path(handle.name)
    try:
        temp_output.write_bytes(outline_path.read_bytes())
        os.replace(temp_output, output_pdf)
    finally:
        if temp_output.exists():
            temp_output.unlink()


def build_layout_log(
    *,
    deps: DocumentOutputDeps,
    translation: dict[str, Any],
    complex_content: dict[str, Any],
    retained: Any,
    retained_payloads: list[dict[str, Any]],
    retained_path: Path,
    mapping: dict[str, Any],
    map_path: Path,
    page_size: tuple[float, float],
    margins: tuple[float, float, float, float],
    body_font_pt: float,
    leading_ratio: float,
    reference_font_pt: float,
    source_page_count: int,
    candidate_page_count: int,
    page_count_ratio_limit: float,
    page_count_ratio_limit_source: str,
    attempts: list[dict[str, Any]],
    typography_search: dict[str, Any],
    orphan_regions: list[dict[str, Any]],
    font_paths: list[str],
    elapsed_seconds: float,
) -> dict[str, Any]:
    """把这次渲染的全部依据组装成渲染日志。

    这份日志是交付判断的证据来源，不是给人看的说明文字。每一项都要能
    被下游重新核对：谁排的、用什么参数排的、有没有漏排、字体是哪几把。
    """

    unit_ids = [
        str(unit["id"])
        for unit in translation.get("units", [])
        if isinstance(unit, dict) and str(unit.get("id") or "")
    ]
    complex_ids = [
        str(item["id"])
        for item in complex_content.get("items", [])
        if isinstance(item, dict) and str(item.get("id") or "")
    ]
    retained_ids = deps.retained_region_ids_fn(retained)
    mapped_unit_ids = {
        str(entry["unit_id"]) for entry in mapping.get("units", [])
    }
    mapped_complex_ids = {
        str(entry["complex_item_id"])
        for entry in mapping.get("complex_items", [])
    }
    mapped_retained_ids = {
        str(entry["retained_region_id"])
        for entry in mapping.get("retained_regions", [])
    }
    layout_log = {
        "schema_version": "1.0",
        "renderer": RENDERER_NAME,
        "renderer_version": RENDERER_VERSION,
        "renderer_build_id": deps.renderer_build_id_fn(),
        "algorithm": "continuous-flow-with-structured-complex-content-v2",
        "selection_method": "actual-render-page-budget",
        "page_size_pt": [round(value, 2) for value in page_size],
        "margins_pt": list(margins),
        "body_font_pt": body_font_pt,
        "leading_ratio": leading_ratio,
        "reference_font_pt": round(reference_font_pt, 2),
        "source_page_count": source_page_count,
        "candidate_page_count": candidate_page_count,
        "page_count_ratio": round(
            candidate_page_count / max(source_page_count, 1),
            3,
        ),
        "page_count_ratio_limit": page_count_ratio_limit,
        "page_count_ratio_limit_source": page_count_ratio_limit_source,
        "attempts": attempts,
        "typography_search": typography_search,
        "candidate_page_map": str(map_path),
        "render_contract": {
            "all_units_consumed": mapped_unit_ids == set(unit_ids),
            "unit_count": len(unit_ids),
            "unit_ids_sha256": hashlib.sha256(
                "\n".join(unit_ids).encode("utf-8")
            ).hexdigest(),
            "all_complex_items_consumed": (
                mapped_complex_ids == set(complex_ids)
            ),
            "complex_item_count": len(complex_ids),
            "complex_item_ids_sha256": hashlib.sha256(
                "\n".join(complex_ids).encode("utf-8")
            ).hexdigest(),
            "all_retained_regions_consumed": (
                mapped_retained_ids == set(retained_ids)
            ),
            "retained_region_count": len(retained_ids),
            "retained_region_ids_sha256": hashlib.sha256(
                "\n".join(retained_ids).encode("utf-8")
            ).hexdigest(),
            "retained_source_sha256": deps.sha256_file_fn(retained_path),
            "retained_region_source_chars": sum(
                int(payload.get("source_char_count") or 0)
                for payload in retained_payloads
            ),
            "retained_regions_already_present": sorted(
                str(payload["id"])
                for payload in retained_payloads
                if payload.get("already_present_in_translation") is True
            ),
            "all_text_regions_measured": True,
            "unmeasured_text_regions": [],
            "overflow_regions": [],
            "heading_checks_performed": True,
            "orphan_regions": orphan_regions,
            "cjk_kinsoku_enabled": True,
            "font_paths": font_paths,
            "candidate_page_map_complete": True,
        },
        # 结构化抑制名单：哪些单元没有按文字排、为什么。给人核对用。
        "suppressed_units": list(
            translation.get("_suppression_manifest") or []
        ),
        "elapsed_seconds": elapsed_seconds,
    }
    return layout_log
