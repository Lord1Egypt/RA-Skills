#!/usr/bin/env python3
"""
summarize.py - 论文摘要/总结模块
提供论文元数据分析、摘要生成、文献综述辅助等功能

命令行参数:
  输入方式 (选择一个):
    --id                  单个 arXiv ID
    --metadata            包含论文元数据的 JSON 文件

  输出选项:
    --output, -o          输出文件路径
    --output-dir          输出目录（用于批量模式，默认: output/summaries）

  功能选项:
    --overview            生成文献综述概览
    --topic               研究主题（用于综述）

  日志 (可选):
    --log-level           日志级别: DEBUG, INFO, WARNING, ERROR (默认: INFO)
    --log-file            日志文件路径
"""

import argparse
import sys
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import Counter, defaultdict

# 支持作为模块导入和独立脚本运行
try:
    from .utils import (
        setup_logging,
        get_logger,
        ensure_dir,
        load_json,
        save_json,
        parse_arxiv_id,
    )
    from .search import ArxivSearch
except ImportError:
    from utils import (
        setup_logging,
        get_logger,
        ensure_dir,
        load_json,
        save_json,
        parse_arxiv_id,
    )
    from search import ArxivSearch


class PaperSummarizer:
    """论文摘要生成器"""

    def __init__(
        self,
        output_dir: str = "output/summaries",
        log_level: str = "INFO",
        log_file: str = None,
    ):
        """
        初始化摘要生成器

        Args:
            output_dir: 输出目录 (默认: output/summaries)
            log_level: 日志级别
            log_file: 日志文件路径
        """
        setup_logging(level=log_level, log_file=log_file)
        self.logger = get_logger()

        self.output_dir = Path(output_dir)
        ensure_dir(self.output_dir)

        self.searcher = ArxivSearch(log_level=log_level, log_file=log_file)

        self.method_keywords = [
            "algorithm", "model", "method", "approach", "framework", "architecture",
            "network", "neural", "deep", "learning", "training", "optimization",
            "regression", "classification", "clustering", "embedding", "attention",
            "transformer", "cnn", "rnn", "lstm", "gan", "vae", "reinforcement",
            "bayesian", "probabilistic", "stochastic", "deterministic", "gradient",
            "backpropagation", "regularization", "normalization", "dropout",
        ]

        self.task_keywords = [
            "classification", "detection", "segmentation", "recognition", "generation",
            "translation", "summarization", "paraphrasing", "question", "answering",
            "reasoning", "inference", "prediction", "forecasting", "recommendation",
            "retrieval", "search", "matching", "alignment", "synthesis", "editing",
            "compression", "denoising", "restoration", "enhancement", "understanding",
        ]

    def extract_key_points(self, abstract: str) -> Dict[str, Any]:
        """
        从摘要中提取关键点

        Args:
            abstract: 摘要文本

        Returns:
            关键点字典
        """
        abstract_lower = abstract.lower()

        methods = []
        for keyword in self.method_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, abstract_lower):
                methods.append(keyword)

        tasks = []
        for keyword in self.task_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, abstract_lower):
                tasks.append(keyword)

        sentences = re.split(r'[.!?]+', abstract)
        problem_statement = sentences[0].strip() if sentences else ""

        contributions = []
        contribution_patterns = [
            r'we (?:propose|introduce|present|describe|develop|create) ([^.]+)',
            r'this (?:paper|work|study) ([^.]+)',
            r'we (?:show|demonstrate|prove|find) ([^.]+)',
            r'our (?:method|approach|model|framework) ([^.]+)',
        ]

        for pattern in contribution_patterns:
            matches = re.findall(pattern, abstract, re.IGNORECASE)
            contributions.extend([m.strip() for m in matches if m.strip()])

        return {
            "methods": methods,
            "tasks": tasks,
            "problem_statement": problem_statement,
            "contributions": contributions[:5],
        }

    def summarize_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成单篇论文的摘要

        Args:
            paper: 论文元数据

        Returns:
            论文摘要
        """
        abstract = paper.get("abstract", "")
        key_points = self.extract_key_points(abstract) if abstract else {}

        summary = {
            "arxiv_id": paper.get("arxiv_id"),
            "title": paper.get("title"),
            "authors": [a.get("name", "") for a in paper.get("authors", [])],
            "published_date": paper.get("published_date"),
            "categories": paper.get("categories", []),
            "primary_category": paper.get("primary_category"),
            "url": paper.get("arxiv_url"),
            "pdf_url": paper.get("pdf_url"),
            "abstract_short": abstract[:500] + "..." if len(abstract) > 500 else abstract,
            "key_points": key_points,
            "generated_at": datetime.now(timezone.utc).isoformat() + "Z",
        }

        return summary

    def analyze_collection(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析论文集合，生成统计和趋势

        Args:
            papers: 论文列表

        Returns:
            集合分析结果
        """
        category_counts = Counter()
        primary_category_counts = Counter()
        for paper in papers:
            for cat in paper.get("categories", []):
                category_counts[cat] += 1
            if paper.get("primary_category"):
                primary_category_counts[paper["primary_category"]] += 1

        year_counts = Counter()
        for paper in papers:
            date = paper.get("published_date") or paper.get("updated_date")
            if date:
                year = date[:4]
                year_counts[year] += 1

        all_methods = Counter()
        all_tasks = Counter()

        for paper in papers:
            abstract = paper.get("abstract", "")
            if abstract:
                key_points = self.extract_key_points(abstract)
                for method in key_points.get("methods", []):
                    all_methods[method] += 1
                for task in key_points.get("tasks", []):
                    all_tasks[task] += 1

        papers_by_year = defaultdict(list)
        for paper in papers:
            date = paper.get("published_date") or paper.get("updated_date")
            if date:
                year = date[:4]
                papers_by_year[year].append(paper)

        return {
            "collection_summary": {
                "total_papers": len(papers),
                "date_range": {
                    "earliest": min([p.get("published_date", "9999-99-99") for p in papers]) if papers else None,
                    "latest": max([p.get("published_date", "0000-00-00") for p in papers]) if papers else None,
                },
            },
            "categories": {
                "primary": dict(primary_category_counts.most_common()),
                "all": dict(category_counts.most_common()),
            },
            "year_distribution": dict(year_counts.most_common()),
            "methods": dict(all_methods.most_common(20)),
            "tasks": dict(all_tasks.most_common(20)),
            "papers_by_year": {
                year: len(papers)
                for year, papers in sorted(papers_by_year.items())
            },
        }

    def generate_literature_overview(
        self,
        papers: List[Dict[str, Any]],
        topic: str = None,
    ) -> Dict[str, Any]:
        """
        生成文献综述概览

        Args:
            papers: 论文列表
            topic: 研究主题

        Returns:
            文献综述
        """
        collection_analysis = self.analyze_collection(papers)
        paper_summaries = [self.summarize_paper(p) for p in papers]

        overview = {
            "topic": topic,
            "generated_at": datetime.now(timezone.utc).isoformat() + "Z",
            "collection_analysis": collection_analysis,
            "paper_summaries": paper_summaries,
            "key_insights": self._generate_key_insights(collection_analysis, paper_summaries),
        }

        return overview

    def _generate_key_insights(
        self,
        analysis: Dict[str, Any],
        summaries: List[Dict[str, Any]],
    ) -> List[str]:
        """生成关键洞察"""
        insights = []

        total = analysis["collection_summary"]["total_papers"]
        insights.append(f"共分析 {total} 篇论文")

        primary_cats = analysis["categories"]["primary"]
        if primary_cats:
            top_cat = list(primary_cats.keys())[0]
            insights.append(f"主要研究领域: {top_cat} ({primary_cats[top_cat]} 篇)")

        methods = analysis["methods"]
        if methods:
            top_methods = list(methods.keys())[:3]
            insights.append(f"常用方法: {', '.join(top_methods)}")

        tasks = analysis["tasks"]
        if tasks:
            top_tasks = list(tasks.keys())[:3]
            insights.append(f"研究任务: {', '.join(top_tasks)}")

        return insights


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="arXiv 论文总结工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 总结单篇论文
  python summarize.py --id 2301.01234

  # 从元数据文件批量生成总结
  python summarize.py --metadata results.json

  # 生成文献综述
  python summarize.py --metadata results.json --overview --topic "deep learning"
        """
    )

    # 输入方式
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--id", help="单个 arXiv ID")
    input_group.add_argument("--metadata", help="包含论文元数据的 JSON 文件")

    # 输出选项
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--output-dir", default="output/summaries", help="输出目录（用于批量模式，默认: output/summaries）")

    # 功能选项
    parser.add_argument("--overview", action="store_true", help="生成文献综述概览")
    parser.add_argument("--topic", help="研究主题（用于综述）")

    # 日志
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="日志级别 (默认: INFO)")
    parser.add_argument("--log-file", help="日志文件路径")

    args = parser.parse_args()

    summarizer = PaperSummarizer(
        output_dir=args.output_dir,
        log_level=args.log_level,
        log_file=args.log_file,
    )

    logger = get_logger()

    try:
        papers = []

        if args.id:
            paper = summarizer.searcher.search_by_id([args.id])["papers"]
            if paper:
                papers = paper
            else:
                logger.error(f"无法获取论文: {args.id}")
                return 1

        elif args.metadata:
            data = load_json(args.metadata)
            if isinstance(data, dict) and "papers" in data:
                papers = data["papers"]
            elif isinstance(data, list):
                papers = data
            else:
                logger.error("无法识别的输入格式")
                return 1

        if not papers:
            logger.warning("没有要处理的论文")
            return 0

        if args.overview:
            overview = summarizer.generate_literature_overview(papers, topic=args.topic)

            if args.output:
                save_json(overview, args.output)
                logger.info(f"综述已保存到: {args.output}")
            else:
                import json
                print(json.dumps(overview, indent=2, ensure_ascii=False))

            print("\n==== 文献综述摘要 ====")
            print(f"论文总数: {overview['collection_analysis']['collection_summary']['total_papers']}")
            print("\n关键洞察:")
            for insight in overview["key_insights"]:
                print(f"  - {insight}")

        else:
            if len(papers) == 1:
                summary = summarizer.summarize_paper(papers[0])
                if args.output:
                    save_json(summary, args.output)
                    logger.info(f"总结已保存到: {args.output}")
                else:
                    import json
                    print(json.dumps(summary, indent=2, ensure_ascii=False))
            else:
                output_dir = Path(args.output_dir) if args.output_dir else summarizer.output_dir
                ensure_dir(output_dir)

                summaries = []
                for paper in papers:
                    summary = summarizer.summarize_paper(paper)
                    summaries.append(summary)

                    arxiv_id = summary["arxiv_id"]
                    paper_file = output_dir / f"{arxiv_id}_summary.json"
                    save_json(summary, paper_file)

                if args.output:
                    save_json(summaries, args.output)
                    logger.info(f"汇总已保存到: {args.output}")

                print(f"\n已生成 {len(summaries)} 篇论文的总结")

        return 0

    except Exception as e:
        logger.error(f"执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
