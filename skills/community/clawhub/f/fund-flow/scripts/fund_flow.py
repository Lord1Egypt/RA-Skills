#!/usr/bin/env python3
"""
Fund Flow — 资金流向分析工具（v1.1.0）

分析股票/板块资金流向数据：主力净流入、散户对比、
板块聚合分析、资金趋势检测、多时间维度分析、
与指数对比、资金强度评分。

用法:
    python3 scripts/fund_flow.py --file fundflow.csv
    python3 scripts/fund_flow.py --file fundflow.csv --rank
    python3 scripts/fund_flow.py --file fundflow.csv --trend
    python3 scripts/fund_flow.py --file fundflow.csv --sector --sector-col 板块
    python3 scripts/fund_flow.py --file fundflow.csv --timeframe week
    python3 scripts/fund_flow.py --file fundflow.csv --compare --index-name 沪深300
    python3 scripts/fund_flow.py --file fundflow.csv --chart
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def read_csv(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _pf(val):
    try:
        return float(str(val).replace(",", "").replace(" ", ""))
    except (ValueError, TypeError):
        return 0.0


def detect_columns(sample, hints):
    """从候选列名列表中检测存在的列。"""
    for c in hints:
        if c in sample:
            return c
    return None


# ── 资金强度评分 ────────────────────────────────────

def compute_strength_score(main_flow, retail_flow, main_ratio, persistence):
    """资金强度综合评分（0-100）。"""
    score = 50

    # 主力净流入方向
    if main_flow > 0:
        score += 15
    elif main_flow < 0:
        score -= 15

    # 主力占比
    if main_ratio > 0.6:
        score += 10
    elif main_ratio > 0.4:
        score += 5
    elif main_ratio < 0.2 and main_flow > 0:
        score -= 5

    # 持续性
    if persistence >= 3:
        score += 10
    elif persistence >= 2:
        score += 5
    elif persistence <= -3:
        score -= 10

    # 主力vs散户背离
    if main_flow > 0 and retail_flow < 0:
        score += 10
    elif main_flow < 0 and retail_flow > 0:
        score -= 10

    return max(0, min(100, score))


# ── 主力流入占比计算 ──────────────────────────────

def compute_main_ratio(main_flow, retail_flow):
    """主力资金占总资金的比率（绝对值）。"""
    total = abs(main_flow) + abs(retail_flow)
    if total == 0:
        return 0.5
    return abs(main_flow) / total


# ── 基础分析 ──────────────────────────────────────────

def analyze_flow(rows, name_col="", main_col="", retail_col="", date_col=""):
    sample = rows[0] if rows else {}

    name_c = name_col if name_col in sample else detect_columns(
        sample, ["name", "代码", "stock", "板块", "sector", "股票"])
    main_candidates = ["main_force", "mainForce", "netamount", "主力净流入",
                        "net_amount", "main_net", "big_force", "大单净流入"]
    main_c = main_col if main_col in sample else detect_columns(sample, main_candidates)
    retail_candidates = ["retail", "retailForce", "小单净流入",
                         "retail_net", "small_net", "smallForce"]
    retail_c = retail_col if retail_col in sample else detect_columns(sample, retail_candidates)
    date_candidates = ["date", "日期", "trade_date", "time"]
    date_c = date_col if date_col in sample else detect_columns(sample, date_candidates)

    by_name = defaultdict(lambda: {"count": 0, "main": 0.0, "retail": 0.0, "dates": set()})

    for row in rows:
        name = row.get(name_c, "?") if name_c else "?"
        by_name[name]["count"] += 1
        if main_c:
            by_name[name]["main"] += _pf(row.get(main_c, 0))
        if retail_c:
            by_name[name]["retail"] += _pf(row.get(retail_c, 0))
        if date_c and row.get(date_c):
            date_str = row[date_c][:10]
            by_name[name]["dates"].add(date_str)

    ranked = []
    for name, data in by_name.items():
        net = (data["main"] - data["retail"]) if (data["main"] or data["retail"]) else data["main"]
        main_ratio = compute_main_ratio(data["main"], data["retail"])
        ranked.append({
            "name": name,
            "records": data["count"],
            "active_days": len(data["dates"]),
            "main_flow": round(data["main"], 2),
            "retail_flow": round(data["retail"], 2),
            "net_flow": round(net, 2),
            "main_ratio": round(main_ratio, 3),
        })

    ranked.sort(key=lambda x: -x["net_flow"])

    total_main = sum(r["main_flow"] for r in ranked)
    total_retail = sum(r["retail_flow"] for r in ranked)

    return {
        "total_items": len(ranked),
        "total_main_flow": round(total_main, 2),
        "total_retail_flow": round(total_retail, 2),
        "detected_columns": {"name": name_c, "main": main_c, "retail": retail_c, "date": date_c},
        "rankings": ranked,
    }


# ── 资金趋势检测 ────────────────────────────────────

def detect_trend(rows, name_col, main_col, retail_col, date_col):
    """检测资金趋势：3日/5日/10日趋势方向。"""
    sample = rows[0] if rows else {}
    name_c = name_col or detect_columns(sample, ["name", "代码", "stock"])
    main_c = main_col or detect_columns(sample, ["main_force", "mainForce", "主力净流入"])
    date_c = date_col or detect_columns(sample, ["date", "日期", "trade_date"])

    if not name_c or not main_c or not date_c:
        return None

    # 按日期分组
    by_date = defaultdict(lambda: defaultdict(float))
    for row in rows:
        d = str(row.get(date_c, ""))[:10]
        n = row.get(name_c, "?")
        by_date[d][n] += _pf(row.get(main_c, 0))

    sorted_dates = sorted(by_date.keys())
    if len(sorted_dates) < 3:
        return None

    trends = {}
    for name in sorted(set(r.get(name_c, "?") for r in rows)):
        daily = []
        for d in sorted_dates:
            daily.append(by_date[d].get(name, 0))

        def trend_slice(period):
            if len(daily) < period:
                return None, 0
            recent = daily[-period:]
            avg = sum(recent) / period
            # 趋势方向
            direction = ""
            if avg > 0:
                direction = "净流入↑" if recent[-1] >= recent[-period] else "流入放缓↓"
            elif avg < 0:
                direction = "净流出↓" if recent[-1] <= recent[-period] else "流出收窄↑"
            else:
                direction = "持平→"
            return avg, direction

        t3, d3 = trend_slice(3)
        t5, d5 = trend_slice(5)
        t10, d10 = trend_slice(min(10, len(daily)))

        # 持续性（连续净流入/流出天数）
        persistence = 0
        for v in reversed(daily):
            if v > 0 and persistence >= 0:
                persistence += 1
            elif v < 0 and persistence <= 0:
                persistence -= 1
            else:
                break

        trends[name] = {
            "3day_avg": round(t3, 2) if t3 else 0,
            "3day_direction": d3,
            "5day_avg": round(t5, 2) if t5 else 0,
            "5day_direction": d5,
            "10day_avg": round(t10, 2) if t10 else 0,
            "10day_direction": d10,
            "persistence": persistence,
            "data_days": len(daily),
        }

    return trends


# ── 板块聚合分析 ────────────────────────────────────

def aggregate_sector(rows, name_col, sector_col, main_col, retail_col):
    """按板块汇总资金流向。"""
    sample = rows[0] if rows else {}
    main_c = main_col or detect_columns(sample, ["main_force", "mainForce", "主力净流入"])
    retail_c = retail_col or detect_columns(sample, ["retail", "retailForce", "小单净流入"])
    sector_c = sector_col or "sector"

    if sector_c not in sample:
        # 尝试识别板块列
        sector_c = detect_columns(sample, ["sector", "板块", "industry", "行业", "category"])

    by_sector = defaultdict(lambda: {"count": 0, "main": 0.0, "retail": 0.0, "members": set()})
    for row in rows:
        sec = row.get(sector_c, "未知") if sector_c else "未知"
        by_sector[sec]["count"] += 1
        if main_c:
            by_sector[sec]["main"] += _pf(row.get(main_c, 0))
        if retail_c:
            if row.get(retail_c):
                by_sector[sec]["retail"] += _pf(row.get(retail_c, 0))
        if name_col:
            by_sector[sec]["members"].add(row.get(name_col, "?"))

    result = []
    for sec, data in by_sector.items():
        net = data["main"] + data["retail"]
        main_ratio = compute_main_ratio(data["main"], data["retail"])
        result.append({
            "sector": sec,
            "items": data["count"],
            "members": len(data["members"]),
            "main_flow": round(data["main"], 2),
            "retail_flow": round(data["retail"], 2),
            "net_flow": round(net, 2),
            "main_ratio": round(main_ratio, 3),
        })

    result.sort(key=lambda x: -x["net_flow"])
    return result


# ── 多时间维度分析 ────────────────────────────────

def timeframe_analysis(rows, name_col, main_col, retail_col, date_col, tf="day"):
    """按日/周/月汇总分析。"""
    sample = rows[0] if rows else {}
    name_c = name_col or detect_columns(sample, ["name", "代码", "stock"])
    main_c = main_col or detect_columns(sample, ["main_force", "mainForce", "主力净流入"])
    retail_c = retail_col or detect_columns(sample, ["retail", "retailForce", "小单净流入"])
    date_c = date_col or detect_columns(sample, ["date", "日期", "trade_date"])

    if not date_c:
        return None

    # 解析日期并分组
    groups = defaultdict(lambda: {"count": 0, "main": 0.0, "retail": 0.0, "names": set()})

    for row in rows:
        dt_str = str(row.get(date_c, ""))[:10]
        try:
            dt = datetime.strptime(dt_str, "%Y-%m-%d")
        except ValueError:
            try:
                dt = datetime.strptime(dt_str, "%Y/%m/%d")
            except ValueError:
                try:
                    dt = datetime.strptime(dt_str[:8], "%Y%m%d")
                except ValueError:
                    continue

        if tf == "week":
            key = f"{dt.year}W{dt.isocalendar()[1]:02d}"
        elif tf == "month":
            key = f"{dt.year}-{dt.month:02d}"
        elif tf == "year":
            key = str(dt.year)
        else:
            key = dt_str

        groups[key]["count"] += 1
        if main_c:
            groups[key]["main"] += _pf(row.get(main_c, 0))
        if retail_c:
            groups[key]["retail"] += _pf(row.get(retail_c, 0))
        if name_c:
            groups[key]["names"].add(row.get(name_c, "?"))

    result = []
    for period in sorted(groups):
        g = groups[period]
        net = g["main"] - g["retail"] if (g["main"] or g["retail"]) else g["main"]
        result.append({
            "period": period,
            "records": g["count"],
            "active_stocks": len(g["names"]),
            "main_flow": round(g["main"], 2),
            "retail_flow": round(g["retail"], 2),
            "net_flow": round(net, 2),
        })
    return result


# ── 与指数对比 ──────────────────────────────────────

def compare_with_index(rows, name_col, main_col, retail_col, index_name):
    """将个股资金流向与指数对比。"""
    sample = rows[0] if rows else {}
    main_c = main_col or detect_columns(sample, ["main_force", "mainForce", "主力净流入"])
    retail_c = retail_col or detect_columns(sample, ["retail", "retailForce", "小单净流入"])

    # 分离指数数据和个股数据
    all_data = analyze_flow(rows, name_col, main_col, retail_col)
    rankings = all_data["rankings"]

    index_flow = next((r for r in rankings if index_name in r["name"]), None)
    stocks = [r for r in rankings if index_name not in r["name"]]

    # 对比：跑赢指数（净流入比指数好）
    index_net = index_flow["net_flow"] if index_flow else 0
    outperform = [s for s in stocks if s["net_flow"] > index_net]
    underperform = [s for s in stocks if s["net_flow"] < index_net]

    return {
        "index": index_flow,
        "index_net_flow": index_net,
        "total_stocks": len(stocks),
        "outperform_count": len(outperform),
        "underperform_count": len(underperform),
        "outperform_stocks": outperform[:10],
        "underperform_stocks": underperform[:10],
    }


# ── ASCII走势图 ──────────────────────────────────────

def ascii_trend_chart(flow_data, width=40):
    """资金流向趋势ASCII可视化。"""
    if not flow_data:
        return ""

    periods = flow_data[-min(len(flow_data), 30):]  # 最多30期
    values = [p["net_flow"] for p in periods]
    labels = [p["period"][-5:] for p in periods]

    lo, hi = min(values), max(values)
    if hi - lo < 1:
        return "（资金变化微小）"

    lines = []
    height = 10
    for row in range(height, 0, -1):
        threshold = lo + (hi - lo) * (row - 1) / height
        line = ""
        for v in values:
            if v >= threshold:
                line += "█"
            else:
                line += " "
        lines.append(f"   {threshold:>+12,.0f} {line}")

    axis = f"   {' '*12} {'─' * width}"
    bottom = f"   {' '*12} {'>' * width}"
    return "\n".join(lines) + f"\n{axis}\n{bottom}"


# ── 打印函数 ──────────────────────────────────────────

def print_report(analysis, top=20):
    print(f"\n💰 资金流向分析")
    print(f"   {'='*65}")
    detected = analysis['detected_columns']
    print(f"   识别列: 代码={detected['name']}, 主力={detected['main']}, 散户={detected['retail']}")
    print(f"   总标的: {analysis['total_items']}")
    print(f"   主力总流入: {analysis['total_main_flow']:+,.0f}")
    print(f"   散户总流入: {analysis['total_retail_flow']:+,.0f}")
    net_total = analysis['total_main_flow'] + analysis['total_retail_flow']
    print(f"   净总额: {net_total:+,.0f}")
    print(f"   {'='*65}")
    header = f"   {'排名':>4} {'代码':<14} {'记录':>5} {'主力净流入':>14} {'散户净流入':>14} {'净额':>14} {'占比':>6}"
    print(header)
    print(f"   {'-'*75}")

    for i, r in enumerate(analysis['rankings'][:top], 1):
        direction = "↑" if r['net_flow'] > 0 else "↓" if r['net_flow'] < 0 else "→"
        ratio_pct = f"{r['main_ratio']*100:.0f}%" if 'main_ratio' in r else ""
        print(f"   {i:>4} {r['name']:<14} {r['records']:>5} {r['main_flow']:>+14,.0f} "
              f"{r['retail_flow']:>+14,.0f} {r['net_flow']:>+13,.0f}{direction} {ratio_pct:>6}")


def print_trends(trends, top=20):
    if not trends:
        return
    print(f"\n📈 资金趋势检测")
    print(f"   {'='*75}")
    header = f"   {'代码':<14} {'3日均额':>12} {'方向':<8} {'5日均额':>12} {'方向':<8} {'持续性':>6}"
    print(header)
    print(f"   {'-'*75}")

    sorted_items = sorted(trends.items(), key=lambda x: -abs(x[1]["3day_avg"]))[:top]
    for name, t in sorted_items:
        print(f"   {name:<14} {t['3day_avg']:>+12,.0f} {t['3day_direction']:<8} "
              f"{t['5day_avg']:>+12,.0f} {t['5day_direction']:<8} {t['persistence']:>6}")


def print_sector_report(sectors, top=15):
    if not sectors:
        return
    print(f"\n📊 板块资金聚合")
    header = f"   {'板块':<12} {'标的':>5} {'成员':>5} {'主力净流入':>14} {'散户净流入':>14} {'净额':>14} {'占比':>6}"
    print(header)
    print(f"   {'-'*75}")
    for s in sectors[:top]:
        direction = "↑" if s['net_flow'] > 0 else "↓"
        ratio_pct = f"{s['main_ratio']*100:.0f}%"
        print(f"   {s['sector']:<12} {s['items']:>5} {s['members']:>5} {s['main_flow']:>+14,.0f} "
              f"{s['retail_flow']:>+14,.0f} {s['net_flow']:>+14,.0f} {ratio_pct:>6}")


def print_timeframe(tf_data):
    if not tf_data:
        return
    print(f"\n📅 多时间维度 — {tf_data[0]['period']} ~ {tf_data[-1]['period']}")
    header = f"   {'期间':<12} {'记录':>6} {'活跃':>5} {'主力':>14} {'散户':>14} {'净额':>14}"
    print(header)
    print(f"   {'-'*70}")
    for p in tf_data:
        print(f"   {p['period']:<12} {p['records']:>6} {p['active_stocks']:>5} "
              f"{p['main_flow']:>+14,.0f} {p['retail_flow']:>+14,.0f} {p['net_flow']:>+14,.0f}")


def print_compare(comp):
    if not comp:
        return
    idx = comp.get("index")
    if idx:
        print(f"\n📊 与指数对比")
        print(f"   指数: {idx['name']} (净额 {idx['net_flow']:+,.0f})")
        print(f"   跑赢指数: {comp['outperform_count']} / {comp['total_stocks']}")
        print(f"   跑输指数: {comp['underperform_count']} / {comp['total_stocks']}")
        if comp.get("outperform_stocks"):
            print(f"\n   跑赢前10:")
            for s in comp["outperform_stocks"][:5]:
                print(f"      {s['name']:<12} {s['net_flow']:>+12,.0f}")
        if comp.get("underperform_stocks"):
            print(f"\n   跑输前5:")
            for s in comp["underperform_stocks"][:5]:
                print(f"      {s['name']:<12} {s['net_flow']:>+12,.0f}")


# ── 主入口 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fund Flow v1.1.0 — 资金流向分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令说明:
  (默认)       资金流向排行分析
  --trend      资金趋势检测（3日/5日/10日方向 + 持续性）
  --sector     板块聚合分析（需要CSV有 sector/板块/industry列）
  --timeframe  多时间维度分析 (day/week/month/year)
  --compare    与指数对比（需要CSV中包含指数数据，如"沪深300"）
  --chart      显示ASCII趋势图

示例:
  python3 %(prog)s --file fundflow.csv
  python3 %(prog)s --file fundflow.csv --trend
  python3 %(prog)s --file fundflow.csv --sector --sector-col 板块
  python3 %(prog)s --file fundflow.csv --timeframe week
  python3 %(prog)s --file fundflow.csv --compare --index-name 沪深300
  python3 %(prog)s --file fundflow.csv --chart

免责声明: 本工具仅提供资金流向分析参考，不构成投资建议。
        """
    )
    parser.add_argument("--file", required=True, help="CSV资金流向数据")
    parser.add_argument("--name-col", help="股票/板块名称列")
    parser.add_argument("--main-col", help="主力净流入列")
    parser.add_argument("--retail-col", help="散户净流入列")
    parser.add_argument("--date-col", help="日期列")
    parser.add_argument("--sector-col", help="板块列（用于--sector）")
    parser.add_argument("--top", type=int, default=20, help="显示前N")
    parser.add_argument("--trend", action="store_true", help="资金趋势检测")
    parser.add_argument("--sector", action="store_true", help="板块聚合分析")
    parser.add_argument("--timeframe", choices=["day", "week", "month", "year"],
                        default="", help="多时间维度")
    parser.add_argument("--compare", action="store_true", help="与指数对比")
    parser.add_argument("--index-name", default="沪深300", help="指数名称")
    parser.add_argument("--chart", action="store_true", help="ASCII趋势图")
    parser.add_argument("--output", help="JSON输出路径")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    rows = read_csv(args.file)
    if not rows:
        print("❌ 空文件")
        sys.exit(1)

    # 收集所有输出
    output = {}

    # --trend
    if args.trend:
        trends = detect_trend(rows, args.name_col or "", args.main_col or "",
                              args.retail_col or "", args.date_col or "")
        output["trends"] = trends
        print_trends(trends, args.top)
        if args.json or args.output:
            print(json.dumps(trends, indent=2, ensure_ascii=False))

    # --sector
    elif args.sector:
        sectors = aggregate_sector(rows, args.name_col or "", args.sector_col or "",
                                   args.main_col or "", args.retail_col or "")
        output["sectors"] = sectors
        print_sector_report(sectors, args.top)
        if args.json or args.output:
            print(json.dumps(sectors, indent=2, ensure_ascii=False))

    # --timeframe
    elif args.timeframe:
        tf_data = timeframe_analysis(rows, args.name_col or "", args.main_col or "",
                                     args.retail_col or "", args.date_col or "", args.timeframe)
        output["timeframe"] = tf_data
        print_timeframe(tf_data)
        if args.json or args.output:
            print(json.dumps(tf_data, indent=2, ensure_ascii=False))

    # --compare
    elif args.compare:
        comp = compare_with_index(rows, args.name_col or "", args.main_col or "",
                                  args.retail_col or "", args.index_name)
        output["comparison"] = comp
        print_compare(comp)
        if args.json or args.output:
            print(json.dumps(comp, indent=2, ensure_ascii=False))

    # --chart
    elif args.chart:
        tf_data = timeframe_analysis(rows, args.name_col or "", args.main_col or "",
                                     args.retail_col or "", args.date_col or "", "day")
        if tf_data:
            print(f"\n📈 资金流向趋势 — {Path(args.file).name}")
            print(ascii_trend_chart(tf_data))

    # 默认：排行分析
    else:
        analysis = analyze_flow(rows, args.name_col or "", args.main_col or "",
                                args.retail_col or "", args.date_col or "")
        output = analysis
        print_report(analysis, args.top)

        if args.json or args.output:
            print(json.dumps(analysis, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n💾 已保存: {args.output}")


if __name__ == "__main__":
    main()
