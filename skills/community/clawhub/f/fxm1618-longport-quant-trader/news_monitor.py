#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻与舆情监控系统
功能：财经新闻抓取、情感分析、事件驱动信号
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re
import json

# ============ 新闻源配置 ============
NEWS_SOURCES = {
    "reuters": {
        "name": "Reuters",
        "url": "https://www.reuters.com/rssfeed/business",
        "language": "en",
        "region": "US"
    },
    "bbc_business": {
        "name": "BBC Business",
        "url": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "language": "en",
        "region": "UK"
    },
    "sina_finance": {
        "name": "新浪财经",
        "url": "https://finance.sina.com.cn/rss/roll.xml",
        "language": "zh",
        "region": "CN"
    },
    "eastmoney": {
        "name": "东方财富",
        "url": "https://rss.eastmoney.com/news_c.xml",
        "language": "zh",
        "region": "CN"
    }
}

# ============ 关键词配置 ============
# 利好关键词
POSITIVE_KEYWORDS = [
    "beat estimates", "earnings beat", "revenue growth", "profit surge",
    "upgrade", "buy rating", "price target raised", "analyst upgrade",
    "new contract", "partnership", "acquisition", "expansion",
    "FDA approval", "patent approved", "product launch",
    "record high", "all-time high", "breakout", "bullish",
    "业绩超预期", "营收增长", "利润大增", "上调评级", "买入评级",
    "新合同", "战略合作", "收购", "扩张", "获批", "专利", "新产品",
    "创新高", "突破", "看涨"
]

# 利空关键词
NEGATIVE_KEYWORDS = [
    "miss estimates", "earnings miss", "revenue decline", "profit warning",
    "downgrade", "sell rating", "price target cut", "analyst downgrade",
    "lawsuit", "investigation", "recall", "scandal", "fraud",
    "layoffs", "cutting jobs", "restructuring", "bankruptcy",
    "record low", "all-time low", "breakdown", "bearish",
    "业绩不及预期", "营收下滑", "利润警告", "下调评级", "卖出评级",
    "诉讼", "调查", "召回", "丑闻", "欺诈", "裁员", "重组", "破产",
    "创新低", "跌破", "看跌"
]

# 重大事件关键词
MAJOR_EVENTS = [
    "FOMC", "Federal Reserve", "interest rate", "rate hike", "rate cut",
    "CPI", "inflation", "unemployment", "GDP", "nonfarm payroll",
    "SEC investigation", "trading halt", "delisting",
    "美联储", "加息", "降息", "利率决议", "CPI", "通胀", "失业", "GDP",
    "非农", "证监会调查", "停牌", "退市"
]

# ============ 情感分析 ============

def analyze_sentiment(text: str) -> Dict:
    """简单情感分析"""
    text_lower = text.lower()
    
    positive_count = sum(1 for kw in POSITIVE_KEYWORDS if kw.lower() in text_lower)
    negative_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw.lower() in text_lower)
    major_event_count = sum(1 for kw in MAJOR_EVENTS if kw.lower() in text_lower)
    
    # 计算情感得分 (-1 到 1)
    total = positive_count + negative_count
    if total == 0:
        sentiment_score = 0
        sentiment_label = "neutral"
    else:
        sentiment_score = (positive_count - negative_count) / total
        if sentiment_score > 0.3:
            sentiment_label = "positive"
        elif sentiment_score < -0.3:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
    
    return {
        "score": sentiment_score,
        "label": sentiment_label,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "major_event": major_event_count > 0
    }

# ============ 新闻抓取 ============

def fetch_news(source: str = "all", hours: int = 24) -> List[Dict]:
    """抓取新闻"""
    all_news = []
    
    sources_to_fetch = [source] if source != "all" else list(NEWS_SOURCES.keys())
    
    for source_key in sources_to_fetch:
        if source_key not in NEWS_SOURCES:
            continue
        
        source_info = NEWS_SOURCES[source_key]
        try:
            feed = feedparser.parse(source_info["url"])
            
            for entry in feed.entries[:50]:  # 限制每次最多 50 条
                # 解析时间
                published = None
                if hasattr(entry, 'published_parsed'):
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed'):
                    published = datetime(*entry.updated_parsed[:6])
                
                # 只取指定时间范围内的新闻
                if published and published < datetime.now() - timedelta(hours=hours):
                    continue
                
                # 情感分析
                content = f"{entry.title} {entry.summary if hasattr(entry, 'summary') else ''}"
                sentiment = analyze_sentiment(content)
                
                news_item = {
                    "id": f"{source_key}_{len(all_news)}",
                    "source": source_info["name"],
                    "title": entry.title,
                    "summary": entry.summary if hasattr(entry, 'summary') else "",
                    "link": entry.link,
                    "published": published.isoformat() if published else None,
                    "language": source_info["language"],
                    "sentiment": sentiment
                }
                
                all_news.append(news_item)
        
        except Exception as e:
            print(f"❌ 抓取 {source_info['name']} 失败：{e}")
    
    # 按时间排序
    all_news.sort(key=lambda x: x['published'] or '', reverse=True)
    
    return all_news

# ============ 股票相关新闻 ============

def fetch_stock_news(symbols: List[str], hours: int = 24) -> Dict[str, List[Dict]]:
    """抓取特定股票相关新闻"""
    result = {}
    
    for symbol in symbols:
        # 使用 Yahoo Finance 新闻
        try:
            url = f"https://finance.yahoo.com/rss/headline?s={symbol}"
            feed = feedparser.parse(url)
            
            news_list = []
            for entry in feed.entries[:20]:
                published = None
                if hasattr(entry, 'published_parsed'):
                    published = datetime(*entry.published_parsed[:6])
                
                if published and published < datetime.now() - timedelta(hours=hours):
                    continue
                
                content = f"{entry.title} {entry.summary if hasattr(entry, 'summary') else ''}"
                sentiment = analyze_sentiment(content)
                
                news_list.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": published.isoformat() if published else None,
                    "sentiment": sentiment
                })
            
            result[symbol] = news_list
        
        except Exception as e:
            print(f"❌ 抓取 {symbol} 新闻失败：{e}")
            result[symbol] = []
    
    return result

# ============ 新闻信号生成 ============

def generate_news_signals(news_list: List[Dict], threshold: float = 0.5) -> List[Dict]:
    """根据新闻生成交易信号"""
    signals = []
    
    # 按情感分组
    positive_news = [n for n in news_list if n['sentiment']['label'] == 'positive']
    negative_news = [n for n in news_list if n['sentiment']['label'] == 'negative']
    major_events = [n for n in news_list if n['sentiment']['major_event']]
    
    # 重大事件信号（最高优先级）
    for event in major_events:
        signals.append({
            "type": "major_event",
            "priority": "high",
            "title": event['title'],
            "source": event['source'],
            "timestamp": event['published'],
            "action": "watch",  # 观望或根据具体内容决定
            "reason": f"重大事件：{event['title']}"
        })
    
    # 强烈正面新闻（买入信号）
    if len(positive_news) >= 3:
        avg_score = sum(n['sentiment']['score'] for n in positive_news) / len(positive_news)
        if avg_score > threshold:
            signals.append({
                "type": "sentiment",
                "priority": "medium",
                "action": "Buy",
                "reason": f"正面新闻集中 ({len(positive_news)}条)，平均情感得分{avg_score:.2f}",
                "news_count": len(positive_news)
            })
    
    # 强烈负面新闻（卖出信号）
    if len(negative_news) >= 3:
        avg_score = sum(n['sentiment']['score'] for n in negative_news) / len(negative_news)
        if avg_score < -threshold:
            signals.append({
                "type": "sentiment",
                "priority": "medium",
                "action": "Sell",
                "reason": f"负面新闻集中 ({len(negative_news)}条)，平均情感得分{avg_score:.2f}",
                "news_count": len(negative_news)
            })
    
    return signals

# ============ 主函数 ============

if __name__ == "__main__":
    print("📰 新闻与舆情监控系统")
    print("=" * 60)
    
    # 抓取新闻
    print("\n📥 抓取新闻...")
    news = fetch_news(hours=24)
    print(f"✅ 获取 {len(news)} 条新闻")
    
    # 情感统计
    positive = sum(1 for n in news if n['sentiment']['label'] == 'positive')
    negative = sum(1 for n in news if n['sentiment']['label'] == 'negative')
    neutral = sum(1 for n in news if n['sentiment']['label'] == 'neutral')
    major = sum(1 for n in news if n['sentiment']['major_event'])
    
    print(f"\n📊 情感分布:")
    print(f"  正面：{positive} 条 ({positive/len(news)*100:.1f}%)")
    print(f"  负面：{negative} 条 ({negative/len(news)*100:.1f}%)")
    print(f"  中性：{neutral} 条 ({neutral/len(news)*100:.1f}%)")
    print(f"  重大事件：{major} 条")
    
    # 生成信号
    print("\n📈 生成交易信号...")
    signals = generate_news_signals(news)
    
    if signals:
        print(f"✅ 生成 {len(signals)} 个信号:")
        for sig in signals:
            emoji = "⚠️" if sig['priority'] == 'high' else "📊"
            print(f"  {emoji} {sig['type']}: {sig['action']} - {sig['reason'][:50]}...")
    else:
        print("⚠️  无显著信号")
    
    # 显示最新新闻
    print("\n📰 最新重大新闻:")
    for n in news[:5]:
        emoji = "🟢" if n['sentiment']['label'] == 'positive' else "🔴" if n['sentiment']['label'] == 'negative' else "⚪"
        print(f"  {emoji} [{n['source']}] {n['title'][:60]}...")
