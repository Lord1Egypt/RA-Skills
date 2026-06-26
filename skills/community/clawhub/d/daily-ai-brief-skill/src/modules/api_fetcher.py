"""
API抓取器
通过API接口抓取数据
"""
import asyncio
import logging
import time
from typing import List, Dict, Any
from datetime import datetime
import aiohttp
import json

from .base_fetcher import BaseFetcher, NewsItem


class APIFetcher(BaseFetcher):
    """API抓取器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.type = config.get("type", "")
        self.endpoint = config.get("endpoint", "")
        self.params = config.get("params", {})
        self.headers = config.get("headers", {})
        self.method = config.get("method", "GET")
        self.logger = logging.getLogger(f"APIFetcher.{self.name}")

    async def fetch(self) -> List[NewsItem]:
        """
        通过API抓取数据

        Returns:
            新闻条目列表
        """
        if not self.enabled:
            self.logger.info(f"数据源已禁用: {self.name}")
            return []

        if not self.endpoint:
            self.logger.error(f"API端点为空: {self.name}")
            return []

        self.logger.info(f"开始调用API: {self.name} ({self.endpoint})")
        start_time = time.time()

        try:
            # 根据API类型选择不同的解析方法
            if self.type == "hackernews":
                items = await self._fetch_hackernews()
            else:
                items = await self._fetch_generic_api()

            # 应用过滤
            filtered_items = self.apply_filters(items)

            elapsed = time.time() - start_time
            self.logger.info(f"API抓取完成: {self.name}, 获取 {len(filtered_items)} 个条目, 耗时 {elapsed:.2f}秒")
            return filtered_items

        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"API调用失败 {self.name}, 耗时 {elapsed:.2f}秒: {e}")
            return []

    async def _fetch_generic_api(self) -> List[NewsItem]:
        """
        调用通用API

        Returns:
            新闻条目列表
        """
        try:
            # 获取fetch配置
            from .config import get_config_loader
            config_loader = get_config_loader()
            fetch_config = config_loader.get_fetch_config()

            timeout = aiohttp.ClientTimeout(total=fetch_config.get("timeout_seconds", 30))

            async with aiohttp.ClientSession(timeout=timeout) as session:
                if self.method.upper() == "GET":
                    async with session.get(
                        self.endpoint,
                        params=self.params,
                        headers=self.headers
                    ) as response:
                        response.raise_for_status()
                        data = await response.json()
                elif self.method.upper() == "POST":
                    async with session.post(
                        self.endpoint,
                        json=self.params,
                        headers=self.headers
                    ) as response:
                        response.raise_for_status()
                        data = await response.json()
                else:
                    self.logger.error(f"不支持的HTTP方法: {self.method}")
                    return []

            # 解析API响应
            items = self._parse_api_response(data)
            return items

        except aiohttp.ClientError as e:
            self.logger.error(f"HTTP请求失败: {e}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {e}")
            return []
        except Exception as e:
            self.logger.error(f"API调用异常: {e}")
            return []

    async def _fetch_hackernews(self) -> List[NewsItem]:
        """
        抓取Hacker News数据

        Returns:
            新闻条目列表
        """
        try:
            # Hacker News API: 先获取热门故事ID
            top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            async with aiohttp.ClientSession() as session:
                async with session.get(top_stories_url) as response:
                    story_ids = await response.json()

                # 获取前N个故事的详细信息
                items = []
                for story_id in story_ids[:self.max_items]:
                    try:
                        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                        async with session.get(story_url) as story_response:
                            story_data = await story_response.json()

                        # 解析故事数据
                        item = self._parse_hackernews_item(story_data)
                        if item and self.validate_item(item):
                            items.append(item)
                    except Exception as e:
                        self.logger.debug(f"获取Hacker News故事 {story_id} 失败: {e}")

                return items

        except Exception as e:
            self.logger.error(f"Hacker News抓取失败: {e}")
            return []

    def _parse_hackernews_item(self, story_data: Dict[str, Any]) -> NewsItem:
        """
        解析Hacker News故事数据

        Args:
            story_data: 故事数据

        Returns:
            新闻条目
        """
        title = story_data.get("title", "")
        title = self.cleanup_content(title)
        url = story_data.get("url", "")

        # 如果没有外部URL，使用HN讨论页
        if not url:
            story_id = story_data.get("id")
            url = f"https://news.ycombinator.com/item?id={story_id}"

        # 提取内容
        text = story_data.get("text", "")
        if text:
            # 清理HTML标签
            text = self.cleanup_content(text)

        # 提取发布时间
        publish_date = None
        time_val = story_data.get("time")
        if time_val:
            publish_date = datetime.fromtimestamp(time_val)

        # 作者和分数
        author = story_data.get("by", "")
        score = story_data.get("score", 0)

        # 创建新闻条目
        item = NewsItem(
            title=title,
            url=url,
            content=text,
            summary=self.cleanup_content(text[:200] if text else title),
            source=self.name,
            source_type="hackernews",
            publish_date=publish_date,
            author=author,
            tags=["hackernews"],
            metadata={
                "type": story_data.get("type", "story"),
                "score": score,
                "descendants": story_data.get("descendants", 0),
                "hn_id": story_data.get("id"),
            }
        )

        return item

    def _parse_api_response(self, data: Any) -> List[NewsItem]:
        """
        解析通用API响应

        Args:
            data: API响应数据

        Returns:
            新闻条目列表
        """
        items = []

        # 尝试根据常见结构解析数据
        if isinstance(data, dict):
            # 如果是字典，尝试提取文章列表
            articles = data.get("articles", data.get("items", data.get("results", [])))
            if isinstance(articles, list):
                for article in articles[:self.max_items]:
                    try:
                        item = self._parse_article_dict(article)
                        if item:
                            items.append(item)
                    except Exception as e:
                        self.logger.debug(f"解析文章失败: {e}")
        elif isinstance(data, list):
            # 如果是列表，直接处理
            for item_data in data[:self.max_items]:
                try:
                    if isinstance(item_data, dict):
                        item = self._parse_article_dict(item_data)
                    else:
                        # 简单处理非字典项
                        item = NewsItem(
                            title=str(item_data)[:100],
                            url=self.endpoint,
                            content=str(item_data),
                            source=self.name,
                            source_type="api",
                            metadata={"raw_data": str(item_data)[:500]}
                        )
                    if item:
                        items.append(item)
                except Exception as e:
                    self.logger.debug(f"解析列表项失败: {e}")

        return items

    def _parse_article_dict(self, article: Dict[str, Any]) -> NewsItem:
        """
        解析文章字典

        Args:
            article: 文章数据字典

        Returns:
            新闻条目
        """
        # 尝试从常见字段中提取信息
        title = article.get("title", article.get("name", article.get("headline", "")))
        title = self.cleanup_content(title)

        url = article.get("url", article.get("link", article.get("webUrl", "")))
        content = article.get("content", article.get("body", article.get("description", article.get("summary", ""))))
        summary = article.get("summary", article.get("description", content[:200] if content else ""))

        # 清理内容
        content = self.cleanup_content(content)
        summary = self.cleanup_content(summary)

        # 提取发布时间
        publish_date = None
        date_fields = ["publishedAt", "pubDate", "date", "createdAt", "timestamp"]
        for field in date_fields:
            if field in article:
                date_str = article[field]
                if date_str:
                    # 尝试解析日期字符串
                    try:
                        # 简化处理，实际应使用dateparser
                        if isinstance(date_str, (int, float)):
                            publish_date = datetime.fromtimestamp(date_str)
                        elif "T" in date_str:
                            publish_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        break
                    except Exception:
                        continue

        # 提取作者
        author = ""
        author_field = article.get("author", article.get("byline", article.get("creator", "")))
        if isinstance(author_field, str):
            author = author_field
        elif isinstance(author_field, list):
            author = ", ".join(author_field)
        elif isinstance(author_field, dict):
            author = author_field.get("name", "")

        # 提取标签
        tags = []
        tags_field = article.get("tags", article.get("keywords", article.get("categories", [])))
        if isinstance(tags_field, list):
            tags = [str(tag) for tag in tags_field]
        elif isinstance(tags_field, str):
            tags = [tag.strip() for tag in tags_field.split(",")]

        item = NewsItem(
            title=title,
            url=url,
            content=content,
            summary=summary,
            source=self.name,
            source_type="api",
            publish_date=publish_date,
            author=author,
            tags=tags,
            metadata={
                "api_endpoint": self.endpoint,
                "api_type": self.type,
            }
        )

        return item