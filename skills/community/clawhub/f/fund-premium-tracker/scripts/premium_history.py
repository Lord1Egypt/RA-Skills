#!/usr/bin/env python3
"""
场内基金溢价率 - 历史查询（多源降级版）
降级链: 东方财富 → 新浪财经

用法：python3 premium_history.py <基金代码> [--days N]
示例：python3 premium_history.py 513050 --days 20
"""

import sys
import os
from datetime import datetime, timedelta

# 确保能import同目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_sources import create_sources, get_fund_history_klines, get_fund_nav


def fetch_history_nav_multi(fund_code: str, days: int, sources: list) -> dict:
    """获取历史净值（多源降级），返回 {日期: 净值} 字典"""
    # 尝试东方财富批量接口
    from data_sources import EastmoneySource, SinaSource
    page_size = days + 10

    errors = []
    for source in sources:
        try:
            if isinstance(source, EastmoneySource):
                from data_sources import http_get
                import json
                url = (
                    f"http://api.fund.eastmoney.com/f10/lsjz"
                    f"?fundCode={fund_code}&pageIndex=1&pageSize={page_size}"
                )
                ok, text, err = http_get(url, headers={"Referer": "http://fund.eastmoney.com/"})
                if ok:
                    data = json.loads(text)
                    nav_list = data.get("Data", {}).get("LSJZList", [])
                    if nav_list:
                        return {item["FSRQ"]: float(item["DWJZ"]) for item in nav_list}
                errors.append(f"东方财富({err or '无数据'})")

            elif isinstance(source, SinaSource):
                from data_sources import http_get
                import json
                url = (
                    f"http://stock.finance.sina.com.cn/fundInfo/api/openapi.php"
                    f"/CaihuiFundInfoService.getNav?symbol={fund_code}"
                    f"&datefrom=2020-01-01&dateto=2099-12-31"
                )
                ok, text, err = http_get(url)
                if ok:
                    data = json.loads(text)
                    nav_data = data.get("result", {}).get("data", {}).get("data", [])
                    if nav_data:
                        return {item["fbrq"][:10]: float(item["jjjz"]) for item in nav_data[:page_size]}
                errors.append(f"新浪财经({err or '无数据'})")
        except Exception as e:
            errors.append(f"{source.name}({e})")

    if errors:
        print(f"⚠️ 历史净值获取: {'; '.join(errors)}", file=sys.stderr)
    return {}


def match_nav_for_date(date: str, nav_dict: dict) -> float:
    """为某个交易日匹配净值。优先当日，否则向前找最近已公布净值。"""
    if date in nav_dict:
        return nav_dict[date]
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
        for i in range(1, 6):
            prev = (d - timedelta(days=i)).strftime("%Y-%m-%d")
            if prev in nav_dict:
                return nav_dict[prev]
    except Exception:
        pass
    return 0.0


def calc_premium(price: float, nav: float):
    """计算溢价率(%)"""
    if nav <= 0:
        return None
    return (price - nav) / nav * 100


def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python3 premium_history.py <基金代码> [--days N]")
        print("示例: python3 premium_history.py 513050 --days 20")
        print("\n默认显示最近 20 个交易日的溢价率变动")
        print("数据源: 东方财富(主) → 新浪财经(备)")
        sys.exit(1)

    fund_code = args[0].strip()
    days = 20

    for i, arg in enumerate(args[1:], 1):
        if arg == "--days" and i + 1 < len(args):
            try:
                days = int(args[i + 1])
            except ValueError:
                pass
        elif arg.startswith("--days="):
            try:
                days = int(arg.split("=")[1])
            except ValueError:
                pass

    if not fund_code.isdigit() or len(fund_code) != 6:
        print(f"❌ 无效代码: {fund_code}（需6位数字）")
        sys.exit(1)

    sources = create_sources()

    # 获取数据（自动降级）
    (name, klines), kline_src = get_fund_history_klines(fund_code, days, sources)
    nav_dict = fetch_history_nav_multi(fund_code, days, sources)

    if not klines:
        print(f"❌ 未获取到 {fund_code} 的历史行情数据（所有数据源均失败）")
        sys.exit(1)

    if not nav_dict:
        print(f"❌ 未获取到 {fund_code} 的历史净值数据（所有数据源均失败）")
        sys.exit(1)

    # 用name兜底
    if not name or name == fund_code:
        # 尝试从实时接口获取名称
        from data_sources import get_fund_realtime_price
        price_data, _ = get_fund_realtime_price(fund_code, sources)
        if "error" not in price_data:
            name = price_data.get("name", fund_code)

    # 计算每日溢价率
    records = []
    for k in klines:
        date = k["date"]
        close = k["close"]
        nav = match_nav_for_date(date, nav_dict)
        premium = calc_premium(close, nav)
        records.append({"date": date, "close": close, "nav": nav, "premium": premium})

    # 统计
    valid_premiums = [r["premium"] for r in records if r["premium"] is not None]

    # 输出
    print(f"\n📈 {name} ({fund_code}) 近{len(records)}个交易日溢价率")
    print(f"   数据源: K线={kline_src} | 净值=自动降级\n")
    print(f"{'日期':<12} {'收盘价':>8} {'净值':>8} {'溢价率':>8}  {'图示'}")
    print("-" * 60)

    for r in records:
        if r["premium"] is not None:
            sign = "+" if r["premium"] >= 0 else ""
            prem_str = f"{sign}{r['premium']:.2f}%"
            bar_len = min(int(abs(r["premium"]) * 2), 20)
            bar = "▓" * bar_len if r["premium"] >= 0 else "░" * bar_len
        else:
            prem_str = "N/A"
            bar = ""

        nav_str = f"{r['nav']:.4f}" if r["nav"] > 0 else "N/A"
        print(f"{r['date']:<12} {r['close']:>8.4f} {nav_str:>8} {prem_str:>8}  {bar}")

    if valid_premiums:
        avg_p = sum(valid_premiums) / len(valid_premiums)
        max_p = max(valid_premiums)
        min_p = min(valid_premiums)
        latest_p = valid_premiums[-1]

        print("-" * 60)
        print(f"  最新: {latest_p:+.2f}%  |  均值: {avg_p:+.2f}%  |  最高: {max_p:+.2f}%  |  最低: {min_p:+.2f}%")

        if len(valid_premiums) >= 3:
            recent_3 = valid_premiums[-3:]
            if recent_3[-1] > recent_3[0] + 1:
                trend = "📈 溢价扩大趋势"
            elif recent_3[-1] < recent_3[0] - 1:
                trend = "📉 溢价收窄/折价扩大趋势"
            else:
                trend = "➡️ 溢价率相对稳定"
            print(f"  趋势: {trend}")

        if latest_p > 5:
            print(f"\n  🚨 当前溢价率 {latest_p:+.2f}% 处于极端水平，场内买入风险较高")
        elif latest_p > 3:
            print(f"\n  ⚠️ 当前溢价率 {latest_p:+.2f}% 偏高，建议关注回落风险")
        elif latest_p < -3:
            print(f"\n  💡 当前折价率 {latest_p:.2f}%，可能存在套利机会")

    print()


if __name__ == "__main__":
    main()
