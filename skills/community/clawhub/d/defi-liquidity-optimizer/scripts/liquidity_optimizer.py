#!/usr/bin/env python3
"""
DeFi Liquidity Optimizer Script
Analyzes CLMM pools across Solana (Meteora, Raydium) and Ethereum (Uniswap V4)
to find optimal liquidity positions and calculate impermanent loss risk.
"""

import json
import sys
import os
from datetime import datetime
from math import sqrt

# Pool data structures - in production these would come from API calls
MOCK_POOLS = [
    {"protocol": "Meteora", "pair": "SOL-USDC", "tvl": 12_500_000, "apr": 45.2, "volume_24h": 8_200_000, "fees_24h": 8200},
    {"protocol": "Meteora", "pair": "BONK-SOL", "tvl": 4_800_000, "apr": 78.5, "volume_24h": 3_100_000, "fees_24h": 3100},
    {"protocol": "Raydium", "pair": "SOL-USDC", "tvl": 8_900_000, "apr": 38.1, "volume_24h": 5_400_000, "fees_24h": 5400},
    {"protocol": "Raydium", "pair": "RAY-SOL", "tvl": 2_100_000, "apr": 62.3, "volume_24h": 1_800_000, "fees_24h": 1800},
    {"protocol": "Uniswap V4", "pair": "ETH-USDC", "tvl": 45_000_000, "apr": 22.8, "volume_24h": 28_000_000, "fees_24h": 28000},
    {"protocol": "Uniswap V4", "pair": "WBTC-ETH", "tvl": 32_000_000, "apr": 18.5, "volume_24h": 19_000_000, "fees_24h": 19000},
]


def calculate_impermanent_loss(price_ratio: float) -> float:
    """Calculate impermanent loss for a given price ratio change."""
    return sqrt(price_ratio) - 1


def analyze_pool(pool: dict, investment: float = 1000) -> dict:
    """Analyze a single pool and estimate returns and IL risk."""
    apr = pool["apr"]
    tvl = pool["tvl"]
    volume = pool["volume_24h"]

    # Estimate daily fees earned on $1000 investment
    daily_rewards = (investment * (apr / 100)) / 365
    fee_yield = daily_rewards / investment * 100

    # TVL concentration risk (higher TVL = safer pool)
    tvl_score = min(tvl / 10_000_000, 1.0)

    # Volume efficiency: fees/volume ratio
    fee_efficiency = pool["fees_24h"] / volume if volume > 0 else 0

    # IL risk simulation (price change scenarios)
    scenarios = [
        ("±10%", calculate_impermanent_loss(1.10), 0.10),
        ("±25%", calculate_impermanent_loss(1.25), 0.25),
        ("±50%", calculate_impermanent_loss(1.50), 0.50),
        ("±100%", calculate_impermanent_loss(2.00), 1.00),
    ]

    return {
        "protocol": pool["protocol"],
        "pair": pool["pair"],
        "apr": apr,
        "daily_rewards": daily_rewards,
        "fee_yield_daily_pct": fee_yield,
        "tvl_score": tvl_score,
        "volume_24h": volume,
        "fee_efficiency": fee_efficiency,
        "il_scenarios": scenarios,
    }


def compare_pools(pools: list, min_tvl: float = 0, sort_by: str = "apr") -> list:
    """Compare multiple pools and rank by specified metric."""
    results = []
    for pool in pools:
        if pool["tvl"] >= min_tvl:
            analysis = analyze_pool(pool)
            results.append(analysis)

    if sort_by == "apr":
        results.sort(key=lambda x: x["apr"], reverse=True)
    elif sort_by == "tvl":
        results.sort(key=lambda x: x["tvl_score"], reverse=True)
    elif sort_by == "efficiency":
        results.sort(key=lambda x: x["fee_efficiency"], reverse=True)

    return results


def print_pool_report(pools: list, investment: float = 1000) -> None:
    """Print formatted pool comparison report."""
    print(f"\n{'='*70}")
    print(f"  DEFI LIQUIDITY OPTIMIZER REPORT | {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}")
    print(f"\nInvestment: ${investment:,.2f} | Sorted by APR\n")

    for i, pool in enumerate(pools, 1):
        print(f"#{i} {pool['protocol']:12s} | {pool['pair']:10s}")
        print(f"   APR: {pool['apr']:.1f}% | Daily: ${pool['daily_rewards']:.2f}")
        print(f"   TVL: ${pool['volume_24h']/1e6:.1f}M | Vol: ${pool['volume_24h']/1e6:.1f}M/day")
        print(f"   Safety: {'⭐'*int(pool['tvl_score']*5)} ({pool['tvl_score']:.0%})")
        print(f"   Fee Eff: {pool['fee_efficiency']*100:.3f}%")
        print()
        print(f"   Impermanent Loss Scenarios:")
        for label, il, change in pool['il_scenarios']:
            print(f"     Price {label:5s}: IL = {il*100:.2f}%")
        print()


def get_rebalancing_recommendation(pool: dict, current_price: float, lower_tick: float, upper_tick: float) -> dict:
    """Generate rebalancing recommendation for out-of-range positions."""
    price_in_range = lower_tick <= current_price <= upper_tick

    if price_in_range:
        return {
            "action": "HOLD",
            "message": "Position is currently in range. No rebalancing needed.",
            "current_price": current_price,
            "range": (lower_tick, upper_tick),
        }
    else:
        # Estimate cost to rebalance
        il_from_drift = calculate_impermanent_loss(current_price / ((lower_tick + upper_tick) / 2))
        return {
            "action": "REBALANCE",
            "message": f"Position is out of range! Price has drifted.",
            "current_price": current_price,
            "range": (lower_tick, upper_tick),
            "estimated_il": il_from_drift * 100,
            "recommendation": "Adjust tick range to capture current price",
        }


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "compare"

    if cmd == "compare":
        pools = compare_pools(MOCK_POOLS, min_tvl=1_000_000, sort_by="apr")
        print_pool_report(pools)

    elif cmd == "rank":
        pools = compare_pools(MOCK_POOLS, min_tvl=1_000_000, sort_by="apr")
        print("\n=== POOL RANKINGS ===\n")
        for i, p in enumerate(pools, 1):
            print(f"{i}. {p['protocol']} {p['pair']} - APR: {p['apr']:.1f}%")

    elif cmd == "il" and len(sys.argv) > 2:
        price_ratio = float(sys.argv[2])
        il = calculate_impermanent_loss(price_ratio)
        print(f"\nIL at {price_ratio:.2f}x price change: {il*100:.2f}%")

    else:
        print("Usage:")
        print("  python liquidity_optimizer.py compare   # Full comparison report")
        print("  python liquidity_optimizer.py rank     # APR rankings")
        print("  python liquidity_optimizer.py il 1.5   # Calculate IL for 1.5x price change")


if __name__ == "__main__":
    main()