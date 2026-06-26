#!/usr/bin/env python3
"""
batch_search.py - 批量检索模块
支持从 JSONL 文件批量执行多个检索任务

命令行参数:
  输入:
    --input, -i           输入 JSONL 文件路径 (必需)

  输出:
    --output, -o          输出目录 (默认: output/metadata)
    --no-individual       不保存单独的查询结果

  检索控制 (可选):
    --timeout             请求超时秒数 (默认: 30)
    --retry-attempts      重试次数 (默认: 3)
    --requests-per-second 每秒最大请求数 (默认: 2.0)
    --min-delay           请求间最小延迟秒数 (默认: 0.5)

  日志 (可选):
    --log-level           日志级别: DEBUG, INFO, WARNING, ERROR (默认: INFO)
    --log-file            日志文件路径
"""

import argparse
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from tqdm import tqdm

# 支持作为模块导入和独立脚本运行
try:
    from .utils import (
        setup_logging,
        get_logger,
        save_json,
        load_jsonl,
        ensure_dir,
    )
    from .search import ArxivSearch
except ImportError:
    from utils import (
        setup_logging,
        get_logger,
        save_json,
        load_jsonl,
        ensure_dir,
    )
    from search import ArxivSearch


class BatchSearch:
    """批量检索器"""

    def __init__(
        self,
        output_dir: str = "output/metadata",
        timeout: int = 30,
        retry_attempts: int = 3,
        requests_per_second: float = 2.0,
        min_delay: float = 0.5,
        log_level: str = "INFO",
        log_file: str = None,
    ):
        """
        初始化批量检索器

        Args:
            output_dir: 输出目录 (默认: output/metadata)
            timeout: 请求超时秒数 (默认: 30)
            retry_attempts: 重试次数 (默认: 3)
            requests_per_second: 每秒最大请求数 (默认: 2.0)
            min_delay: 请求间最小延迟秒数 (默认: 0.5)
            log_level: 日志级别
            log_file: 日志文件路径
        """
        setup_logging(level=log_level, log_file=log_file)
        self.logger = get_logger()

        self.output_dir = Path(output_dir)
        ensure_dir(self.output_dir)

        self.searcher = ArxivSearch(
            timeout=timeout,
            retry_attempts=retry_attempts,
            requests_per_second=requests_per_second,
            min_delay=min_delay,
            log_level=log_level,
            log_file=log_file,
        )

    def parse_query_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析查询规范

        Args:
            spec: 查询规范字典

        Returns:
            解析后的参数字典
        """
        params = {}

        field_map = {
            "query": "query",
            "q": "query",
            "title": "title",
            "t": "title",
            "abstract": "abstract",
            "a": "abstract",
            "author": "author",
            "au": "author",
            "category": "category",
            "c": "category",
            "categories": "category",
            "start_date": "start_date",
            "start-date": "start_date",
            "s": "start_date",
            "end_date": "end_date",
            "end-date": "end_date",
            "e": "end_date",
            "max_results": "max_results",
            "max-results": "max_results",
            "m": "max_results",
            "sort_by": "sort_by",
            "sort-by": "sort_by",
            "sort_order": "sort_order",
            "sort-order": "sort_order",
        }

        for src, dst in field_map.items():
            if src in spec:
                params[dst] = spec[src]

        return params

    def run_query(self, query_spec: Dict[str, Any], index: int = 0) -> Dict[str, Any]:
        """
        运行单个查询

        Args:
            query_spec: 查询规范
            index: 查询索引

        Returns:
            检索结果
        """
        params = self.parse_query_spec(query_spec)
        query_name = query_spec.get("name", f"query_{index:03d}")

        self.logger.info(f"执行查询 [{query_name}]: {params}")

        try:
            results = self.searcher.search(**params)
            results["search_metadata"]["query_name"] = query_name
            results["search_metadata"]["query_spec"] = query_spec

            return {
                "success": True,
                "query_name": query_name,
                "results": results,
                "paper_count": len(results["papers"]),
            }

        except Exception as e:
            self.logger.error(f"查询 [{query_name}] 失败: {e}")
            return {
                "success": False,
                "query_name": query_name,
                "error": str(e),
                "query_spec": query_spec,
            }

    def run_batch(
        self,
        query_specs: List[Dict[str, Any]],
        save_individual: bool = True,
    ) -> Dict[str, Any]:
        """
        运行批量检索

        Args:
            query_specs: 查询规范列表
            save_individual: 是否保存每个查询的单独结果

        Returns:
            批量检索结果汇总
        """
        all_results = []
        all_papers = []
        summary = {
            "total_queries": len(query_specs),
            "successful": 0,
            "failed": 0,
            "total_papers": 0,
            "queries": [],
        }

        self.logger.info(f"开始批量检索: {len(query_specs)} 个查询")

        for i, spec in enumerate(tqdm(query_specs, desc="检索进度")):
            result = self.run_query(spec, i)
            all_results.append(result)

            if result["success"]:
                summary["successful"] += 1
                papers = result["results"]["papers"]
                all_papers.extend(papers)
                summary["total_papers"] += len(papers)

                summary["queries"].append({
                    "name": result["query_name"],
                    "paper_count": result["paper_count"],
                    "success": True,
                })

                if save_individual:
                    output_file = self.output_dir / f"{result['query_name']}.json"
                    save_json(result["results"], output_file)

            else:
                summary["failed"] += 1
                summary["queries"].append({
                    "name": result["query_name"],
                    "error": result["error"],
                    "success": False,
                })

        merged = {
            "search_metadata": {
                "type": "batch_search",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "summary": summary,
            },
            "papers": all_papers,
            "individual_results": all_results,
        }

        merged_file = self.output_dir / "merged_metadata.json"
        save_json(merged, merged_file)

        self.logger.info(f"批量检索完成: 成功={summary['successful']}, 失败={summary['failed']}, 论文总数={summary['total_papers']}")
        return merged


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="arXiv 批量检索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
输入文件格式 (JSONL):
  {"query": "deep learning", "max_results": 50}
  {"author": "Bengio, Y", "max_results": 100, "name": "bengio_papers"}

示例:
  # 从 JSONL 文件运行批量检索
  python batch_search.py --input queries.jsonl

  # 指定输出目录
  python batch_search.py --input queries.jsonl --output batch_results/
        """
    )

    parser.add_argument("--input", "-i", required=True, help="输入 JSONL 文件路径")
    parser.add_argument("--output", "-o", default="output/metadata", help="输出目录 (默认: output/metadata)")
    parser.add_argument("--no-individual", action="store_true", help="不保存单独的查询结果")

    # 检索控制
    parser.add_argument("--timeout", type=int, default=30, help="请求超时秒数 (默认: 30)")
    parser.add_argument("--retry-attempts", type=int, default=3, help="重试次数 (默认: 3)")
    parser.add_argument("--requests-per-second", type=float, default=2.0, help="每秒最大请求数 (默认: 2.0)")
    parser.add_argument("--min-delay", type=float, default=0.5, help="请求间最小延迟秒数 (默认: 0.5)")

    # 日志
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="日志级别 (默认: INFO)")
    parser.add_argument("--log-file", help="日志文件路径")

    args = parser.parse_args()

    setup_logging(level=args.log_level, log_file=args.log_file)
    logger = get_logger()

    # 检查输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"输入文件不存在: {args.input}")
        return 1

    # 加载查询规范
    try:
        query_specs = load_jsonl(input_path)
        logger.info(f"加载了 {len(query_specs)} 个查询")
    except Exception as e:
        logger.error(f"无法加载输入文件: {e}")
        return 1

    # 运行批量检索
    batch_search = BatchSearch(
        output_dir=args.output,
        timeout=args.timeout,
        retry_attempts=args.retry_attempts,
        requests_per_second=args.requests_per_second,
        min_delay=args.min_delay,
        log_level=args.log_level,
        log_file=args.log_file,
    )

    try:
        results = batch_search.run_batch(
            query_specs,
            save_individual=not args.no_individual,
        )

        # 打印摘要
        summary = results["search_metadata"]["summary"]
        print("\n==== 批量检索摘要 ====")
        print(f"总查询数: {summary['total_queries']}")
        print(f"成功: {summary['successful']}")
        print(f"失败: {summary['failed']}")
        print(f"总论文数: {summary['total_papers']}")

        if summary["failed"] > 0:
            print("\n失败的查询:")
            for q in summary["queries"]:
                if not q["success"]:
                    print(f"  - {q['name']}: {q.get('error', 'unknown')}")

        return 0

    except Exception as e:
        logger.error(f"批量检索失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
