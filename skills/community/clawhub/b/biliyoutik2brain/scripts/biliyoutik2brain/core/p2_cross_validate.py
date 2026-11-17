"""
BiliYouTik2Brain — P2 三源仲裁验证 (Phase 2.2)

在 P2 六维动态阈值触发后执行。
用三个独立来源交叉验证"P2 是否误报"，避免不必要升级。

三源权重（经验值）:
  - Whisper原始置信度 (25%): 低置信词本身的可信度
  - 字幕/OCR交叉证据 (50%): 外部来源对词是否存在的客观证据
  - 说话人知识 (25%): UP主历史用语模式校验

设计原则：不修改现有模块(p2_decision)，只增加验证层。
所有现有接口保持原样，在 retry_orchestrator 中插入验证。
"""

from __future__ import annotations

import re
import math
from typing import Dict, List, Optional, Tuple


# ── 默认权重 ──
W_WHISPER = 0.25      # 源1: Whisper原始置信度
W_CROSS = 0.50        # 源2: 字幕/OCR交叉证据
W_SPEAKER = 0.25      # 源3: 说话人知识


def tri_source_validate(
    unresolved_words: List[str],
    p2_debug: Dict,
    full_text: str,
    subtitle_text: str = "",
    subtitle_segments: Optional[List[Dict]] = None,
    ocr_persistent: str = "",
    speaker_profile: Optional[Dict] = None,
    weights: Optional[Dict[str, float]] = None,
) -> Dict:
    """三源仲裁验证主入口

    对 P2 触发的犹豫词做三源加权投票，判断 P2 是否真实需要升级。

    Args:
        unresolved_words: L5残留的犹豫词列表（原始字符串列表）
        p2_debug: should_retranscribe() 返回的 debug dict
        full_text: 全文转录文本
        subtitle_text: B站官方字幕拼接文本
        subtitle_segments: 字幕分段 [{text, start, end}]
        ocr_persistent: OCR 持久文本（多帧累积的关键文字）
        speaker_profile: get_profile(uploader) 返回的知识档案
        weights: 三源权重覆盖，默认 {whisper: 0.25, cross: 0.50, speaker: 0.25}

    Returns:
        dict with:
            - confidence: float (0.0~1.0)，越高表示"P2真实需要升级"
            - recommendation: "honor" | "override" | "downgrade"
            - whisper_score: float (源1得分)
            - cross_evidence_score: float (源2得分)
            - speaker_knowledge_score: float (源3得分)
            - word_breakdown: [{word, whisper_conf, cross_conf, speaker_conf, combined}, ...]
            - details: 人类可读的决策理由
    """
    if not unresolved_words:
        return {
            "confidence": 0.0,
            "recommendation": "override",
            "whisper_score": 0.0,
            "cross_evidence_score": 0.0,
            "speaker_knowledge_score": 0.0,
            "word_breakdown": [],
            "details": "无犹豫词，P2 无需触发",
        }

    w = weights or {}
    w_w = w.get("whisper", W_WHISPER)
    w_c = w.get("cross", W_CROSS)
    w_s = w.get("speaker", W_SPEAKER)

    # ── 逐词分析 ──
    word_breakdown = []
    for word in unresolved_words:
        if not word or not isinstance(word, str):
            continue

        # 源1: Whisper 原始置信度得分
        # 如果词出现在全文中 → 说明 whisper 听到了，置信度较高
        # 如果词不在全文中 → 说明 whisper 也没把握，得分低
        w_score = _whisper_confidence_score(word, full_text)
        if isinstance(word, str):
            pass

        # 源2: 字幕/OCR 交叉证据得分
        c_score = _cross_evidence_score(
            word, subtitle_text, subtitle_segments, ocr_persistent
        )

        # 源3: 说话人知识得分
        s_score = _speaker_knowledge_score(word, speaker_profile)

        # 词级综合
        combined = w_w * w_score + w_c * (1.0 - c_score) + w_s * (1.0 - s_score)
        # 解释：cross_evidence_score 高 = 外部证据确认词存在 → 不需要升级
        # 所以用 1.0 - cross_evidence_score 映射为"需要升级的程度"

        word_breakdown.append({
            "word": word,
            "whisper_conf": round(w_score, 3),
            "cross_evidence": round(c_score, 3),
            "speaker_known": round(s_score, 3),
            "combined": round(combined, 3),
        })

    # ── 汇总得分 ──
    if not word_breakdown:
        return {
            "confidence": 0.0,
            "recommendation": "override",
            "whisper_score": 0.0,
            "cross_evidence_score": 0.0,
            "speaker_knowledge_score": 0.0,
            "word_breakdown": [],
            "details": "所有犹豫词都为空，跳过",
        }

    n = len(word_breakdown)
    whisper_score = sum(b["whisper_conf"] for b in word_breakdown) / n
    cross_evidence_score = sum(b["cross_evidence"] for b in word_breakdown) / n
    speaker_knowledge_score = sum(b["speaker_known"] for b in word_breakdown) / n

    # 综合置信度: 三源加权
    confidence = (
        w_w * whisper_score
        + w_c * (1.0 - cross_evidence_score)   # 外部证据低 → 需要升级
        + w_s * (1.0 - speaker_knowledge_score) # 说话人未确认 → 需要升级
    )

    # ── 生成推荐 ──
    severity = p2_debug.get("effective", 0) / max(p2_debug.get("threshold", 0.05), 0.001)
    
    if confidence < 0.3:
        recommendation = "override"
        details = _generate_details(word_breakdown, whisper_score, cross_evidence_score,
                                     speaker_knowledge_score, confidence, severity, "override")
    elif confidence > 0.7:
        recommendation = "honor"
        details = _generate_details(word_breakdown, whisper_score, cross_evidence_score,
                                     speaker_knowledge_score, confidence, severity, "honor")
    else:
        recommendation = "downgrade"
        details = _generate_details(word_breakdown, whisper_score, cross_evidence_score,
                                     speaker_knowledge_score, confidence, severity, "downgrade")

    return {
        "confidence": round(confidence, 3),
        "recommendation": recommendation,
        "whisper_score": round(whisper_score, 3),
        "cross_evidence_score": round(cross_evidence_score, 3),
        "speaker_knowledge_score": round(speaker_knowledge_score, 3),
        "word_breakdown": word_breakdown,
        "details": details,
    }


# ═══════════════════════════════════════════════════════════════
# 源1: Whisper 原始置信度得分 (25%)
# ═══════════════════════════════════════════════════════════════
# 基于 whisper 跨序列核的置信度评估。
# 如果犹豫词在最终转录文本中保留（改拼写/大小写后仍存在），
# 说明模型对它有基础把握，得分高。
# 如果词被 L1-L5 完全修正掉不在原文中，得分低。
# ═══════════════════════════════════════════════════════════════

def _whisper_confidence_score(word: str, full_text: str) -> float:
    """Whisper 原始置信度得分 (0~1)
    
    判断 whisper 是否"听到了"这个词。
    method: 检查词（或其子串部分）是否出现在最终文本中。
    
    Returns:
        1.0: 词原样存在于全文（whisper 有把握）
        0.7: 中文词 - 部分匹配（有共同子串）
        0.5: 英文词 - 模糊匹配（共同字母较多）
        0.3: 有部分字符匹配但不足以确认
        0.0: 完全不在最终文本
    """
    if not word or not full_text:
        return 0.0

    word_lower = word.lower()

    # 精确匹配
    if word in full_text or word_lower in full_text.lower():
        return 1.0

    # 中文词：用字符重叠度
    if any('\u4e00' <= c <= '\u9fff' for c in word):
        common = sum(1 for c in word if c in full_text)
        overlap = common / max(len(word), 1)
        if overlap >= 0.8:
            return 0.7
        elif overlap >= 0.5:
            return 0.5
        elif overlap >= 0.3:
            return 0.3
        return 0.1

    # 英文词：用字母重叠度
    alpha_chars = re.findall(r'[a-zA-Z]', word)
    if alpha_chars:
        common = sum(1 for c in alpha_chars if c.lower() in full_text.lower())
        overlap = common / max(len(alpha_chars), 1)
        if overlap >= 0.8:
            return 0.7
        elif overlap >= 0.5:
            return 0.5
        return 0.2

    # 混合/其它：保守 0.0
    return 0.0


# ═══════════════════════════════════════════════════════════════
# 源2: 字幕/OCR 交叉证据得分 (50%)
# ═══════════════════════════════════════════════════════════════
# 三个子来源：
#   a) B站官方字幕中存在 → 高置信
#   b) OCR 累积文字中出现 → 中高置信
#   c) 字幕分段中有近似匹配 → 中置信
# 综合为外部证据得分。
# ═══════════════════════════════════════════════════════════════

def _cross_evidence_score(
    word: str,
    subtitle_text: str,
    subtitle_segments: Optional[List[Dict]],
    ocr_persistent: str,
) -> float:
    """字幕/OCR 交叉证据得分 (0~1)
    
    外部来源对词是否存在的客观证据。
    得分越高 = 外部确认词存在 → 原转录可能没错，P2 可能误报。
    
    Returns:
        1.0: 词在字幕或 OCR 中确认
        0.7: 词在字幕分段中有近似匹配
        0.5: OCR 中有部分匹配
        0.2: 仅有微弱痕迹
        0.0: 完全无外部证据
    """
    if not word:
        return 0.0

    word_lower = word.lower()
    scores = []

    # a) 字幕全文精确匹配
    if subtitle_text:
        if word in subtitle_text or word_lower in subtitle_text.lower():
            scores.append(1.0)

    # b) 字幕分段检查
    if subtitle_segments:
        for seg in subtitle_segments:
            seg_text = seg.get("text", "") if isinstance(seg, dict) else ""
            if not seg_text:
                continue
            # 精确匹配
            if word in seg_text or word_lower in seg_text.lower():
                scores.append(1.0)
                break
            # 近似匹配（编辑距离 < 2）
            elif _levenshtein_distance(word, seg_text) <= 2:
                scores.append(0.7)
            # 字符重叠 > 60%
            elif _char_overlap(word, seg_text) >= 0.6:
                scores.append(0.5)

    # c) OCR 持久文本
    if ocr_persistent:
        if word in ocr_persistent or word_lower in ocr_persistent.lower():
            scores.append(1.0)
        elif any('\u4e00' <= c <= '\u9fff' for c in word):
            # 中文 OCR 字符级重叠
            overlap = sum(1 for c in word if c in ocr_persistent) / max(len(word), 1)
            if overlap >= 0.8:
                scores.append(0.7)
            elif overlap >= 0.5:
                scores.append(0.5)

    if not scores:
        return 0.0

    # 取最高得分（一个来源确认就足够）
    return max(scores)


# ═══════════════════════════════════════════════════════════════
# 源3: 说话人知识得分 (25%)
# ═══════════════════════════════════════════════════════════════
# 校验犹豫词是否在 UP主 的历史用语中出现。
# 如果词在说话人的历史语料中出现过 → 词可能是对的
# 如果完全没见过 → 可能是 whisper 幻觉
# ═══════════════════════════════════════════════════════════════

def _speaker_knowledge_score(word: str, speaker_profile: Optional[Dict]) -> float:
    """说话人知识得分 (0~1)
    
    speaker_profile 内容示例:
    {
        "frequent_terms": ["Transformer", "LoRA", ...],
        "domain": "AI",
        "vocab": {"专有名词": [...], "常见搭配": [...]},
        ...
    }
    
    如果 profile 不存在 → 中性 0.5（无法判断）
    如果 profile 存在但无匹配 → 得分低
    """
    if not speaker_profile:
        return 0.5  # 无说话人知识，中性

    word_lower = word.lower()
    sources_checked = 0
    matches = 0

    # 检查 frequent_terms
    freq_terms = speaker_profile.get("frequent_terms", [])
    if freq_terms:
        sources_checked += 1
        if any(word_lower == t.lower() for t in freq_terms):
            matches += 1
        # 部分匹配
        elif any(word_lower in t.lower() or t.lower() in word_lower for t in freq_terms):
            matches += 0.5

    # 检查 vocab 字典
    vocab = speaker_profile.get("vocab", {})
    if vocab:
        sources_checked += 1
        for category, terms in vocab.items():
            if isinstance(terms, list):
                if any(word_lower == t.lower() for t in terms):
                    matches += 1
                    break
                elif any(word_lower in t.lower() or t.lower() in word_lower for t in terms):
                    matches += 0.5
                    break

    # 检查 domain（领域匹配提供微弱的正面信号）
    domain = speaker_profile.get("domain", "")
    word_domain_hint = speaker_profile.get("domain_hint", "")
    if domain:
        sources_checked += 0.5  # domain 证据强度弱于具体词
        if word_lower in domain.lower():
            matches += 0.3

    if sources_checked == 0:
        return 0.5  # 无可用知识源，中性

    score = matches / sources_checked
    return max(0.0, min(1.0, score))


# ═══════════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════════

def _levenshtein_distance(s1: str, s2: str) -> int:
    """计算两个字符串的编辑距离"""
    if not s1 or not s2:
        return max(len(s1), len(s2))
    m, n = len(s1), len(s2)
    if m > n:
        s1, s2 = s2, s1
        m, n = n, m
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
        prev, curr = curr, prev
    return prev[n]


def _char_overlap(word: str, text: str) -> float:
    """计算词和文本的字符重叠比例 (0~1)"""
    if not word or not text:
        return 0.0
    common = sum(1 for c in word if c in text)
    return common / max(len(word), 1)


def _generate_details(
    word_breakdown: List[Dict],
    whisper_score: float,
    cross_score: float,
    speaker_score: float,
    confidence: float,
    severity: float,
    recommendation: str,
) -> str:
    """生成人类可读的决策理由"""
    rec_label = {
        "honor": "✅ 验证通过，继续P2升级",
        "downgrade": "⚠️ 部分验证通过，降级P2严重度",
        "override": "❌ 三源未验证，覆盖P2，容忍",
    }
    parts = [
        f"三源验证({recommendation}):",
        f"  综合置信度={confidence:.2f}, 严重度={severity:.1f}",
        f"  源1-Whisper={whisper_score:.2f} 源2-交叉={cross_score:.2f} 源3-说话人={speaker_score:.2f}",
        f"  {rec_label[recommendation]}",
        f"  词级明细:",
    ]
    for b in word_breakdown:
        parts.append(
            f"    '{b['word']}': "
            f"whisper={b['whisper_conf']:.2f} "
            f"cross={b['cross_evidence']:.2f} "
            f"speaker={b['speaker_known']:.2f} "
            f"→ combined={b['combined']:.2f}"
        )
    return "\n".join(parts)
