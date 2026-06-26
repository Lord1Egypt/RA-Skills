#!/usr/bin/env python3
"""
search_news.py - 搜索 AI Agent 相关新闻

使用 DuckDuckGo 搜索多个关键词，返回原始结果列表。
可配合 blogwatcher 抓取 RSS 源。

用法:
    python search_news.py [--keywords K1,K2,K3] [--time-range 24h] [--output results.json]
"""

import json
import sys
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

# 加载配置文件
SCRIPT_DIR = Path(__file__).parent
SOURCES_FILE = SCRIPT_DIR / "sources.json"

def load_sources():
    """加载数据源配置"""
    if SOURCES_FILE.exists():
        with open(SOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"keywords": [], "rss_sources": []}

def build_ddg_query(keywords, time_range="24h"):
    """构建 DuckDuckGo 搜索 URL"""
    # DDG Lite URL 格式
    base_url = "https://lite.duckduckgo.com/lite/"
    
    # 合并关键词
    query = " OR ".join(keywords[:5])  # DDG 限制最多 5 个关键词
    encoded_query = urllib.parse.quote_plus(query)
    
    # 构建 URL
    url = f"{base_url}?q={encoded_query}"
    
    # 注意：DDG Lite 不支持可靠的时间过滤
    # 如需时间过滤，需要在后续步骤中检查文章日期
    
    return url

def search_ddg(keywords, time_range="24h"):
    """
    执行 DuckDuckGo 搜索
    
    返回格式:
    [
        {"title": "...", "url": "...", "snippet": "...", "source": "ddg"},
        ...
    ]
    """
    url = build_ddg_query(keywords, time_range)
    
    # 返回 URL，由调用方使用 web_fetch 工具抓取
    # 这里不直接执行 HTTP 请求，保持与 OpenClaw 工具链兼容
    
    return {
        "search_url": url,
        "keywords": keywords,
        "time_range": time_range,
        "timestamp": datetime.now().isoformat(),
        "method": "ddg_lite"
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="搜索 AI Agent 新闻")
    parser.add_argument("--keywords", type=str, default="", 
                        help="逗号分隔的关键词列表")
    parser.add_argument("--time-range", type=str, default="24h",
                        help="时间范围 (24h, 7d, 30d)")
    parser.add_argument("--output", type=str, default="",
                        help="输出文件路径")
    parser.add_argument("--config", type=str, default="",
                        help="配置文件路径 (覆盖默认 sources.json)")
    
    args = parser.parse_args()
    
    # 加载配置
    sources = load_sources()
    
    # 命令行关键词覆盖配置
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
    else:
        keywords = sources.get("keywords", [])
    
    time_range = args.time_range or sources.get("filters", {}).get("time_range", "24h")
    
    # 执行搜索
    result = search_ddg(keywords, time_range)
    
    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"结果已保存到 {args.output}")
    else:
        print(output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
