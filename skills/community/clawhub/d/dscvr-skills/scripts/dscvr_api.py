#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "httpx>=0.27",
# ]
# ///
"""DSCVR Intelligence API client.

A unified CLI for querying DSCVR's crypto intelligence endpoints.
Handles HMAC-SHA256 authentication automatically.

Environment variables:
    DSCVR_API_KEY       — 16-character public API key (required)
    DSCVR_SECRET_KEY    — 32-character secret key (required)
    DSCVR_API_BASE_URL  — API server base URL (default: https://dscvr.one)

Usage:
    uv run scripts/dscvr_api.py categories
    uv run scripts/dscvr_api.py events [--category CAT] [--date YYYY-MM-DD] [--page N] [--limit N]
    uv run scripts/dscvr_api.py event-detail --event-id ID
    uv run scripts/dscvr_api.py smart-money [--keyword KW] [--win-rate HOT,STEADY] [--sort TOTAL_PNL] [--page N] [--limit N]
    uv run scripts/dscvr_api.py market-categories [--source polymarket]
    uv run scripts/dscvr_api.py markets [--source SRC] [--category CAT] [--smart-filter all|smart_money] [--sort FIELD] [--page N] [--limit N]
    uv run scripts/dscvr_api.py event-traders --event-id ID [--page N] [--limit N]
    uv run scripts/dscvr_api.py ai-categories
    uv run scripts/dscvr_api.py ai-events [--category CAT] [--platform PLAT] [--active] [--page N] [--limit N]
    uv run scripts/dscvr_api.py ai-search --query KEYWORD [--page N] [--limit N]
    uv run scripts/dscvr_api.py ai-event-detail --provider PROVIDER --event-id ID
    uv run scripts/dscvr_api.py ai-orderbook [--kalshi-id ID] [--polymarket-id ID]
    uv run scripts/dscvr_api.py social-graphql --query GRAPHQL_QUERY
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import httpx

# Import auth from the same scripts/ directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auth import generate_auth_headers  # noqa: E402


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def get_config() -> tuple[str, str, str]:
    """Read configuration from environment variables.

    Returns:
        Tuple of (api_key, secret_key, base_url).

    Raises:
        SystemExit: If required environment variables are missing.
    """
    api_key = os.environ.get("DSCVR_API_KEY", "")
    secret_key = os.environ.get("DSCVR_SECRET_KEY", "")
    base_url = os.environ.get("DSCVR_API_BASE_URL", "https://dscvr.one")

    if not api_key or not secret_key:
        print(
            "Error: DSCVR_API_KEY and DSCVR_SECRET_KEY environment variables are required.\n"
            "\n"
            "Set them with:\n"
            '  export DSCVR_API_KEY="your_api_key"\n'
            '  export DSCVR_SECRET_KEY="your_secret_key"\n'
            "\n"
            "Get your API credentials at https://dscvr.one/subscription",
            file=sys.stderr,
        )
        sys.exit(1)

    return api_key, secret_key, base_url.rstrip("/")


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------

def _handle_response(response: httpx.Response, base_url: str) -> Any:
    """Handle HTTP response, raising on errors."""
    if response.status_code == 401:
        print(
            "Error: Authentication failed (401).\n"
            "Possible causes:\n"
            "  - Invalid API key or secret key\n"
            "  - System clock is out of sync (timestamp must be within 5 minutes)\n"
            "  - API key has been revoked",
            file=sys.stderr,
        )
        sys.exit(1)
    elif response.status_code == 403:
        print(
            "Error: API key is temporarily banned (403).\n"
            "This happens after an authentication failure. Wait 60 seconds and try again.",
            file=sys.stderr,
        )
        sys.exit(1)
    elif response.status_code == 429:
        print(
            "Error: Rate limit exceeded (429).\n"
            "Default limit is 100 requests per minute. Wait and try again.",
            file=sys.stderr,
        )
        sys.exit(1)
    elif response.status_code >= 400:
        print(f"Error: HTTP {response.status_code} — {response.text}", file=sys.stderr)
        sys.exit(1)

    return response.json()


def api_get(base_url: str, path: str, headers: dict[str, str], params: dict[str, Any] | None = None) -> Any:
    """Make an authenticated GET request to the DSCVR API."""
    url = f"{base_url}{path}"
    if params:
        params = {k: v for k, v in params.items() if v is not None}
    try:
        with httpx.Client(timeout=90.0) as client:
            response = client.get(url, headers=headers, params=params)
    except httpx.ConnectError:
        print(f"Error: Cannot connect to {base_url}. Is the server running?", file=sys.stderr)
        sys.exit(1)
    except httpx.TimeoutException:
        print(f"Error: Request to {url} timed out.", file=sys.stderr)
        sys.exit(1)
    return _handle_response(response, base_url)


def api_post(base_url: str, path: str, headers: dict[str, str], body: dict[str, Any] | None = None) -> Any:
    """Make an authenticated POST request to the DSCVR API."""
    url = f"{base_url}{path}"
    if body:
        body = {k: v for k, v in body.items() if v is not None}
    try:
        with httpx.Client(timeout=90.0) as client:
            response = client.post(url, headers={**headers, "Content-Type": "application/json"}, json=body or {})
    except httpx.ConnectError:
        print(f"Error: Cannot connect to {base_url}. Is the server running?", file=sys.stderr)
        sys.exit(1)
    except httpx.TimeoutException:
        print(f"Error: Request to {url} timed out.", file=sys.stderr)
        sys.exit(1)
    return _handle_response(response, base_url)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_categories(args: argparse.Namespace) -> None:
    """Fetch and display all event categories."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)
    data = api_get(base_url, "/developer/v1/product/news/event_category", headers)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_events(args: argparse.Namespace) -> None:
    """Fetch and display paginated event list."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params: dict[str, Any] = {}
    if args.category:
        params["category"] = args.category
    if args.date:
        params["date"] = args.date
    if args.page:
        params["page"] = args.page
    if args.limit:
        params["limit"] = args.limit

    data = api_get(base_url, "/developer/v1/product/news/event_list", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_event_detail(args: argparse.Namespace) -> None:
    """Fetch and display a single event's details."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params = {"event_id": args.event_id}
    data = api_get(base_url, "/developer/v1/product/news/event_detail", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_smart_money(args: argparse.Namespace) -> None:
    """Fetch smart money trader list with filters."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    body: dict[str, Any] = {}
    if args.keyword:
        body["search_keyword"] = args.keyword
    if args.win_rate:
        body["win_rate_range"] = [x.strip() for x in args.win_rate.split(",")]
    if args.position_state:
        body["position_state"] = [x.strip() for x in args.position_state.split(",")]
    if args.tx_size:
        body["transaction_size"] = [x.strip() for x in args.tx_size.split(",")]
    if args.style:
        body["position_style"] = [x.strip() for x in args.style.split(",")]
    if args.identity:
        body["is_human"] = [x.strip() for x in args.identity.split(",")]
    if args.category:
        body["category"] = [x.strip() for x in args.category.split(",")]
    if args.sort:
        body["sort_by"] = args.sort
    if args.ascending is not None:
        body["is_ascending"] = args.ascending
    if args.limit is not None:
        body["limit"] = args.limit
    if args.page is not None:
        body["page"] = args.page

    data = api_post(base_url, "/developer/v1/product/market/smart_money/list", headers, body)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_market_categories(args: argparse.Namespace) -> None:
    """Fetch prediction market categories."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params: dict[str, Any] = {}
    if args.source:
        params["source"] = args.source

    data = api_get(base_url, "/developer/v1/product/market/market/category", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_markets(args: argparse.Namespace) -> None:
    """Fetch prediction market listings."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params: dict[str, Any] = {}
    if args.source:
        params["source"] = args.source
    if args.category:
        params["category"] = args.category
    if args.smart_filter:
        params["smart_filter"] = args.smart_filter
    if args.sort:
        params["sort_by"] = args.sort
    if args.limit is not None:
        params["limit"] = args.limit
    if args.page is not None:
        params["page"] = args.page

    data = api_get(base_url, "/developer/v1/product/market/market/list", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_event_traders(args: argparse.Namespace) -> None:
    """Fetch smart money traders for a specific event."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params: dict[str, Any] = {"event_id": args.event_id}
    if args.limit is not None:
        params["limit"] = args.limit
    if args.page is not None:
        params["page"] = args.page

    data = api_get(base_url, "/developer/v1/product/market/market/event_trader", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


# --- AI Discovery ---

def cmd_ai_categories(args: argparse.Namespace) -> None:
    """Fetch AI discovery categories."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)
    data = api_get(base_url, "/developer/v1/product/ai/category_list", headers)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_ai_events(args: argparse.Namespace) -> None:
    """Fetch AI discovery event list."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params: dict[str, Any] = {}
    if args.category:
        params["category"] = args.category
    if args.platform:
        params["platform"] = args.platform
    if args.active is not None:
        params["is_active"] = args.active
    if args.page is not None:
        params["page"] = args.page
    if args.limit is not None:
        params["limit"] = args.limit

    data = api_get(base_url, "/developer/v1/product/ai/event_list", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_ai_search(args: argparse.Namespace) -> None:
    """Search AI discovery events by keyword."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params: dict[str, Any] = {"query": args.query}
    if args.page is not None:
        params["page"] = args.page
    if args.limit is not None:
        params["limit"] = args.limit

    data = api_get(base_url, "/developer/v1/product/ai/event_search", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_ai_event_detail(args: argparse.Namespace) -> None:
    """Fetch AI discovery event detail."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params = {"provider": args.provider, "event_id": args.event_id}
    data = api_get(base_url, "/developer/v1/product/ai/event_detail", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_ai_orderbook(args: argparse.Namespace) -> None:
    """Fetch market orderbook data."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    params: dict[str, Any] = {}
    if args.kalshi_id:
        params["kalshi_market_id"] = args.kalshi_id
    if args.polymarket_id:
        params["polymarket_market_id"] = args.polymarket_id

    if not params:
        print("Error: At least one of --kalshi-id or --polymarket-id is required.", file=sys.stderr)
        sys.exit(1)

    data = api_get(base_url, "/developer/v1/product/ai/market_orderbook", headers, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))


# --- Social ---

def cmd_social_graphql(args: argparse.Namespace) -> None:
    """Execute a GraphQL query against the DSCVR social API."""
    api_key, secret_key, base_url = get_config()
    headers = generate_auth_headers(api_key, secret_key)

    body = {"query": args.query}
    data = api_post(base_url, "/developer/v1/product/social/graphql", headers, body)
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="dscvr_api",
        description="DSCVR Intelligence API — query crypto news events and market data.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # categories
    subparsers.add_parser("categories", help="List all event categories")

    # events
    events_parser = subparsers.add_parser("events", help="List events (paginated)")
    events_parser.add_argument("--category", type=str, help="Filter by category name")
    events_parser.add_argument("--date", type=str, help="Filter by date (YYYY-MM-DD)")
    events_parser.add_argument("--page", type=int, default=None, help="Page number (default: 1)")
    events_parser.add_argument("--limit", type=int, default=None, help="Results per page (default: 10)")

    # event-detail
    detail_parser = subparsers.add_parser("event-detail", help="Get event details")
    detail_parser.add_argument("--event-id", required=True, type=str, help="Event ID")

    # --- Smart Money & Prediction Markets ---

    # smart-money
    sm_parser = subparsers.add_parser("smart-money", help="List smart money traders")
    sm_parser.add_argument("--keyword", type=str, help="Fuzzy search by name or bio")
    sm_parser.add_argument("--win-rate", type=str, help="Win rate filter (comma-separated: HOT,STEADY,REVERSE)")
    sm_parser.add_argument("--position-state", type=str, help="Position state (comma-separated: ACTIVE,STREAK,SAFE)")
    sm_parser.add_argument("--tx-size", type=str, help="Transaction size (comma-separated: WHALE,MID,SMALL,SMALL_LOSS,MID_LOSS)")
    sm_parser.add_argument("--style", type=str, help="Position style (comma-separated: SWING,DIAMOND,HOT_ONLY)")
    sm_parser.add_argument("--identity", type=str, help="Identity type (comma-separated: BOT,HUMAN,INSIDER)")
    sm_parser.add_argument("--category", type=str, help="Domain category (comma-separated: politics,sports,crypto,economy,...)")
    sm_parser.add_argument("--sort", type=str, help="Sort field (TOTAL_PNL,WIN_RATE,TOTAL_TRADE_COUNT,TOTAL_TURNOVER,AVG_HOLD_TIME)")
    sm_parser.add_argument("--ascending", action="store_true", default=None, help="Sort ascending (default: descending)")
    sm_parser.add_argument("--page", type=int, default=None, help="Page number (default: 1)")
    sm_parser.add_argument("--limit", type=int, default=None, help="Results per page (default: 20, max: 100)")

    # market-categories
    mc_parser = subparsers.add_parser("market-categories", help="List prediction market categories")
    mc_parser.add_argument("--source", type=str, help="Data source (default: polymarket)")

    # markets
    mkt_parser = subparsers.add_parser("markets", help="List prediction markets")
    mkt_parser.add_argument("--source", type=str, help="Data source (default: polymarket)")
    mkt_parser.add_argument("--category", type=str, help="Category filter (default: all)")
    mkt_parser.add_argument("--smart-filter", type=str, help="Smart money filter: all or smart_money")
    mkt_parser.add_argument("--sort", type=str, help="Sort field (prefix with - for asc): smart_money_activity, volume_24h, liquidity, close_time")
    mkt_parser.add_argument("--page", type=int, default=None, help="Page number (default: 1)")
    mkt_parser.add_argument("--limit", type=int, default=None, help="Results per page (default: 20, max: 100)")

    # event-traders
    et_parser = subparsers.add_parser("event-traders", help="List smart money traders for an event")
    et_parser.add_argument("--event-id", required=True, type=str, help="Event ID")
    et_parser.add_argument("--page", type=int, default=None, help="Page number (default: 1)")
    et_parser.add_argument("--limit", type=int, default=None, help="Results per page (default: 5, max: 10)")

    # --- AI Discovery ---

    # ai-categories
    subparsers.add_parser("ai-categories", help="List AI discovery categories")

    # ai-events
    aie_parser = subparsers.add_parser("ai-events", help="List AI discovery events")
    aie_parser.add_argument("--category", type=str, help="Category filter (default: All)")
    aie_parser.add_argument("--platform", type=str, help="Platform filter")
    aie_parser.add_argument("--active", action="store_true", default=None, help="Only active events")
    aie_parser.add_argument("--page", type=int, default=None, help="Page number (default: 1)")
    aie_parser.add_argument("--limit", type=int, default=None, help="Results per page (default: 10)")

    # ai-search
    ais_parser = subparsers.add_parser("ai-search", help="Search AI discovery events by keyword")
    ais_parser.add_argument("--query", required=True, type=str, help="Search keyword")
    ais_parser.add_argument("--page", type=int, default=None, help="Page number (default: 1)")
    ais_parser.add_argument("--limit", type=int, default=None, help="Results per page (default: 10)")

    # ai-event-detail
    aid_parser = subparsers.add_parser("ai-event-detail", help="Get AI discovery event detail")
    aid_parser.add_argument("--provider", required=True, type=str, help="Provider name")
    aid_parser.add_argument("--event-id", required=True, type=str, help="Event ID")

    # ai-orderbook
    aio_parser = subparsers.add_parser("ai-orderbook", help="Get market orderbook data")
    aio_parser.add_argument("--kalshi-id", type=str, help="Kalshi market ID")
    aio_parser.add_argument("--polymarket-id", type=str, help="Polymarket market ID")

    # --- Social ---

    # social-graphql
    sg_parser = subparsers.add_parser("social-graphql", help="Execute a DSCVR social GraphQL query")
    sg_parser.add_argument("--query", required=True, type=str, help='GraphQL query string, e.g. "{ userByName(name: \\"alice\\") { id username } }"')

    return parser


def main() -> None:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "categories": cmd_categories,
        "events": cmd_events,
        "event-detail": cmd_event_detail,
        "smart-money": cmd_smart_money,
        "market-categories": cmd_market_categories,
        "markets": cmd_markets,
        "event-traders": cmd_event_traders,
        "ai-categories": cmd_ai_categories,
        "ai-events": cmd_ai_events,
        "ai-search": cmd_ai_search,
        "ai-event-detail": cmd_ai_event_detail,
        "ai-orderbook": cmd_ai_orderbook,
        "social-graphql": cmd_social_graphql,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
