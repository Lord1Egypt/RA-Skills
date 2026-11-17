"""Deterministic, font-aware text measurement (P4).

Widths come from the shipped metrics registry (engine/font_metrics.py):
real measured tables for known families, a slightly conservative
categorical model otherwise. Never a live font query at compile time —
same checkout, same numbers, on every machine.

The contract with QA: `paragraphs_height_emu` is THE shared formula —
layout fits with it, QA re-checks with it, so the two can never disagree.
"""

from __future__ import annotations

from .font_metrics import char_width_em

EMU_PER_PT = 12700


def text_width_pt(text: str, size_cpt: int, family: str | None = None) -> float:
    size_pt = size_cpt / 100
    return sum(char_width_em(c, family) * size_pt for c in text)


def wrap_lines(text: str, size_cpt: int, width_emu: int,
               family: str | None = None) -> int:
    """Estimated wrapped line count for text in a box of width_emu."""
    if not text:
        return 0
    max_width_pt = max(width_emu / EMU_PER_PT, 1.0)
    size_pt = size_cpt / 100
    lines, current = 1, 0.0
    for char in text:
        w = char_width_em(char, family) * size_pt
        if current + w > max_width_pt:
            lines += 1
            current = w
        else:
            current += w
    return lines


def text_height_emu(text: str, size_cpt: int, width_emu: int,
                    line_height_pct: int = 135,
                    family: str | None = None) -> int:
    lines = max(wrap_lines(text, size_cpt, width_emu, family), 1)
    line_emu = int(size_cpt / 100 * line_height_pct / 100 * EMU_PER_PT)
    return lines * line_emu


def paragraphs_height_emu(paragraphs: list[dict], width_emu: int) -> int:
    """Estimated total height of render-plan paragraphs in a box.

    Uses each paragraph's first run for font/size (engine layouts emit
    single-run paragraphs; mixed-run paragraphs measure conservatively
    at the largest size).
    """
    total = 0
    for para in paragraphs:
        runs = para.get("runs", [])
        text = "".join(r["text"] for r in runs)
        size = max((r["size_cpt"] for r in runs), default=1200)
        family = runs[0].get("font") if runs else None
        total += text_height_emu(text, size, width_emu,
                                 para.get("line_height_pct", 135), family)
        total += int(para.get("space_after_cpt", 0) / 100 * EMU_PER_PT)
    return total


def fit_size_cpt(text: str, width_emu: int, height_emu: int,
                 levels_cpt: list[int], line_height_pct: int = 135,
                 family: str | None = None) -> int | None:
    """Largest size level at which text fits the box; None if even the
    smallest overflows (caller must truncate — deterministically)."""
    for size in levels_cpt:
        if text_height_emu(text, size, width_emu, line_height_pct, family) <= height_emu:
            return size
    return None


def truncate_to_fit(text: str, size_cpt: int, width_emu: int, height_emu: int,
                    line_height_pct: int = 135,
                    family: str | None = None) -> str:
    """Deterministic truncation rule (D9): cut at the last fitting char
    and close with an ellipsis."""
    if text_height_emu(text, size_cpt, width_emu, line_height_pct, family) <= height_emu:
        return text
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        candidate = text[:mid] + "…"
        if text_height_emu(candidate, size_cpt, width_emu,
                           line_height_pct, family) <= height_emu:
            lo = mid
        else:
            hi = mid - 1
    return (text[:lo] + "…") if lo else "…"
