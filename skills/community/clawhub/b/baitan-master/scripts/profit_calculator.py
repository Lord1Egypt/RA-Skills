#!/usr/bin/env python3
"""
摆摊利润精算器 - 多维度成本核算与盈亏分析
用法: python profit_calculator.py --revenue 800 --food-cost 280 --rent 50 --equipment 3000 --days 90
"""

import argparse
import json
import sys
from typing import Dict, Any


def calculate_profit(
    daily_revenue: float = 0,
    food_cost: float = 0,
    rent_cost: float = 0,
    equipment_total: float = 0,
    equipment_days: int = 90,
    labor_cost: float = 0,
    loss_rate: float = 0.05,
    misc_cost: float = 0,
    working_days_per_month: int = 26,
) -> Dict[str, Any]:
    """
    全面计算摆摊利润

    Args:
        daily_revenue: 日均营业额
        food_cost: 日均食材成本
        rent_cost: 日均摊位费
        equipment_total: 设备总投资
        equipment_days: 设备预计使用天数
        labor_cost: 日均人工成本（如请帮手）
        loss_rate: 损耗率（默认5%）
        misc_cost: 日均其他杂费（水电/卫生费）
        working_days_per_month: 月均出摊天数
    """

    # 日成本明细
    equipment_daily = equipment_total / equipment_days if equipment_days > 0 else 0
    loss_cost = daily_revenue * loss_rate
    total_daily_cost = (
        food_cost + rent_cost + equipment_daily + labor_cost + loss_cost + misc_cost
    )

    # 日利润
    daily_profit = daily_revenue - total_daily_cost
    daily_margin = (daily_profit / daily_revenue * 100) if daily_revenue > 0 else 0

    # 月利润
    monthly_revenue = daily_revenue * working_days_per_month
    monthly_cost = total_daily_cost * working_days_per_month
    monthly_profit = daily_profit * working_days_per_month

    # 年利润
    yearly_revenue = monthly_revenue * 12
    yearly_profit = monthly_profit * 12

    # 盈亏平衡分析
    fixed_daily_cost = rent_cost + equipment_daily + labor_cost + misc_cost
    variable_rate = (
        (food_cost + loss_cost) / daily_revenue if daily_revenue > 0 else 0
    )
    breakeven_revenue = (
        fixed_daily_cost / (1 - variable_rate) if variable_rate < 1 else float("inf")
    )
    breakeven_units = (
        breakeven_revenue / (daily_revenue / max(1, daily_revenue // 10))
        if daily_revenue > 0
        else 0
    )

    # 回本周期
    total_investment = equipment_total
    if daily_profit > 0:
        payback_days = total_investment / daily_profit
        payback_working_days = payback_days
    else:
        payback_days = float("inf")
        payback_working_days = float("inf")

    # 成本结构占比
    cost_breakdown = {}
    if total_daily_cost > 0:
        cost_breakdown["食材成本"] = round(food_cost / total_daily_cost * 100, 1)
        cost_breakdown["摊位费"] = round(rent_cost / total_daily_cost * 100, 1)
        cost_breakdown["设备折旧"] = round(equipment_daily / total_daily_cost * 100, 1)
        cost_breakdown["人工成本"] = round(labor_cost / total_daily_cost * 100, 1)
        cost_breakdown["损耗"] = round(loss_cost / total_daily_cost * 100, 1)
        cost_breakdown["其他杂费"] = round(misc_cost / total_daily_cost * 100, 1)

    # 健康度评级
    if daily_margin >= 35:
        health = "优秀 🟢"
        advice = "利润空间充足，可考虑扩大规模或增加品类"
    elif daily_margin >= 20:
        health = "良好 🟡"
        advice = "利润健康，建议优化成本结构提升空间"
    elif daily_margin >= 10:
        health = "一般 🟠"
        advice = "利润偏薄，需重点降低食材成本或提高售价"
    elif daily_margin > 0:
        health = "危险 🔴"
        advice = "几乎无利可图，必须立即调整经营策略"
    else:
        health = "亏损 ⛔"
        advice = "正在亏损！建议停业或彻底转型"

    # 优化建议
    optimizations = []
    if food_cost / daily_revenue > 0.40 if daily_revenue > 0 else False:
        optimizations.append("食材成本占比过高（>{:.0f}%），建议优化供应链或多供应商比价".format(food_cost / daily_revenue * 100))
    if rent_cost / daily_revenue > 0.20 if daily_revenue > 0 else False:
        optimizations.append("摊位费占比过高（>{:.0f}%），考虑换更低成本位置或与物业协商".format(rent_cost / daily_revenue * 100))
    if loss_rate > 0.08:
        optimizations.append("损耗率偏高（>{:.0f}%），建议采用滚动采购法降低损耗".format(loss_rate * 100))
    if daily_margin < 15 and daily_revenue > 0:
        optimizations.append("整体利润率偏低，考虑：1)提价5-10% 2)增加高毛利搭配品 3)降低成本")

    result = {
        "inputs": {
            "daily_revenue": daily_revenue,
            "food_cost": food_cost,
            "rent_cost": rent_cost,
            "equipment_total": equipment_total,
            "equipment_days": equipment_days,
            "labor_cost": labor_cost,
            "loss_rate": loss_rate,
            "misc_cost": misc_cost,
            "working_days_per_month": working_days_per_month,
        },
        "daily": {
            "total_cost": round(total_daily_cost, 2),
            "profit": round(daily_profit, 2),
            "margin_pct": round(daily_margin, 1),
            "cost_breakdown": cost_breakdown,
        },
        "monthly": {
            "revenue": round(monthly_revenue, 2),
            "cost": round(monthly_cost, 2),
            "profit": round(monthly_profit, 2),
        },
        "yearly": {
            "revenue": round(yearly_revenue, 2),
            "profit": round(yearly_profit, 2),
        },
        "breakeven": {
            "daily_revenue_needed": round(breakeven_revenue, 2),
            "fixed_daily_cost": round(fixed_daily_cost, 2),
            "variable_rate_pct": round(variable_rate * 100, 1),
        },
        "payback": {
            "total_investment": total_investment,
            "days": round(payback_days, 1) if payback_days != float("inf") else "无法回本",
            "working_days": round(payback_working_days, 1) if payback_working_days != float("inf") else "无法回本",
        },
        "assessment": {
            "health": health,
            "advice": advice,
            "optimizations": optimizations,
        },
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="摆摊利润精算器")
    parser.add_argument("--revenue", type=float, default=0, help="日均营业额（元）")
    parser.add_argument("--food-cost", type=float, default=0, help="日均食材成本（元）")
    parser.add_argument("--rent", type=float, default=0, help="日均摊位费（元）")
    parser.add_argument("--equipment", type=float, default=0, help="设备总投资（元）")
    parser.add_argument("--equipment-days", type=int, default=90, help="设备预计使用天数")
    parser.add_argument("--labor", type=float, default=0, help="日均人工成本（元）")
    parser.add_argument("--loss-rate", type=float, default=0.05, help="损耗率（默认5%%）")
    parser.add_argument("--misc", type=float, default=0, help="日均其他杂费（元）")
    parser.add_argument("--working-days", type=int, default=26, help="月均出摊天数")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    if args.revenue <= 0:
        print(json.dumps({"error": "日均营业额必须大于0"}, ensure_ascii=False))
        sys.exit(1)

    result = calculate_profit(
        daily_revenue=args.revenue,
        food_cost=args.food_cost,
        rent_cost=args.rent,
        equipment_total=args.equipment,
        equipment_days=args.equipment_days,
        labor_cost=args.labor,
        loss_rate=args.loss_rate,
        misc_cost=args.misc,
        working_days_per_month=args.working_days,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print("📊 摆摊利润精算报告")
        print("=" * 50)
        print(f"\n💰 日营收: ¥{result['daily']['profit']:.2f}  (利润率: {result['daily']['margin_pct']}%)")
        print(f"📅 月利润: ¥{result['monthly']['profit']:.2f}  (出摊{args.working_days}天)")
        print(f"📆 年利润: ¥{result['yearly']['profit']:.2f}")
        print(f"\n📉 盈亏平衡点: 日营收需≥¥{result['breakeven']['daily_revenue_needed']:.2f}")
        print(f"🔄 回本周期: {result['payback']['days']}天")
        print(f"\n🏥 经营健康度: {result['assessment']['health']}")
        print(f"💡 {result['assessment']['advice']}")
        if result['assessment']['optimizations']:
            print("\n🔧 优化建议:")
            for opt in result['assessment']['optimizations']:
                print(f"  • {opt}")
        print("=" * 50)


if __name__ == "__main__":
    main()
