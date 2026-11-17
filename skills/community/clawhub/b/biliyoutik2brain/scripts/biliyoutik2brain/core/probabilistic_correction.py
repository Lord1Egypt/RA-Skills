"""
BiliYouTik2Brain — 词级概率性修正 (Phase 4.2)

专有名词整块糊了的场景（如"MACD金叉"→"马可迪金叉"），
用概率+依据选择最佳候选，每个修正标注来源，不靠LLM凭空猜。

设计原则：
  1. 每个修正必须有来源追溯
  2. 多个候选时投票决定，而不是选最像的
  3. 低置信度修正标记为"存疑"，不下最终结论

数据流：
  Whisper原始文本 → 候选生成（多源） → 权重投票 → 结果排序 → 交付修正

候选来源：
  A: 说话人知识库 (known_mistakes)
  B: 模糊音混淆矩阵 (fuzzy_confusion)
  C: 官方字幕交叉验证  
  D: OCR画面文字交叉验证
  E: 通用纠错词典 (corrector_dictionary)
  F: 确定性规则（同音/形近字）

投票权重：
  - 确定性来源 (E/F): 权重 1.0 → 直接采用
  - 高度可信 (A/B 置信度≥0.7): 权重 0.8
  - 中等可信 (C/D 匹配): 权重 0.6
  - 低可信 (A/B 置信度<0.7): 权重 0.3
"""

import os, re, json, math
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


# 权重定义
SOURCE_WEIGHTS = {
    "dict_exact": 1.0,          # 纠错词典精确匹配
    "rule_deterministic": 1.0,   # 确定性规则（同音/形近字）
    "speaker_mistake_high": 0.8, # 说话人误认高频
    "fuzzy_confusion_high": 0.8, # 混淆矩阵高置信
    "subtitle_match": 0.6,       # 字幕交叉验证
    "ocr_match": 0.6,            # OCR交叉验证
    "speaker_mistake_low": 0.3,  # 说话人误认低频
    "fuzzy_confusion_low": 0.3,  # 混淆矩阵低置信
    "llm_hint": 0.2,             # LLM提示（仅供参考）
}


# ═══════════════════════════════════════════════════════════════
# 1. 候选生成
# ═══════════════════════════════════════════════════════════════

def _generate_candidates_from_speaker(
    word: str,
    speaker_profile: Dict,
) -> List[Dict]:
    """从说话人知识库生成修正候选"""
    candidates = []
    known_mistakes = speaker_profile.get("known_mistakes", {})
    
    if word in known_mistakes:
        candidates.append({
            "text": known_mistakes[word],
            "source": "speaker_mistake_high",
            "source_label": f"说话人字典：{word}→{known_mistakes[word]}",
            "confidence": 0.85,
        })
    
    # 模糊匹配：如果完整词不在，但部分匹配
    for wrong, right in known_mistakes.items():
        if wrong in word and len(wrong) >= 2:
            # 替换匹配的部分
            replaced = word.replace(wrong, right, 1)
            if replaced != word:
                candidates.append({
                    "text": replaced,
                    "source": "speaker_mistake_high",
                    "source_label": f"说话人字典部分匹配：{wrong}→{right}",
                    "confidence": 0.65,
                })
    
    return candidates


def _generate_candidates_from_subtitle(
    word: str,
    subtitle_text: str,
    segments: List[Dict],
) -> List[Dict]:
    """从官方字幕生成修正候选"""
    if not subtitle_text and not segments:
        return []
    
    candidates = []
    
    # 在字幕中搜索相似词
    search_text = subtitle_text.lower() if subtitle_text else ""
    
    # 构建 n-gram 候选（从字幕中提取长度相近的词）
    for length in [len(word) - 1, len(word), len(word) + 1]:
        if length <= 0:
            continue
        if search_text:
            # 查找包含 word 部分字符的字幕段
            for s in re.findall(r'[\u4e00-\u9fff\w]{' + str(length) + '}', search_text):
                # Jaccard 相似度
                set1, set2 = set(word), set(s)
                overlap = len(set1 & set2)
                union = len(set1 | set2)
                if union > 0 and overlap / union > 0.5:
                    candidates.append({
                        "text": s,
                        "source": "subtitle_match",
                        "source_label": f"字幕匹配: {s} (Jaccard={overlap/union:.2f})",
                        "confidence": round(0.4 + 0.3 * (overlap / union), 2),
                    })
                    break  # 每个长度取第一个匹配
    
    return candidates


def _generate_candidates_from_ocr(
    word: str,
    ocr_persistent: str,
) -> List[Dict]:
    """从OCR画面文字生成修正候选"""
    if not ocr_persistent:
        return []
    
    candidates = []
    
    # 在OCR持久文字中搜索包含目标词部分字符的连续文本
    lines = ocr_persistent.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检查是否有字符重叠
        set1 = set(word)
        set2 = set(line)
        overlap = len(set1 & set2)
        union = len(set1 | set2) or 1
        ratio = overlap / union
        
        if ratio > 0.4 and abs(len(line) - len(word)) <= 3:
            candidates.append({
                "text": line,
                "source": "ocr_match",
                "source_label": f"OCR匹配: {line}",
                "confidence": round(0.35 + 0.3 * ratio, 2),
            })
    
    return candidates


def _generate_candidates_from_fuzzy(
    word: str,
    domain: str,
) -> List[Dict]:
    """从模糊音混淆矩阵生成候选"""
    try:
        from .fuzzy_confusion import get_fuzzy_corrections
        corrections = get_fuzzy_corrections(word, domain=domain)
        candidates = []
        for c in corrections:
            for cand in c.get("candidates", []):
                cand["source"] = cand.get("source", "fuzzy_confusion_high")
                # 映射到统一的 source key
                if cand.get("confidence", 0) >= 0.7:
                    cand["source"] = "fuzzy_confusion_high"
                else:
                    cand["source"] = "fuzzy_confusion_low"
                candidates.append(cand)
        return candidates
    except Exception:
        return []


def _generate_candidates_from_dict(word: str) -> List[Dict]:
    """从通用纠错词典生成候选"""
    from .corrector_dictionary import fast_domain_correct
    try:
        corrected = fast_domain_correct(word)
        if corrected and corrected != word:
            return [{
                "text": corrected,
                "source": "dict_exact",
                "source_label": f"词典修正: {word}→{corrected}",
                "confidence": 0.95,
            }]
    except Exception:
        pass
    return []


def _generate_candidates_from_rules(word: str) -> List[Dict]:
    """从确定性规则生成候选（同音/形近字）"""
    candidates = []
    
    # 常见同音字映射
    HOMOPHONE_MAP = {
        "马可迪": "MACD",
        "金叉": "金叉",  # 这个通常不会错
        "死叉": "死叉",
        "缠论": "缠论",
        "止损": "止损",
        "止赢": "止盈",
        "做多": "做多",
        "做空": "做空",
        "阳线": "阳线",
        "阴线": "阴线",
    }
    
    for wrong, right in HOMOPHONE_MAP.items():
        if wrong in word and wrong != right:
            candidates.append({
                "text": word.replace(wrong, right, 1),
                "source": "rule_deterministic",
                "source_label": f"确定性规则: {wrong}→{right}",
                "confidence": 0.9,
            })
    
    return candidates


# ═══════════════════════════════════════════════════════════════
# 2. 投票引擎
# ═══════════════════════════════════════════════════════════════

def _compute_weighted_score(candidates: List[Dict]) -> Dict[str, float]:
    """对候选进行加权投票
    
    流程：
    1. 按 text 内容分组（去重）
    2. 加权求和：每个候选的权重 = SOURCE_WEIGHTS[source] * confidence
    3. 排序
    
    Returns:
        {text: weighted_score}
    """
    vote_map = defaultdict(float)
    
    for cand in candidates:
        text = cand.get("text", "")
        source = cand.get("source", "llm_hint")
        confidence = cand.get("confidence", 0.1)
        
        weight = SOURCE_WEIGHTS.get(source, 0.2)
        score = weight * confidence
        
        vote_map[text] += score
    
    return dict(vote_map)


# ═══════════════════════════════════════════════════════════════
# 3. 主入口
# ═══════════════════════════════════════════════════════════════

def probabilistic_correct(
    text: str,
    low_conf_words: List[Tuple[str, float]] = None,
    speaker_profile: Dict = None,
    domain: str = "",
    subtitle_text: str = "",
    subtitle_segments: List[Dict] = None,
    ocr_persistent: str = "",
) -> Tuple[str, List[Dict]]:
    """词级概率性修正主入口
    
    对低置信度/疑似错误的词，生成多源候选 → 投票 → 选择最佳
    
    Args:
        text: 待修正文本
        low_conf_words: [(word, confidence), ...] whisper 低置信词
        speaker_profile: 说话人知识档案
        domain: 领域标签
        subtitle_text: 官方字幕文本
        subtitle_segments: 字幕分段
        ocr_persistent: OCR 持久文字
    
    Returns:
        (corrected_text, corrections: List[Dict])
        每个 correction 格式:
        {
            "original": str,
            "corrected": str,
            "confidence": float,
            "sources": [{"source": str, "label": str}],
            "vote_score": float,
        }
    """
    if not text:
        return text, []
    
    # 没有低置信词 → 跳过，除非有确定性规则匹配
    if not low_conf_words:
        return text, []
    
    corrections = []
    corrected_text = text
    processed_ranges = []  # [(start, end), ...] 避免重叠修正
    
    for word, raw_conf in low_conf_words:
        if not word or word.strip() in ("", "[BLEEP]"):
            continue
        
        word = word.strip()
        
        # 检查是否已被修正（防止重叠）
        word_start = corrected_text.find(word)
        if word_start < 0:
            # 词可能已经被之前的修正改变了，尝试其他匹配
            continue
        
        # 检查是否与已修正范围重叠
        if any(start <= word_start < end for start, end in processed_ranges):
            continue
        
        # ── 生成候选 ──
        all_candidates = []
        
        # 源A: 说话人知识库
        if speaker_profile:
            all_candidates.extend(
                _generate_candidates_from_speaker(word, speaker_profile))
        
        # 源B: 模糊音混淆矩阵
        all_candidates.extend(
            _generate_candidates_from_fuzzy(word, domain))
        
        # 源C: 官方字幕
        all_candidates.extend(
            _generate_candidates_from_subtitle(word, subtitle_text, subtitle_segments or []))
        
        # 源D: OCR
        all_candidates.extend(
            _generate_candidates_from_ocr(word, ocr_persistent))
        
        # 源E: 通用纠错词典
        all_candidates.extend(
            _generate_candidates_from_dict(word))
        
        # 源F: 确定性规则
        all_candidates.extend(
            _generate_candidates_from_rules(word))
        
        if not all_candidates:
            continue
        
        # ── 加权投票 ──
        scores = _compute_weighted_score(all_candidates)
        if not scores:
            continue
        
        # 按得分排序
        sorted_scores = sorted(scores.items(), key=lambda x: -x[1])
        best_text, best_score = sorted_scores[0]
        
        # 低于阈值 → 不做修正（标记为存疑）
        if best_score < 0.2:
            continue
        
        # ── 执行修正 ──
        # 收集来源信息
        used_sources = []
        for cand in all_candidates:
            if cand.get("text") == best_text:
                used_sources.append({
                    "source": cand.get("source", "unknown"),
                    "label": cand.get("source_label", ""),
                    "confidence": cand.get("confidence", 0),
                })
        
        # 去重 source 标签
        seen_labels = set()
        unique_sources = []
        for s in used_sources:
            label = s.get("label", "")
            if label not in seen_labels:
                seen_labels.add(label)
                unique_sources.append(s)
        
        # 执行替换（只替换第一次出现，且不跨越已修正范围）
        idx = corrected_text.find(word, word_start)
        if idx >= 0:
            corrected_text = corrected_text[:idx] + best_text + corrected_text[idx + len(word):]
            processed_ranges.append((idx, idx + len(best_text)))
            
            corrections.append({
                "original": word,
                "corrected": best_text,
                "confidence": round(best_score, 3),
                "raw_whisper_conf": round(raw_conf, 3),
                "sources": unique_sources,
                "vote_score": round(best_score, 3),
            })
    
    if corrections:
        print(f"  [概率修正] ✅ {len(corrections)}处修正 (总分投票)")
        for c in corrections:
            sources_str = "; ".join(s.get("label", s.get("source", "")) for s in c["sources"][:3])
            print(f"    {c['original']} → {c['corrected']} (score={c['confidence']}, {sources_str})")
    
    return corrected_text, corrections


# ═══════════════════════════════════════════════════════════════
# 4. 辅助：展示候选详情（调试用）
# ═══════════════════════════════════════════════════════════════

def show_candidate_details(word: str, candidates: List[Dict]) -> str:
    """格式化显示候选详情"""
    lines = [f"词: '{word}' 候选数: {len(candidates)}"]
    for i, cand in enumerate(candidates):
        weight = SOURCE_WEIGHTS.get(cand.get("source", "llm_hint"), 0.2)
        score = weight * cand.get("confidence", 0)
        lines.append(
            f"  [{i+1}] '{cand['text']}' "
            f"源={cand['source']} "
            f"权重={weight:.1f} "
            f"置信={cand['confidence']:.2f} "
            f"得分={score:.3f}"
        )
    return "\n".join(lines)
