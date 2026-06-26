#!/usr/bin/env python3
"""
漏斗分析脚本 - 计算各阶段转化率，输出分析报告
用法:
  python analyze-funnel.py analyze --input data.csv [--days 30]
  python analyze-funnel.py compare --input data.csv --period1 2026-03 --period2 2026-02
  python analyze-funnel.py export --input data.csv --format html --output report.html
"""

import argparse
import sys
from datetime import datetime, timedelta

try:
    import pandas as pd
except ImportError:
    print("缺少依赖: pip install pandas")
    sys.exit(1)

STAGE_ORDER = ["lead", "qualification", "demo", "negotiation", "closed_won", "closed_lost"]
STAGE_LABELS = {
    "lead": "初次接触",
    "qualification": "需求确认",
    "demo": "方案演示",
    "negotiation": "报价谈判",
    "closed_won": "成交",
    "closed_lost": "流失",
}

# 行业健康转化率基准（各阶段下限）
BENCHMARKS = {
    "SaaS":  {"lead→qualification": 0.40, "qualification→demo": 0.50, "demo→negotiation": 0.60, "negotiation→closed_won": 0.20},
    "电商":  {"lead→qualification": 0.30, "qualification→demo": 0.60, "demo→negotiation": 0.70, "negotiation→closed_won": 0.30},
    "B2B":   {"lead→qualification": 0.20, "qualification→demo": 0.40, "demo→negotiation": 0.50, "negotiation→closed_won": 0.15},
}


def load_data(path: str) -> pd.DataFrame:
    """加载 CSV/Excel 数据，自动识别格式"""
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    # 标准化列名（兼容中英文）
    col_map = {}
    for col in df.columns:
        lc = col.lower().strip()
        if lc in ("stage", "阶段", "沟通阶段"):
            col_map[col] = "stage"
        elif lc in ("date", "日期", "时间", "create_time"):
            col_map[col] = "date"
        elif lc in ("result", "结果", "最终结果"):
            col_map[col] = "result"
        elif lc in ("customer_id", "客户id", "客户编号"):
            col_map[col] = "customer_id"
    df = df.rename(columns=col_map)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def compute_funnel(df: pd.DataFrame) -> dict:
    """计算漏斗各阶段人数和转化率"""
    counts = {}
    for stage in STAGE_ORDER:
        counts[stage] = len(df[df["stage"] == stage]) if "stage" in df.columns else 0

    # 如果有 result 列，用 result 判断 closed_won/closed_lost
    if "result" in df.columns:
        counts["closed_won"] = len(df[df["result"].str.contains("成交|won|closed_won", case=False, na=False)])
        counts["closed_lost"] = len(df[df["result"].str.contains("流失|lost|closed_lost", case=False, na=False)])

    transitions = [
        ("lead", "qualification"),
        ("qualification", "demo"),
        ("demo", "negotiation"),
        ("negotiation", "closed_won"),
    ]
    rates = {}
    for src, dst in transitions:
        key = f"{src}→{dst}"
        if counts.get(src, 0) > 0:
            rates[key] = counts.get(dst, 0) / counts[src]
        else:
            rates[key] = None
    return {"counts": counts, "rates": rates}


def print_funnel_report(funnel: dict, industry: str = None):
    """打印漏斗分析报告"""
    counts = funnel["counts"]
    rates = funnel["rates"]
    benchmark = BENCHMARKS.get(industry, {}) if industry else {}

    print("\n" + "=" * 50)
    print("📊 销售漏斗分析报告")
    print("=" * 50)
    for stage in STAGE_ORDER:
        label = STAGE_LABELS.get(stage, stage)
        n = counts.get(stage, 0)
        print(f"  {label:8s}: {n:4d} 条")

    print("\n📈 各阶段转化率")
    print("-" * 40)
    for key, rate in rates.items():
        if rate is None:
            print(f"  {key}: 数据不足")
            continue
        pct = f"{rate*100:.1f}%"
        bench = benchmark.get(key)
        if bench and rate < bench:
            flag = f"⚠️  低于基准({bench*100:.0f}%)"
        else:
            flag = "✅"
        print(f"  {key}: {pct:6s} {flag}")

    total_lead = counts.get("lead", 0)
    total_won = counts.get("closed_won", 0)
    if total_lead > 0:
        overall = total_won / total_lead
        print(f"\n🎯 整体转化率: {overall*100:.1f}%  ({total_won}/{total_lead})")
    print("=" * 50)


def cmd_analyze(args):
    df = load_data(args.input)
    if args.days and "date" in df.columns:
        cutoff = datetime.now() - timedelta(days=args.days)
        df = df[df["date"] >= cutoff]
        print(f"筛选最近 {args.days} 天数据，共 {len(df)} 条")
    funnel = compute_funnel(df)
    print_funnel_report(funnel, industry=getattr(args, "industry", None))


def cmd_compare(args):
    df = load_data(args.input)
    results = {}
    for period_str in [args.period1, args.period2]:
        if "date" in df.columns:
            sub = df[df["date"].dt.to_period("M").astype(str) == period_str]
        else:
            sub = df
        results[period_str] = compute_funnel(sub)
        print(f"\n【{period_str}】")
        print_funnel_report(results[period_str])

    # 对比转化率变化
    print("\n📊 转化率对比（period1 vs period2）")
    print("-" * 40)
    r1 = results[args.period1]["rates"]
    r2 = results[args.period2]["rates"]
    for key in r1:
        v1 = r1.get(key)
        v2 = r2.get(key)
        if v1 is not None and v2 is not None:
            delta = (v1 - v2) * 100
            arrow = "↑" if delta > 0 else "↓"
            print(f"  {key}: {v2*100:.1f}% → {v1*100:.1f}%  {arrow}{abs(delta):.1f}pp")


def cmd_export(args):
    df = load_data(args.input)
    funnel = compute_funnel(df)
    counts = funnel["counts"]
    rates = funnel["rates"]

    if args.format == "html":
        rows = ""
        for stage in STAGE_ORDER:
            label = STAGE_LABELS.get(stage, stage)
            n = counts.get(stage, 0)
            rows += f"<tr><td>{label}</td><td>{n}</td></tr>\n"
        rate_rows = ""
        for key, rate in rates.items():
            pct = f"{rate*100:.1f}%" if rate is not None else "N/A"
            rate_rows += f"<tr><td>{key}</td><td>{pct}</td></tr>\n"
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>漏斗分析报告</title>
<style>body{{font-family:sans-serif;padding:20px}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #ddd;padding:8px;text-align:left}}th{{background:#f2f2f2}}</style>
</head><body>
<h1>销售漏斗分析报告</h1>
<h2>各阶段数量</h2>
<table><tr><th>阶段</th><th>数量</th></tr>{rows}</table>
<h2>转化率</h2>
<table><tr><th>路径</th><th>转化率</th></tr>{rate_rows}</table>
</body></html>"""
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ 报告已导出: {args.output}")
    else:
        print_funnel_report(funnel)
        print(f"（纯文本模式，如需 HTML 请指定 --format html）")


def main():
    parser = argparse.ArgumentParser(description="销售漏斗分析工具")
    sub = parser.add_subparsers(dest="cmd")

    p_analyze = sub.add_parser("analyze", help="分析漏斗数据")
    p_analyze.add_argument("--input", required=True, help="数据文件路径 (CSV/Excel)")
    p_analyze.add_argument("--days", type=int, help="只分析最近 N 天")
    p_analyze.add_argument("--industry", choices=["SaaS", "电商", "B2B"], help="行业基准对比")

    p_compare = sub.add_parser("compare", help="对比两个时间段")
    p_compare.add_argument("--input", required=True)
    p_compare.add_argument("--period1", required=True, help="格式: 2026-03")
    p_compare.add_argument("--period2", required=True, help="格式: 2026-02")

    p_export = sub.add_parser("export", help="导出报告")
    p_export.add_argument("--input", required=True)
    p_export.add_argument("--format", choices=["html", "text"], default="html")
    p_export.add_argument("--output", default="funnel-report.html")

    args = parser.parse_args()
    if args.cmd == "analyze":
        cmd_analyze(args)
    elif args.cmd == "compare":
        cmd_compare(args)
    elif args.cmd == "export":
        cmd_export(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
