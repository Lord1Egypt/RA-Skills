#!/usr/bin/env python3
"""
Alibaba 国际站 推广 ROI 分析 CLI
- 用 sql-linker-cli 连库,读 alibaba_intl_orders + alibaba_intl_promotion_daily
- 输出: 月度总览 / 推广类型拆分 / 按日对照

Usage:
    python scripts/cli.py                        # 全量
    python scripts/cli.py --month 2026-01        # 指定月份
    python scripts/cli.py --rate 7.25            # 自定义 USD/CNY 汇率
    python scripts/cli.py --by-type              # 只看推广类型拆分
    python scripts/cli.py --by-date              # 只看按日对照
    python scripts/cli.py --json                 # JSON 输出 (供后续处理)
"""

import sys
import os
import io
import json
import argparse

# 解决 Windows GBK
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except (ValueError, AttributeError):
    pass

# 让 roi.py 可被 import
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import roi  # noqa: E402


# ============================================================
# 报告渲染
# ============================================================
def _fmt(v, kind="num"):
    if v is None:
        return "-"
    if kind == "num":
        return f"{v:,.2f}"
    if kind == "pct":
        return f"{v:.2f}%"
    return str(v)


def render_summary(s):
    print("=" * 72)
    print("Alibaba 国际站 推广 ROI 总览")
    print("=" * 72)
    print(f"\n汇率: 1 USD = {s['rate_used']} CNY")
    print(f"\n[订单状态分布]")
    for st, cnt in sorted(s["status_breakdown"].items()):
        print(f"  {st:24s} {cnt:>3} 笔")

    print(f"\n[整体 KPI]")
    print(f"  总花费 CNY: {_fmt(s['total_cost_cny'])}")
    print(f"  总花费 USD: {_fmt(s['total_cost_usd'])}")
    print(f"  完成订单数: {s['completed_orders']} 笔")
    print(f"  完成订单金额: {_fmt(s['completed_amount_usd'], 'num')} USD")
    print(f"  单订单成本 (CPO): {_fmt(s['cpo_cny'])} CNY")
    print(f"  ROI: {_fmt(s['roi_pct'], 'pct')}")

    print(f"\n[按月明细]")
    header = (f"{'月份':<10} {'花费CNY':>12} {'花费USD':>12} "
              f"{'完成订单':>10} {'订单金额':>12} {'CPO(CNY)':>10} {'ROI':>10}")
    print(header)
    print("─" * 72)
    for m in s["monthly"]:
        print(f"{m['month']:<10} {_fmt(m['cost_cny']):>12} {_fmt(m['cost_usd']):>12} "
              f"{m['completed_cnt']:>10} {_fmt(m['completed_amount_usd']):>12} "
              f"{_fmt(m['cpo_cny']):>10} {_fmt(m['roi_pct'], 'pct'):>10}")


def render_by_type(by_type_rows):
    print("\n" + "─" * 72)
    print("[按推广类型拆分]")
    print("─" * 72)
    header = (f"{'推广类型':<22} {'天数':>4} {'花费CNY':>10} {'花费USD':>10} "
              f"{'曝光':>8} {'点击':>6} {'后台报订单':>10}")
    print(header)
    print("─" * 72)
    for r in by_type_rows:
        print(f"{r['promotion_type']:<22} {r['days']:>4} {_fmt(r['cost_cny']):>10} "
              f"{_fmt(r['cost_usd']):>10} {r['impression']:>8} {r['click']:>6} "
              f"{r['promo_reported_orders']:>10}")
    # 整体
    total_days = sum(r["days"] for r in by_type_rows)
    total_cost = sum(r["cost_cny"] for r in by_type_rows)
    total_imp = sum(r["impression"] for r in by_type_rows)
    total_click = sum(r["click"] for r in by_type_rows)
    total_pr = sum(r["promo_reported_orders"] for r in by_type_rows)
    total_actual = by_type_rows[0]["actual_completed_orders"] if by_type_rows else 0
    total_amt = by_type_rows[0]["actual_completed_amount_usd"] if by_type_rows else 0
    print(f"{'合计':<22} {total_days:>4} {_fmt(total_cost):>10} "
          f"{_fmt(total_cost / roi.DEFAULT_USD_CNY_RATE if total_cost else 0):>10} "
          f"{total_imp:>8} {total_click:>6} {total_pr:>10}")
    print(f"\n  -> 投放期内实际完成订单: {total_actual} 笔, "
          f"金额: {_fmt(total_amt, 'num')} USD")


def render_by_date(date_rows):
    print("\n" + "─" * 72)
    print("[按日对照]")
    print("─" * 72)
    header = (f"{'日期':<12} {'花费CNY':>10} {'后台报订单':>10} "
              f"{'实际完成':>8} {'实际金额':>10} {'CPO(CNY)':>10}")
    print(header)
    print("─" * 72)
    for r in date_rows:
        print(f"{r['date']:<12} {_fmt(r['cost_cny']):>10} {r['promo_reported_orders']:>10} "
              f"{r['actual_completed_cnt']:>8} "
              f"{_fmt(r['actual_completed_amount_usd']):>10} "
              f"{_fmt(r['cpo_cny']):>10}")


# ============================================================
# CLI 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Alibaba 国际站 推广 ROI 分析 (sql-linker-cli 拉数)"
    )
    parser.add_argument(
        "--month",
        default=None,
        help="月份过滤, 格式 YYYY-MM (如 2026-01)。不传则全量。",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=roi.DEFAULT_USD_CNY_RATE,
        help=f"USD/CNY 汇率 (默认 {roi.DEFAULT_USD_CNY_RATE})",
    )
    parser.add_argument(
        "--by-type", action="store_true",
        help="只显示按推广类型拆分",
    )
    parser.add_argument(
        "--by-date", action="store_true",
        help="只显示按日对照",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="JSON 输出",
    )
    args = parser.parse_args()

    # 连库
    db = roi.connect_db(user_label="openclaw-roi-cli")

    # 拉数据
    orders = roi.fetch_orders(db, month=args.month)
    promo = roi.fetch_promotion(db, month=args.month)

    if not orders and not promo:
        print("[WARN] 没有数据。请确认 sql-linker-cli 已连库 + 表已建好 + 数据已加载。")
        sys.exit(1)

    # 计算
    summary = roi.compute_summary(orders, promo, rate=args.rate)
    by_type_rows, _ = roi.compute_by_type(promo, orders, rate=args.rate)
    by_date_rows = roi.compute_by_date(promo, orders, rate=args.rate)

    # 输出
    if args.json:
        payload = {
            "summary": summary,
            "by_type": by_type_rows,
            "by_date": by_date_rows,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return

    if args.by_type:
        render_by_type(by_type_rows)
        return
    if args.by_date:
        render_by_date(by_date_rows)
        return

    # 默认: 全量
    render_summary(summary)
    render_by_type(by_type_rows)
    render_by_date(by_date_rows)
    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()