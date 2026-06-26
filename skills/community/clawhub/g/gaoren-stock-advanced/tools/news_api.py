"""
新闻分析模块
获取股票相关新闻并做情绪分析
"""

import requests
import re

# 利好关键词
BULLISH_KEYWORDS = [
    '上涨', '增长', '盈利', '利润', '业绩', '突破', '创新', '高', '好',
    'up', 'rise', 'gain', 'profit', 'growth', 'beat', 'exceed', 'bullish',
    '上调', '增持', '买入', '推荐', '目标价', '评级', '超预期'
]

# 利空关键词
BEARISH_KEYWORDS = [
    '下跌', '亏损', '风险', '低', '差', '跌', '降',
    'down', 'fall', 'loss', 'bearish', 'miss', 'warning',
    '下调', '减持', '卖出', '风险', '警告', '不及预期'
]

def get_stock_news(symbol, limit=5):
    """
    获取股票相关新闻
    """
    # 搜索这只股票相关的新闻
    # 使用6551 API
    
    news_list = []
    
    try:
        # 尝试获取科技/财经新闻
        categories = ['tech', 'macro', 'crypto']
        
        for cat in categories:
            url = f'https://ai.6551.io/open/free_hot?category={cat}'
            r = requests.get(url, timeout=10)
            data = r.json()
            
            if data.get('success'):
                items = data.get('news', {}).get('items', [])
                
                # 搜索包含股票代码或名称的新闻
                for item in items:
                    title = item.get('title', '')
                    summary = item.get('summary_en', '')
                    text = title + ' ' + summary
                    
                    # 简单匹配
                    if symbol.upper() in text.upper() or symbol in text:
                        news_list.append({
                            'title': title,
                            'source': item.get('source', ''),
                            'summary': summary[:100],
                            'sentiment': analyze_sentiment(title + ' ' + summary)
                        })
                    
                    if len(news_list) >= limit:
                        break
            
            if len(news_list) >= limit:
                break
                
    except Exception as e:
        print(f"获取新闻失败: {e}")
    
    return news_list[:limit]

def analyze_sentiment(text):
    """
    分析新闻情绪
    返回: bullish(利好), bearish(利空), neutral(中性)
    """
    text_lower = text.lower()
    
    bullish_count = 0
    bearish_count = 0
    
    for keyword in BULLISH_KEYWORDS:
        if keyword.lower() in text_lower:
            bullish_count += 1
    
    for keyword in BEARISH_KEYWORDS:
        if keyword.lower() in text_lower:
            bearish_count += 1
    
    if bullish_count > bearish_count:
        return 'bullish'
    elif bearish_count > bullish_count:
        return 'bearish'
    else:
        return 'neutral'

def get_market_news():
    """
    获取市场热点新闻
    """
    news_list = []
    
    try:
        url = 'https://ai.6551.io/open/free_hot?category=macro'
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if data.get('success'):
            items = data.get('news', {}).get('items', [])
            
            for item in items[:10]:
                news_list.append({
                    'title': item.get('title', ''),
                    'source': item.get('source', ''),
                    'sentiment': analyze_sentiment(item.get('title', '') + ' ' + item.get('summary_en', ''))
                })
                
    except Exception as e:
        print(f"获取市场新闻失败: {e}")
    
    return news_list

def summarize_news(news_list):
    """
    总结新闻情绪
    """
    if not news_list:
        return {
            'sentiment': 'neutral',
            'summary': '暂无相关新闻',
            'bullish_count': 0,
            'bearish_count': 0
        }
    
    bullish_count = sum(1 for n in news_list if n.get('sentiment') == 'bullish')
    bearish_count = sum(1 for n in news_list if n.get('sentiment') == 'bearish')
    
    if bullish_count > bearish_count:
        sentiment = '利好'
        summary = f'近期有{bullish_count}条利好消息'
    elif bearish_count > bullish_count:
        sentiment = '利空'
        summary = f'近期有{bearish_count}条利空消息'
    else:
        sentiment = '中性'
        summary = '消息面相对平衡'
    
    return {
        'sentiment': sentiment,
        'summary': summary,
        'bullish_count': bullish_count,
        'bearish_count': bearish_count,
        'news': news_list
    }

if __name__ == '__main__':
    # 测试
    news = get_stock_news('JD')
    print("相关新闻:", news)
    print("\n总结:", summarize_news(news))
