#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T+3d复盘脚本 - content-calibrator Skill的exec脚本
来源: 02手册§十一 W9 / FIX-06降频
模型: deepseek-v4-flash (通过SENSENOVA API直调)
功能: 预测vs实际对比+准确率计算+rubric更新建议
统一入口: record_direct_usage记录Token + db_logger日志
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, List

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(_PROJECT_ROOT))
from mcps.shared.db_logger import get_logger
logger = get_logger("content-calibrator", source="skills/content-calibrator/scripts/calibrate_review.py")
from mcps.shared.atomic_write import atomic_write_json
from mcps.shared.unified_llm import llm_chat

REVIEW_MODEL = os.environ.get("CALIBRATOR_REVIEW_MODEL", "free-first")  # R33防还原: 禁止还原为deepseek-v4-flash(已欠费)
DATA_DIR = _PROJECT_ROOT / "data" / "content-calibrator" / "reviews"


def _parse_range(val) -> Tuple[float, float]:
    """解析预测值(可能是范围"500-800"或数值)"""
    if isinstance(val, (int, float)):
        return float(val), float(val)
    s = str(val).replace("%", "").replace("，", "-").replace(",", "-")
    nums = re.findall(r'\d+\.?\d*', s)
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    if len(nums) == 1:
        return float(nums[0]), float(nums[0])
    return 0.0, 0.0


def _calc_accuracy(pred_range: Tuple[float, float], actual: float) -> float:
    """计算准确率: 实际值落在预测范围内=1.0, 否则按距离衰减"""
    low, high = pred_range
    if high < low:
        low, high = high, low
    if low <= actual <= high:
        return 1.0
    mid = (low + high) / 2 if high > 0 else low
    if mid == 0:
        return 0.0
    deviation = abs(actual - mid) / max(mid, 1)
    return round(max(0.0, 1.0 - deviation), 2)


def _call_llm(prompt: str) -> List[str]:
    """通过llm_chat统一入口生成rubric更新建议
    SenseNova reasoning模型可能返回reasoning而非content,需兼容处理"""
    result = llm_chat(
        prompt=prompt,
        system_prompt="你是内容质量校准专家,分析预测偏差并提出rubric评分标准调整建议。",
        caller="content-calibrator",
        model=REVIEW_MODEL,
        provider="sensenova",
        temperature=0.3,
        max_tokens=1024,
    )
    if not result.get("success"):
        logger.warning(f"review LLM调用失败: {result.get('error', '')},跳过建议")
        return [f"LLM调用失败,跳过建议: {result.get('error', '')}"]
    # Token由llm_chat内部自动记录,无需手动调用record_direct_usage
    text = result.get("raw_text", "").strip()
    # 尝试从reasoning文本中提取JSON
    json_match = re.search(r'\{[^{}]*"suggestions"[^{}]*\}', text)
    if json_match:
        text = json_match.group(0)
    elif text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        data = json.loads(text)
        return data.get("suggestions", [text[:200]]) if isinstance(data, dict) else [str(data)[:200]]
    except json.JSONDecodeError:
        return [text[:200]]


def review(prediction_str: str, actual_str: str, platform: str = "default") -> Dict:
    """T+3d复盘主函数

    P2-07修复: 添加platform参数,evolve脚本按平台分组需要

    Args:
        prediction_str (str): 参数说明
        actual_str (str): 参数说明
        platform (str): 参数说明

    Returns:
        Dict: 返回值说明
    """
    try:
        prediction = json.loads(prediction_str)
        actual = json.loads(actual_str)
    except json.JSONDecodeError as e:
        return {"success": False, "data": {}, "error": f"JSON解析失败: {e}", "code": "JSON_PARSE_FAILED"}
    try:
        actual_views = float(actual.get("views", 0))
        actual_likes = float(actual.get("likes", 0))
        actual_comments = float(actual.get("comments", 0))
        actual_shares = float(actual.get("shares", 0))
        actual_engagement = 0.0
        if actual_views > 0:
            actual_engagement = round((actual_likes + actual_comments + actual_shares) / actual_views * 100, 2)
        pred_views = prediction.get("expected_views") or prediction.get("predicted_views", 0)
        pred_eng = prediction.get("expected_engagement") or prediction.get("predicted_engagement", "0%")
        views_range = _parse_range(pred_views)
        eng_range = _parse_range(pred_eng)
        views_accuracy = _calc_accuracy(views_range, actual_views)
        eng_accuracy = _calc_accuracy(eng_range, actual_engagement)
        overall_accuracy = round((views_accuracy + eng_accuracy) / 2, 2)
        views_dev = round(abs(actual_views - sum(views_range) / 2) / max(actual_views, 1) * 100, 1)
        eng_dev = round(abs(actual_engagement - sum(eng_range) / 2) / max(actual_engagement, 1) * 100, 1)
        llm_prompt = (f"预测: views={pred_views}, engagement={pred_eng}\n"
                      f"实际: views={actual_views}, engagement={actual_engagement}%\n"
                      f"准确率: views={views_accuracy}, engagement={eng_accuracy}\n"
                      f"请提出2-3条rubric评分标准调整建议,返回JSON: {{\"suggestions\": [...]}}")
        suggestions = _call_llm(llm_prompt)
        review_id = f"review_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        # P2-07修复: 保存platform和维度偏差到review记录,evolve脚本需要
        atomic_write_json(DATA_DIR / f"{review_id}.json",
                          {"review_id": review_id, "platform": platform,
                           "prediction": prediction, "actual": actual,
                           "accuracy": overall_accuracy,
                           "deviation": {"views": views_dev, "engagement": eng_dev},
                           "created_at": datetime.now().isoformat()},
                          indent=2, ensure_ascii=False)
        return {"success": True, "data": {"accuracy": overall_accuracy,
                "deviation": {"views": views_dev, "engagement": eng_dev},
                "rubric_update_suggestions": suggestions[:3]}, "error": None, "code": None}
    except (TimeoutError, OSError) as e:
        logger.error(f"review LLM超时: {e}")
        return {"success": False, "data": {}, "error": f"LLM调用超时: {e}", "code": "LLM_TIMEOUT"}
    except Exception as e:
        logger.error(f"review失败: {e}")
        return {"success": False, "data": {}, "error": str(e), "code": "REVIEW_ERROR"}


def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="T+3d复盘(预测vs实际)")
    parser.add_argument("--prediction", required=True, help="预测JSON字符串")
    parser.add_argument("--actual", required=True, help="实际数据JSON字符串")
    parser.add_argument("--platform", default="default", help="平台名(用于evolve按平台分组)")
    args = parser.parse_args()
    result = review(args.prediction, args.actual, args.platform)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
