#!/usr/bin/env python3
"""Utility script for managing the DJ roster (add/list/match)."""

import argparse
import json
import os
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from math import radians, sin, cos, sqrt, asin
from pathlib import Path
from typing import List, Dict, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
ROSTER_PATH = DATA_DIR / "dj_roster.json"
GEOCACHE_PATH = DATA_DIR / "geocache.json"


def load_roster() -> List[Dict]:
    if not ROSTER_PATH.exists():
        return []
    with open(ROSTER_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return []


def save_roster(roster: List[Dict]) -> None:
    ROSTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ROSTER_PATH, "w", encoding="utf-8") as f:
        json.dump(roster, f, indent=2, ensure_ascii=False)


def load_geocache() -> Dict[str, Dict[str, float]]:
    if not GEOCACHE_PATH.exists():
        return {}
    with open(GEOCACHE_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    return {}


def save_geocache(cache: Dict[str, Dict[str, float]]) -> None:
    GEOCACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GEOCACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def normalize_list(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def loose_city_match(first: str, second: str, threshold: float = 0.82) -> bool:
    a = (first or "").strip().lower()
    b = (second or "").strip().lower()
    if not a or not b:
        return False
    if a == b or a in b or b in a:
        return True
    return SequenceMatcher(None, a, b).ratio() >= threshold


def geocode_location(query: str) -> Optional[Tuple[float, float]]:
    key = query.strip().lower()
    if not key:
        return None
    cache = load_geocache()
    if key in cache:
        coords = cache[key]
        return coords.get("lat"), coords.get("lon")
    params = urllib.parse.urlencode({"q": query, "format": "json", "limit": 1})
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "dj-booking-bot/1.0 (contact@djayl.co.uk)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
    except Exception:
        return None
    if not data:
        return None
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    cache[key] = {"lat": lat, "lon": lon}
    save_geocache(cache)
    return lat, lon


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Earth radius in miles
    r = 3958.8
    phi1, phi2 = radians(lat1), radians(lat2)
    d_phi = radians(lat2 - lat1)
    d_lambda = radians(lon2 - lon1)
    a = sin(d_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(d_lambda / 2) ** 2
    c = 2 * asin(min(1, sqrt(a)))
    return r * c


def add_entry(args: argparse.Namespace) -> None:
    roster = load_roster()
    entry = {
        "name": args.name.strip(),
        "country": args.country.strip(),
        "city": args.city.strip(),
        "genres": normalize_list(args.genres),
        "dj_types": normalize_list(args.dj_types),
        "availability": args.availability.strip(),
        "budget_min": args.budget_min,
        "budget_max": args.budget_max,
        "contact": args.contact.strip(),
        "notes": args.notes.strip() if args.notes else "",
        "travel_radius_miles": args.travel_radius,
        "home_location": None,
    }
    location_query = f"{entry['city']}, {entry['country']}"
    coords = geocode_location(location_query)
    if coords:
        entry["home_location"] = {"query": location_query, "lat": coords[0], "lon": coords[1]}
    roster.append(entry)
    save_roster(roster)
    print(f"Added {entry['name']} to roster ({ROSTER_PATH}).")


def list_entries(args: argparse.Namespace) -> None:
    roster = load_roster()
    if not roster:
        print("No DJs recorded yet.")
        return
    for idx, entry in enumerate(roster, 1):
        genres = ", ".join(entry.get("genres", []))
        budget = f"${entry.get('budget_min', 0)}-${entry.get('budget_max', 0)}"
        print(f"{idx}. {entry['name']} — {entry['city']}, {entry['country']} | {genres} | {budget}")


def score_entry(entry: Dict, args: argparse.Namespace) -> int:
    score = 0
    entry_city = entry.get("city", "")
    if args.city:
        if loose_city_match(entry_city, args.city):
            score += 3
    elif args.country and entry.get("country", "").lower() == args.country.lower():
        score += 1

    desired_genres = set(g.lower() for g in (args.genres or []) if g.lower() not in {"any", "all"})
    entry_genres = set(g.lower() for g in entry.get("genres", []))
    overlap = desired_genres & entry_genres
    score += 2 * len(overlap)

    desired_types = set(t.lower() for t in (args.dj_types or []) if t.lower() not in {"any", "all"})
    entry_types = set(t.lower() for t in entry.get("dj_types", []))
    overlap_types = desired_types & entry_types
    if desired_types and overlap_types:
        score += 3 * len(overlap_types)

    if args.budget is not None:
        min_budget = entry.get("budget_min", 0)
        max_budget = entry.get("budget_max", min_budget)
        if min_budget <= args.budget <= max_budget:
            score += 2
        elif args.budget <= max_budget:
            score += 1

    return score


def entry_covers_event(
    entry: Dict, args: argparse.Namespace, event_coords: Optional[Tuple[float, float]]
) -> bool:
    if args.country and entry.get("country", "").lower() != args.country.lower():
        return False
    if not args.city:
        return True
    city_query = args.city
    entry_city = entry.get("city", "")
    if loose_city_match(entry_city, city_query):
        return True
    radius = entry.get("travel_radius_miles", 0) or 0
    home = entry.get("home_location") or {}
    if radius <= 0 or not home or "lat" not in home or not event_coords:
        return False
    distance = haversine_miles(home["lat"], home["lon"], event_coords[0], event_coords[1])
    return distance <= radius


def match_entries(args: argparse.Namespace) -> None:
    roster = load_roster()
    if not roster:
        print("[]")
        return

    event_coords: Optional[Tuple[float, float]] = None
    if args.city:
        query = f"{args.city}, {args.country}" if args.country else args.city
        event_coords = geocode_location(query)
        if event_coords is None:
            print("[]")
            return

    desired_types = set(t.lower() for t in (args.dj_types or []) if t.lower() not in {"any", "all"})
    requested_genres = set(g.lower() for g in (args.genres or []) if g.lower() not in {"any", "all"})

    matches = []
    for entry in roster:
        entry_types = set(t.lower() for t in entry.get("dj_types", []))
        if desired_types and not (entry_types & desired_types):
            continue
        entry_genres = set(g.lower() for g in entry.get("genres", []))
        if requested_genres and not (entry_genres & requested_genres):
            continue
        if not entry_covers_event(entry, args, event_coords):
            continue
        score = score_entry(entry, args)
        if score > 0:
            matches.append((score, entry))

    matches.sort(key=lambda item: item[0], reverse=True)
    top_matches = [entry for _, entry in matches[: args.limit]]
    print(json.dumps(top_matches, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Manage the DJ roster.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a DJ to the roster")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--country", required=True)
    add_parser.add_argument("--city", required=True)
    add_parser.add_argument("--genres", required=True, help="Comma-separated genres")
    add_parser.add_argument("--dj-types", dest="dj_types", required=True, help="Comma-separated DJ types (e.g. wedding, open format, club)")
    add_parser.add_argument("--availability", required=True, help="Free-text availability notes")
    add_parser.add_argument("--budget-min", dest="budget_min", type=int, required=True)
    add_parser.add_argument("--budget-max", dest="budget_max", type=int, required=True)
    add_parser.add_argument(
        "--travel-radius",
        dest="travel_radius",
        type=int,
        required=True,
        help="Maximum travel distance in miles",
    )
    add_parser.add_argument("--contact", required=True, help="Discord handle / email")
    add_parser.add_argument("--notes", default="", help="Optional extra notes")
    add_parser.set_defaults(func=add_entry)

    list_parser = subparsers.add_parser("list", help="List DJs in the roster")
    list_parser.set_defaults(func=list_entries)

    match_parser = subparsers.add_parser("match", help="Find DJs that fit a brief")
    match_parser.add_argument("--city", help="Target city")
    match_parser.add_argument("--country", help="Target country")
    match_parser.add_argument("--genres", nargs="*", help="Preferred genres (space separated)")
    match_parser.add_argument("--dj-types", dest="dj_types", nargs="*", help="Desired DJ types (wedding, open format, club, etc.)")
    match_parser.add_argument("--budget", type=int, help="Budget in the requester currency")
    match_parser.add_argument("--limit", type=int, default=3)
    match_parser.set_defaults(func=match_entries)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
