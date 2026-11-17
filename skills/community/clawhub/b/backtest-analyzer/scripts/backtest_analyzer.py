#!/usr/bin/env python3
"""
Backtest Analyzer v1.1.0 — 回测结果深度分析工具

从交易记录 CSV 中计算回测核心指标，并扩展支持：
月度/季度收益分解、按股票/行业归因、基准对比、
交易频率分析、连续盈亏统计、一句话评级。

用法:
    python3 scripts/backtest_analyzer.py --file trades.csv
    python3 scripts/backtest_analyzer.py --file trades.csv --by month
    python3 scripts/backtest_analyzer.py --file trades.csv --by stock --benchmark bench.csv
    python3 scripts/backtest_analyzer.py --file trades.csv frequency
    python3 scripts/backtest_analyzer.py --file trades.csv streaks
    python3 scripts/backtest_analyzer.py --file trades.csv summary
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict, OrderedDict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

try:
    import numpy as np
    HAS_NP = True
except ImportError:
    HAS_NP = False

try:
    import pandas as pd
    HAS_PD = True
except ImportError:
    HAS_PD = False


# ── 数据读取 ─────────────────────────────────────────────────────────

_DEFAULT_PNL_COLS = ["pnl", "profit", "盈亏", "收益", "return", "net_pnl", "realized_pnl"]
_DEFAULT_PRICE_COLS = ["price", "成交价", "price_avg", "avg_price", "close"]
_DEFAULT_DATE_COLS = ["date", "日期", "trade_date", "time", "时间"]
_DEFAULT_STOCK_COLS = ["stock", "代码", "symbol", "code", "name", "名称"]
_DEFAULT_QTY_COLS = ["shares", "数量", "qty", "volume", "amount"]
_DEFAULT_DIR_COLS = ["direction", "action", "方向", "类型", "side", "type"]
_DEFAULT_SECTOR_COLS = ["sector", "行业", "industry", "板块"]


def _find_col(sample: dict, candidates: list[str]) -> Optional[str]:
    return next((c for c in candidates if c in sample), None)


def read_trades(filepath: str) -> list[dict]:
    """读取交易记录 CSV。自动识别列。"""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return []
    sample = rows[0]

    pnl_col = _find_col(sample, _DEFAULT_PNL_COLS)
    price_col = _find_col(sample, _DEFAULT_PRICE_COLS)
    date_col = _find_col(sample, _DEFAULT_DATE_COLS)
    stock_col = _find_col(sample, _DEFAULT_STOCK_COLS)
    qty_col = _find_col(sample, _DEFAULT_QTY_COLS)
    dir_col = _find_col(sample, _DEFAULT_DIR_COLS)
    sector_col = _find_col(sample, _DEFAULT_SECTOR_COLS)

    trades = []
    for row in rows:
        pnl_raw = row.get(pnl_col, "") if pnl_col else ""
        price_raw = row.get(price_col, "") if price_col else ""
        qty_raw = row.get(qty_col, "") if qty_col else ""

        try:
            pnl = float(pnl_raw.replace(",", "").replace(" ", ""))
        except (ValueError, AttributeError):
            pnl = None

        try:
            price = float(price_raw.replace(",", "").replace(" ", ""))
        except (ValueError, AttributeError):
            price = 0.0

        try:
            qty = float(qty_raw.replace(",", "").replace(" ", ""))
        except (ValueError, AttributeError):
            qty = 0.0

        trade = {
            "date": (row.get(date_col) or "").strip(),
            "stock": (row.get(stock_col) or "").strip(),
            "price": price,
            "qty": qty,
            "pnl": pnl,
            "direction": (row.get(dir_col) or "").lower().strip(),
            "sector": (row.get(sector_col) or "").strip(),
        }
        trades.append(trade)
    return trades


def read_benchmark(filepath: str) -> list[dict]:
    """读取基准 CSV。要求有 date 和 return/close 列。"""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return []
    sample = rows[0]
    ret_col = _find_col(sample, ["return", "收益", "回报", "change", "pct"])
    close_col = _find_col(sample, ["close", "收盘", "收盘价", "price"])
    date_col = _find_col(sample, _DEFAULT_DATE_COLS)

    data = []
    for row in rows:
        d = row.get(date_col, "").strip()
        if ret_col:
            try:
                r = float(row[ret_col].replace("%", "").replace(",", ""))
            except (ValueError, AttributeError):
                r = 0.0
        elif close_col:
            # derive return from close prices
            r = None  # will be computed later
        else:
            r = 0.0
        data.append({"date": d, "return": r})
    # If close-based, compute returns
    if not ret_col and close_col:
        closes = []
        for row in rows:
            try:
                c = float(row[close_col].replace(",", ""))
            except (ValueError, AttributeError):
                c = 0.0
            closes.append(c)
        for i, d in enumerate(data):
            if i == 0:
                d["return"] = 0.0
            else:
                d["return"] = (closes[i] - closes[i-1]) / closes[i-1] * 100 if closes[i-1] != 0 else 0.0
    return data


def _parse_date(dt_str: str) -> Optional[datetime]:
    """尝试解析多种日期格式。"""
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(dt_str, fmt)
        except (ValueError, TypeError):
            continue
    return None


def _safe_pnls(trades: list[dict]) -> list[float]:
    return [t["pnl"] for t in trades if t.get("pnl") is not None]


# ── 核心指标计算 ──────────────────────────────────────────────────────

def compute_metrics(trades: list[dict], capital: float = 1_000_000) -> dict:
    """计算回测核心指标。"""
    if not trades:
        return {"error": "无交易数据"}

    pnls = _safe_pnls(trades)
    if not pnls:
        return {"error": "未找到盈亏(PnL)数据"}

    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]

    total_pnl = sum(pnls)
    total_return_pct = total_pnl / capital * 100
    win_rate = len(wins) / len(pnls) * 100 if pnls else 0
    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = abs(sum(losses)) / len(losses) if losses else 0
    profit_factor = abs(sum(wins) / sum(losses)) if losses and sum(losses) != 0 else float("inf")
    payoff = abs(avg_win / avg_loss) if avg_loss > 0 else float("inf")

    # Max drawdown
    if HAS_NP:
        cumulative = np.cumsum(pnls) + capital
        running_max = np.maximum.accumulate(cumulative)
        drawdowns = (running_max - cumulative) / running_max * 100
        max_dd = float(np.max(drawdowns))
    else:
        cum = capital
        peak = capital
        max_dd = 0.0
        for p in pnls:
            cum += p
            if cum > peak:
                peak = cum
            dd = (peak - cum) / peak * 100
            max_dd = max(max_dd, dd)

    # Sharpe (daily, rf=0)
    if HAS_NP:
        daily_ret = np.array(pnls) / capital
        sharpe = float(np.mean(daily_ret) / max(np.std(daily_ret), 1e-12) * math.sqrt(252))
    else:
        mean_ret = sum(pnls) / len(pnls) / capital
        var_ret = sum((p / capital - mean_ret) ** 2 for p in pnls) / len(pnls)
        sharpe = mean_ret / math.sqrt(max(var_ret, 1e-12)) * math.sqrt(252)

    # Sortino (downside deviation)
    target = 0
    if HAS_NP:
        downside = np.array([min(p / capital - target, 0) for p in pnls])
        downside_std = float(np.std(downside)) if np.std(downside) > 0 else 1e-12
        sortino = float(mean_ret / downside_std * math.sqrt(252))
    else:
        downside = [min(p / capital - target, 0) for p in pnls]
        dvar = sum(d * d for d in downside) / len(downside)
        sortino = mean_ret / math.sqrt(max(dvar, 1e-12)) * math.sqrt(252)

    return {
        "total_trades": len(pnls),
        "win_trades": len(wins),
        "loss_trades": len(losses),
        "win_rate_pct": round(win_rate, 1),
        "total_pnl": round(total_pnl, 2),
        "total_return_pct": round(total_return_pct, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "avg_return_per_trade_pct": round(total_return_pct / len(pnls), 2) if pnls else 0,
        "profit_factor": round(profit_factor, 2),
        "payoff_ratio": round(payoff, 2),
        "max_drawdown_pct": round(max_dd, 2),
        "sharpe_ratio": round(sharpe, 2),
        "sortino_ratio": round(sortino, 2),
        "best_trade_pnl": round(max(pnls), 2),
        "worst_trade_pnl": round(min(pnls), 2),
        "expectancy": round(sum(pnls) / len(pnls), 2),
    }


# ── 扩展分析 ──────────────────────────────────────────────────────────

def decompose_by_period(trades: list[dict], period: str = "month") -> dict:
    """按月度/季度分解收益。"""
    pnls = _safe_pnls(trades)
    if not pnls:
        return {"error": "无盈亏数据"}

    period_map: dict[str, dict] = defaultdict(lambda: {"trades": 0, "pnl": 0.0, "wins": 0})
    for t in trades:
        pnl = t.get("pnl")
        if pnl is None:
            continue
        dt = _parse_date(t.get("date", ""))
        if not dt:
            continue
        key = dt.strftime("%Y-%m") if period == "month" else f"{dt.year}Q{(dt.month-1)//3+1}"
        period_map[key]["trades"] += 1
        period_map[key]["pnl"] += pnl
        if pnl > 0:
            period_map[key]["wins"] += 1

    results = {}
    for key in sorted(period_map.keys()):
        d = period_map[key]
        wr = round(d["wins"] / d["trades"] * 100, 1) if d["trades"] else 0
        results[key] = {
            "trades": d["trades"],
            "pnl": round(d["pnl"], 2),
            "win_rate_pct": wr,
        }

    return {
        "period": period,
        "periods": results,
        "positive_periods": sum(1 for v in results.values() if v["pnl"] > 0),
        "total_periods": len(results),
    }


def decompose_by_stock(trades: list[dict]) -> dict:
    """按股票归因分析。"""
    pnls = _safe_pnls(trades)
    if not pnls:
        return {"error": "无盈亏数据"}

    stock_map: dict[str, dict] = defaultdict(lambda: {"trades": 0, "pnl": 0.0, "wins": 0})
    for t in trades:
        pnl = t.get("pnl")
        if pnl is None:
            continue
        stock = t.get("stock", "未知") or "未知"
        stock_map[stock]["trades"] += 1
        stock_map[stock]["pnl"] += pnl
        if pnl > 0:
            stock_map[stock]["wins"] += 1

    total_pnl = sum(v["pnl"] for v in stock_map.values())
    results = {}
    for stock, d in sorted(stock_map.items(), key=lambda x: abs(x[1]["pnl"]), reverse=True):
        wr = round(d["wins"] / d["trades"] * 100, 1) if d["trades"] else 0
        contrib = round(d["pnl"] / total_pnl * 100, 1) if total_pnl != 0 else 0
        results[stock] = {
            "trades": d["trades"],
            "pnl": round(d["pnl"], 2),
            "win_rate_pct": wr,
            "contribution_pct": contrib,
        }

    return {
        "total_pnl": round(total_pnl, 2),
        "stocks": results,
        "positive_stocks": sum(1 for v in results.values() if v["pnl"] > 0),
        "total_stocks": len(results),
    }


def decompose_by_sector(trades: list[dict]) -> dict:
    """按行业归因分析。"""
    sector_map: dict[str, dict] = defaultdict(lambda: {"trades": 0, "pnl": 0.0, "wins": 0})
    for t in trades:
        pnl = t.get("pnl")
        if pnl is None:
            continue
        sector = t.get("sector", "未分类") or "未分类"
        sector_map[sector]["trades"] += 1
        sector_map[sector]["pnl"] += pnl
        if pnl > 0:
            sector_map[sector]["wins"] += 1

    total_pnl = sum(v["pnl"] for v in sector_map.values())
    results = {}
    for sector, d in sorted(sector_map.items(), key=lambda x: abs(x[1]["pnl"]), reverse=True):
        wr = round(d["wins"] / d["trades"] * 100, 1) if d["trades"] else 0
        contrib = round(d["pnl"] / total_pnl * 100, 1) if total_pnl != 0 else 0
        results[sector] = {
            "trades": d["trades"],
            "pnl": round(d["pnl"], 2),
            "win_rate_pct": wr,
            "contribution_pct": contrib,
        }
    return {"total_pnl": round(total_pnl, 2), "sectors": results, "total_sectors": len(results)}


def compare_benchmark(trades: list[dict], bench_data: list[dict]) -> dict:
    """与基准对比分析。"""
    pnls = _safe_pnls(trades)
    if not pnls or not bench_data:
        return {"error": "数据不足"}

    trade_total_ret = sum(pnls) / 1_000_000 * 100  # relative to 1M capital
    bench_total_ret = sum(d.get("return", 0) for d in bench_data)

    # Alpha = strategy_return - benchmark_return
    alpha = trade_total_ret - bench_total_ret

    # Tracking error (std of difference)
    trade_ret_by_date = {}
    for t in trades:
        d = t.get("date", "")
        pnl = t.get("pnl")
        if pnl is not None:
            trade_ret_by_date[d] = trade_ret_by_date.get(d, 0) + (pnl / 1_000_000 * 100)

    diffs = []
    for b in bench_data:
        bd = b.get("date", "")
        bret = b.get("return", 0)
        tret = trade_ret_by_date.get(bd, 0)
        diffs.append(tret - bret)

    te = (sum(d * d for d in diffs) / max(len(diffs), 1)) ** 0.5 if diffs else 0
    info_ratio = (alpha / max(te, 1e-12))

    return {
        "strategy_return_pct": round(trade_total_ret, 2),
        "benchmark_return_pct": round(bench_total_ret, 2),
        "alpha_pct": round(alpha, 2),
        "tracking_error_pct": round(te, 2),
        "information_ratio": round(info_ratio, 2),
        "outperformance": trade_total_ret > bench_total_ret,
    }


def analyze_frequency(trades: list[dict]) -> dict:
    """交易频率分析（间隔分布、持仓时间）。"""
    dated = [t for t in trades if t.get("date") and t.get("pnl") is not None]
    if len(dated) < 2:
        return {"error": "至少需要2条有日期的交易记录"}

    dates = sorted(set(t["date"] for t in dated))
    daily_trades = Counter(t["date"] for t in trades if t.get("date"))

    # Interval between trading days
    intervals = []
    parsed = [d for d in dates if _parse_date(d)]
    for i in range(1, len(parsed)):
        delta = (parsed[i] - parsed[i-1]).days
        intervals.append(delta)

    avg_interval = sum(intervals) / max(len(intervals), 1) if intervals else 0
    max_interval = max(intervals) if intervals else 0

    # Holding period estimation (simplified: assume first trade opens, second closes)
    # More practically: count how many stocks have both buy and sell records
    stock_dates: dict[str, list[str]] = defaultdict(list)
    for t in trades:
        if t.get("stock") and t.get("date"):
            stock_dates[t["stock"]].append(t["date"])

    holding_days = []
    for stock, dts in stock_dates.items():
        unique = sorted(set(dts))
        if len(unique) >= 2:
            days = (_parse_date(unique[-1]) - _parse_date(unique[0])).days
            if days > 0:
                holding_days.append(days)

    avg_hold = sum(holding_days) / max(len(holding_days), 1) if holding_days else 0

    return {
        "total_trading_days": len(dates),
        "daily_trade_count": round(len(trades) / max(len(dates), 1), 1),
        "avg_interval_days": round(avg_interval, 1),
        "max_interval_days": max_interval,
        "min_interval_days": min(intervals) if intervals else 0,
        "avg_holding_days": round(avg_hold, 1) if holding_days else None,
        "days_with_data": len(holding_days),
    }


def analyze_streaks(trades: list[dict]) -> dict:
    """连续盈亏统计。"""
    pnls = _safe_pnls(trades)
    if not pnls:
        return {"error": "无盈亏数据"}

    current_streak = 1
    current_type = "win" if pnls[0] > 0 else "loss"
    max_win, max_loss = 0, 0
    current_max = 1

    for i in range(1, len(pnls)):
        is_win = pnls[i] > 0
        if (is_win and current_type == "win") or (not is_win and current_type == "loss"):
            current_streak += 1
        else:
            if current_type == "win":
                max_win = max(max_win, current_streak)
            else:
                max_loss = max(max_loss, current_streak)
            current_streak = 1
            current_type = "win" if is_win else "loss"

    # Final streak
    if current_type == "win":
        max_win = max(max_win, current_streak)
    else:
        max_loss = max(max_loss, current_streak)

    # Current live streak (from end)
    end_type = "win" if pnls[-1] > 0 else "loss"
    end_streak = 1
    for i in range(len(pnls)-2, -1, -1):
        is_win = pnls[i] > 0
        if (is_win and end_type == "win") or (not is_win and end_type == "loss"):
            end_streak += 1
        else:
            break

    return {
        "max_win_streak": max_win,
        "max_loss_streak": max_loss,
        "current_streak": end_streak,
        "current_streak_type": end_type,
        "win_streak_after_loss": "恢复能力良好" if max_loss < 5 else "连败次数较多",
    }


def generate_summary(metrics: dict, by_stock: dict = None) -> str:
    """生成一句话评级。"""
    if "error" in metrics:
        return f"❌ {metrics['error']}"

    wr = metrics.get("win_rate_pct", 0)
    sharpe = metrics.get("sharpe_ratio", 0)
    dd = metrics.get("max_drawdown_pct", 100)
    pf = metrics.get("profit_factor", 0)
    total_ret = metrics.get("total_return_pct", 0)
    n = metrics.get("total_trades", 0)

    parts = []
    if n < 20:
        parts.append(f"样本偏少({n}笔)，结论参考性有限")
    if sharpe >= 2:
        parts.append(f"夏普{sharpe:.1f}极优")
    elif sharpe >= 1:
        parts.append(f"夏普{sharpe:.1f}良好")
    elif sharpe >= 0:
        parts.append(f"夏普{sharpe:.1f}一般")
    else:
        parts.append(f"夏普{sharpe:.1f}需警惕")

    if wr >= 60:
        parts.append(f"胜率{wr:.0f}%较高")
    elif wr >= 45:
        parts.append(f"胜率{wr:.0f}%中等")
    else:
        parts.append(f"胜率{wr:.0f}%偏低")

    if dd <= 10:
        parts.append(f"回撤{dd:.1f}%可控")
    elif dd <= 20:
        parts.append(f"回撤{dd:.1f}%尚可")
    else:
        parts.append(f"回撤{dd:.1f}%偏高")

    if pf >= 2:
        parts.append(f"获利因子{pf:.1f}出色")
    elif pf >= 1:
        parts.append(f"获利因子{pf:.1f}尚可")
    else:
        parts.append(f"获利因子{pf:.1f}偏低")

    if total_ret > 0:
        parts.append(f"累计收益{total_ret:+.1f}%")
    else:
        parts.append(f"累计亏损{total_ret:.1f}%")

    # Overall grade
    score = 0
    score += 25 if sharpe >= 1.5 else 10 if sharpe >= 0 else -10
    score += 20 if wr >= 55 else 5 if wr >= 40 else -10
    score += 20 if dd <= 10 else 5 if dd <= 20 else -10
    score += 20 if pf >= 2.0 else 5 if pf >= 1.0 else -10
    score += 15 if total_ret > 0 else -15

    grade = "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D"

    return f"[评级 {grade}] {' | '.join(parts)}"


# ── 打印函数 ─────────────────────────────────────────────────────────

def print_report(metrics: dict):
    """打印人类可读的报告。"""
    print(f"\n📊 回测分析报告")
    print(f"   {'='*45}")
    if "error" in metrics:
        print(f"   ❌ {metrics['error']}")
        return
    print(f"   总交易数:    {metrics['total_trades']}")
    print(f"   盈利交易:    {metrics['win_trades']} ({metrics['win_rate_pct']}%)")
    print(f"   亏损交易:    {metrics['loss_trades']} ({100-metrics['win_rate_pct']:.1f}%)")
    print(f"   {'='*45}")
    print(f"   总收益:      {metrics['total_pnl']:+,.2f} ({metrics['total_return_pct']:+.2f}%)")
    print(f"   平均每笔:    {metrics['avg_return_per_trade_pct']:+.2f}%")
    print(f"   胜率:        {metrics['win_rate_pct']:.1f}%")
    print(f"   盈亏比:      {metrics['payoff_ratio']}")
    pf = metrics.get("profit_factor", 0)
    print(f"   获利因子:    {'∞' if pf==float('inf') else f'{pf:.2f}'}")
    print(f"   {'='*45}")
    print(f"   最大回撤:    {metrics['max_drawdown_pct']:.2f}%")
    print(f"   夏普比率:    {metrics['sharpe_ratio']:.2f}")
    print(f"   索提诺比率:  {metrics['sortino_ratio']:.2f}")
    print(f"   期望值:      {metrics['expectancy']:+.2f}")
    print(f"   最佳交易:    {metrics['best_trade_pnl']:+,.2f}")
    print(f"   最差交易:    {metrics['worst_trade_pnl']:+,.2f}")


def print_by_period(result: dict):
    if "error" in result:
        print(f"   ❌ {result['error']}")
        return
    label = "月度" if result["period"] == "month" else "季度"
    print(f"\n📅 {label}收益分解")
    print(f"   {'='*45}")
    print(f"   {'期间':<12} {'交易':<6} {'收益':<12} {'胜率':<8}")
    print(f"   {'-'*45}")
    for period, d in result["periods"].items():
        sign = "+" if d["pnl"] >= 0 else ""
        print(f"   {period:<12} {d['trades']:<6} {sign}{d['pnl']:<10,.2f} {d['win_rate_pct']:<7}%")
    print(f"   {'-'*45}")
    print(f"   正收益期间: {result['positive_periods']}/{result['total_periods']}")


def print_by_stock(result: dict):
    if "error" in result:
        print(f"   ❌ {result['error']}")
        return
    label = "股票" if "stocks" in result else "行业"
    data = result.get("stocks") or result.get("sectors", {})
    print(f"\n📈 按{label}归因")
    print(f"   {'='*55}")
    print(f"   {label:<12} {'交易':<6} {'收益':<12} {'贡献%':<8} {'胜率':<8}")
    print(f"   {'-'*55}")
    for name, d in data.items():
        sign = "+" if d["pnl"] >= 0 else ""
        print(f"   {name:<12} {d['trades']:<6} {sign}{d['pnl']:<10,.2f} {d['contribution_pct']:<7}% {d['win_rate_pct']:<5}%")
    pos = result.get("positive_stocks", result.get("total_stocks", 0))
    total = result.get("total_stocks", result.get("total_sectors", 0))
    print(f"   盈利: {pos}/{total}")


def print_benchmark(result: dict):
    if "error" in result:
        print(f"   ❌ {result['error']}")
        return
    print(f"\n📊 与基准对比")
    print(f"   {'='*45}")
    print(f"   策略收益:     {result['strategy_return_pct']:+.2f}%")
    print(f"   基准收益:     {result['benchmark_return_pct']:+.2f}%")
    print(f"   超额收益α:    {result['alpha_pct']:+.2f}%")
    print(f"   跟踪误差:     {result['tracking_error_pct']:.2f}%")
    print(f"   信息比率:     {result['information_ratio']:.2f}")
    print(f"   跑赢基准:     {'✅ 是' if result['outperformance'] else '❌ 否'}")


def print_frequency(result: dict):
    if "error" in result:
        print(f"   ❌ {result['error']}")
        return
    print(f"\n⏱ 交易频率分析")
    print(f"   {'='*45}")
    print(f"   交易天数:         {result['total_trading_days']}")
    print(f"   日均交易数:       {result['daily_trade_count']}")
    print(f"   平均间隔:         {result['avg_interval_days']} 天")
    print(f"   最短间隔:         {result['min_interval_days']} 天")
    print(f"   最长间隔:         {result['max_interval_days']} 天")
    if result.get("avg_holding_days"):
        print(f"   平均持仓时间:     {result['avg_holding_days']} 天")


def print_streaks(result: dict):
    if "error" in result:
        print(f"   ❌ {result['error']}")
        return
    print(f"\n🔥 连续盈亏统计")
    print(f"   {'='*45}")
    print(f"   最长连胜:        {result['max_win_streak']} 笔")
    print(f"   最长连败:        {result['max_loss_streak']} 笔")
    print(f"   当前状态:        {result['current_streak']} 笔{result['current_streak_type']}")
    print(f"   连败后胜率:      {result['win_streak_after_loss']}")


# ── 主入口 ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Backtest Analyzer v1.1 — 回测结果深度分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python3 scripts/backtest_analyzer.py --file trades.csv\n"
            "  python3 scripts/backtest_analyzer.py --file trades.csv --by month\n"
            "  python3 scripts/backtest_analyzer.py --file trades.csv --by stock\n"
            "  python3 scripts/backtest_analyzer.py --file trades.csv --benchmark bench.csv\n"
            "  python3 scripts/backtest_analyzer.py --file trades.csv frequency\n"
            "  python3 scripts/backtest_analyzer.py --file trades.csv streaks\n"
            "  python3 scripts/backtest_analyzer.py --file trades.csv summary\n"
            "  python3 scripts/backtest_analyzer.py --file trades.csv --output report.json\n"
        ),
    )
    parser.add_argument("--file", help="CSV交易记录文件")
    parser.add_argument("--capital", type=float, default=1_000_000, help="初始本金")
    parser.add_argument("--output", help="保存报告为JSON")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--by", choices=["month", "quarter", "stock", "sector"], help="维度分解")
    parser.add_argument("--benchmark", help="基准CSV文件路径")

    sp = parser.add_subparsers(dest="subcommand", help="子命令")
    sp.add_parser("frequency", help="交易频率分析")
    sp.add_parser("streaks", help="连续盈亏统计")
    sub_summary = sp.add_parser("summary", help="一句话评级")

    args = parser.parse_args()

    if not args.file and not args.subcommand:
        parser.print_help()
        return

    if not args.file:
        print("❌ 需要 --file 参数")
        return

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        return

    trades = read_trades(args.file)
    if not trades:
        print("❌ 未读取到交易记录")
        return

    # Subcommand mode
    if args.subcommand == "frequency":
        result = analyze_frequency(trades)
        if args.json or args.output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_frequency(result)
        if args.output:
            _save_json(args.output, result)
        return

    if args.subcommand == "streaks":
        result = analyze_streaks(trades)
        if args.json or args.output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_streaks(result)
        if args.output:
            _save_json(args.output, result)
        return

    if args.subcommand == "summary":
        metrics = compute_metrics(trades, args.capital)
        if "error" in metrics:
            print(metrics["error"])
            return
        result = {"rating": generate_summary(metrics), "metrics": metrics}
        if args.json or args.output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n📝 {result['rating']}")
        if args.output:
            _save_json(args.output, result)
        return

    # Default: full report
    metrics = compute_metrics(trades, args.capital)
    if args.json or args.output:
        output = dict(metrics)
    else:
        print_report(metrics)

    # --by decomposition
    if args.by == "month" or args.by == "quarter":
        result = decompose_by_period(trades, args.by)
        if args.json:
            output["period_decomposition"] = result
        else:
            print_by_period(result)

    if args.by == "stock":
        result = decompose_by_stock(trades)
        if args.json:
            output["stock_attribution"] = result
        else:
            print_by_stock(result)

    if args.by == "sector":
        result = decompose_by_sector(trades)
        if args.json:
            output["sector_attribution"] = result
        else:
            print_by_stock(result)

    # --benchmark
    if args.benchmark:
        bench = read_benchmark(args.benchmark)
        if bench:
            result = compare_benchmark(trades, bench)
            if args.json:
                output["benchmark"] = result
            else:
                print_benchmark(result)

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.output:
        _save_json(args.output, output if args.json else metrics)


def _save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n📄 已保存: {path}")


if __name__ == "__main__":
    main()
