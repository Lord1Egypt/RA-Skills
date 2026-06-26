#!/usr/bin/env python3
"""Small BrickEconomy API CLI used by the BrickEconomy AFOL skill.

The CLI intentionally sticks to the checked-in BrickEconomy OpenAPI reference
and Python's standard library. Secrets come from environment variables, not
flags, so commands can be copied into agent transcripts without leaking API
keys.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

DEFAULT_BASE_URL = "https://www.brickeconomy.com/api/v1"
READ_TIMEOUT_SECONDS = 30
CURRENCY_CODES = [
    "USD",
    "GBP",
    "CAD",
    "AUD",
    "CNY",
    "KRW",
    "EUR",
    "JPY",
    "CHF",
    "INR",
    "BRL",
    "RUB",
    "ZAR",
    "MXN",
    "SGD",
    "HKD",
    "SEK",
    "NZD",
    "NOK",
    "TRY",
    "DKK",
    "PLN",
]


class BrickEconomyCliError(RuntimeError):
    """Expected CLI/API failure with a clean user-facing message."""


class BrickEconomyClient:
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL, timeout: int = READ_TIMEOUT_SECONDS):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        query = urllib.parse.urlencode(clean_params(params or {}), doseq=True)
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{query}"
        headers = {"Accept": "application/json", "x-apikey": self.api_key}
        return self._request("GET", url, headers)

    def _request(self, method: str, url: str, headers: dict[str, str]) -> Any:
        request = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:  # noqa: S310 - URL is API base/user input by design.
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise BrickEconomyCliError(f"BrickEconomy API HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise BrickEconomyCliError(f"BrickEconomy API request failed: {exc.reason}") from exc

        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw


def clean_params(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def require_api_key() -> str:
    api_key = os.getenv("BRICKECONOMY_API_KEY")
    if not api_key:
        raise BrickEconomyCliError("BRICKECONOMY_API_KEY is required")
    return api_key


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=os.getenv("BRICKECONOMY_BASE_URL", DEFAULT_BASE_URL), help="BrickEconomy API base URL")
    parser.add_argument("--timeout", type=int, default=READ_TIMEOUT_SECONDS, help="HTTP timeout in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Print request shape without calling BrickEconomy")


def add_currency(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--currency", choices=CURRENCY_CODES, default=None, help="Currency code for value fields; API default is USD")


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser], name: str, help_text: str) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=help_text)
    add_common(parser)
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brickeconomy", description="BrickEconomy API CLI for AFOL agent skills")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = add_parser(subparsers, "set", "Get BrickEconomy set value and forecast data")
    p.add_argument("--set-number", required=True, help="Set number with or without suffix, e.g. 10236 or 10236-1")
    add_currency(p)
    p.set_defaults(handler=cmd_set)

    p = add_parser(subparsers, "minifig", "Get BrickEconomy minifig value and forecast data")
    p.add_argument("--minifig-number", required=True, help="Minifig number, e.g. sw0509")
    add_currency(p)
    p.set_defaults(handler=cmd_minifig)

    p = add_parser(subparsers, "collection-sets", "Get authenticated user's BrickEconomy set collection")
    add_currency(p)
    p.set_defaults(handler=cmd_collection_sets)

    p = add_parser(subparsers, "collection-minifigs", "Get authenticated user's BrickEconomy minifig collection")
    add_currency(p)
    p.set_defaults(handler=cmd_collection_minifigs)

    p = add_parser(subparsers, "sales-ledger", "Get authenticated user's BrickEconomy sales ledger")
    p.set_defaults(handler=cmd_sales_ledger)

    return parser


def client_from_args(args: argparse.Namespace) -> BrickEconomyClient:
    return BrickEconomyClient(require_api_key(), args.base_url, args.timeout)


def dry_run(args: argparse.Namespace, path: str, params: dict[str, Any] | None = None) -> bool:
    if not args.dry_run:
        return False
    print_json(
        {
            "dry_run": True,
            "command": args.command,
            "method": "GET",
            "base_url": args.base_url,
            "path": path,
            "query": clean_params(params or {}),
            "headers": {"x-apikey": "[from BRICKECONOMY_API_KEY]"},
        }
    )
    return True


def encode_path_segment(value: str) -> str:
    return urllib.parse.quote(value, safe="")


def cmd_set(args: argparse.Namespace) -> Any:
    path = f"/set/{encode_path_segment(args.set_number)}"
    params = {"currency": args.currency}
    if dry_run(args, path, params):
        return None
    return client_from_args(args).get(path, params)


def cmd_minifig(args: argparse.Namespace) -> Any:
    path = f"/minifig/{encode_path_segment(args.minifig_number)}"
    params = {"currency": args.currency}
    if dry_run(args, path, params):
        return None
    return client_from_args(args).get(path, params)


def cmd_collection_sets(args: argparse.Namespace) -> Any:
    path = "/collection/sets"
    params = {"currency": args.currency}
    if dry_run(args, path, params):
        return None
    return client_from_args(args).get(path, params)


def cmd_collection_minifigs(args: argparse.Namespace) -> Any:
    path = "/collection/minifigs"
    params = {"currency": args.currency}
    if dry_run(args, path, params):
        return None
    return client_from_args(args).get(path, params)


def cmd_sales_ledger(args: argparse.Namespace) -> Any:
    # Provider quirk: the checked-in OpenAPI spec does not define a currency
    # parameter for /salesledger, unlike set/minifig/collection value endpoints.
    path = "/salesledger"
    if dry_run(args, path):
        return None
    return client_from_args(args).get(path)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
        if result is not None:
            print_json(result)
        return 0
    except BrickEconomyCliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
