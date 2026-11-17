#!/usr/bin/env python3
"""Discover Precog upcoming (launchpad) markets from the backend proxy.

Read-only discovery for funders. Hits GET upcoming-markets/ with tracker
filters passed straight through (status, network/chain_id, category,
collateral_symbol, funder_address, ...). No key, no RPC, stdlib only.

Default lists fundable markets only: VALIDATED rows plus FUNDED rows with
room under the max cap. Pass --all to list every status instead.

Domain logic lives in common/launchpad_service.py. Diagnostics go to stderr
via logging. Stdout carries compact lines, or full JSON under --json.

Usage:
  python list_upcoming.py [--status VALIDATED,FUNDED] [--chain-id 8453] [--all] [--limit 20] [--json]
"""
import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common.launchpad_service import DEFAULT_API, LaunchpadService

log = logging.getLogger('list-upcoming')

# Statuses a funder can act on without further filtering.
FUNDABLE_STATUSES = ("VALIDATED", "FUNDED")


def clean(text, width):
    # Truncate display text and strip non-ASCII for Windows consoles.
    text = str(text or "").replace("\n", " ")
    text = text.encode("ascii", "replace").decode("ascii")
    if len(text) > width:
        text = text[:width - 1] + "…".encode("ascii", "replace").decode("ascii")
    return text


def describe(row):
    # Build one compact line for a market row.
    funded = row.get("collateral_funding") or 0
    max_funding = row.get("max_funding_amount")
    cap = max_funding if max_funding is not None else "?"
    incentive = row.get("incentive_collateral_symbol") or "none"
    end = LaunchpadService.parse_end(row)
    end_text = end.strftime("%Y-%m-%d") if end else "?"
    return (f"{row.get('id')} | {row.get('status')} | chain {row.get('chain_id')} | "
            f"{clean(row.get('question'), 50)} | fund {funded}/{cap} "
            f"{row.get('collateral_symbol')} | min {row.get('min_funding_amount')} | "
            f"ends {end_text} | incentive {incentive}")


def main():
    # Diagnostics go to stderr, stdout carries only market lines or JSON.
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s', stream=sys.stderr)
    p = argparse.ArgumentParser()
    p.add_argument("--status", default=None,
                   help="comma-separated statuses, repeatable filter (default VALIDATED,FUNDED)")
    p.add_argument("--chain-id", default=None, help="filter by chain id")
    p.add_argument("--category", default=None, help="filter by category")
    p.add_argument("--collateral-symbol", default=None, help="filter by collateral symbol")
    p.add_argument("--funder-address", default=None, help="only markets this address funded")
    p.add_argument("--all", action="store_true",
                   help="list every status, tagging non-fundable rows with the reason")
    p.add_argument("--limit", default=None, type=int, help="max rows to print")
    p.add_argument("--json", action="store_true", help="print full rows as JSON")
    p.add_argument("--api-url", default=os.environ.get("PRECOG_API_URL", DEFAULT_API))
    args = p.parse_args()

    # Case: explorer mode lists everything, tagging rows the funder cannot act on.
    # Case: funder mode (default) lists fundable rows only.
    statuses = [s.strip().upper() for s in args.status.split(",")] if args.status else list(FUNDABLE_STATUSES)
    params = {"status": statuses}
    if args.chain_id:
        params["network"] = args.chain_id
    if args.category:
        params["category"] = args.category
    if args.collateral_symbol:
        params["collateral_symbol"] = args.collateral_symbol
    if args.funder_address:
        params["funder_address"] = args.funder_address

    try:
        rows = LaunchpadService.list_markets(args.api_url, params)
    except Exception as e:
        log.error("error: %s", e)
        return 2

    # Funder mode drops rows with no room left or a past end date.
    # Explorer mode keeps and tags them instead.
    shown = []
    dropped_ended = 0
    for row in rows:
        ok, reason = LaunchpadService.is_fundable(row)
        if LaunchpadService.has_ended(row):
            if args.all:
                shown.append((row, False, "ENDED"))
            else:
                dropped_ended += 1
            continue
        if ok or args.all:
            shown.append((row, ok, reason))
        if args.limit and len(shown) >= args.limit:
            break

    # Build and print full JSON on stdout only.
    if args.json:
        print(json.dumps([row for row, _, _ in shown], indent=2))
        return 0

    # Build and print one compact line per market.
    for row, ok, reason in shown:
        line = describe(row)
        if args.all and not ok:
            line += f" | not fundable: {reason}"
        print(line)
    log.info("%s market(s) shown.", len(shown))
    if dropped_ended and not args.all:
        log.info("%s ended market(s) hidden (use --all to see them).", dropped_ended)
    return 0


if __name__ == "__main__":
    sys.exit(main())
