#!/usr/bin/env python3
"""
Amazon Ads Calculator & Bid Optimizer
Calculates ACoS, ROAS, break-even CPC, and provides bid guardrails
with flywheel optimization recommendations.

Usage:
    python ads-calculator.py --revenue 10000 --ad-spend 2800 --product-cost 4000 --other-costs 500
    python ads-calculator.py --input '{"revenue":10000,"ad_spend":2800,"product_cost":4000,"other_costs":500,"target_acos":18}'
"""

import argparse
import json
import sys
from datetime import datetime


# ── Benchmarks ───────────────────────────────────────────────────

ACoS_ZONES = {
    "profitable": (0, 15),      # Strongly profitable
    "healthy": (15, 22),        # Healthy range
    "caution": (22, 30),        # Needs optimization
    "danger": (30, 100),        # Losing money on ads
}

FLYWHEEL_THRESHOLDS = {
    "strong": 0.35,    # Organic >35% of total = strong flywheel
    "emerging": 0.20,  # Organic 20-35% = emerging
    "weak": 0.0,       # Organic <20% = weak
}

BID_POSITION_RANGES = {
    # (min_bid, max_bid, target_position_range)
    "top_of_search": (1.5, 5.0, (1, 3)),
    "first_page": (0.75, 2.5, (4, 10)),
    "rest_of_search": (0.30, 1.0, (11, 50)),
}

# Category ACoS benchmarks
CATEGORY_BENCHMARKS = {
    "electronics": {"avg_acos": 25, "good_acos": 15},
    "home_kitchen": {"avg_acos": 22, "good_acos": 14},
    "clothing": {"avg_acos": 28, "good_acos": 18},
    "beauty": {"avg_acos": 20, "good_acos": 12},
    "sports": {"avg_acos": 24, "good_acos": 16},
    "toys": {"avg_acos": 26, "good_acos": 17},
    "default": {"avg_acos": 25, "good_acos": 16},
}


# ── Calculation Functions ────────────────────────────────────────

def calc_acos(ad_spend: float, revenue: float) -> float:
    """ACoS = Ad Spend / Revenue * 100"""
    if revenue == 0:
        return 0.0
    return round((ad_spend / revenue) * 100, 2)


def calc_roas(ad_spend: float, revenue: float) -> float:
    """ROAS = Revenue / Ad Spend"""
    if ad_spend == 0:
        return 0.0
    return round(revenue / ad_spend, 2)


def calc_profit_margin(revenue: float, product_cost: float, other_costs: float, ad_spend: float) -> float:
    """Net profit margin %"""
    if revenue == 0:
        return 0.0
    profit = revenue - product_cost - other_costs - ad_spend
    return round((profit / revenue) * 100, 2)


def calc_break_even_cpc(revenue: float, product_cost: float, other_costs: float, conv_rate: float, total_units: int = 100) -> float:
    """Maximum CPC you can pay without losing money per click.
    Break-even CPC = Profit per sale * Conversion Rate
    profit_per_sale = (Revenue - Product Cost - Other Costs) / total_units
    """
    if conv_rate == 0 or total_units == 0:
        return 0.0
    profit_per_sale = (revenue - product_cost - other_costs) / total_units
    return round(profit_per_sale * conv_rate, 2)


def calc_target_cpc(break_even_cpc: float, target_acos: float, current_acos: float) -> float:
    """Calculate target CPC based on desired ACoS.
    Target CPC = Break-even CPC * (Target ACoS / Current ACoS)
    """
    if current_acos == 0:
        return break_even_cpc * 0.7  # Conservative default
    ratio = target_acos / current_acos
    return round(break_even_cpc * min(ratio, 1.0), 2)


def classify_acos(acos: float) -> str:
    """Classify ACoS into zone."""
    for zone, (low, high) in ACoS_ZONES.items():
        if low <= acos < high:
            return zone
    return "danger"


def calc_flywheel_health(organic_revenue: float, total_revenue: float) -> dict:
    """Calculate flywheel effect health."""
    if total_revenue == 0:
        return {"ratio": 0, "status": "weak"}

    ratio = organic_revenue / total_revenue
    if ratio >= FLYWHEEL_THRESHOLDS["strong"]:
        status = "strong"
    elif ratio >= FLYWHEEL_THRESHOLDS["emerging"]:
        status = "emerging"
    else:
        status = "weak"

    return {"ratio": round(ratio, 3), "status": status}


def generate_bid_recommendations(acos: float, break_even_cpc: float, category: str) -> dict:
    """Generate bid recommendations based on ACoS zone."""
    zone = classify_acos(acos)
    benchmark = CATEGORY_BENCHMARKS.get(category, CATEGORY_BENCHMARKS["default"])

    recommendations = {}
    if zone == "profitable":
        recommendations = {
            "strategy": "Aggressive Growth",
            "top_bid_max": round(break_even_cpc * 0.85, 2),
            "first_page_bid_max": round(break_even_cpc * 0.60, 2),
            "ros_bid_max": round(break_even_cpc * 0.30, 2),
            "position_strategy": "Push for Top of Search on high-converting keywords",
            "budget_action": "Increase daily budget by 15-20% for winning campaigns",
        }
    elif zone == "healthy":
        recommendations = {
            "strategy": "Balanced Optimization",
            "top_bid_max": round(break_even_cpc * 0.70, 2),
            "first_page_bid_max": round(break_even_cpc * 0.45, 2),
            "ros_bid_max": round(break_even_cpc * 0.20, 2),
            "position_strategy": "Maintain Top of Search, optimize first page presence",
            "budget_action": "Maintain current budget, shift spend to high-converting keywords",
        }
    elif zone == "caution":
        recommendations = {
            "strategy": "Defensive Optimization",
            "top_bid_max": round(break_even_cpc * 0.50, 2),
            "first_page_bid_max": round(break_even_cpc * 0.35, 2),
            "ros_bid_max": round(break_even_cpc * 0.15, 2),
            "position_strategy": "Reduce Top of Search bids, focus on first page",
            "budget_action": "Cut budget on low-converting campaigns by 25-30%",
        }
    else:  # danger
        recommendations = {
            "strategy": "Emergency Cost Control",
            "top_bid_max": round(break_even_cpc * 0.35, 2),
            "first_page_bid_max": round(break_even_cpc * 0.20, 2),
            "ros_bid_max": round(break_even_cpc * 0.10, 2),
            "position_strategy": "Pause all Top of Search bids, run only proven keywords",
            "budget_action": "Cut budget by 40-50%, pause underperforming campaigns",
        }

    recommendations["zone"] = zone
    recommendations["benchmark_acos"] = benchmark["avg_acos"]
    recommendations["target_acos"] = benchmark["good_acos"]

    return recommendations


def analyze(params: dict) -> dict:
    """Run full ad performance analysis."""
    revenue = float(params.get("revenue", 0))
    ad_spend = float(params.get("ad_spend", 0))
    product_cost = float(params.get("product_cost", 0))
    other_costs = float(params.get("other_costs", 0))
    conv_rate = float(params.get("conversion_rate", 0.10))  # Default 10%
    organic_revenue = float(params.get("organic_revenue", 0))
    category = params.get("category", "default")
    target_acos = float(params.get("target_acos", 18))
    total_units = int(params.get("total_units", 100))

    # Core metrics
    acos = calc_acos(ad_spend, revenue)
    roas = calc_roas(ad_spend, revenue)
    profit_margin = calc_profit_margin(revenue, product_cost, other_costs, ad_spend)
    break_even_cpc = calc_break_even_cpc(revenue, product_cost, other_costs, conv_rate, total_units)
    target_cpc = calc_target_cpc(break_even_cpc, target_acos, acos)
    zone = classify_acos(acos)
    flywheel = calc_flywheel_health(organic_revenue, revenue)
    bids = generate_bid_recommendations(acos, break_even_cpc, category)

    return {
        "metrics": {
            "revenue": revenue,
            "ad_spend": ad_spend,
            "product_cost": product_cost,
            "other_costs": other_costs,
            "acos": acos,
            "roas": roas,
            "profit_margin": profit_margin,
            "break_even_cpc": break_even_cpc,
            "target_cpc": target_cpc,
        },
        "classification": {
            "zone": zone,
            "zone_cn": {"profitable": "盈利区", "healthy": "健康区", "caution": "警戒区", "danger": "危险区"}.get(zone, zone),
            "flywheel": flywheel,
        },
        "bids": bids,
        "timestamp": datetime.now().isoformat(),
    }


def format_report(result: dict) -> str:
    """Format analysis result as readable report."""
    m = result["metrics"]
    c = result["classification"]
    b = result["bids"]
    zone_emoji = {"profitable": "🟢", "healthy": "🟡", "caution": "🟠", "danger": "🔴"}

    lines = []
    lines.append("📊 广告绩效分析报告")
    lines.append("━" * 40)
    lines.append("")
    lines.append("【核心指标】")
    lines.append(f"  总收入：      ${m['revenue']:,.0f}")
    lines.append(f"  广告花费：    ${m['ad_spend']:,.0f}")
    lines.append(f"  ACoS：       {m['acos']:.1f}%  {zone_emoji.get(c['zone'], '⚪')} {c['zone_cn']}")
    lines.append(f"  ROAS：       {m['roas']:.2f}x")
    lines.append(f"  利润率：      {m['profit_margin']:.1f}%")
    lines.append(f"  盈亏平衡CPC： ${m['break_even_cpc']:.2f}")
    lines.append(f"  目标CPC：     ${m['target_cpc']:.2f}")
    lines.append("")

    lines.append("【竞价护栏】")
    lines.append(f"  策略：{b.get('strategy', 'N/A')}")
    lines.append(f"  搜索顶部最高出价：${b.get('top_bid_max', 0):.2f}")
    lines.append(f"  首页最高出价：    ${b.get('first_page_bid_max', 0):.2f}")
    lines.append(f"  其余位置最高出价：${b.get('ros_bid_max', 0):.2f}")
    lines.append(f"  位置策略：{b.get('position_strategy', 'N/A')}")
    lines.append(f"  预算建议：{b.get('budget_action', 'N/A')}")
    lines.append("")

    fw = c.get("flywheel", {})
    if fw:
        fw_cn = {"strong": "🟢 强劲飞轮", "emerging": "🟡 飞轮形成中", "weak": "🔴 飞轮效应弱"}
        lines.append("【飞轮效应】")
        lines.append(f"  自然订单占比：{fw.get('ratio', 0)*100:.1f}%")
        lines.append(f"  状态：{fw_cn.get(fw.get('status', 'weak'), 'N/A')}")

    lines.append("")
    lines.append(f"  品类基准ACoS：{b.get('benchmark_acos', 'N/A')}%")
    lines.append(f"  目标ACoS：{b.get('target_acos', 'N/A')}%")

    lines.append("")
    lines.append("━" * 40)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Amazon Ads Calculator & Bid Optimizer")
    parser.add_argument("--revenue", type=float, required=True, help="Total revenue")
    parser.add_argument("--ad-spend", type=float, required=True, help="Total ad spend")
    parser.add_argument("--product-cost", type=float, default=0, help="Product cost (COGS)")
    parser.add_argument("--other-costs", type=float, default=0, help="Other costs (FBA, shipping, etc)")
    parser.add_argument("--conversion-rate", type=float, default=0.10, help="Ad conversion rate (default 0.10)")
    parser.add_argument("--organic-revenue", type=float, default=0, help="Revenue from organic sales")
    parser.add_argument("--category", default="default", help="Product category for benchmark")
    parser.add_argument("--target-acos", type=float, default=18, help="Target ACoS percentage")
    parser.add_argument("--total-units", type=int, default=100, help="Total units sold (for CPC calculation)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--input", type=str, help="JSON string with all parameters")

    args = parser.parse_args()

    if args.input:
        params = json.loads(args.input)
    else:
        params = {
            "revenue": args.revenue,
            "ad_spend": args.ad_spend,
            "product_cost": args.product_cost,
            "other_costs": args.other_costs,
            "conversion_rate": args.conversion_rate,
            "organic_revenue": args.organic_revenue,
            "category": args.category,
            "target_acos": args.target_acos,
            "total_units": args.total_units,
        }

    result = analyze(params)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
