#!/usr/bin/env python3
"""
gaokao-tutor: 分数线查询脚本
用法:
  python3 score_query.py province --province 广东 --year 2024
  python3 score_query.py province --province 广东          # 近5年全部
  python3 score_query.py university --name 清华大学 --province 广东 --year 2024
  python3 score_query.py estimate --province 广东 --score 650 --category 物理类 --year 2024
  python3 score_query.py list_universities               # 列出所有大学
"""

import json
import os
import sys
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROVINCE_FILE = os.path.join(BASE, "data", "province_scores.json")
UNIVERSITY_FILE = os.path.join(BASE, "data", "university_scores.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def query_province(province, year=None):
    data = load_json(PROVINCE_FILE)
    if province not in data:
        print(f"❌ 未找到 [{province}] 的数据。")
        print(f"   已有数据的省份：{', '.join(k for k in data if not k.startswith('_'))}")
        return

    info = data[province]
    print(f"\n📊 {province} 高考分数线")
    print(f"   考试类型：{info.get('exam_type', '未知')}")
    print(f"   总分：{info.get('total_score', 750)}分")
    if info.get("note"):
        print(f"   特别说明：{info['note']}")
    print()

    years = [str(year)] if year else ["2024", "2023", "2022", "2021", "2020"]
    for y in years:
        if y in info:
            scores = info[y]
            print(f"  【{y}年】")
            for k, v in scores.items():
                print(f"    {k}：{v}分")
        else:
            print(f"  【{y}年】暂无数据")
    print()
    print("⚠️ 数据仅供参考，以当年招生考试院官方公布为准")


def query_university(name, province=None, year=None):
    data = load_json(UNIVERSITY_FILE)

    # 支持模糊匹配
    matched = [k for k in data if name in k and not k.startswith("_")]
    if not matched:
        print(f"❌ 未找到包含 [{name}] 的大学")
        print(f"   发送「大学列表」查看所有已收录大学")
        return

    for uni_name in matched:
        uni = data[uni_name]
        print(f"\n🏫 {uni_name}")
        print(f"   类型：{uni.get('tier', '未知')} | 所在地：{uni.get('location', '未知')}")
        print()

        years = [str(year)] if year else ["2024", "2023", "2022"]
        for y in years:
            if y not in uni:
                continue
            year_data = uni[y]
            print(f"  【{y}年录取分数线】")

            if province:
                # 查找匹配的省份键
                matched_keys = [k for k in year_data if province in k]
                if matched_keys:
                    for k in matched_keys:
                        print(f"    {k}：{year_data[k]}分")
                else:
                    avail = ", ".join(year_data.keys())
                    print(f"    暂无 [{province}] 数据。已有：{avail}")
            else:
                for k, v in year_data.items():
                    print(f"    {k}：{v}分")
        print()
    print("⚠️ 数据仅供参考，以当年招生办官方数据为准")


def estimate_admission(province, score, category, year="2024"):
    """根据分数估算可报考的大学层次"""
    prov_data = load_json(PROVINCE_FILE)
    uni_data = load_json(UNIVERSITY_FILE)

    if province not in prov_data:
        print(f"❌ 未找到 [{province}] 的省份数据")
        return

    # 找省控线
    prov_year = prov_data[province].get(str(year), {})
    ctrl_line = None
    for k, v in prov_year.items():
        if "本科一" in k or "本科" in k:
            if category and category[:2] in k:
                ctrl_line = v
                break
            elif ctrl_line is None:
                ctrl_line = v

    print(f"\n🎯 录取预估 — {province} {year}年 {score}分 ({category})")
    print(f"   省控一本线：{ctrl_line or '未知'}分")
    print(f"   超出省线：{score - ctrl_line if ctrl_line else '?'}分")
    print()

    # 按分差分层
    reach = []     # 冲 (score+5 ~ score+20)
    match = []     # 稳 (score-5 ~ score+5)
    safe = []      # 保 (score-20 ~ score-5)

    key_suffix = f"_{province}_{category}" if category else f"_{province}"

    for uni_name, uni in uni_data.items():
        if uni_name.startswith("_"):
            continue
        year_data = uni.get(str(year), {})

        # 查找匹配的键
        uni_score = None
        for k, v in year_data.items():
            if province in k:
                if category and category[:2] in k:
                    uni_score = v
                    break
                elif uni_score is None:
                    uni_score = v

        if uni_score is None:
            continue

        diff = uni_score - score
        entry = f"{uni_name}（{uni_score}分，差{abs(diff)}分）"
        if 5 <= diff <= 25:
            reach.append((diff, entry))
        elif -5 <= diff < 5:
            match.append((abs(diff), entry))
        elif -20 <= diff < -5:
            safe.append((abs(diff), entry))

    reach.sort()
    match.sort()
    safe.sort()

    if reach:
        print("【冲刺院校】（分数线高于你5-25分，有一定风险）")
        for _, e in reach[:5]:
            print(f"  · {e}")
    else:
        print("【冲刺院校】数据库中暂无匹配院校")

    print()
    if match:
        print("【稳妥院校】（分数线与你相近，录取概率较高）")
        for _, e in match[:5]:
            print(f"  · {e}")
    else:
        print("【稳妥院校】数据库中暂无匹配院校")

    print()
    if safe:
        print("【保底院校】（分数线低于你5-20分，安全选择）")
        for _, e in safe[:5]:
            print(f"  · {e}")
    else:
        print("【保底院校】数据库中暂无匹配院校")

    print()
    print("⚠️ 以上仅为参考，建议结合当年一分一段表和招生计划综合判断")
    print("   最终志愿填报请以当年官方数据为准")


def list_universities():
    data = load_json(UNIVERSITY_FILE)
    unis = [(k, v) for k, v in data.items() if not k.startswith("_")]
    print(f"\n🏫 已收录 {len(unis)} 所高校：\n")
    for name, info in unis:
        print(f"  · {name}（{info.get('tier', '')} | {info.get('location', '')}）")


def main():
    parser = argparse.ArgumentParser(description="高考分数线查询工具")
    subparsers = parser.add_subparsers(dest="command")

    # 省控线查询
    p = subparsers.add_parser("province", help="查询省控分数线")
    p.add_argument("--province", required=True)
    p.add_argument("--year", type=int, default=None)

    # 大学录取线查询
    u = subparsers.add_parser("university", help="查询大学录取分数线")
    u.add_argument("--name", required=True)
    u.add_argument("--province", default=None)
    u.add_argument("--year", type=int, default=None)

    # 录取预估
    e = subparsers.add_parser("estimate", help="根据分数预估可报院校")
    e.add_argument("--province", required=True)
    e.add_argument("--score", type=int, required=True)
    e.add_argument("--category", default="物理类", help="科类：物理类/历史类/理科/文科")
    e.add_argument("--year", type=int, default=2024)

    # 大学列表
    subparsers.add_parser("list_universities", help="列出所有收录大学")

    args = parser.parse_args()

    if args.command == "province":
        query_province(args.province, args.year)
    elif args.command == "university":
        query_university(args.name, args.province, args.year)
    elif args.command == "estimate":
        estimate_admission(args.province, args.score, args.category, args.year)
    elif args.command == "list_universities":
        list_universities()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
