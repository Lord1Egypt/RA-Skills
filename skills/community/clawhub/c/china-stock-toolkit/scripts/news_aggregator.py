#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻聚合器 - 整合新闻抓取 + 情感分析 + 汇总
Author: Lin Hui
"""

import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from news_fetcher import (
    fetch_stock_news, fetch_sector_news, fetch_policy_news, 
    fetch_cls_news, NewsItem
)
from sentiment_analyzer import SentimentAnalyzer, summarize_sentiment


# ============================================================================
# 新闻聚合器
# ============================================================================

class NewsAggregator:
    """新闻聚合器"""
    
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
    
    def get_stock_news_with_sentiment(self, stock_code: str, stock_name: str, 
                                       limit: int = 5) -> dict:
        """
        获取个股新闻 + 情感分析
        返回: {
            "stock_code": "...",
            "stock_name": "...",
            "news": [...],
            "summary": {"overall": "看涨", ...}
        }
        """
        # 抓取新闻
        news_items = fetch_stock_news(stock_code, stock_name, limit=limit)
        
        # 转换为字典
        news_list = [n.to_dict() for n in news_items]
        
        # 情感分析
        analyzed = self.analyzer.batch_analyze(news_list, sector="")
        
        # 汇总
        summary = summarize_sentiment(analyzed)
        
        return {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "news_count": len(analyzed),
            "news": analyzed,
            "summary": summary
        }
    
    def get_sector_news_with_sentiment(self, sector_name: str, 
                                        limit: int = 5) -> dict:
        """
        获取板块新闻 + 情感分析
        """
        news_items = fetch_sector_news(sector_name, limit=limit)
        news_list = [n.to_dict() for n in news_items]
        
        analyzed = self.analyzer.batch_analyze(news_list, sector=sector_name)
        summary = summarize_sentiment(analyzed)
        
        return {
            "sector_name": sector_name,
            "news_count": len(analyzed),
            "news": analyzed,
            "summary": summary
        }
    
    def get_policy_news_with_sentiment(self, limit: int = 5) -> dict:
        """
        获取政策新闻 + 情感分析
        """
        news_items = fetch_policy_news(limit=limit)
        news_list = [n.to_dict() for n in news_items]
        
        analyzed = self.analyzer.batch_analyze(news_list, sector="")
        summary = summarize_sentiment(analyzed)
        
        return {
            "type": "policy",
            "news_count": len(analyzed),
            "news": analyzed,
            "summary": summary
        }
    
    def get_market_sentiment(self) -> dict:
        """
        获取整体市场情绪（基于财联社快讯）
        """
        news_items = fetch_cls_news(limit=10)
        news_list = [n.to_dict() for n in news_items]
        
        analyzed = self.analyzer.batch_analyze(news_list, sector="")
        summary = summarize_sentiment(analyzed)
        
        return {
            "type": "market_sentiment",
            "news_count": len(analyzed),
            "news": analyzed[:5],  # 只返回前5条
            "summary": summary
        }


# ============================================================================
# CLI 入口
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("用法: python news_aggregator.py <命令> [参数]")
        print("命令:")
        print("  stock <代码> <名称>  - 个股新闻+情感")
        print("  sector <板块名>      - 板块新闻+情感")
        print("  policy              - 政策新闻+情感")
        print("  market              - 市场整体情绪")
        print("  test                - 测试情感分析")
        sys.exit(1)
    
    cmd = sys.argv[1]
    aggregator = NewsAggregator()
    
    if cmd == "stock" and len(sys.argv) >= 4:
        code = sys.argv[2]
        name = sys.argv[3]
        result = aggregator.get_stock_news_with_sentiment(code, name, limit=5)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "sector" and len(sys.argv) >= 3:
        sector = sys.argv[2]
        result = aggregator.get_sector_news_with_sentiment(sector, limit=5)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "policy":
        result = aggregator.get_policy_news_with_sentiment(limit=5)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "market":
        result = aggregator.get_market_sentiment()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "test":
        # 测试情感分析
        test_news = [
            {"title": "公司业绩大增50%，超预期", "source": "测试", "pub_time": "", "url": ""},
            {"title": "监管趋严，行业承压", "source": "测试", "pub_time": "", "url": ""},
            {"title": "公司发布年度财报", "source": "测试", "pub_time": "", "url": ""},
        ]
        analyzed = aggregator.analyzer.batch_analyze(test_news)
        print(json.dumps(analyzed, ensure_ascii=False, indent=2))
        summary = summarize_sentiment(analyzed)
        print("\n汇总:")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    else:
        print("未知命令")
        sys.exit(1)


if __name__ == "__main__":
    main()
