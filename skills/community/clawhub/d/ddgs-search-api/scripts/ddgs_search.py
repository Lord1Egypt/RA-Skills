#!/usr/bin/env python3
"""
DuckDuckGo Search CLI Tool
使用 ddgs 包执行网络搜索

依赖安装:
    uv pip install ddgs
    或直接运行: uv run ddgs_search.py "query"
"""

import argparse
import json
import os
import sys
from typing import Optional

try:
    from ddgs import DDGS
except ImportError:
    print("Error: ddgs package not found.", file=sys.stderr)
    print("Install it with: uv pip install ddgs", file=sys.stderr)
    print("Or run directly: uv run ddgs_search.py 'query'", file=sys.stderr)
    sys.exit(1)


def get_proxy(cli_proxy: Optional[str] = None) -> Optional[str]:
    """
    按优先级获取代理设置:
    1. 命令行参数
    2. 环境变量 HTTP_PROXY
    3. 环境变量 DDGS_PROXY

    Args:
        cli_proxy: 命令行传入的代理地址

    Returns:
        代理地址字符串或 None
    """
    if cli_proxy:
        return cli_proxy

    # 检查 HTTP_PROXY (requests 库标准环境变量)
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    if http_proxy:
        return http_proxy

    # 检查 DDGS_PROXY (ddgs 库专用环境变量)
    ddgs_proxy = os.environ.get("DDGS_PROXY")
    if ddgs_proxy:
        return ddgs_proxy

    return None


def search_web(
    query: str,
    max_results: int = 10,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    backend: str = "auto",
    proxy: Optional[str] = None,
) -> list:
    """
    执行DuckDuckGo网络搜索

    Args:
        query: 搜索关键词
        max_results: 最大返回结果数 (默认10)
        region: 地区代码 (默认 wt-wt 全球)
        safesearch: 安全搜索级别 (on/moderate/off)
        timelimit: 时间限制 (d/w/m/y 或 None)
        backend: 搜索后端 (auto/html/lite)
        proxy: 代理服务器地址

    Returns:
        搜索结果列表
    """
    ddgs = DDGS(proxy=proxy)
    results = ddgs.text(
        query,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
        backend=backend,
    )
    return list(results)


def search_news(
    query: str,
    max_results: int = 10,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    proxy: Optional[str] = None,
) -> list:
    """
    执行DuckDuckGo新闻搜索

    Args:
        query: 搜索关键词
        max_results: 最大返回结果数 (默认10)
        region: 地区代码
        safesearch: 安全搜索级别
        timelimit: 时间限制
        proxy: 代理服务器地址

    Returns:
        新闻结果列表
    """
    ddgs = DDGS(proxy=proxy)
    results = ddgs.news(
        query,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
    )
    return list(results)


def format_result(result: dict, index: int = 0) -> str:
    output = []
    if index > 0:
        output.append(f"\n{'=' * 60}")

    title = result.get("title", "N/A")
    href = result.get("href", "N/A")
    body = result.get("body", "N/A")

    output.append(f"[{index}] {title}")
    output.append(f"URL: {href}")
    output.append(f"摘要: {body}")

    # 新闻特有字段
    if "date" in result:
        output.append(f"日期: {result['date']}")
    if "source" in result:
        output.append(f"来源: {result['source']}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="DuckDuckGo Search CLI - 网络搜索工具\n\n使用 uv 运行: uv run ddgs_search.py 'query'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  uv run ddgs_search.py "Python tutorial"              # 基本搜索
  uv run ddgs_search.py "AI news" --max-results 5      # 限制结果数量
  uv run ddgs_search.py "tech" --region us-en          # 指定地区
  uv run ddgs_search.py "sports" --timelimit d         # 今日结果
  uv run ddgs_search.py "politics" --news              # 搜索新闻
  uv run ddgs_search.py "query" --json                 # JSON格式输出
  uv run ddgs_search.py "query" --proxy http://1.2.3.4:8080   # 使用代理
        """,
    )

    parser.add_argument("query", help="搜索关键词")
    parser.add_argument(
        "-n", "--max-results", type=int, default=10, help="最大返回结果数 (默认: 10)"
    )
    parser.add_argument(
        "-r",
        "--region",
        default="wt-wt",
        help="地区代码 (默认: wt-wt, 如: us-en, cn-zh)",
    )
    parser.add_argument(
        "-s",
        "--safesearch",
        default="moderate",
        choices=["on", "moderate", "off"],
        help="安全搜索级别 (默认: moderate)",
    )
    parser.add_argument(
        "-t",
        "--timelimit",
        choices=["d", "w", "m", "y"],
        help="时间限制 (d=天, w=周, m=月, y=年)",
    )
    parser.add_argument(
        "-b",
        "--backend",
        default="auto",
        choices=["auto", "html", "lite"],
        help="搜索后端 (默认: auto)",
    )
    parser.add_argument("--news", action="store_true", help="搜索新闻 (默认搜索网页)")
    parser.add_argument("-j", "--json", action="store_true", help="JSON格式输出")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    parser.add_argument(
        "-p",
        "--proxy",
        help="代理服务器地址 (默认优先级: 命令行参数 > HTTP_PROXY环境变量 > DDGS_PROXY环境变量)",
    )

    args = parser.parse_args()

    proxy = get_proxy(args.proxy)

    try:
        if args.news:
            results = search_news(
                query=args.query,
                max_results=args.max_results,
                region=args.region,
                safesearch=args.safesearch,
                timelimit=args.timelimit,
                proxy=proxy,
            )
            search_type = "新闻"
        else:
            results = search_web(
                query=args.query,
                max_results=args.max_results,
                region=args.region,
                safesearch=args.safesearch,
                timelimit=args.timelimit,
                backend=args.backend,
                proxy=proxy,
            )
            search_type = "网页"

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f'\n🔍 DuckDuckGo {search_type}搜索: "{args.query}"')
            print(f"找到 {len(results)} 条结果\n")

            for i, result in enumerate(results, 1):
                print(format_result(result, i))

            if args.verbose:
                print(f"\n{'=' * 60}")
                print(f"搜索参数: region={args.region}, safesearch={args.safesearch}")
                if args.timelimit:
                    print(f"时间限制: {args.timelimit}")

    except KeyboardInterrupt:
        print("\n\n搜索已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
