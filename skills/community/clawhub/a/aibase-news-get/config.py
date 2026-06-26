"""
新闻爬虫配置文件
"""

import os
from pathlib import Path

# ========== 基础配置 ==========

# 每次爬取最大数量
MAX_NEWS_PER_CRAWL = 20

# JSON文件名（固定文件名，避免每次创建新文件）
NEWS_JSON_FILENAME = "news_latest.json"

# ========== 网站配置 ==========
# key: 网站标识符
# value: 爬虫类名（scrapers目录下）
SITES = {
    "aibase": "AIBaseScraper",
}

# ========== 请求配置 ==========
REQUEST_TIMEOUT = 30
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
