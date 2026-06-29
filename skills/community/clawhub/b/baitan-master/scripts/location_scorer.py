#!/usr/bin/env python3
"""
摆摊选址评估器 - 多维度加权评分与选址建议
用法: python location_scorer.py --traffic 8 --match 8 --competition 6 --access 7 --cost 6
"""

import argparse
import json
import sys
from typing import Dict, Any, List, Tuple


# 评估因子定义
FACTORS = {
    "traffic": {
        "name": "人流量密度",
        "weight": 0.25,
        "levels": [
            (10, "极高", "日均>10000人次（核心商圈/交通枢纽）"),
            (8, "高", "日均5000-10000人次（地铁口/大型社区入口）"),
            (6, "中", "日均2000-5000人次（社区商业街/学校门口）"),
            (4, "低", "日均1000-2000人次（普通街道）"),
            (2, "极低", "日均<1000人次（偏僻地段）"),
        ],
    },
    "match": {
        "name": "目标客群匹配度",
        "weight": 0.25,
        "levels": [
            (10, "完美匹配", "客群画像与品类完全一致"),
            (8, "高度匹配", "客群与品类高度相关"),
            (6, "中度匹配", "有一定关联但需筛选"),
            (4, "低度匹配", "关联度低"),
            (2, "不匹配", "客群与品类无关"),
        ],
    },
    "competition": {
        "name": "竞品密度（反向）",
        "weight": 0.20,
        "levels": [
            (10, "零竞品", "500米内无同类摊位"),
            (8, "低竞争", "500米内1-2家同类"),
            (6, "中竞争", "500米内3-4家同类"),
            (4, "高竞争", "500米内5-6家同类"),
            (2, "极度饱和", "500米内>6家同类"),
        ],
    },
    "access": {
        "name": "交通可达性",
        "weight": 0.15,
        "levels": [
            (10, "极佳", "近地铁站出口/公交枢纽，步行<2分钟"),
            (8, "良好", "距地铁/公交站步行<5分钟"),
            (6, "一般", "距公交站步行5-10分钟"),
            (4, "较差", "距公共交通>10分钟"),
            (2, "很差", "无明显公共交通"),
        ],
    },
    "cost": {
        "name": "经营成本",
        "weight": 0.15,
        "levels": [
            (10, "零成本", "免费摊位（政府划定）"),
            (8, "极低", "日摊位费<30元"),
            (6, "较低", "日摊位费30-60元"),
            (4, "中等", "日摊位费60-100元"),
            (2, "较高", "日摊位费>100元"),
        ],
    },
}


def score_location(
    traffic: int = 5,
    match: int = 5,
    competition: int = 5,
    access: int = 5,
    cost: int = 5,
) -> Dict[str, Any]:
    """
    多维度选址评估

    Args:
        traffic: 人流量密度得分(2/4/6/8/10)
        match: 目标客群匹配度得分(2/4/6/8/10)
        competition: 竞品密度得分(2/4/6/8/10，越高竞争越少)
        access: 交通可达性得分(2/4/6/8/10)
        cost: 经营成本得分(2/4/6/8/10，越高成本越低)
    """

    scores_input = {
        "traffic": traffic,
        "match": match,
        "competition": competition,
        "access": access,
        "cost": cost,
    }

    # 计算加权总分
    total_score = 0
    detail_scores = {}

    for key, factor in FACTORS.items():
        raw = scores_input[key]
        weighted = raw * 10 * factor["weight"]
        total_score += weighted

        # 找到对应评级
        level_desc = ""
        for score_val, level_name, description in factor["levels"]:
            if raw >= score_val:
                level_desc = f"{level_name}（{description}）"
                break

        detail_scores[key] = {
            "factor": factor["name"],
            "weight": f"{factor['weight']*100:.0f}%",
            "raw_score": raw,
            "weighted_score": round(weighted, 1),
            "level": level_desc,
        }

    total_score = round(total_score, 1)

    # 评级与建议
    if total_score >= 80:
        grade = "A - 黄金选址 🌟"
        advice = "非常适合出摊！客群匹配+低竞争，建议立即行动"
        action_items = [
            "优先锁定此位置",
            "可适当提高定价（5-10%）",
            "做好长期经营准备",
        ]
    elif total_score >= 65:
        grade = "B - 优质选址 ✅"
        advice = "条件不错，建议出摊试运营，持续观察优化"
        action_items = [
            "可出摊但需监测竞品动态",
            "优化时段选择最大化收益",
            "积累熟客建立私域",
        ]
    elif total_score >= 50:
        grade = "C - 一般选址 ⚠️"
        advice = "有一定机会但风险偏高，建议周末试水后再决定"
        action_items = [
            "只建议周末/节假日出摊",
            "做好2周内不盈利的心理准备",
            "密切关注周边摊位变化",
        ]
    elif total_score >= 35:
        grade = "D - 不建议 🚫"
        advice = "条件较差，建议寻找备选位置后再比较"
        action_items = [
            "不建议长期出摊",
            "寻找至少2个备选位置对比",
            "考虑换品类适配现有位置",
        ]
    else:
        grade = "E - 绝对避开 ⛔"
        advice = "该位置不具备商业价值，请勿在此投入"
        action_items = [
            "立即放弃此位置",
            "参考购物中心/夜市/集市开启位置搜索",
        ]

    # 星图数据（用于前端可视化）
    radar_data = {
        "labels": [FACTORS[k]["name"] for k in FACTORS],
        "values": [scores_input[k] for k in FACTORS],
        "weights": [FACTORS[k]["weight"] for k in FACTORS],
    }

    result = {
        "total_score": total_score,
        "grade": grade,
        "advice": advice,
        "action_items": action_items,
        "detail_scores": detail_scores,
        "radar_data": radar_data,
    }

    return result


def compare_locations(locations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """比较多个人选址方案"""
    results = []
    for i, loc in enumerate(locations):
        name = loc.get("name", f"位置{i+1}")
        scores = {
            "traffic": loc.get("traffic", 5),
            "match": loc.get("match", 5),
            "competition": loc.get("competition", 5),
            "access": loc.get("access", 5),
            "cost": loc.get("cost", 5),
        }
        result = score_location(**scores)
        result["name"] = name
        results.append(result)

    # 按总分排序
    results.sort(key=lambda x: x["total_score"], reverse=True)

    best = results[0] if results else None

    return {
        "locations": results,
        "best": best,
        "recommendation": f"推荐选择「{best['name']}」（{best['grade']}）" if best else "无数据",
    }


def main():
    parser = argparse.ArgumentParser(description="摆摊选址评估器")
    parser.add_argument("--traffic", type=int, default=5, help="人流量密度(2/4/6/8/10)")
    parser.add_argument("--match", type=int, default=5, help="目标客群匹配度(2/4/6/8/10)")
    parser.add_argument("--competition", type=int, default=5, help="竞品密度(2/4/6/8/10)")
    parser.add_argument("--access", type=int, default=5, help="交通可达性(2/4/6/8/10)")
    parser.add_argument("--cost", type=int, default=5, help="经营成本(2/4/6/8/10)")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    for val, name in [
        (args.traffic, "traffic"),
        (args.match, "match"),
        (args.competition, "competition"),
        (args.access, "access"),
        (args.cost, "cost"),
    ]:
        if val not in [2, 4, 6, 8, 10]:
            print(json.dumps({"error": f"{name} 必须是 2/4/6/8/10 之一，当前值: {val}"}, ensure_ascii=False))
            sys.exit(1)

    result = score_location(
        traffic=args.traffic,
        match=args.match,
        competition=args.competition,
        access=args.access,
        cost=args.cost,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print("📍 摆摊选址评估报告")
        print("=" * 50)
        print(f"\n🏆 综合得分: {result['total_score']}/100")
        print(f"📊 评级: {result['grade']}")
        print(f"💡 {result['advice']}")
        print("\n📋 各维度详情:")
        for key, detail in result["detail_scores"].items():
            bar = "█" * (detail["raw_score"] // 2) + "░" * (5 - detail["raw_score"] // 2)
            print(f"  {detail['factor']}: [{bar}] {detail['raw_score']}/10 (权重{detail['weight']})")
            print(f"    → {detail['level']}")
        print("\n🎯 行动建议:")
        for item in result["action_items"]:
            print(f"  • {item}")
        print("=" * 50)


if __name__ == "__main__":
    main()
