"""
transcription_corrector.py — thin wrapper for backward compatibility

v3: 所有逻辑已迁入 core/corrector_engine/ + core/corrector_dictionary.py
此文件只做 re-export，保持旧 import 路径正常工作。
"""

import os, sys, json, re, time, math
from typing import Dict, Optional, List, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict

# 所有核心逻辑从新模块导入
from ..core.corrector_engine import correct_transcription as _engine_correct
from ..core.corrector_dictionary import (
    DOMAIN_CORRECTIONS, CORRECTION_DICT_PATH, CORRECTION_STATS_FILE,
    TRADING_TERMS, SPEECH_FILLERS, BEEP_TERMS,
    fast_domain_correct,
    check_bleep, check_multi_word_pattern,
    load_correction_dict, save_correction_dict,
    record_correction, update_stats,
)

# ── 保持旧的数据模型和导出接口 ──

@dataclass
class CorrectionCandidate:
    """单次修正候选（向后兼容）"""
    original_word: str
    corrected_word: str
    source: str
    confidence: float
    evidence: str
    context_snippet: str = ""
    priority: int = 0
    applied: bool = False

@dataclass
class CorrectionResult:
    """完整修正结果（向后兼容）"""
    bvid: str = ""
    original_text: str = ""
    corrected_text: str = ""
    corrections: List[CorrectionCandidate] = field(default_factory=list)
    final_confidence: float = 0.0
    layers_used: List[str] = field(default_factory=list)
    regression_passed: bool = False
    total_tokens_saved: int = 0
    l5_full_correction: str = ""
    l5_unresolved_words: List[str] = field(default_factory=list)


# ── 旧常量（保持向后兼容） ──
_DEBUG = os.environ.get("BILI_DEBUG", "").lower() in ("1", "true", "yes")
HARD_THRESHOLD = 0.6
LAYER_EXIT_THRESHOLD = 0.9

# DeepSeek配置（旧版本可能直接引用这些变量）
try:
    from ..extra.transcription_enhancer import (
        DEEPSEEK_API_KEY, DEEPSEEK_BASE, LLM_MODEL,
        _call_llm as _enhancer_call_llm,
    )
    _HAVE_ENHANCER = True
except ImportError:
    DEEPSEEK_API_KEY = os.environ.get("LLM_API_KEY") or ""
    DEEPSEEK_BASE = os.environ.get("LLM_BASE_URL") or "https://api.deepseek.com/v1"
    LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-flash")
    _HAVE_ENHANCER = False


# ── 旧函数（保持向后兼容，实际调用新引擎） ──

def _safe_float(value, default=0.0):
    from ..core.corrector_engine.utils import safe_float
    return safe_float(value, default)


def _load_correction_dict() -> Dict:
    return load_correction_dict()

def _save_correction_dict(d: Dict):
    save_correction_dict(d)

def _append_to_lessons(pattern: str, correction: str, bvid: str, source: str, confidence: float):
    from ..core.corrector_engine.feedback import append_to_lessons
    append_to_lessons(pattern, correction, bvid, source, confidence)

def _record_to_stats(bvid: str, corrections: List[CorrectionCandidate]):
    for c in corrections:
        update_stats(bvid, c.corrected_word, c.original_word, c.source, c.confidence)

def _extract_json(text: str) -> Optional[dict]:
    from ..core.corrector_engine.utils import extract_json
    return extract_json(text)

def _extract_json_array(text: str) -> Optional[list]:
    from ..core.corrector_engine.utils import extract_json_array
    return extract_json_array(text)

def _compute_priority(word: str) -> int:
    from ..core.corrector_engine.utils import compute_priority
    return compute_priority(word)

def _is_noise_word(word: str) -> bool:
    from ..core.corrector_engine.utils import is_noise_word
    return is_noise_word(word)

def _sort_low_conf_words(words: List[Tuple[str, float]]) -> List[Tuple[str, float, int]]:
    from ..core.corrector_engine.utils import sort_low_conf_words
    return sort_low_conf_words(words)

def _call_llm(messages: List[Dict], timeout: int = 60) -> Optional[str]:
    from ..core.corrector_engine.utils import call_llm
    return call_llm(messages, timeout)

def _check_bleep(word: str) -> Optional[Tuple[str, float, str]]:
    return check_bleep(word)

def _check_multi_word_pattern(words: List[str], text: str) -> List[Dict]:
    return check_multi_word_pattern(words, text)

def _handle_gotchas(candidate: CorrectionCandidate) -> CorrectionCandidate:
    from ..core.corrector_engine.exit import handle_gotchas as _gh
    gh = _gh(candidate.original_word, candidate.corrected_word, candidate.confidence, candidate.context_snippet)
    return CorrectionCandidate(
        original_word=candidate.original_word,
        corrected_word=gh["corrected"],
        source=candidate.source,
        confidence=gh["confidence"],
        evidence=candidate.evidence + gh["evidence"],
        context_snippet=candidate.context_snippet,
        priority=candidate.priority,
        applied=candidate.applied,
    )

def _check_exit(candidates: List[CorrectionCandidate]) -> bool:
    from ..core.corrector_engine.exit import check_exit as _ce
    applied = {c.original_word: {"confidence": c.confidence} for c in candidates}
    return _ce([(c.original_word, c.confidence) for c in candidates], applied)

def _filter_by_confidence(candidates: List[CorrectionCandidate]) -> List[CorrectionCandidate]:
    return [c for c in candidates if c.confidence >= HARD_THRESHOLD]

def _regression_check(original: str, corrected: str) -> Tuple[bool, List[str]]:
    from ..core.corrector_engine.exit import regression_check
    return regression_check(original, corrected)

def _workflow_recorder(bvid, text, low_conf_words, result, token_usage=None):
    pass  # v3 feedback engine handles this

def _feedback_loop(candidates: List[CorrectionCandidate], bvid: str):
    from ..core.corrector_engine.feedback import feedback_loop
    dict_candidates = [
        {"original": c.original_word, "corrected": c.corrected_word,
         "source": c.source, "confidence": c.confidence,
         "evidence": c.evidence, "context_snippet": c.context_snippet,
         "applied": c.applied}
        for c in candidates
    ]
    feedback_loop(dict_candidates, bvid)

def _get_context_snippet(full_text: str, word: str, window_sentences: int = 2) -> str:
    from ..core.corrector_engine.layer1 import _get_context_snippet
    return _get_context_snippet(full_text, word)

def _get_context_snippet_by_chars(full_text: str, word: str, window_chars: int = 50) -> str:
    from ..core.corrector_engine.layer2 import _get_context_snippet
    return _get_context_snippet(full_text, word)

def _mark_text_with_low_conf(text: str, words: List[Tuple[str, float]]) -> str:
    # stub — 旧代码中使用，实际无实现
    return text

def _subtitle_api_stub(bvid: str, word: str, context: str):
    return None

def _estimate_tokens_saved(candidates, layer_order):
    return len(candidates) * 100  # 粗略估算


# ── 核心入口（包装为旧接口） ──

def correct_transcription(
    text: str,
    segments: List[Dict] = None,
    low_conf_words: List[Tuple[str, float]] = None,
    bvid: str = "",
    bleep_text: str = "",
    subtitle_segments: Optional[List[Dict]] = None,
    video_path: str = "",
    speaker_knowledge: str = "",
    ocr_context: str = "",
    enable_ocr: bool = False,
    l2_max_words: int = 50,
    skip_l3: bool = False,
    skip_l5: bool = False,
) -> CorrectionResult:
    """层次化修正主入口 — 旧接口包装新引擎
    
    输出仍然是旧版 CorrectionResult，保持 pipeline.py 兼容。
    """
    result_dict = _engine_correct(
        text=text,
        segments=segments,
        low_conf_words=low_conf_words,
        bvid=bvid,
        bleep_text=bleep_text,
        subtitle_segments=subtitle_segments,
        video_path=video_path,
        speaker_knowledge=speaker_knowledge,
        ocr_context=ocr_context,
        enable_ocr=enable_ocr,
        l2_max_words=l2_max_words,
        skip_l3=skip_l3,
        skip_l5=skip_l5,
    )
    
    # 转换回旧版 dataclass
    corrections = []
    for c in result_dict.get("corrections", []):
        corrections.append(CorrectionCandidate(
            original_word=c.get("original", ""),
            corrected_word=c.get("corrected", ""),
            source=c.get("source", ""),
            confidence=c.get("confidence", 0.0),
            evidence=c.get("evidence", ""),
            context_snippet=c.get("context_snippet", ""),
            priority=c.get("priority", 0),
            applied=c.get("applied", False),
        ))
    
    return CorrectionResult(
        bvid=result_dict.get("bvid", bvid),
        original_text=result_dict.get("original_text", text),
        corrected_text=result_dict.get("corrected_text", text),
        corrections=corrections,
        final_confidence=result_dict.get("final_confidence", 0.0),
        layers_used=result_dict.get("layers_used", []),
        regression_passed=result_dict.get("regression_passed", True),
        l5_full_correction=result_dict.get("l5_full_correction", ""),
        l5_unresolved_words=result_dict.get("l5_unresolved_words", []),
    )


# ── 导出（兼容旧 import） ──

__all__ = [
    "CorrectionCandidate", "CorrectionResult",
    "correct_transcription", "fast_domain_correct",
    "level1_cross_validate", "level2_llm_local_repair",
    "level2_5_sentence_context", "level3_paragraph_context",
    "level4_ocr_frame", "level5_full_degradation",
]
