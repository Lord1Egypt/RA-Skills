#!/usr/bin/env python3
"""
Fetch prices for multiple cryptocurrency assets from CoinGecko API.
"""

import json
import sys
import requests
from pathlib import Path
from fetch_price import get_coingecko_api_key

def get_multi_asset_prices(assets=None, timeout=10):
    """
    Fetch prices for multiple cryptocurrencies.
    
    Args:
        assets: list of CoinGecko asset IDs (lowercase)
        timeout: HTTP timeout in seconds
    
    Returns:
        {
            "success": bool,
            "asset_id": {"price": N, "price_str": "$N.00", ...},
            ...
        }
    """
    
    if assets is None:
        assets = ["bitcoin", "ethereum"]
    
    if isinstance(assets, str):
        assets = [assets]
    
    try:
        api_key = get_coingecko_api_key()
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(assets),
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        
        if api_key:
            params["x_cg_demo_api_key"] = api_key
        
        response = requests.get(url, params=params, timeout=timeout)
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}"
            }
        
        data = response.json()
        result = {"success": True}
        
        for asset_id, asset_data in data.items():
            if "usd" in asset_data:
                price = float(asset_data["usd"])
                change_24h = float(asset_data.get("usd_24h_change", 0))
                
                if change_24h > 0:
                    change_badge = f"▲ {abs(change_24h):.2f}%"
                elif change_24h < 0:
                    change_badge = f"▼ {abs(change_24h):.2f}%"
                else:
                    change_badge = "→ 0.00%"
                
                result[asset_id] = {
                    "price": price,
                    "price_str": f"${price:,.2f}",
                    "change_24h": change_24h,
                    "change_badge": change_badge,
                    "market_cap": asset_data.get("usd_market_cap"),
                    "volume_24h": asset_data.get("usd_24h_vol")
                }
        
        return result
    
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # If called with arguments, use those as asset IDs
    assets = sys.argv[1:] if len(sys.argv) > 1 else ["bitcoin", "ethereum"]
    
    result = get_multi_asset_prices(assets)
    print(json.dumps(result, indent=2))
