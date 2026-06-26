#!/usr/bin/env python3
"""Small Brickset API CLI used by the Brickset AFOL skill.

The CLI intentionally uses only Python's standard library and the checked-in
Brickset API shape. Credentials come from environment variables, not flags, so
commands can be copied into transcripts without leaking secrets.
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

DEFAULT_BASE_URL = "https://brickset.com/api/v3.asmx"
READ_TIMEOUT_SECONDS = 30
WRITE_COMMANDS = {"collection-set"}


class BricksetCliError(RuntimeError):
    """Expected CLI/API failure with a clean user-facing message."""


class BricksetClient:
    def __init__(self, api_key: str, user_hash: str = "", base_url: str = DEFAULT_BASE_URL, timeout: int = READ_TIMEOUT_SECONDS):
        self.api_key = api_key
        self.user_hash = user_hash
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def post_form(self, path: str, fields: dict[str, Any], *, user_hash: str | None = None) -> Any:
        body_fields = {
            "apiKey": self.api_key,
            "userHash": self.user_hash if user_hash is None else user_hash,
            **clean_params(fields),
        }
        body = urllib.parse.urlencode(body_fields, doseq=True).encode()
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        return self._request("POST", url, body, headers)

    def login(self, username: str, password: str) -> Any:
        body = urllib.parse.urlencode({"apiKey": self.api_key, "username": username, "password": password}).encode()
        url = f"{self.base_url}/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        return self._request("POST", url, body, headers)

    def _request(self, method: str, url: str, body: bytes | None = None, headers: dict[str, str] | None = None) -> Any:
        request = urllib.request.Request(url, data=body, headers=headers or {"Accept": "application/json"}, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:  # noqa: S310 - URL is API base/user input by design.
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise BricksetCliError(f"Brickset API HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise BricksetCliError(f"Brickset API request failed: {exc.reason}") from exc

        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw


def clean_params(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def require_api_key() -> str:
    api_key = os.getenv("BRICKSET_API_KEY")
    if not api_key:
        raise BricksetCliError("BRICKSET_API_KEY is required")
    return api_key


def require_user_hash() -> str:
    user_hash = os.getenv("BRICKSET_USER_HASH")
    if not user_hash:
        raise BricksetCliError("BRICKSET_USER_HASH is required for this private Brickset operation")
    return user_hash


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))


def parse_params_json(params_json: str) -> dict[str, Any]:
    try:
        parsed = json.loads(params_json)
    except json.JSONDecodeError as exc:
        raise BricksetCliError(f"params JSON is invalid: {exc}") from exc
    if not isinstance(parsed, dict):
        raise BricksetCliError("params JSON must be an object")
    return parsed


def params_to_json(fields: dict[str, Any]) -> str:
    return json.dumps(clean_params(fields), separators=(",", ":"), ensure_ascii=False)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=os.getenv("BRICKSET_BASE_URL", DEFAULT_BASE_URL), help="Brickset API base URL")
    parser.add_argument("--timeout", type=int, default=READ_TIMEOUT_SECONDS, help="HTTP timeout in seconds")


def add_write_safety(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--yes", action="store_true", help="Actually execute this mutating request")
    parser.add_argument("--dry-run", action="store_true", help="Print request shape without calling Brickset")


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser], name: str, help_text: str) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=help_text)
    add_common(parser)
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brickset", description="Brickset API CLI for AFOL agent skills")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = add_parser(subparsers, "sets", "Search Brickset sets/details through getSets")
    p.add_argument("--set-number", help="Set number, e.g. 10270-1")
    p.add_argument("--query", help="Text query when supported by Brickset params")
    p.add_argument("--theme")
    p.add_argument("--year")
    p.add_argument("--owned", choices=["0", "1"], help="Private collection filter; requires BRICKSET_USER_HASH")
    p.add_argument("--wanted", choices=["0", "1"], help="Private wishlist filter; requires BRICKSET_USER_HASH")
    p.add_argument("--params-json", help="Raw getSets params JSON object")
    p.set_defaults(handler=cmd_sets)

    p = add_parser(subparsers, "details", "Alias for sets by set number")
    p.add_argument("--set-number", required=True)
    p.set_defaults(handler=cmd_details)

    p = add_parser(subparsers, "images", "Get additional images for a Brickset internal setID")
    p.add_argument("--set-id", required=True, type=int)
    p.set_defaults(handler=cmd_images)

    p = add_parser(subparsers, "instructions", "Get building instruction PDF links by set number")
    p.add_argument("--set-number", required=True)
    p.set_defaults(handler=cmd_instructions)

    p = add_parser(subparsers, "reviews", "Get community reviews by Brickset internal setID")
    p.add_argument("--set-id", required=True, type=int)
    p.set_defaults(handler=cmd_reviews)

    p = add_parser(subparsers, "login", "Obtain a Brickset user hash from BRICKSET_USERNAME/BRICKSET_PASSWORD")
    p.set_defaults(handler=cmd_login)

    p = add_parser(subparsers, "collection", "List owned collection through getSets owned=1")
    p.set_defaults(handler=cmd_collection)

    p = add_parser(subparsers, "wishlist", "List wanted sets through getSets wanted=1")
    p.set_defaults(handler=cmd_wishlist)

    p = add_parser(subparsers, "notes", "List Brickset user notes")
    p.set_defaults(handler=cmd_notes)

    p = add_parser(subparsers, "collection-set", "Mutate collection/wishlist state through setCollection")
    add_write_safety(p)
    p.add_argument("--set-id", required=True, type=int)
    p.add_argument("--own", choices=["0", "1"])
    p.add_argument("--want", choices=["0", "1"])
    p.add_argument("--qty-owned", type=int)
    p.add_argument("--notes")
    p.add_argument("--rating", type=int, choices=range(1, 6))
    p.add_argument("--params-json", help="Raw setCollection params JSON object")
    p.set_defaults(handler=cmd_collection_set)

    return parser


def client_from_args(args: argparse.Namespace, *, private: bool = False) -> BricksetClient:
    user_hash = require_user_hash() if private else os.getenv("BRICKSET_USER_HASH", "")
    return BricksetClient(require_api_key(), user_hash, args.base_url, args.timeout)


def needs_private_hash(params: dict[str, Any]) -> bool:
    return params.get("owned") == 1 or params.get("owned") == "1" or params.get("wanted") == 1 or params.get("wanted") == "1"


def getsets_params(args: argparse.Namespace) -> dict[str, Any]:
    if getattr(args, "params_json", None):
        params = parse_params_json(args.params_json)
    else:
        params = {
            "setNumber": getattr(args, "set_number", None),
            "query": getattr(args, "query", None),
            "theme": getattr(args, "theme", None),
            "year": int(args.year) if getattr(args, "year", None) else None,
            "owned": int(args.owned) if getattr(args, "owned", None) else None,
            "wanted": int(args.wanted) if getattr(args, "wanted", None) else None,
        }
    params = clean_params(params)
    if not params:
        raise BricksetCliError("provide at least one getSets filter")
    return params


def cmd_sets(args: argparse.Namespace) -> Any:
    params = getsets_params(args)
    return client_from_args(args, private=needs_private_hash(params)).post_form("/getSets", {"params": params_to_json(params)})


def cmd_details(args: argparse.Namespace) -> Any:
    args.params_json = None
    args.query = None
    args.theme = None
    args.year = None
    args.owned = None
    args.wanted = None
    return cmd_sets(args)


def cmd_images(args: argparse.Namespace) -> Any:
    return client_from_args(args).post_form("/getAdditionalImages", {"setID": args.set_id})


def cmd_instructions(args: argparse.Namespace) -> Any:
    return client_from_args(args).post_form("/getInstructions2", {"setNumber": args.set_number})


def cmd_reviews(args: argparse.Namespace) -> Any:
    return client_from_args(args).post_form("/getReviews", {"setID": args.set_id})


def cmd_login(args: argparse.Namespace) -> Any:
    username = os.getenv("BRICKSET_USERNAME")
    password = os.getenv("BRICKSET_PASSWORD")
    if not username or not password:
        raise BricksetCliError("BRICKSET_USERNAME and BRICKSET_PASSWORD are required for login")
    return client_from_args(args).login(username, password)


def cmd_collection(args: argparse.Namespace) -> Any:
    return client_from_args(args, private=True).post_form("/getSets", {"params": params_to_json({"owned": 1})})


def cmd_wishlist(args: argparse.Namespace) -> Any:
    return client_from_args(args, private=True).post_form("/getSets", {"params": params_to_json({"wanted": 1})})


def cmd_notes(args: argparse.Namespace) -> Any:
    return client_from_args(args, private=True).post_form("/getUserNotes", {})


def dry_run(command: str, path: str, fields: dict[str, Any]) -> None:
    print_json(
        {
            "dry_run": True,
            "command": command,
            "method": "POST",
            "path": path,
            "form_fields": {"apiKey": "[from BRICKSET_API_KEY]", "userHash": "[from BRICKSET_USER_HASH]", **clean_params(fields)},
        }
    )


def require_any_change(args: argparse.Namespace, field_names: Iterable[str]) -> None:
    if getattr(args, "params_json", None):
        return
    if not any(getattr(args, field) is not None for field in field_names):
        raise BricksetCliError("provide at least one collection/wishlist field to change")


def ensure_write_allowed(args: argparse.Namespace, path: str, fields: dict[str, Any]) -> bool:
    if args.dry_run:
        dry_run(args.command, path, fields)
        return False
    if not args.yes:
        raise BricksetCliError(f"{args.command} mutates Brickset data; rerun with --dry-run to inspect or --yes after explicit user confirmation")
    return True


def cmd_collection_set(args: argparse.Namespace) -> Any:
    require_any_change(args, ["own", "want", "qty_owned", "notes", "rating"])
    if args.params_json:
        params = parse_params_json(args.params_json)
    else:
        params = clean_params(
            {
                "own": int(args.own) if args.own is not None else None,
                "want": int(args.want) if args.want is not None else None,
                "qtyOwned": args.qty_owned,
                "notes": args.notes,
                "rating": args.rating,
            }
        )
    fields = {"setID": args.set_id, "params": params_to_json(params)}
    path = "/setCollection"
    if not ensure_write_allowed(args, path, fields):
        return None
    return client_from_args(args, private=True).post_form(path, fields)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
        if result is not None:
            print_json(result)
        return 0
    except BricksetCliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
