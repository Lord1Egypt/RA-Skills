#!/usr/bin/env python3
"""
场内基金溢价率 - 实时查询（多源降级版）
降级链: 东方财富 → 新浪财经 → 腾讯财经

用法：python3 premium_realtime.py <基金代码> [基金代码2 ...]
示例：python3 premium_realtime.py 513050 159915 164824
"""

import sys
import os
from datetime import datetime

# 确保能import同目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_sources import (
    create_sources, get_fund_realtime_price,
    get_fund_nav, get_fund_intraday_estimate
)


def calc_premium(price: float, nav: float) -> float:
    """计算溢价率(%)"""
    if nav <= 0:
        return 0.0
    return (price - nav) / nav * 100


def premium_level(pct: float) -> str:
    """溢价率等级标注"""
    abs_pct = abs(pct)
    if abs_pct < 1:
        return "正常"
    elif abs_pct < 3:
        return "轻微" + ("溢价" if pct > 0 else "折价")
    elif abs_pct < 5:
        return "⚠️ 较高" + ("溢价" if pct > 0 else "折价")
    else:
        return "🚨 极端" + ("溢价" if pct > 0 else "折价")


def query_one(fund_code: str, sources: list) -> str:
    """查询单只基金的实时溢价率"""
    # 1. 获取实时价格
    price_data, price_src = get_fund_realtime_price(fund_code, sources)
    if "error" in price_data:
        return f"❌ {fund_code}: {price_data['error']}"

    # 2. 获取净值
    nav_data, nav_src = get_fund_nav(fund_code, sources)
    if "error" in nav_data:
        return f"❌ {fund_code}: {nav_data['error']}"

    # 3. 尝试获取盘中估值
    estimate, est_src = get_fund_intraday_estimate(fund_code, sources)

    price = price_data["price"]
    name = price_data["name"]

    # 计算溢价率
    if estimate.get("available") and estimate["estimated_nav"] > 0:
        ref_nav = estimate["estimated_nav"]
        nav_label = "盘中估值"
    else:
        ref_nav = nav_data["nav"]
        nav_label = f"净值({nav_data['nav_date']})"

    premium_pct = calc_premium(price, ref_nav)
    level = premium_level(premium_pct)

    # 数据源标注
    src_info = f"行情:{price_src}"
    if estimate.get("available"):
        src_info += f" | 估值:东方财富"
    else:
        src_info += f" | 净值:{nav_src}"

    # 格式化输出
    sign = "+" if premium_pct >= 0 else ""
    lines = [
        f"📊 {name} ({fund_code})",
        f"   场内价: {price:.4f}  |  {nav_label}: {ref_nav:.4f}",
        f"   溢价率: {sign}{premium_pct:.2f}%  [{level}]",
        f"   涨跌幅: {price_data['change_pct']:+.2f}%  |  昨收: {price_data['prev_close']:.4f}",
    ]

    # 如果有盘中估值，补充显示最新公布净值
    if estimate.get("available"):
        nav_premium = calc_premium(price, nav_data["nav"])
        lines.append(
            f"   参考净值({nav_data['nav_date']}): {nav_data['nav']:.4f}  "
            f"(vs净值溢价: {nav_premium:+.2f}%)"
        )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"   数据源: [{src_info}]")
    lines.append(f"   查询时间: {now}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 premium_realtime.py <基金代码> [基金代码2 ...]")
        print("示例: python3 premium_realtime.py 513050 159915 164824")
        print("\n支持类型: ETF(51/15开头) LOF(16开头) QDII场内份额")
        print("数据源: 东方财富(主) → 新浪财经(备) → 腾讯财经(备)")
        sys.exit(1)

    codes = sys.argv[1:]
    sources = create_sources()
    results = []

    for code in codes:
        code = code.strip()
        if not code.isdigit() or len(code) != 6:
            results.append(f"❌ {code}: 无效代码（需6位数字）")
            continue
        results.append(query_one(code, sources))

    print("\n" + "\n\n".join(results) + "\n")


if __name__ == "__main__":
    main()
