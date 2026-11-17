"""
BiliYouTik2Brain — Corrector Engine L2: LLM局部修复 + L2.5句级上下文

L2: 批量LLM调用（v3改造：从逐词调LLM改为1次批量调用）
L2.5: 扩大上下文到整句，更多token

改造宗旨：
  1. 先查确定性词典（代码做确定的事）
  2. 剩余打包为1次LLM调用（提示词做不确定的事）
  3. 批量失败才逐词兜底

职责单一: 生成修正候选列表，不做置信度过滤/退出判断（在exit.py）。
"""

from typing import List, Tuple, Optional, Dict
from .utils import call_llm, extract_json, safe_float
from ..corrector_dictionary import DOMAIN_CORRECTIONS


def level2_llm_local_repair(
    low_conf_words: List[Tuple[str, float]],
    full_text: str,
    bvid: str = "",
    bleep_text: str = "",
    ocr_text: str = "",
    max_words: int = 50,
) -> List[dict]:
    """L2: LLM局部修复 — 批量版（v3改造）
    
    v3 核心改动：从逐词独立调LLM → 确定性查表 + 批量LLM。
    
    流程：
      1. 先过 DOMAIN_CORRECTIONS（代码确定的事）
      2. 剩余打包为1次批量LLM调用（提示词做不确定的事）
      3. 批量失败降级为逐词兜底
    
    Args:
        low_conf_words: [(word, confidence), ...]
        full_text: 全量转录文本
        bvid: 视频ID
        bleep_text: BLEEP检测文本
        ocr_text: OCR帧文本（可选）
        max_words: 单次最多处理的词数
    
    Returns:
        [{"original", "corrected", "source", "confidence", "evidence", "context_snippet"}, ...]
    """
    if not low_conf_words:
        return []
    
    candidates = []
    words_to_check = low_conf_words[:max_words]
    
    # ── Phase A: 确定性词典查找（代码做确定的事）──
    # 0 LLM调用，纯查表
    llm_pending = []  # [(word, confidence), ...]
    
    for w, c in words_to_check:
        if c >= 0.9:
            continue  # 已经足够高置信
        
        domain_match = DOMAIN_CORRECTIONS.get(w)
        if domain_match:
            ctx = _get_context_snippet(full_text, w)
            candidates.append({
                "original": w,
                "corrected": domain_match,
                "source": "L2_llm_local",
                "confidence": 0.9,
                "evidence": "确定性词典匹配",
                "context_snippet": ctx,
            })
        else:
            llm_pending.append((w, c))
    
    # ── Phase B: 批量LLM调用（提示词做不确定的事）──
    # 所有未命中确定性查表的词，打包为1次API调用
    if llm_pending:
        try:
            batch_candidates = _llm_batch_fix(
                llm_pending, full_text,
                bleep_text=bleep_text, ocr_text=ocr_text, bvid=bvid,
            )
            candidates.extend(batch_candidates)
        except Exception as e:
            print(f"  [L2] 批量LLM异常: {e}, 降级为逐词兜底")
            fallback = _llm_individual_fallback(
                llm_pending, full_text,
                bleep_text, ocr_text, bvid
            )
            candidates.extend(fallback)
    
    return candidates


def level2_5_sentence_context(
    low_conf_words: List[Tuple[str, float]],
    full_text: str,
    bvid: str = "",
) -> List[dict]:
    """L2.5: 句级上下文修复（批量版）
    
    对L2未解决的低置信词，用完整句子+前后句做LLM修复。
    把所有待修复的词打包为一次LLM调用，避免逐个调用的超时浪费。
    
    Args:
        low_conf_words: [(word, confidence), ...]
        full_text: 全量转录文本
        bvid: 视频ID
    
    Returns:
        修正候选列表
    """
    if not low_conf_words:
        return []
    
    # 只处理置信度<0.7的词（L2没解决的）
    pending = [(w, c) for w, c in low_conf_words if c < 0.7 and _get_sentence_context(full_text, w)]
    if not pending:
        return []
    
    # 批量构建：把所有待修复词的上下文打包为一次调用
    word_details = []
    for w, c in pending:
        ctx = _get_sentence_context(full_text, w)
        word_details.append(f"词: \"{w}\" (置信度={c:.3f})\n  上下文: {ctx}")
    
    batch_prompt = "请检查以下各低置信词在对应句子上下文中是否需要修正。逐条判断：\n\n" + \
                   "\n---\n".join(word_details) + \
                   "\n\n输出JSON格式: {\"corrections\": [{\"original\": \"原始词\", \"corrected\": \"修正后\", \"confidence\": 0.95, \"evidence\": \"原因\"}]}\n" + \
                   "如果某个词不需要修正, 不放入列表。confidence低于0.6不应用。"
    
    messages = [
        {
            "role": "system",
            "content": "你是一个专业的转录文本修正助手。根据句子上下文判断是否有需要修正的语音识别错误。"
        },
        {"role": "user", "content": batch_prompt}
    ]
    
    response = call_llm(messages, timeout=120)
    if not response:
        return []
    
    parsed = extract_json(response)
    if not parsed or "corrections" not in parsed:
        return []
    
    candidates = []
    for corr in parsed["corrections"]:
        orig = corr.get("original", "")
        if any(orig == w for w, _ in pending):
            ctx = _get_sentence_context(full_text, orig)
            candidates.append({
                "original": orig,
                "corrected": corr.get("corrected", orig),
                "source": "L2_5_sentence_ctx",
                "confidence": safe_float(corr.get("confidence", 0.7)),
                "evidence": corr.get("evidence", ""),
                "context_snippet": ctx[:200],
            })
    
    return candidates


# ═══════════════════════════════════════════════════════════════
# 批量LLM修复（核心新函数）
# ═══════════════════════════════════════════════════════════════

def _llm_batch_fix(
    pending_words: List[Tuple[str, float]],
    full_text: str,
    bleep_text: str = "",
    ocr_text: str = "",
    bvid: str = "",
) -> List[dict]:
    """批量LLM修复：所有待修复词打包为1次调用
    
    Args:
        pending_words: [(word, confidence), ...] — 已排除确定性匹配的词
        full_text: 全量转录文本
        bleep_text: BLEEP检测文本
        ocr_text: OCR帧文本
        bvid: 视频ID
    
    Returns:
        修正候选列表
    """
    if not pending_words:
        return []
    
    # 过滤掉无上下文的词
    word_details = []
    for w, c in pending_words:
        ctx = _get_context_snippet(full_text, w)
        if not ctx:
            continue
        word_details.append(f"词: \"{w}\" (置信度={c:.3f})\n  上下文: {ctx}")
    
    if not word_details:
        return []
    
    batch_prompt = (
        "请检查以下各低置信词在对应局部上下文中是否需要修正。逐条判断：\n\n"
        + "\n---\n".join(word_details)
        + "\n\n输出JSON格式: {\"corrections\": [{\"original\": \"原始词\", \"corrected\": \"修正后\", "
        "\"confidence\": 0.95, \"evidence\": \"原因说明\"}]}\n"
        + "如果某个词不需要修正, 不放入列表。confidence低于0.6不应用。"
    )
    
    # 补充OCR/BLEEP上下文
    extra_parts = []
    if ocr_text:
        extra_parts.append(f"OCR帧文字: {ocr_text[:300]}")
    if bleep_text:
        extra_parts.append(f"BLEEP检测: {bleep_text[:300]}")
    if extra_parts:
        batch_prompt += "\n\n额外参考信息:\n" + "\n".join(extra_parts)
    
    messages = [
        {
            "role": "system",
            "content": "你是一个专业的转录文本修正助手。根据局部上下文判断是否有需要修正的语音识别错误。"
        },
        {"role": "user", "content": batch_prompt}
    ]
    
    response = call_llm(messages, timeout=120)
    if not response:
        # 批量失败 → 降级为逐词兜底
        print("  [L2] 批量LLM失败, 降级为逐词兜底")
        return _llm_individual_fallback(pending_words, full_text, bleep_text, ocr_text, bvid)
    
    parsed = extract_json(response)
    if not parsed or "corrections" not in parsed:
        print("  [L2] 批量LLM返回格式异常, 降级为逐词兜底")
        return _llm_individual_fallback(pending_words, full_text, bleep_text, ocr_text, bvid)
    
    candidates = []
    pending_set = {w for w, _ in pending_words}
    for corr in parsed["corrections"]:
        orig = corr.get("original", "")
        if orig in pending_set:
            ctx = _get_context_snippet(full_text, orig)
            candidates.append({
                "original": orig,
                "corrected": corr.get("corrected", orig),
                "source": "L2_llm_local",
                "confidence": safe_float(corr.get("confidence", 0.7)),
                "evidence": corr.get("evidence", ""),
                "context_snippet": ctx[:200],
            })
    
    return candidates


def _llm_individual_fallback(
    pending_words: List[Tuple[str, float]],
    full_text: str,
    bleep_text: str = "",
    ocr_text: str = "",
    bvid: str = "",
) -> List[dict]:
    """逐词兜底：批量调用失败时逐个尝试
    
    仅当批量LLM失败时才降级到此函数。
    """
    candidates = []
    for w, c in pending_words:
        try:
            if c >= 0.9:
                continue
            ctx = _get_context_snippet(full_text, w)
            if not ctx:
                continue
            correction = _llm_fix_one_word(w, ctx, bleep_text, ocr_text, bvid)
            if correction:
                candidates.append(correction)
        except Exception as e:
            print(f"    [L2兜底] '{w}' 异常: {e}, 跳过")
            continue
    return candidates


# ═══════════════════════════════════════════════════════════════
# 上下文提取工具
# ═══════════════════════════════════════════════════════════════

def _get_context_snippet(full_text: str, word: str, window_chars: int = 50) -> str:
    """取词前后各window_chars字作为上下文"""
    if not full_text or not word:
        return ""
    pos = full_text.find(word)
    if pos < 0:
        return ""
    start = max(0, pos - window_chars)
    end = min(len(full_text), pos + len(word) + window_chars)
    snippet = full_text[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(full_text):
        snippet = snippet + "..."
    return snippet.strip()


def _get_sentence_context(full_text: str, word: str) -> str:
    """取词所在的完整句子+前后各一句"""
    if not full_text or not word:
        return ""
    pos = full_text.find(word)
    if pos < 0:
        return ""
    
    # 向前找句子边界
    start = 0
    for sep in ["\n\n", "。", "！", "？", "；"]:
        p = full_text.rfind(sep, 0, pos)
        if p >= 0:
            start = max(start, p + len(sep))
    
    # 向后找句子边界
    end = len(full_text)
    for sep in ["\n\n", "。", "！", "？", "；"]:
        p = full_text.find(sep, pos + len(word))
        if 0 <= p < end:
            end = p + len(sep)
    
    return full_text[start:end].strip()


# ═══════════════════════════════════════════════════════════════
# 逐词LLM修复（保留为兜底函数）
# ═══════════════════════════════════════════════════════════════

def _llm_fix_one_word(word: str, context: str, bleep_text: str, ocr_text: str, bvid: str) -> Optional[dict]:
    """用LLM修复一个词（兜底用，仅当批量LLM失败时调用）"""
    messages = [
        {
            "role": "system",
            "content": "你是专业转录文本修正助手。修正语音识别错误，返回JSON。\n\n"
                       "输出格式: {\"original\": \"原始词\", \"corrected\": \"修正后词\", "
                       "\"confidence\": 0.95, \"evidence\": \"原因说明\"}\n"
                       "confidence: 0~1浮点数。低于0.6不应用。\n"
                       "如果不确定, 返回confidence=0.0。"
        },
        {
            "role": "user",
            "content": f"上下文: {context}\n低置信词: {word}\n修正:"
        }
    ]
    
    # 如果有OCR或BLEEP上下文, 加入
    if ocr_text and word in ocr_text:
        messages[1]["content"] += f"\n\nOCR帧文字提示: '{word}' 出现在视频画面文字中, 可能是专有名词"
    
    response = call_llm(messages, timeout=120)
    if not response:
        return None
    
    parsed = extract_json(response)
    if not parsed:
        return None
    
    if parsed.get("corrected") and parsed.get("corrected") != word:
        return {
            "original": word,
            "corrected": parsed["corrected"],
            "source": "L2_llm_local",
            "confidence": safe_float(parsed.get("confidence", 0.5)),
            "evidence": parsed.get("evidence", ""),
            "context_snippet": context[:200],
        }
    
    return None
