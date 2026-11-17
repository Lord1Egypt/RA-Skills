#!/usr/bin/env python3
"""
AstroClaw daily forecast fetcher for AI agents.

Calculates your zodiac sign from your birth/creation date, then fetches
today's cosmic alignment forecast.

Usage:
  python3 astroclaw.py                          # use DEFAULT_BIRTHDAY
  python3 astroclaw.py --birthday 2024-01-15    # explicit birthday
  python3 astroclaw.py --sign gemini            # override sign manually
  python3 astroclaw.py --help                   # full options

For cron jobs (no_agent=True), set DEFAULT_BIRTHDAY below to your
agent's creation/deployment date. The sign is then computed automatically.
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
import urllib.request
from datetime import date

# ── CONFIGURE THIS ──────────────────────────────────────────────
# Set to your agent's creation/deployment date (YYYY-MM-DD).
# The script computes your zodiac sign from this date automatically.
# If unset (None), defaults to Aquarius (the water bearer — innovation,
# technology, and forward-thinking — a fitting default for AI agents).
DEFAULT_BIRTHDAY = None  # e.g. "2024-03-15"
# ────────────────────────────────────────────────────────────────

VALID_SIGNS = {
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
}

# First day of each sign, latest in the year first. Matches astroclaw.xyz/api/sign.
SIGN_STARTS = [
    ("capricorn",   (12, 22)),  # Dec 22 – Jan 19
    ("sagittarius", (11, 22)),  # Nov 22 – Dec 21
    ("scorpio",     (10, 23)),  # Oct 23 – Nov 21
    ("libra",       (9, 23)),   # Sep 23 – Oct 22
    ("virgo",       (8, 23)),   # Aug 23 – Sep 22
    ("leo",         (7, 23)),   # Jul 23 – Aug 22
    ("cancer",      (6, 21)),   # Jun 21 – Jul 22
    ("gemini",      (5, 21)),   # May 21 – Jun 20
    ("taurus",      (4, 20)),   # Apr 20 – May 20
    ("aries",       (3, 21)),   # Mar 21 – Apr 19
    ("pisces",      (2, 19)),   # Feb 19 – Mar 20
    ("aquarius",    (1, 20)),   # Jan 20 – Feb 18
]

API_BASE = "https://www.astroclaw.xyz"


def calculate_sign(birthday: date) -> str:
    """Return the zodiac sign for a given birth date."""
    key = (birthday.month, birthday.day)
    for sign, start in SIGN_STARTS:
        if key >= start:
            return sign
    return "capricorn"  # Jan 1 – Jan 19


def validate_sign(sign: str) -> str:
    """Normalize and validate a zodiac sign."""
    normalized = sign.lower().strip()
    if normalized not in VALID_SIGNS:
        valid = ", ".join(sorted(VALID_SIGNS))
        raise ValueError(f"Unknown zodiac sign '{sign}'. Valid signs: {valid}.")
    return normalized


def sanitize_forecast(raw_forecast: str, max_chars: int = 500) -> str:
    """Convert fetched HTML content into bounded, plain text."""
    text = re.sub(r"<[^>]+>", "", raw_forecast)
    text = html_lib.unescape(text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > max_chars:
        text = text[: max_chars - 1].rstrip() + "..."

    return text or "Forecast not available today."


def fetch_forecast(sign: str, forecast_date: date | None = None) -> tuple[str, str]:
    """Fetch a forecast; returns (forecast date, sanitized text).

    Without a date this reads the latest published forecast, which avoids 404s
    around midnight UTC and in time zones ahead of UTC.
    """
    sign = validate_sign(sign)
    if forecast_date:
        url = f"{API_BASE}/api/forecasts/{forecast_date}/{sign}.json"
    else:
        url = f"{API_BASE}/api/forecasts/today/{sign}.json"

    request = urllib.request.Request(url, headers={"X-Astroclaw-Agent": "astroclaw-skill-script"})
    with urllib.request.urlopen(request, timeout=15) as resp:
        data = json.load(resp)

    return data["date"], sanitize_forecast(data.get("horoscope", ""))


def main():
    parser = argparse.ArgumentParser(
        description="Fetch your AstroClaw daily cosmic forecast."
    )
    parser.add_argument(
        "--birthday", "-b",
        help="Your birth/creation date (YYYY-MM-DD). Overrides DEFAULT_BIRTHDAY."
    )
    parser.add_argument(
        "--sign", "-s",
        help="Zodiac sign override (e.g. gemini, aries). Skips birthday calculation."
    )
    parser.add_argument(
        "--date", "-d",
        help="Forecast date (YYYY-MM-DD). Defaults to the latest published forecast."
    )
    args = parser.parse_args()

    # Determine birth date
    if args.birthday:
        birthday = date.fromisoformat(args.birthday)
    elif DEFAULT_BIRTHDAY:
        birthday = date.fromisoformat(DEFAULT_BIRTHDAY)
    else:
        birthday = None

    # Determine sign
    if args.sign:
        try:
            sign = validate_sign(args.sign)
        except ValueError as e:
            print(f"AstroClaw configuration error: {e}", file=sys.stderr)
            sys.exit(2)
    elif birthday:
        sign = calculate_sign(birthday)
    else:
        sign = "aquarius"  # no birthday set, sensible default

    # Forecast date (None means the latest published forecast)
    forecast_date = date.fromisoformat(args.date) if args.date else None

    # Fetch
    try:
        published_date, forecast = fetch_forecast(sign, forecast_date)
    except Exception as e:
        print(f"⚠️  AstroClaw fetch failed: {e}")
        sys.exit(1)

    # Output
    print(f"🌌  ASTROCLAW DAILY FORECAST")
    print(f"{'=' * 40}")
    if birthday:
        print(f"Sign: {sign.title()} (born {birthday})")
    else:
        print(f"Sign: {sign.title()}")
    print(f"Date: {published_date}")
    print()
    print(forecast)
    print()
    print("— astroclaw.xyz —")


if __name__ == "__main__":
    main()
