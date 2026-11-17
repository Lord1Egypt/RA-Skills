#!/usr/bin/env python3
"""
Fetch live BTC/USD price from price service API with Kraken fallback.
Supports both Demo (free) and Pro (paid) API keys.
"""

import os
import json
import requests
from pathlib import Path


def fetch_btc_price_coingecko(timeout: int = 10) -> dict:
    """
    Fetch BTC/USD price from price service API.
    
    Returns:
        {
            "price": float,           # e.g., 81267.00
            "price_str": str,         # e.g., "$81,267.00"
            "change_24h": float,      # e.g., -0.22
            "change_badge": str,      # e.g., "▼ 0.22%"
            "badge_type": str,        # "GOOD NEWS", "CAUTION", "BAD NEWS"
            "source": str,            # "price service" or "Kraken"
            "market_cap_usd": float,  # (CoinGecko only)
            "volume_24h_usd": float   # (CoinGecko only)
        }
    """
    try:
        # Load API key inline from dotenv or environment - used only for API call
        try:
            from dotenv import dotenv_values
            env_data = dotenv_values()
            api_key = env_data.get("CG_API_KEY") or env_data.get("API_KEY") or ""
        except:
            api_key = ""
        
        # Construct headers with key only if available (never logged or exposed)
        headers = {}
        if api_key:
            headers["x-cg-pro-api-key"] = api_key
        
        # Fetch from price service API
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            btc = data.get("bitcoin", {})
            
            price = btc.get("usd", 0)
            change_24h = btc.get("usd_24h_change", 0)
            market_cap = btc.get("usd_market_cap", 0)
            volume_24h = btc.get("usd_24h_vol", 0)
            
            # Determine badge
            if change_24h > 0.5:
                badge = f"▲ {abs(change_24h):.2f}%"
                badge_type = "GOOD NEWS"
            elif change_24h < -0.5:
                badge = f"▼ {abs(change_24h):.2f}%"
                badge_type = "BAD NEWS"
            else:
                badge = f"→ {abs(change_24h):.2f}%"
                badge_type = "SIDEWAYS MOVEMENT"
            
            return {
                "success": True,
                "price": price,
                "price_str": f"${price:,.2f}",
                "change_24h": change_24h,
                "change_badge": badge,
                "badge_type": badge_type,
                "source": "price service",
                "market_cap_usd": market_cap,
                "volume_24h_usd": volume_24h
            }
    except Exception as e:
        # Silently fall through to Kraken
        pass
    
    # Fallback: Kraken API (public, no auth required)
    return fetch_btc_price_kraken(timeout)


def fetch_btc_price_kraken(timeout: int = 10) -> dict:
    """
    Fallback: Fetch BTC/USD price from Kraken (public API, no auth).
    """
    try:
        url = "https://api.kraken.com/0/public/Ticker"
        params = {"pair": "XBTUSDT"}
        
        response = requests.get(url, params=params, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                result = data["result"]
                # Kraken returns XBTUSDT under that key
                ticker = next(iter(result.values())) if result else {}
                
                # Extract price (c = close)
                close_price = float(ticker.get("c", [0])[0])
                
                # Extract bid/ask
                bid = float(ticker.get("b", [0])[0])
                ask = float(ticker.get("a", [0])[0])
                
                return {
                    "success": True,
                    "price": close_price,
                    "price_str": f"${close_price:,.2f}",
                    "change_24h": 0,
                    "change_badge": "→ Live",
                    "badge_type": "SIDEWAYS MOVEMENT",
                    "source": "Kraken",
                    "bid": bid,
                    "ask": ask
                }
    except Exception as e:
        pass
    
    # Final fallback
    return {
        "success": False,
        "error": "Unable to fetch BTC price from any source",
        "source": "error"
    }


def main():
    result = fetch_btc_price_coingecko()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
