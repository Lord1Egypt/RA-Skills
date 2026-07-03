#!/usr/bin/env python3
"""
general-talent-grader 评分一致性校验器（v1.0）

用途：
1. 校验输入的六维度分数是否符合充要条件
2. 校验综合得分→级别映射是否正确
3. 校验一致性检验规则（高分/低分/非均衡）
4. 输出校验报告

用法：
    python scripts/validate_scores.py --scores scores.json
    python scripts/validate_scores.py --scores scores.json --env high --leverage high
    python scripts/validate_scores.py --scores '{"ai_fluency":3,"human_ai_judgment":2.5,"architecture_design":3,"hybrid_orchestration":2.5,"cognitive_depth":2.5,"problem_modeling":3}'
"""

import argparse
import json
import sys
from typing import Optional

# ============================================================
# 常量定义（唯一标准 v3.2）
# ============================================================

DIMENSIONS = {
    "ai_fluency": "AI流利度",
    "human_ai_judgment": "人机判断力",
    "architecture_design": "架构设计力",
    "hybrid_orchestration": "混合编排力",
    "cognitive_depth": "认知深度",
    "problem_modeling": "问题建模能力",
}

LEVEL_THRESHOLDS = [
    (4, 7, "L1", "AI 工具使用者"),
    (8, 11, "L2", "AI 协作者"),
    (12, 14, "L3", "AI 架构者"),
    (15, 16, "L4", "AI 战略者"),
]

L4_MANDATORY = {
    "architecture_design": 3.0,
    "human_ai_judgment": 3.0,
}

# ============================================================
# 校验函数
# ============================================================

def validate_scores(scores: dict) -> list:
    """校验维度分数的合法性和一致性，返回校验报告列表。"""
    report = []

    # 1. 检查必需维度
    missing = set(DIMENSIONS.keys()) - set(scores.keys())
    if missing:
        report.append(f"❌ 缺少维度: {', '.join(missing)}")
        return report

    # 2. 检查分数范围
    for key, name in DIMENSIONS.items():
        val = scores[key]
        if not isinstance(val, (int, float)):
            report.append(f"❌ {name} 不是数字: {val}")
        elif val < 1 or val > 4:
            report.append(f"❌ {name} 超出范围 [1,4]: {val}")
        else:
            report.append(f"✅ {name}: {val} (有效)")

    # 3. 计算综合得分
    avg = sum(scores[k] for k in DIMENSIONS) / 6
    composite = avg * 4
    report.append(f"\n📊 能力平均分: {avg:.2f}")
    report.append(f"📊 综合得分: {composite:.1f} (满分16)")

    # 4. 定级
    level = None
    level_name = None
    for low, high, lvl, name in LEVEL_THRESHOLDS:
        if low <= round(composite) <= high:
            level = lvl
            level_name = name
            break

    if level:
        report.append(f"🏷️  级别: {level} · {level_name}")
    else:
        report.append(f"⚠️  综合得分 {composite:.1f} 不在任何区间内，边界候选人")

    # 5. 评分一致性检验
    if composite >= 13:
        report.append(f"\n⚠️  【高分触发】综合得分≥13，必须输出置信度说明")
        report.append("   → 请说明：哪些维度证据充分？哪些维度存在不确定性？")
    elif composite <= 7:
        report.append(f"\n⚠️  【低分触发】综合得分≤7，必须输出置信度说明")
        report.append("   → 请说明：是否有信息不足的情况？是否建议补充面试？")

    # 6. 非均衡检测
    max_dim = max(scores, key=scores.get)
    min_dim = min(scores, key=scores.get)
    diff = scores[max_dim] - scores[min_dim]
    if diff >= 2:
        report.append(f"\n⚠️  【非均衡型】{DIMENSIONS[max_dim]}({scores[max_dim]}) vs {DIMENSIONS[min_dim]}({scores[min_dim]}) 分差={diff:.1f}")
        report.append("   → 必须标注非均衡型并解释原因")

    # 7. L4 强制校验
    if level == "L4":
        report.append(f"\n🔒 【L4强制校验】")
        for dim, threshold in L4_MANDATORY.items():
            if scores[dim] < threshold:
                report.append(f"   ❌ {DIMENSIONS[dim]}={scores[dim]} < {threshold}，L4 不成立，应降为 L3")
                report.append(f"   → L4 必须 {DIMENSIONS[dim]}≥{threshold}")
            else:
                report.append(f"   ✅ {DIMENSIONS[dim]}={scores[dim]} ≥ {threshold}")

    # 8. 双乘数计算（如果提供了环境和杠杆参数）
    return report


def compute_weighted(avg: float, env: str = "medium", leverage: str = "medium", growth: str = "medium") -> dict:
    """计算双乘数加权和成长速度调整。"""
    env_map = {"low": 0.7, "medium": 1.0, "high": 1.2}
    lev_map = {"low": 0.7, "medium": 1.0, "high": 1.3}
    growth_map = {"low": -0.5, "medium": 0, "high": 0.5}

    env_factor = env_map.get(env, 1.0)
    lev_factor = lev_map.get(leverage, 1.0)
    growth_adj = growth_map.get(growth, 0)

    weighted = avg * env_factor * lev_factor + growth_adj
    weighted_composite = weighted * 4

    # 定级
    level = None
    level_name = None
    # 加权分封顶/保底处理
    if weighted_composite >= 15:
        level = "L4"
        level_name = "AI 战略者"
    elif weighted_composite < 4:
        level = "L1"
        level_name = "AI 工具使用者"
        weighted_composite = max(weighted_composite, 4)  # 保底显示
    else:
        for low, high, lvl, name in LEVEL_THRESHOLDS:
            if low <= round(weighted_composite) <= high:
                level = lvl
                level_name = name
                break

    return {
        "env_factor": env_factor,
        "lev_factor": lev_factor,
        "growth_adj": growth_adj,
        "weighted_avg": weighted,
        "weighted_composite": weighted_composite,
        "level": level,
        "level_name": level_name,
    }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="ai-talent-grader 评分一致性校验器 v3.4")
    parser.add_argument("--scores", type=str, required=True, help="六维度分数（JSON 字符串或文件路径）")
    parser.add_argument("--env", choices=["low", "medium", "high"], default="medium", help="环境复杂度")
    parser.add_argument("--leverage", choices=["low", "medium", "high"], default="medium", help="个人杠杆率")
    parser.add_argument("--growth", choices=["low", "medium", "high"], default="medium", help="成长速度")
    args = parser.parse_args()

    # 解析分数
    try:
        scores = json.loads(args.scores)
    except json.JSONDecodeError:
        # 尝试作为文件路径读取
        try:
            with open(args.scores, "r") as f:
                scores = json.load(f)
        except Exception:
            print(f"❌ 无法解析分数: {args.scores}", file=sys.stderr)
            sys.exit(1)

    # 执行校验
    print("=" * 60)
    print("🔍 ai-talent-grader 评分一致性校验报告 v3.4")
    print("=" * 60)
    report = validate_scores(scores)
    for line in report:
        print(line)

    # 双乘数计算
    avg = sum(scores[k] for k in DIMENSIONS) / 6
    weighted = compute_weighted(avg, args.env, args.leverage, args.growth)

    print(f"\n📐 双乘数加权：")
    print(f"   环境复杂度: ×{weighted['env_factor']}")
    print(f"   个人杠杆率: ×{weighted['lev_factor']}")
    print(f"   成长速度调整: {weighted['growth_adj']:+.1f}")
    print(f"   加权能力平均分: {weighted['weighted_avg']:.2f}")
    print(f"   加权综合得分: {weighted['weighted_composite']:.1f}")
    if weighted["level"]:
        print(f"   加权级别: {weighted['level']} · {weighted['level_name']}")
    else:
        print(f"   ⚠️  加权得分不在标准区间内")

    print("\n" + "=" * 60)
    print("✅ 校验完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
