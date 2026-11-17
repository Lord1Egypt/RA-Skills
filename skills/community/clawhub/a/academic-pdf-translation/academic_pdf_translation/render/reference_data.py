"""参考文献的数据判定：哪一段是文献标题、题录用多大字号。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。都是纯函数：
吃单元或作业配置，吐字符串与数字，不碰 ReportLab。
"""

from __future__ import annotations

import re
from typing import Any

from academic_pdf_translation.render.text_blocks import (
    HEADING_KINDS,
    split_blocks,
)

#: 保留区域的文献类目名。它决定一块保留区域是不是"题录"，
#: 进而决定排版顺序与字号。以前长在 scripts/retained_source.py，
#: 包内也要用，就挪到这里做唯一定义，scripts 侧改成从这里取。
REFERENCE_CATEGORIES = {"references", "bibliography"}

#: 各语言的"参考文献"标题写法。判定按去空白后的前缀匹配。
REFERENCE_HEADING_TOKENS = (
    "参考文献",
    "參考文獻",
    "references",
    "bibliography",
    "参考資料",
    "참고문헌",
)

def _reference_unit_parts(unit: dict[str, Any]) -> tuple[str, str]:
    text = str(
        unit.get("translation")
        or unit.get("source")
        or ""
    ).strip()
    blocks = split_blocks(text)
    if not blocks:
        return "", ""
    first = re.sub(r"\s+", "", blocks[0]).casefold()
    if any(
        first.startswith(token.casefold())
        for token in REFERENCE_HEADING_TOKENS
    ):
        return blocks[0], "\n\n".join(blocks[1:])
    return "", text


def _is_reference_heading_unit(unit: dict[str, Any]) -> bool:
    kind = str(unit.get("kind") or "").lower()
    if kind not in HEADING_KINDS:
        return False
    text = re.sub(
        r"\s+",
        "",
        str(unit.get("translation") or unit.get("source") or ""),
    ).casefold()
    return any(
        text.startswith(token.casefold())
        for token in REFERENCE_HEADING_TOKENS
    )


def _reference_font_size(job: dict[str, Any], body_font_pt: float) -> float:
    quality = job.get("quality", {})
    search = quality.get("typography_search") or {}
    configured = search.get("reference_font_range_pt", [8.2, 10.5])
    if not (
        isinstance(configured, list)
        and len(configured) == 2
        and all(isinstance(value, (int, float)) for value in configured)
    ):
        configured = [8.2, 10.5]
    lower, upper = sorted(map(float, configured))
    lower = max(lower, float(quality.get("body_font_min_pt", 8.0)))
    upper = max(upper, lower)
    return round(min(max(body_font_pt * 0.9, lower), upper), 2)


