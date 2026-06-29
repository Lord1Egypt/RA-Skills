#!/usr/bin/env python3
"""
risk_classifier.py — 冲稳保三档分类器

将匹配结果分为冲刺/稳妥/保底三档，并按梯度分配志愿位置。
支持新高考45志愿、96志愿和传统高考9/12志愿等多种模式。

用法:
  python risk_classifier.py --matches matches.json --volunteer-count 45 \
    --output classified.json
"""

import json
import argparse
from pathlib import Path


def classify_and_allocate(matches: list[dict], total_volunteers: int,
                          reach_ratio: float = 0.18,
                          match_ratio: float = 0.45,
                          safety_ratio: float = 0.37) -> dict:
    """
    将匹配结果分为冲稳保三档并分配志愿位置。

    参数:
      matches: ranking_matcher的输出（已按概率降序排列）
      total_volunteers: 总志愿数
      reach_ratio: 冲刺志愿比例
      match_ratio: 稳妥志愿比例
      safety_ratio: 保底志愿比例

    返回: 分类后的志愿方案
    """
    reach_list = []
    match_list = []
    safety_list = []

    for m in matches:
        risk = m.get("risk_level", "稳")
        if risk == "冲":
            reach_list.append(m)
        elif risk == "稳":
            match_list.append(m)
        else:
            safety_list.append(m)

    # 按概率排：冲(低→高) / 稳(低→高) / 保(低→高)
    reach_list.sort(key=lambda x: x["admission_probability"])
    match_list.sort(key=lambda x: x["admission_probability"])
    safety_list.sort(key=lambda x: x["admission_probability"])

    # 如果分类后的数量不足以填满志愿，从相邻档补充
    target_reach = max(1, int(total_volunteers * reach_ratio))
    target_match = max(1, int(total_volunteers * match_ratio))
    target_safety = total_volunteers - target_reach - target_match

    # 确保安全数目充足
    if target_safety < 3:
        target_safety = 3
        target_match = total_volunteers - target_reach - target_safety

    # 截断或填充
    reach_list = reach_list[:target_reach]
    match_list = match_list[:target_match]
    safety_list = safety_list[:target_safety]

    # 生成最终志愿列表
    plan = []
    volunteer_index = 1

    # 冲刺志愿 (1 ~ target_reach)
    for item in reach_list:
        item["volunteer_rank"] = volunteer_index
        plan.append(item)
        volunteer_index += 1

    # 稳妥志愿
    for item in match_list:
        item["volunteer_rank"] = volunteer_index
        plan.append(item)
        volunteer_index += 1

    # 保底志愿
    for item in safety_list:
        item["volunteer_rank"] = volunteer_index
        plan.append(item)
        volunteer_index += 1

    # 缺口填充（如果总数不够）
    gap = total_volunteers - len(plan)
    if gap > 0:
        # 在保底后面添加占位，建议用户自行补充
        for i in range(gap):
            plan.append({
                "volunteer_rank": volunteer_index,
                "university_name": f"[请补充第{volunteer_index}志愿]",
                "risk_level": "保",
                "admission_probability": 0.0,
                "note": "建议补充更低层次的保底院校或本省/本市院校"
            })
            volunteer_index += 1

    return {
        "total_volunteers": total_volunteers,
        "actual_count": len(plan),
        "strategy": {
            "reach_count": len(reach_list),
            "reach_ratio": round(len(reach_list) / total_volunteers * 100, 1),
            "match_count": len(match_list),
            "match_ratio": round(len(match_list) / total_volunteers * 100, 1),
            "safety_count": len(safety_list),
            "safety_ratio": round(len(safety_list) / total_volunteers * 100, 1),
            "gap": gap
        },
        "plan": plan
    }


def validate_plan(plan_data: dict) -> list[str]:
    """验证志愿方案合理性，返回警告列表"""
    warnings = []
    strategy = plan_data.get("strategy", {})

    reach_ratio = strategy.get("reach_ratio", 0)
    safety_ratio = strategy.get("safety_ratio", 0)
    gap = strategy.get("gap", 0)

    if reach_ratio > 25:
        warnings.append(f"冲刺志愿占比 {reach_ratio}%，偏高，建议 ≤20%")
    if reach_ratio < 5:
        warnings.append(f"冲刺志愿占比 {reach_ratio}%，偏低，建议 ≥10%")

    if safety_ratio < 25:
        warnings.append(f"保底志愿占比 {safety_ratio}%，偏低，建议 ≥30%，防止滑档")
    if safety_ratio > 50:
        warnings.append(f"保底志愿占比 {safety_ratio}%，偏高，可适当增加稳妥和冲刺")

    if gap > 0:
        warnings.append(f"志愿不足，缺 {gap} 个，建议补充")

    # 检查是否有相邻志愿录取概率跳跃过大
    plans = plan_data.get("plan", [])
    for i in range(1, len(plans) - 1):
        prev_p = plans[i - 1].get("admission_probability", 0)
        curr_p = plans[i].get("admission_probability", 0)
        next_p = plans[i + 1].get("admission_probability", 0)
        if curr_p > 0 and prev_p > 0 and curr_p - prev_p > 0.3:
            warnings.append(f"第{i+1}志愿与第{i}志愿概率跨度 {round((curr_p - prev_p) * 100)}%，梯度过大")

    return warnings


def main():
    parser = argparse.ArgumentParser(description="冲稳保三档分类器")
    parser.add_argument("--matches", type=str, required=True, help="匹配结果JSON文件")
    parser.add_argument("--volunteer-count", type=int, required=True, help="总志愿数")
    parser.add_argument("--reach-ratio", type=float, default=0.18, help="冲刺比例")
    parser.add_argument("--match-ratio", type=float, default=0.45, help="稳妥比例")
    parser.add_argument("--safety-ratio", type=float, default=0.37, help="保底比例")
    parser.add_argument("--output", type=str, default=None, help="输出JSON文件")

    args = parser.parse_args()

    with open(args.matches, "r", encoding="utf-8") as f:
        data = json.load(f)

    matches = data.get("matches", data if isinstance(data, list) else [])

    result = classify_and_allocate(
        matches, args.volunteer_count,
        args.reach_ratio, args.match_ratio, args.safety_ratio
    )

    result["warnings"] = validate_plan(result)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[risk_classifier] 方案已保存到 {args.output}", file=__import__("sys").stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
