#!/usr/bin/env python3
"""Claim investment (funding collateral) or incentive for a deployed Precog market.

Tracker flow: EIP-712 sign action CLAIM_UPCOMING_MARKET_INVESTMENT[_INCENTIVE]
(domain: Precog Markets v1, verifyingContract = PrecogMaster, nonce = pending
nonce), then POST {network, market, investor_address, investor_signature}.
NOTE market = *deployed* master market id (deployed_market_id), network =
market chain for investment, incentive chain for incentive. The two claims pay
different tokens (collateral vs incentive collateral).

Domain logic lives in common/launchpad_service.py (MarketService shape).
Diagnostics go to stderr via logging. Stdout carries only the result JSON.

Usage:
  python claim_upcoming.py --kind investment|incentive --market <deployed_id> --chain-id 8453 [--rpc URL] [--confirm]
"""
import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common.launchpad_service import DEFAULT_API, LaunchpadService

ACTIONS = {"investment": "CLAIM_UPCOMING_MARKET_INVESTMENT",
           "incentive": "CLAIM_UPCOMING_MARKET_INCENTIVE"}
ENDPOINTS = {"investment": "claim-upcoming-market-investment",
             "incentive": "claim-upcoming-market-incentive"}

log = logging.getLogger('claim-upcoming')


def preview_claimable(base, deployed_id, chain, kind):
    """Best-effort read-only lookup of claimable amounts."""
    # Get backend response for the open funded markets list (best effort, preview only)
    try:
        m = LaunchpadService.api_get(base, "upcoming-markets", "")
        rows = (m.get("results") or []) if isinstance(m, dict) else (m or [])

        # Walk the deployed markets looking for the received market id on this chain
        for row in rows:
            if str(row.get("deployed_market_id")) == str(deployed_id) and int(row.get("chain_id", -1)) == int(chain):
                # Sum the claimable amounts across all funder contributions
                funders = row.get("funders") or []
                field = "claimable_collateral" if kind == "investment" else "claimable_incentive"
                total = sum(float(f.get(field) or 0) for f in funders)
                tok = row.get("collateral_symbol") if kind == "investment" else row.get("incentive_collateral_symbol")

                # Build and return the preview hint
                return (f"market {deployed_id}: status={row.get('status')} token={tok} "
                        f"total_claimable={total}")
    except Exception:
        pass
    return None


def main():
    # Diagnostics go to stderr, stdout carries only the result JSON
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s', stream=sys.stderr)
    p = argparse.ArgumentParser()
    p.add_argument("--kind", required=True, choices=["investment", "incentive"])
    p.add_argument("--market", required=True, help="deployed master market id")
    p.add_argument("--chain-id", required=True, type=int)
    p.add_argument("--rpc", default=None)
    p.add_argument("--api-url", default=os.environ.get("PRECOG_API_URL", DEFAULT_API))
    p.add_argument("--key-file", default=None)
    p.add_argument("--config", default=None)
    p.add_argument("--confirm", action="store_true")
    args = p.parse_args()

    # Case: preview only, stop before any write
    if not args.confirm:
        hint = preview_claimable(args.api_url, args.market, args.chain_id, args.kind)
        if hint:
            log.info(hint)
        log.info("preview: claim %s deployed_market=%s network=%s. Re-run with --confirm.",
                 args.kind, args.market, args.chain_id)
        return 0

    try:
        # Load the investor key and initialize the web3 provider for the claim chain
        key, address = LaunchpadService.load_key(args.key_file, args.config)
        log.info("using %s", address)
        service = LaunchpadService(name='claim-upcoming')
        service.initialize_web3_provider(args.chain_id, key, args.rpc)

        # Check that the investor holds native token for gas
        native = service.web3_service.get_account_balance(address)
        if native == 0:
            raise RuntimeError("no native token for gas.")
        log.info("native balance: %s wei.", native)

        # Sign the claim authorization and register it on the backend
        signature = service.sign_action(args.chain_id, address, ACTIONS[args.kind])
        payload = {"network": args.chain_id, "market": int(args.market),
                   "investor_address": address, "investor_signature": signature}

        # Build and print the claim response
        print(json.dumps(LaunchpadService.api_post(args.api_url, ENDPOINTS[args.kind], payload), indent=2))
    except RuntimeError as e:
        log.error("error: %s", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
