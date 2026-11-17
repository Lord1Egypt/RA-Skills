"""文本分块与标题资格判定：纯函数，不碰 ReportLab。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。

"谁是标题"这件事在这里只回答一半：``role_may_head`` 用**结构分析**给的
元素角色否决冻结标签（作者单位、arXiv 版本戳、图内标签长得再像标题
也不是标题），``looks_like_heading`` 只是外观启发式，没有否决权。
"""

from __future__ import annotations

import re
from typing import Any

REFERENCE_KINDS = {
    "reference",
    "references",
    "bibliography",
}
HEADING_KINDS = {"title", "subtitle", "heading", "section-heading"}


def split_blocks(text: str) -> list[str]:
    blocks = [
        block.strip()
        for block in re.split(r"\n\s*\n", text or "")
        if block.strip()
    ]
    return blocks or ([text.strip()] if text and text.strip() else [])


def unit_text_blocks(unit: dict[str, Any], text: str) -> list[str]:
    blocks = split_blocks(text)
    if len(blocks) <= 1:
        return blocks
    source_lines = [
        line.strip()
        for line in str(unit.get("source") or "").splitlines()
        if line.strip()
    ]
    edge_page_numbers = {
        line
        for line in (
            source_lines[:1] + source_lines[-1:]
            if source_lines
            else []
        )
        if re.fullmatch(r"\d{1,4}", line)
    }
    while (
        len(blocks) > 1
        and blocks[0].strip() in edge_page_numbers
    ):
        blocks.pop(0)
    while (
        len(blocks) > 1
        and blocks[-1].strip() in edge_page_numbers
    ):
        blocks.pop()
    return blocks


def role_may_head(unit: dict[str, Any]) -> bool:
    """这个单元有没有资格当标题。

    单元冻结时带的 kind / heading_level 是当年抽取启发式打的标签，
    和"看着像标题就算标题"是同一个来源。绑定的元素角色来自结构分析，
    它说不是标题（作者单位、arXiv 戳、正文句子），冻结标签就不作数。
    角色未知时不否决，维持原行为。
    """

    role = str(unit.get("_element_role") or "")
    return role in ("", "heading", "document-title")


def looks_like_heading(text: str) -> bool:
    compact = " ".join(text.split())
    if not compact or len(compact) > 42 or "\n" in text:
        return False
    return not compact.endswith(
        ("。", "！", "？", "；", "，", ".", "!", "?", ";", ",")
    )
