#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站视频批量提取脚本
支持多视频并行处理，自动去重，结果汇总
"""

import argparse
import json
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from get_video_content import BilibiliExtractor


class BatchExtractor:
    """批量提取器"""

    def __init__(self, max_workers: int = 3, delay: float = 1.0):
        self.max_workers = max_workers
        self.delay = delay
        self.extractor = BilibiliExtractor()
        self.results = []
        self.errors = []

    def parse_urls(self, input_path: str) -> List[str]:
        """从文件或字符串解析URL列表"""
        urls = []

        if os.path.exists(input_path):
            # 从文件读取
            with open(input_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        urls.append(line)
        else:
            # 逗号分隔的字符串
            urls = [u.strip() for u in input_path.split(',') if u.strip()]

        # 去重
        return list(dict.fromkeys(urls))

    def process_single(self, url: str, mode: str) -> Dict[str, Any]:
        """处理单个视频"""
        video_id = self.extractor.extract_video_id(url)

        if not video_id:
            return {
                "url": url,
                "error": "无法解析视频ID",
                "success": False
            }

        try:
            # 使用摘要模式加快速度
            extract_mode = "summary" if mode == "fast" else "full"
            data = self.extractor.extract(url, mode=extract_mode)

            return {
                "url": url,
                "video_id": video_id,
                "title": data.get("info", {}).get("title", ""),
                "owner": data.get("info", {}).get("owner", {}).get("name", ""),
                "stat": data.get("info", {}).get("stat", {}),
                "data": data,
                "success": True
            }
        except Exception as e:
            return {
                "url": url,
                "video_id": video_id,
                "error": str(e),
                "success": False
            }

    def run(self, urls: List[str], mode: str = "full") -> Dict[str, Any]:
        """执行批量处理"""
        total = len(urls)
        print(f"[信息] 开始批量提取，共 {total} 个视频")
        print(f"[信息] 并发数: {self.max_workers}, 模式: {mode}")
        print("-" * 50)

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.process_single, url, mode): url
                for url in urls
            }

            for i, future in enumerate(as_completed(future_to_url), 1):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result["success"]:
                        self.results.append(result)
                        title = result.get("title", "未知")[:30]
                        stat = result.get("stat", {})
                        views = stat.get("view", 0)
                        print(f"[{i}/{total}] ✅ {title}... | 播放: {views:,}")
                    else:
                        self.errors.append(result)
                        print(f"[{i}/{total}] ❌ {url} | {result.get('error', '未知错误')}")
                except Exception as e:
                    self.errors.append({"url": url, "error": str(e)})
                    print(f"[{i}/{total}] ❌ {url} | 处理异常")

                # 控制请求频率
                time.sleep(self.delay)

        elapsed = time.time() - start_time

        return self.generate_report(elapsed)

    def generate_report(self, elapsed: float) -> Dict[str, Any]:
        """生成汇总报告"""
        report = {
            "summary": {
                "total": len(self.results) + len(self.errors),
                "success": len(self.results),
                "failed": len(self.errors),
                "elapsed_seconds": round(elapsed, 1),
                "timestamp": datetime.now().isoformat()
            },
            "results": self.results,
            "errors": self.errors,
            "ranking": self.generate_ranking()
        }

        return report

    def generate_ranking(self) -> Dict[str, List]:
        """生成排行榜"""
        if not self.results:
            return {"by_views": [], "by_likes": [], "by_favorites": []}

        # 按播放排序
        by_views = sorted(
            self.results,
            key=lambda x: x.get("stat", {}).get("view", 0),
            reverse=True
        )[:10]

        # 按点赞排序
        by_likes = sorted(
            self.results,
            key=lambda x: x.get("stat", {}).get("like", 0),
            reverse=True
        )[:10]

        # 按收藏排序
        by_favorites = sorted(
            self.results,
            key=lambda x: x.get("stat", {}).get("favorite", 0),
            reverse=True
        )[:10]

        return {
            "by_views": [
                {"title": r.get("title"), "owner": r.get("owner"), "views": r.get("stat", {}).get("view", 0)}
                for r in by_views
            ],
            "by_likes": [
                {"title": r.get("title"), "owner": r.get("owner"), "likes": r.get("stat", {}).get("like", 0)}
                for r in by_likes
            ],
            "by_favorites": [
                {"title": r.get("title"), "owner": r.get("owner"), "favorites": r.get("stat", {}).get("favorite", 0)}
                for r in by_favorites
            ]
        }


def main():
    parser = argparse.ArgumentParser(description="B站视频批量提取工具")
    parser.add_argument("--input", "-i", required=True,
                        help="输入文件路径(每行一个URL)或逗号分隔的URL字符串")
    parser.add_argument("--output", "-o", default="batch_result.json",
                        help="输出文件路径")
    parser.add_argument("--mode", "-m", default="fast",
                        choices=["fast", "full"],
                        help="提取模式: fast(摘要) / full(完整)")
    parser.add_argument("--workers", "-w", type=int, default=3,
                        help="并发数 (默认3)")
    parser.add_argument("--delay", "-d", type=float, default=1.0,
                        help="请求间隔(秒) (默认1.0)")

    args = parser.parse_args()

    extractor = BatchExtractor(max_workers=args.workers, delay=args.delay)
    urls = extractor.parse_urls(args.input)

    if not urls:
        print("[错误] 未找到有效URL")
        sys.exit(1)

    result = extractor.run(urls, mode=args.mode)

    # 保存结果
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 打印摘要
    summary = result["summary"]
    print("-" * 50)
    print(f"[完成] 成功: {summary['success']}/{summary['total']} | 耗时: {summary['elapsed_seconds']}s")
    print(f"[保存] 结果已保存至: {args.output}")

    # 打印TOP10
    if result["ranking"]["by_views"]:
        print("\n📊 播放量TOP10:")
        for i, item in enumerate(result["ranking"]["by_views"], 1):
            print(f"  {i}. {item['title'][:25]}... | {item['views']:,}")


if __name__ == "__main__":
    main()
