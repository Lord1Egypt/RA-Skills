"""
爬虫模块
"""

from scrapers.base import BaseScraper
from scrapers.aibase import AIBaseScraper

# 导出所有爬虫类
__all__ = ["BaseScraper", "AIBaseScraper"]


def get_scraper(site_id: str) -> BaseScraper:
    """根据网站标识符获取爬虫实例"""
    scrapers = {
        "aibase": AIBaseScraper,
    }
    scraper_class = scrapers.get(site_id)
    if not scraper_class:
        raise ValueError(f"未知的网站: {site_id}")
    return scraper_class()
