#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 订阅收集模块
支持自定义 RSS 源，包括 PaperWeekly 等论文解读平台
"""

import json
import logging
import re
from datetime import datetime, timedelta

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# 预定义的 RSS 源配置
PREDEFINED_RSS_SOURCES = {
    "paperweekly_zhihu": {
        "name": "PaperWeekly (知乎专栏)",
        # 知乎专栏 RSS 需要通过 rsshub 或其他服务转换
        # 示例: https://rsshub.app/zhihu/column/paperweekly
        "rss_url": "",
        "description": "PaperWeekly AI论文解读社区",
        "category": "论文解读"
    },
    "paperweekly_wechat": {
        "name": "PaperWeekly (微信公众号)",
        # 微信公众号 RSS 需要通过第三方服务
        "rss_url": "",
        "description": "PaperWeekly 微信公众号",
        "category": "论文解读"
    }
}


def fetch_rss_feed(rss_url, source_name="Unknown", days_back=7, max_items=5, category="资讯"):
    """
    获取指定RSS源的内容
    
    Args:
        rss_url: RSS feed URL
        source_name: 来源名称
        days_back: 回溯天数
        max_items: 最大条目数
        category: 内容分类
    
    Returns:
        list: 格式化的新闻条目列表
    """
    items = []
    
    if not rss_url:
        logger.warning(f"RSS URL 为空: {source_name}")
        return items
    
    try:
        logger.info(f"正在获取 RSS: {source_name} ...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36'
        }
        
        response = requests.get(rss_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for entry in feed.entries[:max_items * 2]:  # 多获取一些以便筛选
            try:
                # 解析发布时间
                published_str = entry.get('published', entry.get('updated', ''))
                published = None
                
                if published_str:
                    # 尝试多种日期格式
                    date_formats = [
                        '%Y-%m-%dT%H:%M:%S',
                        '%Y-%m-%dT%H:%M:%S%z',
                        '%Y-%m-%d %H:%M:%S',
                        '%a, %d %b %Y %H:%M:%S %z',
                        '%a, %d %b %Y %H:%M:%S',
                        '%Y-%m-%d'
                    ]
                    
                    for fmt in date_formats:
                        try:
                            published = datetime.strptime(published_str[:len(fmt)], fmt)
                            break
                        except:
                            continue
                
                # 检查时间范围
                if published and published < cutoff_date:
                    continue
                
                # 提取内容摘要
                summary = entry.get('summary', entry.get('description', ''))
                if summary:
                    soup = BeautifulSoup(summary, 'html.parser')
                    summary = soup.get_text()
                    summary = re.sub(r'\s+', ' ', summary).strip()
                    summary = summary[:200] + "..." if len(summary) > 200 else summary
                else:
                    summary = f"{source_name} 最新内容"
                
                # 构建条目
                item = {
                    "type": category,
                    "tag": f"[{category}·{source_name}]",
                    "title": entry.get('title', '无标题').strip(),
                    "summary": summary,
                    "url": entry.get('link', ''),
                    "published": published.strftime('%Y-%m-%d') if published else datetime.now().strftime('%Y-%m-%d'),
                    "source": source_name,
                    "rss_source": rss_url
                }
                
                items.append(item)
                
                if len(items) >= max_items:
                    break
                    
            except Exception as e:
                logger.warning(f"解析 RSS 条目失败: {e}")
                continue
        
        logger.info(f"获取到 {source_name} 的 {len(items)} 条内容")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"请求 RSS 失败 {source_name}: {e}")
    except Exception as e:
        logger.error(f"解析 RSS 失败 {source_name}: {e}")
    
    return items[:max_items]


def fetch_all_rss_content(rss_configs, days_back=7):
    """
    获取所有配置的 RSS 内容
    
    Args:
        rss_configs: RSS 配置列表，每个配置包含 name, url, max_items, category
        days_back: 回溯天数
    
    Returns:
        list: 所有新闻条目
    """
    all_items = []
    
    for config in rss_configs:
        if not config.get('enabled', True):
            continue
        
        items = fetch_rss_feed(
            rss_url=config.get('url', ''),
            source_name=config.get('name', 'Unknown'),
            days_back=config.get('days_back', days_back),
            max_items=config.get('max_items', 3),
            category=config.get('category', '资讯')
        )
        all_items.extend(items)
    
    logger.info(f"RSS 内容总计: {len(all_items)} 条")
    return all_items


# 为 PaperWeekly 预留的专用函数
def fetch_paperweekly_content(rss_url=None, days_back=7, max_items=3):
    """
    获取 PaperWeekly 内容
    
    如果提供了 rss_url 则直接使用，否则尝试使用预配置
    """
    if not rss_url:
        # 如果用户没有提供 RSS URL，返回空并记录提示
        logger.warning("PaperWeekly RSS URL 未配置，请在 config.json 中设置 rss.url")
        return []
    
    return fetch_rss_feed(
        rss_url=rss_url,
        source_name="PaperWeekly",
        days_back=days_back,
        max_items=max_items,
        category="论文解读"
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # 测试示例
    print("测试 RSS 收集器...")
    
    # 示例：测试一个公共 RSS
    test_configs = [
        {
            "name": "测试源",
            "url": "https://news.ycombinator.com/rss",  # Hacker News RSS
            "max_items": 3,
            "category": "技术",
            "enabled": True
        }
    ]
    
    items = fetch_all_rss_content(test_configs, days_back=7)
    
    print(f"\n获取到 {len(items)} 条内容:\n")
    for item in items:
        print(f"[{item['tag']}] {item['title']}")
        print(f"发布时间: {item['published']}")
        print(f"摘要: {item['summary'][:100]}...")
        print(f"链接: {item['url']}")
        print("-" * 50)
