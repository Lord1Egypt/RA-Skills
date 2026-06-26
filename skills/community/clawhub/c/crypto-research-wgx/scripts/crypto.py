#!/usr/bin/env python3
"""
加密货币价格查询脚本
"""

import requests
import json
import sys

def get_price(coin_id):
    """获取单个币种价格"""
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "cny,usd",
        "include_24hr_change": "true",
        "include_market_cap": "true"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        if coin_id in data:
            info = data[coin_id]
            return {
                "name": coin_id.title(),
                "price_usd": info.get("usd", 0),
                "price_cny": info.get("cny", 0),
                "change_24h": info.get("usd_24h_change", 0),
                "market_cap": info.get("usd_market_cap", 0)
            }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Unknown error"}

def get_top_coins(limit=10):
    """获取市值前N的币种"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        results = []
        for coin in data:
            results.append({
                "rank": coin.get("market_cap_rank"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol").upper(),
                "price_usd": coin.get("current_price"),
                "change_24h": coin.get("price_change_percentage_24h"),
                "market_cap": coin.get("market_cap")
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]

def search_coin(query):
    """搜索币种"""
    url = "https://api.coingecko.com/api/v3/search"
    params = {"query": query}
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        results = []
        for coin in data.get("coins", [])[:5]:
            results.append({
                "id": coin.get("id"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol").upper(),
                "thumb": coin.get("thumb")
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: crypto.py <command> [args]")
        print("Commands: price <coin_id>, top, search <query>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "price" and len(sys.argv) > 2:
        result = get_price(sys.argv[2])
        print(json.dumps(result, indent=2))
    elif cmd == "top":
        result = get_top_coins()
        print(json.dumps(result, indent=2))
    elif cmd == "search" and len(sys.argv) > 2:
        result = search_coin(sys.argv[2])
        print(json.dumps(result, indent=2))
    else:
        print("Unknown command")
