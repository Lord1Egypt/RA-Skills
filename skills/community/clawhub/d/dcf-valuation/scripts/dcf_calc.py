#!/usr/env python3
"""
十年DCF估值计算器
用法: python3 dcf_calc.py --json '<JSON参数>'
或:   python3 dcf_calc.py --config '<JSON配置文件路径>'

支持两种估值方法:
1. 传统DCF (Gordon永续折现)
2. 段永平式PE退出法 (10年后净利润 × PE + 分红折现)
"""

import json
import argparse
import sys


def calc_dcf(params):
    """传统DCF: 10年FCF折现 + Gordon永续终值"""
    base_revenue = params["base_revenue"]
    scenarios = params["scenarios"]
    net_cash = params.get("net_cash", 0)
    total_shares = params.get("total_shares", None)
    current_market_cap = params.get("current_market_cap", None)
    current_price = params.get("current_price", None)
    stock_name = params.get("stock_name", "目标公司")

    results = {}

    for name, s in scenarios.items():
        revenue_growth = s["revenue_growth"]
        net_margin = s["net_margin"]
        fcf_ratio = s["fcf_ratio"]
        discount_rate = s["discount_rate"]
        terminal_growth = s["terminal_growth"]

        revenue = base_revenue
        yearly = []
        total_fcf_pv = 0

        for i in range(10):
            year = 2026 + i
            growth = revenue_growth[i] if i < len(revenue_growth) else revenue_growth[-1]
            margin = net_margin[i] if i < len(net_margin) else net_margin[-1]

            revenue = revenue * (1 + growth)
            net_profit = revenue * margin
            fcf = net_profit * fcf_ratio
            pv_fcf = fcf / (1 + discount_rate) ** (i + 1)
            total_fcf_pv += pv_fcf

            yearly.append({
                "year": year,
                "revenue": round(revenue, 1),
                "growth": round(growth * 100, 1),
                "net_margin": round(margin * 100, 1),
                "net_profit": round(net_profit, 1),
                "fcf": round(fcf, 1),
                "pv_fcf": round(pv_fcf, 1),
            })

        final_fcf = yearly[-1]["fcf"]
        terminal_value = final_fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
        pv_terminal = terminal_value / (1 + discount_rate) ** 10

        intrinsic_value = total_fcf_pv + pv_terminal + net_cash
        value_per_share = (intrinsic_value / total_shares * 100) if total_shares else None

        ratio = (intrinsic_value / current_market_cap) if current_market_cap else None
        price_upside = ((value_per_share / current_price - 1) * 100) if (value_per_share and current_price) else None

        if ratio:
            if ratio > 1.3:
                verdict = "🟢 明显便宜（安全边际>30%）"
            elif ratio > 1.1:
                verdict = "🟡 略有折价（安全边际10-30%）"
            elif ratio > 0.9:
                verdict = "🟠 基本合理（±10%）"
            elif ratio > 0.7:
                verdict = "🔴 偏贵（溢价10-30%）"
            else:
                verdict = "🔴 明显偏贵（溢价>30%）"
        else:
            verdict = "N/A"

        total_fcf_10y = sum(y["fcf"] for y in yearly)
        payback = (current_market_cap / (total_fcf_10y / 10)) if current_market_cap else None

        results[name] = {
            "yearly": yearly,
            "total_fcf_pv": round(total_fcf_pv, 1),
            "pv_terminal": round(pv_terminal, 1),
            "net_cash": net_cash,
            "intrinsic_value": round(intrinsic_value, 1),
            "value_per_share": round(value_per_share, 0) if value_per_share else None,
            "current_market_cap": current_market_cap,
            "ratio": round(ratio, 2) if ratio else None,
            "price_upside": round(price_upside, 1) if price_upside else None,
            "verdict": verdict,
            "total_fcf_10y": round(total_fcf_10y, 1),
            "avg_annual_fcf": round(total_fcf_10y / 10, 1),
            "payback_years": round(payback, 1) if payback else None,
        }

    return results


def calc_pe_exit(params):
    """
    段永平式PE退出法:
    - 预测未来10年每年净利润
    - 预测10年后合理PE
    - 终值 = 10年后净利润 × PE + 10年累计分红
    - 不做永续折现，用机会成本思维评判回报率
    """
    base_profit = params.get("base_profit")   # 基准年净利润(亿)
    base_revenue = params["base_revenue"]       # 用于推算营收
    scenarios = params.get("pe_exit_scenarios", {})
    net_cash = params.get("net_cash", 0)
    total_shares = params.get("total_shares", None)
    current_market_cap = params.get("current_market_cap", None)
    current_price = params.get("current_price", None)
    stock_name = params.get("stock_name", "目标公司")

    # 如果没有base_profit，用base_revenue估算
    if base_profit is None:
        # 尝试从scenarios里拿第一个的净利率
        for s in scenarios.values():
            if "avg_net_margin" in s:
                base_profit = base_revenue * s["avg_net_margin"]
                break

    results = {}

    for name, s in scenarios.items():
        profit_growth = s["profit_growth"]   # 净利润增速数组(10年)
        exit_pe = s["exit_pe"]               # 10年后给多少PE
        dividend_ratio = s.get("dividend_ratio", 0.70)  # 分红比例，默认70%
        discount_rate = s.get("discount_rate", 0.015)   # 机会成本折现率，默认1.5%

        yearly = []
        total_dividends_pv = 0
        profit = base_profit

        for i in range(10):
            year = 2026 + i
            growth = profit_growth[i] if i < len(profit_growth) else profit_growth[-1]
            profit = profit * (1 + growth)
            dividend = profit * dividend_ratio
            pv_dividend = dividend / (1 + discount_rate) ** (i + 1)
            total_dividends_pv += pv_dividend

            yearly.append({
                "year": year,
                "profit": round(profit, 1),
                "growth": round(growth * 100, 1),
                "dividend": round(dividend, 1),
                "pv_dividend": round(pv_dividend, 1),
            })

        # 10年后净利润 × PE = 退出市值
        exit_value = profit * exit_pe
        # 退出市值折现到今天
        pv_exit_value = exit_value / (1 + discount_rate) ** 10
        # 加上净现金（段永平认为净现金要加回来）
        intrinsic_value = pv_exit_value + total_dividends_pv + net_cash
        value_per_share = (intrinsic_value / total_shares * 100) if total_shares else None

        ratio = (intrinsic_value / current_market_cap) if current_market_cap else None
        price_upside = ((value_per_share / current_price - 1) * 100) if (value_per_share and current_price) else None

        # 隐含年化回报
        if current_market_cap and intrinsic_value:
            annual_return = (intrinsic_value / current_market_cap) ** (1/10) - 1
            annual_return_pct = round(annual_return * 100, 1)
        else:
            annual_return_pct = None

        if ratio:
            if ratio > 1.3:
                verdict = "🟢 明显便宜（安全边际>30%）"
            elif ratio > 1.1:
                verdict = "🟡 略有折价（安全边际10-30%）"
            elif ratio > 0.9:
                verdict = "🟠 基本合理（±10%）"
            elif ratio > 0.7:
                verdict = "🔴 偏贵（溢价10-30%）"
            else:
                verdict = "🔴 明显偏贵（溢价>30%）"
        else:
            verdict = "N/A"

        results[name] = {
            "yearly": yearly,
            "final_profit": round(profit, 1),
            "exit_value": round(exit_value, 1),
            "pv_exit_value": round(pv_exit_value, 1),
            "total_dividends_pv": round(total_dividends_pv, 1),
            "net_cash": net_cash,
            "intrinsic_value": round(intrinsic_value, 1),
            "value_per_share": round(value_per_share, 0) if value_per_share else None,
            "current_market_cap": current_market_cap,
            "exit_pe": exit_pe,
            "ratio": round(ratio, 2) if ratio else None,
            "price_upside": round(price_upside, 1) if price_upside else None,
            "annual_return_pct": annual_return_pct,
            "verdict": verdict,
            "discount_rate": discount_rate,
        }

    return results


def print_dcf_report(params, results):
    stock_name = params.get("stock_name", "目标公司")
    current_market_cap = params.get("current_market_cap")
    current_price = params.get("current_price")
    total_shares = params.get("total_shares")

    print("=" * 80)
    print(f"{'─' * 80}")
    print(f"{'【方法一】传统DCF折现 (Gordon永续模型)':^80}")
    print(f"{'─' * 80}")
    print(f"{stock_name} 十年DCF估值")
    if current_market_cap:
        print(f"当前市值: {current_market_cap}亿", end="")
    if current_price:
        print(f"  当前股价: {current_price}元", end="")
    if total_shares:
        print(f"  总股本: {total_shares}亿股", end="")
    print()

    for name, r in results.items():
        print(f"\n{'─' * 80}")
        print(f"【{name}情景】")
        print(f"{'─' * 80}")

        print(f"\n{'年份':<6} {'营收(亿)':<10} {'增速':<8} {'净利率':<8} {'净利润(亿)':<12} {'FCF(亿)':<10} {'折现FCF(亿)':<12}")
        print("-" * 80)
        for y in r["yearly"]:
            print(f"{y['year']:<6} {y['revenue']:<10.1f} {y['growth']:>5.1f}%   {y['net_margin']:>5.1f}%   {y['net_profit']:<12.1f} {y['fcf']:<10.1f} {y['pv_fcf']:<12.1f}")

        print(f"\n{'─' * 40}")
        print(f"10年FCF折现合计:    {r['total_fcf_pv']:>10.1f} 亿")
        print(f"终值折现:           {r['pv_terminal']:>10.1f} 亿")
        print(f"净现金:             {r['net_cash']:>10.1f} 亿")
        print(f"{'─' * 40}")
        print(f"内在价值:           {r['intrinsic_value']:>10.1f} 亿")
        if r["value_per_share"]:
            print(f"每股内在价值:       {r['value_per_share']:>10.0f} 元")
        if current_market_cap:
            print(f"当前市值:           {current_market_cap:>10d} 亿")
        if r["ratio"]:
            print(f"内在价值/市值:      {r['ratio']:>10.2f}")
        if r["price_upside"] is not None:
            print(f"股价空间:           {r['price_upside']:>9.1f}%")
        print(f"判断: {r['verdict']}")
        if r["payback_years"]:
            print(f"\n10年累计FCF: {r['total_fcf_10y']}亿  年均: {r['avg_annual_fcf']}亿  回本: {r['payback_years']}年")


def print_pe_exit_report(params, results):
    stock_name = params.get("stock_name", "目标公司")
    current_market_cap = params.get("current_market_cap")
    current_price = params.get("current_price")
    total_shares = params.get("total_shares")

    print(f"\n")
    print("=" * 80)
    print(f"{'─' * 80}")
    print(f"{'【方法二】段永平式PE退出法 (10年后净利润×PE+分红折现)':^80}")
    print(f"{'─' * 80}")
    print(f"{stock_name} 十年PE退出估值")
    print(f"\n核心逻辑: 10年后净利润 × 合理PE + 10年累计分红 → 折现到今天")
    print(f"折现率逻辑: 机会成本 = 你拿着现金存银行能赚多少（国债/定存利率）")
    if current_market_cap:
        print(f"当前市值: {current_market_cap}亿", end="")
    if current_price:
        print(f"  当前股价: {current_price}元", end="")
    if total_shares:
        print(f"  总股本: {total_shares}亿股", end="")
    print()

    for name, r in results.items():
        print(f"\n{'─' * 80}")
        print(f"【{name}情景】  (折现率={r['discount_rate']*100:.1f}%, 退出PE={r['exit_pe']}x)")
        print(f"{'─' * 80}")

        print(f"\n{'年份':<6} {'净利润(亿)':<12} {'增速':<8} {'当年分红(亿)':<14} {'分红折现(亿)':<14}")
        print("-" * 70)
        for y in r["yearly"]:
            print(f"{y['year']:<6} {y['profit']:<12.1f} {y['growth']:>5.1f}%    {y['dividend']:<14.1f} {y['pv_dividend']:<14.1f}")

        print(f"\n{'─' * 55}")
        print(f"10年后净利润:        {r['final_profit']:>10.1f} 亿")
        print(f"10年后市值(×{r['exit_pe']}x PE): {r['exit_value']:>10.1f} 亿")
        print(f"退出市值折现:        {r['pv_exit_value']:>10.1f} 亿")
        print(f"10年累计分红折现:    {r['total_dividends_pv']:>10.1f} 亿")
        print(f"净现金:              {r['net_cash']:>10.1f} 亿")
        print(f"{'─' * 55}")
        print(f"内在价值:            {r['intrinsic_value']:>10.1f} 亿")
        if r["value_per_share"]:
            print(f"每股内在价值:        {r['value_per_share']:>10.0f} 元")
        if current_market_cap:
            print(f"当前市值:            {current_market_cap:>10d} 亿")
        if r["ratio"]:
            print(f"内在价值/市值:       {r['ratio']:>10.2f}")
        if r["price_upside"] is not None:
            print(f"股价空间:            {r['price_upside']:>9.1f}%")
        if r["annual_return_pct"] is not None:
            print(f"隐含10年年化回报:    {r['annual_return_pct']:>9.1f}%")
        print(f"判断: {r['verdict']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="十年DCF估值计算器（支持DCF+PE退出双模式）")
    parser.add_argument("--json", type=str, help="JSON参数字符串")
    parser.add_argument("--config", type=str, help="JSON配置文件路径")
    parser.add_argument("--method", type=str, default="both",
                        choices=["dcf", "pe_exit", "both"],
                        help="计算方法: dcf(仅DCF) / pe_exit(仅PE退出) / both(两种都跑)")
    args = parser.parse_args()

    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            params = json.load(f)
    elif args.json:
        params = json.loads(args.json)
    else:
        print("请提供 --json 或 --config 参数")
        sys.exit(1)

    if args.method in ("dcf", "both"):
        results_dcf = calc_dcf(params)
        print_dcf_report(params, results_dcf)

    if args.method in ("pe_exit", "both"):
        results_pe = calc_pe_exit(params)
        print_pe_exit_report(params, results_pe)
