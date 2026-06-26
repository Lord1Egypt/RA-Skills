#!/usr/bin/env python3
"""Minimal Navitia client (no external deps).

Commands:
- coverage: list available coverages
- places: autocomplete places within coverage
- journeys: compute journeys between two places (first place match per query)

Env:
- NAVITIA_TOKEN (required)
- NAVITIA_HOST (default https://api.navitia.io)
- NAVITIA_COVERAGE (default sandbox)

Docs: https://doc.navitia.io/
"""

import os
import sys
import json
import argparse
import base64
import urllib.parse
import urllib.request
import urllib.error


def env(name: str, default: str | None = None) -> str:
    v = os.environ.get(name, default)
    if v is None or v == "":
        raise RuntimeError(f"Missing required env var: {name}")
    return v


def navitia_get(path: str, query: dict | None = None) -> dict:
    host = os.environ.get("NAVITIA_HOST", "https://api.navitia.io").rstrip("/")
    token = env("NAVITIA_TOKEN")

    qs = f"?{urllib.parse.urlencode(query)}" if query else ""
    url = f"{host}{path}{qs}"

    req = urllib.request.Request(url, method="GET")

    # Navitia accepts token as basic auth username, but the docs also show Authorization header usage.
    # We use Basic auth with token as username and empty password.
    auth = base64.b64encode(f"{token}:".encode("utf-8")).decode("ascii")
    req.add_header("Authorization", f"Basic {auth}")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} for {url}: {txt}") from e

    return json.loads(raw)


def cmd_coverage(_args: argparse.Namespace) -> int:
    j = navitia_get("/v1/coverage")
    coverages = j.get("coverages") or []
    for c in coverages:
        print(f"{c.get('id')}\t{c.get('name')}")
    return 0


def cmd_places(args: argparse.Namespace) -> int:
    cov = os.environ.get("NAVITIA_COVERAGE", "sandbox")
    j = navitia_get(f"/v1/coverage/{urllib.parse.quote(cov)}/places", {"q": args.q, "count": str(args.count)})
    places = j.get("places") or []
    for p in places:
        # p has keys: embedded_type, quality, [stop_area|administrative_region|...]
        et = p.get("embedded_type")
        obj = p.get(et) if et else None
        name = (obj or {}).get("name")
        pid = (obj or {}).get("id")
        ptype = (obj or {}).get("type")
        print(f"{et}\t{ptype}\t{name}\t{pid}")
    return 0


def resolve_place_id(query: str, count: int = 1) -> str:
    cov = os.environ.get("NAVITIA_COVERAGE", "sandbox")
    j = navitia_get(f"/v1/coverage/{urllib.parse.quote(cov)}/places", {"q": query, "count": str(max(1, count))})
    places = j.get("places") or []
    if not places:
        raise RuntimeError(f"No place found for query: {query} (coverage={cov})")

    p = places[0]
    et = p.get("embedded_type")
    obj = p.get(et) if et else None
    pid = (obj or {}).get("id")
    if not pid:
        raise RuntimeError(f"Place has no id for query: {query}: {p}")
    return pid


def cmd_journeys(args: argparse.Namespace) -> int:
    cov = os.environ.get("NAVITIA_COVERAGE", "sandbox")

    from_id = resolve_place_id(args.from_query)
    to_id = resolve_place_id(args.to_query)

    query = {
        "from": from_id,
        "to": to_id,
        "count": str(args.count),
    }
    if args.datetime:
        query["datetime"] = args.datetime
    if args.datetime_represents:
        query["datetime_represents"] = args.datetime_represents

    j = navitia_get(f"/v1/coverage/{urllib.parse.quote(cov)}/journeys", query)

    journeys = j.get("journeys") or []
    if not journeys:
        print("No journeys returned.")
        return 0

    def t(x: str | None) -> str:
        if not x:
            return "?"
        # YYYYMMDDTHHMMSS -> DD/MM/YY HH:MM
        try:
            y = x[0:4]
            m = x[4:6]
            d = x[6:8]
            hh = x[9:11]
            mm = x[11:13]
            return f"{d}/{m}/{y[2:]} {hh}:{mm}"
        except Exception:
            return x

    for idx, it in enumerate(journeys[: args.count], start=1):
        dep = t(it.get("departure_date_time"))
        arr = t(it.get("arrival_date_time"))
        dur = it.get("duration")
        nb = it.get("nb_transfers")
        print(f"{idx}. {dep} → {arr} | {dur}s | transfers {nb}")

    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Navitia mini client")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_cov = sub.add_parser("coverage", help="List coverages")
    p_cov.set_defaults(fn=cmd_coverage)

    p_places = sub.add_parser("places", help="Autocomplete places")
    p_places.add_argument("--q", required=True)
    p_places.add_argument("--count", type=int, default=5)
    p_places.set_defaults(fn=cmd_places)

    p_j = sub.add_parser("journeys", help="Compute journeys")
    p_j.add_argument("--from", dest="from_query", required=True)
    p_j.add_argument("--to", dest="to_query", required=True)
    p_j.add_argument("--datetime", help="ISO datetime, e.g. 2026-03-07T08:00:00")
    p_j.add_argument("--datetime-represents", dest="datetime_represents", choices=["departure", "arrival"], default="departure")
    p_j.add_argument("--count", type=int, default=5)
    p_j.set_defaults(fn=cmd_journeys)

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise
