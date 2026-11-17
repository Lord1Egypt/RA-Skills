#!/usr/bin/env python3
"""Check live gas prices across major EVM chains via free public RPC endpoints (no API key)."""

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone

CHAINS = {
    "ethereum": {"rpc": "https://ethereum-rpc.publicnode.com", "native": "ETH", "unit": "gwei"},
    "base": {"rpc": "https://base-rpc.publicnode.com", "native": "ETH", "unit": "gwei"},
    "arbitrum": {"rpc": "https://arbitrum-one-rpc.publicnode.com", "native": "ETH", "unit": "gwei"},
    "optimism": {"rpc": "https://optimism-rpc.publicnode.com", "native": "ETH", "unit": "gwei"},
    "polygon": {"rpc": "https://polygon-bor-rpc.publicnode.com", "native": "MATIC", "unit": "gwei"},
}

# Typical low-traffic UTC hours for Ethereum-family chains (weekend / US overnight),
# based on well-documented usage cycles tied to US/EU/Asia trading-day overlap.
LOW_TRAFFIC_UTC_HOURS = set(list(range(2, 9)))  # ~2am-9am UTC (US overnight, Asia early)


def rpc_call(rpc_url, method, params=None):
    body = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or [], "id": 1}).encode()
    req = urllib.request.Request(
        rpc_url, data=body,
        headers={"Content-Type": "application/json", "User-Agent": "curl/8.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if "error" in payload:
        raise RuntimeError(payload["error"].get("message", "RPC error"))
    return payload["result"]


def wei_to_gwei(hex_wei):
    return int(hex_wei, 16) / 1e9


def get_chain_gas(name, cfg):
    gas_price_gwei = wei_to_gwei(rpc_call(cfg["rpc"], "eth_gasPrice"))
    result = {"chain": name, "native": cfg["native"], "gas_price_gwei": round(gas_price_gwei, 4)}
    try:
        block = rpc_call(cfg["rpc"], "eth_getBlockByNumber", ["latest", False])
        base_fee_hex = block.get("baseFeePerGas")
        if base_fee_hex:
            result["base_fee_gwei"] = round(wei_to_gwei(base_fee_hex), 4)
    except Exception:
        pass
    return result


def estimate_cost_usd(gas_price_gwei, gas_limit, native_price_usd):
    native_amount = (gas_price_gwei * gas_limit) / 1e9
    return native_amount * native_price_usd


def fetch_native_prices():
    """USD prices for ETH and MATIC via CoinGecko's free simple-price endpoint."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum,matic-network&vs_currencies=usd"
    req = urllib.request.Request(url, headers={"User-Agent": "clawhub-gas-optimizer/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return {
        "ETH": data.get("ethereum", {}).get("usd"),
        "MATIC": data.get("matic-network", {}).get("usd"),
    }


def timing_advice():
    hour = datetime.now(timezone.utc).hour
    if hour in LOW_TRAFFIC_UTC_HOURS:
        return (f"Current UTC hour ({hour:02d}:00) falls in a typically lower-traffic window "
                "(~02:00-09:00 UTC, US overnight / early Asia session). Good general window for non-urgent txs.")
    return (f"Current UTC hour ({hour:02d}:00) is outside the typical low-traffic window "
            "(~02:00-09:00 UTC). If the tx isn't urgent, consider waiting or checking back during that window.")


def main():
    ap = argparse.ArgumentParser(description="Live EVM gas price checker across major chains (free public RPCs)")
    ap.add_argument("--chains", type=str, default="ethereum,base,arbitrum,optimism,polygon",
                     help="Comma-separated chain list from: " + ",".join(CHAINS))
    ap.add_argument("--gas-limit", type=int, default=21000, help="Gas limit to price out (default 21000 = simple ETH transfer)")
    ap.add_argument("--json", action="store_true", help="Print raw JSON")
    args = ap.parse_args()

    requested = [c.strip().lower() for c in args.chains.split(",") if c.strip()]
    unknown = [c for c in requested if c not in CHAINS]
    if unknown:
        print(json.dumps({"error": f"Unknown chain(s): {unknown}. Known: {list(CHAINS)}"}))
        sys.exit(1)

    results = []
    errors = []
    for name in requested:
        try:
            results.append(get_chain_gas(name, CHAINS[name]))
        except Exception as e:
            errors.append({"chain": name, "error": str(e)})

    try:
        prices = fetch_native_prices()
    except Exception:
        prices = {}

    for r in results:
        px = prices.get(r["native"])
        if px:
            r["est_tx_cost_usd"] = round(estimate_cost_usd(r["gas_price_gwei"], args.gas_limit, px), 4)

    output = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "gas_limit_used": args.gas_limit,
        "results": sorted(results, key=lambda r: r.get("est_tx_cost_usd", r["gas_price_gwei"])),
        "errors": errors,
        "timing_note": timing_advice(),
    }

    if args.json:
        print(json.dumps(output, indent=2))
        return

    print(f"Gas check @ {output['checked_at_utc']} (gas limit: {args.gas_limit})\n")
    print(f"{'Chain':<12}{'Gas (gwei)':>14}{'Base Fee':>12}{'Est. Cost USD':>16}")
    print("-" * 56)
    for r in output["results"]:
        base = f"{r.get('base_fee_gwei', ''):.4f}" if r.get("base_fee_gwei") is not None else "-"
        cost = f"${r['est_tx_cost_usd']:.4f}" if "est_tx_cost_usd" in r else "n/a"
        print(f"{r['chain']:<12}{r['gas_price_gwei']:>14.4f}{base:>12}{cost:>16}")
    if errors:
        print("\nErrors:", errors)
    print(f"\n{output['timing_note']}")
    print("Cheapest chain right now:", output["results"][0]["chain"] if output["results"] else "n/a")


if __name__ == "__main__":
    main()
