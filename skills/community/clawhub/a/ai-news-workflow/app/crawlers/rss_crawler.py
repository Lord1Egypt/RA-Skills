from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional
from zoneinfo import ZoneInfo

import feedparser

from app.models.news_item import NewsItem
from app.models.source import Source
from app.parsers.content_cleaner import ContentCleaner
from app.utils.hash_utils import build_content_hash


SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


class RSSCrawler:
    """
    RSS 抓取器。
    支持：
    - 抓取 RSS
    - 只保留近 N 天内的资讯
    """

    def __init__(
        self,
        request_timeout: int = 20,
        lookback_days: int = 3,
    ) -> None:
        self.request_timeout = request_timeout
        self.lookback_days = lookback_days
        self.cleaner = ContentCleaner()

    def fetch(self, source: Source) -> List[NewsItem]:
        feed = feedparser.parse(source.url)

        items: List[NewsItem] = []
        now_dt = datetime.now(SHANGHAI_TZ)

        for entry in feed.entries:
            title = (getattr(entry, "title", "") or "").strip()
            link = (getattr(entry, "link", "") or "").strip()

            raw_summary = (
                getattr(entry, "summary", "")
                or getattr(entry, "description", "")
                or ""
            )
            raw_summary = str(raw_summary).strip()

            publish_time = self._extract_publish_time(entry)

            # 只保留近 N 天内的资讯
            if not self._is_within_lookback(publish_time, now_dt):
                continue

            summary = self.cleaner.clean_summary(raw_summary, max_length=300)
            cleaned_content = self.cleaner.clean_text(raw_summary)

            item = NewsItem(
                title=title if title else "Untitled",
                summary=summary,
                source_name=source.source_name,
                source_url=link if link else source.url,
                source_type=source.source_type,
                source_region_scope=getattr(source, "region_scope", None),
                is_official=(source.source_type in {"official", "government"}),
                publish_time=publish_time,
                crawl_time=now_dt,
                raw_content=raw_summary,
                cleaned_content=cleaned_content,
                content_hash=build_content_hash(
                    title=title,
                    summary=summary,
                    content=cleaned_content,
                ),
                normalized_title=(title or "").strip().lower(),
                language=None,
                entry_status="pending",
                dedup_status="unique",
            )
            items.append(item)

        return items

    def _extract_publish_time(self, entry) -> Optional[datetime]:
        """
        从 RSS entry 中提取发布时间，优先 published_parsed / updated_parsed。
        """
        time_struct = None

        if hasattr(entry, "published_parsed") and entry.published_parsed:
            time_struct = entry.published_parsed
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            time_struct = entry.updated_parsed

        if not time_struct:
            return None

        try:
            dt = datetime(
                year=time_struct.tm_year,
                month=time_struct.tm_mon,
                day=time_struct.tm_mday,
                hour=time_struct.tm_hour,
                minute=time_struct.tm_min,
                second=time_struct.tm_sec,
                tzinfo=ZoneInfo("UTC"),
            )
            return dt.astimezone(SHANGHAI_TZ)
        except Exception:
            return None

    def _is_within_lookback(
        self,
        publish_time: Optional[datetime],
        now_dt: datetime,
    ) -> bool:
        """
        判断是否在近 N 天内。
        - publish_time 为空时，默认保留，避免误漏抓
        """
        if publish_time is None:
            return True

        threshold = now_dt - timedelta(days=self.lookback_days)
        return publish_time >= threshold