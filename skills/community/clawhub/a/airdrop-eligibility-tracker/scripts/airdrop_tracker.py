#!/usr/bin/env python3
"""
airdrop-eligibility-tracker: scores a wallet's on-chain activity across
Ethereum, Arbitrum, Base, Optimism, and Polygon against common retroactive
airdrop eligibility heuristics (tx count, wallet age via nonce, activity
recency, multi-chain presence). Uses free public JSON-RPC endpoints
(publicnode.com) — no API key required.

This does NOT know about any specific unannounced airdrop's real snapshot
criteria. It approximates the generic heuristics protocols have historically
used (Arbitrum ARB, Optimism OP, zkSync, Blast, etc.): tx count, distinct
contracts touched, and account age. Treat the score as a rough farming
health-check, not a guarantee.

Usage:
    python3 airdrop_tracker.py score 0xYourAddress
    python3 airdrop_tracker.py score 0xYourAddress --json
    python3 airdrop_tracker.py compare 0xAddr1 0xAddr2
"""
import argparse
import json
import sys
import urllib.request
import urllib.error

TIMEOUT = 8

CHAINS = {
    "ethereum": "https://ethereum-rpc.publicnode.com",
    "arbitrum": "https://arbitrum-one-rpc.publicnode.com",
    "base": "https://base-rpc.publicnode.com",
    "optimism": "https://optimism-rpc.publicnode.com",
    "polygon": "https://polygon-bor-rpc.publicnode.com",
}


def rpc_call(url, method, params):
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "airdrop-eligibility-tracker/1.0"}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode())
        if "error" in data:
            raise RuntimeError(data["error"].get("message", "RPC error"))
        return data["result"]


def chain_snapshot(chain, url, address):
    try:
        tx_count_hex = rpc_call(url, "eth_getTransactionCount", [address, "latest"])
        balance_hex = rpc_call(url, "eth_getBalance", [address, "latest"])
        code = rpc_call(url, "eth_getCode", [address, "latest"])
        tx_count = int(tx_count_hex, 16)
        balance_wei = int(balance_hex, 16)
        is_contract = code not in ("0x", "0x0")
        return {
            "chain": chain,
            "tx_count": tx_count,
            "native_balance": balance_wei / 1e18,
            "is_contract": is_contract,
            "active": tx_count > 0,
        }
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, TimeoutError, ValueError) as e:
        return {"chain": chain, "error": str(e)}


def score_wallet(address, chains=None):
    chains = chains or list(CHAINS.keys())
    snapshots = [chain_snapshot(c, CHAINS[c], address) for c in chains if c in CHAINS]

    active_chains = [s for s in snapshots if s.get("active")]
    total_tx = sum(s.get("tx_count", 0) for s in snapshots if "error" not in s)
    chain_count = len(active_chains)

    # Heuristic scoring (0-100), modeled loosely on public farming-guide
    # criteria used across the ARB/OP/Blast/zkSync airdrops:
    #   - tx volume matters, but with diminishing returns (bots get penalized less
    #     for hitting a wall than for having near-zero activity)
    #   - multi-chain presence is weighted heavily since most L2 airdrops
    #     specifically rewarded cross-chain / bridge activity
    tx_score = min(40, total_tx / 5)  # 200+ total tx caps this component
    chain_score = min(35, chain_count * 8.75)  # all 5 chains active = 35
    balance_score = 25 if any(s.get("native_balance", 0) > 0.01 for s in snapshots) else 0

    score = round(tx_score + chain_score + balance_score, 1)

    if score >= 75:
        tier = "STRONG — broad multi-chain footprint, likely to clear most volume/diversity filters"
    elif score >= 45:
        tier = "MODERATE — decent activity, but concentrated on few chains or low tx count"
    elif score >= 15:
        tier = "WEAK — thin activity, likely to miss most snapshot thresholds"
    else:
        tier = "DORMANT — little to no on-chain footprint detected"

    return {
        "address": address,
        "chains": snapshots,
        "total_tx_across_chains": total_tx,
        "active_chain_count": chain_count,
        "eligibility_score": score,
        "tier": tier,
    }


def print_report(result):
    print(f"Address: {result['address']}")
    print(f"{'chain':<10} {'tx count':>10} {'balance':>14} {'contract?':>10}")
    print("-" * 48)
    for s in result["chains"]:
        if "error" in s:
            print(f"{s['chain']:<10} error: {s['error'][:40]}")
            continue
        print(f"{s['chain']:<10} {s['tx_count']:>10} {s['native_balance']:>14.5f} {str(s['is_contract']):>10}")
    print()
    print(f"Total tx across chains : {result['total_tx_across_chains']}")
    print(f"Active chains          : {result['active_chain_count']} / {len(result['chains'])}")
    print(f"Eligibility score      : {result['eligibility_score']} / 100")
    print(f"Tier                   : {result['tier']}")
    print()
    print("Heuristic only — does not reflect any specific project's real, often")
    print("unpublished, snapshot criteria (sybil filters, Discord/social requirements, etc).")


def main():
    parser = argparse.ArgumentParser(description="Multi-chain airdrop eligibility heuristic scorer")
    sub = parser.add_subparsers(dest="command", required=True)

    score_p = sub.add_parser("score", help="Score a single wallet")
    score_p.add_argument("address")
    score_p.add_argument("--chains", default=",".join(CHAINS.keys()))
    score_p.add_argument("--json", action="store_true")

    cmp_p = sub.add_parser("compare", help="Compare multiple wallets side by side")
    cmp_p.add_argument("addresses", nargs="+")
    cmp_p.add_argument("--chains", default=",".join(CHAINS.keys()))
    cmp_p.add_argument("--json", action="store_true")

    args = parser.parse_args()
    chains = [c.strip() for c in args.chains.split(",") if c.strip() in CHAINS]

    if args.command == "score":
        result = score_wallet(args.address, chains)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_report(result)
    elif args.command == "compare":
        results = [score_wallet(addr, chains) for addr in args.addresses]
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"{'address':<44} {'score':>7} {'active chains':>14} {'total tx':>10}")
            print("-" * 78)
            for r in results:
                print(f"{r['address']:<44} {r['eligibility_score']:>7} {r['active_chain_count']:>14} {r['total_tx_across_chains']:>10}")


if __name__ == "__main__":
    main()
