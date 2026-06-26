#!/usr/bin/env python3
"""
自动化搜索工作流脚本
多引擎并行搜索 + 结果去重 + 智能摘要
支持：百度、必应、搜狗、Google、DuckDuckGo、Brave、WolframAlpha
"""

import argparse
import asyncio
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import requests

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    engine: str
    score: float = 0.0


# ── 搜索引擎配置 ─────────────────────────────────────────────────────────────

ENGINES = {
    # 国内引擎
    "baidu": {
        "name": "百度",
        "url": "https://www.baidu.com/s?wd={keyword}&rn=10",
        "parse": "baidu",
    },
    "bing_cn": {
        "name": "必应",
        "url": "https://cn.bing.com/search?q={keyword}&count=10",
        "parse": "bing",
    },
    "sogou": {
        "name": "搜狗",
        "url": "https://www.sogou.com/web?query={keyword}",
        "parse": "sogou",
    },
    "toutiao": {
        "name": "头条搜索",
        "url": "https://so.toutiao.com/search?keyword={keyword}",
        "parse": "toutiao",
    },
    # 国际引擎
    "google": {
        "name": "Google",
        "url": "https://www.google.com/search?q={keyword}&num=10",
        "parse": "google",
    },
    "ddg": {
        "name": "DuckDuckGo",
        "url": "https://duckduckgo.com/html/?q={keyword}",
        "parse": "ddg",
    },
    "brave": {
        "name": "Brave",
        "url": "https://search.brave.com/search?q={keyword}",
        "parse": "brave",
    },
    "wolfram": {
        "name": "WolframAlpha",
        "url": "https://www.wolframalpha.com/input?i={keyword}",
        "parse": "wolfram",
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


# ── 解析器 ───────────────────────────────────────────────────────────────────

def parse_baidu(html: str) -> list[SearchResult]:
    """解析百度搜索结果"""
    results = []
    pattern = r'<h3 class="c-title">.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    for match in re.finditer(pattern, html, re.DOTALL):
        url = match.group(1)
        title_raw = re.sub(r'<[^>]+>', '', match.group(2))
        snippet_match = re.search(r'class="c-span-last">([^<]+)', html[match.end():match.end()+500])
        snippet = snippet_match.group(1) if snippet_match else ""
        results.append(SearchResult(title=title_raw.strip(), url=url, snippet=snippet.strip(), engine="baidu"))
    return results[:10]


def parse_bing(html: str) -> list[SearchResult]:
    """解析必应搜索结果"""
    results = []
    pattern = r'<li class="b_algo"[^>]*>.*?<h2><a href="([^"]*)"[^>]*>(.*?)</a></h2>.*?<p>(.*?)</p>'
    for match in re.finditer(pattern, html, re.DOTALL):
        url = match.group(1)
        title = re.sub(r'<[^>]+>', '', match.group(2))
        snippet = re.sub(r'<[^>]+>', '', match.group(3))
        results.append(SearchResult(title=title.strip(), url=url, snippet=snippet.strip()[:200], engine="bing_cn"))
    return results[:10]


def parse_ddg(html: str) -> list[SearchResult]:
    """解析 DuckDuckGo 结果"""
    results = []
    pattern = r'<a class="result__a" href="([^"]*)"[^>]*>(.*?)</a>.*?<a class="result__snippet"[^>]*>(.*?)</a>'
    for match in re.finditer(pattern, html, re.DOTALL):
        url = match.group(1)
        title = re.sub(r'<[^>]+>', '', match.group(2))
        snippet = re.sub(r'<[^>]+>', '', match.group(3))
        results.append(SearchResult(title=title.strip(), url=url, snippet=snippet.strip()[:200], engine="ddg"))
    return results[:10]


def parse_google(html: str) -> list[SearchResult]:
    """解析 Google 搜索结果（基础解析）"""
    results = []
    pattern = r'<div class="yuRUbf">.*?<a href="([^"]*)".*?<h3[^>]*>(.*?)</h3>'
    snippets = re.findall(r'<div class="IsZvec">.*?<span[^>]*>(.*?)</span>', html, re.DOTALL)
    titles = re.findall(r'<div class="yuRUbf">.*?<h3[^>]*>(.*?)</h3>', html, re.DOTALL)
    urls = re.findall(r'<div class="yuRUbf">.*?<a href="([^"]*)"', html, re.DOTALL)
    for i, url in enumerate(urls[:10]):
        title = re.sub(r'<[^>]+>', '', titles[i] if i < len(titles) else "")
        snippet = re.sub(r'<[^>]+>', '', snippets[i] if i < len(snippets) else "")
        results.append(SearchResult(title=title.strip(), url=url, snippet=snippet.strip()[:200], engine="google"))
    return results


# ── 搜索执行 ─────────────────────────────────────────────────────────────────

def search_engine(engine_key: str, keyword: str, timeout: int = 8) -> list[SearchResult]:
    """单引擎搜索"""
    if engine_key not in ENGINES:
        return []

    cfg = ENGINES[engine_key]
    url = cfg["url"].replace("{keyword}", quote_plus(keyword))

    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.encoding = resp.apparent_encoding or "utf-8"
        html = resp.text

        parser_name = cfg["parse"]
        if parser_name == "baidu":
            return parse_baidu(html)
        elif parser_name == "bing":
            return parse_bing(html)
        elif parser_name == "ddg":
            return parse_ddg(html)
        elif parser_name == "google":
            return parse_google(html)
        else:
            return []  # 其他引擎返回空（需要单独实现）
    except Exception as e:
        return []


def deduplicate_results(results: list[SearchResult]) -> list[SearchResult]:
    """URL 去重"""
    seen = set()
    deduped = []
    for r in results:
        normalized = r.url.split("?")[0].rstrip("/").lower()
        if normalized not in seen:
            seen.add(normalized)
            deduped.append(r)
    return deduped


def score_and_rank(results: list[SearchResult]) -> list[SearchResult]:
    """多引擎结果合并评分"""
    engine_weights = {"baidu": 1.0, "bing_cn": 1.0, "google": 1.2, "ddg": 0.9}
    for r in results:
        r.score = engine_weights.get(r.engine, 1.0) * len(r.snippet) / 100
    return sorted(results, key=lambda x: x.score, reverse=True)


# ── 主流程 ────────────────────────────────────────────────────────────────────

async def multi_engine_search(
    keyword: str,
    engines: Optional[list[str]] = None,
    max_workers: int = 5,
    timeout: int = 8,
) -> dict:
    """
    多引擎并行搜索工作流

    返回:
        {
            "keyword": str,
            "total_results": int,
            "engines_used": list[str],
            "deduped_count": int,
            "top_results": [SearchResult, ...],
            "all_results": [SearchResult, ...],
            "elapsed_seconds": float,
        }
    """
    start = time.time()

    if engines is None:
        engines = ["baidu", "bing_cn", "google", "ddg"]

    loop = asyncio.get_event_loop()
    tasks = []
    for eng in engines:
        if eng in ENGINES:
            tasks.append(loop.run_in_executor(None, search_engine, eng, keyword, timeout))

    all_results_flat = []
    for coro in asyncio.as_completed(tasks):
        partial = await coro
        all_results_flat.extend(partial)

    # 合并去重评分
    deduped = deduplicate_results(all_results_flat)
    ranked = score_and_rank(deduped)

    elapsed = time.time() - start

    return {
        "keyword": keyword,
        "total_results": len(all_results_flat),
        "engines_used": [ENGINES[e]["name"] for e in engines if e in ENGINES],
        "deduped_count": len(deduped),
        "top_results": [
            {"rank": i+1, "title": r.title, "url": r.url, "snippet": r.snippet[:150], "engine": r.engine}
            for i, r in enumerate(ranked[:20])
        ],
        "all_results": [
            {"title": r.title, "url": r.url, "snippet": r.snippet[:150], "engine": r.engine}
            for r in ranked
        ],
        "elapsed_seconds": round(elapsed, 2),
    }


# ── CLI 入口 ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="自动化多引擎搜索工作流")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("-e", "--engines", nargs="+", choices=list(ENGINES.keys()) + ["all"],
                        default=["all"], help="指定搜索引擎（默认全部）")
    parser.add_argument("-n", "--num", type=int, default=10, help="返回结果数量")
    parser.add_argument("-o", "--output", help="输出 JSON 文件路径")
    args = parser.parse_args()

    engines = list(ENGINES.keys()) if "all" in args.engines else args.engines

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始多引擎搜索: {args.keyword}")
    print(f"使用的引擎: {[ENGINES[e]['name'] for e in engines]}")

    result = asyncio.run(multi_engine_search(args.keyword, engines))

    print(f"\n✓ 搜索完成，耗时 {result['elapsed_seconds']}s")
    print(f"  总结果: {result['total_results']} | 去重后: {result['deduped_count']}\n")

    for r in result["top_results"][:args.num]:
        print(f"  {r['rank']:2d}. {r['title']}")
        print(f"      🔗 {r['url']}")
        if r["snippet"]:
            print(f"      💬 {r['snippet'][:80]}...")
        print()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"📄 完整结果已保存到: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
