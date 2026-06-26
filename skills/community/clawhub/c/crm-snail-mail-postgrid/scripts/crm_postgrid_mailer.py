#!/usr/bin/env python3
"""Pull contacts from GHL/FUB and send direct mail via PostGrid."""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

DEFAULT_GHL_BASE_URL = "https://services.leadconnectorhq.com"
DEFAULT_FUB_BASE_URL = "https://api.followupboss.com/v1"
DEFAULT_POSTGRID_BASE_URL = "https://api.postgrid.com/print-mail/v1"


class MailerError(RuntimeError):
    pass


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _pick(data: Dict[str, Any], keys: Sequence[str], default: Optional[Any] = None) -> Optional[Any]:
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        if isinstance(value, str):
            value = value.strip()
            if not value:
                continue
        return value
    return default


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _render_template(template: str, values: Dict[str, Any]) -> str:
    pattern = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        val = values.get(key)
        return "" if val is None else str(val)

    return pattern.sub(repl, template)


def _deep_merge(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in src.items():
        if isinstance(value, dict) and isinstance(dst.get(key), dict):
            _deep_merge(dst[key], value)
        else:
            dst[key] = value
    return dst


def _text_to_html(text: str) -> str:
    text = text.replace("\\n", "\n")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [text.strip()]
    body = "\n".join(f"    <p>{html.escape(p).replace(chr(10), '<br/>')}</p>" for p in paragraphs if p)
    return "<!doctype html>\n<html>\n  <body style=\"font-family: Arial, sans-serif; line-height: 1.5;\">\n" + body + "\n  </body>\n</html>\n"


def _http_json(
    method: str,
    url: str,
    headers: Dict[str, str],
    body: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    data = None
    req_headers = dict(headers)
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        req_headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, method=method.upper(), headers=req_headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise MailerError(f"HTTP {exc.code} {method} {url}: {raw}") from exc
    except urllib.error.URLError as exc:
        raise MailerError(f"Request failed {method} {url}: {exc}") from exc


def _normalize_contact(contact: Dict[str, Any], provider: str) -> Dict[str, Any]:
    first_name = _pick(contact, ["firstName", "first_name", "firstname", "givenName"])
    last_name = _pick(contact, ["lastName", "last_name", "lastname", "familyName"])

    if not first_name and not last_name:
        full_name = _pick(contact, ["name", "fullName", "displayName"])
        if isinstance(full_name, str) and full_name.strip():
            parts = full_name.strip().split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

    emails = _as_list(_pick(contact, ["emails", "email"]))
    email = None
    for item in emails:
        if isinstance(item, str) and item.strip():
            email = item.strip()
            break
        if isinstance(item, dict):
            candidate = _pick(item, ["value", "email", "address"])
            if candidate:
                email = str(candidate)
                break

    phones = _as_list(_pick(contact, ["phones", "phone"]))
    phone = None
    for item in phones:
        if isinstance(item, str) and item.strip():
            phone = item.strip()
            break
        if isinstance(item, dict):
            candidate = _pick(item, ["value", "number", "phone"])
            if candidate:
                phone = str(candidate)
                break

    address = _pick(contact, ["address", "primaryAddress"], default={})
    address = address if isinstance(address, dict) else {}

    normalized = {
        "provider": provider,
        "id": _pick(contact, ["id", "_id", "contactId", "personId"]),
        "first_name": first_name or "",
        "last_name": last_name or "",
        "full_name": " ".join([v for v in [first_name, last_name] if v]).strip(),
        "email": email or "",
        "phone": phone or "",
        "address1": _pick(
            contact,
            ["address1", "addressLine1", "streetAddress"],
            default=_pick(address, ["address1", "addressLine1", "streetAddress"]),
        )
        or "",
        "address2": _pick(
            contact,
            ["address2", "addressLine2"],
            default=_pick(address, ["address2", "addressLine2"]),
        )
        or "",
        "city": _pick(contact, ["city"], default=_pick(address, ["city", "locality"])) or "",
        "state": _pick(contact, ["state", "province"], default=_pick(address, ["state", "province"])) or "",
        "postal_code": _pick(
            contact,
            ["postalCode", "zip", "postal_code"],
            default=_pick(address, ["postalCode", "zip", "postal_code"]),
        )
        or "",
        "country": _pick(contact, ["country"], default=_pick(address, ["country"])) or "US",
        "tags": _as_list(_pick(contact, ["tags", "tagIds", "labels"], default=[])),
        "raw": contact,
    }

    if not normalized["full_name"]:
        normalized["full_name"] = _pick(contact, ["name", "fullName", "displayName"], default="") or ""

    return normalized


def _extract_ghl_contacts(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ("contacts", "data", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    if isinstance(payload.get("contact"), dict):
        return [payload["contact"]]
    return []


def _extract_fub_people(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    people = payload.get("people")
    if isinstance(people, list):
        return [item for item in people if isinstance(item, dict)]
    embedded = payload.get("_embedded")
    if isinstance(embedded, dict):
        for value in embedded.values():
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    for key in ("items", "results", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def fetch_contacts_from_ghl(args: argparse.Namespace) -> List[Dict[str, Any]]:
    api_key = args.api_key or os.getenv("GHL_API_KEY")
    if not api_key:
        raise MailerError("Missing GHL API key. Set GHL_API_KEY or pass --api-key.")

    base_url = (args.base_url or os.getenv("GHL_BASE_URL") or DEFAULT_GHL_BASE_URL).rstrip("/")
    query: Dict[str, Any] = {"limit": args.limit}
    if args.location_id:
        query["locationId"] = args.location_id

    url = f"{base_url}/contacts/?{urllib.parse.urlencode(query)}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Version": args.ghl_version,
    }
    payload = _http_json("GET", url, headers=headers, timeout=args.timeout)
    contacts = _extract_ghl_contacts(payload)
    return [_normalize_contact(item, "ghl") for item in contacts]


def fetch_contacts_from_fub(args: argparse.Namespace) -> List[Dict[str, Any]]:
    api_key = args.api_key or os.getenv("FUB_API_KEY")
    if not api_key:
        raise MailerError("Missing FUB API key. Set FUB_API_KEY or pass --api-key.")

    base_url = (args.base_url or os.getenv("FUB_BASE_URL") or DEFAULT_FUB_BASE_URL).rstrip("/")
    auth_header = base64.b64encode(f"{api_key}:".encode("utf-8")).decode("ascii")

    query = {"limit": args.limit}
    url = f"{base_url}/people?{urllib.parse.urlencode(query)}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {auth_header}",
    }

    payload = _http_json("GET", url, headers=headers, timeout=args.timeout)
    people = _extract_fub_people(payload)
    return [_normalize_contact(item, "fub") for item in people]


def _load_contacts_file(path: str) -> List[Dict[str, Any]]:
    data = _read_json(path)
    if isinstance(data, list):
        raw_contacts = data
    elif isinstance(data, dict):
        for key in ("contacts", "people", "items", "results", "data"):
            value = data.get(key)
            if isinstance(value, list):
                raw_contacts = value
                break
        else:
            raw_contacts = []
    else:
        raw_contacts = []

    out: List[Dict[str, Any]] = []
    for item in raw_contacts:
        if not isinstance(item, dict):
            continue
        if {"address1", "city", "state", "postal_code"}.issubset(item.keys()):
            out.append(item)
        else:
            provider = str(item.get("provider") or "external")
            out.append(_normalize_contact(item, provider=provider))
    return out


def _has_required_address(contact: Dict[str, Any]) -> bool:
    required = ["address1", "city", "state", "postal_code"]
    return all(str(contact.get(k, "")).strip() for k in required)


def _build_to_object(contact: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "firstName": contact.get("first_name", ""),
        "lastName": contact.get("last_name", ""),
        "addressLine1": contact.get("address1", ""),
        "addressLine2": contact.get("address2", ""),
        "city": contact.get("city", ""),
        "provinceOrState": contact.get("state", ""),
        "postalOrZip": contact.get("postal_code", ""),
        "country": contact.get("country", "US"),
    }


def _build_mail_payload(
    contact: Dict[str, Any],
    sender: Dict[str, Any],
    description: str,
    html_template: Optional[str],
    overrides: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "to": _build_to_object(contact),
        "from": sender,
        "description": description,
        "mergeVariables": {
            "id": contact.get("id"),
            "first_name": contact.get("first_name"),
            "last_name": contact.get("last_name"),
            "full_name": contact.get("full_name"),
            "email": contact.get("email"),
            "phone": contact.get("phone"),
            "city": contact.get("city"),
            "state": contact.get("state"),
            "postal_code": contact.get("postal_code"),
        },
    }

    if html_template is not None:
        render_values = dict(payload["mergeVariables"])
        render_values["agent_name"] = _pick(sender, ["fullName", "firstName", "companyName"], default="") or ""
        payload["html"] = _render_template(html_template, render_values)

    if overrides:
        payload = _deep_merge(payload, overrides)

    return payload


def _load_overrides(args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    if args.payload_overrides_json and args.payload_overrides_file:
        raise MailerError("Use only one of --payload-overrides-json or --payload-overrides-file")
    if args.payload_overrides_json:
        parsed = json.loads(args.payload_overrides_json)
        if not isinstance(parsed, dict):
            raise MailerError("--payload-overrides-json must be a JSON object")
        return parsed
    if args.payload_overrides_file:
        parsed = _read_json(args.payload_overrides_file)
        if not isinstance(parsed, dict):
            raise MailerError("--payload-overrides-file must contain a JSON object")
        return parsed
    return None


def _postgrid_send(
    payload: Dict[str, Any],
    route: str,
    base_url: str,
    api_key: str,
    api_key_header: str,
    timeout: int,
) -> Dict[str, Any]:
    base = base_url.rstrip("/")
    clean_route = route.strip().lstrip("/")
    url = f"{base}/{clean_route}"
    headers = {
        "Accept": "application/json",
        api_key_header: api_key,
    }
    return _http_json("POST", url, headers=headers, body=payload, timeout=timeout)


def _run_fetch(provider: str, args: argparse.Namespace) -> List[Dict[str, Any]]:
    if provider == "ghl":
        return fetch_contacts_from_ghl(args)
    if provider == "fub":
        return fetch_contacts_from_fub(args)
    raise MailerError(f"Unsupported provider: {provider}")


def cmd_fetch(args: argparse.Namespace) -> int:
    try:
        contacts = _run_fetch(args.provider, args)
    except MailerError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    _write_json(args.output, contacts)
    print(json.dumps({"output": args.output, "count": len(contacts)}, indent=2))
    return 0


def _resolve_contacts_for_send(args: argparse.Namespace) -> List[Dict[str, Any]]:
    if args.contacts_file:
        return _load_contacts_file(args.contacts_file)
    raise MailerError("Missing contacts source. Pass --contacts-file.")


def _execute_send(args: argparse.Namespace, contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
    api_key = args.postgrid_api_key or os.getenv("POSTGRID_API_KEY")
    if not api_key and not args.dry_run:
        raise MailerError("Missing POSTGRID_API_KEY or --postgrid-api-key for live send")

    sender = _read_json(args.from_json_file)
    if not isinstance(sender, dict):
        raise MailerError("--from-json-file must contain a JSON object")

    html_template = None
    if args.html_template_file:
        html_template = Path(args.html_template_file).read_text(encoding="utf-8")

    overrides = _load_overrides(args)

    base_url = (args.postgrid_base_url or os.getenv("POSTGRID_BASE_URL") or DEFAULT_POSTGRID_BASE_URL).rstrip("/")
    route = args.postgrid_route or args.mail_route

    total = len(contacts)
    sent = 0
    skipped = 0
    failed = 0
    results: List[Dict[str, Any]] = []

    limit = args.max_send if args.max_send and args.max_send > 0 else total

    for idx, contact in enumerate(contacts):
        if idx >= limit:
            break

        contact_id = str(contact.get("id") or f"row-{idx+1}")
        if args.require_address and not _has_required_address(contact):
            skipped += 1
            results.append({
                "contact_id": contact_id,
                "status": "skipped",
                "reason": "missing_required_address",
            })
            continue

        payload = _build_mail_payload(
            contact=contact,
            sender=sender,
            description=args.description,
            html_template=html_template,
            overrides=overrides,
        )

        if args.dry_run:
            sent += 1
            results.append({
                "contact_id": contact_id,
                "status": "dry_run",
                "payload": payload,
            })
            continue

        try:
            response = _postgrid_send(
                payload=payload,
                route=route,
                base_url=base_url,
                api_key=api_key,
                api_key_header=args.postgrid_key_header,
                timeout=args.timeout,
            )
            sent += 1
            results.append({
                "contact_id": contact_id,
                "status": "sent",
                "response": response,
            })
        except MailerError as exc:
            failed += 1
            results.append({
                "contact_id": contact_id,
                "status": "failed",
                "error": str(exc),
            })

    summary = {
        "total_contacts_input": total,
        "attempted": min(total, limit),
        "sent_or_dry_run": sent,
        "skipped": skipped,
        "failed": failed,
        "results": results,
    }
    return summary


def cmd_send(args: argparse.Namespace) -> int:
    try:
        contacts = _resolve_contacts_for_send(args)
        summary = _execute_send(args, contacts)
    except (MailerError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.output:
        _write_json(args.output, summary)
    print(json.dumps(summary, indent=2))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    try:
        if args.contacts_file:
            contacts = _load_contacts_file(args.contacts_file)
        else:
            contacts = _run_fetch(args.provider, args)
        summary = _execute_send(args, contacts)
    except (MailerError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.contacts_output:
        _write_json(args.contacts_output, contacts)
    if args.output:
        _write_json(args.output, summary)

    result = {
        "contacts_count": len(contacts),
        "summary": summary,
        "contacts_output": args.contacts_output,
        "output": args.output,
    }
    print(json.dumps(result, indent=2))
    return 0


def _resolve_one_off_html(args: argparse.Namespace) -> str:
    provided = sum(
        1
        for value in [args.content_html, args.content_html_file, args.content_text, args.content_text_file]
        if value
    )
    if provided == 0:
        raise MailerError("Provide one content input via --content-text, --content-text-file, --content-html, or --content-html-file")
    if provided > 1:
        raise MailerError("Provide only one content input")

    if args.content_html:
        return args.content_html
    if args.content_html_file:
        return Path(args.content_html_file).read_text(encoding="utf-8")
    if args.content_text:
        return _text_to_html(args.content_text)
    return _text_to_html(Path(args.content_text_file).read_text(encoding="utf-8"))


def _build_one_off_contact(args: argparse.Namespace) -> Dict[str, Any]:
    first_name = args.to_first_name or ""
    last_name = args.to_last_name or ""

    if args.to_name and not (first_name or last_name):
        parts = args.to_name.strip().split(" ", 1)
        first_name = parts[0] if parts else ""
        last_name = parts[1] if len(parts) > 1 else ""

    full_name = " ".join([v for v in [first_name, last_name] if v]).strip() or (args.to_name or "")
    return {
        "id": "one-off-recipient",
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "email": args.to_email or "",
        "phone": args.to_phone or "",
        "address1": args.to_address1,
        "address2": args.to_address2 or "",
        "city": args.to_city,
        "state": args.to_state,
        "postal_code": args.to_postal_code,
        "country": args.to_country,
    }


def cmd_one_off(args: argparse.Namespace) -> int:
    try:
        sender = _read_json(args.from_json_file)
        if not isinstance(sender, dict):
            raise MailerError("--from-json-file must contain a JSON object")
        recipient = _build_one_off_contact(args)
        html_content = _resolve_one_off_html(args)
        overrides = _load_overrides(args)
        payload = _build_mail_payload(
            contact=recipient,
            sender=sender,
            description=args.description,
            html_template=None,
            overrides=overrides,
        )
        payload["html"] = html_content

        if args.dry_run:
            summary = {"status": "dry_run", "payload": payload}
        else:
            api_key = args.postgrid_api_key or os.getenv("POSTGRID_API_KEY")
            if not api_key:
                raise MailerError("Missing POSTGRID_API_KEY or --postgrid-api-key for live send")
            base_url = (args.postgrid_base_url or os.getenv("POSTGRID_BASE_URL") or DEFAULT_POSTGRID_BASE_URL).rstrip("/")
            route = args.postgrid_route or args.mail_route
            response = _postgrid_send(
                payload=payload,
                route=route,
                base_url=base_url,
                api_key=api_key,
                api_key_header=args.postgrid_key_header,
                timeout=args.timeout,
            )
            summary = {"status": "sent", "response": response}
    except (MailerError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.output:
        _write_json(args.output, summary)
    print(json.dumps(summary, indent=2))
    return 0


def _add_shared_fetch_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--provider", choices=["ghl", "fub"], required=False, default="fub")
    parser.add_argument("--api-key", help="CRM API key override. Uses provider-specific env var by default.")
    parser.add_argument("--base-url", help="CRM base URL override. Uses provider-specific env var by default.")
    parser.add_argument("--limit", type=int, default=100, help="Max contacts to request")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout (seconds)")
    parser.add_argument("--location-id", help="GHL location ID (optional)")
    parser.add_argument("--ghl-version", default="2021-07-28", help="GHL API version header")


def _add_send_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contacts-file", help="Normalized contacts JSON file or raw CRM export JSON file")
    parser.add_argument("--from-json-file", required=True, help="Sender JSON file used as PostGrid 'from' object")
    parser.add_argument("--html-template-file", help="HTML template with {{first_name}} style placeholders")
    parser.add_argument("--mail-route", default="letters", help="Mail type route alias, e.g. letters or postcards")
    parser.add_argument("--postgrid-route", help="Explicit PostGrid route path. Overrides --mail-route")
    parser.add_argument("--description", default="CRM direct-mail campaign", help="PostGrid job description")
    parser.add_argument("--postgrid-api-key", help="PostGrid API key override (else POSTGRID_API_KEY)")
    parser.add_argument(
        "--postgrid-base-url",
        default=DEFAULT_POSTGRID_BASE_URL,
        help=f"PostGrid API base URL (default: {DEFAULT_POSTGRID_BASE_URL})",
    )
    parser.add_argument("--postgrid-key-header", default="x-api-key", help="PostGrid API key header name")
    parser.add_argument("--payload-overrides-json", help="JSON object merged into every payload")
    parser.add_argument("--payload-overrides-file", help="JSON file merged into every payload")
    parser.add_argument("--max-send", type=int, default=0, help="Limit sends for controlled rollout (0 = no cap)")
    parser.add_argument("--require-address", action="store_true", default=True, help="Skip contacts missing address")
    parser.add_argument("--dry-run", action="store_true", help="Do not call PostGrid; print generated payloads")
    parser.add_argument("--output", help="Write send summary JSON to file")


def _add_one_off_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--to-name", help="Recipient full name")
    parser.add_argument("--to-first-name", help="Recipient first name")
    parser.add_argument("--to-last-name", help="Recipient last name")
    parser.add_argument("--to-email", help="Recipient email (optional)")
    parser.add_argument("--to-phone", help="Recipient phone (optional)")
    parser.add_argument("--to-address1", required=True, help="Recipient address line 1")
    parser.add_argument("--to-address2", help="Recipient address line 2")
    parser.add_argument("--to-city", required=True, help="Recipient city")
    parser.add_argument("--to-state", required=True, help="Recipient state/province")
    parser.add_argument("--to-postal-code", required=True, help="Recipient postal/zip")
    parser.add_argument("--to-country", default="US", help="Recipient country code (default: US)")
    parser.add_argument("--from-json-file", required=True, help="Sender JSON file used as PostGrid 'from' object")
    parser.add_argument("--content-text", help="Mail body plain text; converted to simple HTML")
    parser.add_argument("--content-text-file", help="File containing plain-text body content")
    parser.add_argument("--content-html", help="Mail body HTML")
    parser.add_argument("--content-html-file", help="File containing HTML body content")
    parser.add_argument("--mail-route", default="letters", help="Mail type route alias, e.g. letters or postcards")
    parser.add_argument("--postgrid-route", help="Explicit PostGrid route path. Overrides --mail-route")
    parser.add_argument("--description", default="One-off direct-mail campaign", help="PostGrid job description")
    parser.add_argument("--postgrid-api-key", help="PostGrid API key override (else POSTGRID_API_KEY)")
    parser.add_argument(
        "--postgrid-base-url",
        default=DEFAULT_POSTGRID_BASE_URL,
        help=f"PostGrid API base URL (default: {DEFAULT_POSTGRID_BASE_URL})",
    )
    parser.add_argument("--postgrid-key-header", default="x-api-key", help="PostGrid API key header name")
    parser.add_argument("--payload-overrides-json", help="JSON object merged into payload")
    parser.add_argument("--payload-overrides-file", help="JSON file merged into payload")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout (seconds)")
    parser.add_argument("--dry-run", action="store_true", help="Do not call PostGrid; print generated payload")
    parser.add_argument("--output", help="Write result JSON to file")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CRM to PostGrid mailer")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fetch = sub.add_parser("fetch", help="Fetch contacts from CRM and normalize")
    _add_shared_fetch_args(p_fetch)
    p_fetch.add_argument("--output", required=True, help="Output JSON file for normalized contacts")
    p_fetch.set_defaults(func=cmd_fetch)

    p_send = sub.add_parser("send", help="Send mail from contacts JSON")
    _add_send_args(p_send)
    p_send.set_defaults(func=cmd_send)

    p_run = sub.add_parser("run", help="Fetch from CRM (or use contacts file) then send")
    _add_shared_fetch_args(p_run)
    p_run.add_argument("--contacts-output", help="Write normalized contacts to this file")
    _add_send_args(p_run)
    p_run.set_defaults(func=cmd_run)

    p_one_off = sub.add_parser("one-off", help="Send one mailer from direct address + content")
    _add_one_off_args(p_one_off)
    p_one_off.set_defaults(func=cmd_one_off)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
