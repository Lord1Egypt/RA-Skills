#!/usr/bin/env python3
"""Shared HTTP and validation helpers for AI Web API skills."""

from __future__ import annotations

import ipaddress
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


ENV_BASE_URL = "AI_WEB_API_BASE_URL"
DEFAULT_BASE_URL = "https://aiwebapi.dataify.com"
ENV_TOKEN = "DATAIFY_API_TOKEN"
DEFAULT_REQUEST_TIMEOUT = 300
EXTRACT_FORMATS = {"markdown", "raw_html", "clean_html", "links"}
HOP_BY_HOP_HEADERS = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailer", "transfer-encoding", "upgrade",
}


def configure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError):
                pass


def normalize_base_url(value: str) -> str:
    raw = value.strip().rstrip("/")
    parsed = urllib.parse.urlsplit(raw)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("AI_WEB_API_BASE_URL must be a complete http:// or https:// origin.")
    if parsed.query or parsed.fragment:
        raise ValueError("AI_WEB_API_BASE_URL must not include a query or fragment.")
    return raw


def resolve_base_url(cli_value: str | None, required: bool = True) -> str:
    value = (cli_value or os.environ.get(ENV_BASE_URL, "") or DEFAULT_BASE_URL).strip()
    if not value:
        if required:
            raise ValueError("AI_WEB_API_BASE_URL is empty.")
        return ""
    return normalize_base_url(value)


def resolve_token() -> str:
    return os.environ.get(ENV_TOKEN, "").strip()


def normalize_public_url(value: str) -> str:
    raw = value.strip()
    try:
        parsed = urllib.parse.urlsplit(raw)
    except ValueError as exc:
        raise ValueError("Invalid URL: {}".format(exc)) from exc
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL must be a complete public http:// or https:// address.")
    if parsed.username or parsed.password:
        raise ValueError("URL user information is not allowed.")
    hostname = parsed.hostname.lower()
    if hostname == "localhost" or hostname.endswith(".local"):
        raise ValueError("Local hostnames are not allowed.")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return raw
    if not address.is_global:
        raise ValueError("Private, loopback, link-local, and reserved IPs are not allowed.")
    return raw


def validate_country(value: str | None) -> str | None:
    if value is None:
        return None
    country = value.strip().upper()
    if len(country) != 2 or not country.isalpha():
        raise ValueError("country must be a two-letter country code.")
    return country


def validate_int_range(name: str, value: int | None, minimum: int, maximum: int) -> int | None:
    if value is None:
        return None
    if value < minimum or value > maximum:
        raise ValueError("{} must be between {} and {}.".format(name, minimum, maximum))
    return value


def validate_formats(values: list[str] | None) -> list[str]:
    formats = list(values or [])
    if len(set(formats)) != len(formats):
        raise ValueError("formats must not contain duplicates.")
    invalid = [item for item in formats if item not in EXTRACT_FORMATS]
    if invalid:
        raise ValueError("Unsupported formats: {}".format(", ".join(invalid)))
    return formats


def validate_string_list(name: str, values: list[str] | None, max_items: int = 50, max_bytes: int = 2048) -> list[str]:
    result = list(values or [])
    if len(result) > max_items:
        raise ValueError("{} supports at most {} items.".format(name, max_items))
    for item in result:
        if not item or len(item.encode("utf-8")) > max_bytes:
            raise ValueError("{} items must be non-empty and no longer than {} bytes.".format(name, max_bytes))
    return result


def parse_headers(values: list[str] | None) -> dict[str, str]:
    headers: dict[str, str] = {}
    for raw in values or []:
        separator = ":" if ":" in raw else "="
        if separator not in raw:
            raise ValueError("headers must use 'Name: Value' or 'Name=Value'.")
        name, value = raw.split(separator, 1)
        name, value = name.strip(), value.strip()
        lowered = name.lower()
        if not name or not value or "\n" in name or "\n" in value:
            raise ValueError("headers must contain non-empty names and values.")
        if lowered == "host" or lowered in HOP_BY_HOP_HEADERS:
            raise ValueError("header {} is not allowed.".format(name))
        headers[name] = value
    return headers


def emit_dry_run(path: str, payload: dict, base_url: str, token: str) -> None:
    endpoint = (base_url + path) if base_url else "<{}>{}".format(ENV_BASE_URL, path)
    print(json.dumps({
        "endpoint": endpoint,
        "authorization": "Bearer <redacted>" if token else "Bearer <missing {}>".format(ENV_TOKEN),
        "body": payload,
    }, ensure_ascii=False, indent=2))


def post_json(path: str, payload: dict, base_url: str, token: str, request_timeout: int = DEFAULT_REQUEST_TIMEOUT) -> int:
    endpoint = base_url.rstrip("/") + path
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(endpoint, data=body, headers={
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=request_timeout) as response:
            content = response.read()
            request_id = response.headers.get("X-Request-Id")
            if request_id:
                print("X-Request-Id: {}".format(request_id), file=sys.stderr)
            if content:
                charset = response.headers.get_content_charset() or "utf-8"
                sys.stdout.write(content.decode(charset, errors="replace"))
                if not content.endswith(b"\n"):
                    sys.stdout.write("\n")
            return 0
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        print(error_body or "HTTP {}".format(exc.code), file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print("Request failed: {}".format(exc.reason), file=sys.stderr)
        return 1
