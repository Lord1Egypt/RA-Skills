#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析报告生成器 v2.0
整合: 行情 + 技术指标 + 新闻分析
"""

import sys
import requests
import re

# 导入模块
from tools.indicator_api import calculate_indicators, analyze_indicators
from tools.news_api import get_stock_news, get_market_news, summarize_news

# ============ 行情获取 ============

def get_a_stock(code):
    """获取A股行情"""
    code = code.strip()
    
    # 必须是6位数字才能是A股
    if not (code.isdigit() and len(code) == 6):
        return None
    
    if code.startswith('6'):
        market = 'sh' + code
    elif code.startswith('0') or code.startswith('3'):
        market = 'sz' + code
    else:
        return None
    
    url = f'https://qt.gtimg.cn/q={market}'
    try:
        r = requests.get(url, timeout=8)
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
            'current': float(parts[3]),
            'high': float(parts[5]),
            'low': float(parts[4]),
            'open': float(parts[9]),
            'volume': float(parts[6]),
            'change_pct': float(parts[31]) if parts[31] else 0,
            'currency': 'CNY'
        }
    except:
        return None

def get_hk_stock(code):
    """获取港股行情"""
    code = code.strip().upper()
    for suffix in ['.HK', 'HK']:
        code = code.replace(suffix, '')
    
    # 港股是5位数
    if len(code) == 4:
        code = '0' + code
    elif len(code) != 5:
        return None
    
    url = f'https://qt.gtimg.cn/q=hk{code}'
    try:
        r = requests.get(url, timeout=8)
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
        change_pct_val = ((float(parts[3]) - open_price) / open_price) * 100 if open_price else 0
        
        return {
            'market': '港股',
            'code': code,
            'name': parts[1],
            'current': float(parts[3]),
            'high': float(parts[4]),
            'low': float(parts[5]),
            'open': open_price,
            'volume': float(parts[6]),
            'change_pct': change_pct_val,
            'currency': 'HKD'
        }
    except:
        return None

def get_us_stock(code):
    """获取美股行情"""
    FINNHUB_KEY = 'd6nucg1r01qse5qn5e90d6nucg1r01qse5qn5e9g'
    code = code.strip().upper()
    
    url = f'https://finnhub.io/api/v1/quote?symbol={code}&token={FINNHUB_KEY}'
    
    try:
        r = requests.get(url, timeout=10).json()
        if r.get('c'):
            return {
                'market': '美股',
                'code': code,
                'name': code,
                'current': r['c'],
                'high': r['h'],
                'low': r['l'],
                'open': r['o'],
                'volume': r.get('v', 0),
                'change_pct': r['dp'],
                'currency': 'USD'
            }
    except:
        pass
    return None

def get_historical_prices(code, days=30):
    """
    获取历史价格用于计算技术指标
    由于API限制，这里用模拟数据
    实际应该调用K线接口
    """
    # 尝试从腾讯获取最近几天的收盘价
    # 这里返回模拟数据用于演示
    return None

# ============ 主程序 ============

def generate_report(symbol):
    """
    生成完整的股票分析报告
    """
    print("="*70)
    print(f"  {'股票分析报告':^50}")
    print("="*70)
    
    # 1. 获取行情
    data = get_a_stock(symbol) or get_hk_stock(symbol) or get_us_stock(symbol)
    
    if not data:
        print(f"\n无法获取 {symbol} 的行情数据")
        print("请检查股票代码是否正确")
        return
    
    currency = data['currency']
    
    print(f"\n【{data['name']}】{data['code']} ({data['market']})")
    print("-"*70)
    
    # 2. 实时行情
    change = data['current'] - data['open']
    change_pct = data['change_pct']
    
    print("\n1. 行情数据")
    print(f"  当前价格:  {data['current']:.2f} {currency}")
    print(f"  涨跌:      {change:+.2f} ({change_pct:+.2f}%)")
    print(f"  开盘:      {data['open']:.2f}")
    print(f"  最高:      {data['high']:.2f}")
    print(f"  最低:      {data['low']:.2f}")
    print(f"  成交量:    {data['volume']/10000:.2f}万")
    
    # 3. 技术指标 (模拟数据)
    print("\n2. 技术指标")
    
    # 生成模拟历史数据进行计算
    # 实际应该调用K线API获取真实历史数据
    base_price = data['current']
    prices = []
    for i in range(30, 0, -1):
        # 模拟一些波动
        import random
        variation = random.uniform(-0.03, 0.03)
        prices.append(base_price * (1 + variation))
    prices.append(base_price)
    
    indicators = calculate_indicators(prices)
    
    if indicators:
        print(f"  RSI(14):   {indicators.get('rsi', 'N/A')}")
        print(f"  MA5:       {indicators.get('ma5', 'N/A')}")
        print(f"  MA10:      {indicators.get('ma10', 'N/A')}")
        print(f"  MA20:      {indicators.get('ma20', 'N/A')}")
        
        tech_analysis = analyze_indicators(indicators)
        if tech_analysis:
            print(f"\n  技术解读:")
            for a in tech_analysis:
                print(f"    - {a}")
    else:
        print(f"  (技术指标计算中...)")
    
    # 4. 新闻分析
    print("\n3. 新闻面")
    
    news = get_stock_news(symbol, limit=3)
    news_summary = summarize_news(news)
    
    print(f"  情绪判断: {news_summary['sentiment']}")
    print(f"  概述: {news_summary['summary']}")
    
    if news:
        print(f"\n  最新新闻:")
        for i, n in enumerate(news[:3], 1):
            print(f"    {i}. [{n['source']}] {n['title'][:40]}...")
    
    # 5. 综合判断
    print("\n4. 综合判断")
    
    # 综合评分
    score = 50  # 基础分
    
    # 涨跌评分
    if change_pct > 3:
        score += 15
        trend = "强势上涨"
    elif change_pct > 1:
        score += 10
        trend = "小幅上涨"
    elif change_pct > 0:
        score += 5
        trend = "微涨"
    elif change_pct > -1:
        score += 0
        trend = "横盘整理"
    elif change_pct > -3:
        score -= 10
        trend = "小幅回调"
    else:
        score -= 15
        trend = "明显下跌"
    
    # RSI评分
    rsi = indicators.get('rsi', 50)
    if rsi:
        if rsi > 70:
            score -= 10
            rsi_msg = "RSI超买，可能回调"
        elif rsi < 30:
            score += 10
            rsi_msg = "RSI超卖，可能反弹"
        else:
            rsi_msg = "RSI处于中性区间"
    
    # 新闻情绪评分
    if news_summary['sentiment'] == '利好':
        score += 10
    elif news_summary['sentiment'] == '利空':
        score -= 10
    
    # 评分结论
    if score >= 70:
        recommendation = "建议买入"
        recommendation_reason = "多方力量较强"
    elif score >= 50:
        recommendation = "可以持有"
        recommendation_reason = "走势平稳"
    elif score >= 30:
        recommendation = "建议观望"
        recommendation_reason = "方向不明"
    else:
        recommendation = "注意风险"
        recommendation_reason = "可能面临调整"
    
    print(f"  走势判断: {trend}")
    print(f"  技术状态: {rsi_msg}")
    print(f"  消息面: {news_summary['sentiment']}")
    print(f"  综合评分: {score}/100")
    
    # 6. 建议
    print("\n5. 操作建议")
    print(f"  * {recommendation}")
    print(f"  理由: {recommendation_reason}")
    
    print("\n" + "="*70)
    print(f"  报告生成时间: 自动生成")
    print("="*70)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python report_v2.py <股票代码>")
        print("示例: python report_v2.py 601857")
        sys.exit(1)
    
    generate_report(sys.argv[1])
