#!/usr/bin/env python3
"""
GEO Master Pro API Service
使用Tavily API提供品牌AI可见性搜索服务
"""

import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Tavily API配置
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')
if not TAVILY_API_KEY:
    raise ValueError("请设置 TAVILY_API_KEY 环境变量")
TAVILY_API_URL = "https://api.tavily.com/search"

# API认证（简易版：检查X-API-Key头）
API_KEYS = {
    "pro_key_placeholder": {"tier": "pro", "brand_limit": float('inf')},
}

def verify_api_key(api_key):
    """验证API密钥"""
    if api_key in API_KEYS:
        return API_KEYS[api_key]
    return None

def search_brand_tavily(brand_name, max_results=5):
    """使用Tavily搜索品牌信息"""
    try:
        response = requests.post(
            TAVILY_API_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": f"{brand_name} 品牌 AI 服务",
                "search_depth": "basic",
                "max_results": max_results,
                "include_answer": True,
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "data": {
                "query": brand_name,
                "results": data.get("results", []),
                "answer": data.get("answer", ""),
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def calculate_visibility_score(results):
    """根据搜索结果计算机可见性评分（简化版）"""
    if not results:
        return 0
    
    # 简化的评分逻辑
    score = min(len(results) * 15, 100)  # 每个结果+15分，上限100
    return score

@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "geo-api"})

@app.route("/search", methods=["POST"])
def search():
    """搜索品牌可见性"""
    # 验证API Key
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "缺少API密钥"}), 401
    
    tier_info = verify_api_key(api_key)
    if not tier_info:
        return jsonify({"error": "无效的API密钥"}), 401
    
    # 获取请求数据
    data = request.get_json()
    if not data or "brand" not in data:
        return jsonify({"error": "缺少brand参数"}), 400
    
    brand = data["brand"]
    max_results = data.get("max_results", 5)
    
    # 调用Tavily搜索
    result = search_brand_tavily(brand, max_results)
    
    if not result["success"]:
        return jsonify({"error": result["error"]}), 500
    
    # 计算评分
    search_results = result["data"]["results"]
    score = calculate_visibility_score(search_results)
    
    return jsonify({
        "brand": brand,
        "score": score,
        "results_count": len(search_results),
        "tavily_results": search_results[:max_results],
        "answer": result["data"]["answer"],
        "tier": tier_info["tier"],
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
