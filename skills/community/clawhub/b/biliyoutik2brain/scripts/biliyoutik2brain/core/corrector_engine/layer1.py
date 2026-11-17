"""
BiliYouTik2Brain — Corrector Engine L1: 源交叉验证

成本≈0，不调LLM。
检查:
  1. B站官方字幕 → 交叉验证低置信词（正面确认 + 反面语义匹配）
  2. BLEEP/消音标记检测
  3. Bleep感知音频检测结果交叉验证
  4. Phase 2.1: n-gram 向量反面验证 — 对修正候选做语境连贯性检查

代码做确定的事：字典匹配 + 模式匹配 + 编辑距离 + n-gram统计。
不下LLM结论，只做确定性计算。
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from ..corrector_dictionary import check_bleep
from .exit import HARD_THRESHOLD


# ═══════════════════════════════════════════════════════════════
# 编辑距离（Levenshtein Distance）
# ═══════════════════════════════════════════════════════════════

def _levenshtein_distance(s1: str, s2: str) -> int:
    """计算两个字符串的编辑距离（增、删、改各算1步）"""
    if not s1 or not s2:
        return max(len(s1), len(s2))
    
    # 使用2行滚动数组减少内存
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
            curr[j] = min(
                prev[j] + 1,          # 删除
                curr[j - 1] + 1,      # 插入
                prev[j - 1] + cost,   # 替换
            )
        prev, curr = curr, prev
    
    return prev[n]


def _normalized_similarity(s1: str, s2: str) -> float:
    """计算归一化语义相似度 (0~1)，1为完全相同"""
    if not s1 or not s2:
        return 0.0
    dist = _levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    return 1.0 - (dist / max_len)


# ═══════════════════════════════════════════════════════════════
# Phase 2.1: n-gram 向量反面验证（穷人版语义检查）
# ═══════════════════════════════════════════════════════════════
# 不使用 sentence_transformers / sklearn 等重型依赖。
# 用字符 n-gram 词袋向量 + numpy 余弦相似度实现"语境连贯性检查"。
# 
# 核心思路：
#   修正后的句子在 n-gram 空间中应与原始句子保持"合理相似"。
#   如果修正后 n-gram 分布剧烈变化，说明修正可能离谱。
#   这不是"语义理解"，而是"分布异常检测"。
# ═══════════════════════════════════════════════════════════════

def _char_ngrams(text: str, n: int = 2) -> List[str]:
    """提取字符 n-gram"""
    if not text or len(text) < n:
        return [text]
    return [text[i:i+n] for i in range(len(text) - n + 1)]


def _build_ngram_vector(
    text: str,
    vocab: Dict[str, int],
    n_values: Tuple[int, ...] = (2, 3),
) -> np.ndarray:
    """将文本转为 n-gram 频率向量
    
    对每个 n 值做 n-gram 分解，按 vocab 映射为固定维度频率向量。
    """
    vec = np.zeros(len(vocab), dtype=np.float32)
    for n in n_values:
        for ng in _char_ngrams(text, n):
            idx = vocab.get(ng)
            if idx is not None:
                vec[idx] += 1.0
    # L2 归一化（避免文本长度影响）
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


def _build_ngram_vocab(texts: List[str], n_values: Tuple[int, ...] = (2, 3)) -> Dict[str, int]:
    """从多个文本中提取 n-gram 词汇表"""
    vocab = {}
    for text in texts:
        for n in n_values:
            for ng in _char_ngrams(text, n):
                if ng not in vocab:
                    vocab[ng] = len(vocab)
    return vocab


def _cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """纯 numpy 余弦相似度"""
    dot = float(np.dot(v1, v2))
    n1 = float(np.linalg.norm(v1))
    n2 = float(np.linalg.norm(v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


def semantic_reverse_check(
    original_sentence: str,
    corrected_sentence: str,
    original_word: str,
    corrected_word: str,
    threshold: float = 0.75,
) -> Optional[Dict]:
    """n-gram 反面验证：修正是否保持了语境连贯性
    
    把 original_sentence 中的 original_word 替换为 corrected_word，
    比较替换前后两句的 n-gram 向量余弦相似度。
    
    如果替换后的句子与原始句子过于不相似（cos < threshold），
    说明修正可能破坏了语境 → 降低 confidence 或标记为可疑。
    
    Args:
        original_sentence: 修正前的完整句子
        corrected_sentence: 整体修正后的句子（含其他修正）
        original_word: 原低置信词
        corrected_word: 候选修正词
        threshold: 相似度阈值（低于此值扣分）
    
    Returns:
        None（通过验证）或 dict（未通过，含详细指标）
    """
    if not original_word or not corrected_word:
        return None
    
    # 构造"仅替换目标词"的句子
    replaced = original_sentence.replace(original_word, corrected_word, 1)
    
    # 如果被替换词在句子中找不到，回退到逐个字符检查
    if replaced == original_sentence and original_word not in original_sentence:
        return None
    
    # 从两句中共建 n-gram 词汇表
    vocab = _build_ngram_vocab([original_sentence, replaced, corrected_sentence])
    if len(vocab) < 3:
        return None  # 文本太短，无法做向量分析
    
    # 计算三组向量
    v_orig = _build_ngram_vector(original_sentence, vocab)
    v_repl = _build_ngram_vector(replaced, vocab)
    v_corr = _build_ngram_vector(corrected_sentence, vocab)
    
    # 相似度比较
    # sim_repl: 原始 vs 仅替换目标词 — 反映词替换的"冲击"
    # sim_corr: 原始 vs 整体修正 — 反映全句修正后整体偏移
    sim_repl = _cosine_similarity(v_orig, v_repl)
    sim_corr = _cosine_similarity(v_orig, v_corr)
    
    if sim_repl >= threshold:
        # 替换前后 n-gram 分布稳定 → 修正合理
        return None
    
    # 分布剧烈变化 → 修正可疑
    return {
        "original_word": original_word,
        "corrected_word": corrected_word,
        "ngram_similarity": round(float(sim_repl), 4),
        "full_sentence_similarity": round(float(sim_corr), 4),
        "threshold": threshold,
        "violation": "替换后n-gram分布偏移过大，修正可能破坏语境",
    }


def batch_semantic_reverse_check(
    candidates: List[Dict],
    full_text: str,
    threshold: float = 0.75,
) -> List[Dict]:
    """批量执行 n-gram 反面验证
    
    对候选列表中的每条修正做语义连贯性检查。
    未通过的候选 confidence 乘以 penalty_factor。
    
    Returns:
        修正后的候选列表（confidence 可能已降低）
    """
    for c in candidates:
        result = semantic_reverse_check(
            original_sentence=full_text,
            corrected_sentence=full_text,  # 如果没有完整的修正版本，用原文本
            original_word=c.get("original", ""),
            corrected_word=c.get("corrected", ""),
            threshold=threshold,
        )
        if result:
            # n-gram 验证未通过 → 降低 confidence
            c["confidence"] = c.get("confidence", 0.5) * 0.6  # 打六折
            c["ngram_warning"] = result["violation"]
            c["ngram_similarity"] = result["ngram_similarity"]
    
    return candidates


def level1_cross_validate(
    low_conf_words: List[Tuple[str, float]],
    full_text: str,
    bvid: str = "",
    bleep_text: str = "",
    subtitle_segments: Optional[List[Dict]] = None,
) -> List[dict]:
    """L1: 源交叉验证 — 不调LLM，纯确定性匹配
    
    输入:
        low_conf_words: [(word, confidence), ...]
        full_text: 全量转录文本
        subtitle_segments: 官方字幕分段 [{text: str, ...}]
        bleep_text: BLEEP检测结果文本
    
    返回:
        [{"original": str, "corrected": str, "source": "L1_cross_validate",
          "confidence": float, "evidence": str, "context_snippet": str}, ...]
    """
    candidates = []
    
    if not low_conf_words:
        return candidates
    
    subtitle_texts = set()
    if subtitle_segments:
        for seg in subtitle_segments:
            if isinstance(seg, dict):
                t = seg.get("text", "").strip()
                if t:
                    subtitle_texts.add(t)
    
    # ── 步骤1: BLEEP检测 ──
    for w, c in low_conf_words:
        bleep_result = check_bleep(w)
        if bleep_result:
            corrected, conf, evidence = bleep_result
            context_snippet = _get_context_snippet(full_text, w)
            candidates.append({
                "original": w,
                "corrected": corrected,
                "source": "L1_cross_validate",
                "confidence": conf,
                "evidence": evidence,
                "context_snippet": context_snippet,
            })
    
    # ── 步骤2: 字幕交叉验证（正面） ──
    if subtitle_texts:
        for sub_text in subtitle_texts:
            for w, c in low_conf_words:
                if candidates_already(candidates, w):
                    continue
                if w in sub_text or _overlap_score(w, sub_text) > 0.7:
                    context_snippet = _get_context_snippet(full_text, w)
                    candidates.append({
                        "original": w,
                        "corrected": w,  # 字幕确认原始词是对的
                        "source": "L1_cross_validate",
                        "confidence": 0.95,
                        "evidence": f"字幕确认: '{w}' 在官方字幕中",
                        "context_snippet": context_snippet,
                    })
    
    # ── 步骤3（新增）: 字幕语义匹配（反面） ──
    # 对未在"正面"匹配到的词，检查与字幕文字的语义相似度
    # 如果高度相似但字形不同 → 标记为"需人工确认"
    # 不自动修正，只标记
    if subtitle_texts:
        for w, c in low_conf_words:
            if candidates_already(candidates, w):
                continue
            
            best_similarity = 0.0
            best_match = ""
            for sub_text in subtitle_texts:
                sim = _normalized_similarity(w, sub_text)
                if sim > best_similarity:
                    best_similarity = sim
                    best_match = sub_text
                # 也检查字幕中的单个词
                for sub_word in sub_text.split():
                    sub_word = sub_word.strip("，。！？、；：""''（）【】《》")
                    if sub_word and len(sub_word) >= 2:
                        sim = _normalized_similarity(w, sub_word)
                        if sim > best_similarity:
                            best_similarity = sim
                            best_match = sub_word
            
            # 高度相似但不同形 → 提示但不自动修正
            if 0.7 <= best_similarity < 1.0 and best_match != w:
                context_snippet = _get_context_snippet(full_text, w)
                candidates.append({
                    "original": w,
                    "corrected": w,  # 不自动修正，只标记为低置信
                    "source": "L1_cross_validate",
                    "confidence": 0.6,  # 需人工确认
                    "evidence": f"字幕语义提示: '{w}' 可能与 '{best_match}' 相关 (相似度={best_similarity:.2f})",
                    "context_snippet": context_snippet,
                })
            elif best_similarity < 0.3:
                # 完全不在字幕中且无语义等价 → 保持原置信度
                # 仅做记录，不加候选（让后续层处理）
                pass
    
    # ── 步骤4: BLEEP感知音频检测结果交叉验证 ──
    if bleep_text:
        for w, c in low_conf_words:
            if candidates_already(candidates, w):
                continue
            if w in bleep_text or any(marker in w for marker in ["[消音]", "[BLEEP]"]):
                context_snippet = _get_context_snippet(full_text, w)
                candidates.append({
                    "original": w,
                    "corrected": "[消音]",
                    "source": "L1_cross_validate",
                    "confidence": 0.9,
                    "evidence": f"BLEEP感知检测确认: '{w}' 对应音频消音段",
                    "context_snippet": context_snippet,
                })
    
    # ── Phase 2.1: n-gram 向量反面验证 ──
    # 对已有候选做语境连贯性检查，标记"修正正确但语境荒谬"的情形
    candidates = batch_semantic_reverse_check(candidates, full_text)
    
    return candidates


def candidates_already(candidates: List[dict], word: str) -> bool:
    """检查某个词是否已被候选列表覆盖"""
    return any(c.get("original") == word for c in candidates)


def _overlap_score(word: str, subtitle: str) -> float:
    """计算词和字幕片段的重叠度"""
    if not word or not subtitle:
        return 0.0
    # 简单字符重叠
    common = sum(1 for c in word if c in subtitle)
    return common / max(len(word), 1)


def _get_context_snippet(full_text: str, word: str, window_sentences: int = 2) -> str:
    """获取词在全文中的上下文片段"""
    if not full_text or not word:
        return ""
    
    pos = full_text.find(word)
    if pos < 0:
        return ""
    
    # 向前找句子边界
    start = pos
    sentence_boundaries = ["。", "！", "？", "\n"]
    for _ in range(window_sentences):
        prev = max(full_text.rfind(b, 0, start) for b in sentence_boundaries)
        if prev >= 0:
            start = prev + 1
        else:
            start = 0
            break
    
    # 向后找句子边界
    end = pos + len(word)
    for _ in range(window_sentences):
        next_pos = min(
            (full_text.find(b, end) for b in sentence_boundaries),
            default=-1
        )
        if next_pos >= 0:
            end = next_pos + 1
        else:
            end = len(full_text)
            break
    
    return full_text[start:end].strip()[:200]
