#!/usr/bin/env python3
"""Small Rebrickable API CLI used by the Rebrickable AFOL skill.

The CLI uses only Python's standard library and checked-in Rebrickable API
references. Secrets come from environment variables, never flags, so commands
can be copied into transcripts without exposing API keys.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable

DEFAULT_BASE_URL = "https://rebrickable.com/api/v3"
READ_TIMEOUT_SECONDS = 30
WRITE_COMMANDS = {
    "create-set-list",
    "update-set-list",
    "delete-set-list",
    "add-sets-to-list",
    "update-set-in-list",
    "remove-set-from-list",
    "create-part-list",
    "delete-part-list",
    "add-part-to-list",
    "update-part-in-list",
    "remove-part-from-list",
    "add-lost-part",
    "remove-lost-part",
}


class RebrickableCliError(RuntimeError):
    """Expected CLI/API failure with a clean user-facing message."""


class RebrickableClient:
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL, timeout: int = READ_TIMEOUT_SECONDS):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", self._url(path, params), headers=self._headers())

    def post_form(self, path: str, fields: dict[str, Any]) -> Any:
        return self._request("POST", self._url(path), body=form_body(fields), headers=self._headers("application/x-www-form-urlencoded"))

    def put_form(self, path: str, fields: dict[str, Any]) -> Any:
        return self._request("PUT", self._url(path), body=form_body(fields), headers=self._headers("application/x-www-form-urlencoded"))

    def patch_form(self, path: str, fields: dict[str, Any]) -> Any:
        return self._request("PATCH", self._url(path), body=form_body(fields), headers=self._headers("application/x-www-form-urlencoded"))

    def post_json(self, path: str, payload: Any) -> Any:
        return self._request("POST", self._url(path), body=json.dumps(payload).encode(), headers=self._headers("application/json"))

    def delete(self, path: str) -> Any:
        return self._request("DELETE", self._url(path), headers=self._headers())

    def _headers(self, content_type: str | None = None) -> dict[str, str]:
        headers = {"Accept": "application/json", "Authorization": f"key {self.api_key}"}
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _url(self, path: str, params: dict[str, Any] | None = None) -> str:
        query = urllib.parse.urlencode(clean_params(params or {}), doseq=True)
        suffix = f"?{query}" if query else ""
        return f"{self.base_url}{path}{suffix}"

    def _request(self, method: str, url: str, body: bytes | None = None, headers: dict[str, str] | None = None) -> Any:
        request = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:  # noqa: S310 - API base is user-configurable by design.
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RebrickableCliError(f"Rebrickable API HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RebrickableCliError(f"Rebrickable API request failed: {exc.reason}") from exc

        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw


def clean_params(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def form_body(fields: dict[str, Any]) -> bytes:
    return urllib.parse.urlencode(clean_params(fields), doseq=True).encode()


def require_api_key() -> str:
    api_key = os.getenv("REBRICKABLE_API_KEY")
    if not api_key:
        raise RebrickableCliError("REBRICKABLE_API_KEY is required")
    return api_key


def user_token(args: argparse.Namespace) -> str:
    token = getattr(args, "user_token", None) or os.getenv("REBRICKABLE_USER_TOKEN")
    if not token:
        raise RebrickableCliError("provide --user-token or set REBRICKABLE_USER_TOKEN for user collection endpoints")
    return token


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))


def redacted_headers(content_type: str | None = None) -> dict[str, str]:
    headers = {"Accept": "application/json", "Authorization": "key [from REBRICKABLE_API_KEY]"}
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def redact_private_path(path: str) -> str:
    return re.sub(r"/users/[^/]+/", "/users/[from REBRICKABLE_USER_TOKEN]/", path)


def dry_run(command: str, method: str, path: str, *, fields: dict[str, Any] | None = None, json_payload: Any = None) -> None:
    content_type = "application/json" if json_payload is not None else "application/x-www-form-urlencoded" if fields is not None else None
    payload: dict[str, Any] = {
        "dry_run": True,
        "command": command,
        "method": method,
        "path": redact_private_path(path),
        "headers": redacted_headers(content_type),
    }
    if fields is not None:
        payload["form_fields"] = clean_params(fields)
    if json_payload is not None:
        payload["json"] = json_payload
    print_json(payload)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=os.getenv("REBRICKABLE_BASE_URL", DEFAULT_BASE_URL), help="Rebrickable API base URL")
    parser.add_argument("--timeout", type=int, default=READ_TIMEOUT_SECONDS, help="HTTP timeout in seconds")


def add_user_token(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--user-token", help="Rebrickable user token; defaults to REBRICKABLE_USER_TOKEN")


def add_write_safety(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--yes", action="store_true", help="Actually execute this mutating request")
    parser.add_argument("--dry-run", action="store_true", help="Print request shape without calling Rebrickable")


def add_optional(parser: argparse.ArgumentParser, *names: str) -> None:
    for name in names:
        parser.add_argument(f"--{name.replace('_', '-')}", dest=name)


def add_pagination(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, dest="page_size")
    parser.add_argument("--ordering")


def add_catalog_filters(parser: argparse.ArgumentParser, *names: str) -> None:
    for name in names:
        parser.add_argument(f"--{name.replace('_', '-')}", dest=name)


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser], name: str, help_text: str) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=help_text)
    add_common(parser)
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rebrickable", description="Rebrickable API CLI for AFOL agent skills")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = add_parser(subparsers, "colors", "List LEGO colors")
    add_pagination(p)
    p.set_defaults(handler=lambda args: client_from_args(args).get("/lego/colors/", page_params(args)))

    p = add_parser(subparsers, "color", "Show one LEGO color")
    p.add_argument("--id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/colors/{quote(args.id)}/"))

    p = add_parser(subparsers, "element", "Show one LEGO element")
    p.add_argument("--element-id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/elements/{quote(args.element_id)}/"))

    p = add_parser(subparsers, "minifigs", "List minifigs")
    add_pagination(p)
    add_catalog_filters(p, "min_parts", "max_parts", "in_set_num", "in_theme_id", "search")
    p.set_defaults(handler=lambda args: client_from_args(args).get("/lego/minifigs/", page_params(args, "min_parts", "max_parts", "in_set_num", "in_theme_id", "search")))

    p = add_parser(subparsers, "minifig", "Show one minifig")
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/minifigs/{quote(args.set_num)}/"))

    p = add_parser(subparsers, "minifig-parts", "List parts in a minifig")
    add_pagination(p)
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/minifigs/{quote(args.set_num)}/parts/", page_params(args)))

    p = add_parser(subparsers, "minifig-sets", "List sets containing a minifig")
    add_pagination(p)
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/minifigs/{quote(args.set_num)}/sets/", page_params(args)))

    p = add_parser(subparsers, "part-categories", "List part categories")
    add_pagination(p)
    p.set_defaults(handler=lambda args: client_from_args(args).get("/lego/part_categories/", page_params(args)))

    p = add_parser(subparsers, "part-category", "Show one part category")
    p.add_argument("--id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/part_categories/{quote(args.id)}/"))

    p = add_parser(subparsers, "parts", "List LEGO parts")
    add_pagination(p)
    add_catalog_filters(p, "part_num", "part_nums", "part_cat_id", "color_id", "bricklink_id", "brickowl_id", "lego_id", "ldraw_id", "search")
    p.set_defaults(handler=lambda args: client_from_args(args).get("/lego/parts/", page_params(args, "part_num", "part_nums", "part_cat_id", "color_id", "bricklink_id", "brickowl_id", "lego_id", "ldraw_id", "search")))

    p = add_parser(subparsers, "part", "Show one LEGO part")
    p.add_argument("--part-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/parts/{quote(args.part_num)}/"))

    p = add_parser(subparsers, "part-colors", "List colors for a part")
    add_pagination(p)
    p.add_argument("--part-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/parts/{quote(args.part_num)}/colors/", page_params(args)))

    p = add_parser(subparsers, "part-color", "Show one part/color combination")
    p.add_argument("--part-num", required=True)
    p.add_argument("--color-id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/parts/{quote(args.part_num)}/colors/{quote(args.color_id)}/"))

    p = add_parser(subparsers, "part-color-sets", "List sets using a part/color combination")
    add_pagination(p)
    p.add_argument("--part-num", required=True)
    p.add_argument("--color-id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/parts/{quote(args.part_num)}/colors/{quote(args.color_id)}/sets/", page_params(args)))

    p = add_parser(subparsers, "sets", "List LEGO sets")
    add_pagination(p)
    add_catalog_filters(p, "theme_id", "min_year", "max_year", "min_parts", "max_parts", "search")
    p.set_defaults(handler=lambda args: client_from_args(args).get("/lego/sets/", page_params(args, "theme_id", "min_year", "max_year", "min_parts", "max_parts", "search")))

    p = add_parser(subparsers, "set", "Show one LEGO set")
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/sets/{quote(args.set_num)}/"))

    p = add_parser(subparsers, "set-parts", "List inventory parts in a set")
    add_pagination(p)
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/sets/{quote(args.set_num)}/parts/", page_params(args)))

    p = add_parser(subparsers, "set-minifigs", "List minifigs in a set")
    add_pagination(p)
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/sets/{quote(args.set_num)}/minifigs/", page_params(args)))

    p = add_parser(subparsers, "set-alternates", "List alternate builds for a set")
    add_pagination(p)
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/sets/{quote(args.set_num)}/alternates/", page_params(args)))

    p = add_parser(subparsers, "themes", "List LEGO themes")
    add_pagination(p)
    p.set_defaults(handler=lambda args: client_from_args(args).get("/lego/themes/", page_params(args)))

    p = add_parser(subparsers, "theme", "Show one LEGO theme")
    p.add_argument("--id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/lego/themes/{quote(args.id)}/"))

    add_user_readers(subparsers)
    add_user_writers(subparsers)
    return parser


def add_user_readers(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    p = add_parser(subparsers, "profile", "Show Rebrickable user profile")
    add_user_token(p)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/users/{quote(user_token(args))}/profile/"))

    for name, path, help_text in [
        ("set-lists", "setlists", "List user set lists"),
        ("part-lists", "partlists", "List user part lists"),
        ("all-sets", "sets", "List all user sets"),
        ("all-parts", "allparts", "List all user parts including set inventory; resource-intensive"),
        ("all-minifigs", "minifigs", "List minifigs from user sets"),
        ("lost-parts", "lost_parts", "List user's lost parts"),
    ]:
        p = add_parser(subparsers, name, help_text)
        add_user_token(p)
        add_pagination(p)
        if name in {"all-sets"}:
            add_catalog_filters(p, "set_num", "theme_id", "min_year", "max_year", "min_parts", "max_parts", "search")
            fields = ("set_num", "theme_id", "min_year", "max_year", "min_parts", "max_parts", "search")
        elif name in {"all-parts"}:
            add_catalog_filters(p, "part_num", "part_cat_id", "color_id")
            fields = ("part_num", "part_cat_id", "color_id")
        elif name in {"all-minifigs"}:
            add_catalog_filters(p, "fig_set_num", "search")
            fields = ("fig_set_num", "search")
        else:
            fields = ()
        p.set_defaults(handler=lambda args, path=path, fields=fields: client_from_args(args).get(f"/users/{quote(user_token(args))}/{path}/", page_params(args, *fields)))

    p = add_parser(subparsers, "set-list", "Show one user set list")
    add_user_token(p)
    p.add_argument("--list-id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/users/{quote(user_token(args))}/setlists/{quote(args.list_id)}/"))

    p = add_parser(subparsers, "set-list-sets", "List sets in a user set list")
    add_user_token(p)
    add_pagination(p)
    p.add_argument("--list-id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/users/{quote(user_token(args))}/setlists/{quote(args.list_id)}/sets/", page_params(args)))

    p = add_parser(subparsers, "part-list-parts", "List parts in a user part list")
    add_user_token(p)
    add_pagination(p)
    p.add_argument("--list-id", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/users/{quote(user_token(args))}/partlists/{quote(args.list_id)}/parts/", page_params(args)))

    p = add_parser(subparsers, "build", "Analyze whether the user can build a set")
    add_user_token(p)
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=lambda args: client_from_args(args).get(f"/users/{quote(user_token(args))}/build/{quote(args.set_num)}/"))


def add_user_writers(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    p = write_parser(subparsers, "create-set-list", "Create a user set list")
    p.add_argument("--name", required=True)
    p.add_argument("--is-buildable", choices=["true", "false"])
    p.set_defaults(handler=cmd_create_set_list)

    p = write_parser(subparsers, "update-set-list", "Update a user set list")
    p.add_argument("--list-id", required=True)
    p.add_argument("--name")
    p.add_argument("--is-buildable", choices=["true", "false"])
    p.set_defaults(handler=cmd_update_set_list)

    p = write_parser(subparsers, "delete-set-list", "Delete a user set list")
    p.add_argument("--list-id", required=True)
    p.set_defaults(handler=cmd_delete_set_list)

    p = write_parser(subparsers, "add-sets-to-list", "Add sets to a specific set list as a JSON array")
    p.add_argument("--list-id", required=True)
    p.add_argument("--sets-json", required=True, help='JSON array, e.g. [{"set_num":"8043-1","quantity":1}]')
    p.set_defaults(handler=cmd_add_sets_to_list)

    p = write_parser(subparsers, "update-set-in-list", "Update set quantity/include_spares in a set list")
    p.add_argument("--list-id", required=True)
    p.add_argument("--set-num", required=True)
    p.add_argument("--quantity", type=int)
    p.add_argument("--include-spares", choices=["true", "false"])
    p.set_defaults(handler=cmd_update_set_in_list)

    p = write_parser(subparsers, "remove-set-from-list", "Remove a set from a set list")
    p.add_argument("--list-id", required=True)
    p.add_argument("--set-num", required=True)
    p.set_defaults(handler=cmd_remove_set_from_list)

    p = write_parser(subparsers, "create-part-list", "Create a user part list")
    p.add_argument("--name", required=True)
    p.add_argument("--is-buildable", choices=["true", "false"])
    p.set_defaults(handler=cmd_create_part_list)

    p = write_parser(subparsers, "delete-part-list", "Delete a user part list")
    p.add_argument("--list-id", required=True)
    p.set_defaults(handler=cmd_delete_part_list)

    p = write_parser(subparsers, "add-part-to-list", "Add a part to a part list")
    p.add_argument("--list-id", required=True)
    p.add_argument("--part-num", required=True)
    p.add_argument("--color-id", required=True, type=int)
    p.add_argument("--quantity", required=True, type=int)
    p.set_defaults(handler=cmd_add_part_to_list)

    p = write_parser(subparsers, "update-part-in-list", "Update part quantity in a part list")
    p.add_argument("--list-id", required=True)
    p.add_argument("--part-num", required=True)
    p.add_argument("--color-id", required=True)
    p.add_argument("--quantity", required=True, type=int)
    p.set_defaults(handler=cmd_update_part_in_list)

    p = write_parser(subparsers, "remove-part-from-list", "Remove a part from a part list")
    p.add_argument("--list-id", required=True)
    p.add_argument("--part-num", required=True)
    p.add_argument("--color-id", required=True)
    p.set_defaults(handler=cmd_remove_part_from_list)

    p = write_parser(subparsers, "add-lost-part", "Mark an inventory part as lost")
    p.add_argument("--inv-part-id", required=True, type=int)
    p.add_argument("--lost-quantity", type=int)
    p.set_defaults(handler=cmd_add_lost_part)

    p = write_parser(subparsers, "remove-lost-part", "Remove a lost-part record")
    p.add_argument("--lost-part-id", required=True)
    p.set_defaults(handler=cmd_remove_lost_part)


def write_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser], name: str, help_text: str) -> argparse.ArgumentParser:
    parser = add_parser(subparsers, name, help_text)
    add_user_token(parser)
    add_write_safety(parser)
    return parser


def client_from_args(args: argparse.Namespace) -> RebrickableClient:
    return RebrickableClient(require_api_key(), args.base_url, args.timeout)


def quote(value: str) -> str:
    return urllib.parse.quote(str(value), safe="")


def user_path(args: argparse.Namespace, suffix: str) -> str:
    token = "[from REBRICKABLE_USER_TOKEN]" if getattr(args, "dry_run", False) else quote(user_token(args))
    return f"/users/{token}/{suffix.lstrip('/')}"


def page_params(args: argparse.Namespace, *field_names: str) -> dict[str, Any]:
    params = {"page": args.page, "page_size": args.page_size, "ordering": args.ordering}
    params.update({field: getattr(args, field) for field in field_names})
    return params


def ensure_write_allowed(args: argparse.Namespace, method: str, path: str, *, fields: dict[str, Any] | None = None, json_payload: Any = None) -> bool:
    if args.dry_run:
        dry_run(args.command, method, path, fields=fields, json_payload=json_payload)
        return False
    if not args.yes:
        raise RebrickableCliError(f"{args.command} mutates Rebrickable data; rerun with --dry-run to inspect or --yes after explicit user confirmation")
    return True


def require_any(args: argparse.Namespace, field_names: Iterable[str]) -> None:
    if not any(getattr(args, field) is not None for field in field_names):
        raise RebrickableCliError("provide at least one field to update")


def parse_json_array(raw: str, option: str) -> list[Any]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RebrickableCliError(f"{option} is not valid JSON: {exc}") from exc
    if not isinstance(payload, list):
        raise RebrickableCliError(f"{option} must be a JSON array; Rebrickable requires an array even for one set")
    return payload


def cmd_create_set_list(args: argparse.Namespace) -> Any:
    path = user_path(args, "setlists/")
    fields = {"name": args.name, "is_buildable": args.is_buildable}
    if not ensure_write_allowed(args, "POST", path, fields=fields):
        return None
    return client_from_args(args).post_form(path, fields)


def cmd_update_set_list(args: argparse.Namespace) -> Any:
    require_any(args, ["name", "is_buildable"])
    path = user_path(args, f"setlists/{quote(args.list_id)}/")
    fields = {"name": args.name, "is_buildable": args.is_buildable}
    if not ensure_write_allowed(args, "PATCH", path, fields=fields):
        return None
    return client_from_args(args).patch_form(path, fields)


def cmd_delete_set_list(args: argparse.Namespace) -> Any:
    path = user_path(args, f"setlists/{quote(args.list_id)}/")
    if not ensure_write_allowed(args, "DELETE", path):
        return None
    return client_from_args(args).delete(path)


def cmd_add_sets_to_list(args: argparse.Namespace) -> Any:
    payload = parse_json_array(args.sets_json, "--sets-json")
    path = user_path(args, f"setlists/{quote(args.list_id)}/sets/")
    if not ensure_write_allowed(args, "POST", path, json_payload=payload):
        return None
    return client_from_args(args).post_json(path, payload)


def cmd_update_set_in_list(args: argparse.Namespace) -> Any:
    require_any(args, ["quantity", "include_spares"])
    path = user_path(args, f"setlists/{quote(args.list_id)}/sets/{quote(args.set_num)}/")
    fields = {"quantity": args.quantity, "include_spares": args.include_spares}
    if not ensure_write_allowed(args, "PATCH", path, fields=fields):
        return None
    return client_from_args(args).patch_form(path, fields)


def cmd_remove_set_from_list(args: argparse.Namespace) -> Any:
    path = user_path(args, f"setlists/{quote(args.list_id)}/sets/{quote(args.set_num)}/")
    if not ensure_write_allowed(args, "DELETE", path):
        return None
    return client_from_args(args).delete(path)


def cmd_create_part_list(args: argparse.Namespace) -> Any:
    path = user_path(args, "partlists/")
    fields = {"name": args.name, "is_buildable": args.is_buildable}
    if not ensure_write_allowed(args, "POST", path, fields=fields):
        return None
    return client_from_args(args).post_form(path, fields)


def cmd_delete_part_list(args: argparse.Namespace) -> Any:
    path = user_path(args, f"partlists/{quote(args.list_id)}/")
    if not ensure_write_allowed(args, "DELETE", path):
        return None
    return client_from_args(args).delete(path)


def cmd_add_part_to_list(args: argparse.Namespace) -> Any:
    path = user_path(args, f"partlists/{quote(args.list_id)}/parts/")
    fields = {"part_num": args.part_num, "color_id": args.color_id, "quantity": args.quantity}
    if not ensure_write_allowed(args, "POST", path, fields=fields):
        return None
    return client_from_args(args).post_form(path, fields)


def cmd_update_part_in_list(args: argparse.Namespace) -> Any:
    path = user_path(args, f"partlists/{quote(args.list_id)}/parts/{quote(args.part_num)}/{quote(args.color_id)}/")
    fields = {"quantity": args.quantity}
    if not ensure_write_allowed(args, "PUT", path, fields=fields):
        return None
    return client_from_args(args).put_form(path, fields)


def cmd_remove_part_from_list(args: argparse.Namespace) -> Any:
    path = user_path(args, f"partlists/{quote(args.list_id)}/parts/{quote(args.part_num)}/{quote(args.color_id)}/")
    if not ensure_write_allowed(args, "DELETE", path):
        return None
    return client_from_args(args).delete(path)


def cmd_add_lost_part(args: argparse.Namespace) -> Any:
    path = user_path(args, "lost_parts/")
    fields = {"inv_part_id": args.inv_part_id, "lost_quantity": args.lost_quantity}
    if not ensure_write_allowed(args, "POST", path, fields=fields):
        return None
    return client_from_args(args).post_form(path, fields)


def cmd_remove_lost_part(args: argparse.Namespace) -> Any:
    path = user_path(args, f"lost_parts/{quote(args.lost_part_id)}/")
    if not ensure_write_allowed(args, "DELETE", path):
        return None
    return client_from_args(args).delete(path)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
        if result is not None:
            print_json(result)
        return 0
    except RebrickableCliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
