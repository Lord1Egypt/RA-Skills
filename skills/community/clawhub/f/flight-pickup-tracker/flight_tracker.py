#!/usr/bin/env python3
"""
Flight Tracker - Monitors a flight and alerts when it's approaching the destination.

Uses OpenSky Network (free, no key) as primary source.
Falls back to AirLabs if AIRLABS_API_KEY is set.

Usage:
    python3 flight_tracker.py --flight AS594 --dest SEA --dry-run
    python3 flight_tracker.py --flight AS594 --dest SEA --poll-interval 300

Environment:
    AIRLABS_API_KEY       Optional fallback API key
"""

import argparse
import json
import math
import os
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError


OPENSKY_BASE = "https://opensky-network.org/api"
AIRLABS_BASE = "https://airlabs.co/api/v9"

# Airport coordinates (IATA code -> lat, lon)
AIRPORT_COORDS = {
    "SEA": (47.4502, -122.3088),
    "ONT": (34.0560, -117.6012),
    "LAX": (33.9425, -118.4081),
    "SFO": (37.6213, -122.3790),
    "JFK": (40.6413, -73.7781),
    "ORD": (41.9742, -87.9073),
    "DFW": (32.8998, -97.0403),
    "ATL": (33.6407, -84.4277),
    "DEN": (39.8561, -104.6737),
    "PHX": (33.4373, -112.0078),
    "LAS": (36.0840, -115.1537),
    "PDX": (45.5898, -122.5951),
    "SAN": (32.7338, -117.1933),
    "BOS": (42.3656, -71.0096),
    "MSP": (44.8848, -93.2223),
    "EWR": (40.6895, -74.1745),
    "IAD": (38.9531, -77.4565),
    "MIA": (25.7959, -80.2870),
}

# Airline IATA -> ICAO callsign prefix
AIRLINE_CALLSIGN = {
    "AS": "ASA", "AA": "AAL", "DL": "DAL", "UA": "UAL",
    "WN": "SWA", "B6": "JBU", "NK": "NKS", "F9": "FFT",
    "HA": "HAL", "SY": "SCX", "QX": "QXE", "OO": "SKW",
    "G4": "AAY", "MX": "MXA",
    "LH": "DLH", "AI": "AIC", "SQ": "SIA", "EK": "UAE",
    "QR": "QTR", "KL": "KLM", "TG": "THA", "NH": "ANA",
    "BA": "BAW", "AF": "AFR", "TK": "THY", "EY": "ETD",
    "CX": "CPA", "JL": "JAL", "6E": "IGO", "IX": "AXB",
}


def iata_to_callsign(flight_iata):
    """Convert IATA flight code (e.g. AS594) to ICAO callsign (e.g. ASA594)."""
    for prefix_len in (2, 3):
        airline = flight_iata[:prefix_len]
        number = flight_iata[prefix_len:]
        if airline in AIRLINE_CALLSIGN and number.isdigit():
            return AIRLINE_CALLSIGN[airline] + number
    return flight_iata


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two points in km."""
    R = 6371.0
    rlat1, rlat2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_flight_opensky(callsign):
    """Query OpenSky Network (free, no key). Returns normalized flight dict."""
    # Pad callsign to 8 chars for OpenSky matching
    url = f"{OPENSKY_BASE}/states/all?callsign={callsign}"
    try:
        req = Request(url, headers={"User-Agent": "OpenClaw-FlightTracker/1.0"})
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
    except (URLError, json.JSONDecodeError) as e:
        return None, str(e)

    states = data.get("states")
    if not states:
        return None, "Flight not found or not airborne"

    # State vector: [icao24, callsign, origin_country, time_position, last_contact,
    #   longitude, latitude, baro_altitude, on_ground, velocity,
    #   true_track, vertical_rate, sensors, geo_altitude, squawk, spi, position_source]
    s = states[0]
    return {
        "lat": s[6],
        "lng": s[5],
        "alt": s[7],            # meters (barometric)
        "on_ground": s[8],
        "speed": round(s[9] * 3.6, 1) if s[9] else 0,  # m/s -> km/h
        "dir": s[10],
        "v_speed": s[11],       # m/s (positive=climbing, negative=descending)
        "updated": s[4],
    }, None


def get_flight_airlabs(api_key, flight_iata):
    """Query AirLabs (needs key). Returns normalized flight dict."""
    url = f"{AIRLABS_BASE}/flights?flight_iata={flight_iata}&api_key={api_key}"
    try:
        req = Request(url, headers={"User-Agent": "OpenClaw-FlightTracker/1.0"})
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except (URLError, json.JSONDecodeError) as e:
        return None, str(e)

    if not data.get("response"):
        return None, "Flight not found or not airborne"

    r = data["response"][0]
    return {
        "lat": r.get("lat"),
        "lng": r.get("lng"),
        "alt": r.get("alt"),
        "on_ground": r.get("status") == "landed",
        "speed": r.get("speed", 0),
        "dir": r.get("dir"),
        "v_speed": r.get("v_speed", 0),
        "updated": r.get("updated"),
    }, None


def get_flight(flight_iata, api_key=None):
    """Try OpenSky first (free), fall back to AirLabs."""
    callsign = iata_to_callsign(flight_iata)
    data, err = get_flight_opensky(callsign)
    if data:
        return data, None

    if api_key:
        data, err2 = get_flight_airlabs(api_key, flight_iata)
        if data:
            return data, None
        return None, f"OpenSky: {err}; AirLabs: {err2}"

    return None, f"OpenSky: {err}; no AirLabs key"


def assess_flight(flight_data, dest_coords, origin_coords=None):
    """Assess flight phase and ETA relative to destination.
    If origin_coords provided, reject flights too far from the origin-dest corridor."""
    lat = flight_data.get("lat")
    lng = flight_data.get("lng")
    alt = flight_data.get("alt")
    v_speed = flight_data.get("v_speed") or 0
    speed = flight_data.get("speed") or 0
    on_ground = flight_data.get("on_ground", False)

    if on_ground:
        return {"phase": "landed", "distance_km": 0, "eta_min": 0}

    if lat is None or lng is None:
        return {"phase": "unknown", "distance_km": None, "eta_min": None}

    distance_km = haversine_km(lat, lng, dest_coords[0], dest_coords[1])

    # Route sanity check: reject if flight is way off the origin-dest corridor
    if origin_coords:
        route_dist = haversine_km(origin_coords[0], origin_coords[1], dest_coords[0], dest_coords[1])
        dist_from_origin = haversine_km(lat, lng, origin_coords[0], origin_coords[1])
        # Flight should be within 2x the route distance from either endpoint
        max_reasonable = max(route_dist * 2, 1000)  # at least 1000 km tolerance
        if dist_from_origin > max_reasonable and distance_km > max_reasonable:
            return {"phase": "wrong-flight", "distance_km": distance_km,
                    "eta_min": None, "note": f"Aircraft is {dist_from_origin:.0f} km from origin, likely a different rotation"}

    # Estimate ETA from speed + distance
    eta_min = None
    if speed > 0:
        eta_min = round((distance_km / speed) * 60)

    # Classify phase
    if distance_km < 50:
        phase = "final_approach"
    elif distance_km < 150 and v_speed < -2:
        phase = "descending_close"
    elif distance_km < 300:
        phase = "approaching"
    else:
        phase = "en-route"

    return {
        "phase": phase,
        "distance_km": round(distance_km, 1),
        "eta_min": eta_min,
        "alt_m": alt,
        "v_speed_ms": v_speed,
        "lat": lat,
        "lng": lng,
        "speed_kmh": speed,
    }


def main():
    parser = argparse.ArgumentParser(description="Track a flight to destination")
    parser.add_argument("--flight", required=True, help="IATA flight code, e.g. AS594")
    parser.add_argument("--dest", required=True, help="Destination airport IATA, e.g. SEA")
    parser.add_argument("--origin", help="Origin airport IATA, e.g. ONT (for route sanity check)")
    parser.add_argument("--api-key", default=os.environ.get("AIRLABS_API_KEY", ""),
                        help="AirLabs API key (optional fallback)")
    parser.add_argument("--poll-interval", type=int, default=300,
                        help="Seconds between polls (default 300 = 5 min)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Single check, print JSON status, exit")
    args = parser.parse_args()

    flight_code = args.flight.upper()
    dest = args.dest.upper()

    if dest not in AIRPORT_COORDS:
        print(json.dumps({"error": f"Unknown destination airport: {dest}"}))
        sys.exit(1)

    dest_coords = AIRPORT_COORDS[dest]
    origin_coords = None
    if args.origin:
        origin = args.origin.upper()
        if origin in AIRPORT_COORDS:
            origin_coords = AIRPORT_COORDS[origin]
        else:
            print(json.dumps({"error": f"Unknown origin airport: {origin}"}), file=sys.stderr)

    if args.dry_run:
        data, err = get_flight(flight_code, args.api_key or None)
        if err:
            print(json.dumps({"error": err, "flight": flight_code, "status": "not-found", "note": "Flight may not have departed yet"}))
            sys.exit(0)
        result = assess_flight(data, dest_coords, origin_coords)
        if result["phase"] == "wrong-flight":
            print(json.dumps({"flight": flight_code, "status": "not-departed", "note": result["note"], "destination": dest}))
            sys.exit(0)
        result["flight"] = flight_code
        result["destination"] = dest
        print(json.dumps(result, indent=2))
        sys.exit(0)

    # Polling loop
    print(f"Tracking {flight_code} -> {dest} every {args.poll_interval}s", file=sys.stderr)
    while True:
        data, err = get_flight(flight_code, args.api_key or None)
        now = time.strftime("%H:%M:%S")

        if err:
            print(f"[{now}] Waiting... ({err})", file=sys.stderr)
            time.sleep(args.poll_interval)
            continue

        assessment = assess_flight(data, dest_coords, origin_coords)
        phase = assessment["phase"]
        if phase == "wrong-flight":
            print(f"[{now}] Wrong flight detected ({assessment.get('note', '')}), waiting...", file=sys.stderr)
            time.sleep(args.poll_interval)
            continue
        dist = assessment.get("distance_km", "?")
        eta = assessment.get("eta_min", "?")

        print(f"[{now}] {phase} | {dist} km | ETA ~{eta} min | alt={assessment.get('alt_m')}m",
              file=sys.stderr)

        # Output JSON events for landed or close approach
        if phase == "landed":
            print(json.dumps({"event": "landed", "flight": flight_code, "destination": dest}))
            sys.exit(0)

        if phase in ("final_approach", "descending_close"):
            print(json.dumps({
                "event": "approaching",
                "flight": flight_code,
                "destination": dest,
                "distance_km": dist,
                "eta_min": eta,
                "phase": phase,
            }))
            # Poll faster when close
            time.sleep(60)
        else:
            time.sleep(args.poll_interval)


if __name__ == "__main__":
    main()
