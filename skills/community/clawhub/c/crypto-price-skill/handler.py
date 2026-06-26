"""
Crypto Price Skill - Get Cryptocurrency Prices
Powered by OpenClaw + SkillPay
"""

import json
import requests
import re

# SkillPay Configuration
SKILLPAY_API_KEY = "sk_93c5ff38cc3e6112623d361fffcc5d1eb1b5844eac9c40043b57c0e08f91430e"
PRICE_USDT = "0.001"
SKILLPAY_API_URL = "https://skillpay.me/api/v1/billing"

# CoinGecko ID mapping
CRYPTO_MAP = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "solana": "solana", "sol": "solana",
    "binance": "binancecoin", "bnb": "binancecoin",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "ripple": "ripple", "xrp": "ripple",
    "cardano": "cardano", "ada": "cardano",
    "polkadot": "polkadot", "dot": "polkadot",
    "avalanche": "avalanche-2", "avax": "avalanche-2",
    "chainlink": "chainlink", "link": "chainlink",
    "polygon": "matic-network", "matic": "matic-network",
    "litecoin": "litecoin", "ltc": "litecoin",
    "uniswap": "uniswap", "uni": "uniswap",
    "cosmos": "cosmos", "atom": "cosmos",
}

def charge_user(user_id: str) -> dict:
    """Charge user via SkillPay"""
    try:
        payload = {
            "api_key": SKILLPAY_API_KEY,
            "user_id": user_id,
            "amount": PRICE_USDT,
            "skill_id": SKILL_ID, "currency": "USDT",
            "description": "Crypto price query"
        }
            headers = {"Content-Type": "application/json", "X-API-Key": SKILLPAY_API_KEY}
        response = requests.post(f"{SKILLPAY_API_URL}/charge", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": True, "demo": True, "error": str(e)}

def get_crypto_price(crypto: str) -> dict:
    """Get crypto price from CoinGecko"""
    try:
        coin_id = CRYPTO_MAP.get(crypto.lower(), crypto.lower())
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if coin_id in data:
                price_data = data[coin_id]
                return {
                    "crypto": coin_id,
                    "price_usd": f"${price_data.get('usd', 0):,.2f}",
                    "change_24h": f"{price_data.get('usd_24h_change', 0):.2f}%"
                }
        return {"error": f"Crypto '{crypto}' not found"}
    except Exception as e:
        return {"error": str(e)}

def get_top_coins() -> dict:
    """Get top 10 cryptocurrencies"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            coins = []
            for coin in data:
                coins.append({
                    "name": coin.get("name"),
                    "symbol": coin.get("symbol").upper(),
                    "price": f"${coin.get('current_price', 0):,.2f}",
                    "change_24h": f"{coin.get('price_change_percentage_24h', 0):.2f}%"
                })
            return {"coins": coins, "count": len(coins)}
        return {"error": "Could not fetch data"}
    except Exception as e:
        return {"error": str(e)}

def handle(input_text: str, user_id: str = "default") -> dict:
    """Main handler"""
    crypto = extract_crypto(input_text)
    
    charge_result = charge_user(user_id)
    
    if not charge_result.get("success") and not charge_result.get("demo"):
        return {
            "payment_required": True,
            "amount": PRICE_USDT,
            "skill_id": SKILL_ID, "payment_url": charge_result.get("payment_url", "https://skillpay.me")
        }
    
    if "top" in input_text.lower() or "list" in input_text.lower() or "all" in input_text.lower():
        result = get_top_coins()
    elif crypto:
        result = get_crypto_price(crypto)
    else:
        return {"error": "Please specify a crypto", "usage": "Example: 'Bitcoin price' or 'Top cryptos'"}
    
    result["payment_status"] = "free_demo" if charge_result.get("demo") else "paid"
    return result

def extract_crypto(text: str) -> str:
    """Extract crypto name from input"""
    text = text.lower()
    for key in CRYPTO_MAP:
        if key in text:
            return CRYPTO_MAP[key]
    
    # Try to extract any word that might be a crypto
    words = text.replace('price', '').replace('value', '').strip().split()
    if words:
        return words[0]
    return ""

if __name__ == "__main__":
    import sys
    user_input = sys.argv[1] if len(sys.argv) > 1 else input("Crypto: ")
    user_id = sys.argv[2] if len(sys.argv) > 2 else "cli"
    print(json.dumps(handle(user_input, user_id), indent=2, ensure_ascii=False))
