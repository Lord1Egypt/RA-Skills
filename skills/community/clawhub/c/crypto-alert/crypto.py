#!/usr/bin/env python3
"""
Crypto Alert Skill for OpenClaw
加密貨幣價格監控與提醒
"""

import sys
import requests

# 幣種對照表
CRYPTO_MAP = {
    "比特幣": "BTC",
    "比特": "BTC",
    "btc": "BTC",
    "以太坊": "ETH",
    "以太": "ETH",
    "eth": "ETH",
    "solana": "SOL",
    "sol": "SOL",
    "bnb": "BNB",
    "幣安幣": "BNB",
    "xrp": "XRP",
    "瑞波幣": "XRP",
    "doge": "DOGE",
    "狗狗幣": "DOGE",
    "ada": "ADA",
    "艾達幣": "ADA",
    "dot": "DOT",
    "波卡": "DOT",
}

def get_crypto_price(symbol="BTC"):
    """取得加密貨幣價格"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "lastPrice" in data:
            return {
                "price": float(data["lastPrice"]),
                "change_24h": float(data["priceChangePercent"])
            }
        return None
    except Exception as e:
        return {"error": str(e)}

def get_multiple_prices(symbols):
    """取得多種加密貨幣價格"""
    result = {}
    for symbol in symbols:
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
            response = requests.get(url, timeout=5)
            data = response.json()
            if "lastPrice" in data:
                result[symbol.lower()] = {
                    "usd": float(data["lastPrice"]),
                    "usd_24h_change": float(data["priceChangePercent"])
                }
        except:
            pass
    return result

def analyze_crypto(query):
    """分析加密貨幣查詢"""
    symbol = "BTC"
    for key, value in CRYPTO_MAP.items():
        if key in query:
            symbol = value
            break
    
    data = get_crypto_price(symbol)
    
    if data is None or "error" in data:
        return f"無法取得 {symbol} 的價格數據"
    
    price = data["price"]
    change_24h = data["change_24h"]
    
    change_emoji = "🟢" if change_24h >= 0 else "🔴"
    change_str = f"{change_24h:+.2f}%"
    
    name_map = {
        "BTC": "比特幣",
        "ETH": "以太坊",
        "SOL": "Solana",
        "BNB": "幣安幣",
        "XRP": "瑞波幣",
        "DOGE": "狗狗幣",
        "ADA": "艾達幣",
        "DOT": "波卡",
    }
    name = name_map.get(symbol, symbol)
    
    if price >= 1000:
        price_str = f"${price:,.2f}"
    elif price >= 1:
        price_str = f"${price:.4f}"
    else:
        price_str = f"${price:.6f}"
    
    alert = ""
    if change_24h > 10:
        alert = "\n🔥 暴漲中！"
    elif change_24h < -10:
        alert = "\n📉 大跌中！"
    
    return f"""
💰 **{name} ({symbol})**

現價: **{price_str}**
24小時漲跌幅: {change_emoji} {change_str}
{alert}
"""

def show_top_coins():
    """顯示熱門加密貨幣"""
    coins = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "DOT"]
    data = get_multiple_prices(coins)
    
    if not data:
        return "無法取得加密貨幣數據"
    
    result = "🔥 **熱門加密貨幣**\n\n"
    
    for coin in coins:
        if coin.lower() in data:
            price = data[coin.lower()]["usd"]
            change = data[coin.lower()]["usd_24h_change"]
            
            if price >= 1:
                price_str = f"${price:,.2f}"
            else:
                price_str = f"${price:.6f}"
            
            emoji = "🟢" if change >= 0 else "🔴"
            result += f"{emoji} {coin}: {price_str} ({change:+,.2f}%)\n"
    
    return result

def main():
    if len(sys.argv) < 2:
        print(show_top_coins())
        return
    
    query = " ".join(sys.argv[1:])
    
    if "熱門" in query or "全部" in query or "列表" in query:
        print(show_top_coins())
    else:
        print(analyze_crypto(query))

if __name__ == "__main__":
    main()
