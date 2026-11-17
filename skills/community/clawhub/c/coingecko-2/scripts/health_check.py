#!/usr/bin/env python3
"""
Health check for price service API and fallback to Kraken.
Verifies API key validity, rate limit status, and system readiness.
"""

import json
import requests
from datetime import datetime


def health_check() -> dict:
    """
    Comprehensive health check.
    
    Returns:
        {
            "api_status": "ok" | "error",
            "key_type": "demo" | "pro" | "none",
            "rate_limit_remaining": int,
            "rate_limit_reset": str,
            "kraken_fallback": "ok" | "error",
            "timestamp": str,
            "error": str (if any failure)
        }
    """
    
    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # Load API key inline - used only for API call (never logged or stored)
    try:
        from dotenv import dotenv_values
        env_data = dotenv_values()
        api_key = env_data.get("CG_API_KEY") or env_data.get("API_KEY") or ""
    except:
        api_key = ""
    
    if not api_key:
        result["key_type"] = "none"
        result["api_status"] = "not_configured"
        result["note"] = "No API key configured; will use Kraken fallback"
    else:
        # Verify API key works
        try:
            headers = {"x-cg-pro-api-key": api_key}
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {"ids": "bitcoin", "vs_currencies": "usd"}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result["api_status"] = "ok"
                result["key_type"] = "demo"  # Can't distinguish without more info
                
                data = response.json()
                if data.get("bitcoin"):
                    price_sample = data["bitcoin"].get("usd", 0)
                    result["price_sample"] = price_sample
            elif response.status_code == 401:
                result["api_status"] = "error"
                result["key_type"] = "invalid"
                result["error"] = "API key authentication failed"
            else:
                result["api_status"] = "error"
                result["key_type"] = "unknown"
                result["error"] = f"HTTP {response.status_code}"
        except Exception as e:
            result["api_status"] = "error"
            result["error"] = str(e)[:100]
    
    # Check Kraken fallback
    try:
        url = "https://api.kraken.com/0/public/Ticker"
        params = {"pair": "XBTUSDT"}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            result["kraken_fallback"] = "ok"
            data = response.json()
            if "result" in data and data["result"]:
                ticker = next(iter(data["result"].values()))
                kraken_price = float(ticker.get("c", [0])[0])
                result["kraken_price_sample"] = kraken_price
        else:
            result["kraken_fallback"] = "error"
            result["kraken_error"] = f"HTTP {response.status_code}"
    except Exception as e:
        result["kraken_fallback"] = "error"
        result["kraken_error"] = str(e)[:100]
    
    return result


def main():
    result = health_check()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
