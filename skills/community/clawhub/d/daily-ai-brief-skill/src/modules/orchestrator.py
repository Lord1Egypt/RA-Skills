"""
抓取协调器
管理多个抓取器的并发执行和结果聚合
"""
import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import time

from .base_fetcher import BaseFetcher, NewsItem
from .fetcher_factory import get_fetcher_factory
from .config import get_config_loader


class Orchestrator:
    """抓取协调器"""

    def __init__(self, max_concurrent: int = 10):
        """
        初始化协调器

        Args:
            max_concurrent: 最大并发抓取数
        """
        self.max_concurrent = max_concurrent
        self.logger = logging.getLogger(__name__)
        self.fetchers: List[BaseFetcher] = []
        self.results: List[NewsItem] = []
        self.failed_fetchers: List[Dict[str, Any]] = []  # 存储失败的抓取器信息

    def load_fetchers(self) -> List[BaseFetcher]:
        """
        加载所有抓取器

        Returns:
            抓取器列表
        """
        # 加载配置
        config_loader = get_config_loader()
        config = config_loader.load()

        # 创建抓取器
        factory = get_fetcher_factory()
        self.fetchers = factory.create_fetchers_from_config(config)

        # 按优先级排序（优先级数字越小优先级越高）
        self.fetchers.sort(key=lambda x: x.priority)

        self.logger.info(f"加载了 {len(self.fetchers)} 个抓取器")
        return self.fetchers

    async def fetch_all(self) -> List[NewsItem]:
        """
        并发执行所有抓取器

        Returns:
            所有抓取器的结果列表
        """
        if not self.fetchers:
            self.load_fetchers()

        self.logger.info(f"开始并发抓取，最大并发数: {self.max_concurrent}")

        # 创建信号量限制并发数
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def fetch_with_semaphore(fetcher: BaseFetcher):
            async with semaphore:
                return await self._fetch_single(fetcher)

        # 创建所有任务
        tasks = [fetch_with_semaphore(fetcher) for fetcher in self.fetchers]

        # 等待所有任务完成
        all_results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理结果
        self.results = []
        self.failed_fetchers = []
        for i, result in enumerate(all_results):
            fetcher = self.fetchers[i]
            if isinstance(result, Exception):
                self.logger.error(f"抓取器 {fetcher.name} 失败: {result}")
                self.failed_fetchers.append({
                    "name": fetcher.name,
                    "type": fetcher.__class__.__name__,
                    "error": str(result),
                    "config": fetcher.config
                })
            elif isinstance(result, list):
                self.results.extend(result)
            else:
                self.logger.warning(f"抓取器 {fetcher.name} 返回了意外结果类型: {type(result)}")
                self.failed_fetchers.append({
                    "name": fetcher.name,
                    "type": fetcher.__class__.__name__,
                    "error": f"意外结果类型: {type(result)}",
                    "config": fetcher.config
                })

        self.logger.info(f"所有抓取完成，共获取 {len(self.results)} 个条目")
        return self.results

    async def _fetch_single(self, fetcher: BaseFetcher) -> List[NewsItem]:
        """
        执行单个抓取器

        Args:
            fetcher: 抓取器实例

        Returns:
            抓取结果列表
        """
        start_time = time.time()
        try:
            items = await fetcher.fetch()
            return items
        except asyncio.CancelledError:
            raise
        except Exception as e:
            return []

    def filter_results(self, max_age_hours: int = 72) -> List[NewsItem]:
        """
        过滤结果

        Args:
            max_age_hours: 最大年龄（小时）

        Returns:
            过滤后的结果列表
        """
        if not self.results:
            return []

        # 首先过滤模拟数据
        real_results = []
        simulated_count = 0
        for item in self.results:
            # 检查是否为模拟数据
            if item.metadata.get("simulated", False):
                simulated_count += 1
                continue
            real_results.append(item)

        if simulated_count > 0:
            self.logger.info(f"过滤掉 {simulated_count} 个模拟数据条目")

        # 过滤重复条目（基于URL）
        seen_urls = set()
        unique_results = []
        for item in real_results:
            if item.url not in seen_urls:
                seen_urls.add(item.url)
                unique_results.append(item)

        self.logger.info(f"去重后剩余 {len(unique_results)} 个条目")

        # 按时间过滤
        if max_age_hours:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            filtered_results = [item for item in unique_results if item.publish_date >= cutoff_time]
            self.logger.info(f"按时间过滤后剩余 {len(filtered_results)} 个条目")
        else:
            filtered_results = unique_results

        return filtered_results

    def sort_results(self, results: List[NewsItem] = None) -> List[NewsItem]:
        """
        排序结果

        Args:
            results: 要排序的结果列表，如果为None则使用内部结果

        Returns:
            排序后的结果列表
        """
        if results is None:
            results = self.results

        if not results:
            return []

        # 按发布时间降序排序（最新的在前）
        sorted_results = sorted(
            results,
            key=lambda x: x.publish_date,
            reverse=True
        )

        return sorted_results

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计信息字典
        """
        successful_fetchers = len(self.fetchers) - len(self.failed_fetchers)

        stats = {
            "total_fetchers": len(self.fetchers),
            "successful_fetchers": successful_fetchers,
            "failed_fetchers": len(self.failed_fetchers),
            "total_results": len(self.results),
            "results_by_source": {},
            "results_by_type": {},
            "failed_sources": [f["name"] for f in self.failed_fetchers],
        }

        # 按来源统计
        for item in self.results:
            source = item.source
            stats["results_by_source"][source] = stats["results_by_source"].get(source, 0) + 1

            source_type = item.source_type
            stats["results_by_type"][source_type] = stats["results_by_type"].get(source_type, 0) + 1

        return stats

    async def run(self) -> List[NewsItem]:
        """
        运行完整抓取流程

        Returns:
            抓取结果列表
        """
        self.logger.info("开始运行抓取流程")

        # 1. 加载抓取器
        self.load_fetchers()

        # 2. 并发抓取
        await self.fetch_all()

        # 3. 过滤结果
        filtered_results = self.filter_results()

        # 4. 排序结果（按发布时间降序）
        sorted_results = self.sort_results(filtered_results)

        # 5. 输出统计信息
        stats = self.get_statistics()
        self.logger.info(f"抓取流程完成，最终结果: {len(sorted_results)} 个条目")
        self.logger.info(f"统计信息: {stats}")

        return sorted_results