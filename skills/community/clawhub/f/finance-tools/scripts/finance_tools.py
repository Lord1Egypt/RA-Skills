#!/usr/bin/env python3
"""
财务分析工具集 (Finance Tools) v1.1.0

功能: analyze, ratios, trend, category, budget, yoy, forecast
纯 Python 标准库，无外部依赖。

用法:
    python3 scripts/finance_tools.py analyze --file transactions.csv
    python3 scripts/finance_tools.py category --file transactions.csv
    python3 scripts/finance_tools.py budget --file actual.csv --budget-file budget.csv
    python3 scripts/finance_tools.py forecast --file revenue.csv --periods 3
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


def _parse_float(val):
    try:
        return float(val.replace(",", "").replace(" ", ""))
    except (ValueError, AttributeError):
        return None


def _detect_columns(rows):
    """自动识别金额、日期、类别列。"""
    if not rows:
        return {}
    sample = rows[0]
    money_cols, date_cols, cat_cols = [], [], []
    for col in sample:
        val = sample[col]
        if val and _parse_float(val) is not None:
            money_cols.append(col)
        elif val and any(c in val for c in ["/", "-", "."]) and len(val) in (7, 8, 10):
            date_cols.append(col)
        else:
            cat_cols.append(col)

    money_keywords = ["amount", "金额", "revenue", "收入", "expense", "支出",
                      "cost", "成本", "profit", "利润", "price", "单价", "actual", "实际",
                      "budget", "预算"]
    date_keywords = ["date", "日期", "time", "时间", "month", "月份", "year", "年份",
                     "period", "期间"]
    cat_keywords = ["category", "类别", "type", "类型", "name", "名称", "product", "产品",
                    "department", "部门", "project", "项目"]

    money_lower = [c.lower().strip() for c in money_cols]
    date_lower = [c.lower().strip() for c in date_cols]
    cat_lower = [c.lower().strip() for c in cat_cols]

    money = next((money_cols[i] for i, c in enumerate(money_lower)
                  if c in money_keywords), None)
    date = next((date_cols[i] for i, c in enumerate(date_lower)
                 if c in date_keywords), None)
    cat = next((cat_cols[i] for i, c in enumerate(cat_lower)
                if c in cat_keywords), None)

    return {
        "money_col": money or (money_cols[0] if money_cols else None),
        "date_col": date or (date_cols[0] if date_cols else None),
        "cat_col": cat or (cat_cols[0] if cat_cols else None),
        "money_all": money_cols,
        "date_all": date_cols,
        "cat_all": cat_cols,
    }


def _month_key(val):
    """将日期字符串转为 YYYY-MM 键。"""
    val = str(val).strip()
    if len(val) == 10:
        return val[:7]
    if len(val) == 8 and val.isdigit():
        return val[:4] + "-" + val[4:6]
    if len(val) == 7:
        return val
    return val


def _ascii_bar(value, max_value, width=15):
    if max_value == 0:
        return "░" * width
    filled = int((value / max_value) * width)
    return "█" * filled + "░" * (width - filled)


# ─── Analyze ────────────────────────────────────────────────────
def cmd_analyze(args):
    rows = read_csv(args.file)
    cols = _detect_columns(rows)
    mc = cols["money_col"]
    if not mc:
        print("❌ 无法识别金额列。")
        return

    vals = [_parse_float(r[mc]) for r in rows if r.get(mc)]
    vals = [v for v in vals if v is not None]
    if not vals:
        print("❌ 未找到有效的金额数据")
        return

    pos = sum(v for v in vals if v >= 0)
    neg = abs(sum(v for v in vals if v < 0))

    print(f"📊 财务分析 — {Path(args.file).name}")
    print(f"   {'=' * 40}")
    print(f"   总交易数: {len(rows)}")
    print(f"   收入合计: {pos:>14,.2f}")
    print(f"   支出合计: {neg:>14,.2f}")
    net = sum(vals)
    print(f"   净额:     {net:>14,.2f}")
    if neg > 0:
        print(f"   收支比:   {pos / neg:>13.2f}x")
    if len(vals) > 1:
        avg = sum(vals) / len(vals)
        print(f"   平均金额: {avg:>14,.2f}")
        print(f"   最大金额: {max(vals):>14,.2f}")
        print(f"   最小金额: {min(vals):>14,.2f}")
        if len(vals) >= 4:
            sorted_vals = sorted(vals)
            q1 = sorted_vals[len(sorted_vals) // 4]
            q3 = sorted_vals[len(sorted_vals) * 3 // 4]
            print(f"   P25(四分之一): {q1:>10,.2f} | P75(四分之三): {q3:>10,.2f}")

    if cols.get("date_col"):
        dc = cols["date_col"]
        monthly = defaultdict(float)
        for r in rows:
            v = _parse_float(r.get(mc, ""))
            if v is not None:
                monthly[_month_key(r.get(dc, ""))] += v
        if monthly:
            print(f"\n   月度净额:")
            for m in sorted(monthly):
                print(f"     {m}: {monthly[m]:>12,.2f}")


# ─── Ratios (expanded) ──────────────────────────────────────────
def cmd_ratios(args):
    rows = read_csv(args.file)
    cols = _detect_columns(rows)
    money = cols["money_all"]

    if len(money) < 2:
        print("❌ 需要至少2个金额列来计算比率。")
        return

    print(f"📈 财务比率分析 — {Path(args.file).name}")
    print(f"   {'=' * 40}")

    # 汇总各列
    sums = {}
    for col in money:
        vals = [_parse_float(r[col]) for r in rows if r.get(col)]
        vals = [v for v in vals if v is not None]
        sums[col] = sum(vals) if vals else 0
        avg = sum(vals) / len(vals) if vals else 0
        print(f"   {col}: 合计={sums[col]:>12,.2f}  平均={avg:>10,.2f}")

    print()

    # 常见财务比率
    rev = next((k for k in money if k.lower() in ("revenue", "收入", "income")), None)
    cost = next((k for k in money if k.lower() in ("cost", "成本", "cogs")), None)
    profit = next((k for k in money if k.lower() in ("profit", "利润", "gross")), None)
    assets = next((k for k in money if k.lower() in ("assets", "资产", "total_assets")), None)
    liabilities = next((k for k in money if k.lower() in ("liabilities", "负债", "debt")), None)
    equity = next((k for k in money if k.lower() in ("equity", "权益", "净资产")), None)
    net_income = next((k for k in money if k.lower() in ("net_income", "净利润", "net")), None)
    investment = next((k for k in money if k.lower() in ("investment", "投资")), None)

    print("   财务比率:")
    if rev and cost and sums.get(cost, 0) > 0:
        margin = (sums[rev] - sums[cost]) / sums[rev] * 100
        print(f"   毛利率: {margin:.2f}%  (收入={sums[rev]:,.2f}, 成本={sums[cost]:,.2f})")
    if profit and rev and sums.get(rev, 0) > 0:
        net_margin = sums[profit] / sums[rev] * 100
        print(f"   净利率: {net_margin:.2f}%")
    if liabilities and assets and sums.get(assets, 0) > 0:
        debt_ratio = sums[liabilities] / sums[assets] * 100
        print(f"   资产负债率: {debt_ratio:.2f}%")
    if net_income and equity and sums.get(equity, 0) > 0:
        roe = sums[net_income] / sums[equity] * 100
        print(f"   ROE(净资产收益率): {roe:.2f}%")
    if net_income and assets and sums.get(assets, 0) > 0:
        roa = sums[net_income] / sums[assets] * 100
        print(f"   ROA(总资产收益率): {roa:.2f}%")
    if net_income and investment and sums.get(investment, 0) > 0:
        roi = sums[net_income] / sums[investment] * 100
        print(f"   ROI(投资回报率): {roi:.2f}%")

    # 两两比率
    print(f"\n   两两对比比率:")
    for i in range(len(money)):
        for j in range(i + 1, min(i + 2, len(money))):
            d = sums.get(money[j], 0)
            ratio = sums[money[i]] / d if d != 0 else float("inf")
            print(f"   {money[i]} / {money[j]} = {ratio:.4f}")


# ─── Trend ──────────────────────────────────────────────────────
def cmd_trend(args):
    rows = read_csv(args.file)
    cols = _detect_columns(rows)
    mc, dc = cols["money_col"], cols["date_col"]
    if not mc or not dc:
        print("❌ 需要日期列和金额列")
        return

    monthly = defaultdict(float)
    for r in rows:
        v = _parse_float(r.get(mc, ""))
        if v is not None:
            monthly[_month_key(r.get(dc, ""))] += v

    if not monthly:
        print("❌ 无法解析日期数据")
        return

    # 计算移动平均
    sorted_months = sorted(monthly)
    ma_window = args.ma or 3
    ma_values = []
    for i, m in enumerate(sorted_months):
        start = max(0, i - ma_window + 1)
        window_vals = [monthly[sorted_months[j]] for j in range(start, i + 1)]
        ma_values.append(sum(window_vals) / len(window_vals))

    print(f"📈 月度趋势分析 — {Path(args.file).name}")
    print(f"   {'=' * 50}")
    print(f"   {'月份':<12} {'金额':>12} {'环比':>8} {'同比':>8} {'MA-{ma_window if args.ma else 3}':>12}")
    print(f"   {'-' * 52}")

    prev_month = None
    year_data = defaultdict(list)
    for m in sorted_months:
        year_data[m[:4]].append((m, monthly[m]))

    for i, m in enumerate(sorted_months):
        val = monthly[m]
        mom = (val / monthly[prev_month] - 1) * 100 if prev_month and monthly.get(prev_month) else None
        yoy = None
        prev_year = str(int(m[:4]) - 1) + m[4:]
        if prev_year in monthly:
            yoy = (val / monthly[prev_year] - 1) * 100

        mom_str = f"{mom:+.1f}%" if mom is not None else "—"
        yoy_str = f"{yoy:+.1f}%" if yoy is not None else "—"
        ma_str = f"{ma_values[i]:>10,.2f}"

        print(f"   {m:<12} {val:>10,.2f}  {mom_str:>8} {yoy_str:>8}  {ma_str}")
        prev_month = m

    # 汇总
    total = sum(monthly.values())
    avg = total / len(monthly)
    print(f"   {'-' * 52}")
    print(f"   合计: {total:>12,.2f} | 月均: {avg:>10,.2f}")


# ─── Category (NEW) ────────────────────────────────────────────
def cmd_category(args):
    rows = read_csv(args.file)
    cols = _detect_columns(rows)
    mc, cc = cols["money_col"], cols["cat_col"]
    if not mc or not cc:
        print("❌ 需要金额列和类别列")
        return

    by_cat = defaultdict(float)
    for r in rows:
        v = _parse_float(r.get(mc, ""))
        if v is not None:
            by_cat[r.get(cc, "未知")] += v

    if not by_cat:
        print("❌ 未找到有效数据")
        return

    total = sum(by_cat.values())
    sorted_cats = sorted(by_cat.items(), key=lambda x: -abs(x[1]))
    max_val = max(abs(v) for v in by_cat.values())

    print(f"📂 分类汇总 — {Path(args.file).name}")
    print(f"   {'=' * 40}")
    for cat, val in sorted_cats:
        pct = val / total * 100
        bar = _ascii_bar(abs(val), max_val, 20)
        print(f"   {bar} {cat:<20} {val:>12,.2f} ({pct:5.1f}%)")

    print(f"\n   {'=' * 20} {'=' * 20}")
    print(f"   {'合计':<20} {total:>12,.2f} (100%)")

    # 正负分类
    pos_cats = {k: v for k, v in by_cat.items() if v >= 0}
    neg_cats = {k: v for k, v in by_cat.items() if v < 0}
    if pos_cats and neg_cats:
        total_pos = sum(pos_cats.values())
        total_neg = abs(sum(neg_cats.values()))
        print(f"\n   收入类合计: {total_pos:>12,.2f}")
        print(f"   支出类合计: {total_neg:>12,.2f}")
        if total_neg > 0:
            print(f"   收支比:     {total_pos / total_neg:>12.2f}x")


# ─── Budget (NEW) ──────────────────────────────────────────────
def cmd_budget(args):
    actual_rows = read_csv(args.file)
    budget_rows = read_csv(args.actual_budget_file or args.budget_file) if args.budget_file else []
    cols = _detect_columns(actual_rows)
    mc, cc = cols["money_col"], cols["cat_col"]

    if not mc:
        print("❌ 需要金额列")
        return

    # 按类别汇总实际值
    actual_by_cat = defaultdict(float)
    for r in actual_rows:
        v = _parse_float(r.get(mc, ""))
        cat = r.get(cc, "总计") if cc else "总计"
        if v is not None:
            actual_by_cat[cat] += v

    # 按类别汇总预算值
    budget_by_cat = defaultdict(float)
    if budget_rows:
        bcols = _detect_columns(budget_rows)
        bmc = bcols["money_col"]
        bcc = bcols["cat_col"]
        if bmc:
            for r in budget_rows:
                v = _parse_float(r.get(bmc, ""))
                cat = r.get(bcc, "总计") if bcc else "总计"
                if v is not None:
                    budget_by_cat[cat] += v

    all_cats = sorted(set(list(actual_by_cat.keys()) + list(budget_by_cat.keys())))
    if not budget_rows:
        all_cats = sorted(actual_by_cat.keys())

    print(f"📋 预算 vs 实际 — {Path(args.file).name}")
    print(f"   {'=' * 50}")
    print(f"   {'类别':<20} {'实际':>12} {'预算':>12} {'差异':>12} {'执行率':>8}")
    print(f"   {'-' * 64}")

    total_actual = 0
    total_budget = 0
    max_val = max(
        max(abs(actual_by_cat.get(c, 0)), abs(budget_by_cat.get(c, 0)))
        for c in all_cats
    ) if all_cats else 1

    for cat in all_cats:
        a = actual_by_cat.get(cat, 0)
        b = budget_by_cat.get(cat, 0) if budget_rows else 0
        diff = a - b
        rate = (a / b * 100) if b != 0 else (float("inf") if a != 0 else 0)
        total_actual += a
        total_budget += b

        bar = _ascii_bar(abs(a), max_val, 10)
        rate_str = f"{rate:6.1f}%" if isinstance(rate, float) and rate != float("inf") else "新项目"
        print(f"   {bar} {cat:<16} {a:>10,.2f} {b:>10,.2f} {diff:>+10,.2f} {rate_str:>8}")

    if budget_rows:
        total_diff = total_actual - total_budget
        total_rate = (total_actual / total_budget * 100) if total_budget != 0 else 0
        print(f"   {'-' * 64}")
        print(f"   {'合计':<20} {total_actual:>10,.2f} {total_budget:>10,.2f} "
              f"{total_diff:>+10,.2f} {total_rate:>7.1f}%")


# ─── YoY (NEW) ────────────────────────────────────────────────
def cmd_yoy(args):
    rows = read_csv(args.file)
    cols = _detect_columns(rows)
    mc, dc = cols["money_col"], cols["date_col"]
    if not mc or not dc:
        print("❌ 需要日期列和金额列")
        return

    # 按年月汇总
    monthly = defaultdict(float)
    for r in rows:
        v = _parse_float(r.get(mc, ""))
        if v is not None:
            monthly[_month_key(r.get(dc, ""))] += v

    if not monthly:
        print("❌ 无有效数据")
        return

    sorted_months = sorted(monthly)
    print(f"📊 同比/环比增长分析 — {Path(args.file).name}")
    print(f"   {'=' * 50}")
    print(f"   {'月份':<10} {'金额':>12} {'环比(MoM)':>10} {'同比(YoY)':>10}")

    for i, m in enumerate(sorted_months):
        val = monthly[m]

        # 环比（与上个月）
        mom = None
        if i > 0:
            prev = sorted_months[i - 1]
            if monthly.get(prev, 0) > 0:
                mom = (val / monthly[prev] - 1) * 100

        # 同比（与12个月前）
        yoy = None
        m_parts = m.split("-")
        if len(m_parts) == 2:
            yoy_key = f"{int(m_parts[0]) - 1}-{m_parts[1]}"
            if yoy_key in monthly and monthly[yoy_key] > 0:
                yoy = (val / monthly[yoy_key] - 1) * 100

        mom_str = f"{mom:+.1f}%" if mom is not None else "—"
        yoy_str = f"{yoy:+.1f}%" if yoy is not None else "—"
        print(f"   {m:<10} {val:>10,.2f}  {mom_str:>9} {yoy_str:>9}")

    # 年度汇总
    by_year = defaultdict(float)
    for m, v in monthly.items():
        by_year[m[:4]] += v

    if len(by_year) >= 2:
        print(f"\n   年度对比:")
        years = sorted(by_year)
        for i, y in enumerate(years):
            if i > 0:
                growth = (by_year[y] - by_year[years[i - 1]]) / by_year[years[i - 1]] * 100
                print(f"   {y}: {by_year[y]:>12,.2f} (同比 {growth:+.1f}%)")
            else:
                print(f"   {y}: {by_year[y]:>12,.2f} (基准)")


# ─── Forecast (NEW) ────────────────────────────────────────────
def _linear_regression(xs, ys):
    """最小二乘法线性回归。"""
    n = len(xs)
    if n < 2:
        return None, None
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    intercept = (sy - slope * sx) / n
    return slope, intercept


def cmd_forecast(args):
    rows = read_csv(args.file)
    cols = _detect_columns(rows)
    mc, dc = cols["money_col"], cols["date_col"]

    if not mc or not dc:
        print("❌ 需要日期列和金额列")
        return

    # 按年月汇总
    monthly = defaultdict(float)
    for r in rows:
        v = _parse_float(r.get(mc, ""))
        if v is not None:
            monthly[_month_key(r.get(dc, ""))] += v

    if not monthly:
        print("❌ 无有效数据")
        return

    sorted_months = sorted(monthly)
    n = len(sorted_months)
    if n < 3:
        print("❌ 至少需要3个月数据才能预测")
        return

    # 线性回归：x=月份序号, y=金额
    xs = list(range(n))
    ys = [monthly[m] for m in sorted_months]
    slope, intercept = _linear_regression(xs, ys)

    if slope is None:
        print("❌ 无法计算趋势")
        return

    periods = max(1, args.periods)

    # 计算拟合优度 R²
    y_mean = sum(ys) / n
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - y_mean) ** 2 for y in ys)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    print(f"🔮 趋势预测 — {Path(args.file).name}")
    print(f"   {'=' * 45}")

    if args.trend == "linear":
        trend_name = "线性增长"
        sign = "+" if slope >= 0 else ""
        print(f"   模型: {trend_name}  (斜率={sign}{slope:,.2f}/月, R²={r2:.3f})")
    elif args.trend == "moving_avg":
        trend_name = f"{args.window}期移动平均"
        print(f"   模型: {trend_name}  (窗口={args.window})")
    else:
        trend_name = f"{args.window}期加权移动平均"
        print(f"   模型: {trend_name}  (窗口={args.window})")

    print()

    # 历史数据
    print(f"   历史 ({n} 期):")
    if len(sorted_months) > 12:
        print(f"     {sorted_months[0]} to {sorted_months[-1]}")
    last = None
    for i, m in enumerate(sorted_months):
        v = monthly[m]
        change = f"({(v / monthly[sorted_months[max(0,i-1)]] - 1) * 100:+.1f}%)" if i > 0 else ""
        trend_val = slope * i + intercept
        print(f"     {m}: {v:>12,.2f}  {change:<10}")
        last = v

    print()

    # 预测
    print(f"   预测 (未来 {periods} 期):")
    predictions = []
    for p in range(1, periods + 1):
        if args.trend == "linear":
            pred = slope * (n - 1 + p) + intercept
        elif args.trend == "moving_avg":
            window = min(args.window, n)
            pred = sum(ys[-window:]) / window
        else:  # weighted
            window = min(args.window, n)
            weights = list(range(1, window + 1))
            weight_sum = sum(weights)
            pred = sum(ys[-window + i] * w for i, w in enumerate(weights)) / weight_sum

        predictions.append(pred)
        next_month = _increment_month(sorted_months[-1], p)
        print(f"     {next_month}: {pred:>12,.2f}  "
              f"(vs last: {(pred / last - 1) * 100:+.1f}% 预测增长)" if last else
              f"     {next_month}: {pred:>12,.2f}")

    # 预测汇总
    total_pred = sum(predictions)
    avg_pred = total_pred / len(predictions)
    print(f"\n   预测合计: {total_pred:>12,.2f}")
    print(f"   预测月均: {avg_pred:>12,.2f}")
    print(f"\n   ⚠️ 本预测基于历史数据趋势，仅供参考。实际结果可能因市场变化、"
          f"政策调整等因素与预测产生显著差异。")


def _increment_month(ym, offset):
    """将 YYYY-MM 增加 offset 个月。"""
    year, month = int(ym[:4]), int(ym[5:7])
    month += offset
    while month > 12:
        year += 1
        month -= 12
    return f"{year}-{month:02d}"


# ─── Main ──────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Finance Tools v1.1.0")
    sp = p.add_subparsers(dest="command", required=True)

    # analyze
    a = sp.add_parser("analyze", help="基础财务分析（收支汇总/分位数）")
    a.add_argument("--file", required=True)

    # ratios (expanded)
    r = sp.add_parser("ratios", help="财务比率分析（含毛利率/净利率/ROE/ROA/ROI）")
    r.add_argument("--file", required=True)

    # trend (with MA)
    t = sp.add_parser("trend", help="月度趋势分析（含移动平均）")
    t.add_argument("--file", required=True)
    t.add_argument("--ma", type=int, default=3, help="移动平均窗口（月数）")

    # category — NEW
    c = sp.add_parser("category", help="分类汇总（含ASCII条形图）")
    c.add_argument("--file", required=True)

    # budget — NEW
    b = sp.add_parser("budget", help="预算 vs 实际对比")
    b.add_argument("--file", required=True, help="实际数据文件")
    b.add_argument("--budget-file", help="预算数据文件")
    b.add_argument("--actual-budget-file", help="含预算列的实际数据文件")

    # yoy — NEW
    y = sp.add_parser("yoy", help="同比/环比增长分析")
    y.add_argument("--file", required=True)

    # forecast — NEW
    f = sp.add_parser("forecast", help="趋势预测（线性回归/移动平均）")
    f.add_argument("--file", required=True)
    f.add_argument("--periods", type=int, default=3, help="预测期数")
    f.add_argument("--trend", choices=["linear", "moving_avg", "weighted"],
                   default="linear", help="预测模型")
    f.add_argument("--window", type=int, default=3, help="移动平均窗口")

    args = p.parse_args()

    dispatcher = {
        "analyze": cmd_analyze,
        "ratios": cmd_ratios,
        "trend": cmd_trend,
        "category": cmd_category,
        "budget": cmd_budget,
        "yoy": cmd_yoy,
        "forecast": cmd_forecast,
    }
    dispatcher[args.command](args)


if __name__ == "__main__":
    main()
