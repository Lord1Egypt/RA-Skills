#!/usr/bin/env python3
"""Small BrickLink API CLI used by the BrickLink AFOL skill.

The CLI is self-contained and uses only Python's standard library. It signs
requests with OAuth 1.0 credentials from environment variables and keeps write
operations behind --yes / --dry-run guards.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable

DEFAULT_BASE_URL = "https://api.bricklink.com/api/store/v1"
READ_TIMEOUT_SECONDS = 30
WRITE_METHODS = {"POST", "PUT", "DELETE"}
REQUIRED_ENV = (
    "BRICKLINK_API_CONSUMER_KEY",
    "BRICKLINK_API_CONSUMER_SECRET",
    "BRICKLINK_API_TOKEN_VALUE",
    "BRICKLINK_API_TOKEN_SECRET",
)
ITEM_TYPES = ("MINIFIG", "PART", "SET", "BOOK", "GEAR", "CATALOG", "INSTRUCTION", "ORIGINAL_BOX")


class BrickLinkCliError(RuntimeError):
    """Expected CLI/API failure with a clean user-facing message."""


class BrickLinkClient:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        token_value: str,
        token_secret: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = READ_TIMEOUT_SECONDS,
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_value = token_value
        self.token_secret = token_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def request(self, method: str, path: str, params: dict[str, Any] | None = None, body: Any | None = None) -> Any:
        method = method.upper()
        params = clean_params(params or {})
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"
        data = None
        headers = {"Accept": "application/json"}
        if body is not None:
            data = json.dumps(body, separators=(",", ":")).encode("utf-8")
            headers["Content-Type"] = "application/json"
        headers["Authorization"] = self.oauth_header(method, url)
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:  # noqa: S310 - intentional API client.
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise BrickLinkCliError(f"BrickLink API HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise BrickLinkCliError(f"BrickLink API request failed: {exc.reason}") from exc
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw

    def oauth_header(self, method: str, url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        oauth_params = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_nonce": secrets.token_hex(16),
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_token": self.token_value,
            "oauth_version": "1.0",
        }
        normalized_params = query_pairs + list(oauth_params.items())
        normalized_params.sort(key=lambda pair: (percent_encode(pair[0]), percent_encode(pair[1])))
        normalized = "&".join(f"{percent_encode(k)}={percent_encode(v)}" for k, v in normalized_params)
        base_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
        signature_base = "&".join([method.upper(), percent_encode(base_url), percent_encode(normalized)])
        signing_key = f"{percent_encode(self.consumer_secret)}&{percent_encode(self.token_secret)}".encode("utf-8")
        digest = hmac.new(signing_key, signature_base.encode("utf-8"), hashlib.sha1).digest()
        oauth_params["oauth_signature"] = base64.b64encode(digest).decode("ascii")
        return "OAuth " + ", ".join(f'{percent_encode(k)}="{percent_encode(v)}"' for k, v in sorted(oauth_params.items()))


def percent_encode(value: Any) -> str:
    return urllib.parse.quote(str(value), safe="~-._")


def clean_params(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def load_credentials() -> tuple[str, str, str, str]:
    values = {name: os.getenv(name) for name in REQUIRED_ENV}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise BrickLinkCliError("missing env vars: " + ", ".join(missing))
    return tuple(values[name] or "" for name in REQUIRED_ENV)  # type: ignore[return-value]


def client_from_args(args: argparse.Namespace) -> BrickLinkClient:
    return BrickLinkClient(*load_credentials(), base_url=args.base_url, timeout=args.timeout)


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))


def parse_json_payload(raw: str | None) -> Any:
    if raw in (None, ""):
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BrickLinkCliError(f"payload is not valid JSON: {exc}") from exc


def dry_run(command: str, method: str, path: str, params: dict[str, Any] | None = None, body: Any | None = None) -> None:
    print_json(
        {
            "dry_run": True,
            "command": command,
            "method": method.upper(),
            "path": path,
            "query": clean_params(params or {}),
            "json_body": body,
            "auth": "OAuth1 from BRICKLINK_API_* environment variables",
        }
    )


def ensure_write_allowed(args: argparse.Namespace, method: str, path: str, params: dict[str, Any] | None = None, body: Any | None = None) -> bool:
    if method.upper() not in WRITE_METHODS:
        return True
    if args.dry_run:
        dry_run(args.command, method, path, params, body)
        return False
    if not args.yes:
        raise BrickLinkCliError(f"{args.command} mutates BrickLink data; rerun with --dry-run to inspect or --yes after explicit user confirmation")
    return True


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=os.getenv("BRICKLINK_API_BASE_URL", DEFAULT_BASE_URL), help="BrickLink API base URL")
    parser.add_argument("--timeout", type=int, default=READ_TIMEOUT_SECONDS, help="HTTP timeout in seconds")


def add_write_safety(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--yes", action="store_true", help="Actually execute this mutating request")
    parser.add_argument("--dry-run", action="store_true", help="Print request shape without calling BrickLink")


def add_optional(parser: argparse.ArgumentParser, *names: str) -> None:
    for name in names:
        parser.add_argument(f"--{name.replace('_', '-')}", dest=name)


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser], name: str, help_text: str) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=help_text)
    add_common(parser)
    return parser


def add_item_path(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--type", required=True, choices=ITEM_TYPES)
    parser.add_argument("--no", required=True, help="BrickLink item number")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bricklink", description="BrickLink OAuth1 API CLI for AFOL agent skills")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = add_parser(subparsers, "colors", "List BrickLink colors")
    p.set_defaults(handler=cmd_colors)

    p = add_parser(subparsers, "color", "Show one BrickLink color")
    p.add_argument("--color-id", required=True, type=int)
    p.set_defaults(handler=cmd_color)

    p = add_parser(subparsers, "categories", "List BrickLink categories")
    p.set_defaults(handler=cmd_categories)

    p = add_parser(subparsers, "category", "Show one BrickLink category")
    p.add_argument("--category-id", required=True, type=int)
    p.set_defaults(handler=cmd_category)

    p = add_parser(subparsers, "item", "Look up one BrickLink catalog item")
    add_item_path(p)
    p.set_defaults(handler=cmd_item)

    p = add_parser(subparsers, "item-price", "Get the BrickLink price guide for an item")
    add_item_path(p)
    add_optional(p, "color_id", "country_code", "currency_code")
    p.add_argument("--guide-type", choices=["sold", "stock"], default="stock")
    p.add_argument("--new-or-used", choices=["N", "U"], default="N")
    p.add_argument("--region", choices=["asia", "africa", "north_america", "south_america", "middle_east", "europe", "eu", "oceania"])
    p.add_argument("--vat", choices=["N", "Y", "O"], default="N")
    p.set_defaults(handler=cmd_item_price)

    p = add_parser(subparsers, "item-colors", "List known colors for an item")
    add_item_path(p)
    p.set_defaults(handler=cmd_item_colors)

    p = add_parser(subparsers, "item-images", "Get item images for a color")
    add_item_path(p)
    p.add_argument("--color-id", required=True, type=int)
    p.set_defaults(handler=cmd_item_images)

    p = add_parser(subparsers, "item-supersets", "Get supersets containing an item")
    add_item_path(p)
    add_optional(p, "color_id")
    p.set_defaults(handler=cmd_item_supersets)

    p = add_parser(subparsers, "item-subsets", "Get subsets/contents for an item or set")
    add_item_path(p)
    add_optional(p, "color_id", "box")
    p.add_argument("--break-minifigs", choices=["Y", "N"])
    p.add_argument("--break-subsets", choices=["Y", "N"])
    p.set_defaults(handler=cmd_item_subsets)

    p = add_parser(subparsers, "item-mapping", "Map BrickLink PART number + color to LEGO Element IDs")
    p.add_argument("--type", default="PART", choices=["PART"])
    p.add_argument("--no", required=True)
    p.add_argument("--color-id", type=int)
    p.set_defaults(handler=cmd_item_mapping)

    p = add_parser(subparsers, "element-mapping", "Map a LEGO Element ID to BrickLink item data")
    p.add_argument("--element-id", required=True)
    p.set_defaults(handler=cmd_element_mapping)

    p = add_parser(subparsers, "orders", "List orders")
    p.add_argument("--direction", choices=["in", "out"], default="in")
    p.add_argument("--status")
    p.add_argument("--filed", choices=["true", "false"])
    p.set_defaults(handler=cmd_orders)

    p = add_parser(subparsers, "order", "View one order")
    p.add_argument("--order-id", required=True)
    p.set_defaults(handler=cmd_order)

    p = add_parser(subparsers, "order-items", "View order line items")
    p.add_argument("--order-id", required=True)
    p.set_defaults(handler=cmd_order_items)

    p = add_parser(subparsers, "order-messages", "View order messages")
    p.add_argument("--order-id", required=True)
    p.set_defaults(handler=cmd_order_messages)

    p = add_parser(subparsers, "order-feedback", "View order feedback")
    p.add_argument("--order-id", required=True)
    p.set_defaults(handler=cmd_order_feedback)

    p = add_parser(subparsers, "inventory-list", "List store inventory")
    add_optional(p, "item_type", "status", "category_id", "color_id")
    p.set_defaults(handler=cmd_inventory_list)

    p = add_parser(subparsers, "inventory", "View one inventory lot")
    p.add_argument("--inventory-id", required=True)
    p.set_defaults(handler=cmd_inventory)

    p = add_parser(subparsers, "feedback", "List feedback")
    p.add_argument("--direction", choices=["in", "out"], default="in")
    p.set_defaults(handler=cmd_feedback)

    p = add_parser(subparsers, "feedback-view", "View one feedback record")
    p.add_argument("--feedback-id", required=True)
    p.set_defaults(handler=cmd_feedback_view)

    p = add_parser(subparsers, "notifications", "List notifications")
    p.set_defaults(handler=cmd_notifications)

    p = add_parser(subparsers, "coupons", "List coupons")
    p.set_defaults(handler=cmd_coupons)

    p = add_parser(subparsers, "coupon", "View one coupon")
    p.add_argument("--coupon-id", required=True)
    p.set_defaults(handler=cmd_coupon)

    p = add_parser(subparsers, "shipping-methods", "List shipping methods")
    p.set_defaults(handler=cmd_shipping_methods)

    p = add_parser(subparsers, "shipping-method", "View one shipping method")
    p.add_argument("--method-id", required=True)
    p.set_defaults(handler=cmd_shipping_method)

    p = add_parser(subparsers, "member-ratings", "View member ratings")
    p.add_argument("--username", required=True)
    p.set_defaults(handler=cmd_member_ratings)

    p = add_parser(subparsers, "member-notes", "Read private notes for a member")
    p.add_argument("--username", required=True)
    p.set_defaults(handler=cmd_member_notes)

    for name, help_text, method, path_template in [
        ("inventory-create", "Create inventory lot(s)", "POST", "/inventories"),
        ("inventory-update", "Update an inventory lot", "PUT", "/inventories/{inventory_id}"),
        ("inventory-delete", "Delete an inventory lot", "DELETE", "/inventories/{inventory_id}"),
        ("order-update", "Update order details", "PUT", "/orders/{order_id}"),
        ("order-status", "Update order status", "PUT", "/orders/{order_id}/status"),
        ("order-payment-status", "Update order payment status", "PUT", "/orders/{order_id}/payment_status"),
        ("order-drive-thru", "Send order drive-thru action", "POST", "/orders/{order_id}/drive_thru"),
        ("feedback-create", "Post feedback", "POST", "/feedback"),
        ("feedback-reply", "Reply to feedback", "POST", "/feedback/{feedback_id}/reply"),
        ("coupon-create", "Create coupon", "POST", "/coupons"),
        ("coupon-update", "Update coupon", "PUT", "/coupons/{coupon_id}"),
        ("coupon-delete", "Delete coupon", "DELETE", "/coupons/{coupon_id}"),
        ("member-notes-create", "Create private member note", "POST", "/members/{username}/my_notes"),
        ("member-notes-update", "Update private member note", "PUT", "/members/{username}/my_notes"),
        ("member-notes-delete", "Delete private member note", "DELETE", "/members/{username}/my_notes"),
    ]:
        p = add_parser(subparsers, name, help_text)
        add_write_safety(p)
        add_identifier_args(p, path_template)
        p.add_argument("--json", dest="json_payload", help="JSON request body for POST/PUT endpoints")
        p.set_defaults(handler=cmd_mutating, method=method, path_template=path_template)

    return parser


def add_identifier_args(parser: argparse.ArgumentParser, path_template: str) -> None:
    if "{inventory_id}" in path_template:
        parser.add_argument("--inventory-id", required=True)
    if "{order_id}" in path_template:
        parser.add_argument("--order-id", required=True)
    if "{feedback_id}" in path_template:
        parser.add_argument("--feedback-id", required=True)
    if "{coupon_id}" in path_template:
        parser.add_argument("--coupon-id", required=True)
    if "{username}" in path_template:
        parser.add_argument("--username", required=True)


def fill_path(template: str, args: argparse.Namespace) -> str:
    values = {
        "inventory_id": getattr(args, "inventory_id", None),
        "order_id": getattr(args, "order_id", None),
        "feedback_id": getattr(args, "feedback_id", None),
        "coupon_id": getattr(args, "coupon_id", None),
        "username": getattr(args, "username", None),
        "type": getattr(args, "type", None),
        "no": getattr(args, "no", None),
        "element_id": getattr(args, "element_id", None),
        "color_id": getattr(args, "color_id", None),
        "category_id": getattr(args, "category_id", None),
        "method_id": getattr(args, "method_id", None),
    }
    path = template
    for key, value in values.items():
        if value is not None:
            path = path.replace("{" + key + "}", urllib.parse.quote(str(value), safe=""))
    return path


def get(args: argparse.Namespace, path: str, params: dict[str, Any] | None = None) -> Any:
    return client_from_args(args).request("GET", path, params=params)


def cmd_colors(args: argparse.Namespace) -> Any: return get(args, "/colors")
def cmd_color(args: argparse.Namespace) -> Any: return get(args, fill_path("/colors/{color_id}", args))
def cmd_categories(args: argparse.Namespace) -> Any: return get(args, "/categories")
def cmd_category(args: argparse.Namespace) -> Any: return get(args, fill_path("/categories/{category_id}", args))
def cmd_item(args: argparse.Namespace) -> Any: return get(args, fill_path("/items/{type}/{no}", args))
def cmd_item_colors(args: argparse.Namespace) -> Any: return get(args, fill_path("/items/{type}/{no}/colors", args))
def cmd_item_images(args: argparse.Namespace) -> Any: return get(args, fill_path("/items/{type}/{no}/images/{color_id}", args))
def cmd_item_supersets(args: argparse.Namespace) -> Any: return get(args, fill_path("/items/{type}/{no}/supersets", args), {"color_id": args.color_id})
def cmd_item_subsets(args: argparse.Namespace) -> Any: return get(args, fill_path("/items/{type}/{no}/subsets", args), {"color_id": args.color_id, "box": args.box, "break_minifigs": args.break_minifigs, "break_subsets": args.break_subsets})
def cmd_item_mapping(args: argparse.Namespace) -> Any: return get(args, fill_path("/item_mapping/{type}/{no}", args), {"color_id": args.color_id})
def cmd_element_mapping(args: argparse.Namespace) -> Any: return get(args, fill_path("/item_mapping/{element_id}", args))
def cmd_orders(args: argparse.Namespace) -> Any: return get(args, "/orders", {"direction": args.direction, "status": args.status, "filed": args.filed})
def cmd_order(args: argparse.Namespace) -> Any: return get(args, fill_path("/orders/{order_id}", args))
def cmd_order_items(args: argparse.Namespace) -> Any: return get(args, fill_path("/orders/{order_id}/items", args))
def cmd_order_messages(args: argparse.Namespace) -> Any: return get(args, fill_path("/orders/{order_id}/messages", args))
def cmd_order_feedback(args: argparse.Namespace) -> Any: return get(args, fill_path("/orders/{order_id}/feedback", args))
def cmd_inventory_list(args: argparse.Namespace) -> Any: return get(args, "/inventories", {"item_type": args.item_type, "status": args.status, "category_id": args.category_id, "color_id": args.color_id})
def cmd_inventory(args: argparse.Namespace) -> Any: return get(args, fill_path("/inventories/{inventory_id}", args))
def cmd_feedback(args: argparse.Namespace) -> Any: return get(args, "/feedback", {"direction": args.direction})
def cmd_feedback_view(args: argparse.Namespace) -> Any: return get(args, fill_path("/feedback/{feedback_id}", args))
def cmd_notifications(args: argparse.Namespace) -> Any: return get(args, "/notifications")
def cmd_coupons(args: argparse.Namespace) -> Any: return get(args, "/coupons")
def cmd_coupon(args: argparse.Namespace) -> Any: return get(args, fill_path("/coupons/{coupon_id}", args))
def cmd_shipping_methods(args: argparse.Namespace) -> Any: return get(args, "/settings/shipping_methods")
def cmd_shipping_method(args: argparse.Namespace) -> Any: return get(args, fill_path("/settings/shipping_methods/{method_id}", args))
def cmd_member_ratings(args: argparse.Namespace) -> Any: return get(args, fill_path("/members/{username}/ratings", args))
def cmd_member_notes(args: argparse.Namespace) -> Any: return get(args, fill_path("/members/{username}/my_notes", args))


def cmd_item_price(args: argparse.Namespace) -> Any:
    params = {
        "color_id": args.color_id,
        "guide_type": args.guide_type,
        "new_or_used": args.new_or_used,
        "country_code": args.country_code,
        "region": args.region,
        "currency_code": args.currency_code,
        "vat": args.vat,
    }
    return get(args, fill_path("/items/{type}/{no}/price", args), params)


def cmd_mutating(args: argparse.Namespace) -> Any:
    path = fill_path(args.path_template, args)
    body = parse_json_payload(args.json_payload)
    if not ensure_write_allowed(args, args.method, path, body=body):
        return None
    return client_from_args(args).request(args.method, path, body=body)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
        if result is not None:
            print_json(result)
        return 0
    except BrickLinkCliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
