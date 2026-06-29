#!/usr/bin/env python3
"""
ranking_matcher.py — 位次法匹配引擎

基于考生位次，匹配历年高校投档数据，计算录取概率。
支持从JSON/admissions数据文件中读取历年录取信息。

用法:
  python ranking_matcher.py --rank 4500 --province hubei \
    --subject 物理类 --admissions references/admission_sample.json

输出: JSON格式的匹配结果，含冲/稳/保分类和录取概率
"""

import json
import argparse
import sys
from pathlib import Path


def compute_admission_probability(current_rank: int, hist_min_ranks: list[int]) -> float:
    """
    基于历年最低录取位次计算录取概率。

    算法:
    1. 取近3年最低录取位次的均值作为参考
    2. 如果考生位次 < 历年最低录取位次均值 → 高概率
    3. 用位次差距和位次波动计算概率得分

    返回: 0.0~1.0 的概率值
    """
    if not hist_min_ranks:
        return 0.5

    avg_rank = sum(hist_min_ranks) / len(hist_min_ranks)
    rank_std = 0
    if len(hist_min_ranks) > 1:
        mean = avg_rank
        rank_std = (sum((r - mean) ** 2 for r in hist_min_ranks) / len(hist_min_ranks)) ** 0.5

    # 位次差距（正值=考生排位更高/数字更小，负值=考生排位更低/数字更大）
    rank_diff_pct = (avg_rank - current_rank) / avg_rank * 100

    # 使用sigmoid-like函数映射到位次概率
    if rank_diff_pct > 5:
        # 考生位次明显领先 → 高录取概率
        prob = 0.85 + min(rank_diff_pct / 100, 0.14)  # max ~0.99
    elif rank_diff_pct > 0:
        prob = 0.6 + rank_diff_pct / 25  # 0.6~0.85
    elif rank_diff_pct > -5:
        prob = 0.5 + rank_diff_pct / 25  # 0.3~0.6
    elif rank_diff_pct > -15:
        prob = 0.2 + (rank_diff_pct + 5) / 40  # 0.1~0.3
    else:
        prob = max(0.01, 0.1 + rank_diff_pct / 200)  # < 0.1

    return round(max(0.01, min(0.99, prob)), 4)


def classify_risk(prob: float) -> str:
    """将录取概率映射到冲/稳/保"""
    if prob < 0.50:
        return "冲"
    elif prob < 0.80:
        return "稳"
    else:
        return "保"


def match_by_rank(current_rank: int, admissions: list[dict], province: str, subject: str) -> list[dict]:
    """
    位次法匹配主函数。

    参数:
      current_rank: 考生今年的省排位
      admissions: 历年录取数据列表
      province: 省份代码
      subject: 科类

    返回: 排序后的匹配结果列表
    """
    results = []

    for adm in admissions:
        # 过滤省份和科类
        if adm.get("province", "").lower() != province.lower():
            continue
        if adm.get("subject", "") != subject:
            continue

        min_ranks = adm.get("hist_min_ranks", [])
        if not min_ranks:
            continue

        prob = compute_admission_probability(current_rank, min_ranks)
        risk = classify_risk(prob)

        results.append({
            "university_id": adm.get("university_id", ""),
            "university_name": adm.get("university_name", ""),
            "major_group_code": adm.get("major_group_code", ""),
            "major_group_name": adm.get("major_group_name", ""),
            "hist_min_ranks": min_ranks,
            "hist_min_scores": adm.get("hist_min_scores", []),
            "admission_probability": prob,
            "risk_level": risk,
            "majors_in_group": adm.get("majors_in_group", []),
        })

    # 按录取概率降序排列（概率高的排后面，保底靠后）
    results.sort(key=lambda x: x["admission_probability"], reverse=True)
    return results


def generate_sample_admissions() -> list[dict]:
    """生成示例录取数据（实际使用时替换为搜索到的真实数据）"""
    return [
        {
            "university_id": "10486",
            "university_name": "武汉大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1048601",
            "major_group_name": "物理+化学组",
            "hist_min_ranks": [4100, 4200, 4350],
            "hist_min_scores": [646, 645, 643],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 120,
            "majors_in_group": ["计算机科学与技术", "软件工程", "人工智能", "电子信息工程"]
        },
        {
            "university_id": "10487",
            "university_name": "华中科技大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1048701",
            "major_group_name": "物理+化学组",
            "hist_min_ranks": [4200, 4300, 4400],
            "hist_min_scores": [648, 644, 642],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 150,
            "majors_in_group": ["计算机科学与技术", "光电信息科学与工程", "机械设计制造及其自动化"]
        },
        {
            "university_id": "10610",
            "university_name": "四川大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1061001",
            "major_group_name": "物理+化学组",
            "hist_min_ranks": [8500, 8700, 8600],
            "hist_min_scores": [628, 626, 625],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 80,
            "majors_in_group": ["计算机科学与技术", "软件工程", "临床医学"]
        },
        {
            "university_id": "10701",
            "university_name": "西安电子科技大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1070101",
            "major_group_name": "物理+不限组",
            "hist_min_ranks": [7800, 7900, 8100],
            "hist_min_scores": [635, 632, 630],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 60,
            "majors_in_group": ["通信工程", "电子信息工程", "计算机科学与技术"]
        },
        {
            "university_id": "10013",
            "university_name": "北京邮电大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1001301",
            "major_group_name": "物理+不限组",
            "hist_min_ranks": [5000, 5100, 5200],
            "hist_min_scores": [640, 638, 635],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 45,
            "majors_in_group": ["通信工程", "计算机科学与技术", "网络空间安全"]
        },
        {
            "university_id": "10497",
            "university_name": "武汉理工大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1049701",
            "major_group_name": "物理+化学组",
            "hist_min_ranks": [16000, 16200, 16500],
            "hist_min_scores": [605, 602, 600],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 200,
            "majors_in_group": ["材料科学与工程", "车辆工程", "计算机科学与技术"]
        },
        {
            "university_id": "10520",
            "university_name": "中南财经政法大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1052001",
            "major_group_name": "物理+不限组",
            "hist_min_ranks": [13500, 13800, 14000],
            "hist_min_scores": [615, 612, 610],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 100,
            "majors_in_group": ["金融学", "会计学", "法学", "统计学"]
        },
        {
            "university_id": "10491",
            "university_name": "中国地质大学(武汉)",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1049101",
            "major_group_name": "物理+化学组",
            "hist_min_ranks": [21000, 21500, 22000],
            "hist_min_scores": [590, 587, 585],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 180,
            "majors_in_group": ["地质学", "计算机科学与技术", "地理信息科学"]
        },
        {
            "university_id": "10358",
            "university_name": "中国科学技术大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1035801",
            "major_group_name": "物理+化学组",
            "hist_min_ranks": [900, 850, 800],
            "hist_min_scores": [675, 678, 676],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 30,
            "majors_in_group": ["物理学", "计算机科学与技术", "数学与应用数学", "人工智能"]
        },
        {
            "university_id": "10614",
            "university_name": "电子科技大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1061401",
            "major_group_name": "物理+不限组",
            "hist_min_ranks": [5500, 5600, 5700],
            "hist_min_scores": [638, 635, 632],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 50,
            "majors_in_group": ["电子信息工程", "通信工程", "计算机科学与技术", "微电子科学与工程"]
        },
        {
            "university_id": "10558",
            "university_name": "中山大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1055801",
            "major_group_name": "物理+化学组",
            "hist_min_ranks": [5000, 5200, 5300],
            "hist_min_scores": [642, 638, 635],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 55,
            "majors_in_group": ["临床医学", "计算机科学与技术", "数据科学与大数据技术"]
        },
        {
            "university_id": "10422",
            "university_name": "山东大学",
            "province": "hubei",
            "subject": "物理类",
            "major_group_code": "1042201",
            "major_group_name": "物理+不限组",
            "hist_min_ranks": [9500, 9800, 10000],
            "hist_min_scores": [622, 618, 615],
            "years": [2025, 2024, 2023],
            "plan_enrollment": 70,
            "majors_in_group": ["数学与应用数学", "计算机科学与技术", "自动化"]
        }
    ]


def main():
    parser = argparse.ArgumentParser(description="位次法匹配引擎")
    parser.add_argument("--rank", type=int, required=True, help="考生省排位")
    parser.add_argument("--province", type=str, required=True, help="省份代码 (如 hubei)")
    parser.add_argument("--subject", type=str, required=True, help="科类 (如 物理类)")
    parser.add_argument("--admissions", type=str, default=None, help="录取数据JSON文件路径")
    parser.add_argument("--output", type=str, default=None, help="输出JSON文件路径")

    args = parser.parse_args()

    # 加载录取数据
    if args.admissions and Path(args.admissions).exists():
        with open(args.admissions, "r", encoding="utf-8") as f:
            admissions = json.load(f)
        if isinstance(admissions, dict):
            admissions = admissions.get("admissions", [])
    else:
        print("[ranking_matcher] 未提供录取数据，使用示例数据", file=sys.stderr)
        admissions = generate_sample_admissions()

    # 执行匹配
    results = match_by_rank(args.rank, admissions, args.province, args.subject)

    # 统计
    stats = {"冲": 0, "稳": 0, "保": 0, "total": len(results)}
    for r in results:
        stats[r["risk_level"]] += 1

    output = {
        "current_rank": args.rank,
        "province": args.province,
        "subject": args.subject,
        "match_count": len(results),
        "distribution": stats,
        "matches": results
    }

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"[ranking_matcher] 结果已保存到 {args.output}")

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
