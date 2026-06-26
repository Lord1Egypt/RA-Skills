#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股新闻情绪分析脚本
使用 Firecrawl 抓取财经新闻，分析市场情绪
"""

import subprocess
import json
import re
from typing import Dict, List, Optional
from datetime import datetime
import logging
import sys

# Windows UTF-8 输出设置

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AShareNewsSentimentAnalyzer:
    """A 股新闻情绪分析器"""

    # 财经新闻源
    NEWS_SOURCES = [
        "site:eastmoney.com",
        "site:sina.com.cn/stock",
        "site:10jqka.com.cn",
        "site:cs.com.cn",
        "site:stock.star.cn",
    ]

    # 情绪关键词
    POSITIVE_KEYWORDS = [
        "上涨", "利好", "突破", "创新高", "买入", "推荐", "增持",
        "业绩增长", "超预期", "强势", "放量", "涨停", "牛股"
    ]

    NEGATIVE_KEYWORDS = [
        "下跌", "利空", "跌破", "新低", "卖出", "减持", "风险",
        "业绩下滑", "不及预期", "弱势", "缩量", "跌停", "暴雷"
    ]

    def __init__(self):
        self.firecrawl_available = self._check_firecrawl()

    def _check_firecrawl(self) -> bool:
        """检查 Firecrawl 是否可用"""
        try:
            result = subprocess.run(
                ["firecrawl", "--status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            logger.warning(f"Firecrawl 检查失败：{e}")
            return False

    def search_news(self, query: str, limit: int = 10) -> List[Dict]:
        """使用 Firecrawl 搜索新闻"""
        if not self.firecrawl_available:
            logger.warning("Firecrawl 不可用，返回空结果")
            return []

        try:
            # 构建搜索命令
            cmd = [
                "firecrawl", "search", query,
                "--limit", str(limit),
                "--sources", "news",
                "--tbs", "qdr:d",  # 只搜索最近 1 天
                "--json"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get('data', {}).get('web', [])
            else:
                logger.error(f"Firecrawl 搜索失败：{result.stderr}")
                return []

        except Exception as e:
            logger.error(f"搜索新闻失败：{e}")
            return []

    def analyze_sentiment(self, text: str) -> Dict:
        """分析文本情绪"""
        positive_count = sum(1 for keyword in self.POSITIVE_KEYWORDS if keyword in text)
        negative_count = sum(1 for keyword in self.NEGATIVE_KEYWORDS if keyword in text)

        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0.5  # 中性
            sentiment_label = "NEUTRAL"
        else:
            sentiment_score = positive_count / total
            if sentiment_score > 0.6:
                sentiment_label = "BULLISH"
            elif sentiment_score < 0.4:
                sentiment_label = "BEARISH"
            else:
                sentiment_label = "NEUTRAL"

        return {
            "positive_count": positive_count,
            "negative_count": negative_count,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label
        }

    def analyze_stock_news(self, stock_code: str, stock_name: str) -> Dict:
        """分析个股新闻情绪"""
        # 搜索股票相关新闻
        query = f"{stock_name} {stock_code} 股票 行情"
        news_items = self.search_news(query, limit=10)

        if not news_items:
            # 尝试简化搜索
            query = f"{stock_name} 股票"
            news_items = self.search_news(query, limit=5)

        # 分析每条新闻的情绪
        sentiments = []
        for item in news_items:
            title = item.get('title', '')
            snippet = item.get('description', '')
            text = f"{title} {snippet}"

            sentiment = self.analyze_sentiment(text)
            sentiment['title'] = title
            sentiment['url'] = item.get('url', '')
            sentiment['time'] = item.get('age', '')
            sentiments.append(sentiment)

        # 计算总体情绪
        if sentiments:
            avg_score = sum(s['sentiment_score'] for s in sentiments) / len(sentiments)
            bullish_count = sum(1 for s in sentiments if s['sentiment_label'] == 'BULLISH')
            bearish_count = sum(1 for s in sentiments if s['sentiment_label'] == 'BEARISH')
            neutral_count = sum(1 for s in sentiments if s['sentiment_label'] == 'NEUTRAL')

            if avg_score > 0.6:
                overall_label = "BULLISH"
            elif avg_score < 0.4:
                overall_label = "BEARISH"
            else:
                overall_label = "NEUTRAL"
        else:
            avg_score = 0.5
            overall_label = "UNKNOWN"
            bullish_count = 0
            bearish_count = 0
            neutral_count = 0

        return {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "news_count": len(news_items),
            "bullish_count": bullish_count,
            "bearish_count": bearish_count,
            "neutral_count": neutral_count,
            "avg_sentiment_score": avg_score,
            "overall_sentiment": overall_label,
            "news_items": sentiments[:5],  # 只保留前 5 条
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def analyze_market_news(self) -> Dict:
        """分析大盘新闻情绪"""
        # 搜索大盘相关新闻
        queries = [
            "A 股 大盘 行情",
            "上证指数 深证成指 走势",
            "股市 分析 预测"
        ]

        all_news = []
        for query in queries:
            news_items = self.search_news(query, limit=5)
            all_news.extend(news_items)

        # 分析情绪
        sentiments = []
        for item in all_news[:15]:  # 最多分析 15 条
            title = item.get('title', '')
            snippet = item.get('description', '')
            text = f"{title} {snippet}"
            sentiment = self.analyze_sentiment(text)
            sentiment['title'] = title
            sentiments.append(sentiment)

        # 计算总体情绪
        if sentiments:
            avg_score = sum(s['sentiment_score'] for s in sentiments) / len(sentiments)
            bullish_ratio = sum(1 for s in sentiments if s['sentiment_label'] == 'BULLISH') / len(sentiments) * 100
            bearish_ratio = sum(1 for s in sentiments if s['sentiment_label'] == 'BEARISH') / len(sentiments) * 100
            neutral_ratio = sum(1 for s in sentiments if s['sentiment_label'] == 'NEUTRAL') / len(sentiments) * 100

            if avg_score > 0.6:
                overall_label = "BULLISH"
            elif avg_score < 0.4:
                overall_label = "BEARISH"
            else:
                overall_label = "NEUTRAL"
        else:
            avg_score = 0.5
            overall_label = "UNKNOWN"
            bullish_ratio = 0
            bearish_ratio = 0
            neutral_ratio = 0

        return {
            "news_count": len(sentiments),
            "bullish_ratio": round(bullish_ratio, 2),
            "bearish_ratio": round(bearish_ratio, 2),
            "neutral_ratio": round(neutral_ratio, 2),
            "avg_sentiment_score": round(avg_score, 3),
            "overall_sentiment": overall_label,
            "news_items": sentiments[:5],
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == "__main__":
    analyzer = AShareNewsSentimentAnalyzer()

    print("=" * 60)
    print("A 股新闻情绪分析系统")
    print("=" * 60)

    # 测试个股新闻分析
    print("\n📈 测试：贵州茅台 (600519) 新闻情绪")
    print("-" * 60)
    result = analyzer.analyze_stock_news("600519", "贵州茅台")
    print(f"新闻数量：{result['news_count']}")
    print(f"看多：{result['bullish_count']} | 看空：{result['bearish_count']} | 中性：{result['neutral_count']}")
    print(f"情绪评分：{result['avg_sentiment_score']:.3f}")
    print(f"总体情绪：{result['overall_sentiment']}")
    print(f"更新时间：{result['update_time']}")

    if result['news_items']:
        print("\n📰 最新新闻:")
        for i, news in enumerate(result['news_items'][:3], 1):
            print(f"  {i}. {news['title']}")
            print(f"     情绪：{news['sentiment_label']} (评分：{news['sentiment_score']:.2f})")

    # 测试大盘新闻分析
    print("\n" + "=" * 60)
    print("📊 大盘新闻情绪分析")
    print("-" * 60)
    market_result = analyzer.analyze_market_news()
    print(f"新闻数量：{market_result['news_count']}")
    print(f"看多：{market_result['bullish_ratio']:.1f}% | 看空：{market_result['bearish_ratio']:.1f}% | 中性：{market_result['neutral_ratio']:.1f}%")
    print(f"情绪评分：{market_result['avg_sentiment_score']:.3f}")
    print(f"总体情绪：{market_result['overall_sentiment']}")
