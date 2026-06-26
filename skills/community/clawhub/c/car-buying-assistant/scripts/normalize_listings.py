#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

EXPECTED_KEYS = [
    "source",
    "url",
    "year_make_model",
    "asking_price",
    "location",
    "odometer_km",
    "transmission",
    "drivetrain",
    "fuel_type",
    "trim",
    "seller_type",
    "notes",
]


def normalize_listing(listing: dict) -> dict:
    out = {}
    for key in EXPECTED_KEYS:
        out[key] = listing.get(key)
    # Allow passing through extra keys if present
    for key, value in listing.items():
        if key not in out:
            out[key] = value
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize car listings JSON.")
    parser.add_argument("--input", required=True, help="Path to input JSON array of listings")
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    args = parser.parse_args()

    in_path = Path(args.input).expanduser()
    out_path = Path(args.output).expanduser()

    with in_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise SystemExit("Input JSON must be an array of listing objects")

    normalized = [normalize_listing(item) for item in data]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(normalized)} normalized listings to {out_path}")


if __name__ == "__main__":
    main()
