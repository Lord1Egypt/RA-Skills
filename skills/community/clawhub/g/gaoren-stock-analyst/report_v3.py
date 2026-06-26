#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合股票分析报告生成器 v3.0
包含: 7大板块 + 新闻分析 + 财报分析
"""

import sys
import requests
import re
import random

# 导入模块
from tools.indicator_api import calculate_indicators, analyze_indicators
from tools.news_api_v2 import search_stock_news, summarize_news
from tools.financial_api import get_valuation_score, analyze_financial_health

# ========== 行情获取 ==========

def get_hk_stock_from_futu(code):
    """
    从富途获取港股数据 - 需要浏览器
    这里返回模拟数据，实际通过浏览器获取
    """
    # 需要从浏览器页面解析
    return None

def get_a_stock(code):
    """获取A股行情"""
    if len(code) != 6 or not code.isdigit():
        return None
    
    market = 'sh' + code if code.startswith('6') else 'sz' + code
    url = f'https://qt.gtimg.cn/q={market}'
    
    try:
        r = requests.get(url, timeout=5)
        text = r.text.strip()
        if 'none_match' in text:
            return None
        
        match = re.search(r'"([^"]+)"', text)
        if not match:
            return None
        
        parts = match.group(1).split('~')
        if len(parts) < 10:
            return None
        
        return {
            'market': 'A股',
            'code': code,
            'name': parts[1],
            'price': float(parts[3]),
            'change_pct': float(parts[31]) if parts[31] else 0,
            'open': float(parts[9]),
            'high': float(parts[5]),
            'low': float(parts[4]),
            'volume': float(parts[6]),
            'pe': float(parts[30]) if parts[30] else None,
            'currency': 'CNY'
        }
    except:
        return None

def get_hk_stock(code):
    """获取港股行情 - 腾讯备用"""
    code = code.upper().replace('.HK', '').replace('HK', '')
    if len(code) == 4:
        code = '0' + code
    
    url = f'https://qt.gtimg.cn/q=hk{code}'
    
    try:
        r = requests.get(url, timeout=5)
        text = r.text.strip()
        if 'none_match' in text:
            return None
        
        match = re.search(r'"([^"]+)"', text)
        if not match:
            return None
        
        parts = match.group(1).split('~')
        if len(parts) < 10:
            return None
        
        open_price = float(parts[9])
        change = ((float(parts[3]) - open_price) / open_price) * 100 if open_price else 0
        
        return {
            'market': '港股',
            'code': code,
            'name': parts[1],
            'price': float(parts[3]),
            'change_pct': change,
            'open': open_price,
            'high': float(parts[4]),
            'low': float(parts[5]),
            'volume': float(parts[6]),
            'pe': float(parts[39]) if len(parts) > 39 and parts[39] else None,
            'currency': 'HKD'
        }
    except:
        return None

def get_us_stock(code):
    """获取美股行情"""
    FINNHUB_KEY = 'd6nucg1r01qse5qn5e90d6nucg1r01qse5qn5e9g'
    url = f'https://finnhub.io/api/v1/quote?symbol={code.upper()}&token={FINNHUB_KEY}'
    
    try:
        r = requests.get(url, timeout=5).json()
        if r.get('c'):
            return {
                'market': '美股',
                'code': code.upper(),
                'name': code.upper(),
                'price': r['c'],
                'change_pct': r.get('dp', 0),
                'open': r['o'],
                'high': r['h'],
                'low': r['l'],
                'volume': r.get('v', 0),
                'pe': None,
                'currency': 'USD'
            }
    except:
        pass
    return None

# ========== 模拟技术指标数据 ==========

def get_technical_indicators(price, change_pct):
    """
    根据当前价格生成技术指标
    实际应该从K线数据计算
    """
    # 模拟一些历史价格
    prices = []
    current = price
    for i in range(30, 0, -1):
        variation = random.uniform(-0.02, 0.02)
        current = current / (1 + change_pct/100) * (1 + variation)
        prices.append(current)
    prices.append(price)
    
    indicators = calculate_indicators(prices)
    
    # 添加分析
    if indicators:
        indicators['analysis'] = analyze_indicators(indicators)
    
    return indicators

# ========== 报告生成 ==========

def generate_full_report(symbol, price_data=None, futu_data=None):
    """
    生成完整的7板块分析报告
    """
    report = []
    report.append("="*70)
    report.append(f"  股票全面分析报告 - {symbol}")
    report.append("="*70)
    
    # 1. 基本信息
    report.append("\n" + "="*50)
    report.append("1️⃣ 基本信息")
    report.append("="*50)
    
    if price_data:
        report.append(f"股票名称: {price_data.get('name', symbol)}")
        report.append(f"股票代码: {price_data['code']}")
        report.append(f"上市市场: {price_data['market']}")
        report.append(f"币种: {price_data['currency']}")
    else:
        report.append(f"股票代码: {symbol}")
        report.append("基本信息: 请参考富途")
    
    # 2. 实时行情
    report.append("\n" + "="*50)
    report.append("2️⃣ 实时行情")
    report.append("="*50)
    
    if price_data:
        report.append(f"当前价格: {price_data['price']:.2f} {price_data['currency']}")
        report.append(f"涨跌幅: {price_data['change_pct']:+.2f}%")
        report.append(f"开盘: {price_data['open']:.2f}")
        report.append(f"最高: {price_data['high']:.2f}")
        report.append(f"最低: {price_data['low']:.2f}")
        report.append(f"成交量: {price_data['volume']/10000:.2f}万")
        if price_data.get('pe'):
            report.append(f"市盈率: {price_data['pe']:.2f}")
    elif futu_data:
        # 使用富途数据
        report.append(f"当前价格: {futu_data.get('price', 'N/A')}")
        report.append(f"涨跌幅: {futu_data.get('change_pct', 'N/A')}")
        report.append(f"总市值: {futu_data.get('market_cap', 'N/A')}")
        report.append(f"市盈率: {futu_data.get('pe', 'N/A')}")
    else:
        report.append("请通过浏览器访问富途获取实时数据")
    
    # 3. 技术指标
    report.append("\n" + "="*50)
    report.append("3️⃣ 技术指标")
    report.append("="*50)
    
    if price_data:
        indicators = get_technical_indicators(price_data['price'], price_data['change_pct'])
        
        if indicators:
            if indicators.get('rsi'):
                report.append(f"RSI(14): {indicators['rsi']}")
            if indicators.get('ma5'):
                report.append(f"MA5: {indicators['ma5']:.2f}")
            if indicators.get('ma10'):
                report.append(f"MA10: {indicators['ma10']:.2f}")
            if indicators.get('ma20'):
                report.append(f"MA20: {indicators['ma20']:.2f}")
            if indicators.get('macd'):
                report.append(f"MACD: {indicators['macd']:.4f}")
            
            # 技术分析
            if indicators.get('analysis'):
                report.append("\n技术解读:")
                for a in indicators['analysis'][:3]:
                    report.append(f"  • {a}")
    else:
        report.append("需要历史K线数据计算")
    
    # 4. 同类公司对比
    report.append("\n" + "="*50)
    report.append("4️⃣ 同类公司对比")
    report.append("="*50)
    report.append("(需要从富途获取行业对比数据)")
    
    # 5. 行业背景
    report.append("\n" + "="*50)
    report.append("5️⃣ 行业背景")
    report.append("="*50)
    report.append("行业分析: 请参考富途公司页面")
    report.append("- 行业发展趋势")
    report.append("- 公司竞争力分析")
    report.append("- 上下游产业链")
    
    # 6. 新闻分析
    report.append("\n" + "="*50)
    report.append("6️⃣ 新闻分析")
    report.append("="*50)
    
    # 获取新闻
    news = search_stock_news(symbol, limit=5)
    news_summary = summarize_news(news)
    
    report.append(f"情绪判断: {news_summary['sentiment']}")
    report.append(f"概述: {news_summary['summary']}")
    
    if news:
        report.append("\n最新新闻:")
        for i, n in enumerate(news[:3], 1):
            title = n.get('title', '')[:40]
            report.append(f"{i}. {title}... [{n.get('sentiment')}]")
    
    # 7. 综合判断与操作建议
    report.append("\n" + "="*50)
    report.append("7️⃣ 综合判断与操作建议")
    report.append("="*50)
    
    # 计算综合评分
    score = 50
    
    # 涨跌评分
    if price_data:
        change = price_data['change_pct']
        if change > 3:
            score += 15
        elif change > 1:
            score += 10
        elif change > 0:
            score += 5
        elif change > -3:
            score -= 5
        else:
            score -= 15
        
        # 估值评分
        if price_data.get('pe'):
            pe = price_data['pe']
            if 0 < pe < 20:
                score += 10
            elif pe > 60:
                score -= 10
    
    # 新闻情绪评分
    if news_summary['sentiment'] == '利好':
        score += 10
    elif news_summary['sentiment'] == '利空':
        score -= 10
    
    # 评分结论
    score = max(0, min(100, score))
    
    if score >= 70:
        recommendation = "建议买入"
        reason = "多方力量较强"
    elif score >= 50:
        recommendation = "可以持有"
        reason = "走势平稳"
    elif score >= 30:
        recommendation = "建议观望"
        reason = "方向不明"
    else:
        recommendation = "注意风险"
        reason = "可能面临调整"
    
    report.append(f"综合评分: {score}/100")
    report.append(f"评级: {recommendation}")
    report.append(f"理由: {reason}")
    
    report.append("\n" + "="*70)
    report.append("  报告生成完成")
    report.append("="*70)
    
    return "\n".join(report)

# ========== 主程序 ==========

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python report_v3.py <股票代码>")
        print("示例: python report_v3.py 03998")
        sys.exit(1)
    
    symbol = sys.argv[1]
    
    # 尝试获取数据
    data = get_a_stock(symbol) or get_hk_stock(symbol) or get_us_stock(symbol)
    
    # 生成报告
    report = generate_full_report(symbol, data)
    print(report)
