#!/usr/bin/env python3
"""
DuckDuckGo Search Skill for OpenClaw
使用 DuckDuckGo 进行搜索，无需 API Key
支持关键信息提取和 AI 总结

Usage:
    python3 duckduckgo_search.py "搜索关键词" [options]
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Optional, Tuple
import re
import time
from html import unescape

# 配置
DEFAULT_TOP_K = 5
TIMEOUT = 10  # 秒
USER_AGENT = "Mozilla/5.0 (compatible; DuckDuckGo-OpenClaw/1.0)"
MAX_CONTENT_CHARS = 1000  # 单个网页最大提取字符数

# DuckDuckGo API 端点
DDG_HTML_URL = "https://html.duckduckgo.com/html/"


def search_instant(query: str, top_k: int = 5) -> List[Dict]:
    """
    使用 DuckDuckGo Instant API（只返回即时答案，不是完整搜索）
    适合事实性问题
    """
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": "1",
        "skip_disambig": "1"
    }
    
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    
    headers = {
        "User-Agent": USER_AGENT
    }
    
    req = urllib.request.Request(full_url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            results = []
            
            # 提取即时答案
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", query),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("AbstractText", ""),
                    "source": "instant",
                    "type": "abstract"
                })
            
            # 提取相关主题
            related = data.get("RelatedTopics", [])
            for topic in extract_topics(related):
                if len(results) >= top_k:
                    break
                results.append(topic)
            
            return results[:top_k]
            
    except urllib.error.HTTPError as e:
        print(f"⚠️  API 错误：{e.code} - {e.reason}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"⚠️  请求失败：{e}", file=sys.stderr)
        return []


def extract_topics(topics: list, depth: int = 0) -> List[Dict]:
    """递归提取 RelatedTopics"""
    results = []
    for topic in topics:
        if isinstance(topic, dict):
            if "Topics" in topic:
                # 嵌套主题
                results.extend(extract_topics(topic["Topics"], depth + 1))
            else:
                # 普通结果
                text = topic.get("Text", "")
                first_url = topic.get("FirstURL", "")
                result_obj = topic.get("Result", "")
                
                # 清理 HTML
                snippet = re.sub(r'<[^>]+>', '', result_obj).strip() if result_obj else ""
                
                results.append({
                    "title": text or first_url,
                    "url": first_url,
                    "snippet": snippet,
                    "source": "instant",
                    "type": "related"
                })
    return results


def search_html(query: str, top_k: int = 5, fetch_content: bool = False, 
                summarize: bool = False) -> Tuple[List[Dict], Optional[str]]:
    """
    使用 DuckDuckGo HTML 端点（返回完整搜索结果）
    支持内容抓取和总结
    
    Returns:
        (results, summary) - 结果列表和总结文本
    """
    url = DDG_HTML_URL
    
    # 构建请求
    data = urllib.parse.urlencode({"q": query}).encode("utf-8")
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            html = response.read().decode("utf-8")
            results = parse_html_results(html, top_k, fetch_content)
            
            # 如果需要总结
            if summarize and results:
                summary = generate_summary(query, results)
                return results, summary
            
            return results, None
            
    except urllib.error.HTTPError as e:
        print(f"⚠️  HTTP 错误：{e.code} - {e.reason}", file=sys.stderr)
        if e.code == 403:
            print("💡 DuckDuckGo 可能限制了访问，请稍后重试", file=sys.stderr)
        return [], None
    except Exception as e:
        print(f"⚠️  请求失败：{e}", file=sys.stderr)
        return [], None


def parse_html_results(html: str, top_k: int, fetch_content: bool) -> List[Dict]:
    """解析 HTML 搜索结果（简单版本，不依赖外部库）"""
    results = []
    
    # 简单正则提取（生产环境建议用 BeautifulSoup）
    # 匹配结果块
    result_pattern = r'<a[^>]+class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]+)</a>'
    
    for match in re.finditer(result_pattern, html, re.IGNORECASE):
        if len(results) >= top_k:
            break
        
        href = match.group(1)
        title = match.group(2).strip()
        
        # 提取真实 URL
        real_url = extract_real_url(href)
        
        # 提取摘要（简化）
        snippet = ""
        snippet_match = re.search(rf'{re.escape(title)}[^{{}}]*<[^>]*>([^<]+)', html, re.IGNORECASE)
        if snippet_match:
            snippet = snippet_match.group(1).strip()[:200]
        
        results.append({
            "title": title,
            "url": real_url,
            "snippet": snippet,
            "source": "html",
            "type": "search_result"
        })
    
    return results


def extract_real_url(href: str) -> str:
    """从 DuckDuckGo 重定向链接提取真实 URL"""
    try:
        # DuckDuckGo 重定向格式：https://duckduckgo.com/l/?uddg=ENCODED_URL
        if "uddg=" in href:
            parsed = urllib.parse.urlparse(href)
            params = urllib.parse.parse_qs(parsed.query)
            if "uddg" in params:
                return urllib.parse.unquote(params["uddg"][0])
        
        # 如果是直接链接
        if href.startswith("http://") or href.startswith("https://"):
            return href
        
        # 相对链接
        if href.startswith("/"):
            return f"https://duckduckgo.com{href}"
        
        return href
    except:
        return href


def extract_key_info(query: str, results: List[Dict]) -> Dict:
    """
    从搜索结果中提取关键信息
    """
    key_info = {
        "query": query,
        "total_results": len(results),
        "sources": [],
        "topics": [],
        "dates": [],
        "key_entities": []
    }
    
    # 提取来源
    for result in results:
        url = result.get("url", "")
        title = result.get("title", "")
        
        # 提取域名
        try:
            domain = urllib.parse.urlparse(url).netloc
            if domain and domain not in key_info["sources"]:
                key_info["sources"].append(domain)
        except:
            pass
        
        # 提取日期（简单正则）
        date_pattern = r'\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}月\d{1,2}日'
        dates = re.findall(date_pattern, title)
        key_info["dates"].extend(dates)
        
        # 提取关键实体（人名、地名、组织名等）
        # 简单实现：提取引号内内容、专有名词
        entity_pattern = r'[「」""\'\'《》]()|([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)+)|([\\u4e00-\\u9fa5]{2,}(?:局 | 部 | 委 | 国 | 市 | 省))'
        entities = re.findall(entity_pattern, title)
        for entity_group in entities:
            for entity in entity_group:
                if entity and len(entity) > 1:
                    key_info["key_entities"].append(entity)
    
    # 去重
    key_info["sources"] = list(set(key_info["sources"]))
    key_info["key_entities"] = list(set(key_info["key_entities"]))[:10]
    
    return key_info


def generate_summary(query: str, results: List[Dict]) -> str:
    """
    生成搜索结果的简要总结
    """
    if not results:
        return "⚠️  未找到相关信息"
    
    # 提取关键信息
    key_info = extract_key_info(query, results)
    
    summary = f"\n📋 关键信息摘要\n"
    summary += "=" * 60 + "\n\n"
    
    # 搜索主题
    summary += f"🔍 搜索主题：{query}\n\n"
    
    # 来源分析
    summary += f"📰 信息来源 ({len(key_info['sources'])} 个):\n"
    for source in key_info["sources"][:5]:
        summary += f"   • {source}\n"
    summary += "\n"
    
    # 时间信息
    if key_info["dates"]:
        summary += f"📅 时间信息:\n"
        for date in key_info["dates"][:3]:
            summary += f"   • {date}\n"
        summary += "\n"
    
    # 关键实体
    if key_info["key_entities"]:
        summary += f"🏷️ 关键实体:\n"
        for entity in key_info["key_entities"][:5]:
            summary += f"   • {entity}\n"
        summary += "\n"
    
    # 结果概览
    summary += f"📊 结果概览:\n"
    summary += f"   共找到 {len(results)} 条相关信息\n"
    
    # 提取标题关键词
    titles = [r.get("title", "") for r in results[:5]]
    if titles:
        summary += f"   主要关注点:\n"
        for title in titles:
            # 简化标题（去除副标题）
            simple_title = re.split(r'[|:——-]', title)[0].strip()
            summary += f"   - {simple_title}\n"
    
    return summary


def format_output(results: List[Dict], json_output: bool = False, 
                summary: Optional[str] = None, include_key_info: bool = False) -> str:
    """格式化输出"""
    if json_output:
        output_data = {"results": results}
        if summary:
            output_data["summary"] = summary
        return json.dumps(output_data, ensure_ascii=False, indent=2)
    
    if not results:
        return "⚠️  未找到搜索结果"
    
    output = f"\n🔍 DuckDuckGo 搜索结果 ({len(results)} 条)\n"
    output += "=" * 60 + "\n\n"
    
    # 先显示总结（如果有）
    if summary:
        output += summary + "\n"
    
    # 显示详细结果
    output += "📄 详细信息:\n"
    output += "-" * 60 + "\n\n"
    
    for i, result in enumerate(results, 1):
        title = result.get("title", "无标题")
        url = result.get("url", "")
        snippet = result.get("snippet", "")[:200]
        source = result.get("source", "unknown")
        
        output += f"{i}. {title}\n"
        output += f"   🔗 {url}\n"
        if snippet:
            output += f"   📝 {snippet}...\n"
        output += f"   📊 来源：{source}\n"
        output += "\n"
    
    return output


def main():
    parser = argparse.ArgumentParser(
        description="DuckDuckGo Search Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 duckduckgo_search.py "Python 教程"
  python3 duckduckgo_search.py "AI 新闻" -n 10
  python3 duckduckgo_search.py "天气" --mode html
  python3 duckduckgo_search.py "API" --json
  python3 duckduckgo_search.py "伊朗局势" --summarize  # 带总结
        """
    )
    
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("-n", "--top-k", type=int, default=DEFAULT_TOP_K,
                        help=f"返回结果数量 (默认：{DEFAULT_TOP_K})")
    parser.add_argument("--mode", choices=["instant", "html"], default="html",
                        help="搜索模式：instant=即时 API, html=网页抓取 (默认：html)")
    parser.add_argument("--fetch-content", action="store_true",
                        help="抓取网页内容（仅 html 模式）")
    parser.add_argument("--summarize", action="store_true",
                        help="生成关键信息总结")
    parser.add_argument("--json", action="store_true",
                        help="输出原始 JSON 格式")
    
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    # 执行搜索
    if args.mode == "instant":
        results = search_instant(args.query, args.top_k)
        summary = None
    else:
        results, summary = search_html(
            args.query, 
            args.top_k, 
            args.fetch_content,
            summarize=args.summarize
        )
    
    # 输出结果
    print(format_output(
        results, 
        json_output=args.json,
        summary=summary,
        include_key_info=args.summarize
    ))


if __name__ == "__main__":
    main()
