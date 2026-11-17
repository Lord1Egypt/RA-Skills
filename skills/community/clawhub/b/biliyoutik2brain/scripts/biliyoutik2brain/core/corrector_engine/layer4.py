"""
BiliYouTik2Brain — Corrector Engine L4: OCR帧验证

通过视频画面中的文字来交叉验证低置信词。
不直接调用OCR模型（由 enhance_engine 预处理后传入 ocr_text）。

职责单一: OCR文字匹配 → 确认或修正whisper的错误识别。
代码做确定的事：字典匹配 + 模式匹配，不调LLM。
"""

import re
from typing import List, Tuple, Optional, Set
from .utils import safe_float


def level4_ocr_frame(
    low_conf_words: List[Tuple[str, float]],
    full_text: str,
    segments: List[dict],
    bvid: str = "",
    video_path: str = "",
    ocr_text: str = "",
) -> List[dict]:
    """L4: OCR帧验证
    
    利用 enhance_engine 预计算/传入的OCR文字（非空时不额外调OCR模型）。
    代码做确定的事：OCR中有低置信词 → 确认；OCR中有不同写法 → 建议修正。
    
    Args:
        low_conf_words: [(word, confidence), ...]
        full_text: 全量转录文本
        segments: 时间分段 [{start, end, text}, ...]
        bvid: 视频ID
        video_path: 视频文件路径（已弃用，改为从ocr_text获取）
        ocr_text: 预计算OCR文字（来自 enhance_engine 的 ocr_persistent + ocr_timeline）
    
    Returns:
        修正候选列表
    """
    if not low_conf_words or not ocr_text:
        return []
    
    # ── 步骤1: 从 ocr_text 中提取所有有意义的词 ──
    ocr_words = _extract_words_from_ocr(ocr_text)
    if not ocr_words:
        return []
    
    # ── 步骤2: 与低置信词交叉验证 ──
    candidates = []
    for w, c in low_conf_words:
        # 跳过空词和短词
        if not w or len(w) <= 1:
            continue
        
        found_exact = w in ocr_words
        if found_exact:
            # OCR确认原始词正确
            ctx = _get_context(full_text, w)
            candidates.append({
                "original": w,
                "corrected": w,
                "source": "L4_ocr_frame",
                "confidence": 0.95,
                "evidence": f"OCR视频画面确认: '{w}' 在帧文字中",
                "context_snippet": ctx[:200],
            })
            continue
        
        # 检查是否与OCR中某个高度相似的词匹配
        best_similarity = 0.0
        best_match = ""
        for ocr_w in ocr_words:
            if len(ocr_w) >= 2 and len(w) >= 2:
                # 简单重叠：w 中的字符出现在 ocr_w 中的比例
                common = sum(1 for ch in w if ch in ocr_w)
                sim = common / max(len(w), len(ocr_w))
                if sim > best_similarity:
                    best_similarity = sim
                    best_match = ocr_w
        
        if best_similarity >= 0.6 and best_match != w:
            # OCR确认有不同写法
            ctx = _get_context(full_text, w)
            candidates.append({
                "original": w,
                "corrected": best_match,
                "source": "L4_ocr_frame",
                "confidence": 0.85,
                "evidence": f"OCR画面匹配: '{w}' → '{best_match}' (重叠度={best_similarity:.2f})",
                "context_snippet": ctx[:200],
            })
    
    return candidates


def _extract_words_from_ocr(ocr_text: str) -> Set[str]:
    """从OCR文本中提取有意义的词
    
    从 enhance_engine 传入的 ocr_persistent + timeline 文本中
    提取中英文词。
    """
    words = set()
    
    # 按行分割
    for line in ocr_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("[") or line.startswith("视频画面"):
            continue
        
        # 提取中文词（2字及以上）
        chinese_chars = re.findall(r'[\u4e00-\u9fff]{2,}', line)
        for cw in chinese_chars:
            words.add(cw)
        
        # 提取英文词（2字母及以上）
        english_words = re.findall(r'[a-zA-Z]{2,}', line)
        for ew in english_words:
            words.add(ew.lower())
        
        # 提取混合词（中英文数字混合）
        mixed = re.findall(r'[\u4e00-\u9fff0-9a-zA-Z]{2,}', line)
        for mw in mixed:
            words.add(mw)
    
    return words


def _get_context(text: str, word: str, width: int = 50) -> str:
    pos = text.find(word)
    if pos < 0:
        return ""
    start = max(0, pos - width)
    end = min(len(text), pos + len(word) + width)
    snippet = text[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet.strip()
