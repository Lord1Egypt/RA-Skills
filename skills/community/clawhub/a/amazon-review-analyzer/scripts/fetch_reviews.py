#!/usr/bin/env python3
"""
Amazon评论采集模块
通过RapidAPI获取Amazon产品评论
"""

import requests
import time
import json
from typing import List, Dict, Optional


def fetch_reviews(
    asin: str,
    market: str = "US",
    max_reviews: int = 500,
    rapidapi_key: Optional[str] = None,
    debug: bool = False
) -> Dict:
    """
    获取Amazon产品评论
    
    Args:
        asin: Amazon ASIN
        market: 市场代码 (US/UK/DE/JP/FR/CA/IT/ES)
        max_reviews: 最大评论数量
        rapidapi_key: RapidAPI Key（ None则使用内置免费Key）
        debug: 是否打印调试信息
    
    Returns:
        {
            "product": {...},  # 产品信息
            "reviews": [...],  # 评论列表
            "total_reviews": int,
            "fetched_reviews": int
        }
    """
    
    # RapidAPI 配置
    # 使用内置免费Key（可能会过期，建议用户自备）
    if rapidapi_key is None:
        rapidapi_key = "a3c8a396d7msh1234567890abcdef"  # 这是一个示例Key，实际使用时需要替换
    
    # 市场代码映射
    market_hosts = {
        "US": "amazon.com",
        "UK": "amazon.co.uk",
        "DE": "amazon.de",
        "JP": "amazon.co.jp",
        "FR": "amazon.fr",
        "CA": "amazon.ca",
        "IT": "amazon.it",
        "ES": "amazon.es"
    }
    
    host = market_hosts.get(market.upper(), "amazon.com")
    
    # 先获取产品信息
    print(f"🔍 正在获取产品信息 (ASIN: {asin}, Market: {market})...")
    product_info = _fetch_product_info(asin, host, rapidapi_key, debug)
    
    # 获取评论
    print(f"📝 正在获取评论 (最多 {max_reviews} 条)...")
    reviews = _fetch_all_reviews(asin, host, rapidapi_key, max_reviews, debug)
    
    print(f"✅ 评论采集完成：共获取 {len(reviews)} 条评论")
    
    return {
        "product": product_info,
        "reviews": reviews,
        "total_reviews": len(reviews),
        "fetched_reviews": len(reviews)
    }


def _fetch_product_info(asin: str, host: str, api_key: str, debug: bool) -> Dict:
    """获取产品基本信息"""
    url = "https://amazon-products-and-reviews.p.rapidapi.com/products/detail"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "amazon-products-and-reviews.p.rapidapi.com"
    }
    
    params = {
        "asin": asin,
        "country": "US"  # 默认US，后续可以改进为动态
    }
    
    if debug:
        print(f"  API URL: {url}")
        print(f"  Params: {params}")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if debug:
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            # 解析产品信息
            product = {
                "asin": asin,
                "title": data.get("title", "Unknown Product"),
                "price": data.get("price", "N/A"),
                "rating": data.get("rating", 0),
                "total_reviews": data.get("reviews_count", 0),
                "image_url": data.get("image", ""),
                "url": f"https://www.{host}/dp/{asin}"
            }
            print(f"  产品: {product['title'][:50]}...")
            print(f"  评分: {product['rating']} | 评论数: {product['total_reviews']}")
            return product
        else:
            print(f"  ⚠️ 获取产品信息失败: HTTP {response.status_code}")
            # 返回基本信息
            return {
                "asin": asin,
                "title": f"Product {asin}",
                "price": "N/A",
                "rating": 0,
                "total_reviews": 0,
                "image_url": "",
                "url": f"https://www.{host}/dp/{asin}"
            }
    except Exception as e:
        print(f"  ⚠️ 获取产品信息异常: {e}")
        return {
            "asin": asin,
            "title": f"Product {asin}",
            "price": "N/A",
            "rating": 0,
            "total_reviews": 0,
            "image_url": "",
            "url": f"https://www.{host}/dp/{asin}"
        }


def _fetch_all_reviews(asin: str, host: str, api_key: str, max_reviews: int, debug: bool) -> List[Dict]:
    """分页获取所有评论"""
    all_reviews = []
    page = 1
    per_page = 50  # RapidAPI通常每次返回50条
    
    while len(all_reviews) < max_reviews:
        reviews = _fetch_reviews_page(asin, host, api_key, page, debug)
        
        if not reviews:
            break  # 没有更多评论了
        
        all_reviews.extend(reviews)
        print(f"  已获取 {len(all_reviews)} 条评论...")
        
        if len(reviews) < per_page:
            break  # 最后一页
        
        page += 1
        time.sleep(1)  # 避免API限流
    
    return all_reviews[:max_reviews]


def _fetch_reviews_page(asin: str, host: str, api_key: str, page: int, debug: bool) -> List[Dict]:
    """获取单页评论"""
    url = "https://amazon-products-and-reviews.p.rapidapi.com/reviews/list"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "amazon-products-and-reviews.p.rapidapi.com"
    }
    
    params = {
        "asin": asin,
        "country": "US",
        "page": page
    }
    
    if debug:
        print(f"  Fetching page {page}...")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            reviews = []
            
            # 解析评论数据（根据实际API返回格式调整）
            raw_reviews = data.get("reviews", data.get("data", []))
            
            for review in raw_reviews:
                reviews.append({
                    "id": review.get("id", ""),
                    "rating": review.get("rating", 0),
                    "title": review.get("title", ""),
                    "body": review.get("body", review.get("content", "")),
                    "author": review.get("author", "Anonymous"),
                    "date": review.get("date", ""),
                    "verified_purchase": review.get("verified_purchase", False),
                    "helpful_votes": review.get("helpful_votes", 0)
                })
            
            return reviews
        else:
            print(f"  ⚠️ 获取评论失败 (page {page}): HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"  ⚠️ 获取评论异常 (page {page}): {e}")
        return []


if __name__ == "__main__":
    # 测试代码
    result = fetch_reviews("B08N5WRWNW", "US", 10, debug=True)
    print(f"\n获取到 {result['total_reviews']} 条评论")
    if result['reviews']:
        print(f"\n第一条评论示例:")
        print(f"  评分: {result['reviews'][0]['rating']}")
        print(f"  标题: {result['reviews'][0]['title']}")
        print(f"  内容: {result['reviews'][0]['body'][:100]}...")
