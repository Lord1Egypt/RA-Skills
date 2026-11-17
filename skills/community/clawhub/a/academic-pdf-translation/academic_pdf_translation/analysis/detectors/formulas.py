"""公式检测。

独立公式必须自成元素：它一旦被当成普通文字流，求和号会变成字母、
分式线会消失、根号会变成字母。快速档对公式一律保留原区域，
前提是先能把它认出来。
"""

from __future__ import annotations

import re
from typing import Any

from academic_pdf_translation.contracts.models import (
    normalize_bbox,
    union_bbox,
)

DETECTOR_VERSION = "formulas-v1"

#: 行尾的公式编号，例如 "(1)"、"(2.3)"。
FORMULA_NUMBER_RE = re.compile(r"\(\s*(\d+(?:\.\d+)*[a-z]?)\s*\)\s*$")
#: 数学符号。出现得越密，越可能是公式而不是句子。
MATH_CHARS = set(
    "=+−-×÷±∓≈≠≤≥<>∈∉⊂⊃∪∩∑∏∫√∂∇∞→←↔⇒⇔∀∃¬∧∨⊕⊗"
    "αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ"
    "ˆ˜¯′″‴⌊⌋⌈⌉|/^_"
)
SUPERSCRIPT_CHARS = set("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")
PROSE_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]{2,}")

#: 数学符号密度超过它就认为是公式片段。
MATH_DENSITY_FLOOR = 0.10
#: 公式片段里允许出现的普通词上限。
MAX_PROSE_WORDS = 3
#: 公式主体与编号之间的最大垂直错位。
FORMULA_NUMBER_ROW_TOLERANCE_PT = 14.0


def math_density(text: str) -> float:
    stripped = [char for char in str(text or "") if not char.isspace()]
    if not stripped:
        return 0.0
    hits = sum(
        1
        for char in stripped
        if char in MATH_CHARS or char in SUPERSCRIPT_CHARS
    )
    return hits / len(stripped)


def looks_like_formula(text: str) -> bool:
    value = str(text or "").strip()
    if not value:
        return False
    prose = [
        word
        for word in PROSE_WORD_RE.findall(value)
        if not word.isupper()
    ]
    if len(prose) > MAX_PROSE_WORDS:
        return False
    return math_density(value) >= MATH_DENSITY_FLOOR


def formula_number(text: str) -> str | None:
    match = FORMULA_NUMBER_RE.search(str(text or "").strip())
    return match.group(1) if match else None


def detect_display_formulas(page: dict[str, Any]) -> list[dict[str, Any]]:
    """把相邻的公式片段合并成独立公式元素。

    数学排版常把一个公式拆成好几个文本块（求和号、上下标、主体、编号
    各一块）。这里按垂直邻接把它们合回去。
    """

    candidates: list[dict[str, Any]] = []
    for block in page.get("blocks") or []:
        if block.get("page_furniture"):
            continue
        text = str(block.get("text") or "")
        box = normalize_bbox(block.get("bbox"))
        if box is None:
            continue
        if not looks_like_formula(text):
            continue
        candidates.append(
            {
                "block": block,
                "bbox": box,
                "text": text.strip(),
                "number": formula_number(text),
            }
        )
    if not candidates:
        return []
    candidates.sort(key=lambda item: (item["bbox"][1], item["bbox"][0]))

    groups: list[list[dict[str, Any]]] = []
    for item in candidates:
        if groups:
            previous = groups[-1][-1]
            gap = item["bbox"][1] - previous["bbox"][3]
            if gap <= FORMULA_NUMBER_ROW_TOLERANCE_PT:
                groups[-1].append(item)
                continue
        groups.append([item])

    formulas: list[dict[str, Any]] = []
    for group in groups:
        bbox = union_bbox([item["bbox"] for item in group])
        if bbox is None:
            continue
        numbers = [item["number"] for item in group if item["number"]]
        text = " ".join(item["text"] for item in group)
        density = math_density(text)
        confidence = min(0.95, 0.55 + density * 1.5 + (0.15 if numbers else 0.0))
        formulas.append(
            {
                "bbox": bbox,
                "block_ids": [int(item["block"]["id"]) for item in group],
                "text": text,
                "formula_number": numbers[-1] if numbers else None,
                "math_density": round(density, 4),
                "fragment_count": len(group),
                "confidence": round(confidence, 4),
            }
        )
    return formulas
