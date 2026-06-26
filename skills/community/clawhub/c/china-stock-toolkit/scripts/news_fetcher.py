#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻聚合模块 - 抓取个股/板块相关新闻
Author: Lin Hui
"""

import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any


# ============================================================================
# 数据结构
# ============================================================================

class NewsItem:
    """新闻条目"""
    def __init__(self, title: str, source: str, pub_time: str, 
                 url: str, summary: str = "", sentiment: str = "中性"):
        self.title = title
        self.source = source
        self.pub_time = pub_time
        self.url = url
        self.summary = summary
        self.sentiment = sentiment  # 利好/利空/中性
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "source": self.source,
            "pub_time": self.pub_time,
            "url": self.url,
            "summary": self.summary,
            "sentiment": self.sentiment
        }


# ============================================================================
# 东方财富新闻API
# ============================================================================

def fetch_eastmoney_news(stock_code: str, limit: int = 10) -> List[NewsItem]:
    """
    抓取东方财富个股新闻
    stock_code: 如 sh600519 或 sz000001
    """
    items = []
    try:
        # 东方财富个股新闻API
        # 将 sh600519 转为 1.600519 或 0.000001
        if stock_code.startswith("sh"):
            market_code = "1." + stock_code[2:]
        elif stock_code.startswith("sz"):
            market_code = "0." + stock_code[2:]
        else:
            return items
        
        # 新闻列表API
        url = f"https://np-anotice-stock.eastmoney.com/api/security/ann?cb=&page_size={limit}&page_index=1&ann_type=A&client_source=web&stock_list={market_code}"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Referer': 'https://www.eastmoney.com/'
        })
        
        with urllib.request.urlopen(req, timeout=8) as response:
            content = response.read().decode('utf-8')
            
            # 如果是JSONP，去掉回调包装
            if content.startswith('('):
                content = content[1:-1]
            
            data = json.loads(content)
            
            if 'data' in data and 'list' in data['data']:
                for item in data['data']['list'][:limit]:
                    title = item.get('title', '')
                    pub_time = item.get('notice_date', '')
                    url_link = item.get('url', '')
                    
                    items.append(NewsItem(
                        title=title,
                        source="东方财富",
                        pub_time=pub_time,
                        url=url_link,
                        sentiment="中性"  # 公告通常中性
                    ))
    except Exception as e:
        print(f"东方财富新闻抓取失败: {e}")
    
    return items


def fetch_eastmoney_general_news(keyword: str, limit: int = 10) -> List[NewsItem]:
    """
    抓取东方财富通用新闻（按关键词）
    """
    items = []
    try:
        # 搜索新闻API
        encoded_keyword = urllib.request.quote(keyword)
        url = f"https://searchapi.eastmoney.com/bk/GetSearchList?cb=&type=2&pageindex=1&pagesize={limit}&keyword={encoded_keyword}"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Referer': 'https://www.eastmoney.com/'
        })
        
        with urllib.request.urlopen(req, timeout=8) as response:
            content = response.read().decode('utf-8')
            
            # 去掉JSONP回调
            if '(' in content and ')' in content:
                content = content[content.find('(')+1:content.rfind(')')]
            
            data = json.loads(content)
            
            if 'data' in data and 'list' in data['data']:
                for item in data['data']['list'][:limit]:
                    title = item.get('title', '')
                    pub_time = item.get('publishtime', '')
                    url_link = item.get('url', '')
                    
                    items.append(NewsItem(
                        title=title,
                        source="东方财富",
                        pub_time=pub_time,
                        url=url_link,
                        sentiment="中性"
                    ))
    except Exception as e:
        print(f"东方财富通用新闻抓取失败: {e}")
    
    return items


# ============================================================================
# 新浪财经新闻API
# ============================================================================

def fetch_sina_news(stock_code: str, limit: int = 10) -> List[NewsItem]:
    """
    抓取新浪财经个股新闻
    stock_code: 如 sh600519
    """
    items = []
    try:
        # 新浪财经新闻API
        url = f"https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/NewsInfoService.getNewsList?page=1&limit={limit}&symbol={stock_code}"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Referer': 'https://finance.sina.com.cn/'
        })
        
        with urllib.request.urlopen(req, timeout=8) as response:
            content = response.read().decode('gbk')
            
            data = json.loads(content)
            
            if isinstance(data, list):
                for item in data[:limit]:
                    title = item.get('title', '')
                    pub_time = item.get('time', '')
                    url_link = item.get('url', '')
                    
                    items.append(NewsItem(
                        title=title,
                        source="新浪财经",
                        pub_time=pub_time,
                        url=url_link,
                        sentiment="中性"
                    ))
    except Exception as e:
        print(f"新浪财经新闻抓取失败: {e}")
    
    return items


# ============================================================================
# 财联社快讯API
# ============================================================================

def fetch_cls_news(limit: int = 10) -> List[NewsItem]:
    """
    抓取财联社实时快讯
    """
    items = []
    try:
        # 财联社API（需要解析）
        url = "https://www.cls.cn/nodeapi/telegraphList?page=1&last_time=0"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Referer': 'https://www.cls.cn/'
        })
        
        with urllib.request.urlopen(req, timeout=8) as response:
            content = response.read().decode('utf-8')
            data = json.loads(content)
            
            if 'data' in data and 'roll_data' in data['data']:
                for item in data['data']['roll_data'][:limit]:
                    title = item.get('title', '')
                    pub_time = item.get('time', '')
                    url_link = "https://www.cls.cn/detail/" + str(item.get('id', ''))
                    
                    items.append(NewsItem(
                        title=title,
                        source="财联社",
                        pub_time=pub_time,
                        url=url_link,
                        sentiment="中性"
                    ))
    except Exception as e:
        print(f"财联社新闻抓取失败: {e}")
    
    return items


# ============================================================================
# 聚合查询
# ============================================================================

def fetch_stock_news(stock_code: str, stock_name: str, limit: int = 5) -> List[NewsItem]:
    """
    聚合查询个股新闻（多源合并）
    """
    all_items = []
    
    # 1. 东方财富公告
    em_news = fetch_eastmoney_news(stock_code, limit=3)
    all_items.extend(em_news)
    
    # 2. 新浪财经新闻
    sina_news = fetch_sina_news(stock_code, limit=3)
    all_items.extend(sina_news)
    
    # 3. 按股票名称搜索东方财富新闻
    if stock_name:
        keyword_news = fetch_eastmoney_general_news(stock_name, limit=2)
        all_items.extend(keyword_news)
    
    # 去重（按标题）
    seen_titles = set()
    unique_items = []
    for item in all_items:
        if item.title not in seen_titles:
            seen_titles.add(item.title)
            unique_items.append(item)
    
    # 按时间排序（最新的在前）
    unique_items.sort(key=lambda x: x.pub_time, reverse=True)
    
    return unique_items[:limit]


def fetch_sector_news(sector_name: str, limit: int = 5) -> List[NewsItem]:
    """
    查询板块新闻（如：新能源、人工智能、芯片等）
    """
    all_items = []
    
    # 东方财富板块新闻
    keyword_news = fetch_eastmoney_general_news(sector_name, limit=limit)
    all_items.extend(keyword_news)
    
    # 财联社快讯（包含板块动态）
    cls_news = fetch_cls_news(limit=3)
    # 过滤出包含板块关键词的新闻
    filtered_cls = [n for n in cls_news if sector_name in n.title]
    all_items.extend(filtered_cls)
    
    # 去重
    seen_titles = set()
    unique_items = []
    for item in all_items:
        if item.title not in seen_titles:
            seen_titles.add(item.title)
            unique_items.append(item)
    
    unique_items.sort(key=lambda x: x.pub_time, reverse=True)
    return unique_items[:limit]


def fetch_policy_news(limit: int = 5) -> List[NewsItem]:
    """
    查询最新政策新闻
    """
    all_items = []
    
    # 财联社政策快讯
    cls_news = fetch_cls_news(limit=10)
    # 过滤政策相关关键词
    policy_keywords = ["政策", "监管", "央行", "证监会", "发改委", "国务院", "工信部"]
    for item in cls_news:
        if any(kw in item.title for kw in policy_keywords):
            item.source = "财联社(政策)"
            all_items.append(item)
    
    # 搜索政策新闻
    policy_news = fetch_eastmoney_general_news("政策", limit=3)
    all_items.extend(policy_news)
    
    # 去重
    seen_titles = set()
    unique_items = []
    for item in all_items:
        if item.title not in seen_titles:
            seen_titles.add(item.title)
            unique_items.append(item)
    
    unique_items.sort(key=lambda x: x.pub_time, reverse=True)
    return unique_items[:limit]


# ============================================================================
# CLI入口
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python news_fetcher.py <命令> [参数]")
        print("命令:")
        print("  stock <代码> <名称>  - 查询个股新闻")
        print("  sector <板块名>      - 查询板块新闻")
        print("  policy              - 查询政策新闻")
        print("  cls                 - 财联社快讯")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "stock" and len(sys.argv) >= 4:
        code = sys.argv[2]
        name = sys.argv[3]
        news = fetch_stock_news(code, name, limit=5)
        print(json.dumps([n.to_dict() for n in news], ensure_ascii=False, indent=2))
    
    elif cmd == "sector" and len(sys.argv) >= 3:
        sector = sys.argv[2]
        news = fetch_sector_news(sector, limit=5)
        print(json.dumps([n.to_dict() for n in news], ensure_ascii=False, indent=2))
    
    elif cmd == "policy":
        news = fetch_policy_news(limit=5)
        print(json.dumps([n.to_dict() for n in news], ensure_ascii=False, indent=2))
    
    elif cmd == "cls":
        news = fetch_cls_news(limit=5)
        print(json.dumps([n.to_dict() for n in news], ensure_ascii=False, indent=2))
    
    else:
        print("未知命令或参数不足")
        sys.exit(1)
