#!/usr/bin/env python3
"""Scan live DeFi stablecoin yields via the free DeFiLlama yields API (no API key required)."""

import argparse
import json
import sys
import urllib.request

LLAMA_POOLS_URL = "https://yields.llama.fi/pools"

STABLE_SYMBOLS = {
    "USDC", "USDT", "DAI", "USDE", "USDS", "FRAX", "TUSD", "USDP", "GUSD",
    "LUSD", "SUSD", "CRVUSD", "USDD", "PYUSD", "USDC.E", "USDT.E", "FDUSD",
    "USR", "USDY", "SDAI", "SUSDE", "MKUSD",
}


def fetch_pools():
    req = urllib.request.Request(LLAMA_POOLS_URL, headers={"User-Agent": "clawhub-stablecoin-yield-scanner/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload.get("data", [])


def is_stablecoin_pool(pool):
    if pool.get("stablecoin") is True:
        return True
    symbol = (pool.get("symbol") or "").upper()
    tokens = [t.strip() for t in symbol.replace("-", "/").split("/") if t.strip()]
    return bool(tokens) and all(t in STABLE_SYMBOLS for t in tokens)


def scan(min_tvl_usd=1_000_000, min_apy=0.0, max_apy=100.0, chain=None, top=15):
    pools = fetch_pools()
    results = []
    for p in pools:
        if not is_stablecoin_pool(p):
            continue
        tvl = p.get("tvlUsd") or 0
        apy = p.get("apy") or 0
        if tvl < min_tvl_usd:
            continue
        if apy < min_apy or apy > max_apy:
            continue
        if chain and (p.get("chain") or "").lower() != chain.lower():
            continue
        results.append({
            "project": p.get("project"),
            "chain": p.get("chain"),
            "symbol": p.get("symbol"),
            "apy": round(apy, 3),
            "apy_base": round(p.get("apyBase") or 0, 3),
            "apy_reward": round(p.get("apyReward") or 0, 3),
            "tvl_usd": round(tvl, 2),
            "il_risk": p.get("ilRisk"),
            "pool_id": p.get("pool"),
        })
    results.sort(key=lambda r: r["apy"], reverse=True)
    return results[:top]


def main():
    ap = argparse.ArgumentParser(description="Scan live stablecoin DeFi yields (DeFiLlama)")
    ap.add_argument("--min-tvl", type=float, default=1_000_000, help="Minimum pool TVL in USD (default 1,000,000; higher TVL = lower rug/liquidity risk)")
    ap.add_argument("--min-apy", type=float, default=0.0, help="Minimum APY percent")
    ap.add_argument("--max-apy", type=float, default=100.0, help="Maximum APY percent (filters out likely unsustainable/broken pools)")
    ap.add_argument("--chain", type=str, default=None, help="Filter to one chain, e.g. Ethereum, Base, Arbitrum")
    ap.add_argument("--top", type=int, default=15, help="Number of results to return")
    ap.add_argument("--json", action="store_true", help="Print raw JSON instead of a table")
    args = ap.parse_args()

    try:
        results = scan(args.min_tvl, args.min_apy, args.max_apy, args.chain, args.top)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    if not results:
        print("No pools matched your filters. Try lowering --min-tvl or --min-apy.")
        return

    print(f"{'Project':<22}{'Chain':<12}{'Symbol':<16}{'APY %':>8}{'TVL USD':>16}  IL Risk")
    print("-" * 90)
    for r in results:
        tvl_str = f"${r['tvl_usd']:,.0f}"
        print(f"{r['project'][:21]:<22}{r['chain'][:11]:<12}{r['symbol'][:15]:<16}{r['apy']:>8.2f}{tvl_str:>16}  {r['il_risk']}")
    print("\nData: DeFiLlama yields API (https://yields.llama.fi). APY figures include reward emissions, "
          "which can drop sharply — read apy_base vs apy_reward with --json before committing capital. "
          "Not financial advice; verify contracts before depositing.")


if __name__ == "__main__":
    main()
