"""
BiliYouTik2Brain — Corrector Engine 退出条件、置信度过滤、回归检查、Gotchas

v3: 错题库改题型模式。反馈闭环 → feedback.py。
确定性规则（Gotchas/BLEEP/置信度裁剪）保留在此。
"""

from typing import List, Tuple, Dict
from .utils import safe_float
from ..corrector_dictionary import SPEECH_FILLERS, check_bleep


# ── 阈值 ──
HARD_THRESHOLD = 0.6       # 硬关阈值（低于此不应用）
LAYER_EXIT_THRESHOLD = 0.9 # 层退出阈值（所有词高于此→跳过后续层）


# ═══════════════════════════════════════════════════════════════
# Gotchas — 边界情况确定性检查
# ═══════════════════════════════════════════════════════════════

def handle_gotchas(original: str, corrected: str, confidence: float, context_snippet: str = "") -> dict:
    """处理各种边界情况 (Gotchas) — 代码做确定性规则检查
    
    Returns:
        {"corrected": str, "confidence": float, "evidence": str, 修改后的值}
    """
    result = {
        "corrected": corrected,
        "confidence": confidence,
        "evidence": "",
    }
    
    # 1. 字幕*** → 保持消音标记
    if '*' in original or '*' in corrected:
        result["corrected"] = "[消音]"
        result["confidence"] = min(confidence, 0.9)
        result["evidence"] = " [Gotcha: 字幕消音标记]"
    
    # 2. BLEEP → 保持标记
    if 'BLEEP' in original or '[BLEEP]' in context_snippet:
        result["corrected"] = "[消音]"
        result["confidence"] = min(confidence, 0.85)
        result["evidence"] = " [Gotcha: 音频BLEEP]"
    
    # 3. 口语填充词 → 不修正
    if original.strip() in SPEECH_FILLERS:
        result["confidence"] = 0.0
        result["evidence"] = " [Gotcha: 口语填充词]"
    
    # 4. 置信度边界裁剪
    result["confidence"] = max(0.0, min(1.0, result["confidence"]))
    
    return result


# ═══════════════════════════════════════════════════════════════
# 退出条件检查
# ═══════════════════════════════════════════════════════════════

def check_exit(low_conf_words: List[Tuple[str, float]],
               applied_corrections: Dict[str, dict]) -> bool:
    """检查是否所有低置信词都已被高置信修正覆盖"""
    remaining = []
    for w, c in low_conf_words:
        if w not in applied_corrections:
            remaining.append(w)
        elif applied_corrections[w].get("confidence", 0) < LAYER_EXIT_THRESHOLD:
            remaining.append(w)
    return len(remaining) == 0


def get_remaining_words(low_conf_words: List[Tuple[str, float]],
                        applied_corrections: Dict[str, dict]) -> List[Tuple[str, float]]:
    """获取仍未高置信修正的低置信词"""
    remaining = []
    for w, c in low_conf_words:
        if w not in applied_corrections:
            remaining.append((w, c))
        elif applied_corrections[w].get("confidence", 0) < LAYER_EXIT_THRESHOLD:
            remaining.append((w, c))
    return remaining


# ═══════════════════════════════════════════════════════════════
# 置信度过滤
# ═══════════════════════════════════════════════════════════════

def filter_by_confidence(candidates: List[dict]) -> List[dict]:
    """硬关阈值过滤 — 低于HARD_THRESHOLD的修正不应用"""
    return [c for c in candidates if c.get("confidence", 0) >= HARD_THRESHOLD]


# ═══════════════════════════════════════════════════════════════
# 回归检查
# ═══════════════════════════════════════════════════════════════

def regression_check(original: str, corrected: str) -> Tuple[bool, List[str]]:
    """修正前后整段语义一致性检查
    
    代码做事实检查:
      1. 修正后文本不能缩短超过10%
      2. 修正后不能出现连续重复字符超过40字（死循环防性护）
      3. 修正后不能全是单一字符重复
    """
    issues = []
    
    # 1. 长度检查
    len_ratio = len(corrected) / max(len(original), 1)
    if len_ratio < 0.9:
        issues.append(f"文本缩短超过10% ({len(original)}→{len(corrected)})")
    if len_ratio > 1.5:
        issues.append(f"文本增长超过50% ({len(original)}→{len(corrected)})")
    
    # 2. 死循环检查
    if len(corrected) >= 40:
        for i in range(len(corrected) - 10):
            segment = corrected[i:i+10]
            repeats = corrected.count(segment)
            if repeats > 3 and len(segment) >= 5:
                issues.append(f"发现连续重复模式: '{segment[:10]}' 出现{repeats}次")
                break
    
    # 3. 单一字符重复
    if corrected and len(corrected) >= 20:
        unique_chars = len(set(corrected))
        if unique_chars <= 3:
            issues.append(f"仅含{unique_chars}个不同字符, 疑似死循环")
    
    return len(issues) == 0, issues


def needs_regression_check(applied_count: int, text_len: int) -> bool:
    """判断是否需要进行回归检查"""
    min_changes = max(3, int(text_len * 0.005))
    return applied_count >= min_changes
