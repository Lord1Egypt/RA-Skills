#!/usr/bin/env python3
"""
百度 AI 搜索 - 智能搜索生成
联网搜索 + AI 总结 + 来源引用

API: POST https://qianfan.baidubce.com/v2/ai_search/chat/completions
"""

import sys
import json
import os
import requests
from datetime import datetime, timedelta


def baidu_ai_search(api_key, request_body):
    url = "https://qianfan.baidubce.com/v2/ai_search/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=request_body, headers=headers, timeout=120)
    response.raise_for_status()
    result = response.json()

    if "code" in result:
        raise Exception(result.get("message", str(result)))

    return result


def parse_result(result):
    """解析 API 返回结果，提取 AI 回答和参考来源"""
    output = {
        "answer": "",
        "references": [],
        "request_id": result.get("request_id", ""),
        "is_safe": result.get("is_safe", True),
        "usage": result.get("usage", {})
    }

    choices = result.get("choices", [])
    if choices:
        choice = choices[0]
        message = choice.get("message", {})
        output["answer"] = message.get("content", "")

    references = result.get("references", [])
    for ref in references:
        output["references"].append({
            "id": ref.get("id"),
            "title": ref.get("title", ""),
            "url": ref.get("url", ""),
            "content": ref.get("content", ""),
            "date": ref.get("date", ""),
            "type": ref.get("type", "web"),
            "website": ref.get("website", ""),
        })

    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py '<json>'")
        sys.exit(1)

    try:
        parse_data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)

    query = parse_data.get("query")
    if not query:
        print("Error: 'query' is required")
        sys.exit(1)

    count = min(int(parse_data.get("count", 10)), 20)

    # 时间筛选
    freshness = parse_data.get("freshness", "")
    recency_filter = ""
    if freshness == "pd":
        recency_filter = "week"
    elif freshness == "pw":
        recency_filter = "week"
    elif freshness == "pm":
        recency_filter = "month"
    elif freshness == "py":
        recency_filter = "year"
    elif freshness in ("week", "month", "semiyear", "year"):
        recency_filter = freshness

    # 深度搜索
    deep_search = parse_data.get("deep_search", False)

    # 构建请求体
    request_body = {
        "messages": [
            {
                "content": query,
                "role": "user"
            }
        ],
        "stream": False,
        "search_source": "baidu_search_v2",
        "resource_type_filter": [{"type": "web", "top_k": count}],
        "model": "deepseek-v3.2-think",
        "enable_deep_search": deep_search,
        "enable_corner_markers": True,
    }

    if recency_filter:
        request_body["search_recency_filter"] = recency_filter

    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        print("Error: BAIDU_API_KEY must be set in environment")
        sys.exit(1)

    try:
        result = baidu_ai_search(api_key, request_body)
        parsed = parse_result(result)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
