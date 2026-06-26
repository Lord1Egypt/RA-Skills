#!/usr/bin/env python3
"""
download.py - arXiv 论文下载模块
提供单个或批量论文 PDF 下载功能

命令行参数:
  输入源 (选择一个):
    --id                  arXiv ID（可多次指定）
    --id-list             包含 arXiv ID 列表的文本文件
    --metadata            包含论文元数据的 JSON 文件

  输出选项:
    --output-dir, -o      输出目录 (默认: output/pdfs)
    --skip-existing       跳过已存在的文件 (默认)
    --no-skip-existing    覆盖已存在的文件

  下载控制 (可选):
    --parallel            并行下载数 (默认: 3)
    --chunk-size          下载块大小字节 (默认: 8192)
    --verify-ssl          验证 SSL 证书 (默认: true)

  速率限制 (可选):
    --requests-per-second 每秒最大请求数 (默认: 2.0)
    --min-delay           请求间最小延迟秒数 (默认: 0.5)

  日志 (可选):
    --log-level           日志级别: DEBUG, INFO, WARNING, ERROR (默认: INFO)
    --log-file            日志文件路径
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from tqdm import tqdm

# 支持作为模块导入和独立脚本运行
try:
    from .utils import (
        setup_logging,
        get_logger,
        ensure_dir,
        sanitize_filename,
        slugify,
        parse_arxiv_id,
        RateLimiter,
        load_json,
    )
except ImportError:
    from utils import (
        setup_logging,
        get_logger,
        ensure_dir,
        sanitize_filename,
        slugify,
        parse_arxiv_id,
        RateLimiter,
        load_json,
    )


class PaperDownloader:
    """论文下载器"""

    def __init__(
        self,
        output_dir: str = "output/pdfs",
        max_parallel: int = 3,
        chunk_size: int = 8192,
        skip_existing: bool = True,
        verify_ssl: bool = True,
        requests_per_second: float = 2.0,
        min_delay: float = 0.5,
        log_level: str = "INFO",
        log_file: str = None,
    ):
        """
        初始化下载器

        Args:
            output_dir: 输出目录 (默认: output/pdfs)
            max_parallel: 并行下载数 (默认: 3)
            chunk_size: 下载块大小字节 (默认: 8192)
            skip_existing: 跳过已存在的文件 (默认: true)
            verify_ssl: 验证 SSL 证书 (默认: true)
            requests_per_second: 每秒最大请求数 (默认: 2.0)
            min_delay: 请求间最小延迟秒数 (默认: 0.5)
            log_level: 日志级别
            log_file: 日志文件路径
        """
        setup_logging(level=log_level, log_file=log_file)
        self.logger = get_logger()

        self.output_dir = Path(output_dir)
        ensure_dir(self.output_dir)

        self.chunk_size = chunk_size
        self.skip_existing = skip_existing
        self.verify_ssl = verify_ssl
        self.max_parallel = max_parallel

        self.rate_limiter = RateLimiter(requests_per_second, min_delay)
        self.session = requests.Session()

    def _get_pdf_url(self, arxiv_id: str) -> str:
        """获取 PDF URL"""
        normalized_id = parse_arxiv_id(arxiv_id)
        return f"https://arxiv.org/pdf/{normalized_id}.pdf"

    def _generate_filename(self, paper: Dict[str, Any]) -> str:
        """生成文件名"""
        arxiv_id = paper.get("arxiv_id", "unknown")
        title = paper.get("title", "paper")
        title_slug = slugify(title, max_length=60)
        return sanitize_filename(f"{arxiv_id}_{title_slug}.pdf")

    def download_by_id(
        self,
        arxiv_id: str,
        filename: str = None,
        paper_metadata: Dict[str, Any] = None,
    ) -> Optional[Path]:
        """
        通过 arXiv ID 下载论文

        Args:
            arxiv_id: arXiv ID
            filename: 输出文件名，如 None 则自动生成
            paper_metadata: 论文元数据（用于生成文件名）

        Returns:
            下载的文件路径，失败返回 None
        """
        normalized_id = parse_arxiv_id(arxiv_id)
        pdf_url = self._get_pdf_url(normalized_id)

        # 确定文件名
        if not filename:
            if paper_metadata:
                filename = self._generate_filename(paper_metadata)
            else:
                filename = f"{normalized_id}.pdf"

        filepath = self.output_dir / filename

        # 检查是否已存在
        if self.skip_existing and filepath.exists():
            self.logger.debug(f"文件已存在，跳过: {filepath}")
            return filepath

        self.logger.info(f"下载: {arxiv_id} -> {filename}")

        try:
            self.rate_limiter.wait()

            response = self.session.get(
                pdf_url,
                stream=True,
                verify=self.verify_ssl,
                timeout=60,
            )
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            with open(filepath, "wb") as f:
                if total_size > 0:
                    with tqdm(
                        desc=filename,
                        total=total_size,
                        unit="iB",
                        unit_scale=True,
                        unit_divisor=1024,
                        leave=False,
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=self.chunk_size):
                            size = f.write(chunk)
                            pbar.update(size)
                else:
                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        f.write(chunk)

            self.logger.info(f"下载完成: {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"下载失败 {arxiv_id}: {e}")
            if filepath.exists():
                filepath.unlink()
            return None

    def download_batch(
        self,
        papers: List[Dict[str, Any]],
        skip_existing: bool = None,
    ) -> Dict[str, Any]:
        """
        批量下载论文

        Args:
            papers: 论文元数据列表
            skip_existing: 是否跳过已存在的文件

        Returns:
            下载结果统计
        """
        if skip_existing is not None:
            self.skip_existing = skip_existing

        results = {
            "total": len(papers),
            "success": [],
            "failed": [],
            "skipped": [],
        }

        # 先检查哪些已存在
        to_download = []
        for paper in papers:
            arxiv_id = paper.get("arxiv_id")
            if not arxiv_id:
                continue

            filename = self._generate_filename(paper)
            filepath = self.output_dir / filename

            if self.skip_existing and filepath.exists():
                results["skipped"].append({"arxiv_id": arxiv_id, "filepath": str(filepath)})
            else:
                to_download.append(paper)

        self.logger.info(f"总共 {len(papers)} 篇，跳过 {len(results['skipped'])} 篇，需下载 {len(to_download)} 篇")

        # 并行下载
        if to_download:
            with ThreadPoolExecutor(max_workers=self.max_parallel) as executor:
                futures = {}

                for paper in to_download:
                    arxiv_id = paper.get("arxiv_id")
                    future = executor.submit(self.download_by_id, arxiv_id, paper_metadata=paper)
                    futures[future] = arxiv_id

                for future in tqdm(
                    as_completed(futures),
                    total=len(futures),
                    desc="下载进度",
                ):
                    arxiv_id = futures[future]
                    try:
                        filepath = future.result()
                        if filepath:
                            results["success"].append({"arxiv_id": arxiv_id, "filepath": str(filepath)})
                        else:
                            results["failed"].append(arxiv_id)
                    except Exception as e:
                        self.logger.error(f"下载任务失败 {arxiv_id}: {e}")
                        results["failed"].append(arxiv_id)

        self.logger.info(f"下载统计: 成功={len(results['success'])}, 失败={len(results['failed'])}, 跳过={len(results['skipped'])}")
        return results


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="arXiv 论文下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 下载单个论文
  python download.py --id 2301.01234

  # 下载多个论文
  python download.py --id 2301.01234 --id 2302.05678

  # 从 ID 列表文件下载
  python download.py --id-list ids.txt

  # 从元数据文件下载
  python download.py --metadata results.json

  # 指定输出目录
  python download.py --id 2301.01234 --output-dir my_papers/
        """
    )

    # 输入源（多选一）
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--id", action="append", dest="arxiv_ids", help="arXiv ID（可多次指定）")
    input_group.add_argument("--id-list", help="包含 arXiv ID 列表的文本文件")
    input_group.add_argument("--metadata", help="包含论文元数据的 JSON 文件")

    # 输出选项
    parser.add_argument("--output-dir", "-o", default="output/pdfs", help="输出目录 (默认: output/pdfs)")
    parser.add_argument("--skip-existing", action="store_true", default=None, help="跳过已存在的文件 (默认)")
    parser.add_argument("--no-skip-existing", action="store_false", dest="skip_existing", help="覆盖已存在的文件")

    # 下载控制
    parser.add_argument("--parallel", type=int, default=3, help="并行下载数 (默认: 3)")
    parser.add_argument("--chunk-size", type=int, default=8192, help="下载块大小字节 (默认: 8192)")
    parser.add_argument("--verify-ssl", action="store_true", default=True, help="验证 SSL 证书 (默认: true)")
    parser.add_argument("--no-verify-ssl", action="store_false", dest="verify_ssl", help="不验证 SSL 证书")

    # 速率限制
    parser.add_argument("--requests-per-second", type=float, default=2.0, help="每秒最大请求数 (默认: 2.0)")
    parser.add_argument("--min-delay", type=float, default=0.5, help="请求间最小延迟秒数 (默认: 0.5)")

    # 日志
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="日志级别 (默认: INFO)")
    parser.add_argument("--log-file", help="日志文件路径")

    args = parser.parse_args()

    # 初始化下载器
    downloader = PaperDownloader(
        output_dir=args.output_dir,
        max_parallel=args.parallel,
        chunk_size=args.chunk_size,
        skip_existing=args.skip_existing if args.skip_existing is not None else True,
        verify_ssl=args.verify_ssl,
        requests_per_second=args.requests_per_second,
        min_delay=args.min_delay,
        log_level=args.log_level,
        log_file=args.log_file,
    )

    logger = get_logger()

    # 收集要下载的论文
    papers = []

    if args.arxiv_ids:
        for arxiv_id in args.arxiv_ids:
            papers.append({"arxiv_id": parse_arxiv_id(arxiv_id)})

    elif args.id_list:
        id_list_path = Path(args.id_list)
        if not id_list_path.exists():
            logger.error(f"ID 列表文件不存在: {args.id_list}")
            return 1

        with open(id_list_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    papers.append({"arxiv_id": parse_arxiv_id(line)})

    elif args.metadata:
        metadata_path = Path(args.metadata)
        if not metadata_path.exists():
            logger.error(f"元数据文件不存在: {args.metadata}")
            return 1

        metadata = load_json(metadata_path)
        if "papers" in metadata:
            papers = metadata["papers"]
        elif isinstance(metadata, list):
            papers = metadata
        else:
            logger.error("无法识别的元数据格式")
            return 1

    if not papers:
        logger.warning("没有需要下载的论文")
        return 0

    logger.info(f"准备下载 {len(papers)} 篇论文")

    # 执行下载
    results = downloader.download_batch(papers, skip_existing=args.skip_existing)

    # 打印结果
    print("\n==== 下载结果 ====")
    print(f"总计: {results['total']}")
    print(f"成功: {len(results['success'])}")
    print(f"失败: {len(results['failed'])}")
    print(f"跳过: {len(results['skipped'])}")

    if results["failed"]:
        print(f"\n失败的 ID: {', '.join(results['failed'])}")

    return 0 if len(results["failed"]) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
