from __future__ import annotations

from datetime import datetime, timedelta

from adapters.article_share import (
    build_share_url,
    extract_article_content,
    extract_article_title,
    fetch_article_html,
)
from adapters.telegraph_nodeapi import fetch_telegraph_list
from adapters.telegraph_page_fallback import fetch_telegraph_page_data
from models.schemas import (
    ClsItem,
    ClsQueryResult,
    SHANGHAI_TZ,
    is_red_level,
    normalize_published_at,
)


class ClsService:
    """Unified service layer for CLS telegraph data."""

    def get_telegraph(
        self,
        hours: int | None = None,
        limit: int | None = None,
    ) -> ClsQueryResult:
        items, source_used, fallback_used = self._load_telegraph_items()
        items = self._apply_time_filter(items, hours)
        if limit:
            items = items[:limit]
        return self._build_result("telegraph", items, source_used, fallback_used)

    def get_red(
        self,
        hours: int | None = None,
        limit: int | None = None,
    ) -> ClsQueryResult:
        items, source_used, fallback_used = self._load_telegraph_items()
        items = [item for item in items if item.is_red]
        items = self._apply_time_filter(items, hours)
        if limit:
            items = items[:limit]
        return self._build_result("red", items, source_used, fallback_used)

    def get_hot(
        self,
        hours: int | None = None,
        min_reading: int = 10000,
        limit: int | None = None,
    ) -> ClsQueryResult:
        items, source_used, fallback_used = self._load_telegraph_items()
        items = [item for item in items if item.reading_num >= min_reading]
        items = self._apply_time_filter(items, hours)
        items = sorted(items, key=lambda item: item.reading_num, reverse=True)
        if limit:
            items = items[:limit]
        return self._build_result("hot", items, source_used, fallback_used)

    def get_article(self, article_id: int) -> ClsQueryResult:
        html = fetch_article_html(article_id)
        title = extract_article_title(html)
        content = extract_article_content(html)
        brief = content[:200] if content else ""
        item = ClsItem(
            id=article_id,
            title=title,
            brief=brief,
            content=content,
            level="",
            is_red=False,
            reading_num=0,
            ctime=None,
            published_at="",
            shareurl=build_share_url(article_id),
            stock_list=[],
            subjects=[],
            plate_list=[],
            raw_source="article_share",
        )
        return self._build_result("article", [item], "article_share", False)

    def _load_telegraph_items(self) -> tuple[list[ClsItem], str, bool]:
        try:
            raw_items = fetch_telegraph_list()
            return self._normalize_items(raw_items, "nodeapi"), "nodeapi", False
        except Exception:
            raw_items = fetch_telegraph_page_data()
            return self._normalize_items(raw_items, "page_fallback"), "page_fallback", True

    def _normalize_items(self, raw_items: list[dict], raw_source: str) -> list[ClsItem]:
        normalized = []
        for raw in raw_items:
            level = raw.get("level", "")
            ctime = raw.get("ctime")
            normalized.append(
                ClsItem(
                    id=raw.get("id"),
                    title=raw.get("title", "") or "",
                    brief=raw.get("brief", "") or "",
                    content=raw.get("content", "") or "",
                    level=level,
                    is_red=is_red_level(level),
                    reading_num=raw.get("reading_num", 0) or 0,
                    ctime=ctime,
                    published_at=normalize_published_at(ctime),
                    shareurl=raw.get("shareurl", "") or "",
                    stock_list=raw.get("stock_list") or [],
                    subjects=raw.get("subjects") or [],
                    plate_list=raw.get("plate_list") or [],
                    raw_source=raw_source,
                )
            )
        return normalized

    def _apply_time_filter(self, items: list[ClsItem], hours: int | None) -> list[ClsItem]:
        if hours is None:
            return items
        cutoff = datetime.now(SHANGHAI_TZ) - timedelta(hours=hours)
        cutoff_ts = int(cutoff.timestamp())
        return [item for item in items if item.ctime and item.ctime >= cutoff_ts]

    def _build_result(
        self,
        query_type: str,
        items: list[ClsItem],
        source_used: str,
        fallback_used: bool,
    ) -> ClsQueryResult:
        return ClsQueryResult(
            query_type=query_type,
            count=len(items),
            items=items,
            source_used=source_used,
            fallback_used=fallback_used,
            generated_at=datetime.now(SHANGHAI_TZ).isoformat(),
        )
