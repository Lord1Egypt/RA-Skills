#!/usr/bin/env python3
"""
DAO Treasury Tracker

Pulls on-chain DAO treasury composition from the free DeFiLlama API
(no API key required) and flags treasuries that are dangerously
concentrated in their own governance token vs. diversified into
stablecoins/ETH/other assets.

Why this matters: a DAO treasury that is 80%+ its own token isn't real
runway — if the token price falls 50%, the treasury's spending power
falls 50% too, right when the project probably needs it most. This
tool computes that concentration ratio directly from DeFiLlama's
treasury dataset so you don't have to eyeball a dashboard.

Usage:
    python3 treasury_tracker.py uniswap lido aave ens gitcoin
    python3 treasury_tracker.py --json uniswap
    python3 treasury_tracker.py --list-protocols     # slug hints

Notes:
- Protocol slugs match DeFiLlama's protocol slugs (usually lowercase
  project name, e.g. "uniswap", "lido", "aave", "ens", "gitcoin").
  Not every protocol has a tracked treasury module; those will report
  an error for that slug and the script will continue with the rest.
- This reads treasury/balance-sheet data only. It does not predict
  DAO spending, runway in months, or governance proposals.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

TREASURY_URL = "https://api.llama.fi/treasury/{slug}"
PROTOCOLS_URL = "https://api.llama.fi/protocols"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dao-treasury-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def analyze_treasury(slug):
    url = TREASURY_URL.format(slug=slug)
    try:
        data = fetch_json(url)
    except urllib.error.HTTPError as e:
        return {"slug": slug, "error": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        return {"slug": slug, "error": f"network error: {e.reason}"}
    except json.JSONDecodeError:
        return {"slug": slug, "error": "no treasury data for this slug (check spelling / not tracked)"}

    chain_tvls = data.get("currentChainTvls") or {}
    if not chain_tvls:
        return {"slug": slug, "error": "empty treasury data"}

    # Keys without a "-" are top-level totals (per-chain non-token assets,
    # plus a chain-agnostic "OwnTokens" aggregate). Keys with "-OwnTokens"
    # are a per-chain breakdown already folded into the "OwnTokens" total,
    # so summing only the no-dash keys avoids double-counting.
    total = sum(v for k, v in chain_tvls.items() if "-" not in k)
    own_tokens = chain_tvls.get("OwnTokens", 0.0)
    other_assets = total - own_tokens

    own_pct = (own_tokens / total * 100) if total > 0 else None

    if own_pct is None:
        risk = "UNKNOWN"
    elif own_pct >= 70:
        risk = "TOKEN-CONCENTRATED (high risk)"
    elif own_pct >= 40:
        risk = "MODERATE CONCENTRATION"
    else:
        risk = "DIVERSIFIED"

    return {
        "slug": slug,
        "name": data.get("name"),
        "total_treasury_usd": round(total, 2),
        "own_token_usd": round(own_tokens, 2),
        "other_assets_usd": round(other_assets, 2),
        "own_token_pct": round(own_pct, 1) if own_pct is not None else None,
        "risk_label": risk,
        "chains": sorted({k.split("-")[0] for k in chain_tvls.keys()}),
    }


def list_protocol_hints():
    try:
        protocols = fetch_json(PROTOCOLS_URL)
    except Exception as e:
        print(f"Could not fetch protocol list: {e}", file=sys.stderr)
        sys.exit(1)
    names = sorted({p.get("slug") for p in protocols if p.get("slug")})
    print(f"{len(names)} protocol slugs available on DeFiLlama. Sample:")
    for n in names[:50]:
        print(f"  {n}")
    print("... not every slug has a tracked treasury module.")


def main():
    ap = argparse.ArgumentParser(description="DAO treasury concentration tracker (DeFiLlama-backed)")
    ap.add_argument("slugs", nargs="*", help="DeFiLlama protocol slugs, e.g. uniswap lido aave")
    ap.add_argument("--json", action="store_true", help="Output raw JSON instead of a table")
    ap.add_argument("--list-protocols", action="store_true", help="Print sample protocol slugs and exit")
    args = ap.parse_args()

    if args.list_protocols:
        list_protocol_hints()
        return

    if not args.slugs:
        ap.print_help()
        sys.exit(1)

    results = [analyze_treasury(s) for s in args.slugs]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    ok = [r for r in results if "error" not in r]
    failed = [r for r in results if "error" in r]
    ok.sort(key=lambda r: -(r["own_token_pct"] or 0))

    header = f"{'DAO':<14}{'TOTAL USD':>16}{'OWN TOKEN %':>14}  {'RISK'}"
    print(header)
    print("-" * len(header))
    for r in ok:
        total = f"${r['total_treasury_usd']:,.0f}"
        pct = f"{r['own_token_pct']:.1f}%" if r["own_token_pct"] is not None else "-"
        print(f"{r['name'] or r['slug']:<14}{total:>16}{pct:>14}  {r['risk_label']}")

    if failed:
        print()
        for r in failed:
            print(f"  [skip] {r['slug']}: {r['error']}")


if __name__ == "__main__":
    main()
