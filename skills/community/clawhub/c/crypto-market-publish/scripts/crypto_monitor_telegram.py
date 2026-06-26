#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密市场综合监控 - 发送 Telegram 版本
功能：价格监控 + 经济数据预告 + 发送到 Telegram
"""

import os
import sys
import requests
from datetime import datetime

# 添加工作目录到路径
sys.path.insert(0, '/root/.openclaw/workspace/crypto/economic')

from economic_calendar import EconomicCalendar, EconomicNotifier

# 监控的代币（排名前十，排除稳定币）
TOKENS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'XRP': 'ripple',
    'BNB': 'binancecoin',
    'SOL': 'solana',
    'USDC': 'usd-coin',  # 稳定币（监控但不显示详情）
    'ADA': 'cardano',
    'AVAX': 'avalanche-2',
    'DOGE': 'dogecoin',
    'TRX': 'tron',
    'LINK': 'chainlink',
    'SUI': 'sui',  # 新增
    'WLFI': 'world-liberty-financial',  # 新增
    'XAU': 'tether-gold'  # 新增（黄金代币）
}

# 排除稳定币
STABLECOINS = {'USDC', 'USDT', 'USDD', 'BUSD', 'DAI', 'TUSD', 'FRAX', 'USDP'}

# 预警阈值（±5%）
ALERT_THRESHOLD = 5.0

def get_crypto_prices():
    """获取加密货币价格数据（包含 sparkline 数据用于计算 EMA）"""
    ids = ','.join(TOKENS.values())
    url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&sparkline=true&price_change_percentage=1h,24h,7d,30d'

    # 尝试 CoinGecko API（最多重试 2 次）
    for attempt in range(3):
        try:
            print(f"尝试从 CoinGecko API 获取数据 (第 {attempt + 1}/3 次)...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            print("✅ CoinGecko API 数据获取成功")
            return data
        except Exception as e:
            print(f"⚠️ CoinGecko API 获取失败: {e}")
            if attempt < 2:
                import time
                time.sleep(2)  # 等待 2 秒后重试

    # CoinGecko API 失败，使用 Binance API 作为备用
    print("📡 切换到 Binance API 备用数据源...")
    return get_crypto_prices_from_binance()

def get_crypto_prices_from_binance():
    """从 Binance API 获取加密货币价格数据（备用数据源）"""
    try:
        # 获取 24 小时价格变化
        ticker_url = 'https://api.binance.com/api/v3/ticker/24hr'
        response = requests.get(ticker_url, timeout=10)
        response.raise_for_status()
        tickers = response.json()

        # 过滤我们需要关注的代币
        result = []
        token_symbols = {k.upper(): k for k in TOKENS.keys()}

        for ticker in tickers:
            symbol = ticker['symbol']
            # 只关注 USDT 交易对
            if not symbol.endswith('USDT'):
                continue

            base = symbol.replace('USDT', '')
            if base in token_symbols:
                result.append({
                    'id': token_symbols[base],
                    'symbol': base.lower(),
                    'name': base,
                    'current_price': float(ticker['lastPrice']),
                    'price_change_percentage_24h': float(ticker['priceChangePercent']),
                    'high_24h': float(ticker['highPrice']),
                    'low_24h': float(ticker['lowPrice']),
                    'volume': float(ticker['quoteVolume']),
                    'market_cap': 0,  # Binance 不提供市值数据
                    'sparkline_in_7d': {'price': []}  # 无 sparkline 数据
                })

        print("✅ Binance API 数据获取成功")
        return sorted(result, key=lambda x: x['volume'], reverse=True)

    except Exception as e:
        print(f"❌ Binance API 也失败了: {e}")
        return []

def get_global_market_data():
    """获取全球市场数据"""
    try:
        url = 'https://api.coingecko.com/api/v3/global'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()['data']
    except Exception as e:
        print(f"Error fetching global data: {e}")
        return None

def format_price(price):
    """格式化价格显示"""
    if price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.2f}"
    else:
        return f"${price:.4f}"

def format_volume(volume):
    """格式化交易量"""
    if volume >= 1e12:
        return f"${volume/1e12:.2f}T"
    elif volume >= 1e9:
        return f"${volume/1e9:.2f}B"
    elif volume >= 1e6:
        return f"${volume/1e6:.2f}M"
    else:
        return f"${volume:,.0f}"

def format_market_cap(mcap):
    """格式化市值"""
    if mcap >= 1e12:
        return f"${mcap/1e12:.2f}T"
    elif mcap >= 1e9:
        return f"${mcap/1e9:.2f}B"
    else:
        return f"${mcap:,.0f}"

def check_alerts(crypto_data):
    """检查价格波动预警"""
    alerts = []

    for crypto in crypto_data:
        name = crypto['symbol'].upper()
        price = crypto['current_price']
        change_24h = crypto.get('price_change_percentage_24h', 0)

        if abs(change_24h) >= ALERT_THRESHOLD:
            direction = "🚀" if change_24h > 0 else "⚠️"
            alerts.append({
                'name': name,
                'price': price,
                'change': change_24h,
                'direction': direction
            })

    return alerts

def get_market_sentiment(crypto_data):
    """获取市场情绪（排除稳定币）"""
    non_stable = [c for c in crypto_data if c['symbol'].upper() not in STABLECOINS]
    positive = sum(1 for c in non_stable if c.get('price_change_percentage_24h', 0) > 0)
    total = len(non_stable)
    ratio = positive / total if total > 0 else 0

    if ratio >= 0.8:
        return "🚀 极度贪婪"
    elif ratio >= 0.6:
        return "📈 贪婪"
    elif ratio >= 0.4:
        return "😐 中性"
    elif ratio >= 0.2:
        return "📉 恐惧"
    else:
        return "😱 极度恐惧"

def generate_market_report(crypto_data, global_data, alerts):
    """生成市场报告"""
    report = []

    # 标题
    report.append("=" * 55)
    report.append(f"📊 加密市场监控 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 55)
    report.append("")

    # 全球市场概况
    if global_data:
        report.append("🌍 全球市场概况")
        report.append("-" * 55)
        report.append(f"总市值: {format_market_cap(global_data['total_market_cap']['usd'])} "
                     f"({global_data['market_cap_change_percentage_24h_usd']:+.2f}%)")
        report.append(f"24h交易量: {format_volume(global_data['total_volume']['usd'])}")
        report.append(f"BTC主导: {global_data['market_cap_percentage']['btc']:.1f}%")
        report.append("")

    # 市场情绪
    sentiment = get_market_sentiment(crypto_data)
    report.append(f"😊 市场情绪: {sentiment}")
    report.append("-" * 55)
    report.append("")

    # 价格预警
    if alerts:
        report.append("⚠️ 价格波动预警（±5%）：")
        report.append("-" * 55)
        for alert in alerts:
            report.append(f"{alert['direction']} {alert['name']}: 24h涨跌 {alert['change']:+.2f}%")
            report.append(f"    当前价格: {format_price(alert['price'])}")
        report.append("")
    else:
        report.append("✅ 无价格预警（24h涨跌幅 < 5%）")
        report.append("")

    # 主流代币详情（排除稳定币）
    report.append("💰 主流代币")
    report.append("-" * 55)
    report.append(f"{'币种':<8} {'价格':>15} {'24h':>8} {'7d':>8} {'市值':>12}")
    report.append("-" * 55)

    for crypto in crypto_data:
        # 跳过稳定币
        if crypto['symbol'].upper() in STABLECOINS:
            continue

        name = crypto['symbol'].upper()
        price = crypto['current_price']
        change_24h = crypto.get('price_change_percentage_24h', 0)
        change_7d = crypto.get('price_change_percentage_7d_in_currency', 0)
        mcap = crypto.get('market_cap', 0)

        # 价格趋势 emoji
        if change_24h >= 5:
            trend = "🚀"
        elif change_24h > 0:
            trend = "📈"
        elif change_24h <= -5:
            trend = "📉"
        else:
            trend = "➡️"

        report.append(f"{trend} {name:<6} {format_price(price):>15} {change_24h:+7.2f}% {change_7d:+7.2f}% "
                     f"{format_market_cap(mcap):>12}")

    report.append("")
    report.append("=" * 55)

    return "\n".join(report)

def generate_economic_report():
    """生成经济数据报告（简化版）"""
    sys.path.insert(0, '/root/.openclaw/workspace/crypto/economic')
    from economic_analyzer import EconomicDataAnalyzer

    calendar = EconomicCalendar()
    analyzer = EconomicDataAnalyzer()

    # 检查24小时内的事件
    notifier = EconomicNotifier()
    imminent = notifier.calendar.check_imminent_events(hours=24)

    if not imminent:
        return None

    # 构建报告
    lines = ["\n\n📅 经济数据提醒"]

    # 加载实际值数据
    actual_data = analyzer.load_actual_data()

    for event in imminent["events"]:
        lines.append(f"\n{event['emoji']} **{event['name']}**")
        lines.append(f"🕐 {event['datetime']}")
        lines.append(f"📊 预期: {event.get('expected', 'N/A')}")

        # 如果有实际值，进行分析
        event_key = event['name']
        if event_key in actual_data:
            actual_value = actual_data[event_key].get('actual', '')
            event_with_actual = event.copy()
            event_with_actual['actual'] = actual_value

            analysis = analyzer.analyze_impact(event_with_actual)
            lines.append(f"📈 实际值: **{actual_value}**")
            lines.append(f"{analysis['emoji']} **{analyzer._get_direction_text(analysis['direction'])}** ({analyzer._get_strength_text(analysis['strength'])})")
            lines.append(f"💡 {analysis['reason']}")
        else:
            lines.append(f"⏰ {event['time_until']}")

    lines.append("\n⚠️ 请提前做好仓位管理")
    return "\n".join(lines)


def main():
    print("🚀 加密市场综合监控启动...")
    print()

    # 1. 获取加密货币数据
    print("📊 获取加密货币数据...")
    crypto_data = get_crypto_prices()

    if not crypto_data:
        print("❌ 无法获取价格数据")
        return

    # 2. 获取全球市场数据
    global_data = get_global_market_data()

    # 3. 检查预警
    alerts = check_alerts(crypto_data)

    # 4. 生成市场报告
    print("✅ 生成市场报告...")
    market_report = generate_market_report(crypto_data, global_data, alerts)

    # 5. 生成经济数据报告
    print("📅 检查经济数据...")
    economic_report = generate_economic_report()

    # 6. 组合完整报告
    full_report = market_report

    if economic_report:
        full_report += economic_report

    full_report += "\n\n---\n💡 高重要性数据发布前后市场波动性可能显著增加"

    # 7. 打印报告（会被 OpenClaw 捕获并发送）
    print()
    print("=" * 80)
    print("📤 发送到 Telegram 的报告")
    print("=" * 80)
    print()
    print(full_report)

    # 8. 如果有预警或即将发布的经济数据，需要通知
    if alerts or economic_report:
        print("\n⚠️ 有重要信息需要关注！")


if __name__ == "__main__":
    main()
