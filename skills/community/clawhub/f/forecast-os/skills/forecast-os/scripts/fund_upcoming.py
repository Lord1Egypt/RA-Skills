#!/usr/bin/env python3
"""Fund a Precog upcoming (launchpad) market. Tracker flow (market_service.py):

1. GET market (upcoming-markets?id=) -> chain_id, collateral (address/decimals),
   min/max funding. Each market has ONE funding collateral; the *incentive* token
   (paid via claim-incentive) can be a different token on a different chain —
   that is the "multitoken" split. Check both before funding.
2. ON-CHAIN: ERC20 transfer of collateral to the precog creator. Tracker verifies
   the receipt: sender must be the funder, receiver the creator, amount must match.
3. EIP-712 sign action FUND_UPCOMING_MARKET (domain: Precog Markets v1,
   verifyingContract = PrecogMaster, nonce = pending nonce).
4. POST {upcoming_market, amount, tx_hash, funder_address, funder_signature}.

Domain logic lives in common/launchpad_service.py (MarketService shape).
Diagnostics go to stderr via logging. Stdout carries only the result JSON.

Usage:
  python fund_upcoming.py --market 123 --amount 10 [--rpc URL] [--api-url ...] [--key-file K] [--config C]
  python fund_upcoming.py --market 123 --amount 10 --tx-hash 0xabc... --confirm  # transfer already sent; receipt hard-validated
Amount is human units. Needs: web3, eth-account.
"""
import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common.launchpad_service import DEFAULT_API, LaunchpadService

log = logging.getLogger('fund-upcoming')


def main():
    # Diagnostics go to stderr, stdout carries only the result JSON
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s', stream=sys.stderr)
    p = argparse.ArgumentParser()
    p.add_argument("--market", required=True)
    p.add_argument("--amount", required=True, help="human units, e.g. 10")
    p.add_argument("--tx-hash", default=None, help="transfer already sent; receipt is hard-validated")
    p.add_argument("--rpc", default=None)
    p.add_argument("--api-url", default=os.environ.get("PRECOG_API_URL", DEFAULT_API))
    p.add_argument("--key-file", default=None)
    p.add_argument("--config", default=None)
    p.add_argument("--confirm", action="store_true")
    args = p.parse_args()

    # Get market data for the received market id (chain, collateral, funding state)
    try:
        info = LaunchpadService.get_market(args.api_url, args.market)
    except RuntimeError as e:
        log.warning("%s (preview only).", e)
        return 0
    chain = int(info["chain_id"])

    # NOTE backend names the funding token `collateral_token` (older payloads use `collateral_address`)
    collateral = info.get("collateral_token") or info.get("collateral_address")
    if not collateral:
        log.error("market %s payload has no collateral token field.", args.market)
        return 2
    log.info("market %s: chain=%s collateral=%s (%s) funded=%s/%s incentive=%s on chain %s",
             args.market, chain, collateral, info.get("collateral_symbol"),
             info.get("collateral_funding", info.get("total_funding")),
             info.get("max_funding_amount", info.get("max_funding")),
             info.get("incentive_collateral_symbol"), info.get("incentive_chain_id"))

    # Case: preview only, stop before any write
    if not args.confirm:
        log.info("preview: fund %s to creator %s, then register. Re-run with --confirm.",
                 args.amount, LaunchpadService.precog_creator)
        return 0

    try:
        # Load the funder key and initialize the web3 provider for the market chain
        key, address = LaunchpadService.load_key(args.key_file, args.config)
        log.info("using %s", address)
        service = LaunchpadService(name='fund-upcoming')
        service.initialize_web3_provider(chain, key, args.rpc)

        # Case: transfer was already sent, hard-validate its receipt before registering
        if args.tx_hash:
            token = service.web3_service.get_erc_20_contract(collateral)
            decimals = token.functions.decimals().call()
            ok, reason = service.validate_fund_receipt(args.tx_hash, address, collateral,
                                                       args.amount, decimals)
            if not ok:
                log.error("receipt mismatch, aborting: %s", reason)
                return 2
            tx_hash = args.tx_hash
            log.info("existing transfer validated.")
        # Case: fresh funding, pre-check balances then send the collateral transfer
        else:
            preview = service.transfer_collateral(collateral, args.amount, dry_run=True)
            log.info("balances ok: collateral=%s wei, est_fee=%s wei.",
                     preview["collateral_balance_wei"], preview["est_fee_wei"])
            tx_hash = service.transfer_collateral(collateral, args.amount)["tx_hash"]
            log.info("transfer sent: %s, waiting for receipt...", tx_hash)
            service.web3_service.wait_for_transaction_receipt(tx_hash, block_confirmations=1)

        # Sign the funding authorization and register it on the backend
        signature = service.sign_action(chain, address, "FUND_UPCOMING_MARKET")
        payload = {"upcoming_market": int(args.market), "amount": float(args.amount),
                   "tx_hash": tx_hash, "funder_address": address, "funder_signature": signature}

        # Build and print the registration response
        print(json.dumps(LaunchpadService.api_post(args.api_url, "fund-upcoming-market", payload), indent=2))
    except RuntimeError as e:
        log.error("error: %s", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
