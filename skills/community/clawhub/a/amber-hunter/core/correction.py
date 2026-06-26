"""
core/correction.py — Self-Correction Loop Analysis v1.2.29 G1
标签/分类校正统计 + 规则建议生成
"""
from __future__ import annotations

import time
from typing import Optional


def analyze_corrections(
    field: str = "",
    min_count: int = 2,
) -> dict:
    """
    分析校正数据，生成可读的统计报告。
    返回 {patterns: [{original, suggested, count, strength}], summary: str}
    strength = high/medium/low（基于 count 和置信度）
    """
    from core.db import get_correction_stats, get_correction_suggestions

    stats = get_correction_stats(field)
    suggestions = get_correction_suggestions(threshold=2)

    patterns = []
    for s in suggestions:
        if s["count"] < min_count:
            continue
        strength = "high" if s["count"] >= 5 else "medium" if s["count"] >= 3 else "low"
        patterns.append({
            "original": s["original"],
            "suggested": s["suggested"],
            "count": s["count"],
            "strength": strength,
            "confidence": round(s["confidence"], 2),
        })

    # 生成文字摘要
    if not patterns:
        summary = "未检测到重复校正模式，系统表现正常。"
    elif len(patterns) == 1:
        p = patterns[0]
        summary = f"检测到校正模式：'{p['original']}' 经常被修正为 '{p['suggested']}'（{p['count']}次），建议自动替换。"
    else:
        top = patterns[0]
        summary = f"检测到 {len(patterns)} 个校正模式。最常见：'{top['original']}' → '{top['suggested']}'（{top['count']}次）。"

    return {
        "patterns": patterns,
        "summary": summary,
        "total_corrections": stats["total"],
    }


def record_tag_correction(
    original_tag: str,
    corrected_tag: str,
    session_id: str | None = None,
    queue_id: str | None = None,
) -> str:
    """记录一次标签校正事件"""
    from core.db import record_correction
    return record_correction(
        field="tag",
        original_value=original_tag.strip().lower(),
        corrected_value=corrected_tag.strip().lower(),
        source="queue_edit",
        session_id=session_id,
        queue_id=queue_id,
        confidence=1.0,
    )


def record_category_correction(
    original_category: str,
    corrected_category: str,
    session_id: str | None = None,
    queue_id: str | None = None,
) -> str:
    """记录一次分类校正事件"""
    from core.db import record_correction
    return record_correction(
        field="category",
        original_value=original_category.strip().lower(),
        corrected_value=corrected_category.strip().lower(),
        source="queue_edit",
        session_id=session_id,
        queue_id=queue_id,
        confidence=1.0,
    )


def record_rejection(
    memo: str,
    reason: str = "",
    session_id: str | None = None,
    queue_id: str | None = None,
) -> str:
    """记录一次记忆被拒绝"""
    from core.db import record_correction
    return record_correction(
        field="reject",
        original_value=memo[:200],
        corrected_value=reason or "rejected",
        source="queue_edit",
        session_id=session_id,
        queue_id=queue_id,
        confidence=1.0,
    )


def get_tag_rules() -> dict[str, str]:
    """返回已采纳的 tag 替换规则：{original: corrected}"""
    from core.db import get_tag_corrections
    return get_tag_corrections()


def apply_tag_rule(original: str, corrected: str) -> bool:
    """采纳一条 tag 替换建议"""
    from core.db import apply_correction_suggestion
    return apply_correction_suggestion(original, corrected, field="tag")
