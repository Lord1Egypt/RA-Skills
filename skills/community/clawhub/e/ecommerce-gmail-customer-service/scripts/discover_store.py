#!/usr/bin/env python3
"""Discover public storefront products, promotions, and policy sources safely."""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

USER_AGENT = "EcomAgentToolsStoreDiscovery/1.0 (+https://ecomagenttools.com)"
MAX_BYTES = 1_000_000
POLICY_TERMS = {
    "refund": ("refund", "money back"),
    "return": ("return", "returns"),
    "exchange": ("exchange", "exchanges"),
    "shipping": ("shipping", "delivery"),
    "cancellation": ("cancel", "cancellation"),
    "warranty": ("warranty", "guarantee"),
    "privacy": ("privacy", "data protection"),
    "terms": ("terms", "conditions"),
}
CAMPAIGN_TERMS = (
    "sale",
    "discount",
    "promotion",
    "promo",
    "offer",
    "free shipping",
    "buy one",
    "black friday",
    "cyber monday",
    "% off",
    "save ",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def runtime_dir() -> Path:
    state_override = os.environ.get("OPENCLAW_STATE_DIR")
    state_root = (
        Path(state_override).expanduser()
        if state_override
        else Path.home() / ".openclaw"
    )
    return state_root / "ecommerce-gmail-customer-service"


def runtime_config() -> dict[str, Any]:
    path = runtime_dir() / "config.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to read runtime config: {exc}") from exc


def owner_confirmed_storefront_url(storefront: Any) -> str | None:
    if not isinstance(storefront, dict):
        return None
    url = storefront.get("url")
    confirmed_at = storefront.get("owner_confirmed_at")
    if (
        storefront.get("status") == "confirmed"
        and isinstance(url, str)
        and url
        and isinstance(confirmed_at, str)
        and confirmed_at
    ):
        return url
    return None


def resolve_discovery_url(
    requested_url: str | None,
    storefront: Any,
    owner_confirmed_request: bool,
) -> str:
    """Allow unattended refreshes only for the exact owner-confirmed URL."""
    configured_url = storefront.get("url") if isinstance(storefront, dict) else ""
    confirmed_url = owner_confirmed_storefront_url(storefront)
    if requested_url:
        if requested_url == confirmed_url:
            return requested_url
        if not owner_confirmed_request:
            raise ValueError(
                "First-time storefront discovery or a changed storefront URL changes operator-owned runtime state. Confirm the current owner's request and rerun with --confirm-owner-request"
            )
        return requested_url
    if confirmed_url:
        return confirmed_url
    if configured_url:
        raise ValueError(
            "Automatic storefront refresh requires a previously owner-confirmed storefront. Review the existing discovery result and run scripts/configure.py storefront confirmed --confirm-owner-request, or supply a new merchant URL with --confirm-owner-request"
        )
    raise ValueError(
        "Store discovery requires --url and --confirm-owner-request during first-time setup"
    )


def normalized_host(host: str) -> str:
    value = host.rstrip(".").lower()
    return value.removeprefix("www.")


def validate_public_url(url: str, storefront_host: str | None = None) -> str:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https storefront URLs are allowed")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(
            "The storefront URL must contain a hostname and no credentials"
        )
    host = parsed.hostname.rstrip(".").lower()
    if storefront_host and normalized_host(host) != normalized_host(storefront_host):
        raise ValueError(f"Cross-host URL is not allowed: {host}")
    try:
        default_port = 443 if parsed.scheme == "https" else 80
        addresses = {
            item[4][0]
            for item in socket.getaddrinfo(
                host, parsed.port or default_port, type=socket.SOCK_STREAM
            )
        }
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve storefront hostname: {host}") from exc
    if not addresses:
        raise ValueError(f"Unable to resolve storefront hostname: {host}")
    for address in addresses:
        ip = ipaddress.ip_address(address.split("%")[0])
        if not ip.is_global:
            raise ValueError(
                f"Storefront URL resolves to a non-public address: {address}"
            )
    clean_path = parsed.path or "/"
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, clean_path, parsed.query, "")
    )


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, storefront_host: str):
        self.storefront_host = storefront_host

    def redirect_request(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> Any:
        safe_url = validate_public_url(
            urllib.parse.urljoin(req.full_url, newurl), self.storefront_host
        )
        return super().redirect_request(req, fp, code, msg, headers, safe_url)


def fetch_public(
    url: str, storefront_host: str, timeout: float, max_bytes: int = MAX_BYTES
) -> tuple[str, bytes, str]:
    safe_url = validate_public_url(url, storefront_host)
    opener = urllib.request.build_opener(SafeRedirectHandler(storefront_host))
    request = urllib.request.Request(
        safe_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xml,application/json;q=0.9,*/*;q=0.1",
        },
    )
    with opener.open(request, timeout=timeout) as response:
        final_url = validate_public_url(response.geturl(), storefront_host)
        content_type = response.headers.get_content_type()
        body = response.read(max_bytes + 1)
    if len(body) > max_bytes:
        raise ValueError(f"Response exceeded the {max_bytes}-byte safety limit")
    return final_url, body, content_type


class StoreHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta: dict[str, str] = {}
        self.links: list[tuple[str, str]] = []
        self.text_parts: list[str] = []
        self.jsonld_parts: list[str] = []
        self._jsonld_buffer: list[str] = []
        self._title = False
        self._skip_depth = 0
        self._jsonld = False
        self._link_href: str | None = None
        self._link_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        if tag == "title":
            self._title = True
        if tag in {"style", "noscript"}:
            self._skip_depth += 1
        if tag == "script":
            if "ld+json" in values.get("type", "").lower():
                self._jsonld = True
                self._jsonld_buffer = []
            else:
                self._skip_depth += 1
        if tag == "meta":
            key = values.get("property") or values.get("name")
            if key and values.get("content"):
                self.meta[key.lower()] = values["content"].strip()
        if tag == "a" and values.get("href"):
            self._link_href = values["href"]
            self._link_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._title = False
        if tag in {"style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "script":
            if self._jsonld:
                self.jsonld_parts.append("".join(self._jsonld_buffer))
                self._jsonld = False
                self._jsonld_buffer = []
            elif self._skip_depth:
                self._skip_depth -= 1
        if tag == "a" and self._link_href:
            self.links.append((self._link_href, " ".join(self._link_text).strip()))
            self._link_href = None
            self._link_text = []

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if not value:
            return
        if self._jsonld:
            self._jsonld_buffer.append(data)
            return
        if self._skip_depth:
            return
        if self._title:
            self.title = f"{self.title} {value}".strip()
        if self._link_href is not None:
            self._link_text.append(value)
        self.text_parts.append(value)


def iter_json_objects(value: Any):
    if isinstance(value, list):
        for item in value:
            yield from iter_json_objects(item)
    elif isinstance(value, dict):
        yield value
        if "@graph" in value:
            yield from iter_json_objects(value["@graph"])


def type_names(value: Any) -> set[str]:
    raw = value.get("@type", []) if isinstance(value, dict) else []
    return {str(item).lower() for item in (raw if isinstance(raw, list) else [raw])}


def first_offer(offers: Any) -> dict[str, Any]:
    if isinstance(offers, list):
        return offers[0] if offers and isinstance(offers[0], dict) else {}
    return offers if isinstance(offers, dict) else {}


def classify_policy(text: str) -> str | None:
    lowered = text.lower()
    for kind, terms in POLICY_TERMS.items():
        if any(term in lowered for term in terms):
            return kind
    return None


def same_store_link(raw_url: str, base_url: str, storefront_host: str) -> str | None:
    joined = urllib.parse.urljoin(base_url, raw_url)
    parsed = urllib.parse.urlsplit(joined)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return None
    if normalized_host(parsed.hostname) != normalized_host(storefront_host):
        return None
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path or "/", parsed.query, "")
    )


def analyze_html(
    html: str, page_url: str, storefront_host: str | None = None
) -> dict[str, Any]:
    host = storefront_host or (urllib.parse.urlsplit(page_url).hostname or "")
    parser = StoreHTMLParser()
    parser.feed(html)
    visible_text = " ".join(parser.text_parts)
    json_objects: list[dict[str, Any]] = []
    for raw in parser.jsonld_parts:
        try:
            json_objects.extend(iter_json_objects(json.loads(raw)))
        except json.JSONDecodeError:
            continue

    products = []
    for item in json_objects:
        if "product" not in type_names(item):
            continue
        offer = first_offer(item.get("offers"))
        products.append(
            {
                "name": str(item.get("name", "")).strip(),
                "sku": str(item.get("sku", "")).strip(),
                "url": same_store_link(str(item.get("url", "")), page_url, host)
                or page_url,
                "price": str(offer.get("price", offer.get("lowPrice", ""))).strip(),
                "currency": str(offer.get("priceCurrency", "")).strip(),
                "availability": str(offer.get("availability", "")).rsplit("/", 1)[-1],
                "source_url": page_url,
            }
        )

    policy_links: list[dict[str, str]] = []
    product_links: list[str] = []
    campaign_links: list[str] = []
    for href, anchor in parser.links:
        link = same_store_link(href, page_url, host)
        if not link:
            continue
        path_text = f"{urllib.parse.urlsplit(link).path} {anchor}".lower()
        policy_kind = classify_policy(path_text)
        if policy_kind:
            policy_links.append({"kind": policy_kind, "url": link, "anchor": anchor})
        if re.search(
            r"/(products?|collections?)/|/p/", urllib.parse.urlsplit(link).path.lower()
        ):
            product_links.append(link)
        if any(term in path_text for term in CAMPAIGN_TERMS):
            campaign_links.append(link)

    campaign_evidence = []
    for sentence in re.split(r"(?<=[.!?])\s+|\s{2,}", visible_text):
        if any(term in sentence.lower() for term in CAMPAIGN_TERMS):
            campaign_evidence.append(sentence[:240])
        if len(campaign_evidence) >= 8:
            break

    source_lower = html.lower()
    platform_evidence: list[str] = []
    platform = "unknown"
    if "shopify" in source_lower or "cdn.shopify.com" in source_lower:
        platform, platform_evidence = "shopify", ["Shopify marker found in public HTML"]
    elif (
        "woocommerce" in source_lower
        or "wp-content/plugins/woocommerce" in source_lower
    ):
        platform, platform_evidence = (
            "woocommerce",
            ["WooCommerce marker found in public HTML"],
        )
    elif "bigcommerce" in source_lower:
        platform, platform_evidence = (
            "bigcommerce",
            ["BigCommerce marker found in public HTML"],
        )
    elif "wixstatic.com" in source_lower or parser.meta.get(
        "generator", ""
    ).lower().startswith("wix"):
        platform, platform_evidence = "wix", ["Wix marker found in public HTML"]

    return {
        "title": parser.title,
        "text": visible_text,
        "products": products,
        "policy_links": policy_links,
        "product_links": list(dict.fromkeys(product_links)),
        "campaign_links": list(dict.fromkeys(campaign_links)),
        "campaign_evidence": list(dict.fromkeys(campaign_evidence)),
        "platform": {
            "name": platform,
            "confidence": 0.9 if platform != "unknown" else 0.0,
            "evidence": platform_evidence,
        },
    }


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def update_runtime_config(
    storefront_url: str,
    output: Path,
    discovered_at: str,
    preserve_confirmation: bool = True,
) -> None:
    config_path = runtime_dir() / "config.json"
    if not config_path.exists():
        return
    config = json.loads(config_path.read_text(encoding="utf-8"))
    storefront = config.setdefault("storefront", {})
    confirmed_url = owner_confirmed_storefront_url(storefront)
    keep_confirmed = preserve_confirmation and confirmed_url == storefront_url
    status = "confirmed" if keep_confirmed else "discovered"
    storefront.update(
        {
            "status": status,
            "owner_confirmed_at": (
                storefront.get("owner_confirmed_at") if keep_confirmed else None
            ),
            "url": storefront_url,
            "discovery_file": str(output),
            "last_discovered_at": discovered_at,
        }
    )
    atomic_json(config_path, config)


def discover(args: argparse.Namespace) -> dict[str, Any]:
    initial = validate_public_url(args.url)
    parsed = urllib.parse.urlsplit(initial)
    host = parsed.hostname or ""
    origin = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
    warnings: list[str] = []
    sources: list[dict[str, str]] = []
    robots_url = f"{origin}/robots.txt"
    robots = urllib.robotparser.RobotFileParser()
    robots.set_url(robots_url)
    sitemap_urls: list[str] = []
    robots_status = "unavailable"
    try:
        _, robots_body, _ = fetch_public(robots_url, host, args.timeout, args.max_bytes)
        robots_text = robots_body.decode("utf-8", errors="replace")
        robots.parse(robots_text.splitlines())
        sitemap_urls = [
            line.split(":", 1)[1].strip()
            for line in robots_text.splitlines()
            if line.lower().startswith("sitemap:")
        ]
        robots_status = "loaded"
        sources.append({"url": robots_url, "type": "robots", "retrieved_at": utc_now()})
    except (OSError, ValueError, urllib.error.URLError) as exc:
        robots.parse([])
        warnings.append(f"robots.txt was unavailable: {exc}")

    queued = [initial]
    if not sitemap_urls:
        sitemap_urls = [f"{origin}/sitemap.xml"]
    sitemap_queue = list(dict.fromkeys(sitemap_urls[:3]))
    seen_sitemaps: set[str] = set()
    while sitemap_queue and len(seen_sitemaps) < 10:
        sitemap_url = sitemap_queue.pop(0)
        link = same_store_link(sitemap_url, initial, host)
        if not link or link in seen_sitemaps:
            continue
        seen_sitemaps.add(link)
        try:
            if robots_status == "loaded" and not robots.can_fetch(USER_AGENT, link):
                continue
            final_url, body, _ = fetch_public(link, host, args.timeout, args.max_bytes)
            if b"<!DOCTYPE" in body.upper() or b"<!ENTITY" in body.upper():
                raise ValueError(
                    "DTD or entity declarations are not allowed in sitemap XML"
                )
            root = ET.fromstring(body)
            for element in root.iter():
                if element.tag.rsplit("}", 1)[-1].lower() == "loc" and element.text:
                    candidate = same_store_link(element.text.strip(), initial, host)
                    if not candidate:
                        continue
                    candidate_path = urllib.parse.urlsplit(candidate).path.lower()
                    if candidate_path.endswith(".xml") or "sitemap" in candidate_path:
                        if (
                            candidate not in seen_sitemaps
                            and candidate not in sitemap_queue
                        ):
                            sitemap_queue.append(candidate)
                    elif classify_policy(candidate_path) or re.search(
                        r"/(products?|collections?)/|/p/", candidate_path
                    ):
                        queued.append(candidate)
            sources.append(
                {"url": final_url, "type": "sitemap", "retrieved_at": utc_now()}
            )
        except (ET.ParseError, OSError, ValueError, urllib.error.URLError) as exc:
            warnings.append(f"Sitemap could not be used: {link}: {exc}")

    products: list[dict[str, Any]] = []
    policies: list[dict[str, Any]] = []
    campaigns: list[dict[str, Any]] = []
    platform = {"name": "unknown", "confidence": 0.0, "evidence": []}
    seen: set[str] = set()
    while queued and len(seen) < args.max_pages:
        page_url = queued.pop(0)
        if page_url in seen:
            continue
        seen.add(page_url)
        if robots_status == "loaded" and not robots.can_fetch(USER_AGENT, page_url):
            warnings.append(f"Skipped by robots.txt: {page_url}")
            continue
        try:
            final_url, body, content_type = fetch_public(
                page_url, host, args.timeout, args.max_bytes
            )
        except (OSError, ValueError, urllib.error.URLError) as exc:
            warnings.append(f"Page could not be fetched: {page_url}: {exc}")
            continue
        if content_type not in {"text/html", "application/xhtml+xml"}:
            continue
        html = body.decode("utf-8", errors="replace")
        page = analyze_html(html, final_url, host)
        sources.append({"url": final_url, "type": "page", "retrieved_at": utc_now()})
        if platform["name"] == "unknown" and page["platform"]["name"] != "unknown":
            platform = page["platform"]
        products.extend(page["products"])
        policy_kind = classify_policy(
            urllib.parse.urlsplit(final_url).path + " " + page["title"]
        )
        if policy_kind:
            policies.append(
                {
                    "kind": policy_kind,
                    "title": page["title"],
                    "url": final_url,
                    "text_excerpt": page["text"][:4000],
                    "retrieved_at": utc_now(),
                    "requires_summary": len(page["text"]) > 1200,
                    "status": "public_source_unverified_applicability",
                }
            )
        for evidence in page["campaign_evidence"]:
            campaigns.append(
                {
                    "evidence": evidence,
                    "url": final_url,
                    "retrieved_at": utc_now(),
                    "status": "public_claim_unverified_applicability",
                }
            )
        candidates = (
            page["product_links"][:12]
            + [item["url"] for item in page["policy_links"]][:16]
            + page["campaign_links"][:8]
        )
        for candidate in candidates:
            if candidate not in seen and candidate not in queued:
                queued.append(candidate)
        if args.delay and queued:
            time.sleep(args.delay)

    def unique_by(
        items: list[dict[str, Any]], keys: tuple[str, ...]
    ) -> list[dict[str, Any]]:
        result, observed = [], set()
        for item in items:
            key = tuple(str(item.get(field, "")) for field in keys)
            if key in observed:
                continue
            observed.add(key)
            result.append(item)
        return result

    discovered_at = utc_now()
    return {
        "schema_version": 1,
        "storefront_url": initial,
        "canonical_origin": origin,
        "retrieved_at": discovered_at,
        "public_sources_only": True,
        "platform": platform,
        "robots": {"url": robots_url, "status": robots_status, "respected": True},
        "products": unique_by(products, ("url", "sku", "name")),
        "campaigns": unique_by(campaigns, ("url", "evidence")),
        "policies": unique_by(policies, ("url", "kind")),
        "sources": unique_by(sources, ("url", "type")),
        "warnings": warnings,
        "limitations": [
            "Only public storefront pages were read; no customer, order, payment, inventory, admin, or unpublished data was accessed.",
            "Public prices, stock labels, promotions, and policy text must be checked for region, customer, product, version, and effective-date applicability before use.",
            "Complete orders still require a separately authorized commerce connector.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover public storefront products, promotions, and policy sources"
    )
    parser.add_argument(
        "--url",
        help="Public storefront URL supplied by the merchant; omit on refresh to reuse config.json",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--max-bytes", type=int)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--delay", type=float)
    parser.add_argument(
        "--confirm-owner-request",
        action="store_true",
        help="Required for first-time discovery or a changed storefront URL",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        config = runtime_config()
    except ValueError as exc:
        print(f"Store discovery failed safely: {exc}", file=sys.stderr)
        return 1
    storefront = config.get("storefront", {})
    try:
        args.url = resolve_discovery_url(
            args.url, storefront, args.confirm_owner_request
        )
    except ValueError as exc:
        print(f"Store discovery failed safely: {exc}", file=sys.stderr)
        return 2
    if storefront.get("discovery_enabled") is False:
        print("Store discovery is disabled in config.json", file=sys.stderr)
        return 2
    try:
        args.output = args.output or Path(
            storefront.get("discovery_file") or runtime_dir() / "store-discovery.json"
        )
        args.max_pages = (
            args.max_pages
            if args.max_pages is not None
            else int(storefront.get("max_pages", 30))
        )
        args.max_bytes = (
            args.max_bytes
            if args.max_bytes is not None
            else int(storefront.get("max_bytes_per_page", MAX_BYTES))
        )
        args.delay = (
            args.delay
            if args.delay is not None
            else float(storefront.get("request_delay_seconds", 0.25))
        )
    except (TypeError, ValueError) as exc:
        print(f"Store discovery configuration is invalid: {exc}", file=sys.stderr)
        return 2
    if not 1 <= args.max_pages <= 100:
        raise SystemExit("--max-pages must be between 1 and 100")
    if not 100_000 <= args.max_bytes <= 5_000_000:
        raise SystemExit("--max-bytes must be between 100000 and 5000000")
    if not 0 <= args.delay <= 5:
        raise SystemExit("--delay must be between 0 and 5 seconds")
    if not 1 <= args.timeout <= 60:
        raise SystemExit("--timeout must be between 1 and 60 seconds")
    try:
        payload = discover(args)
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(f"Store discovery failed safely: {exc}", file=sys.stderr)
        return 1
    output = args.output.expanduser().resolve()
    atomic_json(output, payload)
    update_runtime_config(payload["storefront_url"], output, payload["retrieved_at"])
    print(
        json.dumps(
            {
                "output": str(output),
                "platform": payload["platform"]["name"],
                "products": len(payload["products"]),
                "campaigns": len(payload["campaigns"]),
                "policies": len(payload["policies"]),
                "warnings": len(payload["warnings"]),
                "public_sources_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
