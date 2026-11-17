#!/usr/bin/env python3
"""Validate a guarded browser discovery snapshot and store it in runtime state."""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any

from discover_store import (
    POLICY_TERMS,
    atomic_json,
    normalized_host,
    runtime_config,
    runtime_dir,
    update_runtime_config,
    utc_now,
)

MAX_PRODUCTS = 200
MAX_CAMPAIGNS = 80
MAX_POLICIES = 80
MAX_SOURCES = 200
ALLOWED_SOURCE_TYPES = {"page", "robots", "sitemap", "browser"}
ALLOWED_ROBOTS_STATUS = {"loaded", "browser_checked", "enforced_by_browser_tool"}


def text_value(value: Any, field: str, limit: int, required: bool = False) -> str:
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    cleaned = " ".join(value.split())
    if required and not cleaned:
        raise ValueError(f"{field} is required")
    if len(cleaned) > limit:
        raise ValueError(f"{field} exceeds the {limit}-character limit")
    return cleaned


def public_browser_url(value: Any, field: str, approved_host: str | None = None) -> str:
    raw = text_value(value, field, 2048, required=True)
    parsed = urllib.parse.urlsplit(raw)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"{field} must use http or https")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(f"{field} must contain a hostname and no credentials")
    host = parsed.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        raise ValueError(f"{field} cannot use a local hostname")
    try:
        literal_ip = ipaddress.ip_address(host.split("%", 1)[0])
    except ValueError:
        literal_ip = None
    if literal_ip is not None and not literal_ip.is_global:
        raise ValueError(f"{field} cannot use a non-public IP address")
    if approved_host and normalized_host(host) != normalized_host(approved_host):
        raise ValueError(f"{field} crosses the approved storefront host: {host}")
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path or "/", parsed.query, "")
    )


def list_value(payload: dict[str, Any], field: str, limit: int) -> list[Any]:
    value = payload.get(field, [])
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    if len(value) > limit:
        raise ValueError(f"{field} exceeds the {limit}-item limit")
    return value


def source_record(url: str, kind: str, retrieved_at: str) -> dict[str, str]:
    return {"url": url, "type": kind, "retrieved_at": retrieved_at}


def normalize_snapshot(raw: dict[str, Any]) -> dict[str, Any]:
    if raw.get("public_sources_only") is not True:
        raise ValueError("public_sources_only must be true")
    if raw.get("read_only") is not True:
        raise ValueError("read_only must be true")

    storefront_url = public_browser_url(raw.get("storefront_url"), "storefront_url")
    parsed = urllib.parse.urlsplit(storefront_url)
    approved_host = parsed.hostname or ""
    origin = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
    retrieved_at = utc_now()

    robots = raw.get("robots")
    if not isinstance(robots, dict) or robots.get("respected") is not True:
        raise ValueError("robots.respected must be true")
    robots_status = text_value(robots.get("status"), "robots.status", 64, True)
    if robots_status not in ALLOWED_ROBOTS_STATUS:
        raise ValueError(f"Unsupported robots.status: {robots_status}")
    robots_url = public_browser_url(
        robots.get("url") or f"{origin}/robots.txt", "robots.url", approved_host
    )

    platform_raw = raw.get("platform", {})
    if not isinstance(platform_raw, dict):
        raise ValueError("platform must be an object")
    platform_name = text_value(platform_raw.get("name", "unknown"), "platform.name", 80)
    try:
        confidence = float(platform_raw.get("confidence", 0.0))
    except (TypeError, ValueError) as exc:
        raise ValueError("platform.confidence must be a number") from exc
    if not 0 <= confidence <= 1:
        raise ValueError("platform.confidence must be between 0 and 1")
    platform_evidence = [
        text_value(item, "platform.evidence", 300, True)
        for item in list_value(platform_raw, "evidence", 10)
    ]

    sources: list[dict[str, str]] = []
    observed_sources: set[tuple[str, str]] = set()

    def add_source(url: str, kind: str = "page") -> None:
        key = (url, kind)
        if key not in observed_sources:
            observed_sources.add(key)
            sources.append(source_record(url, kind, retrieved_at))

    add_source(robots_url, "robots")
    products: list[dict[str, Any]] = []
    for index, item in enumerate(list_value(raw, "products", MAX_PRODUCTS)):
        if not isinstance(item, dict):
            raise ValueError(f"products[{index}] must be an object")
        url = public_browser_url(item.get("url"), f"products[{index}].url", approved_host)
        source_url = public_browser_url(
            item.get("source_url") or url,
            f"products[{index}].source_url",
            approved_host,
        )
        products.append(
            {
                "name": text_value(item.get("name"), f"products[{index}].name", 300, True),
                "sku": text_value(item.get("sku"), f"products[{index}].sku", 160),
                "url": url,
                "price": text_value(item.get("price"), f"products[{index}].price", 80),
                "currency": text_value(item.get("currency"), f"products[{index}].currency", 20),
                "availability": text_value(
                    item.get("availability"), f"products[{index}].availability", 120
                ),
                "source_url": source_url,
                "retrieved_at": retrieved_at,
                "status": "public_source_unverified_applicability",
            }
        )
        add_source(source_url)

    campaigns: list[dict[str, Any]] = []
    for index, item in enumerate(list_value(raw, "campaigns", MAX_CAMPAIGNS)):
        if not isinstance(item, dict):
            raise ValueError(f"campaigns[{index}] must be an object")
        url = public_browser_url(item.get("url"), f"campaigns[{index}].url", approved_host)
        campaigns.append(
            {
                "evidence": text_value(
                    item.get("evidence"), f"campaigns[{index}].evidence", 500, True
                ),
                "url": url,
                "retrieved_at": retrieved_at,
                "status": "public_claim_unverified_applicability",
            }
        )
        add_source(url)

    policies: list[dict[str, Any]] = []
    for index, item in enumerate(list_value(raw, "policies", MAX_POLICIES)):
        if not isinstance(item, dict):
            raise ValueError(f"policies[{index}] must be an object")
        kind = text_value(item.get("kind"), f"policies[{index}].kind", 40, True)
        if kind not in POLICY_TERMS:
            raise ValueError(f"Unsupported policy kind: {kind}")
        url = public_browser_url(item.get("url"), f"policies[{index}].url", approved_host)
        excerpt = text_value(
            item.get("text_excerpt"), f"policies[{index}].text_excerpt", 4000, True
        )
        policies.append(
            {
                "kind": kind,
                "title": text_value(
                    item.get("title"), f"policies[{index}].title", 300, True
                ),
                "url": url,
                "text_excerpt": excerpt,
                "retrieved_at": retrieved_at,
                "requires_summary": len(excerpt) > 1200,
                "status": "public_source_unverified_applicability",
            }
        )
        add_source(url)

    for index, item in enumerate(list_value(raw, "sources", MAX_SOURCES)):
        if not isinstance(item, dict):
            raise ValueError(f"sources[{index}] must be an object")
        kind = text_value(item.get("type", "page"), f"sources[{index}].type", 40, True)
        if kind not in ALLOWED_SOURCE_TYPES:
            raise ValueError(f"Unsupported source type: {kind}")
        url = public_browser_url(item.get("url"), f"sources[{index}].url", approved_host)
        add_source(url, kind)

    if len(sources) > MAX_SOURCES:
        raise ValueError(f"Combined sources exceed the {MAX_SOURCES}-item limit")
    warnings = [
        text_value(item, "warnings", 500, True)
        for item in list_value(raw, "warnings", 50)
    ]
    warnings.append("Direct storefront discovery failed; guarded browser fallback was used.")

    return {
        "schema_version": 1,
        "storefront_url": storefront_url,
        "canonical_origin": origin,
        "retrieved_at": retrieved_at,
        "public_sources_only": True,
        "read_only": True,
        "discovery_method": "browser_fallback",
        "fallback_reason": text_value(
            raw.get("fallback_reason", "direct_fetch_failed"), "fallback_reason", 300, True
        ),
        "browser_tool": text_value(raw.get("browser_tool"), "browser_tool", 120, True),
        "platform": {
            "name": platform_name or "unknown",
            "confidence": confidence,
            "evidence": platform_evidence,
        },
        "robots": {"url": robots_url, "status": robots_status, "respected": True},
        "products": products,
        "campaigns": campaigns,
        "policies": policies,
        "sources": sources,
        "warnings": warnings,
        "limitations": [
            "Only visible public storefront pages were read with a guarded browser/browse tool; no forms or write actions were used.",
            "No customer, order, payment, inventory, admin, browser-session, or unpublished data was accessed.",
            "Public prices, stock labels, promotions, and policy text must be checked for region, customer, product, version, and effective-date applicability before use.",
            "Complete orders still require a separately authorized commerce connector.",
        ],
    }


def load_input(path: str) -> dict[str, Any]:
    if path == "-":
        raw = json.load(sys.stdin)
    else:
        raw = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Browser discovery input must be a JSON object")
    return raw


def private_runtime_output(path: Path) -> Path:
    runtime_root = runtime_dir().resolve()
    output = path.expanduser().resolve()
    try:
        output.relative_to(runtime_root)
    except ValueError as exc:
        raise ValueError(
            "Browser discovery output must remain inside the private runtime directory"
        ) from exc
    return output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and import a guarded browser storefront discovery snapshot"
    )
    parser.add_argument("--input", required=True, help="JSON file path, or - for stdin")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--confirm-owner-request",
        action="store_true",
        help="Required because import writes a discovery snapshot and runtime configuration",
    )
    args = parser.parse_args()
    try:
        if not args.confirm_owner_request:
            raise ValueError(
                "Import changes operator-owned runtime state; confirm the current owner's request and rerun with --confirm-owner-request"
            )
        raw = load_input(args.input)
        config = runtime_config()
        storefront = config.get("storefront", {})
        payload = normalize_snapshot(raw)
        configured_url = storefront.get("url")
        if configured_url and normalized_host(
            urllib.parse.urlsplit(configured_url).hostname or ""
        ) != normalized_host(urllib.parse.urlsplit(payload["storefront_url"]).hostname or ""):
            raise ValueError("Browser snapshot host does not match the configured storefront")
        output = private_runtime_output(
            args.output
            or Path(storefront.get("discovery_file") or runtime_dir() / "store-discovery.json")
        )
        atomic_json(output, payload)
        update_runtime_config(
            payload["storefront_url"],
            output,
            payload["retrieved_at"],
            preserve_confirmation=False,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Browser discovery import failed safely: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "output": str(output),
                "discovery_method": payload["discovery_method"],
                "platform": payload["platform"]["name"],
                "products": len(payload["products"]),
                "campaigns": len(payload["campaigns"]),
                "policies": len(payload["policies"]),
                "warnings": len(payload["warnings"]),
                "public_sources_only": True,
                "read_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
