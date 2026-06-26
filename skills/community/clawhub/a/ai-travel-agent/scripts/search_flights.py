#!/usr/bin/env python3
"""
Search Google Flights via SerpAPI.
Usage: python3 search_flights.py --from LGW --to BCN --date 2026-06-15 --return-date 2026-06-22 --adults 2 --class economy --currency GBP

API key is read from the SERPAPI_KEY environment variable, or from ~/.serpapi_credentials /
~/.travel_agent_config (key=value format). Never pass the key as a CLI argument.
"""

import argparse
import json
import os
import sys
import requests


def load_api_key():
    """Load SerpAPI key from env var or credential files. Never from CLI args."""
    key = os.environ.get("SERPAPI_KEY")
    if key:
        return key
    for path in [os.path.expanduser("~/.serpapi_credentials"),
                 os.path.expanduser("~/.travel_agent_config")]:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("SERPAPI_KEY="):
                        return line.split("=", 1)[1].strip()
    print("ERROR: SERPAPI_KEY not found. Set it as an environment variable or store it in "
          "~/.serpapi_credentials (SERPAPI_KEY=yourkey).", file=sys.stderr)
    sys.exit(1)


def search_flights(departure_id, arrival_id, outbound_date, return_date=None,
                   adults=1, children=0, seat_class=1, currency="GBP", api_key=None):
    """
    seat_class: 1=Economy, 2=Premium Economy, 3=Business, 4=First
    """
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "adults": adults,
        "children": children,
        "travel_class": seat_class,
        "currency": currency,
        "hl": "en",
        "api_key": api_key,
    }

    if return_date:
        params["return_date"] = return_date
    else:
        params["type"] = 2  # one-way

    resp = requests.get("https://serpapi.com/search", params=params)
    resp.raise_for_status()
    data = resp.json()

    if "error" in data:
        print(f"ERROR: {data['error']}", file=sys.stderr)
        sys.exit(1)

    results = []

    for category, flights in [("best", data.get("best_flights", [])),
                               ("other", data.get("other_flights", []))]:
        for f in flights:
            legs = f.get("flights", [])
            entry = {
                "category": category,
                "price": f.get("price"),
                "stops": f.get("stops", 0),
                "total_duration_min": f.get("total_duration"),
                "booking_token": f.get("booking_token"),
                "legs": []
            }
            for leg in legs:
                entry["legs"].append({
                    "airline": leg.get("airline"),
                    "flight_number": leg.get("flight_number"),
                    "from": leg.get("departure_airport", {}).get("id"),
                    "from_name": leg.get("departure_airport", {}).get("name"),
                    "to": leg.get("arrival_airport", {}).get("id"),
                    "to_name": leg.get("arrival_airport", {}).get("name"),
                    "departs": leg.get("departure_airport", {}).get("time"),
                    "arrives": leg.get("arrival_airport", {}).get("time"),
                    "duration_min": leg.get("duration"),
                    "class": leg.get("travel_class"),
                    "aircraft": leg.get("airplane"),
                    "legroom": leg.get("legroom"),
                    "overnight": leg.get("overnight", False),
                    "often_delayed": leg.get("often_delayed_by_over_30_min", False),
                })
            results.append(entry)

    print(json.dumps(results, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Search Google Flights via SerpAPI")
    parser.add_argument("--from", dest="departure", required=True, help="Departure airport code (e.g. LGW)")
    parser.add_argument("--to", dest="arrival", required=True, help="Arrival airport code (e.g. BCN)")
    parser.add_argument("--date", required=True, help="Outbound date YYYY-MM-DD")
    parser.add_argument("--return-date", default=None, help="Return date YYYY-MM-DD (omit for one-way)")
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--children", type=int, default=0)
    parser.add_argument("--class", dest="seat_class", default="economy",
                        choices=["economy", "premium_economy", "business", "first"])
    parser.add_argument("--currency", default="GBP")

    args = parser.parse_args()

    class_map = {"economy": 1, "premium_economy": 2, "business": 3, "first": 4}

    search_flights(
        departure_id=args.departure,
        arrival_id=args.arrival,
        outbound_date=args.date,
        return_date=args.return_date,
        adults=args.adults,
        children=args.children,
        seat_class=class_map[args.seat_class],
        currency=args.currency,
        api_key=load_api_key(),
    )


if __name__ == "__main__":
    main()
