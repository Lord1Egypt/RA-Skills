"""Arxiv 论文搜索模块"""

import arxiv
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time


class ArxivSearcher:
    """Arxiv 论文搜索器"""

    def __init__(self, config: Dict[str, Any]):
        self.max_results = config.get('max_results', 10)
        self.time_window_hours = config.get('time_window_hours', 24)
        self.default_query = config.get('default_query', 'AI Agent')
        self.categories = config.get('search_categories', ['cs.AI', 'cs.CL', 'cs.LG'])
        self.request_delay = config.get('request_delay', 3)

    def search_papers(
        self,
        query: Optional[str] = None,
        max_results: Optional[int] = None,
        time_window_hours: Optional[int] = None,
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索 Arxiv 论文

        Args:
            query: 搜索关键词，默认使用配置中的 default_query
            max_results: 最大结果数，默认使用配置中的 max_results
            time_window_hours: 时间窗口（小时），默认使用配置中的 time_window_hours
            categories: 搜索分类，默认使用配置中的 categories

        Returns:
            论文元数据列表
        """
        query = query or self.default_query
        max_results = max_results or self.max_results
        time_window_hours = time_window_hours or self.time_window_hours
        categories = categories or self.categories

        # 构建搜索查询
        search_query = self._build_search_query(query, categories)

        # 计算时间范围
        start_time, end_time = self._get_time_range(time_window_hours)

        # 执行搜索
        papers = []
        try:
            search = arxiv.Search(
                query=search_query,
                max_results=max_results * 3,  # 获取更多结果以过滤时间
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )

            for result in search.results():
                # 检查时间范围
                if start_time <= result.published.replace(tzinfo=None) <= end_time:
                    paper_data = self._extract_metadata(result)
                    papers.append(paper_data)

                    if len(papers) >= max_results:
                        break

                # Arxiv API 已经有内置限流，不需要额外延迟

        except Exception as e:
            print(f"搜索过程中出错: {e}")
            raise

        return papers

    def _build_search_query(self, query: str, categories: List[str]) -> str:
        """构建搜索查询字符串"""
        # arxiv API 查询格式
        category_query = ' OR '.join([f'cat:{cat}' for cat in categories])
        return f'({query}) AND ({category_query})'

    def _get_time_range(self, hours: int) -> tuple[datetime, datetime]:
        """获取时间范围"""
        end_time = datetime.utcnow()  # 使用 UTC 时间以匹配 Arxiv API
        start_time = end_time - timedelta(hours=hours)
        return start_time, end_time

    def _extract_metadata(self, result: arxiv.Result) -> Dict[str, Any]:
        """提取论文元数据"""
        return {
            'title': result.title,
            'arxiv_id': result.entry_id.split('/')[-1],
            'authors': [author.name for author in result.authors],
            'published': result.published.strftime('%Y-%m-%d %H:%M:%S'),
            'updated': result.updated.strftime('%Y-%m-%d %H:%M:%S') if result.updated else None,
            'summary': result.summary.replace('\n', ' ').strip(),
            'categories': [cat for cat in result.categories],
            'pdf_url': result.pdf_url,
            'entry_id': result.entry_id,
            'primary_category': result.primary_category,
            'comment': result.comment,
            'journal_ref': result.journal_ref,
            'doi': result.doi
        }


def search_arxiv_papers(
    query: Optional[str] = None,
    max_results: Optional[int] = None,
    time_window_hours: Optional[int] = None,
    config: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    搜索 Arxiv 论文的便捷函数

    Args:
        query: 搜索关键词
        max_results: 最大结果数
        time_window_hours: 时间窗口（小时）
        config: 配置字典

    Returns:
        论文元数据列表
    """
    if config is None:
        from utils import load_config
        config = load_config()

    searcher = ArxivSearcher(config)
    return searcher.search_papers(query, max_results, time_window_hours)
