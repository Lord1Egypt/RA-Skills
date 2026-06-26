#!/usr/bin/env python3
"""
Baidu Maps Place Search - 多维检索 API
Docs: https://api.map.baidu.com/place/v3/multidimensional
"""

import sys
import json
import requests
import os


def search_multidimensional(query: str, region: str, ak: str, **kwargs) -> dict:
    """
    多维检索 - 支持个性化搜索、多语言、丰富排序

    Args:
        query: 检索关键字
        region: 行政区划区域
        ak: API 访问密钥
        **kwargs: 可选参数

    Returns:
        API 原始响应 dict
    """
    url = "https://api.map.baidu.com/api_place_pro/v1/region"

    params = {
        "query": query,
        "region": region,
        "ak": ak,
        "output": "json",
    }

    optional = [
        "scope", "page_size", "page_num", "type",
        "filter", "center", "sort_name", "sort_rule",
        "coord_type", "ret_coordtype", "region_limit",
        "is_light_version", "extensions_adcode",
        "address_result", "photo_show", "from_language", "language",
        "baidu_user_id", "baidu_session_id",
    ]

    for key in optional:
        if key in kwargs and kwargs[key] is not None:
            if isinstance(kwargs[key], bool):
                params[key] = "true" if kwargs[key] else "false"
            else:
                params[key] = kwargs[key]

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    result = response.json()

    if result.get("status") != 0:
        msg = result.get("message", "Unknown error")
        raise Exception(f"API error {result.get('status')}: {msg}")

    return result


def format_results(data: dict, scope: int = 1) -> list:
    """格式化检索结果"""
    results = []

    for poi in data.get("results", []):
        entry = {
            "name": poi.get("name", ""),
            "uid": poi.get("uid", ""),
            "location": poi.get("location", {}),
            "address": poi.get("address", ""),
            "province": poi.get("province", ""),
            "city": poi.get("city", ""),
            "area": poi.get("area", ""),
        }

        if poi.get("telephone"):
            entry["telephone"] = poi["telephone"]

        if scope == 2:
            di = poi.get("detail_info", {})
            if di.get("overall_rating"):
                entry["overall_rating"] = di["overall_rating"]
            if di.get("price"):
                entry["price"] = di["price"]
            if di.get("shop_hours"):
                entry["shop_hours"] = di["shop_hours"]
            if di.get("classified_poi_tag"):
                entry["tag"] = di["classified_poi_tag"]
            if di.get("detail_url"):
                entry["detail_url"] = di["detail_url"]
            if di.get("comment_num"):
                entry["comment_num"] = di["comment_num"]
            if di.get("brand"):
                entry["brand"] = di["brand"]
            if di.get("navi_location"):
                entry["navi_location"] = di["navi_location"]

        results.append(entry)

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py '<JSON>'")
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
        print(f"success parse request body: {params}", file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)

    if "query" not in params or "region" not in params:
        print("Error: 'query' and 'region' are required.")
        sys.exit(1)

    ak = params.get("ak") or os.getenv("BAIDU_AK")
    if not ak:
        raise ValueError("BAIDU_AK environment variable or 'ak' parameter is required")

    search_params = {k: v for k, v in params.items()
                     if k not in ["query", "region", "ak"]}

    try:
        data = search_multidimensional(
            query=params["query"],
            region=params["region"],
            ak=ak,
            **search_params
        )

        scope = int(params.get("scope", 1))
        #formatted = format_results(data, scope=scope)
        formatted = data

        output = {
            "status": 0,
            "message": "ok",
            "query": params["query"],
            "region": params["region"],
            "total": len(formatted),
            "results": formatted
        }

        print(json.dumps(output, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
