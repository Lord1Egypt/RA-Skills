#!/usr/bin/env python3
"""内容质量评分脚本 (P2-017)

统一内容质量评分接口,纯Python实现,无LLM调用/无外部依赖。
维度: coherence(叙事连贯) / consistency(内容一致) / quality(基础质量) / overall(35%+30%+35%)。
依赖: db_logger(规则18) + atomic_write(规则18)

用法:
  python content_quality_scorer.py --action score \
      --params '{"content":"第一章 山有木兮。山有木兮木有枝。", "content_type":"novel_chapter"}'
  python content_quality_scorer.py --action batch_score \
      --params '{"chapters":[{"chapter_number":1,"content":"..."}]}'
"""
import sys

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

# R14-R7统一入口: db_logger(规则18) + atomic_write(规则18)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
from mcps.shared.atomic_write import atomic_write_json

import logging
logger = get_logger("system", source="skills/content-orchestrator/scripts/content_quality_scorer.py")

logger = get_logger("content-quality-scorer", source="skills/content-orchestrator/scripts/content_quality_scorer.py")

# 各类型最低字数目标(来源:02手册§五5.2) / AI典型过渡词(02手册§八8.3) / 叙事过渡词
_TARGET_LENGTH = {"novel_chapter": 2000, "drama_script": 500, "article": 800}
_AI_PHRASES = ["首先", "其次", "最后", "总之", "综上所述", "由此可见"]
_TRANSITION_WORDS = ["因此", "然而", "于是", "接着", "然后", "所以", "不过", "可是", "随后"]

def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))

def _score_coherence(content: str) -> Tuple[float, Dict]:
    """连贯性评分: 段落平均长度(30-200佳)/人名一致性/过渡词"""
    paragraphs = [p for p in content.split("\n") if p.strip()]
    avg_len = sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0
    para_score = 100.0 if 30 <= avg_len <= 200 else max(0.0, 100 - abs(avg_len - 115) * 0.5)
    names = set(re.findall(r"[\u4e00-\u9fa5]{2,4}(?:说|道|想|看|笑)", content))
    name_score = min(100.0, len(names) * 25) if names else 60.0
    trans_hits = sum(1 for w in _TRANSITION_WORDS if w in content)
    score = _clamp(para_score * 0.4 + name_score * 0.3 + min(100.0, trans_hits * 20) * 0.3)
    return score, {"avg_paragraph_len": round(avg_len, 1), "name_count": len(names), "transition_hits": trans_hits}

def _score_consistency(content: str) -> Tuple[float, Dict]:
    """一致性评分: 重复句率(<10%佳)/词汇丰富度(>40%佳)"""
    sentences = [s.strip() for s in re.split(r"[。！？!?.]", content) if s.strip()]
    dup_ratio = (len(sentences) - len(set(sentences))) / len(sentences) if sentences else 0.0
    dup_score = 100.0 if dup_ratio < 0.1 else max(0.0, 100 - dup_ratio * 300)
    words = re.findall(r"[\u4e00-\u9fa5]+|\w+", content)
    unique_ratio = len(set(words)) / len(words) if words else 0.0
    word_score = 100.0 if unique_ratio > 0.4 else max(0.0, unique_ratio * 250)
    score = _clamp(dup_score * 0.5 + word_score * 0.5)
    return score, {"duplicate_ratio": round(dup_ratio, 3), "unique_word_ratio": round(unique_ratio, 3)}

def _score_quality(content: str, content_type: str) -> Tuple[float, Dict]:
    """基础质量评分: 长度达标/句式多样/AI味抑制"""
    target = _TARGET_LENGTH.get(content_type, 800)
    length = len(content.strip())
    len_score = min(100.0, length / target * 100) if target > 0 else 60.0
    sentences = [s for s in re.split(r"[。！？!?.]", content) if s.strip()]
    if len(sentences) >= 2:
        avg = sum(len(s) for s in sentences) / len(sentences)
        variety = min(100.0, (sum((len(s) - avg) ** 2 for s in sentences) / len(sentences)) ** 0.5 * 10)
    else:
        variety = 30.0
    ai_hits = sum(content.count(p) for p in _AI_PHRASES)
    ai_score = max(0.0, 100 - ai_hits * 15)
    score = _clamp(len_score * 0.4 + variety * 0.3 + ai_score * 0.3)
    return score, {"length": length, "target": target, "sentence_variety": round(variety, 1), "ai_phrase_hits": ai_hits}

def score_content(content: str, content_type: str, chapter_number: int = 0) -> Dict:
    """单内容评分,返回结构化结果

    Args:
        content (str): 参数说明
        content_type (str): 参数说明
        chapter_number (int): 参数说明

    Returns:
        Dict: 返回值说明
    """
    coh, coh_d = _score_coherence(content)
    con, con_d = _score_consistency(content)
    qual, qual_d = _score_quality(content, content_type)
    overall = _clamp(coh * 0.35 + con * 0.30 + qual * 0.35)
    return {"success": True, "data": {
        "chapter_number": chapter_number, "content_type": content_type,
        "scores": {"coherence_score": round(coh, 1), "consistency_score": round(con, 1),
                   "quality_score": round(qual, 1), "overall_score": round(overall, 1)},
        "details": {"coherence": coh_d, "consistency": con_d, "quality": qual_d}},
        "error": None, "code": None}

def batch_score(chapters: List[Dict]) -> Dict:
    """批量评分,返回逐章分数+平均分

    Args:
        chapters (List[Dict]): 参数说明

    Returns:
        Dict: 返回值说明
    """
    results = [score_content(ch.get("content", ""), ch.get("content_type", "novel_chapter"),
                             ch.get("chapter_number", 0))["data"] for ch in chapters]
    avg = sum(r["scores"]["overall_score"] for r in results) / len(results) if results else 0.0
    return {"success": True, "data": {"chapters": results, "average_overall_score": round(avg, 1),
                                      "count": len(results)}, "error": None, "code": None}

def main() -> None:
    """CLI入口: python content_quality_scorer.py --action score --params '{...}'
    
    Raises:
        ValueError: 异常说明
    """
    parser = argparse.ArgumentParser(description="内容质量评分(P2-017)")
    parser.add_argument("--action", required=True, choices=["score", "batch_score"], help="执行动作")
    parser.add_argument("--params", type=str, default="{}", help="参数JSON字符串")
    parser.add_argument("--output", type=str, default="", help="结果输出文件路径(可选,原子写入)")
    args = parser.parse_args()
    try:
        params = json.loads(args.params) if args.params else {}
        if args.action == "score":
            content = params.get("content", "")
            if not content or not content.strip():
                raise ValueError(f"content不能为空: action={args.action}, content_len={len(content)}, params_keys={list(params.keys())}")
            content_type = params.get("content_type", "novel_chapter")
            if content_type not in _TARGET_LENGTH:
                raise ValueError(f"content_type无效,可选: {list(_TARGET_LENGTH.keys())}")
            result = score_content(content, content_type, params.get("chapter_number", 0))
        else:
            chapters = params.get("chapters", [])
            if not chapters or not isinstance(chapters, list):
                raise ValueError("chapters不能为空且必须为列表")
            result = batch_score(chapters)
        logger.info(f"内容质量评分[{args.action}]完成")
        if args.output:
            atomic_write_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    except ValueError as e:
        logger.error(f"参数错误: {e}")
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "INVALID_INPUT"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        logger.error(f"评分异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": f"评分异常: {e}", "code": "SCORE_ERROR"}, ensure_ascii=False))
        sys.exit(2)

if __name__ == "__main__":
    main()
