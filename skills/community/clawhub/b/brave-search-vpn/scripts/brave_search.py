import os
import requests
import json
import argparse
from typing import Any, Optional, Union

def to_bool(value: Any, default: bool = False) -> bool:
    """健壮的布尔值转换器，支持 1, '1', 'true', 'TRUE', 'yes' 等"""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        val_lower = value.strip().lower()
        if val_lower in ('true', '1', 'yes', 'y', 't'):
            return True
        if val_lower in ('false', '0', 'no', 'n', 'f'):
            return False
    return default

def to_int(value: Any, default: int, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """健壮的整数转换器，支持边界矫正"""
    try:
        val = int(value)
    except (TypeError, ValueError):
        val = default
    
    if min_val is not None:
        val = max(min_val, val)
    if max_val is not None:
        val = min(max_val, val)
    return val

def run_brave_search(
    q: str,
    country: str = "CN",
    search_lang: str = "zh-hans",
    count: Union[int, str] = 20,
    offset: Union[int, str] = 0,
    safesearch: str = "moderate",
    freshness: Optional[str] = None,
    text_decorations: Union[bool, str] = True,
    spellcheck: Union[bool, str] = True,
    result_filter: Optional[str] = None,
    goggles: Optional[str] = None,
    extra_snippets: Union[bool, str] = False
) -> str:
    """
    执行 Brave 搜索并返回解析后的精简 JSON 结果（包含网页、新闻、视频）。
    """
    # 1. 验证环境变量
    api_key = os.environ.get("BRAVE_SEARCH_API_KEY")
    proxy_port = os.environ.get("HTTP_PROXY_PORT")
    
    if not api_key:
        return json.dumps({"error": "BRAVE_SEARCH_API_KEY environment variable is not set."})
    if not proxy_port:
        return json.dumps({"error": "HTTP_PROXY_PORT environment variable is not set."})

    # 2. 配置代理
    proxies = {
        "http": f"http://127.0.0.1:{proxy_port}",
        "https": f"http://127.0.0.1:{proxy_port}"
    }

    # 3. 参数校验与类型矫正
    params = {
        "q": q,
        "country": country,
        "search_lang": search_lang,
        "count": to_int(count, 20, min_val=1, max_val=20),
        "offset": to_int(offset, 0, min_val=0, max_val=9),
        "safesearch": safesearch if safesearch in ["off", "moderate", "strict"] else "moderate",
        "text_decorations": 1 if to_bool(text_decorations) else 0,
        "spellcheck": 1 if to_bool(spellcheck) else 0,
    }
    
    # 可选参数
    if freshness: params["freshness"] = freshness
    if result_filter: params["result_filter"] = result_filter
    if goggles: params["goggles"] = goggles
    if to_bool(extra_snippets): params["extra_snippets"] = 1

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }

    # 4. 发起请求
    try:
        url = "https://api.search.brave.com/res/v1/web/search"
        response = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=15)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        return json.dumps({"error": f"Search request failed: {str(e)}"})

    # 5. 结果解析与精简
    parsed_result = {
        "query": raw_data.get("query", {}).get("original", q),
    }
    
    if raw_data.get("query", {}).get("altered"):
        parsed_result["corrected_query"] = raw_data["query"]["altered"]

    # --- 提取网页结果 (Web) ---
    web_results = raw_data.get("web", {}).get("results", [])
    if web_results:
        parsed_result["web"] = []
        for item in web_results:
            clean_item = {
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
            }
            if item.get("page_age"):
                clean_item["published_time"] = item.get("page_age")
            elif item.get("age"):
                clean_item["age"] = item.get("age")
            if item.get("extra_snippets"):
                clean_item["extra_snippets"] = item.get("extra_snippets")
                
            parsed_result["web"].append(clean_item)

    # --- 提取新闻结果 (News) ---
    news_results = raw_data.get("news", {}).get("results", [])
    if news_results:
        parsed_result["news"] = []
        for item in news_results:
            clean_item = {
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
            }
            if item.get("age"):
                clean_item["age"] = item.get("age")
            
            profile = item.get("profile", {})
            if profile and profile.get("name"):
                clean_item["source"] = profile.get("name")
                
            parsed_result["news"].append(clean_item)

    # --- 提取视频结果 (Videos) ---
    video_results = raw_data.get("videos", {}).get("results", [])
    if video_results:
        parsed_result["videos"] = []
        for item in video_results:
            clean_item = {
                "title": item.get("title"),
                "url": item.get("url"),
            }
            if item.get("description"):
                clean_item["description"] = item.get("description")
            if item.get("age"):
                clean_item["age"] = item.get("age")
                
            vid_meta = item.get("video", {})
            if vid_meta:
                if vid_meta.get("duration"):
                    clean_item["duration"] = vid_meta.get("duration")
                if vid_meta.get("creator"):
                    clean_item["creator"] = vid_meta.get("creator")
                if vid_meta.get("views"):
                    clean_item["views"] = vid_meta.get("views")
                    
            parsed_result["videos"].append(clean_item)

    # 6. 返回结果
    return json.dumps(parsed_result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brave Web Search CLI Wrapper")
    parser.add_argument("--q", required=True, type=str, help="Search query")
    parser.add_argument("--country", type=str, default="CN", help="Country code")
    parser.add_argument("--search_lang", type=str, default="zh-hans", help="Search language")
    parser.add_argument("--count", type=str, default="20", help="Max results count (1-20)")
    parser.add_argument("--offset", type=str, default="0", help="Pagination offset (0-9)")
    parser.add_argument("--safesearch", type=str, default="moderate", help="Adult content filter (off/moderate/strict)")
    parser.add_argument("--freshness", type=str, default=None, help="Time filter (pd/pw/pm/py)")
    parser.add_argument("--text_decorations", type=str, default="true", help="Include highlight markers")
    parser.add_argument("--spellcheck", type=str, default="true", help="Auto-correct query")
    parser.add_argument("--result_filter", type=str, default=None, help="Filter result types (comma-separated)")
    parser.add_argument("--goggles", type=str, default=None, help="Custom ranking filter")
    parser.add_argument("--extra_snippets", type=str, default="false", help="Get extra snippets per result")

    args = parser.add_argument_args = parser.parse_args()

    result = run_brave_search(
        q=args.q,
        country=args.country,
        search_lang=args.search_lang,
        count=args.count,
        offset=args.offset,
        safesearch=args.safesearch,
        freshness=args.freshness,
        text_decorations=args.text_decorations,
        spellcheck=args.spellcheck,
        result_filter=args.result_filter,
        goggles=args.goggles,
        extra_snippets=args.extra_snippets
    )
    
    # 打印到标准输出，供调用方（LLM或管道）捕获
    print(result)