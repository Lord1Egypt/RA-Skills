#!/usr/bin/env python3
"""
设计师情报站 - 统一抓取入口

整合 RSS、API、网页三种抓取方式，输出统一的 JSON 格式供 Agent 使用。

使用方式:
    # 完整抓取（推荐）
    python3 fetch_all.py --all --output /tmp/all_items.json
    
    # 仅 RSS
    python3 fetch_all.py --rss
    
    # 仅 API
    python3 fetch_all.py --api
    
    # 仅网页
    python3 fetch_all.py --web
    
    # 合并已有缓存
    python3 fetch_all.py --merge rss_cache.json api_cache.json web_cache.json
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 缓存目录
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def run_command(cmd: list, description: str) -> tuple[bool, str]:
    """运行抓取命令"""
    print(f"\n{'='*60}")
    print(f"开始：{description}")
    print(f"命令：{' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"✅ {description} 完成")
            return True, result.stdout
        else:
            print(f"❌ {description} 失败：{result.stderr}")
            return False, result.stderr
    
    except subprocess.TimeoutExpired:
        print(f"❌ {description} 超时")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ {description} 异常：{e}")
        return False, str(e)


def fetch_rss() -> list[dict]:
    """抓取 RSS 源"""
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "rss_fetcher.py"),
        "fetch-all",
        "--json"
    ]
    
    success, output = run_command(cmd, "RSS 抓取")
    
    if success:
        # 解析 JSON 输出
        try:
            # 找到 JSON 部分（可能包含日志输出）
            json_start = output.find('[')
            json_end = output.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = output[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"解析 RSS 结果失败：{e}")
    
    return []


def fetch_api() -> list[dict]:
    """抓取 API 源"""
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "api_fetcher.py"),
        "fetch-all",
        "--json"
    ]
    
    success, output = run_command(cmd, "API 抓取")
    
    if success:
        try:
            json_start = output.find('[')
            json_end = output.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = output[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"解析 API 结果失败：{e}")
    
    return []


def fetch_web() -> list[dict]:
    """抓取网页源"""
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "web_fetcher.py"),
        "fetch-all",
        "--json"
    ]
    
    success, output = run_command(cmd, "网页抓取")
    
    if success:
        try:
            json_start = output.find('[')
            json_end = output.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = output[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"解析网页结果失败：{e}")
    
    return []


def merge_items(rss_items: list[dict], api_items: list[dict], 
                web_items: list[dict]) -> list[dict]:
    """合并并去重"""
    all_items = rss_items + api_items + web_items
    
    # 按链接去重
    seen_links = set()
    unique_items = []
    duplicates = 0
    
    for item in all_items:
        link = item.get("link", "")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_items.append(item)
        else:
            duplicates += 1
    
    # 按发布时间排序（最新的在前）
    unique_items.sort(
        key=lambda x: x.get("published", ""),
        reverse=True
    )
    
    print(f"\n{'='*60}")
    print(f"合并结果:")
    print(f"  RSS:  {len(rss_items)} 条")
    print(f"  API:  {len(api_items)} 条")
    print(f"  Web:  {len(web_items)} 条")
    print(f"  总计：{len(all_items)} 条")
    print(f"  去重：{duplicates} 条")
    print(f"  唯一：{len(unique_items)} 条")
    print(f"{'='*60}\n")
    
    return unique_items


def save_output(items: list[dict], output_file: str):
    """保存输出"""
    output_path = Path(output_file)
    if not output_path.is_absolute():
        output_path = CACHE_DIR / output_file
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 输出已保存：{output_path}")
    print(f"   共 {len(items)} 条情报")


def main():
    parser = argparse.ArgumentParser(
        description="设计师情报站 - 统一抓取工具"
    )
    parser.add_argument("--all", action="store_true", help="抓取所有源（RSS + API + 网页）")
    parser.add_argument("--rss", action="store_true", help="仅抓取 RSS")
    parser.add_argument("--api", action="store_true", help="仅抓取 API")
    parser.add_argument("--web", action="store_true", help="仅抓取网页")
    parser.add_argument("--merge", nargs="*", help="合并已有的缓存文件")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    parser.add_argument("--no-dedup", action="store_true", help="不去重")
    
    args = parser.parse_args()
    
    # 默认行为：如果没有指定任何选项，抓取所有
    if not (args.all or args.rss or args.api or args.web or args.merge):
        args.all = True
    
    start_time = datetime.now()
    print(f"\n🚀 设计师情报站抓取工具 v1.4.0")
    print(f"开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    rss_items, api_items, web_items = [], [], []
    
    # 执行抓取
    if args.all or args.rss:
        rss_items = fetch_rss()
    
    if args.all or args.api:
        api_items = fetch_api()
    
    if args.all or args.web:
        web_items = fetch_web()
    
    # 合并已有缓存
    if args.merge:
        from web_fetcher import merge_all_sources
        merged = merge_all_sources(*args.merge)
        if args.output:
            save_output(merged, args.output)
        return merged
    
    # 合并结果
    if args.no_dedup:
        all_items = rss_items + api_items + web_items
    else:
        all_items = merge_items(rss_items, api_items, web_items)
    
    # 保存输出
    if args.output:
        save_output(all_items, args.output)
    else:
        # 默认输出到缓存目录
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"all_items_{timestamp}.json"
        save_output(all_items, output_file)
    
    # 输出统计
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"⏱️  耗时：{duration:.1f} 秒")
    print(f"📊 平均：{duration/max(len(all_items), 1):.2f} 秒/条")
    
    return all_items


if __name__ == "__main__":
    main()
