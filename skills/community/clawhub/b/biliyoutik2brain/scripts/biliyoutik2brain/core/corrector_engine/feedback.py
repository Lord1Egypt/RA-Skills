"""
BiliYouTik2Brain — Corrector Engine 反馈闭环

v3: 错题库从"词对"升级为"题型+解题思路+示例"结构。
    每次修正写入题型模式库，高置信修正追加到 lessons.md。

题型分类:
  - 同音误识: whisper听错同音词（最常见）
  - 术语校准: 交易/专业术语whisper不识别
  - 语义修复: 上下文决定正确的词
  - 消音标记: BLEEP/***
  - 口语填充: 啊/呢/吧等不修正
  - 其他
"""

import os, json, time
from typing import List, Dict, Tuple
from ..corrector_dictionary import (
    record_correction, update_stats, load_correction_stats, save_correction_stats,
    get_problem_type, SPEECH_FILLERS,
)

_LESSONS_PATH = os.path.expanduser("~/openclaw/workspace/lessons.md")
_WIKI_PATH = os.path.expanduser("~/wiki/wiki/lessons/anti-patterns.md")


def append_to_lessons(pattern: str, correction: str, bvid: str, source: str, confidence: float):
    """将高置信修正追加到 lessons.md（以 rule 格式写入）"""
    problem_type = get_problem_type(pattern)
    entry = f"""
### [{problem_type}] {pattern} → {correction}
- When: transcription contains "{pattern}"
- Do: correct to "{correction}" (confirmed by {source}, conf={confidence:.2f})
- Why: whisper misheard in {bvid} due to similar pronunciation
"""
    try:
        os.makedirs(os.path.dirname(_LESSONS_PATH), exist_ok=True)
        with open(_LESSONS_PATH, "a") as f:
            f.write(entry)
    except OSError:
        pass


def feedback_loop(candidates: List[dict], bvid: str):
    """反馈闭环：题型模式库 + lessons.md + 统计
    
    Args:
        candidates: 修正结果列表，每项含 original/corrected/source/confidence 等
        bvid: 视频ID
    """
    for c in candidates:
        if c.get("original") == c.get("corrected"):
            continue
        
        problem_type = get_problem_type(c.get("original", ""))
        
        # 核心：题型模式存储
        record_correction(
            original=c.get("original", ""),
            corrected=c.get("corrected", ""),
            source=c.get("source", "unknown"),
            confidence=c.get("confidence", 0.0),
            bvid=bvid,
            problem_type=problem_type,
            solution=c.get("evidence", ""),
            example="",
        )
        
        # 统计更新
        update_stats(
            bvid=bvid,
            original=c.get("original", ""),
            corrected=c.get("corrected", ""),
            source=c.get("source", "unknown"),
            confidence=c.get("confidence", 0.0),
        )
        
        # 高置信修正 → lessons.md
        if c.get("confidence", 0) >= 0.85 and c.get("original") != c.get("corrected"):
            append_to_lessons(
                c.get("original", ""),
                c.get("corrected", ""),
                bvid, c.get("source", "unknown"),
                c.get("confidence", 0.0),
            )


def workflow_recorder(
    bvid: str,
    text: str,
    low_conf_words: List[Tuple[str, float]],
    layer_used: List[str],
    correction_count: int,
    applied_count: int,
    final_confidence: float,
    text_changed: bool,
    regression_passed: bool,
    unresolved_words: List[str],
    corrections: List[dict],
    token_usage: dict = None,
):
    """工作流数据记录器 — 自进化引擎原材料"""
    from collections import defaultdict
    
    layer_counts = defaultdict(int)
    for c in corrections:
        src = c.get("source", "unknown").split("_")[0] if "_" in c.get("source", "") else c.get("source", "unknown")
        layer_counts[src] += 1
    
    risky_corrections = []
    for c in corrections:
        if c.get("applied", False) and c.get("confidence", 0) < 0.7:
            risky_corrections.append({
                "original": c.get("original"),
                "corrected": c.get("corrected"),
                "confidence": c.get("confidence"),
                "source": c.get("source"),
                "context": (c.get("context_snippet") or "")[:60],
            })
    
    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "bvid": bvid,
        "text_len": len(text),
        "low_conf_count": len(low_conf_words),
        "correction_count": correction_count,
        "applied_count": applied_count,
        "layers_hit": layer_used,
        "layers_detail": dict(layer_counts),
        "final_confidence": round(final_confidence, 3),
        "regression_passed": regression_passed,
        "text_changed": text_changed,
        "unresolved_words": unresolved_words[:20],
        "risky_corrections": risky_corrections[:10],
        "token_usage": token_usage or {},
    }
    
    daily_file = os.path.expanduser(
        f"~/openclaw/workspace/temp/self-evolve/raw-{time.strftime('%Y-%m-%d')}.jsonl"
    )
    try:
        os.makedirs(os.path.dirname(daily_file), exist_ok=True)
        with open(daily_file, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass
