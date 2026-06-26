#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器备选抓取模块
当 RSS/API/yt-dlp 等方法失效时，使用 agent-browser 或 playwright 进行网页抓取
"""

import json
import logging
import re
import subprocess
import time
from datetime import datetime, timedelta

import requests

logger = logging.getLogger(__name__)

# 抓取策略配置
BROWSER_FALLBACK_CONFIG = {
    "timeout": 30,  # 浏览器操作超时时间
    "retry_times": 2,  # 重试次数
    "delay_between_retries": 2,  # 重试间隔秒数
}


def run_agent_browser_command(command, timeout=30):
    """
    执行 agent-browser 命令
    
    Args:
        command: 命令字符串（不含 'agent-browser' 前缀）
        timeout: 超时时间
    
    Returns:
        tuple: (success, output, error)
    """
    try:
        full_cmd = f"agent-browser {command}"
        result = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            return True, result.stdout, None
        else:
            return False, result.stdout, result.stderr
            
    except subprocess.TimeoutExpired:
        return False, None, "Command timeout"
    except FileNotFoundError:
        return False, None, "agent-browser not found"
    except Exception as e:
        return False, None, str(e)


def scrape_with_agent_browser(url, extraction_rules, wait_time=3):
    """
    使用 agent-browser 抓取网页内容
    
    Args:
        url: 目标URL
        extraction_rules: 提取规则字典，包含 selector 和 attribute
        wait_time: 等待页面加载时间
    
    Returns:
        list: 提取的数据列表
    """
    items = []
    
    try:
        # 打开页面
        success, output, error = run_agent_browser_command(f'open "{url}"', timeout=15)
        if not success:
            logger.error(f"agent-browser open failed: {error}")
            return items
        
        # 等待页面加载
        time.sleep(wait_time)
        
        # 获取页面快照
        success, output, error = run_agent_browser_command('snapshot -i --json', timeout=10)
        if not success:
            logger.error(f"agent-browser snapshot failed: {error}")
            run_agent_browser_command('close')
            return items
        
        # 解析快照，根据规则提取数据
        # 这里简化处理，实际使用时根据具体页面结构调整
        logger.info(f"agent-browser snapshot captured for {url}")
        
        # 尝试用 eval 执行 JS 提取数据
        if 'js_extractor' in extraction_rules:
            js_code = extraction_rules['js_extractor']
            success, output, error = run_agent_browser_command(f'eval "{js_code}"', timeout=10)
            if success and output:
                try:
                    items = json.loads(output)
                except:
                    items = [{"text": output.strip()}]
        
        # 关闭浏览器
        run_agent_browser_command('close')
        
    except Exception as e:
        logger.error(f"agent-browser scraping failed: {e}")
        run_agent_browser_command('close')
    
    return items


def scrape_with_playwright(url, extraction_config):
    """
    使用 Playwright Python API 抓取网页
    
    Args:
        url: 目标URL
        extraction_config: 提取配置，包含 selectors
    
    Returns:
        list: 提取的数据列表
    """
    items = []
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # 设置超时
            page.set_default_timeout(30000)
            
            # 访问页面
            logger.info(f"Playwright navigating to {url}")
            page.goto(url, wait_until='networkidle')
            
            # 等待特定元素（如果配置了）
            if 'wait_for_selector' in extraction_config:
                page.wait_for_selector(extraction_config['wait_for_selector'])
            
            # 提取数据
            selectors = extraction_config.get('selectors', {})
            
            if 'item_selector' in selectors:
                # 列表模式
                elements = page.query_selector_all(selectors['item_selector'])
                
                for element in elements[:extraction_config.get('max_items', 10)]:
                    item = {}
                    
                    # 提取标题
                    if 'title' in selectors:
                        title_el = element.query_selector(selectors['title'])
                        if title_el:
                            item['title'] = title_el.inner_text().strip()
                            # 尝试获取链接
                            link_el = title_el if title_el.tag_name == 'a' else element.query_selector('a')
                            if link_el:
                                item['url'] = link_el.get_attribute('href') or ''
                    
                    # 提取摘要/描述
                    if 'summary' in selectors:
                        summary_el = element.query_selector(selectors['summary'])
                        if summary_el:
                            item['summary'] = summary_el.inner_text().strip()[:200]
                    
                    # 提取时间
                    if 'date' in selectors:
                        date_el = element.query_selector(selectors['date'])
                        if date_el:
                            item['published'] = date_el.inner_text().strip()
                    
                    if item.get('title'):
                        items.append(item)
            
            else:
                # 单页模式 - 提取页面主要文本
                title = page.title()
                content = page.inner_text('body')
                items.append({
                    'title': title,
                    'summary': content[:500] if content else 'No content',
                    'url': url
                })
            
            browser.close()
            
    except ImportError:
        logger.error("Playwright not installed. Run: pip install playwright")
    except Exception as e:
        logger.error(f"Playwright scraping failed: {e}")
    
    return items


def fallback_arxiv_papers(categories=None, max_results=5, days_back=1):
    """
    使用浏览器备选方案抓取 arXiv 论文
    参数与 fetch_arxiv_papers 保持一致
    """
    if categories is None:
        categories = ['cs.CL', 'cs.LG', 'cs.AI']
    
    items = []
    cutoff_date = datetime.now() - timedelta(days=days_back + 1)
    
    for category in categories:
        url = f"https://arxiv.org/list/{category}/recent"
        
        extraction_config = {
            'wait_for_selector': '.meta',
            'selectors': {
                'item_selector': 'dl dt, .meta',
                'title': 'div.list-title',
                'summary': 'div.list-title',
                'date': 'div.dateline'
            },
            'max_items': max_results
        }
        
        try:
            results = scrape_with_playwright(url, extraction_config)
            
            for item in results:
                # 检查日期
                pub_date_str = item.get('published', '')
                if pub_date_str:
                    try:
                        pub_date = datetime.strptime(pub_date_str[:10], '%Y-%m-%d')
                        if pub_date < cutoff_date:
                            continue
                    except:
                        pass
                
                item.update({
                    'type': '论文',
                    'tag': f'[论文·{category}]',
                    'category': category,
                    'source': 'arxiv-browser'
                })
            
            items.extend(results[:max_results])
        except Exception as e:
            logger.error(f"Fallback arXiv [{category}] failed: {e}")
    
    return items[:max_results * len(categories)]


def fallback_huggingface_papers(max_results=4):
    """
    使用浏览器备选方案抓取 Hugging Face Papers
    """
    url = "https://huggingface.co/papers"
    
    extraction_config = {
        'wait_for_selector': 'article',
        'selectors': {
            'item_selector': 'article',
            'title': 'h3',
            'summary': 'p',
        },
        'max_items': max_results
    }
    
    items = scrape_with_playwright(url, extraction_config)
    
    for item in items:
        item.update({
            'type': '资讯',
            'tag': '[资讯·HuggingFace]',
            'source': 'huggingface-browser'
        })
    
    return items


def fallback_product_hunt(max_results=4):
    """
    使用浏览器备选方案抓取 Product Hunt
    """
    url = "https://www.producthunt.com/categories/artificial-intelligence"
    
    extraction_config = {
        'wait_for_selector': '[data-test^="post-item"]',
        'selectors': {
            'item_selector': '[data-test^="post-item"]',
            'title': 'a[data-test^="post-name"]',
            'summary': 'a[data-test^="post-tagline"]',
        },
        'max_items': max_results
    }
    
    items = scrape_with_playwright(url, extraction_config)
    
    for item in items:
        item.update({
            'type': '产品',
            'tag': '[产品·ProductHunt]',
            'source': 'producthunt-browser'
        })
    
    return items


def fallback_youtube_videos(creator_config, max_videos=2):
    """
    使用浏览器备选方案抓取 YouTube 视频
    """
    handle = creator_config.get('handle', '').lstrip('@')
    url = f"https://www.youtube.com/{creator_config.get('handle', '')}/videos"
    
    extraction_config = {
        'wait_for_selector': 'ytd-rich-grid-media, ytd-video-renderer',
        'selectors': {
            'item_selector': 'ytd-rich-grid-media, ytd-video-renderer',
            'title': '#video-title',
            'summary': '#video-title',  # YouTube 列表页没有描述，只能获取标题
        },
        'max_items': max_videos
    }
    
    items = scrape_with_playwright(url, extraction_config)
    
    for item in items:
        item.update({
            'creator': creator_config['name'],
            'type': '视频',
            'tag': f'[视频·{creator_config["name"].split("(")[0].strip()}]',
            'source': 'youtube-browser'
        })
    
    return items


def fallback_rss_feed(rss_url, source_name="Unknown", max_items=5, category="资讯"):
    """
    使用浏览器直接访问 RSS URL 作为备选
    适用于 RSS 被墙或无法直接访问的情况
    """
    items = []
    
    try:
        # 尝试直接获取 RSS
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(rss_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            import feedparser
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:max_items]:
                from bs4 import BeautifulSoup
                summary = entry.get('summary', '')
                if summary:
                    summary = BeautifulSoup(summary, 'html.parser').get_text()[:200]
                
                items.append({
                    'type': category,
                    'tag': f'[{category}·{source_name}]',
                    'title': entry.get('title', '无标题'),
                    'summary': summary,
                    'url': entry.get('link', ''),
                    'published': datetime.now().strftime('%Y-%m-%d'),
                    'source': f'{source_name}-rss-fallback'
                })
    except Exception as e:
        logger.error(f"RSS fallback failed: {e}")
    
    return items


def try_with_fallback(primary_func, fallback_func, *args, **kwargs):
    """
    尝试主方法，失败时使用备选方法
    
    Args:
        primary_func: 主抓取函数
        fallback_func: 备选抓取函数
        *args, **kwargs: 传递给两个函数的参数
    
    Returns:
        list: 抓取结果
    """
    # 尝试主方法
    try:
        logger.info(f"Trying primary method: {primary_func.__name__}")
        result = primary_func(*args, **kwargs)
        if result and len(result) > 0:
            logger.info(f"Primary method succeeded: {len(result)} items")
            return result
        else:
            logger.warning("Primary method returned empty result")
    except Exception as e:
        logger.error(f"Primary method failed: {e}")
    
    # 尝试备选方法
    try:
        logger.info(f"Trying fallback method: {fallback_func.__name__}")
        result = fallback_func(*args, **kwargs)
        if result:
            logger.info(f"Fallback method succeeded: {len(result)} items")
        return result
    except Exception as e:
        logger.error(f"Fallback method failed: {e}")
        return []


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("测试浏览器备选抓取...")
    
    # 测试 arXiv 备选
    print("\n测试 arXiv 备选抓取...")
    items = fallback_arxiv_papers(['cs.CL'], max_results=2)
    print(f"获取到 {len(items)} 条")
    for item in items[:2]:
        print(f"  - {item.get('title', 'N/A')[:50]}...")
