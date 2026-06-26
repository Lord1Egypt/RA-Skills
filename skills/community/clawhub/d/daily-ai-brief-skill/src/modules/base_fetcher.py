"""
抽象抓取器基类
定义所有抓取器必须实现的接口和通用功能
"""
import abc
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re


class NewsItem:
    """新闻条目数据类"""

    def __init__(
        self,
        title: str,
        url: str,
        summary: str = "",
        content: str = "",
        source: str = "",
        source_type: str = "",
        publish_date: Optional[datetime] = None,
        author: str = "",
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ):
        self.title = title
        self.url = url
        self.summary = summary
        self.content = content
        self.source = source
        self.source_type = source_type
        self.publish_date = publish_date or datetime.now()
        self.author = author
        self.tags = tags or []
        self.metadata = metadata or {}

        # 计算热度分数（初始为0，后续由热度评估模块计算）
        self.hotness_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "content": self.content[:500] + "..." if len(self.content) > 500 else self.content,
            "source": self.source,
            "source_type": self.source_type,
            "publish_date": self.publish_date.isoformat() if self.publish_date else None,
            "author": self.author,
            "tags": self.tags,
            "hotness_score": self.hotness_score,
            "metadata": self.metadata,
        }

    def __repr__(self):
        return f"NewsItem(title={self.title[:50]}..., source={self.source}, date={self.publish_date})"


class BaseFetcher(abc.ABC):
    """抓取器抽象基类"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化抓取器

        Args:
            config: 该数据源的配置信息
        """
        self.config = config
        self.name = config.get("name", "unknown")
        self.enabled = config.get("enabled", True)
        self.priority = config.get("priority", 3)
        self.max_items = config.get("num_items", 10)
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.name}")

        # 过滤配置
        self.filters = config.get("filters", {})
        self.include_keywords = self.filters.get("include_keywords", [])
        self.exclude_keywords = self.filters.get("exclude_keywords", [])

    @abc.abstractmethod
    async def fetch(self) -> List[NewsItem]:
        """
        抓取数据 - 子类必须实现

        Returns:
            新闻条目列表
        """
        pass

    def apply_filters(self, items: List[NewsItem]) -> List[NewsItem]:
        """
        应用关键词过滤

        Args:
            items: 原始新闻条目列表

        Returns:
            过滤后的新闻条目列表
        """
        if not items:
            return []

        filtered_items = []
        for item in items:
            # 检查是否包含关键词
            text_to_check = f"{item.title} {item.summary} {item.content}".lower()

            # 排除关键词检查
            if self.exclude_keywords:
                # 检查是否包含任意排除关键词（使用改进的边界，允许中文后跟）
                excluded = False
                for keyword in self.exclude_keywords:
                    # 使用正则表达式匹配，前后不能是英文字母
                    import re
                    pattern = r'(?<![a-zA-Z])' + re.escape(keyword.lower()) + r'(?![a-zA-Z])'
                    if re.search(pattern, text_to_check):
                        self.logger.debug(f"排除条目（含排除关键词）: {item.title[:50]}")
                        excluded = True
                        break
                if excluded:
                    continue

            # 包含关键词检查（如果有配置）
            if self.include_keywords:
                # 检查是否包含任意关键词（使用改进的边界，允许中文后跟）
                found = False
                for keyword in self.include_keywords:
                    # 使用正则表达式匹配，前后不能是英文字母
                    import re
                    pattern = r'(?<![a-zA-Z])' + re.escape(keyword.lower()) + r'(?![a-zA-Z])'
                    if re.search(pattern, text_to_check):
                        found = True
                        break
                if not found:
                    self.logger.debug(f"排除条目（不含包含关键词）: {item.title[:50]}")
                    continue

            filtered_items.append(item)

        # 限制数量
        if self.max_items and len(filtered_items) > self.max_items:
            filtered_items = filtered_items[:self.max_items]

        return filtered_items

    def filter_by_age(self, items: List[NewsItem], max_age_hours: int = 72) -> List[NewsItem]:
        """
        根据发布时间过滤条目

        Args:
            items: 新闻条目列表
            max_age_hours: 最大年龄（小时）

        Returns:
            过滤后的新闻条目列表
        """
        if not max_age_hours:
            return items

        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        filtered_items = [item for item in items if item.publish_date >= cutoff_time]

        removed_count = len(items) - len(filtered_items)
        if removed_count > 0:
            self.logger.debug(f"根据时间过滤掉 {removed_count} 个条目（发布时间早于 {cutoff_time}）")

        return filtered_items

    def validate_item(self, item: NewsItem) -> bool:
        """
        验证新闻条目的基本有效性

        Args:
            item: 新闻条目

        Returns:
            是否有效
        """
        if not item.title or not item.url:
            return False

        # 检查URL格式
        if not (item.url.startswith("http://") or item.url.startswith("https://")):
            return False

        # 检查标题长度
        if len(item.title.strip()) < 5:
            return False

        return True

    def cleanup_content(self, content: str) -> str:
        """
        清理内容文本，移除HTML标签和多余格式

        Args:
            content: 原始内容

        Returns:
            清理后的内容
        """
        if not content:
            return ""

        # 确保content是字符串
        if not isinstance(content, str):
            content = str(content)

        # 移除HTML标签（包括<script>、<style>等）
        # 先移除script和style标签及其内容
        content = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', content, flags=re.DOTALL | re.IGNORECASE)

        # 移除其他HTML标签，但保留文本内容
        content = re.sub(r'<[^>]+>', ' ', content)

        # 解码HTML实体
        try:
            import html
            content = html.unescape(content)
        except ImportError:
            # 如果html模块不可用，使用简单的替换
            content = re.sub(r'&nbsp;', ' ', content)
            content = re.sub(r'&amp;', '&', content)
            content = re.sub(r'&lt;', '<', content)
            content = re.sub(r'&gt;', '>', content)
            content = re.sub(r'&quot;', '"', content)
            content = re.sub(r'&#39;', "'", content)
            content = re.sub(r'&[a-z]+;', ' ', content)
        except Exception:
            # 如果html.unescape失败，也使用简单替换
            content = re.sub(r'&nbsp;', ' ', content)
            content = re.sub(r'&amp;', '&', content)
            content = re.sub(r'&lt;', '<', content)
            content = re.sub(r'&gt;', '>', content)
            content = re.sub(r'&quot;', '"', content)
            content = re.sub(r'&#39;', "'", content)
            content = re.sub(r'&[a-z]+;', ' ', content)

        # 移除多余空白字符（包括换行、制表符等）
        content = re.sub(r'\s+', ' ', content)

        # 清理多余的空格
        content = re.sub(r' +', ' ', content)

        return content.strip()