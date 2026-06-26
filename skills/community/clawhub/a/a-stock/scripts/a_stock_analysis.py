#!/usr/bin/env python3
"""
A-Stock Analyst - A-share stock analysis engine
Integrated with East Money data, self-select stocks, smart screening, monitoring alerts
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional

# East Money API Config
MX_API_KEY = os.environ.get("MX_API_KEY", "") or os.environ.get("MX_SEARCH_API_KEY", "")
API_BASE = "https://mkapi2.dfcfs.com/finskillshub/api/claw"


class AStockAnalyst:
    """A-Share Stock Analyst Engine"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or MX_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }

    def query_data(self, query: str) -> Dict[str, Any]:
        """Call Miaoxiang Data API"""
        import requests
        url = f"{API_BASE}/query"
        data = {"toolQuery": query}

        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def stock_screen(self, keyword: str, page: int = 1, size: int = 20) -> Dict[str, Any]:
        """Smart Stock Screening"""
        import requests
        url = f"{API_BASE}/stock-screen"
        data = {"keyword": keyword, "pageNo": page, "pageSize": size}

        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_selfselect(self) -> Dict[str, Any]:
        """Query Self-Select Stocks"""
        import requests
        url = f"{API_BASE}/self-select/get"

        try:
            response = requests.post(url, headers=self.headers, timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def manage_selfselect(self, query: str) -> Dict[str, Any]:
        """Manage Self-Select Stocks (Add/Delete)"""
        import requests
        url = f"{API_BASE}/self-select/manage"
        data = {"query": query}

        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def search_news(self, keyword: str) -> Dict[str, Any]:
        """News Search"""
        import requests
        url = f"{API_BASE}/search"
        data = {"keyword": keyword, "pageNo": 1, "pageSize": 10}

        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def analyze_stock(self, code: str) -> Dict[str, Any]:
        """Deep Analysis of a Stock"""
        results = {}

        # 1. Get Basic Info
        basic_info = self.query_data(f"{code} Basic Info")
        results["basic_info"] = basic_info

        # 2. Get Financial Indicators
        financial = self.query_data(f"{code} Financial Indicators")
        results["financial"] = financial

        # 3. Get Money Flow
        money_flow = self.query_data(f"{code} Main Force Money Flow")
        results["money_flow"] = money_flow

        return results


if __name__ == "__main__":
    # Test
    analyst = AStockAnalyst()
    result = analyst.query_data("600519 Latest Price")
    print(result)
