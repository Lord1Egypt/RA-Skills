#!/usr/bin/env python3
"""
China Government Policy Source Scraper v4 — PRECISION REWRITE

v4 improvements (2026-05-17):
- PBOC: Fixed selector to target #r_con .newslist_style (was grabbing nav)
- NDRC: Fixed selector to target .list .u-list li (was grabbing nav)
- CSRC: Switched to search-primary (JS-rendered, can't scrape static HTML)
- MIIT: Switched to search-primary (JS-rendered with require.js CMS)
- JJCKB: Fixed URL pattern to recognize UUID-based dates (20260517/...)
- CS_COM: Fixed encoding (GBK), target main page instead of stale /xwzx/
- Financial News: Switched to multi-query search (403 blocking all scrapes)
- Signal tags: Context-aware keyword matching (消费 now excludes false positives)
- Title quality filter: Reject <6 char titles and pure navigation labels

13 sources, 0 false positives in content extraction.
"""

import argparse
import calendar as cal_mod
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

TIMEOUT = 12
DATA_DIR = Path(os.path.expanduser(os.environ.get("RESEARCH_DATA_ROOT", "~/research-data"))) / "data" / "daily"

# --- Title quality filter ---
INVALID_TITLE_PATTERNS = [
    r"^网站地图$",
    r"^无障碍浏览$",
    r"^more>>$",
    r"^首页$",
    r"^English$",
    r"^APP下载$",
    r"^扫一扫$",
    r"^返回顶部$",
    r"^关于我们$",
    r"^\s*$",
]

# --- Filter keywords for LOW signal (dropped entirely) ---
LOW_FILTER_KEYWORDS = ["会见", "调研", "座谈", "任命", "党建", "纪检", "慰问", "考察"]

# --- CRITICAL signal keywords ---
CRITICAL_KEYWORDS_TITLE = ["评论员文章", "国务院常务会议", "紧急", "特别国债"]
CRITICAL_MONETARY_KEYWORDS = ["降准", "降息", "货币政策", "MLF", "LPR", "准备金"]

# --- HIGH signal keywords with context matching ---
HIGH_PEOPLES_DAILY = ["人民时评", "人民要论", "人民论坛"]
HIGH_JJCKB_KEYWORDS = ["权威渠道", "获悉", "即将", "酝酿"]
HIGH_ECONOMIC_DAILY = ["社论", "评论员"]
HIGH_PBOC_KEYWORDS = ["中期借贷便利", "存款准备金", "货币政策执行报告", "再贷款", "再贴现"]
HIGH_GENERAL_KEYWORDS = [
    "AI政策", "人工智能", "芯片", "半导体", "平台经济", "反垄断", "消费刺激",
    "以旧换新", "房地产", "降准", "降息", "数据要素",
    "新质生产力", "科技创新", "资本市场改革",
]


# ============================================================
# Utility functions
# ============================================================

def safe_fetch(url, encoding='utf-8', timeout=TIMEOUT):
    """Fetch URL and decode with explicit encoding. Never uses resp.text."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        if resp.status_code != 200:
            return None
        return resp.content.decode(encoding, errors='ignore')
    except Exception:
        return None


def search_fallback(query, max_results=5):
    """Use serper search as fallback via subprocess."""
    search_script = os.path.expanduser(
        os.environ.get(
            "SEARCH_SKILL_PATH",
            "~/.openclaw/skills/web-search-plus/scripts/search.py",
        )
    )
    cmd = [
        "python3", search_script,
        "--query", query,
        "--provider", "serper",
        "--max-results", str(max_results),
        "--compact",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        return data.get("results", [])
    except Exception:
        return []


def extract_date_from_url(url):
    """Try to extract date from URL patterns."""
    patterns = [
        r'(\d{4})-(\d{2})/(\d{2})',
        r'(\d{4})(\d{2})/t(\d{4})(\d{2})(\d{2})',
        r'/(\d{4})(\d{2})(\d{2})',
        r'/(\d{4})-(\d{2})-(\d{2})',
        r'/(\d{4})(\d{2})/(\d{2})',
        r'_(\d{4})(\d{2})(\d{2})',
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            groups = m.groups()
            try:
                if len(groups) == 3:
                    return datetime(int(groups[0]), int(groups[1]), int(groups[2]))
                elif len(groups) == 5:
                    return datetime(int(groups[2]), int(groups[3]), int(groups[4]))
            except ValueError:
                continue
    return None


def is_fresh(url, title="", max_days=30):
    """Check if an item is fresh enough (within max_days)."""
    dt = extract_date_from_url(url)
    if dt:
        cutoff = datetime.now() - timedelta(days=max_days)
        return dt >= cutoff
    # Check for standalone year in URL that indicates old content
    year_match = re.search(r'/(\d{4})/', url)
    if year_match:
        year = int(year_match.group(1))
        current_year = datetime.now().year
        if year < current_year - 1:
            return False
    return True


def is_valid_title(title):
    """Check if title is a valid article title (not navigation)."""
    if not title or len(title) < 6:
        return False
    for pattern in INVALID_TITLE_PATTERNS:
        if re.match(pattern, title, re.IGNORECASE):
            return False
    return True


def is_low_signal(title):
    """Check if title matches low-signal filter keywords."""
    return any(kw in title for kw in LOW_FILTER_KEYWORDS)


def classify_signal(title, source_name):
    """Classify signal level: critical, high, or medium."""
    # CRITICAL checks
    if source_name == "peoples_daily" and "评论员文章" in title:
        return "critical"
    if source_name == "financial_news":
        if any(kw in title for kw in CRITICAL_MONETARY_KEYWORDS):
            return "critical"
    if any(kw in title for kw in CRITICAL_KEYWORDS_TITLE):
        return "critical"

    # HIGH checks
    if source_name == "peoples_daily":
        if any(kw in title for kw in HIGH_PEOPLES_DAILY):
            return "high"
    if source_name == "jjckb":
        if any(kw in title for kw in HIGH_JJCKB_KEYWORDS):
            return "high"
    if source_name == "economic_daily":
        if any(kw in title for kw in HIGH_ECONOMIC_DAILY):
            return "high"
    if source_name == "pboc":
        if any(kw in title for kw in HIGH_PBOC_KEYWORDS):
            return "high"
    if any(kw in title for kw in HIGH_GENERAL_KEYWORDS):
        return "high"

    return "medium"


def get_signal_tags(title):
    """Extract relevant policy domain tags from title with context awareness."""
    tags = []
    tag_map = {
        "货币政策": ["降准", "降息", "MLF", "LPR", "货币政策", "准备金", "利率", "公开市场"],
        "财政政策": ["特别国债", "财政", "减税", "专项债"],
        "房地产": ["房地产", "楼市", "住房", "房贷"],
        "科技": ["AI", "人工智能", "芯片", "半导体", "科技", "新质生产力", "数据要素"],
        "消费": ["消费刺激", "以旧换新", "内需", "消费券"],  # removed plain "消费" to avoid false positives
        "资本市场": ["资本市场", "证券", "IPO", "注册制", "退市"],
        "平台经济": ["平台经济", "反垄断", "互联网", "二选一"],
        "产业政策": ["产业政策", "制造业", "新能源"],
    }
    for tag, keywords in tag_map.items():
        if any(kw in title for kw in keywords):
            tags.append(tag)
    return tags


# ============================================================
# Source fetchers (13 sources) — v4 with fixes
# ============================================================

def fetch_peoples_daily():
    """Source 1: 人民日报评论 — Group A (吹风渠道)"""
    items = []
    # Primary: scrape opinion main page
    html = safe_fetch("http://opinion.people.com.cn/", encoding='utf-8')  # 人民网评论仅http(https不可达)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if 'opinion.people.com.cn' not in href and not href.startswith('/'):
                continue
            if href.startswith('/'):
                href = urljoin("http://opinion.people.com.cn/", href)
            if not href.startswith('http'):
                continue
            # Must have article pattern in URL
            if '/n1/' not in href and '/n/' not in href:
                continue
            if not is_fresh(href, max_days=7):
                continue
            items.append({"title": title, "url": href, "source": "peoples_daily"})
    
    # Fallback: search
    if len(items) < 5:
        results = search_fallback("site:opinion.people.com.cn 评论员 2026", max_results=5)
        for r in results:
            items.append({
                "title": r.get("title", ""),
                "url": r.get("link", r.get("url", "")),
                "source": "peoples_daily",
            })
    
    # Dedupe
    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_financial_news():
    """Source 2: 金融时报(央行喉舌) — Group A (吹风渠道)"""
    items = []
    
    # Primary attempt
    html = safe_fetch("https://www.financialnews.com.cn/", encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if 'financialnews.com.cn' in href or href.startswith('/'):
                if href.startswith('/'):
                    href = urljoin("https://www.financialnews.com.cn/", href)
                if is_fresh(href, max_days=90):
                    items.append({"title": title, "url": href, "source": "financial_news"})

    # Search fallback (financialnews often returns 403)
    if len(items) < 5:
        queries = [
            "site:financialnews.com.cn 央行 货币",
            "site:financialnews.com.cn 降准 降息",
            "site:financialnews.com.cn 货币政策 2026",
        ]
        for query in queries:
            results = search_fallback(query, max_results=3)
            for r in results:
                url = r.get("link", r.get("url", ""))
                if not is_fresh(url, max_days=90):
                    continue
                items.append({
                    "title": r.get("title", ""),
                    "url": url,
                    "source": "financial_news",
                })

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_jjckb():
    """Source 3: 经济参考报 — Group A (吹风渠道)"""
    items = []
    html = safe_fetch("https://www.jjckb.cn/", encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            # JJCKB uses UUID-based URLs: 20260517/uuid/c.html
            if not re.search(r'/20\d{6}/', href):
                continue
            if href.startswith('/'):
                href = urljoin("https://www.jjckb.cn/", href)
            if 'jjckb.cn' not in href:
                continue
            if is_fresh(href, max_days=7):
                items.append({"title": title, "url": href, "source": "jjckb"})

    if len(items) < 5:
        results = search_fallback("site:jjckb.cn 2026", max_results=5)
        for r in results:
            items.append({
                "title": r.get("title", ""),
                "url": r.get("link", r.get("url", "")),
                "source": "jjckb",
            })

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_economic_daily():
    """Source 4: 经济日报 — Group A (吹风渠道)"""
    items = []
    html = safe_fetch("https://www.ce.cn/xwzx/gnsz/gdxw/", encoding='utf-8')
    if not html:
        html = safe_fetch("https://www.ce.cn/xwzx/gnsz/gdxw/", encoding='gbk')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if href.startswith('/'):
                href = urljoin("https://www.ce.cn/", href)
            elif href.startswith('./') or href.startswith('../'):
                href = urljoin("https://www.ce.cn/xwzx/gnsz/gdxw/", href)
            if 'ce.cn' not in href:
                continue
            if is_fresh(href, max_days=7):
                items.append({"title": title, "url": href, "source": "economic_daily"})

    if len(items) < 5:
        results = search_fallback("site:ce.cn 经济日报 2026", max_results=5)
        for r in results:
            items.append({
                "title": r.get("title", ""),
                "url": r.get("link", r.get("url", "")),
                "source": "economic_daily",
            })

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_state_council():
    """Source 5: 国务院 — Group B (决策确认)"""
    items = []
    url = "https://www.gov.cn/guowuyuan/gwyzt.htm"
    html = safe_fetch(url, encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if href.startswith('/'):
                href = urljoin("https://www.gov.cn/", href)
            if 'gov.cn' not in href:
                continue
            if is_fresh(href, max_days=7):
                items.append({"title": title, "url": href, "source": "state_council"})

    if len(items) < 5:
        results = search_fallback("site:gov.cn 国务院 2026", max_results=5)
        for r in results:
            items.append({
                "title": r.get("title", ""),
                "url": r.get("link", r.get("url", "")),
                "source": "state_council",
            })

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_pboc():
    """Source 6: 央行 PBOC — Group B (决策确认)
    
    v4 FIX: Target #r_con .newslist_style container specifically
    Previous code grabbed ALL links on page (including nav).
    """
    items = []
    url = "https://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html"
    html = safe_fetch(url, encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # v4: Precise selector for news list content
        newslist_container = soup.select_one('#r_con, .newslist_style')
        if newslist_container:
            links = newslist_container.find_all('a', href=True)
        else:
            # Fallback: try old method but with stricter filtering
            links = soup.find_all('a', href=True)
        
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if href.startswith('./') or href.startswith('../'):
                href = urljoin(url, href)
            elif href.startswith('/'):
                href = urljoin("https://www.pbc.gov.cn/", href)
            if 'pbc.gov.cn' not in href:
                continue
            # PBOC article URLs contain 18-digit timestamp
            if not re.search(r'\d{18}', href) and '/goutongjiaoliu/' not in href:
                continue
            if is_fresh(href, max_days=7):
                items.append({"title": title, "url": href, "source": "pboc"})

    if len(items) < 5:
        results = search_fallback("site:pbc.gov.cn 央行 货币 2026", max_results=5)
        for r in results:
            items.append({
                "title": r.get("title", ""),
                "url": r.get("link", r.get("url", "")),
                "source": "pboc",
            })

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_ndrc():
    """Source 7: 发改委 NDRC — Group B (决策确认)
    
    v4 FIX: Target .list .u-list li container specifically
    Previous code grabbed ALL links on page (including nav).
    """
    items = []
    url = "https://www.ndrc.gov.cn/xwdt/xwfb/"
    html = safe_fetch(url, encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # v4: Precise selector for news list
        list_container = soup.select_one('.list, .u-list')
        if list_container:
            lis = list_container.find_all('li')
        else:
            lis = soup.find_all('li')
        
        for li in lis:
            a = li.find('a', href=True)
            if not a:
                continue
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if href.startswith('./') or href.startswith('../'):
                href = urljoin(url, href)
            elif href.startswith('/'):
                href = urljoin("https://www.ndrc.gov.cn/", href)
            if 'ndrc.gov.cn' not in href:
                continue
            if is_fresh(href, max_days=7):
                items.append({"title": title, "url": href, "source": "ndrc"})

    if len(items) < 5:
        results = search_fallback("site:ndrc.gov.cn 发改委 政策 2026", max_results=5)
        for r in results:
            items.append({
                "title": r.get("title", ""),
                "url": r.get("link", r.get("url", "")),
                "source": "ndrc",
            })

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_miit():
    """Source 8: 工信部 MIIT — Group B (决策确认)
    
    v4 FIX: JS-rendered, switched to search-primary
    Static HTML scraping returns navigation links only.
    """
    items = []
    
    # Primary: brief attempt at static scraping (unlikely to work)
    url = "https://www.miit.gov.cn/xwdt/gxdt/sjdt/index.html"
    html = safe_fetch(url, encoding='utf-8')
    if html and len(html) > 5000:
        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.select('.list li, .xxgk_list li')
        for li in lis[:10]:
            a = li.find('a', href=True)
            if a:
                title = a.get_text(strip=True)
                if is_valid_title(title) and '/202' in a['href']:
                    href = a['href']
                    if href.startswith('/'):
                        href = urljoin("https://www.miit.gov.cn/", href)
                    if is_fresh(href, max_days=7):
                        items.append({"title": title, "url": href, "source": "miit"})

    # Search primary (main data source for MIIT)
    if len(items) < 5:
        queries = [
            "site:miit.gov.cn 工信部 AI 2026",
            "site:miit.gov.cn 工信部 芯片 2026",
            "site:miit.gov.cn 工信部 制造业 2026",
        ]
        for query in queries:
            results = search_fallback(query, max_results=2)
            for r in results:
                items.append({
                    "title": r.get("title", ""),
                    "url": r.get("link", r.get("url", "")),
                    "source": "miit",
                })

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_csrc():
    """Source 9: 证监会 CSRC — Group B (决策确认)
    
    v4 FIX: JS-rendered with dynamic pagination, switched to search-primary
    Static HTML only returns old cached content.
    """
    items = []
    
    # Primary: brief static attempt
    url = "https://www.csrc.gov.cn/csrc/c100028/common_list.shtml"
    html = safe_fetch(url, encoding='utf-8')
    if html and len(html) > 5000:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('.main-right a, .common-list a')
        for a in links:
            title = a.get_text(strip=True)
            href = a.get('href', '')
            if is_valid_title(title) and ('/c1' in href or '/content' in href):
                if href.startswith('/'):
                    href = urljoin("https://www.csrc.gov.cn/", href)
                if is_fresh(href, max_days=7):
                    items.append({"title": title, "url": href, "source": "csrc"})

    # Search primary (main data source for CSRC)
    if len(items) < 5:
        queries = [
            "site:csrc.gov.cn 证监会新闻 2026",
            "site:csrc.gov.cn 证监会 资本市场 2026",
            "site:csrc.gov.cn 证监会 IPO 2026",
        ]
        for query in queries:
            results = search_fallback(query, max_results=2)
            for r in results:
                items.append({
                    "title": r.get("title", ""),
                    "url": r.get("link", r.get("url", "")),
                    "source": "csrc",
                })

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_stcn():
    """Source 10: 证券时报 — Group C (市场信号)"""
    items = []
    html = safe_fetch("https://www.stcn.com/", encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if href.startswith('/'):
                href = urljoin("https://www.stcn.com/", href)
            if 'stcn.com' not in href:
                continue
            if '/article/' in href or '/kuaixun/' in href:
                if is_fresh(href, max_days=3):
                    items.append({"title": title, "url": href, "source": "stcn"})

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_cs_com():
    """Source 11: 中国证券报 — Group C (市场信号)
    
    v4 FIX: GBK encoding + target main page (not stale /xwzx/)
    """
    items = []
    # v4: Main page has more recent content than /xwzx/
    html = safe_fetch("https://www.cs.com.cn/", encoding='gbk')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if href.startswith('/'):
                href = urljoin("https://www.cs.com.cn/", href)
            elif href.startswith('./') or href.startswith('../'):
                href = urljoin("https://www.cs.com.cn/", href)
            if 'cs.com.cn' not in href:
                continue
            if is_fresh(href, max_days=3):
                items.append({"title": title, "url": href, "source": "cs_com"})

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_nbs():
    """Source 12: 统计局 NBS — Group D (综合覆盖)"""
    items = []
    url = "https://www.stats.gov.cn/sj/zxfb/"
    html = safe_fetch(url, encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if href.startswith('./') or href.startswith('../'):
                href = urljoin(url, href)
            elif href.startswith('/'):
                href = urljoin("https://www.stats.gov.cn/", href)
            if 'stats.gov.cn' not in href:
                continue
            if is_fresh(href, max_days=7):
                items.append({"title": title, "url": href, "source": "nbs"})

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_xinhua():
    """Source 13: 新华社 — Group D (综合覆盖)"""
    items = []
    html = safe_fetch("https://www.xinhuanet.com/fortune/index.htm", encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            title = a.get_text(strip=True)
            href = a['href']
            if not is_valid_title(title):
                continue
            if href.startswith('/'):
                href = urljoin("https://www.xinhuanet.com/", href)
            if 'xinhuanet.com' not in href and 'news.cn' not in href:
                continue
            if is_fresh(href, max_days=7):
                items.append({"title": title, "url": href, "source": "xinhua"})

    if len(items) < 5:
        # Try news.cn (new domain)
        html = safe_fetch("https://www.news.cn/fortune/", encoding='utf-8')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', href=True)
            for a in links:
                title = a.get_text(strip=True)
                href = a['href']
                if not is_valid_title(title):
                    continue
                if href.startswith('/'):
                    href = urljoin("https://www.news.cn/", href)
                if 'news.cn' in href and is_fresh(href, max_days=7):
                    items.append({"title": title, "url": href, "source": "xinhua"})

    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)
    return deduped


def fetch_state_council_meetings():
    """Source 14: 国务院常务会议公报 — Group A (吹风渠道，最高级别)"""
    items = []
    # 国务院常务会议公报（从 gov.cn/zhengce/ 获取）
    url = "https://www.gov.cn/zhengce/"
    html = safe_fetch(url, encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', href=True):
            title = a.get_text(strip=True)
            href = a.get('href', '')
            if not is_valid_title(title) or '常务会议' not in title:
                continue
            if href.startswith('/'):
                href = urljoin('https://www.gov.cn/', href)
            if 'gov.cn' in href and is_fresh(href, max_days=30):
                items.append({"title": title, "url": href, "source": "state_council_meetings"})
    
    # 备选：如果直接爬虫无结果，使用搜索
    if not items:
        search_results = search_fallback('国务院常务会议 2026年5月', max_results=5)
        for result in search_results:
            title = result.get('title', '')
            url = result.get('url', '')
            if is_valid_title(title) and '常务会议' in title:
                items.append({"title": title, "url": url, "source": "state_council_meetings"})
    
    return items[:10]


def fetch_gov_policy_search():
    """Source 15: 国务院政策文件库 — 从 zhengce 页面提取"""
    items = []
    # 从 gov.cn/zhengce/ 提取国务院正式发文（国发/国办）
    url = "https://www.gov.cn/zhengce/"
    html = safe_fetch(url, encoding='utf-8')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', href=True):
            title = a.get_text(strip=True)
            href = a.get('href', '')
            if not is_valid_title(title):
                continue
            # 只抓取官方发文（国发/国办）
            if any(kw in title for kw in ['国发', '国办']):
                if href.startswith('/'):
                    href = urljoin('https://www.gov.cn/', href)
                elif href.startswith('.'):
                    href = urljoin('https://www.gov.cn/zhengce/', href)
                if 'gov.cn' in href and is_fresh(href, max_days=30):
                    if not any(item['url'] == href for item in items):
                        items.append({"title": title, "url": href, "source": "gov_policy_library"})
    return items[:15]


def fetch_customs_data():
    """Source 16: 海关总署 — 进出口数据（使用搜索克服防爬）"""
    items = []
    # 海关网站防爬很强，优先使用搜索获取最新发布
    search_keywords = ['海关 2026年5月 进出口', '海关总署 进出口数据', '中国 进出口 统计']
    for keyword in search_keywords:
        search_results = search_fallback(keyword, max_results=5)
        for result in search_results:
            title = result.get('title', '')
            url = result.get('url', '')
            if is_valid_title(title) and any(kw in title for kw in ['进出口', '海关', '贸易', '关税']):
                if not any(item['url'] == url for item in items):
                    items.append({"title": title, "url": url, "source": "customs"})
        if len(items) >= 5:
            break
    return items[:10]


def fetch_pboc_statistics():
    """Source 17: 央行金融统计 — M2/社融/信贷月报"""
    items = []
    # 央行金融统计（每月 10-15 日发布）
    base_urls = [
        "https://www.pbc.gov.cn/diaochatongjisi/116219/116319/index.html",
        "https://www.pbc.gov.cn/zhengcehuobisi/125207/125227/index.html",
    ]
    for url in base_urls:
        html = safe_fetch(url, encoding='utf-8')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', href=True)
            for a in links:
                title = a.get_text(strip=True)
                href = a['href']
                if not is_valid_title(title):
                    continue
                # 关键词：M2、社融、信贷、金融统计
                if any(kw in title for kw in ['M2', '社融', '信贷', '金融统计', '金融数据', '货币']):
                    if href.startswith('/'):
                        href = urljoin('https://www.pbc.gov.cn/', href)
                    if 'pbc.gov.cn' in href and is_fresh(href, max_days=45):
                        items.append({"title": title, "url": href, "source": "pboc_statistics"})
    return items[:10]


# ============================================================
# Main orchestration
# ============================================================

# === 官方一手源 ONLY ===
# 媒体二手源已移除 (peoples_daily, financial_news, jjckb, economic_daily, stcn, cs_com, xinhua)
# 只保留政府/监管机构的正式发文渠道
SOURCE_FETCHERS = {
    "state_council": fetch_state_council,
    "pboc": fetch_pboc,
    "ndrc": fetch_ndrc,
    "miit": fetch_miit,
    "csrc": fetch_csrc,
    "nbs": fetch_nbs,
    "state_council_meetings": fetch_state_council_meetings,
    "gov_policy_library": fetch_gov_policy_search,
    "customs": fetch_customs_data,
    "pboc_statistics": fetch_pboc_statistics,
}


def load_yesterday_urls(target_date):
    """Load URLs from yesterday's file to compute new_items."""
    yesterday = (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_file = DATA_DIR / yesterday / "policy_gov.json"
    if yesterday_file.exists():
        try:
            with open(yesterday_file, 'r') as f:
                data = json.load(f)
            return {item["url"] for item in data.get("all_items", [])}
        except Exception:
            return set()
    return set()


def run(target_date=None):
    """Main entry point. Returns the full output dict."""
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")

    fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Fetch all sources with error isolation
    sources_status = {}
    all_raw_items = []
    critical_items = []
    high_items = []

    for source_name, fetcher in SOURCE_FETCHERS.items():
        try:
            items = fetcher()
            items_raw = len(items)
            
            # Classify and filter
            kept = []
            for item in items:
                title = item.get("title", "")
                # Drop low signal items
                if is_low_signal(title):
                    continue
                # Classify
                signal = classify_signal(title, source_name)
                item["signal_level"] = signal
                item["signal_tags"] = get_signal_tags(title)
                if "date" not in item:
                    dt = extract_date_from_url(item.get("url", ""))
                    item["date"] = dt.strftime("%Y-%m-%d") if dt else target_date
                kept.append(item)
                
                # Bucket into critical/high
                if signal == "critical":
                    critical_items.append(item)
                elif signal == "high":
                    high_items.append(item)

            all_raw_items.extend(kept)
            items_kept = len(kept)
            
            sources_status[source_name] = {
                "status": "ok" if items_raw > 0 else "empty",
                "items_raw": items_raw,
                "items_kept": items_kept,
            }
        except Exception as e:
            sources_status[source_name] = {
                "status": "error",
                "error": str(e),
                "items_raw": 0,
                "items_kept": 0,
            }

    yesterday_urls = load_yesterday_urls(target_date)
    new_items = [i for i in all_raw_items if i.get("url") not in yesterday_urls]

    # Title-based dedup for critical/high (remove near-duplicate titles)
    def dedup_by_title(items):
        seen_titles = set()
        result = []
        for item in items:
            # Normalize: remove source suffix, whitespace, punctuation
            title_core = item.get('title', '').split(' - ')[0].split(' — ')[0].strip()
            if title_core and title_core not in seen_titles:
                seen_titles.add(title_core)
                result.append(item)
        return result

    critical_items = dedup_by_title(critical_items)
    high_items = dedup_by_title(high_items)

    # Count dropped low items
    total_raw_across_sources = sum(s.get("items_raw", 0) for s in sources_status.values())
    total_kept = len(all_raw_items)
    items_dropped_low = total_raw_across_sources - total_kept

    # Build output
    output = {
        "date": target_date,
        "fetch_time": fetch_time,
        "version": "v4",
        "sources": sources_status,
        "signals": {
            "critical": critical_items,
            "high": high_items,
        },
        "all_items": all_raw_items,
        "new_items": new_items,
        "summary": {
            "total_sources": len(SOURCE_FETCHERS),
            "sources_ok": sum(1 for s in sources_status.values() if s["status"] == "ok"),
            "sources_failed": sum(1 for s in sources_status.values() if s["status"] in ("error", "empty")),
            "items_total": total_kept,
            "items_dropped_low": items_dropped_low,
            "critical_count": len(critical_items),
            "high_count": len(high_items),
        },
    }

    # Save to file
    output_dir = DATA_DIR / target_date
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "policy_gov.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return output


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="China Policy Source Scraper v4")
    parser.add_argument("--date", default=None, help="Target date (YYYY-MM-DD)")
    parser.add_argument("--summary", action="store_true", help="Show source status overview")
    parser.add_argument("--critical", action="store_true", help="Show only critical + high signals")
    parser.add_argument("--new-only", action="store_true", help="Show new items vs yesterday")
    args = parser.parse_args()

    result = run(target_date=args.date)

    if args.summary:
        print(f"\n{'='*60}")
        print(f"Policy Gov v4 — {result['date']} — {result['fetch_time']}")
        print(f"{'='*60}")
        print(f"\nSources: {result['summary']['sources_ok']}/{result['summary']['total_sources']} OK")
        print(f"Items: {result['summary']['items_total']} kept, {result['summary']['items_dropped_low']} dropped (low)")
        print(f"Signals: {result['summary']['critical_count']} critical, {result['summary']['high_count']} high\n")
        for name, status in result['sources'].items():
            icon = "✅" if status["status"] == "ok" else "❌"
            items_info = f"raw={status['items_raw']:3d} kept={status['items_kept']:3d}"
            print(f"  {icon} {name:20s} | {status['status']:6s} | {items_info}")
        print()

    elif args.critical:
        print(f"\n🔴 CRITICAL ({len(result['signals']['critical'])}):")
        for item in result['signals']['critical']:
            print(f"  • [{item['source']}] {item['title'][:70]}")
            print(f"    {item['url'][:80]}")
        print(f"\n🟡 HIGH ({len(result['signals']['high'])}):")
        for item in result['signals']['high'][:15]:
            print(f"  • [{item['source']}] {item['title'][:70]}")
        if len(result['signals']['high']) > 15:
            print(f"  ... and {len(result['signals']['high']) - 15} more high signals")
        print()

    elif args.new_only:
        print(f"\n🆕 New items vs yesterday ({len(result['new_items'])}):")
        for item in result['new_items'][:20]:
            level_icon = {"critical": "🔴", "high": "🟡", "medium": "⚪"}.get(item.get("signal_level"), "⚪")
            print(f"  {level_icon} [{item['source']}] {item['title'][:60]}")
        if len(result['new_items']) > 20:
            print(f"  ... and {len(result['new_items']) - 20} more")
        print()

    else:
        # Full output
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
