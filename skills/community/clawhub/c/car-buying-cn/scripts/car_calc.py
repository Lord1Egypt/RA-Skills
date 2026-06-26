#!/usr/bin/env python3
"""
买车计算器
用法:
  python3 car_calc.py 落地 15              # 15万预算能买什么车
  python3 car_calc.py 贷款 12 3 4.5        # 12万贷款3年利率4.5%
  python3 car_calc.py 养车 10 燃油         # 10万燃油车年养车成本
  python3 car_calc.py 对比 15 20           # 15万vs20万车对比
"""

import sys

def calc_loan_payment(principal: float, years: int, annual_rate: float) -> float:
    """等额本息月供计算"""
    monthly_rate = annual_rate / 100 / 12
    n = years * 12
    if monthly_rate == 0:
        return principal / n
    payment = principal * monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    return payment

def calc_purchase_price(budget: float, is_ev: bool = False) -> dict:
    """根据落地预算反推裸车价"""
    # 落地价 = 裸车价 + 购置税 + 保险 + 上牌
    # 购置税 = 裸车价 / 1.13 * 0.10 (新能源车为0)
    # 保险约 4000-6000
    # 上牌约 500
    
    insurance = 5000  # 预估
    registration = 500
    
    if is_ev:
        # 新能源无购置税
        car_price = budget - insurance - registration
        tax = 0
    else:
        # 燃油车有购置税
        # budget = car_price + car_price/1.13*0.10 + insurance + registration
        # budget = car_price * (1 + 0.10/1.13) + 5500
        # car_price = (budget - 5500) / 1.0885
        car_price = (budget - insurance - registration) / (1 + 0.10/1.13)
        tax = car_price / 1.13 * 0.10
    
    return {
        "裸车价": round(car_price, 2),
        "购置税": round(tax, 2),
        "保险费": insurance,
        "上牌费": registration,
        "落地价": round(car_price + tax + insurance + registration, 2),
    }

def calc_annual_cost(car_price: float, fuel_type: str = "燃油", km_per_year: float = 15000) -> dict:
    """计算年养车成本"""
    
    if fuel_type == "燃油":
        fuel_cost = km_per_year * 0.6  # 0.6元/km
        maintenance = 1500
    elif fuel_type == "新能源":
        fuel_cost = km_per_year * 0.15  # 0.15元/km
        maintenance = 800
    else:  # 混动
        fuel_cost = km_per_year * 0.35
        maintenance = 1200
    
    # 保险按车价比例
    if car_price <= 10:
        insurance = 3500
    elif car_price <= 20:
        insurance = 4500
    else:
        insurance = 5500
    
    parking = 4000  # 月均300-500
    washing = 800
    toll = 3000
    
    total = fuel_cost + insurance + maintenance + parking + washing + toll
    
    return {
        "油费/电费": round(fuel_cost, 2),
        "保险费": insurance,
        "保养费": maintenance,
        "停车费": parking,
        "洗车美容": washing,
        "过路费": toll,
        "年合计": round(total, 2),
        "月均": round(total / 12, 2),
    }

def calc_purchase_from_car(car_price: float, is_ev: bool = False) -> dict:
    """从裸车价计算落地价"""
    insurance = 5000
    registration = 500
    
    if is_ev:
        tax = 0
    else:
        tax = car_price * 10000 / 1.13 * 0.10 / 10000  # 万元
    
    total = car_price + tax + insurance/10000 + registration/10000
    
    return {
        "裸车价": round(car_price, 2),
        "购置税": round(tax, 2),
        "保险费": insurance,
        "上牌费": registration,
        "落地价": round(total, 2),
    }

def loan_calc(car_price: float, down_ratio: float, years: int, rate: float, is_ev: bool = False):
    """贷款购车计算"""
    purchase = calc_purchase_from_car(car_price, is_ev)
    
    # 贷款金额 = 裸车价 × (1 - 首付比例)
    loan_amount = purchase["裸车价"] * (1 - down_ratio)
    down_payment = purchase["裸车价"] * down_ratio + purchase["购置税"] + purchase["保险费"]/10000 + purchase["上牌费"]/10000
    
    monthly = calc_loan_payment(loan_amount * 10000, years, rate)
    total_payment = monthly * years * 12
    total_interest = total_payment - loan_amount * 10000
    
    print(f"\n{'='*50}")
    print(f"  🚗 贷款购车方案")
    print(f"{'='*50}")
    print(f"  裸车价:    {purchase['裸车价']:.1f} 万元")
    print(f"  购置税:    {purchase['购置税']:.1f} 万元")
    print(f"  保险费:    {purchase['保险费']:.0f} 元")
    print(f"  上牌费:    {purchase['上牌费']:.0f} 元")
    print(f"\n  {'─'*45}")
    print(f"  首付比例:  {down_ratio*100:.0f}%")
    print(f"  首付金额:  {down_payment:.1f} 万元")
    print(f"  贷款金额:  {loan_amount:.1f} 万元")
    print(f"  贷款年限:  {years} 年")
    print(f"  年利率:    {rate}%")
    print(f"\n  {'─'*45}")
    print(f"  月供:      {monthly:.0f} 元/月")
    print(f"  总利息:    {total_interest/10000:.1f} 万元")
    print(f"  总成本:    {(down_payment*10000 + total_payment)/10000:.1f} 万元")
    print(f"{'='*50}\n")

def budget_calc(monthly_income: float, down_payment: float, years: int = 3, rate: float = 4.5):
    """根据收入算可买车价"""
    # 月供上限 = 月收入 × 20%
    max_monthly = monthly_income * 0.2
    monthly_rate = rate / 100 / 12
    n = years * 12
    
    if monthly_rate > 0:
        max_loan = max_monthly * ((1 + monthly_rate)**n - 1) / (monthly_rate * (1 + monthly_rate)**n)
    else:
        max_loan = max_monthly * n
    
    # 反推裸车价（假设首付30%）
    # 落地价 = 裸车价 * 1.0885 + 5500
    # 贷款 = 裸车价 * 0.7
    # 裸车价 = 贷款 / 0.7
    max_car_price = max_loan / 0.7 / 10000  # 万
    
    print(f"\n{'='*50}")
    print(f"  💰 可负担车价计算")
    print(f"{'='*50}")
    print(f"  月收入:      {monthly_income:.0f} 元")
    print(f"  月供上限:    {max_monthly:.0f} 元（收入的20%）")
    print(f"  现有首付:    {down_payment:.0f} 万元")
    print(f"\n  {'─'*45}")
    print(f"  可贷款金额:  {max_loan/10000:.1f} 万元")
    print(f"  建议裸车价:  {max_car_price:.1f} 万元")
    print(f"  建议落地价:  {max_car_price*1.1:.1f} 万元")
    print(f"\n  💡 推荐车型价位：{max_car_price*0.8:.0f}-{max_car_price:.0f} 万")
    print(f"{'='*50}\n")

def compare_cars(price1: float, price2: float):
    """对比两款车的落地成本"""
    p1 = calc_purchase_from_car(price1)
    p2 = calc_purchase_from_car(price2)
    
    cost1 = calc_annual_cost(price1)
    cost2 = calc_annual_cost(price2)
    
    print(f"\n{'='*60}")
    print(f"  🆚 {price1:.0f}万 vs {price2:.0f}万 车型对比")
    print(f"{'='*60}")
    
    print(f"\n  {'─'*55}")
    print(f"  {'项目':<15} {price1:.0f}万车型      {price2:.0f}万车型")
    print(f"  {'─'*55}")
    print(f"  {'裸车价':<15} {p1['裸车价']:>8.1f}万      {p2['裸车价']:>8.1f}万")
    print(f"  {'购置税':<15} {p1['购置税']:>8.1f}万      {p2['购置税']:>8.1f}万")
    print(f"  {'落地价':<15} {p1['落地价']:>8.1f}万      {p2['落地价']:>8.1f}万")
    print(f"  {'─'*55}")
    print(f"  {'年油费':<15} {cost1['油费/电费']:>8.0f}元      {cost2['油费/电费']:>8.0f}元")
    print(f"  {'年保险':<15} {cost1['保险费']:>8.0f}元      {cost2['保险费']:>8.0f}元")
    print(f"  {'年保养':<15} {cost1['保养费']:>8.0f}元      {cost2['保养费']:>8.0f}元")
    print(f"  {'年合计':<15} {cost1['年合计']:>8.0f}元      {cost2['年合计']:>8.0f}元")
    print(f"  {'─'*55}")
    print(f"  {'差价':<15} {'':>8}        +{(p2['落地价']-p1['落地价']):.1f}万落地")
    print(f"  {'':<15} {'':>8}        +{(cost2['年合计']-cost1['年合计']):.0f}元/年")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 car_calc.py 落地 15              # 15万预算能买什么车")
        print("  python3 car_calc.py 贷款 12 0.3 3 4.5    # 12万车首付30%贷3年利率4.5%")
        print("  python3 car_calc.py 预算 15000 5         # 月入15000，首付5万，算可买车价")
        print("  python3 car_calc.py 养车 10 燃油         # 10万燃油车年养车成本")
        print("  python3 car_calc.py 对比 12 18           # 12万vs18万车型对比")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "落地":
        budget = float(sys.argv[2])
        is_ev = len(sys.argv) > 3 and sys.argv[3] == "新能源"
        result = calc_purchase_price(budget, is_ev)
        print(f"\n  {budget}万预算可买：")
        print(f"  裸车价: {result['裸车价']:.1f}万")
        print(f"  购置税: {result['购置税']:.1f}万")
        print(f"  保险费: {result['保险费']:.0f}元")
        print(f"  上牌费: {result['上牌费']:.0f}元")
        print(f"  ─────────────────")
        print(f"  落地价: {result['落地价']:.1f}万\n")
    
    elif cmd == "贷款":
        car_price = float(sys.argv[2])
        down_ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
        years = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        rate = float(sys.argv[5]) if len(sys.argv) > 5 else 4.5
        loan_calc(car_price, down_ratio, years, rate)
    
    elif cmd == "预算":
        income = float(sys.argv[2])
        down = float(sys.argv[3]) if len(sys.argv) > 3 else 5
        years = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        rate = float(sys.argv[5]) if len(sys.argv) > 5 else 4.5
        budget_calc(income, down, years, rate)
    
    elif cmd == "养车":
        price = float(sys.argv[2])
        fuel = sys.argv[3] if len(sys.argv) > 3 else "燃油"
        result = calc_annual_cost(price, fuel)
        print(f"\n  {price}万{fuel}车年养车成本：")
        for k, v in result.items():
            print(f"  {k}: {v:,.0f}元")
    
    elif cmd == "对比":
        p1 = float(sys.argv[2])
        p2 = float(sys.argv[3])
        compare_cars(p1, p2)
