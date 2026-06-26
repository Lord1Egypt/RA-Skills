#!/usr/bin/env python3
"""web_search — 网页搜索（需 API Key 或使用 DuckDuckGo 免费端点）"""
import sys, os, json, re, urllib.parse, urllib.request, urllib.error
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *

HEADERS = {"User-Agent": "builtin-tools/1.0"}


def search_duckduckgo(query, max_results=10):
    """DuckDuckGo 免费即时搜索（无需 API Key）"""
    params = urllib.parse.urlencode({"q": query, "format": "json", "no_html": "1"})
    url = f"https://api.duckduckgo.com/?{params}"

    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as e:
        output_error(f"DuckDuckGo 请求失败: {e}", EXIT_EXEC_ERROR)

    results = []

    # Abstract 即搜索摘要
    abstract = data.get("Abstract", "")
    abstract_url = data.get("AbstractURL", "")
    abstract_source = data.get("AbstractSource", "")
    if abstract and abstract_url:
        results.append({
            "title": abstract_source or "DuckDuckGo",
            "url": abstract_url,
            "snippet": abstract[:300],
            "source": "abstract",
        })

    # RelatedTopics
    for topic in data.get("RelatedTopics", []):
        if len(results) >= max_results:
            break
        if isinstance(topic, dict):
            text = topic.get("Text", "")
            url = topic.get("FirstURL", "")
            if text and url:
                results.append({
                    "title": text[:100],
                    "url": url,
                    "snippet": text[:300],
                    "source": "related",
                })

    # Results（内联结果）
    for r in data.get("Results", []):
        if len(results) >= max_results:
            break
        text = r.get("Text", "")
        url = r.get("FirstURL", "")
        if text and url:
            results.append({
                "title": text[:100],
                "url": url,
                "snippet": text[:300],
                "source": "inline",
            })

    return results


def search_duckduckgo_html(query, max_results=10):
    """DuckDuckGo HTML 搜索（更多结果，解析轻量 HTML）"""
    params = urllib.parse.urlencode({"q": query})
    url = f"https://html.duckduckgo.com/html/?{params}"

    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        output_error(f"DuckDuckGo HTML 请求失败: {e}", EXIT_EXEC_ERROR)

    results = []
    # DuckDuckGo HTML 结果在 <a class="result__a" href="...">title</a> 和 <a class="result__snippet">text</a>
    # 以及 redirect URL 格式: /l/?uddg=ENCODED_URL
    blocks = re.findall(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>(?:.*?<a[^>]+class="result__snippet"[^>]*>(.*?)</a>)?', html, re.DOTALL)

    for href, title, snippet in blocks:
        if len(results) >= max_results:
            break
        # 解析 redirect URL
        actual_url = href
        if "/l/?uddg=" in href:
            encoded = href.split("uddg=")[-1].split("&")[0]
            actual_url = urllib.parse.unquote(encoded)
        elif href.startswith("//"):
            actual_url = "https:" + href

        clean_title = re.sub(r"<[^>]+>", "", title).strip()
        clean_snippet = re.sub(r"<[^>]+>", "", snippet or "").strip()

        if actual_url and clean_title:
            results.append({
                "title": clean_title[:200],
                "url": actual_url,
                "snippet": clean_snippet[:500] or clean_title,
                "source": "html",
            })

    return results


def search_custom_api(query, api_url, api_key, max_results=10):
    """自定义搜索 API（如 Google Custom Search、Bing等）"""
    # 替换占位符
    actual_url = api_url.replace("{query}", urllib.parse.quote(query))
    actual_url = actual_url.replace("{key}", api_key)
    actual_url = actual_url.replace("{max}", str(max_results))

    req = urllib.request.Request(actual_url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as e:
        output_error(f"API 请求失败: {e}", EXIT_EXEC_ERROR)

    # 尝试通用解析
    results = []
    items = []
    for key in ("items", "results", "hits", "value", "data", "webPages", "organic_results"):
        if key in data:
            items = data[key]
            break
    # 嵌套一层
    if not items and isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                items = v
                break

    for item in items[:max_results]:
        title = item.get("title", item.get("name", item.get("text", "")))
        url = item.get("url", item.get("link", item.get("href", "")))
        snippet = item.get("snippet", item.get("description", item.get("body", "")))
        if url:
            results.append({
                "title": str(title)[:200],
                "url": str(url),
                "snippet": str(snippet)[:500],
                "source": "custom_api",
            })

    return results


def main():
    params = parse_input()
    query = get_param(params, "query", required=True)
    engine = get_param(params, "engine", "duckduckgo")
    max_results = get_param(params, "max_results", 10)

    if engine == "duckduckgo":
        # 先尝试 API，再尝试 HTML（获取更多结果）
        results = search_duckduckgo(query, max_results)
        if not results:
            results = search_duckduckgo_html(query, max_results)
    elif engine == "duckduckgo_html":
        results = search_duckduckgo_html(query, max_results)
    elif engine == "custom":
        api_url = get_param(params, "api_url", required=True)
        api_key = get_param(params, "api_key", required=True)
        results = search_custom_api(query, api_url, api_key, max_results)
    else:
        output_error(f"未知搜索引擎: {engine}（支持: duckduckgo, duckduckgo_html, custom）", EXIT_PARAM_ERROR)

    if not results:
        output_ok({"query": query, "results": [], "total": 0, "message": "未找到结果"})

    output_ok({
        "query": query,
        "engine": engine,
        "results": results,
        "total": len(results),
    })


if __name__ == "__main__":
    main()
