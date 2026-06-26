#!/usr/bin/env python3
"""
话术提取脚本 - 从对话记录中挖掘高转化话术
用法:
  python extract-scripts.py extract --input data.csv [--top 10]
  python extract-scripts.py rank --input data.csv
  python extract-scripts.py recommend --input data.csv --scenario price_objection
"""

import argparse
import sys
import re
from collections import Counter

try:
    import pandas as pd
except ImportError:
    print("缺少依赖: pip install pandas")
    sys.exit(1)

SCENARIOS = {
    "price_objection": ["太贵", "贵了", "价格", "预算", "费用", "cost", "price"],
    "competitor": ["竞品", "对比", "其他家", "XX公司", "competitor"],
    "delay": ["再考虑", "考虑一下", "回头", "下次", "不急", "think about"],
    "demo": ["演示", "demo", "试用", "看看效果", "功能"],
    "closing": ["签合同", "下单", "付款", "合作", "确认"],
}

SCENARIO_LABELS = {
    "price_objection": "价格异议",
    "competitor": "竞品对比",
    "delay": "拖延决策",
    "demo": "方案演示",
    "closing": "临门一脚",
}


def load_data(path: str) -> pd.DataFrame:
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    col_map = {}
    for col in df.columns:
        lc = col.lower().strip()
        if lc in ("script", "话术", "话术内容", "content", "沟通内容"):
            col_map[col] = "script"
        elif lc in ("result", "结果", "最终结果"):
            col_map[col] = "result"
        elif lc in ("stage", "阶段", "沟通阶段"):
            col_map[col] = "stage"
        elif lc in ("feedback", "客户反馈", "反馈"):
            col_map[col] = "feedback"
        elif lc in ("sales_id", "销售id", "销售编号"):
            col_map[col] = "sales_id"
    return df.rename(columns=col_map)


def is_won(result_val) -> bool:
    if pd.isna(result_val):
        return False
    return bool(re.search(r"成交|won|closed_won|✅", str(result_val), re.IGNORECASE))


def detect_scenario(text: str) -> str:
    """检测话术所属场景"""
    text_lower = str(text).lower()
    for scenario, keywords in SCENARIOS.items():
        if any(kw in text_lower for kw in keywords):
            return scenario
    return "general"


def cmd_extract(args):
    df = load_data(args.input)
    if "script" not in df.columns:
        print("❌ 未找到话术列，请确保数据包含 '话术内容' 或 'script' 列")
        sys.exit(1)

    # 只取成交记录
    if "result" in df.columns:
        won_df = df[df["result"].apply(is_won)]
    else:
        won_df = df
        print("⚠️  未找到结果列，将分析全部记录")

    print(f"\n✅ 成交记录: {len(won_df)} 条（共 {len(df)} 条）")

    # 提取所有话术片段（按句号/换行分割）
    all_scripts = []
    for _, row in won_df.iterrows():
        text = str(row.get("script", ""))
        sentences = re.split(r"[。！？\n]", text)
        for s in sentences:
            s = s.strip()
            if len(s) > 10:  # 过滤太短的片段
                all_scripts.append(s)

    # 统计高频话术
    counter = Counter(all_scripts)
    top_scripts = counter.most_common(args.top)

    print(f"\n🏆 Top {args.top} 高频话术（来自成交记录）")
    print("=" * 60)
    for i, (script, count) in enumerate(top_scripts, 1):
        scenario = detect_scenario(script)
        label = SCENARIO_LABELS.get(scenario, "通用")
        print(f"\n{i}. [{label}] 出现 {count} 次")
        print(f"   {script[:100]}{'...' if len(script) > 100 else ''}")
    print("=" * 60)


def cmd_rank(args):
    df = load_data(args.input)
    if "script" not in df.columns or "result" not in df.columns:
        print("❌ 需要 '话术内容' 和 '结果' 两列")
        sys.exit(1)

    # 按话术统计转化率
    script_stats = {}
    for _, row in df.iterrows():
        text = str(row.get("script", "")).strip()
        if not text or len(text) < 10:
            continue
        won = is_won(row.get("result"))
        if text not in script_stats:
            script_stats[text] = {"total": 0, "won": 0}
        script_stats[text]["total"] += 1
        if won:
            script_stats[text]["won"] += 1

    # 过滤样本量太少的
    ranked = [
        (s, v["won"] / v["total"], v["total"])
        for s, v in script_stats.items()
        if v["total"] >= 3
    ]
    ranked.sort(key=lambda x: x[1], reverse=True)

    print(f"\n📊 话术转化率排行（样本量 ≥ 3）")
    print("=" * 60)
    for i, (script, rate, total) in enumerate(ranked[:20], 1):
        scenario = detect_scenario(script)
        label = SCENARIO_LABELS.get(scenario, "通用")
        print(f"\n{i}. [{label}] 转化率 {rate*100:.0f}%（{int(rate*total)}/{total}）")
        print(f"   {script[:100]}{'...' if len(script) > 100 else ''}")
    print("=" * 60)


def cmd_recommend(args):
    df = load_data(args.input)
    scenario = args.scenario

    if scenario not in SCENARIOS:
        print(f"❌ 未知场景: {scenario}")
        print(f"可用场景: {', '.join(SCENARIOS.keys())}")
        sys.exit(1)

    keywords = SCENARIOS[scenario]
    label = SCENARIO_LABELS.get(scenario, scenario)

    # 筛选包含场景关键词的话术
    if "script" in df.columns:
        mask = df["script"].apply(
            lambda x: any(kw in str(x).lower() for kw in keywords)
        )
        scenario_df = df[mask]
    else:
        scenario_df = df

    if "result" in df.columns:
        won_df = scenario_df[scenario_df["result"].apply(is_won)]
    else:
        won_df = scenario_df

    print(f"\n🎯 场景：{label}")
    print(f"   匹配记录: {len(scenario_df)} 条，其中成交: {len(won_df)} 条")

    if len(won_df) == 0:
        print("   暂无足够的成交数据，推荐使用行业模板（见 references/industry-templates.md）")
        return

    # 提取成交话术
    scripts = []
    for _, row in won_df.iterrows():
        text = str(row.get("script", "")).strip()
        if len(text) > 10:
            scripts.append(text)

    counter = Counter(scripts)
    print(f"\n💡 推荐话术（基于 {len(won_df)} 条成交记录）")
    print("=" * 60)
    for i, (script, count) in enumerate(counter.most_common(5), 1):
        print(f"\n{i}. 出现 {count} 次")
        print(f"   {script[:150]}{'...' if len(script) > 150 else ''}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="话术提取与推荐工具")
    sub = parser.add_subparsers(dest="cmd")

    p_extract = sub.add_parser("extract", help="提取高频话术")
    p_extract.add_argument("--input", required=True)
    p_extract.add_argument("--top", type=int, default=10)

    p_rank = sub.add_parser("rank", help="按转化率排序话术")
    p_rank.add_argument("--input", required=True)

    p_recommend = sub.add_parser("recommend", help="推荐指定场景话术")
    p_recommend.add_argument("--input", required=True)
    p_recommend.add_argument(
        "--scenario",
        required=True,
        choices=list(SCENARIOS.keys()),
        help=f"场景: {', '.join(SCENARIOS.keys())}",
    )

    args = parser.parse_args()
    if args.cmd == "extract":
        cmd_extract(args)
    elif args.cmd == "rank":
        cmd_rank(args)
    elif args.cmd == "recommend":
        cmd_recommend(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
