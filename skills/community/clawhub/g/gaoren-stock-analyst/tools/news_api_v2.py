#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版新闻API - 多数据源
- 富途新闻
- 财经门户
- 搜索API
"""

import requests
import re

# ========== 数据源配置 ==========
DATA_SOURCES = {
    'futu': 'https://news.futunn.com/stock/{symbol}/news',
    'stock_163': 'https://quotes.stock.163.com/service/chddata.html?code={code}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG',
    'sina': 'https://hq.sinajs.cn/list={quote}'
}

# 利好关键词
BULLISH_KEYWORDS = [
    '上涨', '增长', '盈利', '利润', '业绩', '突破', '创新', '高', '好', '增持', '买入', '推荐', '超预期',
    'up', 'rise', 'gain', 'profit', 'growth', 'beat', 'exceed', 'bullish', '上调', '目标价', '评级',
    '利好', '大涨', '飙升', '强劲', '复苏', '扩张', '突破', '首涨', '领涨', '创新高'
]

# 利空关键词
BEARISH_KEYWORDS = [
    '下跌', '亏损', '风险', '低', '差', '跌', '降', '减持', '卖出', '警告', '不及预期',
    'down', 'fall', 'loss', 'bearish', 'miss', 'warning', '下调', '风险', '利空',
    '大跌', '暴跌', '疲软', '萎缩', '下滑', '亏损', '违约', '诉讼', '造假'
]

# ========== 核心函数 ==========

def analyze_sentiment(text):
    """
    分析新闻情绪
    返回: bullish(利好), bearish(利空), neutral(中性)
    """
    if not text:
        return 'neutral'
    
    text_lower = text.lower()
    
    bullish_count = sum(1 for kw in BULLISH_KEYWORDS if kw.lower() in text_lower)
    bearish_count = sum(1 for kw in BEARISH_KEYWORDS if kw.lower() in text_lower)
    
    if bullish_count > bearish_count:
        return 'bullish'
    elif bearish_count > bullish_count:
        return 'bearish'
    else:
        return 'neutral'

def get_futu_news(symbol):
    """
    获取富途新闻
    """
    news_list = []
    
    # 转换代码格式: 03998 -> hk03998
    code = symbol.upper().replace('.HK', '').replace('HK', '')
    if len(code) == 4:
        code = '0' + code
    
    # 富途新闻API
    url = f'https://news.futunn.com/v1/stock/news?symbol=HK{code}&page=1&page_size=10'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        
        if data.get('code') == 0:
            items = data.get('data', {}).get('list', [])
            
            for item in items:
                title = item.get('title', '')
                summary = item.get('digest', '')
                
                news_list.append({
                    'source': '富途',
                    'title': title,
                    'summary': summary[:100] if summary else title[:100],
                    'url': item.get('url', ''),
                    'time': item.get('publish_time', ''),
                    'sentiment': analyze_sentiment(title + ' ' + summary)
                })
                
    except Exception as e:
        print(f"富途新闻获取失败: {e}")
    
    return news_list

def get_tech_news():
    """
    获取科技/财经热点新闻
    """
    news_list = []
    
    # 使用6551 API
    try:
        url = 'https://ai.6551.io/open/free_hot?category=tech'
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if data.get('success'):
            items = data.get('news', {}).get('items', [])
            
            for item in items[:15]:
                title = item.get('title', '')
                summary = item.get('summary_en', '')
                
                news_list.append({
                    'source': item.get('source', '6551'),
                    'title': title,
                    'summary': summary[:100] if summary else '',
                    'sentiment': analyze_sentiment(title + ' ' + summary)
                })
                
    except Exception as e:
        print(f"科技新闻获取失败: {e}")
    
    return news_list

def get_market_news():
    """
    获取市场宏观新闻
    """
    news_list = []
    
    categories = ['macro', 'finance']
    
    for cat in categories:
        try:
            url = f'https://ai.6551.io/open/free_hot?category={cat}'
            r = requests.get(url, timeout=8)
            data = r.json()
            
            if data.get('success'):
                items = data.get('news', {}).get('items', [])
                
                for item in items[:8]:
                    news_list.append({
                        'source': item.get('source', cat),
                        'title': item.get('title', ''),
                        'summary': item.get('summary_en', '')[:100],
                        'sentiment': analyze_sentiment(item.get('title', ''))
                    })
                    
        except:
            continue
    
    return news_list[:10]

def search_stock_news(symbol, limit=10):
    """
    综合搜索股票新闻 - 多源
    """
    all_news = []
    
    # 1. 富途新闻
    futu_news = get_futu_news(symbol)
    all_news.extend(futu_news)
    
    # 富途没有结果时，尝试搜索相关
    if len(all_news) < 3:
        # 2. 搜索相关热点
        tech_news = get_tech_news()
        # 简单过滤可能相关的
        for news in tech_news:
            # 尝试匹配股票代码或常见词汇
            if symbol.upper() in news['title'].upper() or \
               any(kw in news['title'] for kw in ['股票', '财报', '业绩', '股价', '上市', 'IPO', '美股', '港股', 'A股']):
                all_news.append(news)
    
    return all_news[:limit]

def summarize_news(news_list):
    """
    总结新闻情绪
    """
    if not news_list:
        return {
            'sentiment': '中性',
            'summary': '暂无相关新闻',
            'bullish_count': 0,
            'bearish_count': 0,
            'total': 0
        }
    
    bullish_count = sum(1 for n in news_list if n.get('sentiment') == 'bullish')
    bearish_count = sum(1 for n in news_list if n.get('sentiment') == 'bearish')
    
    if bullish_count > bearish_count:
        sentiment = '利好'
        summary = f'近期{bullish_count}条利好，{bearish_count}条利空'
    elif bearish_count > bullish_count:
        sentiment = '利空'
        summary = f'近期{bearish_count}条利空，{bullish_count}条利好'
    else:
        sentiment = '中性'
        summary = f'利好{bullish_count}条，利空{bearish_count}条'
    
    return {
        'sentiment': sentiment,
        'summary': summary,
        'bullish_count': bullish_count,
        'bearish_count': bearish_count,
        'total': len(news_list),
        'news': news_list[:5]  # 返回前5条
    }

# ========== 测试 ==========
if __name__ == '__main__':
    # 测试
    print("="*50)
    print("测试富途新闻: 03998")
    news = get_futu_news('03998')
    for i, n in enumerate(news[:3], 1):
        print(f"{i}. [{n['source']}] {n['title'][:40]}")
        print(f"   情绪: {n['sentiment']}")
    
    print("\n" + "="*50)
    print("新闻总结:")
    print(summarize_news(news))
