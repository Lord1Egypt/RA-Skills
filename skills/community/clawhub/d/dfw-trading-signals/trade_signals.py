#!/usr/bin/env python3
"""
trade_signals.py — OpenClaw trading-signals skill backend
Connects to: CoinGecko API, DeFiLlama, ccxt (public endpoints)
Usage:
  python3 trade_signals.py --mode=momentum --assets=ripple,hedera-hashgraph
  python3 trade_signals.py --mode=defi --min-tvl=100 --min-apy=5
  python3 trade_signals.py --mode=portfolio --assets=bitcoin,ethereum,ripple,hedera-hashgraph
  python3 trade_signals.py --mode=rsi --assets=bitcoin,ethereum --timeframe=4h
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

# ── Constants ─────────────────────────────────────────────────────────────────
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
DEFILLAMA_POOLS = "https://yields.llama.fi/pools"
SAUCER_POOLS = "https://api.saucerswap.finance/pools"
BINANCE_OHLCV = "https://api.binance.com/api/v3/klines"

SYMBOL_MAP = {
    "btc": "bitcoin", "eth": "ethereum", "xrp": "ripple",
    "hbar": "hedera-hashgraph", "matic": "matic-network",
    "sol": "solana", "ada": "cardano", "dot": "polkadot",
    "link": "chainlink", "uni": "uniswap", "aave": "aave",
}

TICKER_MAP = {
    "bitcoin": "BTC", "ethereum": "ETH", "ripple": "XRP",
    "hedera-hashgraph": "HBAR", "matic-network": "MATIC",
    "solana": "SOL", "cardano": "ADA",
}

TIMEFRAME_DAYS = {"1h": 1, "4h": 2, "24h": 7, "7d": 30}


# ── HTTP helpers ───────────────────────────────────────────────────────────────
def fetch_json(url: str, headers=None):
    req = urllib.request.Request(url, headers=headers or {
        "User-Agent": "OpenClaw-TradingSignals/1.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def coingecko_get(path: str, params=None):
    api_key = os.environ.get("COINGECKO_API_KEY", "")
    url = f"{COINGECKO_BASE}{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        url += f"?{qs}"
    headers = {"User-Agent": "OpenClaw-TradingSignals/1.0", "Accept": "application/json"}
    if api_key:
        headers["x-cg-demo-api-key"] = api_key
    return fetch_json(url, headers)


# ── Signal math ────────────────────────────────────────────────────────────────
def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50.0
    gains, losses = [], []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i - 1]
        gains.append(max(delta, 0))
        losses.append(max(-delta, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def calculate_vwap(prices, volumes):
    if not prices or not volumes or sum(volumes) == 0:
        return prices[-1] if prices else 0
    return sum(p * v for p, v in zip(prices, volumes)) / sum(volumes)


def momentum_score(prices):
    if len(prices) < 2:
        return {"pct": 0.0, "direction": "NEUTRAL"}
    pct = (prices[-1] - prices[0]) / prices[0] * 100
    direction = "UP" if pct > 0 else "DOWN"
    return {"pct": round(pct, 2), "direction": direction}


def classify_signal(rsi, momentum_pct, vwap_dev):
    """Returns (signal, strength)."""
    if rsi > 70:
        return "OVERBOUGHT", "STRONG" if rsi > 80 else "MODERATE"
    if rsi < 30:
        return "OVERSOLD", "STRONG" if rsi < 20 else "MODERATE"
    if momentum_pct > 8 and vwap_dev > 1:
        return "BULLISH", "STRONG"
    if momentum_pct > 3 and vwap_dev > 0:
        return "BULLISH", "MODERATE"
    if momentum_pct < -8 and vwap_dev < -1:
        return "BEARISH", "STRONG"
    if momentum_pct < -3 and vwap_dev < 0:
        return "BEARISH", "MODERATE"
    return "NEUTRAL", "WEAK"


# ── Data fetchers ──────────────────────────────────────────────────────────────
def get_asset_signal(coin_id, days=7):
    """Fetch OHLCV from CoinGecko and compute signals."""
    try:
        data = coingecko_get(f"/coins/{coin_id}/ohlc", {"vs_currency": "usd", "days": days})
    except Exception as e:
        return {"error": str(e), "coin_id": coin_id}

    if not data:
        return {"error": "no data", "coin_id": coin_id}

    # data = [[timestamp, open, high, low, close], ...]
    prices = [row[4] for row in data]   # close
    volumes = [1.0] * len(prices)       # CoinGecko OHLC has no volume; use equal weight

    # Try to get 24h volume separately
    try:
        info = coingecko_get(f"/coins/{coin_id}", {
            "localization": "false", "tickers": "false",
            "community_data": "false", "developer_data": "false"
        })
        market = info.get("market_data", {})
        current_price = market.get("current_price", {}).get("usd", prices[-1])
        vol_24h = market.get("total_volume", {}).get("usd", 0)
        change_24h = market.get("price_change_percentage_24h", 0)
        change_7d = market.get("price_change_percentage_7d", 0)
        market_cap = market.get("market_cap", {}).get("usd", 0)
    except Exception:
        current_price = prices[-1]
        vol_24h = 0
        change_24h = 0
        change_7d = 0
        market_cap = 0

    rsi = calculate_rsi(prices)
    vwap = calculate_vwap(prices, volumes)
    vwap_dev = (current_price - vwap) / vwap * 100 if vwap else 0
    signal, strength = classify_signal(rsi, change_24h, vwap_dev)
    ticker = TICKER_MAP.get(coin_id, coin_id.upper())

    note = []
    if abs(change_24h) > 5:
        note.append(f"Strong {'up' if change_24h > 0 else 'down'}move today")
    if rsi > 65:
        note.append("RSI elevated — watch for pullback")
    elif rsi < 35:
        note.append("RSI low — potential reversal setup")
    if vwap_dev > 3:
        note.append("Price extended above VWAP")
    elif vwap_dev < -3:
        note.append("Price below VWAP — mean reversion possible")

    return {
        "asset": ticker,
        "coingecko_id": coin_id,
        "price_usd": round(current_price, 6),
        "change_24h_pct": round(change_24h, 2),
        "change_7d_pct": round(change_7d, 2),
        "volume_24h_usd": int(vol_24h),
        "market_cap_usd": int(market_cap),
        "rsi_14": rsi,
        "vwap_usd": round(vwap, 6),
        "vwap_deviation_pct": round(vwap_dev, 2),
        "signal": signal,
        "strength": strength,
        "notes": " | ".join(note) if note else "No strong signals",
    }


def get_defi_yields(min_tvl_m=10.0, min_apy=3.0):
    """Fetch top yield pools from DeFiLlama."""
    try:
        pools = fetch_json(DEFILLAMA_POOLS).get("data", [])
    except Exception as e:
        return [{"error": str(e)}]

    STABLES = {"USDC", "USDT", "DAI", "USDS", "FRAX", "LUSD", "CRVUSD"}
    min_tvl = min_tvl_m * 1_000_000

    results = []
    for p in pools:
        tvl = p.get("tvlUsd", 0)
        apy = p.get("apy", 0)
        symbol = p.get("symbol", "")
        chain = p.get("chain", "")
        project = p.get("project", "")
        il_risk = p.get("ilRisk", "no")

        if tvl < min_tvl or apy < min_apy or apy > 200:
            continue

        tokens = [t.strip().upper() for t in symbol.split("-")]
        is_stable = all(t in STABLES for t in tokens)
        results.append({
            "symbol": symbol,
            "project": project,
            "chain": chain,
            "apy": round(apy, 2),
            "tvl_usd": int(tvl),
            "tvl_display": f"${tvl/1e9:.2f}B" if tvl > 1e9 else f"${tvl/1e6:.1f}M",
            "il_risk": il_risk,
            "stable_only": is_stable,
            "risk_rating": "LOW" if is_stable and il_risk == "no" else
                           "MEDIUM" if il_risk == "no" else "HIGH",
        })

    results.sort(key=lambda x: x["apy"], reverse=True)
    return results[:20]


def get_saucer_lp():
    """Fetch SaucerSwap LP pool data."""
    try:
        pools = fetch_json(SAUCER_POOLS)
        if not isinstance(pools, list):
            pools = pools.get("pools", [])
    except Exception as e:
        return [{"error": f"SaucerSwap unavailable: {e}"}]

    results = []
    for p in pools:
        apy = p.get("apr7d", p.get("apr", 0)) or 0
        tvl = p.get("tvlUsd", p.get("tvl", 0)) or 0
        name = p.get("name", p.get("pairName", ""))
        if tvl < 10_000 or apy <= 0:
            continue
        results.append({
            "pool": name,
            "apy_7d": round(apy, 2),
            "tvl_usd": int(tvl),
            "tvl_display": f"${tvl/1e6:.1f}M" if tvl > 1e6 else f"${tvl/1e3:.0f}K",
            "chain": "Hedera",
        })

    results.sort(key=lambda x: x["apy_7d"], reverse=True)
    return results[:10]


# ── Report formatters ──────────────────────────────────────────────────────────
def format_signal_row(s: dict) -> str:
    arrow = "↑" if s.get("change_24h_pct", 0) > 0 else "↓"
    return (
        f"{s['asset']:6} ${s['price_usd']:<12}  "
        f"{arrow} {abs(s.get('change_24h_pct',0)):+.1f}% (24h)  "
        f"RSI: {s.get('rsi_14', 50):.0f}  "
        f"{s.get('signal','?')}/{s.get('strength','?')}\n"
        f"       {s.get('notes','')}"
    )


def format_defi_row(p: dict, idx: int) -> str:
    star = "✓" if p.get("risk_rating") == "LOW" else "⚠"
    return (
        f"{idx}. {p['symbol']:25} {p['apy']:6.1f}% APY  "
        f"TVL: {p['tvl_display']:8}  {star} {p['risk_rating']}"
    )


def print_report(mode, signals, defi, saucer, fmt):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if fmt == "json":
        print(json.dumps({
            "timestamp": ts,
            "mode": mode,
            "signals": signals,
            "defi_yields": defi,
            "saucer_lp": saucer,
        }, indent=2))
        return

    bar = "━" * 50
    print(f"\nTRADING SIGNALS — {ts}")
    print(bar)

    if signals:
        print("\nPRICE SIGNALS:")
        for s in signals:
            if "error" not in s:
                print(f"  {format_signal_row(s)}\n")

        bullish = [s["asset"] for s in signals if s.get("signal") in ("BULLISH", "OVERSOLD")]
        bearish = [s["asset"] for s in signals if s.get("signal") in ("BEARISH", "OVERBOUGHT")]
        if bullish:
            print(f"  TOP SIGNALS: {', '.join(bullish)}")
        if bearish:
            print(f"  CAUTION: {', '.join(bearish)}")

    if defi:
        print(f"\nDEFI YIELDS (top 10):")
        stable = [p for p in defi if p.get("stable_only")]
        volatile = [p for p in defi if not p.get("stable_only")]
        if stable:
            print("  Stablecoin (no IL risk):")
            for i, p in enumerate(stable[:5], 1):
                print(f"    {format_defi_row(p, i)}")
        if volatile:
            print("  Volatile pairs:")
            for i, p in enumerate(volatile[:5], 1):
                print(f"    {format_defi_row(p, i)}")

    if saucer:
        print(f"\nSAUCERSWAP LP (HBAR ecosystem):")
        for i, p in enumerate(saucer[:5], 1):
            print(f"  {i}. {p['pool']:30} {p['apy_7d']:.1f}% APY  TVL: {p['tvl_display']}")

    print(f"\n{bar}")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Trading signals from CoinGecko + DeFiLlama + ccxt")
    parser.add_argument("--mode", default="portfolio",
                        choices=["momentum", "rsi", "defi", "portfolio", "scan", "saucer"],
                        help="Signal mode")
    parser.add_argument("--assets", default="bitcoin,ethereum,ripple,hedera-hashgraph",
                        help="Comma-separated CoinGecko IDs or tickers")
    parser.add_argument("--timeframe", default="24h",
                        choices=["1h", "4h", "24h", "7d"],
                        help="Lookback timeframe")
    parser.add_argument("--min-tvl", type=float, default=10.0,
                        help="Min TVL in millions for DeFi scan")
    parser.add_argument("--min-apy", type=float, default=3.0,
                        help="Min APY for DeFi scan")
    parser.add_argument("--format", default="text", choices=["text", "json"],
                        help="Output format")
    args = parser.parse_args()

    days = TIMEFRAME_DAYS.get(args.timeframe, 7)
    asset_list = [SYMBOL_MAP.get(a.lower().strip(), a.lower().strip())
                  for a in args.assets.split(",") if a.strip()]

    signals = []
    defi = []
    saucer = []

    if args.mode in ("momentum", "rsi", "portfolio", "scan"):
        for coin_id in asset_list:
            sys.stderr.write(f"Fetching {coin_id}...\n")
            signals.append(get_asset_signal(coin_id, days))

    if args.mode in ("defi", "portfolio", "scan"):
        sys.stderr.write("Fetching DeFi yields...\n")
        defi = get_defi_yields(args.min_tvl, args.min_apy)

    if args.mode in ("saucer", "portfolio", "scan"):
        sys.stderr.write("Fetching SaucerSwap LP...\n")
        saucer = get_saucer_lp()

    print_report(args.mode, signals, defi, saucer, args.format)


if __name__ == "__main__":
    main()
