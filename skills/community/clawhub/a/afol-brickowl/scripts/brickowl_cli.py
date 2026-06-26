#!/usr/bin/env python3
"""Small BrickOwl API CLI used by the BrickOwl AFOL skill.

The CLI intentionally sticks to the checked-in BrickOwl OpenAPI reference and
Python's standard library. Secrets come from environment variables, not flags,
so commands can be copied into agent transcripts without leaking API keys.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable

DEFAULT_BASE_URL = "https://api.brickowl.com/v1"
READ_TIMEOUT_SECONDS = 30
WRITE_COMMANDS = {"inventory-create", "inventory-update", "inventory-delete", "wishlist-create", "bulk"}


class BrickOwlCliError(RuntimeError):
    """Expected CLI/API failure with a clean user-facing message."""


class BrickOwlClient:
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL, timeout: int = READ_TIMEOUT_SECONDS):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, path: str, params: dict[str, Any]) -> Any:
        query = {"key": self.api_key, **clean_params(params)}
        url = f"{self.base_url}{path}?{urllib.parse.urlencode(query, doseq=True)}"
        return self._request("GET", url)

    def post_form(self, path: str, fields: dict[str, Any]) -> Any:
        body = urllib.parse.urlencode({"key": self.api_key, **clean_params(fields)}, doseq=True).encode()
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        return self._request("POST", url, body, headers)

    def _request(self, method: str, url: str, body: bytes | None = None, headers: dict[str, str] | None = None) -> Any:
        request = urllib.request.Request(url, data=body, headers=headers or {"Accept": "application/json"}, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:  # noqa: S310 - URL is API base/user input by design.
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise BrickOwlCliError(f"BrickOwl API HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise BrickOwlCliError(f"BrickOwl API request failed: {exc.reason}") from exc

        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw


def clean_params(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def require_api_key() -> str:
    api_key = os.getenv("BRICKOWL_API_KEY")
    if not api_key:
        raise BrickOwlCliError("BRICKOWL_API_KEY is required")
    return api_key


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))


def dry_run(command: str, path: str, fields: dict[str, Any]) -> None:
    print_json(
        {
            "dry_run": True,
            "command": command,
            "method": "POST",
            "path": path,
            "form_fields": {"key": "[from BRICKOWL_API_KEY]", **clean_params(fields)},
        }
    )


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=os.getenv("BRICKOWL_BASE_URL", DEFAULT_BASE_URL), help="BrickOwl API base URL")
    parser.add_argument("--timeout", type=int, default=READ_TIMEOUT_SECONDS, help="HTTP timeout in seconds")


def add_write_safety(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--yes", action="store_true", help="Actually execute this mutating request")
    parser.add_argument("--dry-run", action="store_true", help="Print request shape without calling BrickOwl")


def add_optional(parser: argparse.ArgumentParser, *names: str) -> None:
    for name in names:
        parser.add_argument(f"--{name.replace('_', '-')}", dest=name)


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser], name: str, help_text: str) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=help_text)
    add_common(parser)
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brickowl", description="BrickOwl API CLI for AFOL agent skills")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = add_parser(subparsers, "user", "Show the authenticated BrickOwl user")
    p.set_defaults(handler=cmd_user)

    p = add_parser(subparsers, "catalog-search", "Search the BrickOwl catalog by text")
    p.add_argument("--query", required=True)
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--type")
    p.add_argument("--missing-data", action="store_true")
    p.set_defaults(handler=cmd_catalog_search)

    p = add_parser(subparsers, "id-lookup", "Look up BOIDs by known external IDs")
    p.add_argument("--id", required=True)
    p.add_argument("--type", choices=["Part", "Set", "Minifigure", "Gear", "Sticker", "Minibuild", "Instructions", "Packaging"])
    p.add_argument("--id-type", choices=["item_no", "design_id", "bl_item_no", "set_number"])
    p.set_defaults(handler=cmd_id_lookup)

    p = add_parser(subparsers, "inventory-list", "List authenticated store inventory")
    p.add_argument("--page", type=int, default=1)
    p.set_defaults(handler=cmd_inventory_list)

    p = add_parser(subparsers, "inventory-create", "Create a BrickOwl inventory lot")
    add_write_safety(p)
    p.add_argument("--boid", required=True)
    p.add_argument("--quantity", required=True, type=int)
    p.add_argument("--price", required=True)
    p.add_argument("--condition", required=True, choices=["news", "newc", "newi", "usedc", "usedi", "usedn", "usedg", "useda", "other"])
    add_optional(p, "color_id", "external_id")
    p.set_defaults(handler=cmd_inventory_create)

    p = add_parser(subparsers, "inventory-update", "Update an existing BrickOwl inventory lot")
    add_write_safety(p)
    p.add_argument("--lot-id", type=int)
    p.add_argument("--external-lot-id")
    p.add_argument("--absolute-quantity", type=int)
    p.add_argument("--relative-quantity", type=int)
    p.add_argument("--price")
    p.add_argument("--condition")
    p.add_argument("--for-sale", choices=["true", "false"])
    p.add_argument("--public-note")
    p.add_argument("--personal-note")
    p.set_defaults(handler=cmd_inventory_update)

    p = add_parser(subparsers, "inventory-delete", "Delete an existing BrickOwl inventory lot")
    add_write_safety(p)
    p.add_argument("--lot-id", type=int)
    p.add_argument("--external-lot-id")
    p.set_defaults(handler=cmd_inventory_delete)

    p = add_parser(subparsers, "orders", "List store orders")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--status", choices=["Pending", "Processing", "Shipped", "Received", "Cancelled"])
    p.set_defaults(handler=cmd_orders)

    p = add_parser(subparsers, "order", "View a store order")
    p.add_argument("--order-id", required=True, type=int)
    p.set_defaults(handler=cmd_order)

    p = add_parser(subparsers, "wishlist-create", "Create a BrickOwl wishlist")
    add_write_safety(p)
    p.add_argument("--name", required=True)
    p.add_argument("--description")
    p.set_defaults(handler=cmd_wishlist_create)

    p = add_parser(subparsers, "bulk", "Execute a BrickOwl bulk request payload")
    add_write_safety(p)
    p.add_argument("--requests-json", required=True, help="JSON string accepted by BrickOwl's requests field")
    p.set_defaults(handler=cmd_bulk)

    return parser


def client_from_args(args: argparse.Namespace) -> BrickOwlClient:
    return BrickOwlClient(require_api_key(), args.base_url, args.timeout)


def ensure_write_allowed(args: argparse.Namespace, path: str, fields: dict[str, Any]) -> bool:
    if args.dry_run:
        dry_run(args.command, path, fields)
        return False
    if not args.yes:
        raise BrickOwlCliError(f"{args.command} mutates BrickOwl data; rerun with --dry-run to inspect or --yes after explicit user confirmation")
    return True


def require_identifier(args: argparse.Namespace) -> None:
    if not args.lot_id and not args.external_lot_id:
        raise BrickOwlCliError("provide --lot-id or --external-lot-id")


def require_any_change(args: argparse.Namespace, field_names: Iterable[str]) -> None:
    if not any(getattr(args, field) is not None for field in field_names):
        raise BrickOwlCliError("provide at least one field to update")


def cmd_user(args: argparse.Namespace) -> Any:
    return client_from_args(args).get("/user/details", {})


def cmd_catalog_search(args: argparse.Namespace) -> Any:
    return client_from_args(args).get("/catalog/search", {"query": args.query, "page": args.page, "type": args.type, "missing_data": args.missing_data or None})


def cmd_id_lookup(args: argparse.Namespace) -> Any:
    return client_from_args(args).get("/catalog/id_lookup", {"id": args.id, "type": args.type, "id_type": args.id_type})


def cmd_inventory_list(args: argparse.Namespace) -> Any:
    return client_from_args(args).get("/inventory/list", {"page": args.page})


def cmd_inventory_create(args: argparse.Namespace) -> Any:
    fields = {
        "boid": args.boid,
        "quantity": args.quantity,
        "price": args.price,
        "condition": args.condition,
        "color_id": args.color_id,
        "external_id": args.external_id,
    }
    path = "/inventory/create"
    if not ensure_write_allowed(args, path, fields):
        return None
    return client_from_args(args).post_form(path, fields)


def cmd_inventory_update(args: argparse.Namespace) -> Any:
    require_identifier(args)
    change_fields = ["absolute_quantity", "relative_quantity", "price", "condition", "for_sale", "public_note", "personal_note"]
    require_any_change(args, change_fields)
    fields = {"lot_id": args.lot_id, "external_lot_id": args.external_lot_id, **{field: getattr(args, field) for field in change_fields}}
    path = "/inventory/update"
    if not ensure_write_allowed(args, path, fields):
        return None
    return client_from_args(args).post_form(path, fields)


def cmd_inventory_delete(args: argparse.Namespace) -> Any:
    require_identifier(args)
    fields = {"lot_id": args.lot_id, "external_lot_id": args.external_lot_id, "delete": "true"}
    path = "/inventory/update"
    if not ensure_write_allowed(args, path, fields):
        return None
    return client_from_args(args).post_form(path, fields)


def cmd_orders(args: argparse.Namespace) -> Any:
    return client_from_args(args).get("/order/list", {"page": args.page, "status": args.status})


def cmd_order(args: argparse.Namespace) -> Any:
    return client_from_args(args).get("/order/view", {"order_id": args.order_id})


def cmd_wishlist_create(args: argparse.Namespace) -> Any:
    fields = {"name": args.name, "description": args.description}
    path = "/wishlist/create_list"
    if not ensure_write_allowed(args, path, fields):
        return None
    return client_from_args(args).post_form(path, fields)


def cmd_bulk(args: argparse.Namespace) -> Any:
    # BrickOwl accepts this as a form field. Validate JSON locally so the caller
    # catches shell quoting mistakes before sending a mutating batch.
    try:
        json.loads(args.requests_json)
    except json.JSONDecodeError as exc:
        raise BrickOwlCliError(f"--requests-json is not valid JSON: {exc}") from exc
    fields = {"requests": args.requests_json}
    path = "/bulk"
    if not ensure_write_allowed(args, path, fields):
        return None
    return client_from_args(args).post_form(path, fields)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
        if result is not None:
            print_json(result)
        return 0
    except BrickOwlCliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
