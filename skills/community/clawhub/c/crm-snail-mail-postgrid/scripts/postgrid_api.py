#!/usr/bin/env python3
"""PostGrid API utility with broad endpoint coverage + raw caller.

This script is designed to support the full docs surface by combining:
- Cataloged endpoints for common operations across Print & Mail, Address Verification,
  and partner/admin resources.
- Raw caller support so any documented endpoint can be called immediately.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

DEFAULT_PRINT_MAIL_BASE_URL = "https://api.postgrid.com/print-mail/v1"
DEFAULT_CORE_BASE_URL = "https://api.postgrid.com/v1"


@dataclass(frozen=True)
class Endpoint:
    key: str
    method: str
    path: str
    group: str
    description: str
    base: str = "print-mail"


# Coverage target: API Reference groups visible on docs.postgrid.com / postgrid.readme.io.
ENDPOINTS: Dict[str, Endpoint] = {
    # Contacts
    "contacts.create": Endpoint("contacts.create", "POST", "/contacts", "contacts", "Create contact"),
    "contacts.get": Endpoint("contacts.get", "GET", "/contacts/{id}", "contacts", "Get contact"),
    "contacts.list": Endpoint("contacts.list", "GET", "/contacts", "contacts", "List contacts"),
    "contacts.delete": Endpoint("contacts.delete", "DELETE", "/contacts/{id}", "contacts", "Delete contact"),

    # Letters
    "letters.create": Endpoint("letters.create", "POST", "/letters", "letters", "Create letter"),
    "letters.get": Endpoint("letters.get", "GET", "/letters/{id}", "letters", "Get letter"),
    "letters.list": Endpoint("letters.list", "GET", "/letters", "letters", "List letters"),
    "letters.cancel": Endpoint("letters.cancel", "DELETE", "/letters/{id}", "letters", "Cancel letter"),
    "letters.cancel_with_note": Endpoint("letters.cancel_with_note", "POST", "/letters/{id}/cancel", "letters", "Cancel letter with note"),
    "letters.progress_test": Endpoint("letters.progress_test", "POST", "/letters/{id}/progress", "letters", "Progress test letter"),

    # Templates
    "templates.create": Endpoint("templates.create", "POST", "/templates", "templates", "Create template"),
    "templates.get": Endpoint("templates.get", "GET", "/templates/{id}", "templates", "Get template"),
    "templates.list": Endpoint("templates.list", "GET", "/templates", "templates", "List templates"),
    "templates.update": Endpoint("templates.update", "POST", "/templates/{id}", "templates", "Update template"),
    "templates.delete": Endpoint("templates.delete", "DELETE", "/templates/{id}", "templates", "Delete template"),

    # Postcards
    "postcards.create": Endpoint("postcards.create", "POST", "/postcards", "postcards", "Create postcard"),
    "postcards.get": Endpoint("postcards.get", "GET", "/postcards/{id}", "postcards", "Get postcard"),
    "postcards.list": Endpoint("postcards.list", "GET", "/postcards", "postcards", "List postcards"),
    "postcards.cancel": Endpoint("postcards.cancel", "DELETE", "/postcards/{id}", "postcards", "Cancel postcard"),
    "postcards.preview": Endpoint("postcards.preview", "GET", "/postcards/{id}/preview", "postcards", "Get postcard preview"),

    # Bank Accounts
    "bank_accounts.create": Endpoint("bank_accounts.create", "POST", "/bank_accounts", "bank_accounts", "Create bank account"),
    "bank_accounts.get": Endpoint("bank_accounts.get", "GET", "/bank_accounts/{id}", "bank_accounts", "Get bank account"),
    "bank_accounts.list": Endpoint("bank_accounts.list", "GET", "/bank_accounts", "bank_accounts", "List bank accounts"),
    "bank_accounts.delete": Endpoint("bank_accounts.delete", "DELETE", "/bank_accounts/{id}", "bank_accounts", "Delete bank account"),

    # Cheques / Checks
    "cheques.create": Endpoint("cheques.create", "POST", "/cheques", "cheques", "Create cheque"),
    "cheques.get": Endpoint("cheques.get", "GET", "/cheques/{id}", "cheques", "Get cheque"),
    "cheques.list": Endpoint("cheques.list", "GET", "/cheques", "cheques", "List cheques"),
    "cheques.cancel": Endpoint("cheques.cancel", "DELETE", "/cheques/{id}", "cheques", "Cancel cheque"),
    "cheques.cancel_with_note": Endpoint("cheques.cancel_with_note", "POST", "/cheques/{id}/cancel", "cheques", "Cancel cheque with note"),
    "cheques.progress_test": Endpoint("cheques.progress_test", "POST", "/cheques/{id}/progress", "cheques", "Progress test cheque"),
    "cheques.deposit_ready": Endpoint("cheques.deposit_ready", "GET", "/cheques/{id}/deposit_ready", "cheques", "Get deposit-ready e-check"),

    # Webhooks
    "webhooks.create": Endpoint("webhooks.create", "POST", "/webhooks", "webhooks", "Create webhook"),
    "webhooks.get": Endpoint("webhooks.get", "GET", "/webhooks/{id}", "webhooks", "Get webhook"),
    "webhooks.update": Endpoint("webhooks.update", "POST", "/webhooks/{id}", "webhooks", "Update webhook"),
    "webhooks.list": Endpoint("webhooks.list", "GET", "/webhooks", "webhooks", "List webhooks"),
    "webhooks.invocations": Endpoint("webhooks.invocations", "GET", "/webhooks/{id}/invocations", "webhooks", "List webhook invocations"),
    "webhooks.delete": Endpoint("webhooks.delete", "DELETE", "/webhooks/{id}", "webhooks", "Delete webhook"),

    # Return Envelopes
    "return_envelopes.create": Endpoint("return_envelopes.create", "POST", "/return_envelopes", "return_envelopes", "Create return envelope"),
    "return_envelopes.list": Endpoint("return_envelopes.list", "GET", "/return_envelopes", "return_envelopes", "List return envelopes"),
    "return_envelopes.get": Endpoint("return_envelopes.get", "GET", "/return_envelopes/{id}", "return_envelopes", "Get return envelope"),

    # Return Envelope Orders
    "return_envelope_orders.create": Endpoint("return_envelope_orders.create", "POST", "/return_envelope_orders", "return_envelope_orders", "Create return envelope order"),
    "return_envelope_orders.list": Endpoint("return_envelope_orders.list", "GET", "/return_envelope_orders", "return_envelope_orders", "List return envelope orders"),
    "return_envelope_orders.get": Endpoint("return_envelope_orders.get", "GET", "/return_envelope_orders/{id}", "return_envelope_orders", "Get return envelope order"),
    "return_envelope_orders.fill_test": Endpoint("return_envelope_orders.fill_test", "POST", "/return_envelope_orders/{id}/fill_test", "return_envelope_orders", "Fill test return envelope order"),
    "return_envelope_orders.cancel": Endpoint("return_envelope_orders.cancel", "DELETE", "/return_envelope_orders/{id}", "return_envelope_orders", "Cancel return envelope order"),

    # Events / Postal Statements
    "events.list": Endpoint("events.list", "GET", "/events", "events", "List events"),
    "postal_statements.list": Endpoint("postal_statements.list", "GET", "/postal_statements", "postal_statements", "Get postal statements"),
    "postal_statements.get": Endpoint("postal_statements.get", "GET", "/postal_statements/{id}", "postal_statements", "Get postal statement"),

    # Address verification (core)
    "addver.verify_standard": Endpoint("addver.verify_standard", "POST", "/addver/verifications", "address_verification", "Verify standard/freeform address", base="core"),
    "addver.verify_international": Endpoint("addver.verify_international", "POST", "/intl_addver/verifications", "address_verification", "Verify international address", base="core"),
    "addver.autocomplete_standard": Endpoint("addver.autocomplete_standard", "GET", "/addver/completions", "address_verification", "Autocomplete standard address", base="core"),
    "addver.autocomplete_international": Endpoint("addver.autocomplete_international", "GET", "/intl_addver/completions", "address_verification", "Autocomplete international address", base="core"),

    # Sub-organizations
    "sub_orgs.create": Endpoint("sub_orgs.create", "POST", "/sub_organizations", "sub_organizations", "Create sub-organization", base="core"),
    "sub_orgs.list": Endpoint("sub_orgs.list", "GET", "/sub_organizations", "sub_organizations", "List sub-organizations", base="core"),
    "sub_orgs.get": Endpoint("sub_orgs.get", "GET", "/sub_organizations/{id}", "sub_organizations", "Get sub-organization", base="core"),
    "sub_orgs.users": Endpoint("sub_orgs.users", "GET", "/sub_organizations/{id}/users", "sub_organizations", "List sub-organization users", base="core"),

    # Campaigns
    "campaigns.create": Endpoint("campaigns.create", "POST", "/campaigns", "campaigns", "Create campaign", base="core"),
    "campaigns.list": Endpoint("campaigns.list", "GET", "/campaigns", "campaigns", "List campaigns", base="core"),
    "campaigns.get": Endpoint("campaigns.get", "GET", "/campaigns/{id}", "campaigns", "Get campaign", base="core"),
    "campaigns.update": Endpoint("campaigns.update", "POST", "/campaigns/{id}", "campaigns", "Update campaign", base="core"),
    "campaigns.delete": Endpoint("campaigns.delete", "DELETE", "/campaigns/{id}", "campaigns", "Delete campaign", base="core"),
    "campaigns.send": Endpoint("campaigns.send", "POST", "/campaigns/{id}/send", "campaigns", "Send campaign", base="core"),

    # Virtual mailboxes
    "virtual_mailboxes.create": Endpoint("virtual_mailboxes.create", "POST", "/virtual_mailboxes", "virtual_mailboxes", "Create virtual mailbox"),
    "virtual_mailboxes.list": Endpoint("virtual_mailboxes.list", "GET", "/virtual_mailboxes", "virtual_mailboxes", "List virtual mailboxes"),
    "virtual_mailboxes.get": Endpoint("virtual_mailboxes.get", "GET", "/virtual_mailboxes/{id}", "virtual_mailboxes", "Retrieve virtual mailbox"),
    "virtual_mailboxes.address": Endpoint("virtual_mailboxes.address", "GET", "/virtual_mailboxes/{id}/physical_address", "virtual_mailboxes", "Retrieve virtual mailbox physical address"),
    "virtual_mailboxes.items": Endpoint("virtual_mailboxes.items", "GET", "/virtual_mailboxes/{id}/items", "virtual_mailboxes", "List virtual mailbox items"),
    "virtual_mailboxes.item_create_test": Endpoint("virtual_mailboxes.item_create_test", "POST", "/virtual_mailboxes/{id}/items", "virtual_mailboxes", "Create test virtual mailbox item"),
    "virtual_mailboxes.item_get": Endpoint("virtual_mailboxes.item_get", "GET", "/virtual_mailboxes/{id}/items/{itemId}", "virtual_mailboxes", "Retrieve virtual mailbox item"),

    # Snap packs
    "snap_packs.create": Endpoint("snap_packs.create", "POST", "/snap_packs", "snap_packs", "Create snap pack"),
    "snap_packs.list": Endpoint("snap_packs.list", "GET", "/snap_packs", "snap_packs", "List snap packs"),
    "snap_packs.capabilities": Endpoint("snap_packs.capabilities", "GET", "/snap_packs/capabilities", "snap_packs", "Get snap pack capabilities"),
    "snap_packs.get": Endpoint("snap_packs.get", "GET", "/snap_packs/{id}", "snap_packs", "Get snap pack"),
    "snap_packs.cancel": Endpoint("snap_packs.cancel", "DELETE", "/snap_packs/{id}", "snap_packs", "Cancel snap pack"),
    "snap_packs.progress": Endpoint("snap_packs.progress", "POST", "/snap_packs/{id}/progress", "snap_packs", "Progress snap pack status"),
}


class PostGridApiError(RuntimeError):
    pass


def parse_kv_pairs(pairs: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid key=value pair: {pair}")
        key, value = pair.split("=", 1)
        out[key] = value
    return out


def fill_path(path: str, path_params: Dict[str, str]) -> str:
    out = path
    for key, value in path_params.items():
        out = out.replace("{" + key + "}", urllib.parse.quote(str(value), safe=""))
    if "{" in out or "}" in out:
        raise ValueError(f"Missing path params for template: {out}")
    return out


def _load_body(args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    if args.body_json and args.body_file:
        raise ValueError("Use one of --body-json or --body-file")
    if args.body_json:
        payload = json.loads(args.body_json)
        if not isinstance(payload, dict):
            raise ValueError("--body-json must be a JSON object")
        return payload
    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if not isinstance(payload, dict):
            raise ValueError("--body-file must contain a JSON object")
        return payload
    return None


def _request(
    method: str,
    base_url: str,
    path: str,
    api_key: str,
    query: Optional[Dict[str, str]] = None,
    body: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    key_header: str = "x-api-key",
) -> Dict[str, Any]:
    base = base_url.rstrip("/")
    url = base + path
    if query:
        clean = {k: v for k, v in query.items() if v is not None}
        if clean:
            url += "?" + urllib.parse.urlencode(clean, doseq=True)

    headers: Dict[str, str] = {
        "Accept": "application/json",
        key_header: api_key,
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url=url, method=method.upper(), headers=headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise PostGridApiError(f"HTTP {exc.code} {method} {path}: {raw}") from exc
    except urllib.error.URLError as exc:
        raise PostGridApiError(f"Request failed {method} {path}: {exc}") from exc


def _resolve_api_key(args: argparse.Namespace) -> str:
    api_key = args.api_key or os.getenv("POSTGRID_API_KEY")
    if not api_key:
        raise PostGridApiError("Missing API key. Set POSTGRID_API_KEY or pass --api-key.")
    return api_key


def _base_for(endpoint: Endpoint, args: argparse.Namespace) -> str:
    if endpoint.base == "core":
        return args.core_base_url
    return args.print_mail_base_url


def cmd_list_endpoints(args: argparse.Namespace) -> int:
    rows = []
    for ep in ENDPOINTS.values():
        rows.append({
            "key": ep.key,
            "method": ep.method,
            "path": ep.path,
            "group": ep.group,
            "base": ep.base,
            "description": ep.description,
        })
    rows.sort(key=lambda x: x["key"])
    print(json.dumps(rows, indent=2))
    return 0


def cmd_describe(args: argparse.Namespace) -> int:
    ep = ENDPOINTS.get(args.endpoint)
    if ep is None:
        print(f"Unknown endpoint key: {args.endpoint}", file=sys.stderr)
        return 2
    print(json.dumps(ep.__dict__, indent=2))
    return 0


def cmd_call(args: argparse.Namespace) -> int:
    ep = ENDPOINTS.get(args.endpoint)
    if ep is None:
        print(f"Unknown endpoint key: {args.endpoint}", file=sys.stderr)
        return 2

    try:
        api_key = _resolve_api_key(args)
        path_params = parse_kv_pairs(args.path_param)
        query = parse_kv_pairs(args.query)
        body = _load_body(args)
        path = fill_path(ep.path, path_params)
        base_url = _base_for(ep, args)
        response = _request(
            method=ep.method,
            base_url=base_url,
            path=path,
            api_key=api_key,
            query=query,
            body=body,
            timeout=args.timeout,
            key_header=args.key_header,
        )
        print(json.dumps(response, indent=2))
        return 0
    except (ValueError, json.JSONDecodeError, PostGridApiError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


def cmd_call_raw(args: argparse.Namespace) -> int:
    try:
        api_key = _resolve_api_key(args)
        query = parse_kv_pairs(args.query)
        body = _load_body(args)
        base_url = args.base_url
        path = args.path if args.path.startswith("/") else "/" + args.path
        response = _request(
            method=args.method,
            base_url=base_url,
            path=path,
            api_key=api_key,
            query=query,
            body=body,
            timeout=args.timeout,
            key_header=args.key_header,
        )
        print(json.dumps(response, indent=2))
        return 0
    except (ValueError, json.JSONDecodeError, PostGridApiError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PostGrid API catalog + raw caller")
    p.add_argument("--api-key", help="PostGrid API key (or POSTGRID_API_KEY env var)")
    p.add_argument("--key-header", default="x-api-key", help="API key header name (default: x-api-key)")
    p.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds")
    p.add_argument("--print-mail-base-url", default=DEFAULT_PRINT_MAIL_BASE_URL, help=f"Print & Mail base URL (default: {DEFAULT_PRINT_MAIL_BASE_URL})")
    p.add_argument("--core-base-url", default=DEFAULT_CORE_BASE_URL, help=f"Core base URL (default: {DEFAULT_CORE_BASE_URL})")

    sub = p.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list-endpoints", help="List cataloged endpoints")
    p_list.set_defaults(func=cmd_list_endpoints)

    p_desc = sub.add_parser("describe", help="Describe one endpoint key")
    p_desc.add_argument("endpoint", help="Endpoint key")
    p_desc.set_defaults(func=cmd_describe)

    p_call = sub.add_parser("call", help="Call cataloged endpoint")
    p_call.add_argument("endpoint", help="Endpoint key")
    p_call.add_argument("--path-param", action="append", default=[], help="Path params key=value")
    p_call.add_argument("--query", action="append", default=[], help="Query params key=value")
    p_call.add_argument("--body-json", help="Inline JSON body")
    p_call.add_argument("--body-file", help="JSON file body")
    p_call.set_defaults(func=cmd_call)

    p_raw = sub.add_parser("call-raw", help="Call any PostGrid endpoint path directly")
    p_raw.add_argument("method", help="HTTP method")
    p_raw.add_argument("path", help="Path beginning with /")
    p_raw.add_argument("--base-url", default=DEFAULT_PRINT_MAIL_BASE_URL, help="Base URL for raw call")
    p_raw.add_argument("--query", action="append", default=[], help="Query params key=value")
    p_raw.add_argument("--body-json", help="Inline JSON body")
    p_raw.add_argument("--body-file", help="JSON file body")
    p_raw.set_defaults(func=cmd_call_raw)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
