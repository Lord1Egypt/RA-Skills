#!/usr/bin/env python3
"""测试GEO API服务"""
import requests
import json

API_URL = "http://localhost:8080/search"
TEST_KEY = "pro_key_placeholder"

def test_search(brand="91tokenhub"):
    """测试搜索"""
    resp = requests.post(
        API_URL,
        headers={"X-API-Key": TEST_KEY},
        json={"brand": brand, "max_results": 5}
    )
    print(f"状态码: {resp.status_code}")
    data = resp.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    print("=== 测试GEO API ===")
    test_search()
