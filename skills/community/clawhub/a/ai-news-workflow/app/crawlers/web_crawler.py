from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

from app.models.news_item import NewsItem
from app.models.source import Source
from app.parsers.html_extractors import extract_article_by_selectors
from app.utils.hash_utils import build_content_hash


SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


class WebCrawler:
    """
    网页爬虫：
    - 列表页抓链接
    - 详情页抽取标题/时间/正文
    """

    def __init__(
        self,
        request_timeout: int = 20,
        lookback_days: int = 3,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    ) -> None:
        self.request_timeout = request_timeout
        self.lookback_days = lookback_days
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def fetch(self, source: Source) -> List[NewsItem]:
        now_dt = datetime.now(SHANGHAI_TZ)
        threshold = now_dt - timedelta(days=self.lookback_days)

        list_url = getattr(source, "list_url", None) or source.url
        link_selector = getattr(source, "link_selector", None)
        url_prefix = getattr(source, "url_prefix", None) or list_url
        max_items = int(getattr(source, "max_items_per_run", None) or 30)

        title_selector = getattr(source, "title_selector", None)
        date_selector = getattr(source, "date_selector", None)
        content_selector = getattr(source, "content_selector", None)

        html = self._get_text(list_url)
        if not html:
            return []

        links = self._extract_links(html, link_selector=link_selector, base_url=url_prefix)
        links = links[:max_items]

        items: List[NewsItem] = []
        for link in links:
            detail_html = self._get_text(link)
            if not detail_html:
                continue

            article = extract_article_by_selectors(
                detail_html,
                title_selector=title_selector,
                date_selector=date_selector,
                content_selector=content_selector,
            )

            # 近 N 天过滤（发布时间缺失则先保留，后面由统计窗口再筛）
            if article.publish_time and article.publish_time < threshold:
                continue

            content_text = article.content_text

            item = NewsItem(
                title=article.title,
                summary="",  # 后续由豆包生成更好的摘要
                source_name=source.source_name,
                source_url=link,
                source_type=source.source_type,
                source_region_scope=getattr(source, "region_scope", None),
                is_official=(source.source_type in {"official", "government"}),
                publish_time=article.publish_time,
                crawl_time=now_dt,
                raw_content=content_text,
                cleaned_content=content_text,
                content_hash=build_content_hash(
                    title=article.title,
                    summary="",
                    content=content_text,
                ),
                normalized_title=(article.title or "").strip().lower(),
                entry_status="pending",
                dedup_status="unique",
            )

            # 把“详细正文”保存在 original_cleaned_content（供豆包总结用）
            item.original_cleaned_content = content_text
            item.original_title = article.title

            items.append(item)

        return items

    def _get_text(self, url: str) -> str:
        r = self.session.get(url, timeout=self.request_timeout)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or "utf-8"
        return r.text

    @staticmethod
    def _extract_links(html: str, link_selector: Optional[str], base_url: str) -> List[str]:
        soup = BeautifulSoup(html, "lxml")

        anchors = []
        if link_selector:
            anchors = soup.select(link_selector)
        else:
            anchors = soup.select("a")

        urls = []
        for a in anchors:
            href = a.get("href")
            if not href:
                continue
            full = urljoin(base_url, href)
            if full.startswith("http"):
                urls.append(full)

        # 去重保持顺序
        seen = set()
        uniq = []
        for u in urls:
            if u not in seen:
                uniq.append(u)
                seen.add(u)
        return uniq