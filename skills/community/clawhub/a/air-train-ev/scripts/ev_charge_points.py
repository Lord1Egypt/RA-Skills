#!/usr/bin/env python3
"""Find nearby EV charge points via Open Charge Map.

Docs: https://openchargemap.org/site/develop/api
API: GET https://api.openchargemap.io/v3/poi/

Env:
- OPENCHARGEMAP_API_KEY (required)
- OPENCHARGEMAP_HOST (default: https://api.openchargemap.io)

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


def get_json(url: str, headers: dict | None = None):
    req = urllib.request.Request(url, method="GET")
    # Some edge/CDN layers block requests without a UA.
    req.add_header("User-Agent", "OpenClaw/air_train_ev (contact: alessandro@update.solutions)")
    req.add_header("Accept", "application/json")
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


def summarize(item: dict) -> str:
    addr = item.get("AddressInfo") or {}
    title = addr.get("Title") or "(no title)"
    line = addr.get("AddressLine1") or ""
    town = addr.get("Town") or ""
    postcode = addr.get("Postcode") or ""
    country = (addr.get("Country") or {}).get("ISOCode") or (addr.get("Country") or {}).get("Title") or ""
    dist = addr.get("Distance")
    dist_unit = addr.get("DistanceUnit")

    lat = addr.get("Latitude")
    lon = addr.get("Longitude")

    conns = item.get("Connections") or []
    plugs = []
    for c in conns:
        ctype = (c.get("ConnectionType") or {}).get("Title")
        kw = c.get("PowerKW")
        qty = c.get("Quantity")
        if ctype:
            s = ctype
            if kw:
                s += f" {kw:g}kW"
            if qty:
                s += f" x{qty}"
            plugs.append(s)
    plugs_txt = "; ".join(plugs[:6]) if plugs else "(no connector info)"

    parts = [title]
    if line or town:
        parts.append(", ".join([p for p in [line, f"{postcode} {town}".strip()] if p]).strip(", "))
    if country:
        parts.append(country)
    if dist is not None:
        # OCM usually returns distance in km when distanceunit=KM
        parts.append(f"{dist:.2f} km")
    parts.append(plugs_txt)
    if lat is not None and lon is not None:
        parts.append(f"({lat:.5f},{lon:.5f})")

    return " — ".join([p for p in parts if p])


def parse_args():
    p = argparse.ArgumentParser(description="Find EV charge points (Open Charge Map)")
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    p.add_argument("--km", type=float, default=5.0, help="Search radius in km")
    p.add_argument("--max", type=int, default=10, help="Max results")
    p.add_argument("--countrycode", help="Optional ISO 2 country code, e.g. FR")
    p.add_argument("--operators", help="Optional operator IDs comma-separated")
    p.add_argument("--usage", help="Optional usage type ID")
    p.add_argument("--verbose", action="store_true", help="Request verbose results (more fields, including connectors when available)")
    p.add_argument("--dump", help="Write raw JSON to file")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    host = os.environ.get("OPENCHARGEMAP_HOST", "https://api.openchargemap.io").rstrip("/")
    key = env("OPENCHARGEMAP_API_KEY")

    compact = "false" if args.verbose else "true"
    verbose = "true" if args.verbose else "false"

    params = {
        "output": "json",
        "latitude": f"{args.lat}",
        "longitude": f"{args.lon}",
        "distance": f"{args.km}",
        "distanceunit": "KM",
        "maxresults": str(args.max),
        "compact": compact,
        "verbose": verbose,
        "key": key,
    }
    if args.countrycode:
        params["countrycode"] = args.countrycode
    if args.operators:
        params["operatorid"] = args.operators
    if args.usage:
        params["usagetypeid"] = args.usage

    url = f"{host}/v3/poi/?{urllib.parse.urlencode(params)}"
    data = get_json(url)

    if args.dump:
        with open(args.dump, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    if not data:
        print("No charge points returned.")
        return 0

    for i, item in enumerate(data[: args.max], start=1):
        print(f"{i}. {summarize(item)}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise
