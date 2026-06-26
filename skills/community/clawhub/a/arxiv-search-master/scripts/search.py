#!/usr/bin/env python3
"""
search.py - arXiv 检索模块
提供关键词检索、作者检索、分类检索、日期过滤等功能

命令行参数:
  检索条件 (至少提供一个):
    --query, -q          通用查询字符串
    --title, -t          标题关键词
    --abstract, -a       摘要关键词
    --author, -au        作者名
    --category, -c       arXiv 分类 (如 cs.AI, quant-ph)

  日期过滤:
    --start-date, -s     起始日期 (YYYY-MM-DD)
    --end-date, -e       结束日期 (YYYY-MM-DD)

  检索控制 (可选):
    --max-results, -m    最大结果数 (默认: 100)
    --sort-by             排序方式: relevance, lastUpdatedDate, submittedDate (默认: relevance)
    --sort-order          排序顺序: descending, ascending (默认: descending)
    --timeout             请求超时秒数 (默认: 30)
    --retry-attempts      重试次数 (默认: 3)

  速率限制 (可选):
    --requests-per-second 每秒最大请求数 (默认: 2.0)
    --min-delay           请求间最小延迟秒数 (默认: 0.5)

  输出:
    --output, -o          输出元数据 JSON 文件路径
    --id-list             从文件读取 arXiv ID 列表进行检索

  日志 (可选):
    --log-level           日志级别: DEBUG, INFO, WARNING, ERROR (默认: INFO)
    --log-file            日志文件路径
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

import arxiv

# 支持作为模块导入和独立脚本运行
try:
    from .utils import (
        setup_logging,
        get_logger,
        save_json,
        slugify,
        RateLimiter,
        parse_arxiv_id,
        load_json,
    )
except ImportError:
    from utils import (
        setup_logging,
        get_logger,
        save_json,
        slugify,
        RateLimiter,
        parse_arxiv_id,
        load_json,
    )


class ArxivSearch:
    """arXiv 检索类"""

    def __init__(
        self,
        timeout: int = 30,
        retry_attempts: int = 3,
        requests_per_second: float = 2.0,
        min_delay: float = 0.5,
        log_level: str = "INFO",
        log_file: str = None,
    ):
        """
        初始化检索器

        Args:
            timeout: 请求超时秒数
            retry_attempts: 重试次数
            requests_per_second: 每秒最大请求数
            min_delay: 请求间最小延迟秒数
            log_level: 日志级别
            log_file: 日志文件路径
        """
        setup_logging(level=log_level, log_file=log_file)
        self.logger = get_logger()

        self.rate_limiter = RateLimiter(requests_per_second, min_delay)

        # 初始化 arXiv 客户端
        self.client = arxiv.Client(
            page_size=100,
            delay_seconds=min_delay,
            num_retries=retry_attempts,
        )

    def build_query(
        self,
        query: str = None,
        title: str = None,
        abstract: str = None,
        author: str = None,
        category: str = None,
    ) -> str:
        """
        构建 arXiv 查询字符串

        Args:
            query: 通用查询字符串
            title: 标题关键词
            abstract: 摘要关键词
            author: 作者名
            category: arXiv 分类

        Returns:
            组合后的查询字符串
        """
        conditions = []

        if query:
            conditions.append(f"({query})")

        if title:
            title_terms = " AND ".join([f'ti:"{term}"' for term in title.split()])
            conditions.append(f"({title_terms})")

        if abstract:
            abstract_terms = " AND ".join([f'abs:"{term}"' for term in abstract.split()])
            conditions.append(f"({abstract_terms})")

        if author:
            author = author.strip()
            if "," in author:
                conditions.append(f'au:"{author}"')
            else:
                conditions.append(f'au:"{author}"')

        if category:
            categories = [c.strip() for c in category.split(",")]
            if len(categories) == 1:
                conditions.append(f"cat:{categories[0]}")
            else:
                cat_conditions = " OR ".join([f"cat:{c}" for c in categories])
                conditions.append(f"({cat_conditions})")

        if not conditions:
            raise ValueError("至少需要提供一个检索条件")

        return " AND ".join(conditions)

    def _convert_result(self, paper: arxiv.Result) -> Dict[str, Any]:
        """
        将 arxiv.Result 转换为标准化字典
        """
        arxiv_id = parse_arxiv_id(paper.entry_id)

        return {
            "arxiv_id": arxiv_id,
            "arxiv_url": paper.entry_id,
            "pdf_url": paper.pdf_url,
            "title": paper.title.strip(),
            "authors": [{"name": author.name} for author in paper.authors],
            "abstract": paper.summary.strip(),
            "categories": paper.categories,
            "primary_category": paper.primary_category,
            "published_date": paper.published.strftime("%Y-%m-%d") if paper.published else None,
            "updated_date": paper.updated.strftime("%Y-%m-%d") if paper.updated else None,
            "doi": paper.doi,
            "journal_ref": paper.journal_ref,
            "comments": paper.comment,
        }

    def _filter_by_date(
        self,
        papers: List[Dict[str, Any]],
        start_date: str = None,
        end_date: str = None,
    ) -> List[Dict[str, Any]]:
        """按日期范围过滤论文"""
        if not start_date and not end_date:
            return papers

        filtered = []
        for paper in papers:
            pub_date = paper.get("published_date") or paper.get("updated_date")
            if not pub_date:
                continue

            try:
                paper_date = datetime.strptime(pub_date, "%Y-%m-%d").date()

                if start_date:
                    start = datetime.strptime(start_date, "%Y-%m-%d").date()
                    if paper_date < start:
                        continue

                if end_date:
                    end = datetime.strptime(end_date, "%Y-%m-%d").date()
                    if paper_date > end:
                        continue

                filtered.append(paper)
            except (ValueError, TypeError):
                continue

        return filtered

    def search(
        self,
        query: str = None,
        title: str = None,
        abstract: str = None,
        author: str = None,
        category: str = None,
        start_date: str = None,
        end_date: str = None,
        max_results: int = 100,
        sort_by: str = "relevance",
        sort_order: str = "descending",
    ) -> Dict[str, Any]:
        """
        执行检索

        Args:
            query: 通用查询字符串
            title: 标题关键词
            abstract: 摘要关键词
            author: 作者名
            category: arXiv 分类
            start_date: 起始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            max_results: 最大结果数 (默认: 100)
            sort_by: 排序方式: relevance, lastUpdatedDate, submittedDate (默认: relevance)
            sort_order: 排序顺序: descending, ascending (默认: descending)

        Returns:
            检索结果字典
        """
        # 映射排序参数
        sort_by_map = {
            "relevance": arxiv.SortCriterion.Relevance,
            "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
            "submittedDate": arxiv.SortCriterion.SubmittedDate,
        }

        sort_order_map = {
            "descending": arxiv.SortOrder.Descending,
            "ascending": arxiv.SortOrder.Ascending,
        }

        # 构建查询
        query_str = self.build_query(
            query=query,
            title=title,
            abstract=abstract,
            author=author,
            category=category,
        )

        self.logger.info(f"执行检索: {query_str}")

        # 创建检索对象
        search = arxiv.Search(
            query=query_str,
            max_results=max_results * 2,
            sort_by=sort_by_map.get(sort_by, arxiv.SortCriterion.Relevance),
            sort_order=sort_order_map.get(sort_order, arxiv.SortOrder.Descending),
        )

        # 执行检索
        papers = []
        try:
            self.rate_limiter.wait()

            for i, result in enumerate(self.client.results(search)):
                if i >= max_results * 2:
                    break
                papers.append(self._convert_result(result))

        except Exception as e:
            self.logger.error(f"检索失败: {e}")
            raise

        # 日期过滤
        if start_date or end_date:
            papers = self._filter_by_date(papers, start_date, end_date)
            self.logger.info(f"日期过滤后剩余 {len(papers)} 篇论文")

        # 限制结果数
        papers = papers[:max_results]

        self.logger.info(f"检索完成，返回 {len(papers)} 篇论文")

        return {
            "search_metadata": {
                "query": query_str,
                "original_query": {
                    "query": query,
                    "title": title,
                    "abstract": abstract,
                    "author": author,
                    "category": category,
                    "start_date": start_date,
                    "end_date": end_date,
                },
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "returned_results": len(papers),
            },
            "papers": papers,
        }

    def search_by_id(self, arxiv_ids: List[str]) -> Dict[str, Any]:
        """
        通过 arXiv ID 列表检索论文

        Args:
            arxiv_ids: arXiv ID 列表

        Returns:
            检索结果
        """
        papers = []
        failed_ids = []

        for arxiv_id in arxiv_ids:
            try:
                self.rate_limiter.wait()
                normalized_id = parse_arxiv_id(arxiv_id)
                search = arxiv.Search(id_list=[normalized_id])

                for result in self.client.results(search):
                    papers.append(self._convert_result(result))
                    break

            except Exception as e:
                self.logger.warning(f"获取 {arxiv_id} 失败: {e}")
                failed_ids.append(arxiv_id)

        return {
            "search_metadata": {
                "query": "id_list",
                "requested_ids": arxiv_ids,
                "failed_ids": failed_ids,
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "returned_results": len(papers),
            },
            "papers": papers,
        }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="arXiv 论文检索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础关键词检索
  python search.py --query "quantum computing" --max-results 50

  # 标题检索
  python search.py --title "transformer" --max-results 30

  # 作者检索
  python search.py --author "Smith, J" --max-results 100

  # 分类检索
  python search.py --category "cs.AI" --start-date "2023-01-01"

  # 组合检索并保存结果
  python search.py --query "deep learning" --category "cs.LG" --max-results 50 --output results.json
        """
    )

    # 检索条件
    parser.add_argument("--query", "-q", help="通用查询字符串")
    parser.add_argument("--title", "-t", help="标题关键词")
    parser.add_argument("--abstract", "-a", help="摘要关键词")
    parser.add_argument("--author", "-au", help="作者名")
    parser.add_argument("--category", "-c", help="arXiv 分类 (如 cs.AI, quant-ph)")

    # 日期过滤
    parser.add_argument("--start-date", "-s", help="起始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", "-e", help="结束日期 (YYYY-MM-DD)")

    # 检索控制
    parser.add_argument("--max-results", "-m", type=int, default=100, help="最大结果数 (默认: 100)")
    parser.add_argument(
        "--sort-by",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
        default="relevance",
        help="排序方式 (默认: relevance)",
    )
    parser.add_argument(
        "--sort-order",
        choices=["descending", "ascending"],
        default="descending",
        help="排序顺序 (默认: descending)",
    )
    parser.add_argument("--timeout", type=int, default=30, help="请求超时秒数 (默认: 30)")
    parser.add_argument("--retry-attempts", type=int, default=3, help="重试次数 (默认: 3)")

    # 速率限制
    parser.add_argument("--requests-per-second", type=float, default=2.0, help="每秒最大请求数 (默认: 2.0)")
    parser.add_argument("--min-delay", type=float, default=0.5, help="请求间最小延迟秒数 (默认: 0.5)")

    # 输入输出
    parser.add_argument("--id-list", help="从文件读取 arXiv ID 列表进行检索")
    parser.add_argument("--output", "-o", help="输出元数据 JSON 文件路径")

    # 日志
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="日志级别 (默认: INFO)")
    parser.add_argument("--log-file", help="日志文件路径")

    args = parser.parse_args()

    # 初始化检索器
    searcher = ArxivSearch(
        timeout=args.timeout,
        retry_attempts=args.retry_attempts,
        requests_per_second=args.requests_per_second,
        min_delay=args.min_delay,
        log_level=args.log_level,
        log_file=args.log_file,
    )

    logger = get_logger()

    try:
        if args.id_list:
            # 从 ID 列表检索
            id_list_path = Path(args.id_list)
            if not id_list_path.exists():
                logger.error(f"ID 列表文件不存在: {args.id_list}")
                return 1

            arxiv_ids = []
            with open(id_list_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        arxiv_ids.append(line)

            logger.info(f"从列表加载 {len(arxiv_ids)} 个 arXiv ID")
            results = searcher.search_by_id(arxiv_ids)

        else:
            # 执行条件检索
            if not any([args.query, args.title, args.abstract, args.author, args.category]):
                logger.error("至少需要提供一个检索条件 (--query, --title, --abstract, --author, --category)")
                parser.print_help()
                return 1

            results = searcher.search(
                query=args.query,
                title=args.title,
                abstract=args.abstract,
                author=args.author,
                category=args.category,
                start_date=args.start_date,
                end_date=args.end_date,
                max_results=args.max_results,
                sort_by=args.sort_by,
                sort_order=args.sort_order,
            )

        # 输出结果
        if args.output:
            save_json(results, args.output)
            logger.info(f"结果已保存到: {args.output}")
        else:
            import json
            print(json.dumps(results, indent=2, ensure_ascii=False))

        # 打印摘要信息
        print(f"\n==== 检索摘要 ====")
        print(f"返回论文数: {results['search_metadata']['returned_results']}")
        if results["papers"]:
            print(f"\n前 5 篇论文:")
            for i, paper in enumerate(results["papers"][:5]):
                title = paper["title"][:80] + "..." if len(paper["title"]) > 80 else paper["title"]
                print(f"  {i+1}. [{paper['arxiv_id']}] {title}")

        return 0

    except Exception as e:
        logger.error(f"执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
