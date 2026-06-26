#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI日报数据收集脚本
收集arXiv论文、Product Hunt产品、Hugging Face资讯
"""

import json
import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

import feedparser
import requests
from bs4 import BeautifulSoup

# 导入YouTube收集模块
from youtube_collector import fetch_all_youtube_content
from rss_collector import fetch_all_rss_content, fetch_paperweekly_content
from browser_fallback import (
    try_with_fallback,
    fallback_arxiv_papers,
    fallback_huggingface_papers,
    fallback_product_hunt,
    fallback_youtube_videos,
    fallback_rss_feed
)

# 配置日志
def setup_logging(log_dir="logs"):
    """设置日志"""
    Path(log_dir).mkdir(exist_ok=True)
    log_file = os.path.join(log_dir, f"ai_daily_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# 加载配置
def load_config(config_path="config.json"):
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"配置文件未找到: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"配置文件格式错误: {e}")
        raise

# arXiv 论文收集
def fetch_arxiv_papers(categories, max_results=5, days_back=1):
    """
    获取arXiv最新论文
    
    Args:
        categories: 论文分类列表，如 ['cs.CL', 'cs.LG']
        max_results: 每个分类最大返回数量
        days_back: 查询最近几天的论文
    """
    papers = []
    
    for category in categories:
        try:
            # 构建查询URL
            query = f"cat:{category}"
            url = f"http://export.arxiv.org/api/query?search_query={quote(query)}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
            
            logger.info(f"正在获取arXiv [{category}] 论文...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 解析RSS
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:max_results]:
                # 提取日期
                published = entry.get('published', entry.get('updated', ''))
                
                # 检查是否是最近的论文
                try:
                    pub_date = datetime.strptime(published[:10], '%Y-%m-%d')
                    if datetime.now() - pub_date > timedelta(days=days_back + 1):
                        continue
                except:
                    pass
                
                # 清理摘要
                summary = entry.get('summary', '')
                summary = re.sub(r'<[^>]+>', '', summary)  # 移除HTML标签
                summary = summary.replace('\n', ' ').strip()
                
                paper = {
                    "type": "论文",
                    "tag": "[论文]",
                    "title": entry.get('title', '').replace('\n', ' ').strip(),
                    "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                    "url": entry.get('link', ''),
                    "published": published[:10],
                    "category": category,
                    "authors": [author.get('name', '') for author in entry.get('authors', [])[:3]]
                }
                papers.append(paper)
                
        except Exception as e:
            logger.error(f"获取arXiv [{category}] 失败: {e}")
            continue
    
    logger.info(f"arXiv论文获取完成: {len(papers)}条")
    return papers[:max_results * len(categories)]

# Product Hunt 产品收集
def fetch_product_hunt(max_results=4):
    """
    获取Product Hunt热门AI产品
    注意：Product Hunt需要API Token，这里使用网页抓取作为备选
    """
    products = []
    
    try:
        logger.info("正在获取Product Hunt热门产品...")
        
        # 使用备用方案：获取TechCrunch或Product Hunt RSS
        # 这里使用一个简化的方式，实际生产环境建议申请PH API
        url = "https://www.producthunt.com/feed?category=ai"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:max_results]:
                # 尝试提取描述
                summary = entry.get('summary', '')
                summary = BeautifulSoup(summary, 'html.parser').get_text()
                summary = summary[:150] + "..." if len(summary) > 150 else summary
                
                product = {
                    "type": "产品",
                    "tag": "[产品]",
                    "title": entry.get('title', '').strip(),
                    "summary": summary if summary else "热门AI产品",
                    "url": entry.get('link', ''),
                    "published": entry.get('published', '')[:10] if entry.get('published') else datetime.now().strftime('%Y-%m-%d')
                }
                products.append(product)
        
        # 如果RSS获取失败，使用备用数据
        if not products:
            logger.warning("Product Hunt RSS获取失败，使用备用方案")
            # 这里可以添加其他AI产品信息源
            
    except Exception as e:
        logger.error(f"获取Product Hunt失败: {e}")
    
    logger.info(f"Product Hunt产品获取完成: {len(products)}条")
    return products[:max_results]

# Hugging Face Papers 收集
def fetch_huggingface_papers(max_results=4):
    """
    获取Hugging Face每日论文精选
    """
    papers = []
    
    try:
        logger.info("正在获取Hugging Face Papers...")
        
        url = "https://huggingface.co/papers/feed.xml"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:max_results]:
                summary = entry.get('summary', '')
                summary = BeautifulSoup(summary, 'html.parser').get_text()
                summary = summary[:150] + "..." if len(summary) > 150 else summary
                
                paper = {
                    "type": "资讯",
                    "tag": "[资讯]",
                    "title": entry.get('title', '').strip(),
                    "summary": summary if summary else "Hugging Face精选论文",
                    "url": entry.get('link', ''),
                    "published": entry.get('published', '')[:10] if entry.get('published') else datetime.now().strftime('%Y-%m-%d')
                }
                papers.append(paper)
                
    except Exception as e:
        logger.error(f"获取Hugging Face Papers失败: {e}")
    
    logger.info(f"Hugging Face Papers获取完成: {len(papers)}条")
    return papers[:max_results]

# 保存数据
def save_news_data(news_items, output_path="data/daily_news.json"):
    """保存收集的新闻数据"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_count": len(news_items),
        "items": news_items
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"数据已保存到: {output_path}")

# 主函数
def main():
    """主入口"""
    global logger
    
    # 设置日志
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("开始收集AI日报数据")
    logger.info("=" * 50)
    
    # 加载配置
    config = load_config()
    
    all_news = []
    
    # 1. 收集arXiv论文（带浏览器备选）
    if config.get('sources', {}).get('arxiv', {}).get('enabled', True):
        arxiv_config = config['sources']['arxiv']
        papers = try_with_fallback(
            fetch_arxiv_papers,
            fallback_arxiv_papers,
            categories=arxiv_config.get('categories', ['cs.CL', 'cs.LG', 'cs.AI']),
            max_results=arxiv_config.get('max_results', 5)
        )
        all_news.extend(papers)
    
    # 2. 收集Product Hunt产品（带浏览器备选）
    if config.get('sources', {}).get('producthunt', {}).get('enabled', True):
        ph_config = config['sources']['producthunt']
        products = try_with_fallback(
            fetch_product_hunt,
            fallback_product_hunt,
            max_results=ph_config.get('max_results', 4)
        )
        all_news.extend(products)
    
    # 3. 收集Hugging Face Papers（带浏览器备选）
    if config.get('sources', {}).get('huggingface', {}).get('enabled', True):
        hf_config = config['sources']['huggingface']
        hf_papers = try_with_fallback(
            fetch_huggingface_papers,
            fallback_huggingface_papers,
            max_results=hf_config.get('max_results', 4)
        )
        all_news.extend(hf_papers)
    
    # 4. 收集YouTube视频（带浏览器备选）
    if config.get('sources', {}).get('youtube', {}).get('enabled', True):
        yt_config = config['sources']['youtube']
        
        # 先尝试主方法
        yt_videos = fetch_all_youtube_content(
            creators=yt_config.get('creators'),
            days_back=yt_config.get('days_back', 7),
            max_per_creator=yt_config.get('max_per_creator', 2)
        )
        
        # 如果主方法获取太少，尝试浏览器备选
        if len(yt_videos) < len(yt_config.get('creators', [])) * yt_config.get('max_per_creator', 2) // 2:
            logger.info("YouTube主方法获取不足，尝试浏览器备选...")
            from youtube_collector import YOUTUBE_CREATORS
            for creator_key in yt_config.get('creators', []):
                creator = YOUTUBE_CREATORS.get(creator_key)
                if creator:
                    fallback_videos = fallback_youtube_videos(creator, max_videos=yt_config.get('max_per_creator', 2))
                    yt_videos.extend(fallback_videos)
        
        all_news.extend(yt_videos)
    
    # 5. 收集PaperWeekly论文解读（带浏览器备选）
    if config.get('sources', {}).get('paperweekly', {}).get('enabled', True):
        pw_config = config['sources']['paperweekly']
        pw_content = try_with_fallback(
            fetch_paperweekly_content,
            fallback_rss_feed,
            rss_url=pw_config.get('rss_url'),
            source_name="PaperWeekly",
            max_items=pw_config.get('max_items', 3),
            category="论文解读"
        )
        all_news.extend(pw_content)
    
    # 6. 收集其他自定义RSS源（带浏览器备选）
    if config.get('sources', {}).get('rss', {}).get('enabled', True):
        rss_config = config['sources']['rss']
        
        # 尝试主方法
        rss_items = fetch_all_rss_content(
            rss_configs=rss_config.get('feeds', []),
            days_back=rss_config.get('days_back', 7)
        )
        
        # 如果主方法失败或为空，尝试备选
        if not rss_items:
            logger.info("RSS主方法失败，尝试浏览器备选...")
            for feed_config in rss_config.get('feeds', []):
                if feed_config.get('enabled', True):
                    fallback_items = fallback_rss_feed(
                        rss_url=feed_config.get('url'),
                        source_name=feed_config.get('name', 'Unknown'),
                        max_items=feed_config.get('max_items', 3),
                        category=feed_config.get('category', '资讯')
                    )
                    rss_items.extend(fallback_items)
        
        all_news.extend(rss_items)
    
    # 限制总数
    max_total = config.get('output', {}).get('max_total_items', 15)
    all_news = all_news[:max_total]
    
    # 保存数据
    output_path = config.get('output', {}).get('data_file', 'data/daily_news.json')
    save_news_data(all_news, output_path)
    
    logger.info("=" * 50)
    logger.info(f"数据收集完成，共 {len(all_news)} 条")
    logger.info("=" * 50)
    
    return len(all_news)

if __name__ == "__main__":
    main()
