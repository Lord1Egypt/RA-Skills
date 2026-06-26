"""
抓取器工厂
根据配置创建相应的抓取器实例
"""
import logging
from typing import Dict, Any, List, Type, Optional

from .base_fetcher import BaseFetcher
from .rss_fetcher import RSSFetcher
from .x_fetcher import XFetcher
from .web_scraper import WebScraper
from .api_fetcher import APIFetcher


class FetcherFactory:
    """抓取器工厂类"""

    # 抓取器类型映射
    FETCHER_REGISTRY: Dict[str, Type[BaseFetcher]] = {
        "rss": RSSFetcher,
        "twitter": XFetcher,
        "x": XFetcher,
        "web": WebScraper,
        "scraper": WebScraper,
        "api": APIFetcher,
        "hackernews": APIFetcher,
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_fetchers_from_config(self, config: Dict[str, Any]) -> List[BaseFetcher]:
        """
        根据配置创建所有抓取器实例

        Args:
            config: 完整配置字典

        Returns:
            抓取器实例列表
        """
        fetchers = []

        # RSS抓取器
        rss_sources = config.get("rss_sources", [])
        for source_config in rss_sources:
            fetcher = self.create_fetcher("rss", source_config)
            if fetcher:
                fetchers.append(fetcher)

        # X/Twitter抓取器
        x_sources = config.get("x_sources", [])
        for source_config in x_sources:
            fetcher = self.create_fetcher("x", source_config)
            if fetcher:
                fetchers.append(fetcher)

        # 网页爬虫
        web_scrapers = config.get("web_scrapers", [])
        for source_config in web_scrapers:
            fetcher = self.create_fetcher("web", source_config)
            if fetcher:
                fetchers.append(fetcher)

        # API抓取器
        api_sources = config.get("api_sources", [])
        for source_config in api_sources:
            fetcher_type = source_config.get("type", "api")
            fetcher = self.create_fetcher(fetcher_type, source_config)
            if fetcher:
                fetchers.append(fetcher)

        self.logger.info(f"创建了 {len(fetchers)} 个抓取器实例")
        return fetchers

    def create_fetcher(self, fetcher_type: str, config: Dict[str, Any]) -> Optional[BaseFetcher]:
        """
        创建单个抓取器实例

        Args:
            fetcher_type: 抓取器类型
            config: 抓取器配置

        Returns:
            抓取器实例，如果创建失败则返回None
        """
        if not config.get("enabled", True):
            self.logger.debug(f"抓取器已禁用: {config.get('name', 'unknown')}")
            return None

        # 获取对应的抓取器类
        fetcher_class = self.FETCHER_REGISTRY.get(fetcher_type.lower())
        if not fetcher_class:
            self.logger.error(f"未知的抓取器类型: {fetcher_type}")
            return None

        try:
            fetcher = fetcher_class(config)
            self.logger.debug(f"创建抓取器: {fetcher.name} ({fetcher_type})")
            return fetcher
        except Exception as e:
            self.logger.error(f"创建抓取器失败 {config.get('name', 'unknown')}: {e}")
            return None



# 全局工厂实例
_factory: Optional[FetcherFactory] = None


def get_fetcher_factory() -> FetcherFactory:
    """获取全局抓取器工厂实例"""
    global _factory
    if _factory is None:
        _factory = FetcherFactory()
    return _factory