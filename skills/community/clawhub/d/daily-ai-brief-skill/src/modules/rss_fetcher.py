"""
RSS抓取器
使用feedparser库抓取RSS/Atom订阅
"""
import asyncio
import feedparser
import logging
import time
from typing import List, Dict, Any
from datetime import datetime
from urllib.parse import urlparse

from .base_fetcher import BaseFetcher, NewsItem


class RSSFetcher(BaseFetcher):
    """RSS抓取器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.url = config.get("url", "")
        self.logger = logging.getLogger(f"RSSFetcher.{self.name}")

    async def fetch(self) -> List[NewsItem]:
        """
        抓取RSS订阅内容

        Returns:
            新闻条目列表
        """
        if not self.enabled:
            self.logger.info(f"数据源已禁用: {self.name}")
            return []

        if not self.url:
            self.logger.error(f"RSS URL为空: {self.name}")
            return []

        self.logger.info(f"开始抓取RSS: {self.name} ({self.url})")
        start_time = time.time()

        try:
            # feedparser是同步库，使用线程池避免阻塞事件循环
            loop = asyncio.get_event_loop()
            feed = await loop.run_in_executor(None, self._parse_feed, self.url)

            if not feed.entries:
                self.logger.warning(f"RSS没有条目: {self.name}")
                return []

            items = []
            for entry in feed.entries:
                try:
                    item = self._parse_entry(entry)
                    if item and self.validate_item(item):
                        items.append(item)
                except Exception as e:
                    self.logger.error(f"解析RSS条目失败: {e}")

            # 应用过滤
            filtered_items = self.apply_filters(items)

            elapsed = time.time() - start_time
            self.logger.info(f"RSS抓取完成: {self.name}, 获取 {len(filtered_items)} 个条目, 耗时 {elapsed:.2f}秒")
            return filtered_items

        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"抓取RSS失败 {self.name}, 耗时 {elapsed:.2f}秒: {e}")
            return []

    def _parse_feed(self, url: str) -> feedparser.FeedParserDict:
        """解析RSS订阅"""
        return feedparser.parse(url)

    def _parse_entry(self, entry) -> NewsItem:
        """解析RSS条目"""
        # 提取标题
        title = getattr(entry, 'title', '无标题')
        title = self.cleanup_content(title)

        # 提取链接
        link = getattr(entry, 'link', '')
        if not link and hasattr(entry, 'links') and entry.links:
            link = entry.links[0].get('href', '')

        # 提取摘要
        summary = ""
        if hasattr(entry, 'summary'):
            summary = entry.summary
        elif hasattr(entry, 'description'):
            summary = entry.description

        # 提取内容
        content = ""
        if hasattr(entry, 'content'):
            if entry.content:
                content = entry.content[0].get('value', '')
        elif hasattr(entry, 'description'):
            content = entry.description

        # 清理内容
        summary = self.cleanup_content(summary)
        content = self.cleanup_content(content)

        # 提取发布时间
        publish_date = None
        date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                try:
                    time_tuple = getattr(entry, field)
                    publish_date = datetime(*time_tuple[:6])
                    break
                except Exception:
                    continue

        # 提取作者
        author = ""
        if hasattr(entry, 'author'):
            author = entry.author

        # 提取标签/分类
        tags = []
        if hasattr(entry, 'tags'):
            tags = [tag.term for tag in entry.tags if hasattr(tag, 'term')]
        elif hasattr(entry, 'categories'):
            tags = [cat.term for cat in entry.categories if hasattr(cat, 'term')]

        # 创建新闻条目
        item = NewsItem(
            title=title,
            url=link,
            summary=summary,
            content=content,
            source=self.name,
            source_type="rss",
            publish_date=publish_date,
            author=author,
            tags=tags,
            metadata={
                "rss_feed": self.url,
                "source_name": self.name,
            }
        )

        return item