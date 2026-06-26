#!/usr/bin/env python3
"""Amadeus flight offers (Self-Service)

- OAuth2: POST /v1/security/oauth2/token (client_credentials)
- Search: GET /v2/shopping/flight-offers

No external Python deps.
"""

import os
import sys
import json
import argparse
import urllib.parse
import urllib.request
import urllib.error


def env(name: str, default: str | None = None) -> str:
    v = os.environ.get(name, default)
    if v is None or v == "":
        raise RuntimeError(f"Missing required env var: {name}")
    return v


def bool_str(v: str) -> str:
    v = v.strip().lower()
    if v in {"true", "1", "yes", "y"}:
        return "true"
    if v in {"false", "0", "no", "n"}:
        return "false"
    raise argparse.ArgumentTypeError("Expected boolean: true/false")


def post_form(url: str, data: dict, headers: dict | None = None) -> dict:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} for {url}: {txt}") from e
    return json.loads(raw)


def get_json(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, method="GET")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} for {url}: {txt}") from e
    return json.loads(raw)


def get_access_token(host: str) -> str:
    client_id = env("AMADEUS_CLIENT_ID")
    client_secret = env("AMADEUS_CLIENT_SECRET")
    token_url = f"{host}/v1/security/oauth2/token"
    j = post_form(
        token_url,
        {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    token = j.get("access_token")
    if not token:
        raise RuntimeError(f"No access_token in response: {j}")
    return token


def fmt_duration(iso: str | None) -> str:
    if not iso:
        return "?"
    # ISO 8601 duration, commonly PT#H#M
    return iso.replace("PT", "").lower()


def fmt_dt_ddmmyy(dt: str | None) -> str:
    if not dt:
        return "?"
    # Expect: YYYY-MM-DDTHH:MM:SS (or without seconds)
    dt = dt.replace("T", " ")
    date_part, *rest = dt.split(" ")
    time_part = rest[0] if rest else ""
    try:
        yyyy, mm, dd = date_part.split("-")
        yy = yyyy[-2:]
        date_out = f"{dd}/{mm}/{yy}"
    except Exception:
        return dt
    if time_part:
        time_out = time_part[:5]
        return f"{date_out} {time_out}"
    return date_out


def summarize_offer(offer: dict) -> str:
    price = offer.get("price", {})
    total = price.get("total")
    currency = price.get("currency")
    currency_sig = "€" if currency == "EUR" else currency

    itineraries = offer.get("itineraries") or []
    it = itineraries[0] if itineraries else {}
    dur = fmt_duration(it.get("duration"))
    segs = it.get("segments") or []

    if segs:
        dep = segs[0].get("departure", {})
        arr = segs[-1].get("arrival", {})
        dep_code = dep.get("iataCode")
        dep_at = fmt_dt_ddmmyy(dep.get("at"))
        arr_code = arr.get("iataCode")
        arr_at = fmt_dt_ddmmyy(arr.get("at"))
        carriers = []
        for s in segs:
            c = s.get("carrierCode")
            if c and (not carriers or carriers[-1] != c):
                carriers.append(c)
        stops = max(0, len(segs) - 1)
        route = f"{dep_code}→{arr_code}"
        timing = f"{dep_at} → {arr_at}"
        stop_label = "stop" if stops == 1 else "stops"
        return f"{currency_sig} {total} | {route} | {timing} | dur {dur} | {stops} {stop_label} | {','.join(carriers)}"

    return f"{currency_sig} {total} | (no segment details)"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Search flight offers with Amadeus")
    p.add_argument("--origin", required=True, help="Origin IATA code (e.g., ZRH)")
    p.add_argument("--destination", required=True, help="Destination IATA code (e.g., IST)")
    p.add_argument("--departure", required=True, help="Departure date YYYY-MM-DD")
    p.add_argument("--return", dest="return_date", help="Return date YYYY-MM-DD")
    p.add_argument("--adults", type=int, default=1)
    p.add_argument("--travel-class", default="ECONOMY", help="Travel class. Accepts: ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST (also accepts aliases: ECO, PREMIUM_ECO)")
    p.add_argument("--non-stop", type=bool_str, default="false", help="true|false")
    p.add_argument("--included-airlines", default="", help="Comma-separated carrier codes (e.g., AF,LX)")
    p.add_argument("--max", type=int, default=6, help="Max offers")
    p.add_argument("--dump", help="Write raw JSON response to path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    host = os.environ.get("AMADEUS_HOST", "https://api.amadeus.com").rstrip("/")

    token = get_access_token(host)

    travel_class = (args.travel_class or "").strip().upper()
    travel_class_map = {
        "ECO": "ECONOMY",
        "ECONOMY": "ECONOMY",
        "PREMIUM_ECO": "PREMIUM_ECONOMY",
        "PREMIUM_ECONOMY": "PREMIUM_ECONOMY",
        "BUSINESS": "BUSINESS",
        "FIRST": "FIRST",
    }
    if travel_class not in travel_class_map:
        raise RuntimeError(f"Unsupported travel class: {args.travel_class} (try ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)")

    params = {
        "originLocationCode": args.origin,
        "destinationLocationCode": args.destination,
        "departureDate": args.departure,
        "adults": str(args.adults),
        "travelClass": travel_class_map[travel_class],
        "nonStop": args.non_stop,
        "max": str(args.max),
    }
    if args.return_date:
        params["returnDate"] = args.return_date
    if args.included_airlines.strip():
        params["includedAirlineCodes"] = args.included_airlines.strip()

    url = f"{host}/v2/shopping/flight-offers?{urllib.parse.urlencode(params)}"
    j = get_json(url, headers={"Authorization": f"Bearer {token}"})

    if args.dump:
        with open(args.dump, "w", encoding="utf-8") as f:
            json.dump(j, f, ensure_ascii=False, indent=2)

    data = j.get("data") or []
    if not data:
        print("No offers returned.")
        return 0

    print(f"Offers: {len(data)} (showing up to {min(len(data), args.max)})")
    for idx, offer in enumerate(data[: args.max], start=1):
        print(f"{idx}. {summarize_offer(offer)}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise
