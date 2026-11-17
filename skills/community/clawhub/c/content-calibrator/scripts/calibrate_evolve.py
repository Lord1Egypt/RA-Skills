#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rubric进化脚本 - content-calibrator Skill的exec脚本
来源: P2-07修复 / 02手册§十一 W9
功能: 聚合近N天review数据→按平台分组→计算各维度偏差→调整权重→原子写入rubric.json
统一入口: db_logger日志 + atomic_write原子写入
"""
import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
from mcps.shared.db_logger import get_logger
from mcps.shared.atomic_write import atomic_write_json
logger = get_logger("content-calibrator", source="skills/content-calibrator/scripts/calibrate_evolve.py")

REVIEWS_DIR = _PROJECT_ROOT / "data" / "content-calibrator" / "reviews"
RUBRICS_DIR = _PROJECT_ROOT / "data" / "content-calibrator" / "rubrics"

# 7维默认权重(与calibrate_score.py一致)
DEFAULT_WEIGHTS = {"ER": 1.5, "HP": 1.5, "SR": 1.5, "QL": 1.0, "NA": 1.0, "AB": 1.0, "PV": 1.0}
DEVIATION_THRESHOLD = 1.5  # 偏差比率阈值(actual/pred或pred/actual中较大值)
WEIGHT_STEP = 0.1
WEIGHT_MIN = 0.5
WEIGHT_MAX = 2.5

# 偏差→维度映射: views偏差影响HP/SR, engagement偏差影响ER/QL
VIEWS_DIMS = ["HP", "SR"]
ENGAGEMENT_DIMS = ["ER", "QL"]


def _load_recent_reviews(days: int) -> List[Dict]:
    """加载近N天的review记录"""
    if not REVIEWS_DIR.exists():
        return []
    cutoff = datetime.now() - timedelta(days=days)
    reviews = []
    for f in REVIEWS_DIR.glob("review_*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            created = data.get("created_at", "")
            if created:
                review_time = datetime.fromisoformat(created)
                if review_time >= cutoff:
                    reviews.append(data)
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"跳过无效review文件{f.name}: {e}")
    return reviews


def _calc_deviation_ratio(pred_mid: float, actual: float) -> float:
    """计算偏差比率(始终>=1.0, 1.0=完全准确)"""
    if pred_mid <= 0 or actual <= 0:
        return 1.0
    return max(actual / pred_mid, pred_mid / actual)


def _adjust_weights(weights: Dict[str, float], reviews: List[Dict]) -> Dict[str, float]:
    """基于review数据调整权重"""
    if not reviews:
        return weights
    adjusted = dict(weights)
    for review in reviews:
        prediction = review.get("prediction", {})
        actual = review.get("actual", {})
        # 计算views偏差
        pred_views = prediction.get("expected_views") or prediction.get("predicted_views", 0)
        if isinstance(pred_views, str) and "-" in pred_views:
            nums = [float(x) for x in pred_views.replace("%", "").split("-") if x.strip()]
            pred_mid = sum(nums) / len(nums) if nums else 0
        elif isinstance(pred_views, (int, float)):
            pred_mid = float(pred_views)
        else:
            pred_mid = 0
        actual_views = float(actual.get("views", 0))
        views_ratio = _calc_deviation_ratio(pred_mid, actual_views)
        if views_ratio > DEVIATION_THRESHOLD:
            direction = 1 if actual_views > pred_mid else -1
            for dim in VIEWS_DIMS:
                adjusted[dim] = max(WEIGHT_MIN, min(WEIGHT_MAX, round(adjusted[dim] + direction * WEIGHT_STEP, 2)))
        # 计算engagement偏差
        pred_eng = prediction.get("expected_engagement") or prediction.get("predicted_engagement", "0")
        if isinstance(pred_eng, str) and "-" in pred_eng:
            nums = [float(x) for x in pred_eng.replace("%", "").split("-") if x.strip()]
            pred_eng_mid = sum(nums) / len(nums) if nums else 0
        elif isinstance(pred_eng, (int, float)):
            pred_eng_mid = float(pred_eng)
        else:
            pred_eng_mid = 0
        actual_likes = float(actual.get("likes", 0))
        actual_comments = float(actual.get("comments", 0))
        actual_shares = float(actual.get("shares", 0))
        # P2-07修复: 实际engagement转为百分比(与预测格式一致)
        actual_views_for_eng = float(actual.get("views", 0))
        if actual_views_for_eng > 0:
            actual_eng = (actual_likes + actual_comments + actual_shares) / actual_views_for_eng * 100
        else:
            actual_eng = 0
        eng_ratio = _calc_deviation_ratio(pred_eng_mid, actual_eng)
        if eng_ratio > DEVIATION_THRESHOLD:
            direction = 1 if actual_eng > pred_eng_mid else -1
            for dim in ENGAGEMENT_DIMS:
                adjusted[dim] = max(WEIGHT_MIN, min(WEIGHT_MAX, round(adjusted[dim] + direction * WEIGHT_STEP, 2)))
    return adjusted


def evolve(tenant_id: str, days: int) -> Dict:
    """Rubric进化主函数

    Args:
        tenant_id (str): 参数说明
        days (int): 参数说明

    Returns:
        Dict: 返回值说明
    """
    try:
        reviews = _load_recent_reviews(days)
        if not reviews:
            return {"success": True, "data": {"message": f"近{days}天无review记录,跳过进化",
                    "platforms_updated": []}, "error": None, "code": None}
        # 按平台分组
        platform_groups: Dict[str, List[Dict]] = {}
        for r in reviews:
            platform = r.get("platform", "default")
            platform_groups.setdefault(platform, []).append(r)
        RUBRICS_DIR.mkdir(parents=True, exist_ok=True)
        updated_platforms = []
        for platform, group_reviews in platform_groups.items():
            # 读取现有rubric或使用默认权重
            rubric_file = RUBRICS_DIR / f"{platform}.json"
            if rubric_file.exists():
                rubric = json.loads(rubric_file.read_text(encoding="utf-8"))
                weights = rubric.get("weights", dict(DEFAULT_WEIGHTS))
            else:
                weights = dict(DEFAULT_WEIGHTS)
            # 调整权重
            new_weights = _adjust_weights(weights, group_reviews)
            # 原子写入rubric.json
            rubric_data = {
                "platform": platform, "weights": new_weights,
                "previous_weights": weights,
                "review_count": len(group_reviews),
                "updated_at": datetime.now().isoformat(),
                "tenant_id": tenant_id,
            }
            atomic_write_json(str(rubric_file), rubric_data, indent=2, ensure_ascii=False)
            updated_platforms.append({
                "platform": platform,
                "review_count": len(group_reviews),
                "weight_changes": {d: {"from": weights[d], "to": new_weights[d]}
                                   for d in new_weights if weights.get(d, 0) != new_weights[d]},
            })
            logger.info(f"rubric进化完成: {platform} ({len(group_reviews)}条review)")
        return {"success": True, "data": {"message": f"进化完成,处理{len(reviews)}条review",
                "platforms_updated": updated_platforms}, "error": None, "code": None}
    except Exception as e:
        logger.error(f"evolve失败: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "EVOLVE_ERROR"}


def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="Rubric进化(基于review数据调整权重)")
    parser.add_argument("tenant_id", help="租户ID")
    parser.add_argument("--days", type=int, default=7, help="聚合天数(默认7)")
    args = parser.parse_args()
    result = evolve(args.tenant_id, args.days)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
