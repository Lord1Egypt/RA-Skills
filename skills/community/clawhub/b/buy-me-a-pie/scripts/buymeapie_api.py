#!/usr/bin/env python3
"""Thin Buy Me a Pie API client for OpenClaw skills."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_BASE_URL = "https://api.buymeapie.com"


@dataclass
class ApiError(Exception):
    status: int
    message: str
    payload: Any | None = None

    def __str__(self) -> str:
        return f"{self.status}: {self.message}"


def parse_json(raw: bytes) -> Any:
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"raw": raw.decode("utf-8", errors="replace")}


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")


class BuyMeAPieClient:
    def __init__(self, login: str, pin: str, base_url: str = DEFAULT_BASE_URL, timeout: int = 15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        auth = base64.b64encode(f"{login}:{pin}".encode("utf-8")).decode("ascii")
        self.headers = {
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            "Accept-Language": "en",
        }

    def request(
        self,
        method: str,
        path: str,
        payload: Any | None = None,
        params: dict[str, Any] | None = None,
        retries: int = 2,
    ) -> Any:
        url = f"{self.base_url}{path}"
        if params:
            query = urllib.parse.urlencode(params)
            url = f"{url}?{query}"

        body = None
        headers = dict(self.headers)
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(url, data=body, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return parse_json(response.read())
        except urllib.error.HTTPError as exc:
            parsed = parse_json(exc.read())
            if exc.code == 423 and retries > 0:
                time.sleep(0.5 * (3 - retries))
                return self.request(method, path, payload=payload, params=params, retries=retries - 1)
            message = parsed.get("error") if isinstance(parsed, dict) else None
            if not message and isinstance(parsed, dict) and parsed.get("errors"):
                message = "API returned validation errors"
            raise ApiError(exc.code, message or "HTTP request failed", parsed) from exc
        except urllib.error.URLError as exc:
            raise ApiError(0, f"Network error: {exc.reason}") from exc

    def whoami(self) -> Any:
        return self.request("GET", "/bauth")

    def restrictions(self) -> Any:
        return self.request("GET", "/restrictions")

    def lists(self) -> list[dict[str, Any]]:
        result = self.request("GET", "/lists")
        if not isinstance(result, list):
            raise ApiError(0, "Unexpected /lists response shape", result)
        return result

    def list_by_id(self, list_id: str) -> dict[str, Any]:
        for current in self.lists():
            if str(current.get("id")) == str(list_id):
                return current
        raise ApiError(404, f"List not found: {list_id}")

    def items(self, list_id: str) -> Any:
        return self.request("GET", f"/lists/{list_id}/items")

    def unique_items(self) -> Any:
        return self.request("GET", "/unique_items")

    def create_list(self, name: str) -> Any:
        return self.request(
            "POST",
            "/lists",
            payload={"name": name, "items_purchased": 0, "items_not_purchased": 0},
        )

    def update_list(self, list_id: str, *, name: str | None = None, emails: list[str] | None = None) -> Any:
        current = self.list_by_id(list_id)
        payload = {
            "name": name if name is not None else current.get("name"),
            "emails": emails if emails is not None else current.get("emails", []),
        }
        return self.request("PUT", f"/lists/{list_id}", payload=payload)

    def delete_list(self, list_id: str) -> Any:
        return self.request("DELETE", f"/lists/{list_id}")

    def add_item(self, list_id: str, title: str, amount: str, purchased: bool = False) -> Any:
        payload = {"title": title, "amount": amount, "is_purchased": purchased}
        return self.request("POST", f"/lists/{list_id}/items", payload=payload)

    def update_item(
        self,
        list_id: str,
        item_id: str,
        *,
        title: str | None = None,
        amount: str | None = None,
        purchased: bool | None = None,
    ) -> Any:
        payload: dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if amount is not None:
            payload["amount"] = amount
        if purchased is not None:
            payload["is_purchased"] = purchased
        if not payload:
            raise ApiError(0, "Refusing empty item update payload")
        return self.request("PUT", f"/lists/{list_id}/items/{item_id}", payload=payload)

    def delete_item(self, list_id: str, item_id: str) -> Any:
        return self.request("DELETE", f"/lists/{list_id}/items/{item_id}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Buy Me a Pie API helper")
    parser.add_argument("--login", default=os.getenv("BUYMEAPIE_LOGIN"), help="Buy Me a Pie login")
    parser.add_argument("--pin", default=os.getenv("BUYMEAPIE_PIN"), help="Buy Me a Pie PIN")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout in seconds")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("whoami", help="Validate credentials and return account data")
    subparsers.add_parser("restrictions", help="Return account restriction limits")
    subparsers.add_parser("lists", help="Return all lists")

    items_parser = subparsers.add_parser("items", help="Return all items for a list")
    items_parser.add_argument("--list-id", required=True)

    subparsers.add_parser("unique-items", help="Return autocomplete dictionary")

    create_list = subparsers.add_parser("create-list", help="Create a new list")
    create_list.add_argument("--name", required=True)

    rename_list = subparsers.add_parser("rename-list", help="Rename a list")
    rename_list.add_argument("--list-id", required=True)
    rename_list.add_argument("--name", required=True)

    share_list = subparsers.add_parser("share-list", help="Merge or replace list recipients")
    share_list.add_argument("--list-id", required=True)
    share_list.add_argument("--email", action="append", required=True, dest="emails")
    share_list.add_argument("--replace", action="store_true", help="Replace existing recipients instead of merging")

    delete_list = subparsers.add_parser("delete-list", help="Delete a list")
    delete_list.add_argument("--list-id", required=True)

    add_item = subparsers.add_parser("add-item", help="Add an item to a list")
    add_item.add_argument("--list-id", required=True)
    add_item.add_argument("--title", required=True)
    add_item.add_argument("--amount", default="")
    add_item.add_argument("--purchased", type=parse_bool, default=False)

    update_item = subparsers.add_parser("update-item", help="Update an item")
    update_item.add_argument("--list-id", required=True)
    update_item.add_argument("--item-id", required=True)
    update_item.add_argument("--title")
    update_item.add_argument("--amount")
    update_item.add_argument("--purchased", type=parse_bool)

    set_item_state = subparsers.add_parser("set-item-state", help="Set purchased state for an item")
    set_item_state.add_argument("--list-id", required=True)
    set_item_state.add_argument("--item-id", required=True)
    set_item_state.add_argument("--purchased", required=True, type=parse_bool)

    delete_item = subparsers.add_parser("delete-item", help="Delete an item")
    delete_item.add_argument("--list-id", required=True)
    delete_item.add_argument("--item-id", required=True)

    return parser


def require_credentials(args: argparse.Namespace) -> tuple[str, str]:
    if not args.login or not args.pin:
        raise ApiError(0, "Missing credentials. Set BUYMEAPIE_LOGIN and BUYMEAPIE_PIN or pass --login/--pin.")
    return args.login, args.pin


def print_json(payload: Any) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True))
    sys.stdout.write("\n")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        login, pin = require_credentials(args)
        client = BuyMeAPieClient(login=login, pin=pin, base_url=args.base_url, timeout=args.timeout)

        if args.command == "whoami":
            result = client.whoami()
        elif args.command == "restrictions":
            result = client.restrictions()
        elif args.command == "lists":
            result = client.lists()
        elif args.command == "items":
            result = client.items(args.list_id)
        elif args.command == "unique-items":
            result = client.unique_items()
        elif args.command == "create-list":
            result = client.create_list(args.name)
        elif args.command == "rename-list":
            result = client.update_list(args.list_id, name=args.name)
        elif args.command == "share-list":
            current = client.list_by_id(args.list_id)
            current_emails = list(current.get("emails", []))
            if args.replace:
                emails = args.emails
            else:
                emails = current_emails[:]
                for email in args.emails:
                    if email not in emails:
                        emails.append(email)
            result = client.update_list(args.list_id, emails=emails)
        elif args.command == "delete-list":
            result = client.delete_list(args.list_id)
        elif args.command == "add-item":
            result = client.add_item(args.list_id, args.title, args.amount, purchased=args.purchased)
        elif args.command == "update-item":
            result = client.update_item(
                args.list_id,
                args.item_id,
                title=args.title,
                amount=args.amount,
                purchased=args.purchased,
            )
        elif args.command == "set-item-state":
            result = client.update_item(args.list_id, args.item_id, purchased=args.purchased)
        elif args.command == "delete-item":
            result = client.delete_item(args.list_id, args.item_id)
        else:
            parser.error(f"Unsupported command: {args.command}")
            return 2

        print_json(result)
        return 0
    except ApiError as exc:
        error_payload = {
            "error": exc.message,
            "status": exc.status,
        }
        if exc.payload is not None:
            error_payload["payload"] = exc.payload
        sys.stderr.write(json.dumps(error_payload, indent=2, sort_keys=True))
        sys.stderr.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
