#!/usr/bin/env python3
"""
Gas Fee Tracker — live gas price snapshot across EVM chains via free public RPCs.

Queries eth_gasPrice on public RPC endpoints (no API key required) for
Ethereum mainnet, Base, Polygon, and Arbitrum, converts to gwei, classifies
each as low/medium/high relative to configurable thresholds, and can log
snapshots over time to build a simple history file.

Usage:
    python3 gas_tracker.py                      # snapshot all chains
    python3 gas_tracker.py --chain ethereum      # single chain
    python3 gas_tracker.py --log gas_history.jsonl   # append snapshot to log
    python3 gas_tracker.py --alert-below 15 --chain ethereum  # exit 0 only if under threshold
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone

import requests

CHAINS = {
    "ethereum": {
        "rpc": "https://ethereum.publicnode.com",
        "thresholds": {"low": 15, "high": 40},  # gwei
    },
    "base": {
        "rpc": "https://base.publicnode.com",
        "thresholds": {"low": 0.05, "high": 0.5},
    },
    "polygon": {
        "rpc": "https://polygon-bor-rpc.publicnode.com",
        "thresholds": {"low": 50, "high": 200},
    },
    "arbitrum": {
        "rpc": "https://arbitrum-one.publicnode.com",
        "thresholds": {"low": 0.05, "high": 0.3},
    },
}


def fetch_gas_price_gwei(rpc_url: str, timeout=10) -> float:
    resp = requests.post(
        rpc_url,
        json={"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1},
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"].get("message", "RPC error"))
    wei = int(data["result"], 16)
    return wei / 1e9


def classify(gwei: float, thresholds: dict) -> str:
    if gwei <= thresholds["low"]:
        return "LOW"
    if gwei >= thresholds["high"]:
        return "HIGH"
    return "MEDIUM"


def snapshot(chain_names):
    results = {}
    for name in chain_names:
        cfg = CHAINS[name]
        try:
            gwei = fetch_gas_price_gwei(cfg["rpc"])
            level = classify(gwei, cfg["thresholds"])
            results[name] = {"gwei": round(gwei, 4), "level": level, "error": None}
        except Exception as e:
            results[name] = {"gwei": None, "level": None, "error": str(e)}
    return results


def main():
    ap = argparse.ArgumentParser(description="Live EVM gas price tracker (no API key needed)")
    ap.add_argument("--chain", choices=list(CHAINS.keys()), default=None,
                     help="Single chain to query (default: all chains)")
    ap.add_argument("--log", default=None, help="Append JSONL snapshot to this file")
    ap.add_argument("--alert-below", type=float, default=None,
                     help="With --chain, exit 0 if gas is at/below this gwei, exit 1 otherwise")
    ap.add_argument("--json", action="store_true", help="Print raw JSON instead of a table")
    args = ap.parse_args()

    chain_names = [args.chain] if args.chain else list(CHAINS.keys())
    results = snapshot(chain_names)
    ts = datetime.now(timezone.utc).isoformat()

    if args.json:
        print(json.dumps({"timestamp": ts, "chains": results}, indent=2))
    else:
        print(f"Gas Fee Snapshot — {ts}")
        print("-" * 48)
        for name, r in results.items():
            if r["error"]:
                print(f"{name:10s}  ERROR: {r['error']}")
            else:
                print(f"{name:10s}  {r['gwei']:>10.4f} gwei   [{r['level']}]")
        print("-" * 48)

    if args.log:
        with open(args.log, "a") as f:
            f.write(json.dumps({"timestamp": ts, "chains": results}) + "\n")

    if args.alert_below is not None:
        if not args.chain:
            sys.exit("--alert-below requires --chain")
        r = results[args.chain]
        if r["error"] or r["gwei"] is None:
            sys.exit(1)
        sys.exit(0 if r["gwei"] <= args.alert_below else 1)


if __name__ == "__main__":
    main()
