#!/usr/bin/env python3
"""EVE ESI API query helper.

Usage (generic endpoint mode):
    python esi_query.py --char main --endpoint /characters/12345/wallet/
    python esi_query.py --char main --endpoint /characters/12345/assets/ --pages

Usage (high-level PI/market actions):
    python esi_query.py --action pi_planets --char main --pretty
    python esi_query.py --action pi_planet_detail --char main --planet-id 98765 --pretty
    python esi_query.py --action pi_status --char main --pretty
    python esi_query.py --action market_price_bulk --pretty
    python esi_query.py --action jita_price --type-id 2393 --pretty

Authentication:
    --char <name>   refreshes the stored token in-process (recommended; the token
                    never appears in argv, so `ps` and shell history cannot leak it)
    --token-stdin   reads the token from the first line of stdin
    --token <TOK>   accepted for compatibility, but exposes the token via argv

Scope:
    This skill is read-only by default. GET and the documented bulk-lookup POST
    endpoints (/universe/names/, /characters/affiliation/, asset name/location
    resolution) run normally. Any other POST, plus PUT and DELETE, may change
    account state and is refused unless --allow-write is passed explicitly.

Requires: Python 3.8+ (uses only stdlib)
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

from user_agent import USER_AGENT

# ESI has replaced versioned URL prefixes (/latest, /v5, ...) with a
# compatibility date. The base URL carries no version any more; instead every
# request declares which day's API behaviour it was written against.
BASE_URL = "https://esi.evetech.net"

# A request that sends no compatibility date gets the *oldest* date ESI still
# serves — currently 2020-01-01 — and CCP raises that floor over time. Pinning
# it is what keeps this skill on a known contract instead of a moving one.
#
# To bump: check https://esi.evetech.net/meta/changelog for entries newer than
# this date, adjust the code for any `is_breaking` change on an endpoint used
# here, then set the new date. Valid values are listed at
# https://esi.evetech.net/meta/compatibility-dates — the date may not be in the
# future (ESI rolls over at 11:00 UTC).
DEFAULT_COMPATIBILITY_DATE = "2026-08-04"
COMPATIBILITY_DATE = os.environ.get(
    "EVE_ESI_COMPATIBILITY_DATE", DEFAULT_COMPATIBILITY_DATE
)

# POST endpoints that are read-only bulk lookups: they resolve IDs to data and
# change no account state. Everything else non-GET is treated as state-changing
# and requires an explicit --allow-write opt-in.
READ_ONLY_POST_PATTERNS = (
    re.compile(r"^/universe/names/?$"),
    re.compile(r"^/universe/ids/?$"),
    re.compile(r"^/characters/affiliation/?$"),
    re.compile(r"^/characters/\d+/assets/names/?$"),
    re.compile(r"^/characters/\d+/assets/locations/?$"),
    re.compile(r"^/corporations/\d+/assets/names/?$"),
    re.compile(r"^/corporations/\d+/assets/locations/?$"),
    # Route planning became a POST when it moved to a request body. It reads
    # the star map and touches nothing on the account.
    re.compile(r"^/route/\d+/\d+/?$"),
)


class ESIError(Exception):
    """Base exception for ESI API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class ESIRateLimitError(ESIError):
    """Raised when ESI rate limit retries are exhausted."""


class ESINetworkError(ESIError):
    """Raised on network-level failures (DNS, timeout, connection refused)."""


JITA_REGION_ID = 10000002

# Base PI product mapping (P0 + P1 complete, selected P2-P4 common outputs).
PI_PRODUCTS: dict[int, str] = {
    # P0 (core set)
    2393: "Aqueous Liquids",
    2396: "Base Metals",
    2397: "Carbon Compounds",
    2398: "Complex Organisms",
    2401: "Heavy Metals",
    # P1 (core set)
    2389: "Bacteria",
    2390: "Biofuels",
    2399: "Industrial Fibers",
    3779: "Biomass",
    2400: "Precious Metals",
    2317: "Water",
    9828: "Silicon",
    # P2/P3/P4 (selected)
    44: "Enriched Uranium",
    3689: "Mechanical Parts",
    9836: "Consumer Electronics",
    9832: "Construction Blocks",
    3683: "Coolant",
    2867: "Broadcast Node",
    2868: "Camera Drones",
    2869: "Synthetic Synapses",
    2870: "Gel-Matrix Biopaste",
    2871: "Hazmat Detection Systems",
    2872: "Integrity Response Drones",
    2873: "Organic Mortar Applicators",
    2874: "Nano-Factory",
    2875: "Sterile Conduits",
}

# Pin capacities and item volumes are read from ESI, not tabulated here: PI
# buildings exist as a separate type per planet type (Ice Launchpad, Barren
# Launchpad, ...), so any hand-maintained list silently covers only the planets
# its author happened to own. See get_type_info().


# Version prefixes ESI still accepts but has deprecated in favour of the
# compatibility date. Stripping them puts callers that copied an older example
# back on the current contract — and keeps READ_ONLY_POST_PATTERNS matching,
# which otherwise misreads a prefixed bulk lookup as a state-changing write.
VERSION_PREFIX = re.compile(r"^/(?:latest|legacy|dev|v\d+)(?=/)")


def normalize_endpoint(endpoint: str) -> str:
    """Ensure endpoint starts with a leading slash and carries no version prefix."""
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    return VERSION_PREFIX.sub("", endpoint)


def is_read_only_post(endpoint: str) -> bool:
    """True if a POST to this endpoint is a documented bulk lookup, not a write."""
    path = normalize_endpoint(endpoint).split("?", 1)[0]
    return any(pattern.match(path) for pattern in READ_ONLY_POST_PATTERNS)


def is_state_changing(method: str, endpoint: str) -> bool:
    """True if this request may alter account state and needs --allow-write."""
    if method == "GET":
        return False
    if method == "POST" and is_read_only_post(endpoint):
        return False
    return True


def resolve_token(args: argparse.Namespace, parser: argparse.ArgumentParser) -> str | None:
    """Resolve the access token from --char, --token-stdin, or --token.

    --char is preferred: the token is refreshed in-process and never appears in
    argv, so it cannot leak via `ps` or shell history.
    """
    provided = [
        name for name, value in (
            ("--char", args.char),
            ("--token-stdin", args.token_stdin),
            ("--token", args.token),
        ) if value
    ]
    if len(provided) > 1:
        parser.error(f"Use only one of {', '.join(provided)}")

    if args.char:
        try:
            from get_token import resolve_access_token
        except ImportError as exc:
            parser.error(f"--char requires get_token.py alongside this script: {exc}")
        try:
            return resolve_access_token(args.char)["access_token"]
        except Exception as exc:
            parser.error(f"Could not resolve token for character '{args.char}': {exc}")

    if args.token_stdin:
        token = sys.stdin.readline().strip()
        if not token:
            parser.error("--token-stdin was given but stdin provided no token")
        return token

    if args.token:
        print(
            "Warning: --token puts the access token in argv, where `ps` and shell "
            "history can expose it. Prefer --char <name> or --token-stdin.",
            file=sys.stderr,
        )
    return args.token


def parse_utc_timestamp(value: str | None) -> datetime | None:
    """Parse an ESI timestamp in RFC3339 format."""
    if not value:
        return None
    try:
        fixed = value.replace("Z", "+00:00")
        return datetime.fromisoformat(fixed).astimezone(timezone.utc)
    except ValueError:
        print(f"Warning: could not parse timestamp: {value!r}", file=sys.stderr)
        return None


# Names looked up from ESI during this run, for type IDs PI_PRODUCTS misses.
# PI_PRODUCTS only ever covered part of the tree, so the API is the real source.
_resolved_type_names: dict[int, str] = {}


def cache_type_names(type_ids: list[int]) -> None:
    """Resolve type IDs to names in one call and remember them for this run.

    /universe/names/ rejects the whole batch if a single ID is unresolvable, so
    only IDs that are plausibly types are worth sending, and a failure here must
    stay non-fatal — callers fall back to the `type_id:N` label.
    """
    unknown = sorted(
        {t for t in type_ids if isinstance(t, int) and t not in PI_PRODUCTS
         and t not in _resolved_type_names}
    )
    if not unknown:
        return
    try:
        for item in get_universe_names(unknown):
            if isinstance(item, dict) and item.get("category") == "inventory_type":
                _resolved_type_names[item["id"]] = item["name"]
    except ESIError as exc:
        print(f"Warning: could not resolve product names: {exc}", file=sys.stderr)


def resolve_pi_product_name(type_id: int | None) -> str:
    """Map PI type_id to readable product name."""
    if type_id is None:
        return "unknown"
    if type_id in PI_PRODUCTS:
        return PI_PRODUCTS[type_id]
    return _resolved_type_names.get(type_id, f"type_id:{type_id}")


def build_url(endpoint: str, page: int | None = None, params: dict[str, Any] | None = None) -> str:
    """Build endpoint URL with optional query params and pagination."""
    url = f"{BASE_URL}{normalize_endpoint(endpoint)}"
    query: dict[str, Any] = {}
    if params:
        query.update(params)
    if page is not None:
        query["page"] = page
    if query:
        sep = "&" if "?" in url else "?"
        url += sep + urllib.parse.urlencode(query, doseq=True)
    return url


def warn_if_rate_limit_low(resp_headers: dict) -> None:
    """Warn once a route's rate limit bucket is running low.

    ESI asks clients to slow down as X-Ratelimit-Remaining approaches zero
    rather than to keep going until the 429. Only routes with bucket limiting
    send these headers, so their absence is not an error.
    """
    remaining = resp_headers.get("x-ratelimit-remaining", "")
    limit = resp_headers.get("x-ratelimit-limit", "")
    total = limit.split("/")[0]
    if not remaining.isdigit() or not total.isdigit() or int(total) <= 0:
        return
    if int(remaining) <= int(total) * 0.2:
        group = resp_headers.get("x-ratelimit-group", "?")
        print(
            f"Warning: rate limit bucket '{group}' down to {remaining}/{limit} — "
            f"spread requests out.",
            file=sys.stderr,
        )


def esi_request(
    endpoint: str,
    token: str | None = None,
    method: str = "GET",
    body: str | None = None,
    page: int | None = None,
    params: dict[str, Any] | None = None,
    allow_404: bool = False,
    _retry_count: int = 0,
) -> tuple[dict | list | str | None, dict]:
    """Make a single ESI request. Returns (parsed_body, headers)."""
    url = build_url(endpoint, page=page, params=params)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "X-Compatibility-Date": COMPATIBILITY_DATE,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = body.encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_headers = {k.lower(): v for k, v in resp.getheaders()}
            raw = resp.read().decode("utf-8")
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = raw
            warn_if_rate_limit_low(resp_headers)
            return parsed, resp_headers
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        remain = e.headers.get("X-ESI-Error-Limit-Remain", "?")
        reset = e.headers.get("X-ESI-Error-Limit-Reset", "?")
        print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        if e.code == 429:
            group = e.headers.get("X-Ratelimit-Group", "?")
            limit = e.headers.get("X-Ratelimit-Limit", "?")
            print(f"Rate limit bucket '{group}' exhausted (limit {limit})", file=sys.stderr)
        else:
            print(f"Error limit remaining: {remain}, resets in: {reset}s", file=sys.stderr)
        # 420 is the older account-wide error rate limit, 429 the per-route
        # bucket limit. ESI treats them as mutually exclusive and puts the
        # delay in a different header for each.
        if e.code in (420, 429):
            if _retry_count >= 3:
                raise ESIRateLimitError(
                    f"Rate limit retry count exceeded (max 3) on HTTP {e.code}. "
                    f"Remaining: {remain}, reset: {reset}s",
                    status_code=e.code,
                )
            if e.code == 429:
                retry_after = e.headers.get("Retry-After", "")
                wait = int(retry_after) if retry_after.isdigit() else 60
            else:
                wait = int(reset) if reset.isdigit() else 60
            print(f"Rate limited (HTTP {e.code}). Waiting {wait}s...", file=sys.stderr)
            time.sleep(wait)
            return esi_request(
                endpoint=endpoint,
                token=token,
                method=method,
                body=body,
                page=page,
                params=params,
                allow_404=allow_404,
                _retry_count=_retry_count + 1,
            )
        if allow_404 and e.code == 404:
            return None, {k.lower(): v for k, v in e.headers.items()}
        raise ESIError(f"HTTP {e.code}: {error_body}", status_code=e.code)
    except urllib.error.URLError as e:
        raise ESINetworkError(f"Network error: {e.reason}")


def esi_request_all_pages(
    endpoint: str,
    token: str | None = None,
    params: dict[str, Any] | None = None,
) -> list:
    """Fetch all pages of a paginated GET endpoint."""
    first_page, headers = esi_request(endpoint, token=token, page=1, params=params)
    total_pages = int(headers.get("x-pages", "1"))
    if not isinstance(first_page, list):
        if first_page is None:
            return []
        return [first_page]

    all_results = list(first_page)
    for p in range(2, total_pages + 1):
        page_data, _ = esi_request(endpoint, token=token, page=p, params=params)
        if isinstance(page_data, list):
            all_results.extend(page_data)
            page_count = len(page_data)
        elif page_data is None:
            page_count = 0
        else:
            all_results.append(page_data)
            page_count = 1
        print(f"  Page {p}/{total_pages} fetched ({page_count} items)", file=sys.stderr)
    return all_results


def get_pi_planets(character_id: int, token: str) -> list:
    """Return all PI planets for a character."""
    endpoint = f"/characters/{character_id}/planets/"
    return esi_request_all_pages(endpoint, token=token)


def get_pi_planet_detail(character_id: int, planet_id: int, token: str) -> dict:
    """Return full PI colony detail: pins, links and routes."""
    endpoint = f"/characters/{character_id}/planets/{planet_id}/"
    result, _ = esi_request(endpoint, token=token, method="GET")
    if isinstance(result, dict):
        return result
    return {}


def get_universe_planet(planet_id: int) -> dict:
    """Return public planet metadata (name/system/type)."""
    endpoint = f"/universe/planets/{planet_id}/"
    result, _ = esi_request(endpoint, token=None, allow_404=True)
    if isinstance(result, dict):
        return result
    return {}


# Static type data, cached per run so a colony with a dozen pins does not refetch
# the same launchpad description for every one of them.
_type_info_cache: dict[int, dict] = {}


def get_type_info(type_id: int | None) -> dict:
    """Public metadata for an inventory type: name, volume (m³/unit), capacity (m³).

    Failures return an empty dict rather than raising — every caller treats
    missing type data as "cannot compute" and degrades instead of aborting.
    """
    if not isinstance(type_id, int):
        return {}
    if type_id not in _type_info_cache:
        try:
            result, _ = esi_request(f"/universe/types/{type_id}/", token=None, allow_404=True)
            _type_info_cache[type_id] = result if isinstance(result, dict) else {}
        except ESIError as exc:
            print(f"Warning: could not fetch type {type_id}: {exc}", file=sys.stderr)
            _type_info_cache[type_id] = {}
    return _type_info_cache[type_id]


def get_universe_names(ids: list[int]) -> list[dict]:
    """Resolve IDs to names using /universe/names/ (POST)."""
    if not ids:
        return []
    result, _ = esi_request("/universe/names/", method="POST", body=json.dumps(ids))
    if isinstance(result, list):
        return result
    return []


def get_system_kills(system_ids: list[int] | None = None) -> list:
    """Fetch ship/pod/NPC kills per system (last hour). Optionally filter by system IDs."""
    result, _ = esi_request("/universe/system_kills/", token=None)
    if not isinstance(result, list):
        return []
    if system_ids:
        id_set = set(system_ids)
        return [s for s in result if isinstance(s, dict) and s.get("system_id") in id_set]
    return result


def get_system_jumps(system_ids: list[int] | None = None) -> list:
    """Fetch jump traffic per system (last hour). Optionally filter by system IDs."""
    result, _ = esi_request("/universe/system_jumps/", token=None)
    if not isinstance(result, list):
        return []
    if system_ids:
        id_set = set(system_ids)
        return [s for s in result if isinstance(s, dict) and s.get("system_id") in id_set]
    return result


# The old GET /route/ took flag=shortest|secure|insecure; the POST that
# replaced it names the same three choices differently. The skill keeps the old
# words on its own CLI, so this maps between them.
ROUTE_PREFERENCES = {
    "shortest": "Shorter",
    "secure": "Safer",
    "insecure": "LessSecure",
}


def get_route(origin: int, destination: int, flag: str = "secure", avoid: list[int] | None = None) -> list:
    """Plan a route between two systems. flag: shortest, secure, insecure.

    As of compatibility date 2025-09-30 this is a POST with a JSON body, not a
    GET with query parameters, and it answers with {"route": [...]} instead of a
    bare array. It changes nothing on the account despite the method, which is
    why it sits in READ_ONLY_POST_PATTERNS.
    """
    endpoint = f"/route/{origin}/{destination}/"
    payload: dict[str, Any] = {"preference": ROUTE_PREFERENCES.get(flag, "Safer")}
    if avoid:
        payload["avoid_systems"] = avoid

    result, _ = esi_request(
        endpoint, method="POST", body=json.dumps(payload), allow_404=True
    )
    if isinstance(result, dict):
        route = result.get("route")
        return route if isinstance(route, list) else []
    # Pre-2025-09-30 compatibility dates still answer with a bare array.
    if isinstance(result, list):
        return result
    return []


def get_system_info(system_id: int) -> dict:
    """Fetch public system info (name, security status, constellation, star)."""
    endpoint = f"/universe/systems/{system_id}/"
    result, _ = esi_request(endpoint, token=None, allow_404=True)
    if isinstance(result, dict):
        return result
    return {}


def get_character_location(character_id: int, token: str) -> dict:
    """Fetch current location of a character (requires auth)."""
    endpoint = f"/characters/{character_id}/location/"
    result, _ = esi_request(endpoint, token=token)
    if isinstance(result, dict):
        return result
    return {}


def get_incursions() -> list:
    """Fetch active NPC incursions."""
    result, _ = esi_request("/incursions/", token=None)
    if isinstance(result, list):
        return result
    return []


def get_fw_systems() -> list:
    """Fetch faction warfare contested systems."""
    result, _ = esi_request("/fw/systems/", token=None)
    if isinstance(result, list):
        return result
    return []


def get_market_price_bulk() -> list:
    """Fetch bulk adjusted/average prices for all item types."""
    result, _ = esi_request("/markets/prices/", token=None, method="GET")
    if isinstance(result, list):
        return result
    return []


def get_jita_price(type_id: int) -> dict:
    """Fetch current Jita buy/sell snapshot for one type."""
    sell_orders = esi_request_all_pages(
        endpoint=f"/markets/{JITA_REGION_ID}/orders/",
        token=None,
        params={"type_id": type_id, "order_type": "sell"},
    )
    buy_orders = esi_request_all_pages(
        endpoint=f"/markets/{JITA_REGION_ID}/orders/",
        token=None,
        params={"type_id": type_id, "order_type": "buy"},
    )

    sell_prices = [
        o.get("price")
        for o in sell_orders
        if isinstance(o, dict) and isinstance(o.get("price"), (int, float))
    ]
    buy_prices = [
        o.get("price")
        for o in buy_orders
        if isinstance(o, dict) and isinstance(o.get("price"), (int, float))
    ]

    lowest_sell = min(sell_prices) if sell_prices else None
    highest_buy = max(buy_prices) if buy_prices else None
    spread = None
    if lowest_sell is not None and highest_buy is not None:
        spread = round(lowest_sell - highest_buy, 2)

    return {
        "type_id": type_id,
        "region_id": JITA_REGION_ID,
        "lowest_sell": lowest_sell,
        "highest_buy": highest_buy,
        "spread": spread,
        "sell_order_count": len(sell_orders),
        "buy_order_count": len(buy_orders),
    }


def estimate_storage_fill_pct(pins: list[dict]) -> float | None:
    """Highest fill percentage across the colony's storage-capable pins.

    ESI reports pin capacity in cubic metres but pin contents in units, so the
    two only compare after multiplying each item by its type's volume — a P0
    commodity is 0.005 m³ per unit, so treating units as m³ overstates the fill
    by a couple of orders of magnitude. Pins without capacity (extractors,
    factories) are skipped; None means nothing could be measured.
    """
    max_fill = None
    for pin in pins:
        if not isinstance(pin, dict):
            continue
        capacity = get_type_info(pin.get("type_id")).get("capacity")
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            continue
        contents = pin.get("contents") or []
        if not isinstance(contents, list):
            continue
        used_volume = 0.0
        for item in contents:
            if not isinstance(item, dict):
                continue
            amount = item.get("amount")
            volume = get_type_info(item.get("type_id")).get("volume")
            if isinstance(amount, (int, float)) and isinstance(volume, (int, float)):
                used_volume += float(amount) * float(volume)
        fill = min(100.0, round((used_volume / float(capacity)) * 100.0, 2))
        if max_fill is None or fill > max_fill:
            max_fill = fill
    return max_fill


def parse_pi_status(planets_data: list, planet_details: dict | list) -> list[dict]:
    """Parse raw PI ESI responses into actionable per-planet status."""
    details_map: dict[str, dict] = {}
    if isinstance(planet_details, dict):
        details_map = {str(k): v for k, v in planet_details.items() if isinstance(v, dict)}
    elif isinstance(planet_details, list):
        for item in planet_details:
            if not isinstance(item, dict):
                continue
            planet_id = item.get("planet_id")
            detail = item.get("detail") if isinstance(item.get("detail"), dict) else item
            if planet_id is not None and isinstance(detail, dict):
                details_map[str(planet_id)] = detail

    now = datetime.now(timezone.utc)
    parsed: list[dict] = []

    for planet in planets_data:
        if not isinstance(planet, dict):
            continue

        planet_id = planet.get("planet_id")
        detail = details_map.get(str(planet_id), {})
        pins = detail.get("pins", []) if isinstance(detail, dict) else []
        routes = detail.get("routes", []) if isinstance(detail, dict) else []

        extractors: list[dict] = []
        attention_reasons: list[str] = []

        for pin in pins:
            if not isinstance(pin, dict):
                continue
            extractor = pin.get("extractor_details")
            if not isinstance(extractor, dict):
                continue

            product_type_id = extractor.get("product_type_id")
            expiry = pin.get("expiry_time")
            expiry_dt = parse_utc_timestamp(expiry)
            hours_remaining = None
            status = "idle"
            if expiry_dt is not None:
                hours_remaining = round((expiry_dt - now).total_seconds() / 3600.0, 2)
                status = "running" if hours_remaining > 0 else "expired"

            extractors.append({
                "product": resolve_pi_product_name(product_type_id),
                "product_type_id": product_type_id,
                "expiry": expiry,
                "hours_remaining": hours_remaining,
                "status": status,
            })

            if status == "expired":
                attention_reasons.append("Extractor already expired")
            elif hours_remaining is not None and hours_remaining <= 6:
                attention_reasons.append(f"Extractor expires in {hours_remaining}h")

        incoming_by_pin: dict[int, list[int]] = {}
        outgoing_by_pin: dict[int, list[int]] = {}
        for route in routes:
            if not isinstance(route, dict):
                continue
            source_pin = route.get("source_pin_id")
            destination_pin = route.get("destination_pin_id")
            content_type = route.get("content_type_id")
            if isinstance(source_pin, int) and isinstance(content_type, int):
                outgoing_by_pin.setdefault(source_pin, []).append(content_type)
            if isinstance(destination_pin, int) and isinstance(content_type, int):
                incoming_by_pin.setdefault(destination_pin, []).append(content_type)

        factories: list[dict] = []
        for pin in pins:
            if not isinstance(pin, dict):
                continue
            if "factory_details" not in pin and "schematic_id" not in pin:
                continue
            pin_id = pin.get("pin_id")
            if not isinstance(pin_id, int):
                continue
            input_types = sorted(set(incoming_by_pin.get(pin_id, [])))
            output_types = sorted(set(outgoing_by_pin.get(pin_id, [])))
            schematic = pin.get("schematic_id")
            factories.append({
                "input": ", ".join(resolve_pi_product_name(tid) for tid in input_types) if input_types else "unknown",
                "output": ", ".join(resolve_pi_product_name(tid) for tid in output_types) if output_types else "unknown",
                "schematic": f"Schematic {schematic}" if schematic is not None else "unknown",
            })

        storage_fill_pct = estimate_storage_fill_pct(pins)
        if storage_fill_pct is not None and storage_fill_pct >= 80:
            attention_reasons.append(f"Storage/Launchpad at {storage_fill_pct}%")

        unique_reasons = list(dict.fromkeys(attention_reasons))
        parsed.append({
            "planet_id": planet_id,
            "planet_name": detail.get("_planet_name", f"Planet {planet_id}"),
            "planet_type": planet.get("planet_type"),
            "solar_system_id": planet.get("solar_system_id"),
            "character": detail.get("_character_name", "unknown"),
            "extractors": extractors,
            "storage_fill_pct": storage_fill_pct,
            "factories": factories,
            "needs_attention": bool(unique_reasons),
            "action_required": "; ".join(unique_reasons) if unique_reasons else "none",
        })

    return parsed


def collect_pi_type_ids(planet_details: dict) -> list[int]:
    """Gather every product type ID referenced by a set of PI colonies."""
    type_ids: set[int] = set()
    for detail in planet_details.values():
        if not isinstance(detail, dict):
            continue
        for pin in detail.get("pins") or []:
            if not isinstance(pin, dict):
                continue
            extractor = pin.get("extractor_details")
            if isinstance(extractor, dict) and isinstance(extractor.get("product_type_id"), int):
                type_ids.add(extractor["product_type_id"])
        for route in detail.get("routes") or []:
            if isinstance(route, dict) and isinstance(route.get("content_type_id"), int):
                type_ids.add(route["content_type_id"])
    return sorted(type_ids)


def get_pi_status(character_id: int, token: str) -> list[dict]:
    """Fetch planets + details and return parsed, actionable PI status."""
    planets = get_pi_planets(character_id=character_id, token=token)
    details: dict[str, dict] = {}

    planet_ids = []
    for planet in planets:
        if isinstance(planet, dict) and isinstance(planet.get("planet_id"), int):
            planet_ids.append(planet["planet_id"])

    # Planet names come from /universe/planets/{id}/, not /universe/names/:
    # the bulk endpoint does not resolve planet IDs at all, and because it
    # rejects an entire batch containing one unresolvable ID, sending planets
    # there used to fail every lookup in the request. Failures stay non-fatal —
    # the caller falls back to a `Planet <id>` label.
    planet_names = {}
    for planet_id in planet_ids:
        try:
            name = get_universe_planet(planet_id).get("name")
            if isinstance(name, str):
                planet_names[planet_id] = name
        except ESIError as exc:
            print(f"Warning: could not resolve name for planet {planet_id}: {exc}", file=sys.stderr)

    # The colony owner is the character we were asked about; resolving it once
    # is what fills the "character" field, which otherwise always read
    # "unknown". Non-fatal, same as the names above.
    character_name = None
    try:
        for item in get_universe_names([character_id]):
            if isinstance(item, dict) and item.get("id") == character_id:
                character_name = item.get("name")
    except ESIError as exc:
        print(f"Warning: could not resolve character name: {exc}", file=sys.stderr)

    for planet in planets:
        if not isinstance(planet, dict):
            continue
        planet_id = planet.get("planet_id")
        if not isinstance(planet_id, int):
            continue

        detail = get_pi_planet_detail(character_id=character_id, planet_id=planet_id, token=token)
        if planet_id in planet_names:
            detail["_planet_name"] = planet_names[planet_id]
        if character_name:
            detail["_character_name"] = character_name
        details[str(planet_id)] = detail

    cache_type_names(collect_pi_type_ids(details))
    return parse_pi_status(planets_data=planets, planet_details=details)


def run_action(args: argparse.Namespace, parser: argparse.ArgumentParser) -> Any:
    """Execute high-level action mode."""
    if args.action in {"pi_planets", "pi_planet_detail", "pi_status", "character_location"}:
        if not args.token:
            parser.error(f"--char or --token is required for action '{args.action}'")
        if args.character_id is None and args.char:
            # A stored character key already implies its ID — no need to pass both.
            try:
                from get_token import get_character_id
                args.character_id = get_character_id(args.char)
            except Exception as exc:
                parser.error(f"Could not resolve character ID for '{args.char}': {exc}")
        if args.character_id is None:
            parser.error(f"--character-id is required for action '{args.action}'")

    if args.action == "pi_planets":
        return get_pi_planets(character_id=args.character_id, token=args.token)

    if args.action == "pi_planet_detail":
        if args.planet_id is None:
            parser.error("--planet-id is required for action 'pi_planet_detail'")
        return get_pi_planet_detail(
            character_id=args.character_id,
            planet_id=args.planet_id,
            token=args.token,
        )

    if args.action == "pi_status":
        return get_pi_status(character_id=args.character_id, token=args.token)

    if args.action == "market_price_bulk":
        return get_market_price_bulk()

    if args.action == "jita_price":
        if args.type_id is None:
            parser.error("--type-id is required for action 'jita_price'")
        return get_jita_price(type_id=args.type_id)

    if args.action == "system_kills":
        ids = None
        if args.system_ids:
            ids = [int(x) for x in args.system_ids.split(",")]
        return get_system_kills(system_ids=ids)

    if args.action == "system_jumps":
        ids = None
        if args.system_ids:
            ids = [int(x) for x in args.system_ids.split(",")]
        return get_system_jumps(system_ids=ids)

    if args.action == "route_plan":
        if args.origin is None or args.destination is None:
            parser.error("--origin and --destination are required for action 'route_plan'")
        avoid = None
        if args.avoid:
            avoid = [int(x) for x in args.avoid.split(",")]
        return get_route(
            origin=args.origin,
            destination=args.destination,
            flag=args.route_flag or "secure",
            avoid=avoid,
        )

    if args.action == "system_info":
        if args.system_id is None:
            parser.error("--system-id is required for action 'system_info'")
        return get_system_info(system_id=args.system_id)

    if args.action == "character_location":
        return get_character_location(character_id=args.character_id, token=args.token)

    if args.action == "incursions":
        return get_incursions()

    if args.action == "fw_systems":
        return get_fw_systems()

    parser.error(f"Unsupported action: {args.action}")
    return None


def main():
    global COMPATIBILITY_DATE

    parser = argparse.ArgumentParser(description="Query EVE ESI API endpoints")
    parser.add_argument("--token", required=False,
                        help="ESI access token (Bearer). Exposed via ps/shell history — "
                             "prefer --char or --token-stdin")
    parser.add_argument("--char", required=False,
                        help="Stored character key; refreshes the token in-process so it "
                             "never appears in argv (recommended)")
    parser.add_argument("--token-stdin", action="store_true",
                        help="Read the access token from the first line of stdin")
    parser.add_argument("--endpoint", required=False,
                        help="ESI endpoint path, e.g. /characters/12345/wallet/")
    parser.add_argument("--method", default="GET", choices=["GET", "POST", "PUT", "DELETE"],
                        help="HTTP method (default: GET)")
    parser.add_argument("--body", default=None, help="JSON body for POST/PUT requests")
    parser.add_argument("--allow-write", action="store_true",
                        help="Required for state-changing requests (PUT, DELETE, and POST to "
                             "any endpoint that is not a documented bulk lookup)")
    parser.add_argument("--pages", action="store_true",
                        help="Automatically fetch all pages (GET only)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--compatibility-date", default=None,
                        help=f"ESI compatibility date as YYYY-MM-DD (default: "
                             f"{DEFAULT_COMPATIBILITY_DATE}, or EVE_ESI_COMPATIBILITY_DATE). "
                             f"Valid values: https://esi.evetech.net/meta/compatibility-dates")

    parser.add_argument(
        "--action",
        choices=[
            "pi_planets", "pi_planet_detail", "pi_status",
            "market_price_bulk", "jita_price",
            "system_kills", "system_jumps", "route_plan",
            "system_info", "character_location",
            "incursions", "fw_systems",
        ],
        help="Run a high-level helper action instead of raw endpoint mode",
    )
    parser.add_argument("--character-id", type=int, help="EVE character ID for PI actions")
    parser.add_argument("--planet-id", type=int, help="Planet ID for pi_planet_detail")
    parser.add_argument("--type-id", type=int, help="Type ID for jita_price")
    parser.add_argument("--system-ids", type=str, help="Comma-separated system IDs for kill/jump filtering")
    parser.add_argument("--system-id", type=int, help="Single system ID for system_info")
    parser.add_argument("--origin", type=int, help="Origin system ID for route_plan")
    parser.add_argument("--destination", type=int, help="Destination system ID for route_plan")
    parser.add_argument("--route-flag", choices=["shortest", "secure", "insecure"], default="secure",
                        help="Route preference (default: secure)")
    parser.add_argument("--avoid", type=str, help="Comma-separated system IDs to avoid in route")
    args = parser.parse_args()

    if args.compatibility_date:
        # Checked here rather than left to ESI: a rejected date costs 5 tokens
        # from the error rate limit, a local regex costs nothing.
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.compatibility_date):
            parser.error("--compatibility-date must be YYYY-MM-DD")
        COMPATIBILITY_DATE = args.compatibility_date

    args.token = resolve_token(args, parser)

    try:
        if args.action:
            result = run_action(args, parser)
        else:
            if not args.endpoint:
                parser.error("--endpoint is required when --action is not used")
            endpoint = normalize_endpoint(args.endpoint)
            if is_state_changing(args.method, endpoint) and not args.allow_write:
                parser.error(
                    f"{args.method} {endpoint} may change account state and is outside this "
                    f"skill's documented read-only scope. Re-run with --allow-write if you "
                    f"really intend to modify your EVE account."
                )
            if args.pages and args.method == "GET":
                result = esi_request_all_pages(endpoint, token=args.token)
            else:
                result, headers = esi_request(endpoint, token=args.token, method=args.method, body=args.body)
                expires = headers.get("expires", "unknown")
                print(f"Cache expires: {expires}", file=sys.stderr)
    except ESIError as e:
        print(f"ESI error: {e}", file=sys.stderr)
        sys.exit(1)

    indent = 2 if args.pretty else None
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=indent, ensure_ascii=False))
    else:
        print(result)


if __name__ == "__main__":
    main()
