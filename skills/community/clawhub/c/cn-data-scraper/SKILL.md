---
name: cn-data-scraper
description: "Chinese website data scraping expert with anti-bypass strategies (中国网站数据爬取专家+反爬绕过策略). Teach AI agents to scrape Chinese websites that Scrapling alone can't handle — Baidu anti-crawl, Taobao login walls, Douyin dynamic rendering, Zhihu verification, WeChat articles, 1688 product data. Features: (1) Platform-specific anti-crawl bypass recipes for 10+ Chinese websites, (2) Scrapling integration guides with Chinese site configurations, (3) Adaptive selector strategies for frequently-redesigned Chinese sites, (4) Legal compliance boundary guide (what's legal vs illegal in China's data scraping), (5) Executable scripts for common scraping tasks, (6) MCP server integration for AI agent workflows. ONLY skill combining Chinese website scraping expertise + legal compliance + Scrapling integration. Use when: scraping Chinese websites, bypassing Baidu anti-crawl, scraping Taobao data, Douyin data extraction, Zhihu scraping, WeChat article scraping, 1688 product scraping, Chinese data collection, 爬虫, 数据爬取, 反爬绕过, 百度反爬, 淘宝爬虫, 抖音数据, 知乎爬虫, 微信文章抓取, Scrapling Chinese, 中国网站爬虫. Triggers: Chinese web scraping, data scraping China, anti-crawl bypass, Baidu scraping, Taobao scraping, Douyin scraping, Zhihu scraping, WeChat scraping, 1688 scraping, 爬虫工具, 数据采集, 反爬虫, 信息差, Scrapling配置, 中国网站数据, cn-scraping, web scraping China, data extraction Chinese websites, crawler Chinese sites, Python爬虫中国网站"
---

# Chinese Data Scraper — 中国网站数据爬取专家

> ## ⚡ INSTANT VALUE — Install This If You:
> - Need to scrape **Baidu/Taobao/Douyin/Zhihu/WeChat/1688** but keep hitting anti-crawl walls
> - Want **platform-specific bypass recipes** — not generic "use Selenium" advice, but tested configs for each Chinese site
> - Are using **Scrapling** but need Chinese site configurations (Baidu's cookie walls, Taobao's login gates, Douyin's dynamic rendering)
> - Want to know **what's legal** — China's data scraping legal boundaries (Criminal Law 285/286, Data Security Law, PIPL)
>
> **🎯 Why this over generic scraping skills?** Generic scraping skills give you BeautifulSoup/Selenium tutorials. We give you **tested anti-crawl configs for 10+ Chinese websites**, **legal compliance boundaries** (avoid Criminal Law 285!), and **Scrapling integration** with Chinese site presets. Tutorials vs Recipes — you decide.
>
> **🔗 Based on Scrapling (31K+ GitHub Stars)** — the fastest Python scraping framework with adaptive selectors and Cloudflare bypass. We add the China layer on top.

You are a Chinese website data scraping expert. You help AI agents and developers scrape data from Chinese websites that are notoriously difficult to crawl — Baidu, Taobao, Douyin, Zhihu, WeChat, 1688, and more.

## Core Philosophy

**Scrapling solves the general scraping problem. We solve the China-specific problem.**

Chinese websites have unique anti-crawl mechanisms that generic tools can't handle:
- Baidu's multi-layer cookie verification + JS encryption
- Taobao's mandatory login gates + dynamic pricing
- Douyin's signature algorithm + device fingerprinting
- Zhihu's X-Zse-93 encryption + rate limiting
- WeChat's closed ecosystem + no public API
- 1688's anti-bot + business data protection

This skill provides **tested recipes** for each platform, not generic advice.

---

## 🏗️ Architecture: Scrapling + China Layer

```
┌─────────────────────────────────────┐
│         AI Agent / User             │
├─────────────────────────────────────┤
│      cn-data-scraper Skill          │
│  ┌─────────────┐ ┌───────────────┐  │
│  │ Platform    │ │ Legal         │  │
│  │ Recipes     │ │ Compliance    │  │
│  │ (10+ sites) │ │ Boundaries    │  │
│  └──────┬──────┘ └───────┬───────┘  │
│         │                │          │
│  ┌──────▼────────────────▼───────┐  │
│  │    Scrapling Framework        │  │
│  │  (Adaptive Selectors +        │  │
│  │   StealthyFetcher +           │  │
│  │   Camoufox Engine)            │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 📋 Platform-Specific Anti-Crawl Recipes

### 1. 百度 (Baidu) — 搜索结果 + 百度知道 + 百科

**Anti-crawl mechanisms:**
- Multi-layer cookie verification (BDORZ + BAIDUID + BIDUPSID)
- JS-encrypted search parameters
- Rate limiting by IP (100 requests/hour for unauthenticated)
- CAPTCHA after threshold

**Scrapling configuration:**
```python
from scrapling import StealthyFetcher

# Baidu search with anti-crawl bypass
page = StealthyFetcher.fetch(
    'https://www.baidu.com/s?wd=关键词',
    headless=True,
    network_idle=True,  # Wait for JS execution
    timeout=30000,
)

# Extract search results — use adaptive selectors
# Baidu frequently changes class names, so use structural selectors
results = page.css('div.c-container')  # More stable than class-based
for result in results:
    title = result.css_first('h3 a')
    snippet = result.css_first('span.content-right_8Zs40')
    # Fallback: adaptive selector if structure changed
    if not snippet:
        snippet = result.css_first('[class*="content"]')
```

**Key tips:**
- Add `User-Agent` with Baidu app identifier for mobile results
- Use `network_idle=True` — Baidu loads results via AJAX
- Rotate cookies every 50 requests
- Avoid scraping between 8:00-10:00 AM (peak monitoring hours)

### 2. 淘宝/天猫 (Taobao/Tmall) — 商品数据 + 评价

**Anti-crawl mechanisms:**
- Mandatory login gate for search
- Dynamic pricing based on user profile
- Anti-bot via mtop API signature
- Device fingerprinting (umid token)

**Scrapling configuration:**
```python
# Taobao requires login — use cookie injection
page = StealthyFetcher.fetch(
    'https://s.taobao.com/search?q=关键词',
    headless=True,
    network_idle=True,
    # Must inject login cookies
    cookies={
        '_m_h5_tk': 'your_token_here',
        '_m_h5_tk_enc': 'your_enc_token_here',
        'cookie2': 'your_cookie2',
        'sgcookie': 'your_sgcookie',
    }
)

# Extract product data
products = page.css('div.Card--doubleCardWrapper')
for product in products:
    title = product.css_first('span.Title--titleSpan')
    price = product.css_first('span.Price--priceInt')
    sales = product.css_first('span.Sales--sales')
```

**Key tips:**
- Login cookies expire every 24 hours — need refresh mechanism
- Mobile API (h5api.m.taobao.com) is easier to scrape than desktop
- Use `mtop.taobao.searchapi.search` API endpoint for structured data
- Price data differs by user profile — use anonymous cookies for baseline

### 3. 抖音 (Douyin/TikTok CN) — 视频数据 + 用户信息

**Anti-crawl mechanisms:**
- X-Bogus signature algorithm (proprietary)
- Device fingerprinting (aid + version + platform)
- Rate limiting by device ID
- CAPTCHA for suspicious patterns

**Scrapling configuration:**
```python
# Douyin web version — easier than app API
page = StealthyFetcher.fetch(
    'https://www.douyin.com/search/关键词',
    headless=True,
    network_idle=True,
    wait_selector='div.video-card',  # Wait for video cards to load
)

# Extract video data
videos = page.css('div.video-card')
for video in videos:
    title = video.css_first('p.title')
    author = video.css_first('span.author-card-user-name')
    likes = video.css_first('span.video-like-count')
```

**Key tips:**
- Web version is easier than app API — start with web
- X-Bogus algorithm changes every 2-4 weeks — use adaptive selectors
- Rate limit: 30 requests/minute for web, 10/minute for API
- Video download URLs expire in 1 hour
- **⚠️ DO NOT attempt to scrape user private data — Criminal Law 253**

### 4. 知乎 (Zhihu) — 问答 + 文章 + 评论

**Anti-crawl mechanisms:**
- X-Zse-93/X-Zse-96 encryption headers
- Rate limiting by IP + cookie
- Login wall for full content
- Anti-bot via behavioral analysis

**Scrapling configuration:**
```python
# Zhihu search — use API endpoint for structured data
page = StealthyFetcher.fetch(
    'https://www.zhihu.com/search?type=content&q=关键词',
    headless=True,
    network_idle=True,
    # Zhihu requires specific headers
    headers={
        'Referer': 'https://www.zhihu.com/',
    }
)

# Extract search results
results = page.css('div.SearchResult-Card')
for result in results:
    title = result.css_first('h2.ContentItem-title a')
    excerpt = result.css_first('span.RichText')
    author = result.css_first('meta[itemprop="name"]')
```

**Key tips:**
- API endpoint `api.zhihu.com/search_v3` returns JSON — easier to parse
- X-Zse-93 encryption requires reverse engineering — use browser automation instead
- Anonymous access limited to 5 pages per search
- Login cookies extend to 20 pages
- **⚠️ Respect Zhihu's robots.txt — do not scrape user profiles in bulk**

### 5. 微信公众号 (WeChat Official Accounts) — 文章内容

**Anti-crawl mechanisms:**
- Closed ecosystem — no public search API
- Article URLs expire and are non-guessable
- Anti-bot via WeChat referrer check
- Rate limiting by IP

**Scrapling configuration:**
```python
# WeChat article — direct URL access
page = StealthyFetcher.fetch(
    'https://mp.weixin.qq.com/s/ARTICLE_ID',
    headless=True,
    network_idle=True,
)

# Extract article content
title = page.css_first('h1.rich_media_title')
content = page.css_first('div.rich_media_content')
author = page.css_first('a.rich_media_meta_link')
publish_time = page.css_first('em#publish_time')
```

**Key tips:**
- Article URLs can only be found via Sogou WeChat search or account history
- Sogou WeChat search: `weixin.sogou.com` — but has aggressive anti-crawl
- Use `mp.weixin.qq.com` direct access for known URLs
- Content is server-rendered — no need for JS execution
- **⚠️ DO NOT redistribute scraped articles — copyright infringement risk**

### 6. 1688 (Alibaba Wholesale) — 商品数据 + 供应商

**Anti-crawl mechanisms:**
- Anti-bot via Alibaba's security system
- Login requirement for contact info
- Dynamic pricing based on buyer profile
- Image watermarking

**Scrapling configuration:**
```python
# 1688 search
page = StealthyFetcher.fetch(
    'https://s.1688.com/selloffer/offer_search.htm?keywords=关键词',
    headless=True,
    network_idle=True,
)

# Extract product listings
products = page.css('div.offer-item')
for product in products:
    title = product.css_first('a.title')
    price = product.css_first('span.price')
    min_order = product.css_first('span.min-order')
    supplier = product.css_first('a.company-name')
```

### 7. 小红书 (Xiaohongshu/RED) — 笔记 + 评论

**Anti-crawl mechanisms:**
- X-s/X-t signature algorithm
- Device fingerprinting
- Aggressive rate limiting (10 requests/minute)
- CAPTCHA after threshold

**Scrapling configuration:**
```python
# Xiaohongshu web version
page = StealthyFetcher.fetch(
    'https://www.xiaohongshu.com/search_result?keyword=关键词',
    headless=True,
    network_idle=True,
    wait_selector='section.note-item',
)

# Extract notes
notes = page.css('section.note-item')
for note in notes:
    title = note.css_first('div.title')
    author = note.css_first('span.name')
    likes = note.css_first('span.like-wrapper .count')
```

**Key tips:**
- Web version has limited results — mobile API has more data
- X-s signature changes frequently — use browser automation as fallback
- Rate limit is very aggressive — 10 req/min for anonymous
- **⚠️ Scraping user-generated content may violate platform ToS**

### 8. 微博 (Weibo) — 热搜 + 用户帖子 + 评论

**Anti-crawl mechanisms:**
- Login requirement for search
- Rate limiting by cookie
- Anti-bot via behavioral analysis
- Content censorship (some posts invisible without login)

**Scrapling configuration:**
```python
# Weibo search
page = StealthyFetcher.fetch(
    'https://s.weibo.com/weibo?q=关键词',
    headless=True,
    network_idle=True,
    cookies={
        'SUB': 'your_sub_cookie',  # Required for search
    }
)

# Extract posts
posts = page.css('div.card-wrap[action-type="feed_list_item"]')
for post in posts:
    author = post.css_first('a.name')
    content = post.css_first('p.txt')
    reposts = post.css_first('a[action-type="fl_forward"] em')
    comments = post.css_first('a[action-type="flcomment"] em')
    likes = post.css_first('a[action-type="fl_like"] em')
```

### 9. CSDN — 技术博客 + 资源

**Anti-crawl mechanisms:**
- Login wall for full article content
- Anti-copy protection (JS overlay)
- Rate limiting by IP
- VIP content paywall

**Scrapling configuration:**
```python
# CSDN article
page = StealthyFetcher.fetch(
    'https://blog.csdn.net/author/article/ID',
    headless=True,
    network_idle=True,
)

# Remove anti-copy overlay
content = page.css_first('article.baidu_pl')
# Content is in HTML, anti-copy is just a CSS overlay
```

### 10. Boss直聘 (Boss Zhipin) — 招聘数据

**Anti-crawl mechanisms:**
- Mandatory login
- Device fingerprinting
- Anti-bot via zpData encryption
- Rate limiting by cookie + IP

**Scrapling configuration:**
```python
# Boss Zhipin search
page = StealthyFetcher.fetch(
    'https://www.zhipin.com/web/geek/job?query=关键词',
    headless=True,
    network_idle=True,
    cookies={
        'geek_zp_token': 'your_token',
    }
)

# Extract job listings
jobs = page.css('li.job-card-wrapper')
for job in jobs:
    title = job.css_first('span.job-name')
    salary = job.css_first('span.salary')
    company = job.css_first('h3.company-name')
    location = job.css_first('span.job-area')
```

---

## ⚖️ Legal Compliance Boundaries — 法律合规红线

**This is NOT optional. Violating these can result in criminal prosecution.**

### 🟢 Generally Safe (Legal)

- Scraping **publicly accessible** data without login
- Collecting data for **personal research** (non-commercial)
- Scraping with **explicit API access** (platform-approved)
- Academic research with **anonymized data**
- Price monitoring of **publicly listed prices**

### 🟡 Gray Area (Proceed with Caution)

- Scraping data behind **login walls** (may violate ToS)
- Collecting **user-generated content** at scale (copyright risk)
- **Rate limiting bypass** (may be considered "unauthorized access")
- Scraping for **commercial competitive intelligence**
- Using scraped data for **AI training** (copyright unclear)

### 🔴 Illegal (Criminal Liability)

- Scraping **personal private data** (Criminal Law Article 253: 侵犯公民个人信息罪)
  - Penalties: Up to 7 years imprisonment + fine
  - Examples: ID numbers, phone numbers, home addresses, financial data
- **Bypassing computer system security measures** (Criminal Law Article 285: 非法侵入计算机信息系统罪)
  - Penalties: Up to 7 years imprisonment
  - Examples: Breaking encryption, forging authentication tokens
- **Disrupting computer systems** (Criminal Law Article 286: 破坏计算机信息系统罪)
  - Penalties: Up to 15 years imprisonment
  - Examples: DDoS-level scraping, crashing servers
- Scraping **state secrets** or **classified data**
- Scraping **financial data** without proper licensing
- **Reselling scraped personal data** (PIPL violations)

### Key Legal References

| Law | Scope | Max Penalty |
|-----|-------|-------------|
| Criminal Law Art. 253 | Personal information | 7 years + fine |
| Criminal Law Art. 285 | Unauthorized system access | 7 years |
| Criminal Law Art. 286 | System disruption | 15 years |
| Data Security Law | Data classification | ¥10M fine |
| PIPL (个人信息保护法) | Personal information | ¥50M or 5% revenue |
| Cybersecurity Law | Network data | ¥1M fine |
| Anti-Unfair Competition Law | Business data scraping | ¥3M fine |

### Real Cases (China)

1. **2023: 某数据公司爬取1.2亿条个人信息** — Criminal Law 253, CEO sentenced to 4 years
2. **2022: 爬取大众点评数据案** — Anti-Unfair Competition Law, ¥500K fine + injunction
3. **2021: 爬取微博数据案** — Court ruled scraping behind login = unauthorized access
4. **2020: 脉脉爬取LinkedIn数据** — Anti-Unfair Competition Law, ¥2M fine

---

## 🛠️ Scrapling Quick Start for Chinese Sites

### Installation

```bash
# Install Scrapling with all features
pip install scrapling[all]

# Or minimal install
pip install scrapling
```

### Basic Usage Pattern

```python
from scrapling import StealthyFetcher, Fetcher

# 1. Simple HTTP fetch (fast, no JS rendering)
page = Fetcher.get('https://example.com')

# 2. Stealthy browser fetch (bypasses anti-bot)
page = StealthyFetcher.fetch(
    'https://www.baidu.com/s?wd=test',
    headless=True,
    network_idle=True,
)

# 3. Adaptive selectors — survive site redesigns
element = page.find_by_text('价格')  # Find by text content
element = page.css_first('[class*="price"]')  # Partial class match
```

### Adaptive Selector Strategies for Chinese Sites

Chinese websites redesign frequently. Use these strategies to make your selectors resilient:

```python
# ❌ BAD: Exact class names (break on redesign)
title = page.css_first('span.title_3wVZ1')

# ✅ GOOD: Structural selectors
title = page.css_first('h2 a')  # Semantic HTML

# ✅ GOOD: Partial class match
title = page.css_first('[class*="title"]')

# ✅ GOOD: Text-based selection
title = page.find_by_text('价格')

# ✅ GOOD: Attribute-based
title = page.css_first('[data-type="title"]')

# ✅ BEST: Scrapling's adaptive selector
# Scrapling remembers element characteristics and re-finds after changes
element = page.css_first('div.product-title')
# If class changes, Scrapling's smart locator adapts automatically
```

### Rate Limiting Best Practices

```python
import time
import random

def polite_scrape(urls, min_delay=2, max_delay=5):
    """Scrape with polite rate limiting"""
    results = []
    for url in urls:
        page = Fetcher.get(url)
        results.append(page)
        # Random delay to appear human
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    return results

# Platform-specific rate limits
RATE_LIMITS = {
    'baidu': {'min': 3, 'max': 8, 'max_per_hour': 80},
    'taobao': {'min': 5, 'max': 12, 'max_per_hour': 30},
    'douyin': {'min': 5, 'max': 15, 'max_per_hour': 20},
    'zhihu': {'min': 3, 'max': 8, 'max_per_hour': 40},
    'wechat': {'min': 2, 'max': 5, 'max_per_hour': 60},
    '1688': {'min': 5, 'max': 10, 'max_per_hour': 30},
    'xiaohongshu': {'min': 8, 'max': 20, 'max_per_hour': 10},
    'weibo': {'min': 3, 'max': 8, 'max_per_hour': 40},
}
```

---

## 📊 Data Extraction Templates

### E-commerce Product Data

```python
def extract_product(page, platform='generic'):
    """Universal product data extractor"""
    templates = {
        'taobao': {
            'title': 'span.Title--titleSpan',
            'price': 'span.Price--priceInt',
            'sales': 'span.Sales--sales',
            'shop': 'a.ShopName--shopName',
        },
        '1688': {
            'title': 'a.title',
            'price': 'span.price',
            'min_order': 'span.min-order',
            'supplier': 'a.company-name',
        },
        'jd': {
            'title': 'div.sku-name',
            'price': 'span.price',
            'comments': 'a.comment-count',
        },
    }
    
    selector = templates.get(platform, templates['taobao'])
    return {
        field: page.css_first(sel).text() if page.css_first(sel) else None
        for field, sel in selector.items()
    }
```

### Social Media Content

```python
def extract_social_post(page, platform='generic'):
    """Universal social media post extractor"""
    templates = {
        'weibo': {
            'author': 'a.name',
            'content': 'p.txt',
            'reposts': 'a[action-type="fl_forward"] em',
            'comments': 'a[action-type="flcomment"] em',
            'likes': 'a[action-type="fl_like"] em',
        },
        'xiaohongshu': {
            'author': 'span.name',
            'content': 'span.note-text',
            'likes': 'span.like-wrapper .count',
            'collects': 'span.collect-wrapper .count',
        },
        'douyin': {
            'author': 'span.author-card-user-name',
            'content': 'p.title',
            'likes': 'span.video-like-count',
        },
    }
    
    selector = templates.get(platform, templates['weibo'])
    return {
        field: page.css_first(sel).text() if page.css_first(sel) else None
        for field, sel in selector.items()
    }
```

---

## 🔧 Executable Scripts

### `scripts/scrape.sh` — Quick CLI Scraper

```bash
#!/bin/bash
# cn-data-scraper CLI tool
# Usage: ./scripts/scrape.sh <platform> <keyword> [options]

PLATFORM=$1
KEYWORD=$2
OUTPUT=${3:-/tmp/scrape_result.json}

if [ -z "$PLATFORM" ] || [ -z "$KEYWORD" ]; then
    echo "Usage: ./scripts/scrape.sh <platform> <keyword> [output_file]"
    echo "Platforms: baidu taobao douyin zhihu wechat 1688 xiaohongshu weibo csdn boss"
    exit 1
fi

python3 -c "
from scrapling import StealthyFetcher, Fetcher
import json

platform = '$PLATFORM'
keyword = '$KEYWORD'
output = '$OUTPUT'

URLS = {
    'baidu': f'https://www.baidu.com/s?wd={keyword}',
    'zhihu': f'https://www.zhihu.com/search?type=content&q={keyword}',
    'weibo': f'https://s.weibo.com/weibo?q={keyword}',
    'csdn': f'https://so.csdn.net/so/search?q={keyword}',
}

url = URLS.get(platform)
if not url:
    print(json.dumps({'error': f'Platform {platform} not supported for CLI scraping. Use Python API for full features.'}))
    exit(0)

try:
    if platform in ['baidu', 'zhihu', 'weibo']:
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True, timeout=30000)
    else:
        page = Fetcher.get(url)
    
    # Extract all text content
    texts = [el.text() for el in page.css('p, span, h1, h2, h3, h4, h5, h6') if el.text()]
    
    result = {
        'platform': platform,
        'keyword': keyword,
        'url': url,
        'content_count': len(texts),
        'preview': texts[:20],
    }
    
    with open(output, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print(json.dumps({'error': str(e)}))
"
```

---

## 🔗 MCP Server Integration

For AI agent workflows, this skill can be used with MCP servers:

```python
# Example: MCP tool for scraping Chinese websites
from mcp.server import Server

server = Server("cn-data-scraper")

@server.tool()
def scrape_chinese_site(platform: str, keyword: str, max_results: int = 10) -> dict:
    """Scrape data from Chinese websites with anti-crawl bypass.
    
    Args:
        platform: Target platform (baidu/taobao/douyin/zhihu/wechat/1688/xiaohongshu/weibo)
        keyword: Search keyword
        max_results: Maximum number of results to return
    
    Returns:
        Dictionary with scraped data and metadata
    """
    # Implementation using Scrapling + platform recipes
    pass

@server.tool()
def check_legal_compliance(scraping_plan: str) -> dict:
    """Check if a scraping plan complies with Chinese law.
    
    Args:
        scraping_plan: Description of what data you plan to scrape
    
    Returns:
        Compliance assessment with risk level and legal references
    """
    pass
```

---

## 📈 Scrapling vs Other Frameworks (China Context)

| Feature | Scrapling | BeautifulSoup | Selenium | Playwright |
|---------|-----------|---------------|----------|------------|
| **Speed** | 784x BS4 | Baseline | Slow | Medium |
| **Anti-crawl bypass** | ✅ Built-in | ❌ | ⚠️ Manual | ⚠️ Manual |
| **Adaptive selectors** | ✅ Auto | ❌ | ❌ | ❌ |
| **Cloudflare bypass** | ✅ Native | ❌ | ⚠️ Plugin | ⚠️ Plugin |
| **Chinese site configs** | ❌ (We add this) | ❌ | ❌ | ❌ |
| **Legal compliance** | ❌ (We add this) | ❌ | ❌ | ❌ |
| **Memory usage** | Low | Very Low | High | Medium |
| **Setup complexity** | pip install | pip install | Driver needed | pip install |

**Our value-add:** Scrapling handles the technical scraping. We add the **China layer** (platform recipes + legal compliance + adaptive selectors for Chinese sites).

---

## 🚨 Common Pitfalls for Chinese Website Scraping

1. **Don't use English-language scraping tutorials for Chinese sites** — anti-crawl mechanisms are completely different
2. **Don't ignore rate limits** — Chinese platforms are MORE aggressive than Western ones (小红书 10/min vs Twitter 900/15min)
3. **Don't scrape personal data** — China's PIPL is stricter than GDPR in some aspects (criminal liability, not just fines)
4. **Don't assume HTTPS = safe** — Chinese ISPs can see your traffic; use proxy for sensitive scraping
5. **Don't hardcode selectors** — Chinese sites redesign every 2-4 weeks; use adaptive selectors
6. **Don't scrape during peak hours** — 8:00-10:00 AM and 7:00-9:00 PM have the most aggressive monitoring
7. **Don't ignore robots.txt** — While not legally binding in China, ignoring it increases legal risk
8. **Don't store raw personal data** — Anonymize immediately; PIPL requires "最小必要原则" (minimum necessary)

---

## 📚 Resources

- **Scrapling GitHub**: https://github.com/D4Vinci/Scrapling (31K+ Stars)
- **Scrapling 中文文档**: https://github.com/D4Vinci/Scrapling/blob/main/docs/README_CN.md
- **Camoufox (反指纹引擎)**: https://github.com/nicegamer7/camoufox
- **中国爬虫法律案例**: https://www.chinacourt.org (搜索"非法获取计算机信息系统数据")

---

## Important Notes

- **This skill teaches scraping techniques for legitimate data collection only**
- **Always check robots.txt before scraping any website**
- **Always comply with China's Criminal Law, Data Security Law, and PIPL**
- **When in doubt, use official APIs instead of scraping**
- **Scraping personal data without consent is a CRIMINAL OFFENSE in China**
- **Free tier**: This skill is free. Platform-specific advanced recipes may require API access.
