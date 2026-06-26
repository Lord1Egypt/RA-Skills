#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI政策爬虫脚本 - fetch_policy.py
用途：爬取国内各政府官网和权威媒体的AI相关政策，输出JSON供AI分析
依赖：pip install requests beautifulsoup4 lxml python-dateutil
用法：python fetch_policy.py --days 30 --keywords 人工智能 AI 大模型
版本：1.3.0
更新时间：2026-03-27
"""

import argparse
import json
import re
import sys
import time
import random
import logging
import threading
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional, Any

try:
    import requests
    from bs4 import BeautifulSoup
    from dateutil import parser as dateparser
except ImportError as e:
    print(json.dumps({
        "error": f"缺少依赖库: {e}。请运行: pip install requests beautifulsoup4 lxml python-dateutil",
        "results": []
    }, ensure_ascii=False), file=sys.stdout)
    sys.exit(1)

# 只输出错误到stderr，不污染stdout的JSON
logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                    format='[%(levelname)s] %(asctime)s - %(name)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("policy_crawler")

# 请求统计
request_stats = {
    "total": 0,
    "success": 0,
    "failed": 0,
    "domain_stats": {},
}
stats_lock = threading.Lock()

# ─────────────────────────────────────────────
# 通用请求配置
# ─────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
]

REQUEST_TIMEOUT = 15
MAX_RETRIES = 2

# 速率限制配置
RATE_LIMITS = {
    "default": {
        "max_requests": 10,  # 每分钟最大请求数
        "min_interval": 2,    # 最小请求间隔（秒）
    },
    # 可以为特定域名设置不同的速率限制
    "gov.cn": {
        "max_requests": 5,
        "min_interval": 3,
    },
    "cac.gov.cn": {
        "max_requests": 5,
        "min_interval": 3,
    },
    "miit.gov.cn": {
        "max_requests": 5,
        "min_interval": 3,
    },
    "most.gov.cn": {
        "max_requests": 5,
        "min_interval": 3,
    },
    "ndrc.gov.cn": {
        "max_requests": 5,
        "min_interval": 3,
    },
}

# 域名请求记录
domain_requests = {}
domain_lock = threading.Lock()


def get_headers(referer: Optional[str] = None) -> Dict[str, str]:
    """生成HTTP请求头
    
    Args:
        referer: 引用页URL
        
    Returns:
        包含请求头的字典
    """
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
    }
    if referer:
        headers["Referer"] = referer
    return headers


def check_rate_limit(domain: str) -> None:
    """检查并执行速率限制
    
    Args:
        domain: 目标域名
    """
    import time
    
    # 查找适用的速率限制
    rate_limit = RATE_LIMITS.get("default")
    for domain_suffix, limit in RATE_LIMITS.items():
        if domain_suffix in domain:
            rate_limit = limit
            break
    
    current_time = time.time()
    
    with domain_lock:
        if domain not in domain_requests:
            domain_requests[domain] = []
        
        # 清理1分钟前的请求记录
        domain_requests[domain] = [t for t in domain_requests[domain] if current_time - t < 60]
        
        # 检查请求频率
        if len(domain_requests[domain]) >= rate_limit["max_requests"]:
            # 计算需要等待的时间
            oldest_request = domain_requests[domain][0]
            wait_time = 60 - (current_time - oldest_request)
            if wait_time > 0:
                logger.info(f"速率限制：域名 {domain} 请求过于频繁，等待 {wait_time:.2f} 秒")
                time.sleep(wait_time)
        
        # 检查最小间隔
        if domain_requests[domain]:
            last_request = domain_requests[domain][-1]
            time_since_last = current_time - last_request
            if time_since_last < rate_limit["min_interval"]:
                wait_time = rate_limit["min_interval"] - time_since_last
                logger.info(f"速率限制：域名 {domain} 请求间隔过小，等待 {wait_time:.2f} 秒")
                time.sleep(wait_time)
        
        # 记录本次请求
        domain_requests[domain].append(time.time())


def fetch_html(url: str, retries: int = MAX_RETRIES, sleep_range: tuple = (0.5, 1.5), verify_ssl: bool = True) -> Optional[str]:
    """获取页面HTML，带重试、随机延迟和SSL错误处理
    
    Args:
        url: 目标URL
        retries: 重试次数
        sleep_range: 随机延迟范围（秒）
        verify_ssl: 是否验证SSL证书
        
    Returns:
        页面HTML文本，失败返回None
    """
    import urllib3
    from urllib.parse import urlparse
    
    # 禁用SSL验证时，抑制警告
    if not verify_ssl:
        urllib3.disable_warnings()
    
    # 解析域名
    domain = urlparse(url).netloc
    success = False
    
    for attempt in range(retries + 1):
        try:
            # 检查速率限制
            check_rate_limit(domain)
            
            time.sleep(random.uniform(*sleep_range))
            resp = requests.get(
                url,
                headers=get_headers(referer=url),
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
                verify=verify_ssl
            )
            resp.encoding = resp.apparent_encoding or 'utf-8'
            
            # 处理不同的响应状态码
            if resp.status_code == 200:
                success = True
                # 先更新统计信息，再返回结果
                with stats_lock:
                    request_stats["total"] += 1
                    request_stats["success"] += 1
                    
                    if domain not in request_stats["domain_stats"]:
                        request_stats["domain_stats"][domain] = {"total": 0, "success": 0, "failed": 0}
                    request_stats["domain_stats"][domain]["total"] += 1
                    request_stats["domain_stats"][domain]["success"] += 1
                return resp.text
            elif resp.status_code == 404:
                logger.warning(f"HTTP 404: {url} - 页面不存在")
            elif resp.status_code == 403:
                logger.warning(f"HTTP 403: {url} - 访问被拒绝")
            elif resp.status_code == 429:
                logger.warning(f"HTTP 429: {url} - 速率限制")
                # 遇到速率限制时，增加等待时间
                time.sleep(5)
            elif resp.status_code >= 500:
                logger.warning(f"HTTP {resp.status_code}: {url} - 服务器错误")
            else:
                logger.warning(f"HTTP {resp.status_code}: {url}")
        except requests.exceptions.SSLError as e:
            logger.warning(f"SSL错误 (第{attempt+1}次): {url} -> {e}")
            # 不再禁用SSL验证，而是记录错误并继续重试
        except requests.exceptions.Timeout as e:
            logger.warning(f"连接超时 (第{attempt+1}次): {url} -> {e}")
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"连接错误 (第{attempt+1}次): {url} -> {e}")
        except Exception as e:
            logger.warning(f"请求失败 (第{attempt+1}次): {url} -> {e}")
    
    # 更新请求统计
    with stats_lock:
        request_stats["total"] += 1
        if success:
            request_stats["success"] += 1
        else:
            request_stats["failed"] += 1
        
        if domain not in request_stats["domain_stats"]:
            request_stats["domain_stats"][domain] = {"total": 0, "success": 0, "failed": 0}
        request_stats["domain_stats"][domain]["total"] += 1
        if success:
            request_stats["domain_stats"][domain]["success"] += 1
        else:
            request_stats["domain_stats"][domain]["failed"] += 1
    
    return None


# ─────────────────────────────────────────────
# 日期解析工具
# ─────────────────────────────────────────────
CN_DATE_PATTERN = re.compile(
    r'(\d{4})[年\-/.](\d{1,2})[月\-/.](\d{1,2})[日]?'
)


def parse_date(text: Optional[str]) -> Optional[datetime]:
    """解析中文/英文日期，返回 datetime 对象，失败返回 None
    
    Args:
        text: 日期文本
        
    Returns:
        解析后的datetime对象，失败返回None
    """
    if not text:
        return None
    text = text.strip()
    # 中文日期格式
    m = CN_DATE_PATTERN.search(text)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except Exception:
            pass
    # dateutil 通用解析
    try:
        return dateparser.parse(text, fuzzy=True)
    except Exception:
        return None


def is_within_days(date_obj: Optional[datetime], days: int) -> bool:
    """判断日期是否在最近N天内
    
    Args:
        date_obj: 日期对象
        days: 天数
        
    Returns:
        是否在最近N天内
    """
    if date_obj is None:
        return True  # 无法判断时保留
    cutoff = datetime.now() - timedelta(days=days)
    return date_obj >= cutoff


# ─────────────────────────────────────────────
# 关键词过滤
# ─────────────────────────────────────────────
def matches_keywords(text: str, keywords: List[str]) -> bool:
    """判断文本是否包含任意关键词
    
    Args:
        text: 待检查的文本
        keywords: 关键词列表
        
    Returns:
        是否包含任意关键词
    """
    if not keywords:
        return True
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            return True
    return False


# ─────────────────────────────────────────────
# 通用列表页解析器（适合大多数政府网站）
# ─────────────────────────────────────────────
def parse_generic_list(html: Optional[str], base_url: str, source_name: str, source_type: str) -> List[Dict[str, str]]:
    """通用解析器：提取列表页中的标题、链接、日期
    
    Args:
        html: 页面HTML
        base_url: 基础URL
        source_name: 来源名称
        source_type: 来源类型
        
    Returns:
        提取的政策列表
    """
    if not html:
        return []
    soup = BeautifulSoup(html, 'lxml')
    items = []

    # 尝试多种常见列表结构
    selectors = [
        ('ul.list li', 'a', '.date, .time, span[class*="date"], span[class*="time"]'),
        ('ul.news-list li', 'a', 'span'),
        ('div.list-body li', 'a', 'span'),
        ('div.news-list li', 'a', 'span'),
        ('table.list tr', 'a', 'td:last-child'),
        ('div.zwgk-list li', 'a', 'span'),
        ('ul li', 'a', 'span'),
    ]

    for list_sel, link_sel, date_sel in selectors:
        rows = soup.select(list_sel)
        if len(rows) < 3:
            continue
        for row in rows:
            link_el = row.select_one(link_sel)
            if not link_el:
                continue
            title = link_el.get_text(strip=True)
            href = link_el.get('href', '')
            if not title or not href or len(title) < 5:
                continue
            url = urljoin(base_url, href)
            # 日期
            date_el = row.select_one(date_sel) if date_sel else None
            date_text = date_el.get_text(strip=True) if date_el else ''
            # 备用：从整行文本提取日期
            if not date_text:
                row_text = row.get_text()
                m = CN_DATE_PATTERN.search(row_text)
                date_text = m.group(0) if m else ''
            items.append({
                'title': title,
                'url': url,
                'date_text': date_text,
                'source': source_name,
                'source_type': source_type,
            })
        if items:
            break

    # 最后兜底：找所有带日期特征的 <a> 标签
    if not items:
        for a in soup.find_all('a', href=True):
            title = a.get_text(strip=True)
            if len(title) < 8:
                continue
            parent = a.parent
            parent_text = parent.get_text() if parent else ''
            m = CN_DATE_PATTERN.search(parent_text)
            date_text = m.group(0) if m else ''
            href = a.get('href', '')
            url = urljoin(base_url, href)
            domain = urlparse(base_url).netloc
            if domain not in url:
                continue
            items.append({
                'title': title,
                'url': url,
                'date_text': date_text,
                'source': source_name,
                'source_type': source_type,
            })

    return items


# ─────────────────────────────────────────────
# 各站点专用爬虫函数
# ─────────────────────────────────────────────

def crawl_guowuyuan(days, keywords):
    """国务院政策文件"""
    source = "国务院"
    urls = [
        "https://www.gov.cn/",
        "https://www.gov.cn/zhengce/zuixin/",
    ]
    results = []
    for url in urls:
        html = fetch_html(url)
        items = parse_generic_list(html, url, source, "central")
        results.extend(items)
    return results


def crawl_cac(days, keywords):
    """网信办政策法规"""
    source = "网信办"
    urls = [
        
        "https://www.cac.gov.cn/",
    ]
    results = []
    for url in urls:
        html = fetch_html(url)
        items = parse_generic_list(html, url, source, "central")
        results.extend(items)
    return results


def crawl_miit(days, keywords):
    """工信部政策文件"""
    source = "工信部"
    urls = [
        "https://www.miit.gov.cn/",
        "https://www.miit.gov.cn/zwgk/zcwj/wjfb/index.html",
    ]
    results = []
    for url in urls:
        html = fetch_html(url)
        items = parse_generic_list(html, url, source, "central")
        results.extend(items)
    return results


def crawl_most(days, keywords):
    """科技部政策法规"""
    source = "科技部"
    urls = [
        "https://www.most.gov.cn/index.html",
        "https://www.most.gov.cn/satp/",
    ]
    results = []
    for url in urls:
        html = fetch_html(url)
        items = parse_generic_list(html, url, source, "central")
        results.extend(items)
    return results


def crawl_ndrc(days, keywords):
    """发改委政策文件"""
    source = "发改委"
    url = "https://www.ndrc.gov.cn/xxgk/zcfb/"
    html = fetch_html(url)
    return parse_generic_list(html, url, source, "central")


def crawl_gd(days, keywords):
    """广东省人民政府"""
    source = "广东省"
    results = []
    for url in [
        "http://www.gd.gov.cn/zwgk/wjk/index.html",     # 文件库
        "http://www.gd.gov.cn/zwgk/gsgg/index.html",    # 公示公告
    ]:
        html = fetch_html(url)
        results.extend(parse_generic_list(html, url, source, "guangdong"))
    return results


def crawl_gz(days, keywords):
    """广州市人民政府"""
    source = "广州市"
    results = []
    for url in [
        "https://www.gz.gov.cn/gzzcwjk/index.html",        # 政策文件库
        "https://www.gz.gov.cn/zwgk/fggw/index.html",      # 法规公文
        "https://www.gz.gov.cn/zwgk/zcjd/index.html",      # 政策解读
    ]:
        html = fetch_html(url)
        results.extend(parse_generic_list(html, url, source, "guangdong"))
    return results



def crawl_thepaper(days, keywords):
    """澎湃新闻"""
    source = "澎湃新闻"
    urls = [
        "https://www.thepaper.cn/",
        "https://www.thepaper.cn/channel_121666",  # 科技频道
    ]
    results = []
    for url in urls:
        html = fetch_html(url)
        items = parse_generic_list(html, url, source, "media")
        results.extend(items)
    return results


def crawl_sina(days, keywords):
    """新浪新闻科技频道"""
    source = "新浪新闻"
    urls = [
        "https://tech.sina.com.cn/news/",  # 科技新闻列表
    ]
    results = []
    for url in urls:
        html = fetch_html(url)
        items = parse_generic_list(html, "https://tech.sina.com.cn", source, "media")
        results.extend(items)
    return results


def crawl_ifeng(days, keywords):
    """凤凰网资讯"""
    source = "凤凰网"
    url = "https://tech.ifeng.com/shanklist/2-0-1/"
    html = fetch_html(url)
    items = parse_generic_list(html, "https://tech.ifeng.com", source, "media")
    if not items:
        url2 = "https://news.ifeng.com/c/special/7pSRIpVxkBj"
        html2 = fetch_html(url2)
        items = parse_generic_list(html2, "https://news.ifeng.com", source, "media")
    return items


def crawl_xinhua(days, keywords):
    """新华社科技频道"""
    source = "新华社"
    # 新华社科技AI关键词搜索
    url = "https://so.news.cn/#search?keyword=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E6%94%BF%E7%AD%96&lang=cn&curPage=1&sortField=0&searchFields=1&dateFrom=&dateTo="
    html = fetch_html(url)
    items = parse_generic_list(html, "https://www.xinhuanet.com", source, "media")
    if not items:
        url2 = "http://www.xinhuanet.com/tech/"
        html2 = fetch_html(url2)
        items = parse_generic_list(html2, url2, source, "media")
    return items


def crawl_people(days, keywords):
    """人民日报"""
    source = "人民日报"
    url = "http://politics.people.com.cn/GB/1024/index.html"
    html = fetch_html(url)
    items = parse_generic_list(html, "http://www.people.com.cn", source, "media")
    return items


def crawl_cctv(days, keywords):
    """央视网"""
    source = "央视网"
    url = "https://news.cctv.com/tech/"
    html = fetch_html(url)
    return parse_generic_list(html, url, source, "media")


def crawl_smartcity(days, keywords):
    """智慧城市行业分析 - 人工智能大模型政策库"""
    from urllib.parse import unquote
    source = "智慧城市行业分析"
    base_url = "https://www.smartcity.team/category/policies/%e5%a4%a7%e6%a8%a1%e5%9e%8b%e6%94%bf%e7%ad%96%e5%ba%93/"
    html = fetch_html(base_url)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'lxml')
    items = []
    
    # 查找政策文章列表
    for article in soup.select('.post'):
        # 标题和链接
        title_elem = article.select_one('h2 a')
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        href = title_elem.get('href', '')
        if not title or not href:
            continue
        
        # href already is urlencoded, need unquote to get correct url
        url = unquote(href)
        
        # 日期信息 - 支持多种位置：entry-date / post-meta / 正文第一段 / URL
        date_text = ''
        # 先试 wordpress 默认 entry-date
        date_elem = article.select_one('.entry-date')
        if date_elem:
            date_match = re.search(r'(\d{4})[年\-](\d{1,2})[月\-](\d{1,2})[日]?', date_elem.get_text())
            if date_match:
                year, month, day = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
                try:
                    datetime(year, month, day)
                    date_text = f"{year}年{month}月{day}日"
                except ValueError:
                    pass
        # 再试 post-meta
        if not date_text:
            meta_elem = article.select_one('.post-meta')
            if meta_elem:
                date_match = re.search(r'(\d{4})[年\-](\d{1,2})[月\-](\d{1,2})[日]?', meta_elem.get_text())
                if date_match:
                    year, month, day = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
                    try:
                        datetime(year, month, day)
                        date_text = f"{year}年{month}月{day}日"
                    except ValueError:
                        pass
        # 如果还没找到，试试正文第一段
        if not date_text:
            p_elem = article.select_one('p')
            if p_elem:
                p_text = p_elem.get_text()
                date_match = re.search(r'(\d{4})[年\-](\d{1,2})[月\-](\d{1,2})[日]?', p_text)
                if date_match:
                    year, month, day = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
                    try:
                        datetime(year, month, day)
                        date_text = f"{year}年{month}月{day}日"
                    except ValueError:
                        pass
        # 如果还找不到，试试从URL提取（smartcity.team URL包含日期信息）
        if not date_text:
            # 匹配 URL 中常见的日期格式
            url_date_match = re.search(r'[/-](\d{4})[/-](\d{1,2})[/-](\d{1,2})[/-]', url)
            if not url_date_match:
                # 试试中文URL编码后的日期
                url_date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', url)
            if not url_date_match:
                # 试试 URL 路径中的 2026/03/02
                url_date_match = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})', url)
            if url_date_match:
                year, month, day = int(url_date_match.group(1)), int(url_date_match.group(2)), int(url_date_match.group(3))
                try:
                    datetime(year, month, day)
                    date_text = f"{year}年{month}月{day}日"
                except ValueError:
                    pass
        
        items.append({
            'title': title,
            'url': url,
            'date_text': date_text,
            'source': source,
            'source_type': 'media',
        })
    
    return items


# ─────────────────────────────────────────────
# 爬虫任务注册表
# ─────────────────────────────────────────────
CRAWLERS = [
    # ── 国家级（5个）──
    ("国务院",   crawl_guowuyuan),
    ("网信办",   crawl_cac),
    ("工信部",   crawl_miit),
    ("科技部",   crawl_most),
    ("发改委",   crawl_ndrc),
    # ── 广东省（保留你指定的：省 + 广州）──
    ("广东省",   crawl_gd),
    ("广州市",   crawl_gz),
    # ── 权威媒体（保留全部6个）──
    ("新华社",   crawl_xinhua),
    ("人民日报", crawl_people),
    ("央视网",   crawl_cctv),
    ("澎湃新闻", crawl_thepaper),
    ("新浪新闻", crawl_sina),
    ("凤凰网",   crawl_ifeng),
    # ── 行业政策库 ──
    ("智慧城市行业分析", crawl_smartcity),
]


# ─────────────────────────────────────────────
# 去重
# ─────────────────────────────────────────────
def deduplicate(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """去重政策列表
    
    Args:
        items: 原始政策列表
        
    Returns:
        去重后的政策列表
    """
    seen_urls = set()
    seen_titles = set()
    result = []
    for item in items:
        url = item.get('url', '').strip()
        title = item.get('title', '').strip()
        if url and url in seen_urls:
            continue
        if title and title in seen_titles:
            continue
        if url:
            seen_urls.add(url)
        if title:
            seen_titles.add(title)
        result.append(item)
    return result


# ─────────────────────────────────────────────
# 正文片段抓取（可选，耗时较长）
# ─────────────────────────────────────────────
def fetch_snippet(url: str, max_chars: int = 200) -> str:
    """抓取文章正文前N字，失败返回空字符串
    
    Args:
        url: 文章URL
        max_chars: 最大字符数
        
    Returns:
        正文片段，失败返回空字符串
    """
    try:
        html = fetch_html(url, retries=1, sleep_range=(0.2, 0.5))
        if not html:
            return ""
        soup = BeautifulSoup(html, 'lxml')
        # 移除脚本/样式
        for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()
        # 尝试找正文区域
        content = soup.select_one(
            'div.article, div.content, div#content, div.main-content, '
            'div.text, article, div.zwyw_content, div.article-content'
        )
        text = (content or soup.body or soup).get_text(separator=' ', strip=True)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text)
        return text[:max_chars]
    except Exception as e:
        logger.debug(f"snippet fetch failed: {url} -> {e}")
        return ""


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='爬取国内政府官网AI相关政策，输出JSON到stdout'
    )
    parser.add_argument(
        '--days', type=int, default=30,
        help='时间范围（天），默认30天'
    )
    parser.add_argument(
        '--keywords', nargs='+',
        default=['人工智能', 'AI', '大模型', '算法', '算力', '数字经济', '数据要素', '智能制造'],
        help='关键词列表，默认为常用AI关键词'
    )
    parser.add_argument(
        '--sources', nargs='+',
        default=None,
        help='指定爬取的来源（默认全部），如: 国务院 工信部 广东省'
    )
    parser.add_argument(
        '--no-snippet', action='store_true', default=True,
        help='不抓取正文片段（更快），默认开启，需要抓取请用 --no-no-snippet'
    )
    parser.add_argument(
        '--workers', type=int, default=2,
        help='并发线程数，默认2（减小并发避免被网站封禁，网络好可以改大）'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='输出调试日志到stderr'
    )
    args = parser.parse_args()

    # 输入验证
    if args.days < 1:
        print(json.dumps({"error": "时间范围必须大于0天", "results": []}, ensure_ascii=False))
        return
    
    if args.workers < 1 or args.workers > 20:
        print(json.dumps({"error": "并发线程数必须在1-20之间", "results": []}, ensure_ascii=False))
        return
    
    if args.keywords and len(args.keywords) > 20:
        print(json.dumps({"error": "关键词列表长度不能超过20个", "results": []}, ensure_ascii=False))
        return

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    # 过滤指定来源
    active_crawlers = CRAWLERS
    if args.sources:
        # 验证来源名称的有效性
        valid_sources = [name for name, _ in CRAWLERS]
        invalid_sources = [source for source in args.sources if source not in valid_sources]
        if invalid_sources:
            print(json.dumps({"error": f"无效的来源名称: {invalid_sources}，可用: {valid_sources}", "results": []},
                             ensure_ascii=False))
            return
        active_crawlers = [(name, fn) for name, fn in CRAWLERS if name in args.sources]
        if not active_crawlers:
            print(json.dumps({"error": f"未找到指定来源，可用: {valid_sources}", "results": []},
                             ensure_ascii=False))
            return

    logger.info(f"开始爬取 {len(active_crawlers)} 个来源，时间范围: {args.days}天，关键词: {args.keywords}")

    raw_items = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {
            executor.submit(fn, args.days, args.keywords): name
            for name, fn in active_crawlers
        }
        for future in as_completed(future_map):
            name = future_map[future]
            try:
                items = future.result()
                logger.info(f"[{name}] 获取 {len(items)} 条原始数据")
                raw_items.extend(items)
            except Exception as e:
                logger.error(f"[{name}] 爬取失败: {e}")

    # 过滤 + 去重
    filtered = []
    for item in raw_items:
        title = item.get('title', '')
        # 关键词过滤
        if not matches_keywords(title, args.keywords):
            continue
        # 日期过滤
        date_obj = parse_date(item.get('date_text', ''))
        if not is_within_days(date_obj, args.days):
            continue
        # 标准化日期
        item['date'] = date_obj.strftime('%Y-%m-%d') if date_obj else ''
        item.pop('date_text', None)
        filtered.append(item)

    filtered = deduplicate(filtered)

    # 可选：抓正文片段
    if not args.no_snippet and filtered:
        logger.info(f"开始抓取 {len(filtered)} 条政策正文片段...")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_map = {
                executor.submit(fetch_snippet, item['url']): i
                for i, item in enumerate(filtered)
            }
            for future in as_completed(future_map):
                i = future_map[future]
                try:
                    filtered[i]['content_snippet'] = future.result()
                except Exception:
                    filtered[i]['content_snippet'] = ''
    else:
        for item in filtered:
            item.setdefault('content_snippet', '')

    # 按日期降序排列
    filtered.sort(key=lambda x: x.get('date', ''), reverse=True)

    try:
        # 输出结果
        output = {
            "query_date": datetime.now().strftime('%Y-%m-%d'),
            "date_range": {
                "days": args.days,
                "from": (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d'),
                "to": datetime.now().strftime('%Y-%m-%d'),
            },
            "keywords": args.keywords,
            "total": len(filtered),
            "results": filtered,
        }

        # 修复Windows stdout编码问题，强制utf-8输出
        json_str = json.dumps(output, ensure_ascii=False, indent=2)
        if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
            sys.stdout.reconfigure(encoding='utf-8')
        print(json_str)
        logger.info(f"完成，共输出 {len(filtered)} 条政策")
    except Exception as e:
        logger.error(f"输出JSON时出错: {e}")
        # 输出错误信息
        error_output = {
            "error": f"输出结果时出错: {e}",
            "results": []
        }
        json_str = json.dumps(error_output, ensure_ascii=False)
        if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
            sys.stdout.reconfigure(encoding='utf-8')
        print(json_str)
    finally:
        # 输出请求统计信息
        with stats_lock:
            if request_stats["total"] > 0:
                success_rate = (request_stats["success"] / request_stats["total"]) * 100
                logger.info(f"请求统计: 总请求 {request_stats['total']}, 成功 {request_stats['success']}, 失败 {request_stats['failed']}, 成功率 {success_rate:.2f}%")
                if request_stats["domain_stats"]:
                    logger.info("域名请求统计:")
                    for domain, stats in request_stats["domain_stats"].items():
                        domain_success_rate = (stats["success"] / stats["total"]) * 100 if stats["total"] > 0 else 0
                        logger.info(f"  {domain}: 总请求 {stats['total']}, 成功 {stats['success']}, 失败 {stats['failed']}, 成功率 {domain_success_rate:.2f}%")


if __name__ == '__main__':
    main()
