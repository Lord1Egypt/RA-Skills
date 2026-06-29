#!/usr/bin/env python3
"""
gas_tracker.py — Ethereum gas price monitor
Fetches current gas prices from public APIs with automatic fallbacks.
Pure Python stdlib — no external dependencies.

Usage:
  python gas_tracker.py              # show all gas tiers
  python gas_tracker.py --fast       # show fast tier only
  python gas_tracker.py --alert 20   # alert if standard gas > 20 Gwei
  python gas_tracker.py --json       # raw JSON output
"""

import urllib.request
import json
import sys
import argparse
from datetime import datetime

# ─── API Registry ───────────────────────────────────────────────────────────
# Each source: (url, method, params, parse_fn)
# parse_fn receives dict, returns {slow, standard, fast, instant, source, block_num}

APIS = []


def _rpc_body(method, params=None):
    return json.dumps({"jsonrpc": "2.0", "method": method, "params": params or [], "id": 1}).encode()


def _rpc(url):
    def decorator(fn):
        APIS.append(("rpc", url, fn))
        return fn
    return decorator


# ─── Source 1: ethereum.publicnode.com (public RPC, no auth) ────────────────
def fetch_publicnode():
    """Fetch gas via ethereum.publicnode.com public RPC."""
    try:
        # eth_gasPrice → baseline
        body = _rpc_body("eth_gasPrice")
        req = urllib.request.Request(
            "https://ethereum.publicnode.com",
            data=body,
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            if "result" not in data:
                return None
            base_gwei = int(data["result"], 16) / 1e9

        # eth_blockNumber
        body2 = _rpc_body("eth_blockNumber")
        req2 = urllib.request.Request(
            "https://ethereum.publicnode.com",
            data=body2,
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req2, timeout=10) as r2:
            data2 = json.loads(r2.read())
            block = int(data2.get("result", "0x0"), 16)

        # Estimate tiers from base gas price
        # Slow: base, Standard: +2 Gwei, Fast: +5 Gwei, Instant: +10 Gwei
        return {
            "source": "publicnode.com",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "slow": round(base_gwei * 1.0, 1),
            "standard": round(base_gwei * 1.2, 1),
            "fast": round(base_gwei * 1.5, 1),
            "instant": round(base_gwei * 2.0, 1),
            "base_fee": round(base_gwei, 1),
            "block_num": block,
        }
    except Exception:
        return None


# ─── Source 2: blockscout gas oracle ────────────────────────────────────────
def fetch_blockscout():
    """Fetch gas via blockscout public API."""
    try:
        url = "https://api.blockscout.com/api/v1/gasOracle"
        req = urllib.request.Request(
            url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = json.loads(r.read())["data"]
            return {
                "source": "blockscout",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "slow": round(float(raw.get("gas_price_wei_low", 0)) / 1e9, 1),
                "standard": round(float(raw.get("gas_price_wei_standard", 0)) / 1e9, 1),
                "fast": round(float(raw.get("gas_price_wei_fast", 0)) / 1e9, 1),
                "instant": round(float(raw.get("gas_price_wei_instant", 0)) / 1e9, 1),
                "base_fee": round(float(raw.get("base_fee", 0)) / 1e9, 1),
                "block_num": raw.get("block_number", 0),
            }
    except Exception:
        return None


# ─── Source 3: ethgas.info (values × 0.1 = Gwei) ────────────────────────────
def fetch_ethgas_info():
    """Fallback: ethgas.info — no auth, returns Gwei × 10."""
    try:
        url = "https://ethgas.info/api/ethgas"
        req = urllib.request.Request(
            url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            factor = 0.1
            return {
                "source": "ethgas.info",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "slow": round(data.get("safeLow", 0) * factor, 1),
                "standard": round(data.get("average", 0) * factor, 1),
                "fast": round(data.get("fast", 0) * factor, 1),
                "instant": round(data.get("fastest", 0) * factor, 1),
                "base_fee": 0,
                "block_num": data.get("blockNum", 0),
            }
    except Exception:
        return None


# ─── Source 4: web scraping fallback (wttr.in-style page) ──────────────────
def fetch_eth_api():
    """Last resort: try to fetch from ethereum API page."""
    try:
        url = "https://api.ethgas.watch/api/gas"
        req = urllib.request.Request(
            url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            pf = data.get("PriorityFee", {})
            bf = data.get("base_fee", 0)
            return {
                "source": "ethgas.watch",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "slow": round(pf.get("low", 0), 1),
                "standard": round(pf.get("medium", 0), 1),
                "fast": round(pf.get("fast", 0), 1),
                "instant": round(pf.get("instant", 0), 1),
                "base_fee": round(bf, 1),
                "block_num": data.get("blockNumber", 0),
            }
    except Exception:
        return None


def get_gas_data() -> dict:
    """Try all sources, return first successful response."""
    sources = [fetch_publicnode, fetch_blockscout, fetch_ethgas_info, fetch_eth_api]
    for fn in sources:
        data = fn()
        if data and all(k in data for k in ["slow", "standard", "fast", "instant"]):
            return data
    print(
        "ERROR: All gas APIs unreachable. Check internet connection.",
        file=sys.stderr,
    )
    sys.exit(1)


def format_gwei(val: float) -> str:
    return f"{val:.1f} Gwei"


ESTIMATE = {
    "slow": "~15 min",
    "standard": "~5 min",
    "fast": "~2 min",
    "instant": "~30 sec",
}


def print_report(data: dict, only: str | None = None):
    print(f"\n  ETH Gas Tracker  |  Source: {data['source']}  |  Block #{data['block_num']}")
    print(f"  Updated: {data['timestamp']}")
    print()
    print("  Tier      Gwei      ETA")
    print("  ------    ------    -------")
    tiers = [
        ("slow", "Slow", data["slow"]),
        ("standard", "Standard", data["standard"]),
        ("fast", "Fast", data["fast"]),
        ("instant", "Instant", data["instant"]),
    ]
    for key, label, val in tiers:
        if only and key != only:
            continue
        print(f"  {label:<8} {format_gwei(val):<10} {ESTIMATE[key]}")
    if only:
        return
    print()
    if data.get("base_fee"):
        print(f"  Base Fee: {data['base_fee']:.1f} Gwei")
    avg = data["standard"]
    if avg < 15:
        status = "LOW — Good time to transact"
    elif avg < 30:
        status = "MODERATE — Normal conditions"
    elif avg < 60:
        status = "HIGH — Consider waiting"
    else:
        status = "VERY HIGH — Avoid non-urgent txns"
    print(f"  Status: {status}")
    print()


def check_alert(data: dict, threshold: float):
    avg = data["standard"]
    if avg > threshold:
        print(f"ALERT: Standard gas ({avg:.1f} Gwei) exceeds threshold ({threshold} Gwei)")
    else:
        print(f"OK: Standard gas ({avg:.1f} Gwei) is below threshold ({threshold} Gwei)")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Ethereum gas price tracker")
    parser.add_argument("--slow", action="store_true", help="Show slow tier only")
    parser.add_argument("--standard", action="store_true", help="Show standard tier only")
    parser.add_argument("--fast", action="store_true", help="Show fast tier only")
    parser.add_argument("--instant", action="store_true", help="Show instant tier only")
    parser.add_argument("--alert", type=float, metavar="GWEI", help="Alert if standard gas exceeds threshold")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    data = get_gas_data()
    if args.json:
        print(json.dumps(data, indent=2))
        return
    if args.alert is not None:
        check_alert(data, args.alert)
        return
    only = None
    for flag, tier in [
        (args.slow, "slow"),
        (args.standard, "standard"),
        (args.fast, "fast"),
        (args.instant, "instant"),
    ]:
        if flag:
            only = tier
    print_report(data, only=only)


if __name__ == "__main__":
    main()
