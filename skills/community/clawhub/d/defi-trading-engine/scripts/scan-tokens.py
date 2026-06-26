#!/usr/bin/env python3
"""
Token Scanner — scans for trading opportunities using free APIs.

Usage:
  python3 scan-tokens.py --output candidates.json [--min-score 7.0]

Data Sources:
  - CoinGecko trending coins
  - Volume spike detection
  - Price momentum analysis
  - Liquidity filtering

Output: JSON array of candidate tokens with scores and signals
"""
import json
import urllib.request
import urllib.error
import argparse
import sys
from datetime import datetime, timezone


def fetch_json(url, timeout=15):
    """Fetch JSON from URL with error handling."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read())
    except Exception as e:
        print(f"⚠️ Failed to fetch {url[:60]}... — {e}", file=sys.stderr)
        return None


def load_config():
    """Load trading configuration."""
    try:
        with open("trading-config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ trading-config.json not found, using defaults", file=sys.stderr)
        return {
            "data_sources": {
                "use_coingecko_trending": True,
                "min_liquidity_usd": 50000,
                "min_volume_24h_usd": 100000
            }
        }


def fetch_trending_coins():
    """Fetch trending coins from CoinGecko."""
    trending = fetch_json("https://api.coingecko.com/api/v3/search/trending")
    if not trending or "coins" not in trending:
        return []
    
    symbols = [c["item"]["symbol"] for c in trending["coins"][:10]]
    return symbols


def fetch_market_data(symbols):
    """Fetch detailed market data for given symbols."""
    # Get top 100 coins from CoinGecko
    coins = fetch_json(
        "https://api.coingecko.com/api/v3/coins/markets?"
        "vs_currency=usd&order=market_cap_desc&per_page=100&page=1"
        "&sparkline=false&price_change_percentage=1h,4h,24h,7d"
    )
    
    if not coins:
        return []
    
    # Filter to requested symbols
    filtered = [c for c in coins if c["symbol"].upper() in [s.upper() for s in symbols]]
    
    return filtered


def calculate_volume_spike(coin):
    """Calculate volume spike ratio (24h volume vs market cap)."""
    volume = coin.get("total_volume", 0)
    market_cap = coin.get("market_cap", 1)
    
    if market_cap == 0:
        return 0
    
    # Volume/MCap ratio (higher = more activity)
    return volume / market_cap


def score_candidate(coin, config):
    """Score a candidate token based on signals."""
    score = 0
    signals = []
    
    # Price momentum signals
    change_1h = coin.get("price_change_percentage_1h_in_currency") or 0
    change_4h = coin.get("price_change_percentage_4h_in_currency") or 0
    change_24h = coin.get("price_change_percentage_24h") or 0
    
    # Momentum up (1h, 4h, 24h all positive)
    if change_1h > 0 and change_4h > 0 and change_24h > 0:
        score += 3
        signals.append("momentum_up")
    
    # Strong 24h move (>5%)
    if abs(change_24h) > 5:
        score += 2
        signals.append("strong_move_24h")
    
    # Volume spike
    vol_spike = calculate_volume_spike(coin)
    if vol_spike > 0.2:  # Volume > 20% of market cap
        score += 2
        signals.append("volume_spike")
    
    # Liquidity filter
    market_cap = coin.get("market_cap", 0)
    volume_24h = coin.get("total_volume", 0)
    
    min_liquidity = config.get("data_sources", {}).get("min_liquidity_usd", 50000)
    min_volume = config.get("data_sources", {}).get("min_volume_24h_usd", 100000)
    
    if market_cap < min_liquidity:
        score -= 2
        signals.append("low_liquidity")
    
    if volume_24h < min_volume:
        score -= 1
        signals.append("low_volume")
    
    # Trending
    # (We'd need to cross-reference with trending list, simplified here)
    
    return max(score, 0), signals


def scan_tokens(config, min_score=7.0):
    """Scan for trading candidates."""
    print("🔍 Scanning for trading opportunities...", file=sys.stderr)
    
    # Fetch trending coins
    trending_symbols = fetch_trending_coins()
    print(f"  ✅ {len(trending_symbols)} trending coins fetched", file=sys.stderr)
    
    # Fetch market data for trending coins
    market_data = fetch_market_data(trending_symbols)
    print(f"  ✅ {len(market_data)} coins with market data", file=sys.stderr)
    
    # Score each candidate
    candidates = []
    for coin in market_data:
        score, signals = score_candidate(coin, config)
        
        if score >= min_score:
            candidates.append({
                "symbol": coin["symbol"].upper(),
                "name": coin["name"],
                "price": coin["current_price"],
                "market_cap": coin["market_cap"],
                "volume_24h": coin["total_volume"],
                "price_change_1h_pct": coin.get("price_change_percentage_1h_in_currency"),
                "price_change_4h_pct": coin.get("price_change_percentage_4h_in_currency"),
                "price_change_24h_pct": coin.get("price_change_percentage_24h"),
                "volume_spike_ratio": round(calculate_volume_spike(coin), 2),
                "score": score,
                "signals": signals,
                "scanned_at": datetime.now(timezone.utc).isoformat()
            })
    
    # Sort by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    print(f"  ✅ {len(candidates)} candidates with score >= {min_score}", file=sys.stderr)
    
    return candidates


def main():
    parser = argparse.ArgumentParser(description="Scan for trading opportunities")
    parser.add_argument("--output", "-o", default="candidates.json",
                        help="Output JSON file (default: candidates.json)")
    parser.add_argument("--min-score", type=float, default=7.0,
                        help="Minimum score to include (default: 7.0)")
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    
    # Scan for candidates
    candidates = scan_tokens(config, min_score=args.min_score)
    
    # Write output
    with open(args.output, "w") as f:
        json.dump(candidates, f, indent=2)
    
    print(f"\n✅ Scan complete. {len(candidates)} candidates written to {args.output}", file=sys.stderr)
    
    # Print top 3
    if candidates:
        print("\nTop 3 Candidates:", file=sys.stderr)
        for i, c in enumerate(candidates[:3], 1):
            print(f"  {i}. {c['symbol']} (score: {c['score']}) — {', '.join(c['signals'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
