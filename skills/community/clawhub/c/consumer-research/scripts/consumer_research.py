#!/usr/bin/env python3
"""
消费者调研脚本
功能：通过web搜索获取消费者洞察和需求分析
"""

import os
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "consumer_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def search_consumer_profile(target_group: str) -> dict:
    """
    搜索目标人群画像

    Args:
        target_group: 目标人群描述

    Returns:
        搜索指令
    """
    search_queries = [
        f"{target_group} 消费者画像 特征",
        f"{target_group} 人群 行为数据",
        f"{target_group} 消费偏好 趋势",
        f"{target_group} 市场规模 用户规模"
    ]

    return {
        "action": "web_search",
        "target_group": target_group,
        "search_queries": search_queries,
        "note": "请使用web_search工具执行以上查询"
    }


def search_needs_analysis(product_category: str, target_segment: str = None) -> dict:
    """
    搜索需求分析

    Args:
        product_category: 产品品类
        target_segment: 目标细分人群

    Returns:
        搜索指令
    """
    segment = target_segment or product_category
    search_queries = [
        f"{segment} 消费者需求 痛点",
        f"{product_category} 用户 调研 报告",
        f"{segment} 购买决策 因素",
        f"{product_category} 满意度 调查"
    ]

    return {
        "action": "web_search",
        "product_category": product_category,
        "target_segment": segment,
        "search_queries": search_queries,
        "note": "请使用web_search工具执行以上查询"
    }


def save_profile_data(target_group: str, data: dict):
    """保存人群画像数据"""
    data_file = DATA_DIR / "profile_data.json"

    existing_data = {}
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)

    existing_data[target_group] = {
        "data": data,
        "updated_at": datetime.now().isoformat()
    }

    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"人群画像数据已保存至: {data_file}")


def save_needs_data(product_category: str, needs: list):
    """保存需求分析数据"""
    data_file = DATA_DIR / "needs_analysis.json"

    existing_data = {}
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)

    existing_data[product_category] = {
        "needs": needs,
        "updated_at": datetime.now().isoformat()
    }

    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"需求分析数据已保存至: {data_file}")


def generate_profile_report(profile_data: dict = None, needs_data: dict = None,
                          target_group: str = None) -> str:
    """生成人群画像报告"""
    report = ["# 消费者调研报告\n"]
    report.append(f"报告日期：{datetime.now().strftime('%Y-%m-%d')}\n")
    report.append("=" * 50 + "\n")

    if profile_data:
        report.append("## 一、人群概况\n")
        for key, value in profile_data.items():
            report.append(f"- {key}：{value}\n")
        report.append("")

    if needs_data:
        report.append("## 二、需求分析\n")
        for need in needs_data:
            report.append(f"### {need.get('name', '需求')}\n")
            report.append(f"- 重要性：{need.get('importance', 'N/A')}\n")
            report.append(f"- 描述：{need.get('description', 'N/A')}\n\n")

    report.append("## 三、数据来源\n")
    report.append("- CBNData：https://www.cbndata.com\n")
    report.append("- QuestMobile：https://www.questmobile.com\n")
    report.append("- 艾瑞咨询：https://www.iresearch.cn\n")

    return "".join(report)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="消费者调研")
    parser.add_argument("--target", "-t", help="目标人群描述")
    parser.add_argument("--category", "-c", help="产品品类")
    parser.add_argument("--action", "-a", choices=["search", "report"],
                       default="search", help="操作类型")
    parser.add_argument("--output", "-o", default="data/consumer_data/report.md",
                       help="输出报告")
    args = parser.parse_args()

    print("=" * 50)
    print("消费者调研")
    print("=" * 50)

    if args.action == "search":
        if args.target:
            print("\n请使用 web_search 工具执行以下搜索：\n")
            result = search_consumer_profile(args.target)
            for query in result["search_queries"]:
                print(f'  web_search(query="{query}")')
            print()

        if args.category:
            print(f"\n【{args.category} 需求分析】")
            result = search_needs_analysis(args.category, args.target)
            for query in result["search_queries"]:
                print(f'  web_search(query="{query}")')

    elif args.action == "report":
        # 加载已有数据
        profile_file = DATA_DIR / "profile_data.json"
        needs_file = DATA_DIR / "needs_analysis.json"

        profile_data = {}
        needs_data = []

        if profile_file.exists():
            with open(profile_file, "r", encoding="utf-8") as f:
                profile_data = json.load(f)

        if needs_file.exists():
            with open(needs_file, "r", encoding="utf-8") as f:
                needs_data = json.load(f)

        report = generate_profile_report(
            profile_data.get(args.target or "general", {}).get("data", {}),
            needs_data.get(args.category, {}).get("needs", []),
            args.target
        )

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"报告已生成: {output_path}")


if __name__ == "__main__":
    main()
