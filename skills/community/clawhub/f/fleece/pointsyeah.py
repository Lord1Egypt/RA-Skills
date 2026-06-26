from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode

BASE = "https://www.pointsyeah.com/"


@dataclass(frozen=True)
class FlightsQuery:
    origin: str
    destination: str
    date: str  # YYYY-MM-DD
    return_date: str | None = None
    adults: int = 1
    cabin: str = "economy"  # economy|premium-economy|business|first


@dataclass(frozen=True)
class HotelsQuery:
    location: str
    checkin: str  # YYYY-MM-DD
    checkout: str  # YYYY-MM-DD
    guests: int = 1
    rooms: int = 1


def build_flights_url(q: FlightsQuery) -> str:
    """Best-effort PointsYeah URL.

    PointsYeah does not publish a stable, documented deep-link format.
    We therefore generate a URL using query params that are easy to read/share.

    If PointsYeah changes their site, users can still paste these params into
    the site manually.
    """
    params = {
        "type": "flights",
        "origin": q.origin.upper(),
        "destination": q.destination.upper(),
        "date": q.date,
        "return": q.return_date or "",
        "adults": str(q.adults),
        "cabin": q.cabin,
    }
    return BASE + "?" + urlencode(params)


def build_hotels_url(q: HotelsQuery) -> str:
    params = {
        "type": "hotels",
        "location": q.location,
        "checkin": q.checkin,
        "checkout": q.checkout,
        "guests": str(q.guests),
        "rooms": str(q.rooms),
    }
    return BASE + "?" + urlencode(params)
