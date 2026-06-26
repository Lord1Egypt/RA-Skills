"""
agents/crawler_agent.py
────────────────────────
Hybrid web scraper:
  - Direct scraping (requests + BeautifulSoup) for news sites — fast & free
  - Apify for complex sites like Facebook (JS rendering needed)
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup
from apify_client import ApifyClient
from rich.console import Console

import config
from models import ScrapedContent
from utils import logger, validate_url, detect_source_type, clean_text, alert_inaccessible

console = Console()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

# Source types that require Apify (JS rendering)
APIFY_REQUIRED = {"facebook"}

# Apify actor IDs
NEWS_ACTOR_ID = "apify/website-content-crawler"
FB_POST_ACTOR_ID = "apify/facebook-posts-scraper"


class CrawlerAgent:
    def __init__(self):
        self.client = ApifyClient(config.APIFY_API_TOKEN)

    # ── Public API ──────────────────────────────────────────

    def crawl(self, url: str) -> ScrapedContent:
        """Auto-detect URL type and scrape with the best method."""
        is_valid, result = validate_url(url)
        if not is_valid:
            alert_inaccessible(url, result)
            return ScrapedContent(url=url, is_accessible=False, error_message=result)

        clean_url = result
        source_type = detect_source_type(clean_url)
        console.print(f"[cyan]🔍 Scraping [{source_type}]:[/cyan] {clean_url}")

        if source_type in APIFY_REQUIRED:
            return self._scrape_fb_post(clean_url, source_type)
        else:
            return self._scrape_direct(clean_url, source_type)

    def crawl_multiple(self, urls: list[str]) -> list[ScrapedContent]:
        """Scrape multiple URLs sequentially."""
        results = []
        for i, url in enumerate(urls, 1):
            logger.info(f"[{i}/{len(urls)}] Processing: {url}")
            result = self.crawl(url)
            results.append(result)
            console.print(result.summary())
            console.print()
        return results

    # ── Direct scraping (news sites) ───────────────────────

    def _scrape_direct(self, url: str, source_type: str) -> ScrapedContent:
        """Scrape using requests + BeautifulSoup (for news sites)."""
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"

            soup = BeautifulSoup(response.text, "lxml")

            title = self._extract_meta(soup, "og:title") or self._extract_tag(soup, "title")
            description = self._extract_meta(soup, "og:description") or self._extract_meta(soup, "description")
            author = self._extract_meta(soup, "article:author") or self._extract_meta(soup, "author")
            published = self._extract_meta(soup, "article:published_time") or self._extract_meta(soup, "pubdate")

            body_text = self._extract_article_text(soup)

            if not body_text:
                msg = "No article content found on page."
                alert_inaccessible(url, msg)
                return ScrapedContent(url=url, is_accessible=False, error_message=msg)

            console.print(f"[green]✅ Scraped:[/green] {title or url} | {len(body_text)} chars")
            return ScrapedContent(
                url=url,
                title=title,
                text=clean_text(body_text)[:4000],
                description=description,
                author=author,
                published_date=published,
                source_name=source_type,
                is_accessible=True,
            )

        except requests.RequestException as e:
            error_msg = f"HTTP request failed: {type(e).__name__}: {e}"
            logger.error(error_msg)
            alert_inaccessible(url, error_msg)
            return ScrapedContent(url=url, is_accessible=False, error_message=error_msg)

    # ── Facebook scraping (Apify) ──────────────────────────

    def _scrape_fb_post(self, url: str, source_type: str) -> ScrapedContent:
        """Scrape a Facebook post using Apify."""
        try:
            console.print("[yellow]Starting Apify actor run...[/yellow]")

            run = self.client.actor(FB_POST_ACTOR_ID).call(
                run_input={
                    "startUrls": [{"url": url}],
                    "maxPosts": 1,
                    "proxyConfiguration": {"useApifyProxy": True},
                }
            )

            items = list(
                self.client.dataset(run["defaultDatasetId"]).iterate_items()
            )
            if not items:
                msg = "Apify returned no results — post may be inaccessible."
                alert_inaccessible(url, msg)
                return ScrapedContent(url=url, is_accessible=False, error_message=msg)

            item = items[0]
            message = item.get("text") or item.get("message") or item.get("postText", "")
            author = item.get("authorName") or item.get("user", {}).get("name", "Unknown")

            console.print(f"[green]✅ FB post scraped:[/green] {author} | {len(message)} chars")
            return ScrapedContent(
                url=url,
                title=f"Post của {author}",
                text=clean_text(message)[:3000],
                author=author,
                source_name=source_type,
                is_accessible=True,
            )

        except Exception as e:
            error_msg = f"Scraping failed: {type(e).__name__}: {e}"
            logger.error(error_msg)
            alert_inaccessible(url, error_msg)
            return ScrapedContent(url=url, is_accessible=False, error_message=error_msg)

    # ── HTML extraction helpers ────────────────────────────

    @staticmethod
    def _extract_meta(soup: BeautifulSoup, name: str) -> str | None:
        tag = soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name})
        return tag.get("content", "").strip() if tag else None

    @staticmethod
    def _extract_tag(soup: BeautifulSoup, tag_name: str) -> str | None:
        tag = soup.find(tag_name)
        return tag.get_text(strip=True) if tag else None

    @staticmethod
    def _extract_article_text(soup: BeautifulSoup) -> str:
        """Extract article body text using common article selectors."""
        for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside", "iframe", "noscript"]):
            tag.decompose()

        selectors = [
            "article",
            '[class*="article-content"]',
            '[class*="detail-content"]',
            '[class*="post-content"]',
            '[class*="entry-content"]',
            '[class*="content-detail"]',
            '[class*="singular-body"]',
            '[class*="news-content"]',
            '[id*="article"]',
            "main",
            '[role="main"]',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator="\n", strip=True)
                if len(text) > 100:
                    return text

        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20)
        return text


# ── Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    agent = CrawlerAgent()
    test_url = "https://dantri.com.vn/suc-manh-so/cong-nghe-ai-tao-sinh-dang-thay-doi-nganh-truyen-thong-nhu-the-nao-20240101000000000.htm"
    result = agent.crawl(test_url)
    print(f"\n{result.summary()}")
