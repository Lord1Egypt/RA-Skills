#!/usr/bin/env python3
"""
Flight schedule checker - find flights between airports

Usage:
    python3 schedule.py SIN HKG
    python3 schedule.py --from SIN --to HKG
    python3 schedule.py --from SIN --to TFU --countdown
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo


RED_BOLD = "\033[1;31m"
RESET = "\033[0m"


AIRPORTS = {
    "SIN": "Singapore Changi",
    "KUL": "Kuala Lumpur International",
    "PEN": "Penang International",
    "CGK": "Jakarta Soekarno-Hatta",
    "DPS": "Bali Denpasar",
    "BKK": "Bangkok Suvarnabhumi",
    "SGN": "Ho Chi Minh City Tan Son Nhat",
    "HAN": "Hanoi Noi Bai",
    "MNL": "Manila Ninoy Aquino",
    "HKG": "Hong Kong International",
    "TPE": "Taipei Taoyuan",
    "PEK": "Beijing Capital",
    "PKX": "Beijing Daxing",
    "PVG": "Shanghai Pudong",
    "SHA": "Shanghai Hongqiao",
    "CAN": "Guangzhou Baiyun",
    "SZX": "Shenzhen Bao'an",
    "CTU": "Chengdu Shuangliu",
    "TFU": "Chengdu Tianfu",
    "NRT": "Tokyo Narita",
    "HND": "Tokyo Haneda",
    "KIX": "Osaka Kansai",
    "ICN": "Seoul Incheon",
    "DEL": "Delhi Indira Gandhi",
    "BOM": "Mumbai Chhatrapati Shivaji",
    "BLR": "Bangalore Kempegowda",
    "HYD": "Hyderabad Rajiv Gandhi",
    "MAA": "Chennai International",
    "CCU": "Kolkata Netaji Subhas Chandra Bose",
    "SYD": "Sydney Kingsford Smith",
    "MEL": "Melbourne Tullamarine",
    "BNE": "Brisbane",
    "PER": "Perth",
    "AKL": "Auckland International",
    "SFO": "San Francisco International",
    "LAX": "Los Angeles International",
    "JFK": "New York JFK",
}

AIRPORT_TZ = {
    "SIN": "Asia/Singapore",
    "KUL": "Asia/Kuala_Lumpur",
    "PEN": "Asia/Kuala_Lumpur",
    "CGK": "Asia/Jakarta",
    "DPS": "Asia/Makassar",
    "BKK": "Asia/Bangkok",
    "SGN": "Asia/Ho_Chi_Minh",
    "HAN": "Asia/Ho_Chi_Minh",
    "MNL": "Asia/Manila",
    "HKG": "Asia/Hong_Kong",
    "TPE": "Asia/Taipei",
    "PEK": "Asia/Shanghai",
    "PKX": "Asia/Shanghai",
    "PVG": "Asia/Shanghai",
    "SHA": "Asia/Shanghai",
    "CAN": "Asia/Shanghai",
    "SZX": "Asia/Shanghai",
    "CTU": "Asia/Shanghai",
    "TFU": "Asia/Shanghai",
    "NRT": "Asia/Tokyo",
    "HND": "Asia/Tokyo",
    "KIX": "Asia/Tokyo",
    "ICN": "Asia/Seoul",
    "DEL": "Asia/Kolkata",
    "BOM": "Asia/Kolkata",
    "BLR": "Asia/Kolkata",
    "HYD": "Asia/Kolkata",
    "MAA": "Asia/Kolkata",
    "CCU": "Asia/Kolkata",
    "SYD": "Australia/Sydney",
    "MEL": "Australia/Melbourne",
    "BNE": "Australia/Brisbane",
    "PER": "Australia/Perth",
    "AKL": "Pacific/Auckland",
    "SFO": "America/Los_Angeles",
    "LAX": "America/Los_Angeles",
    "JFK": "America/New_York",
}

AIRLINE_BADGES = {
    "Singapore Airlines": "🇸🇬 [SIA]",
    "Scoot": "🇸🇬 [TR]",
    "Sichuan Airlines": "🇨🇳 [3U]",
    "Air China": "🇨🇳 [CA]",
    "Air China LTD": "🇨🇳 [CA]",
    "China Southern Airlines": "🇨🇳 [CZ]",
    "China Eastern Airlines": "🇨🇳 [MU]",
    "Cathay Pacific": "🇭🇰 [CX]",
    "Hong Kong Airlines": "🇭🇰 [HX]",
    "HK Express": "🇭🇰 [UO]",
    "Malaysia Airlines": "🇲🇾 [MH]",
    "Batik Air Malaysia": "🇲🇾 [OD]",
    "AirAsia": "🇲🇾 [AK]",
    "Indonesia AirAsia": "🇮🇩 [QZ]",
    "Thai Airways": "🇹🇭 [TG]",
    "Vietnam Airlines": "🇻🇳 [VN]",
    "Philippine Airlines": "🇵🇭 [PR]",
    "Japan Airlines": "🇯🇵 [JL]",
    "All Nippon Airways": "🇯🇵 [NH]",
    "ANA": "🇯🇵 [NH]",
    "Korean Air": "🇰🇷 [KE]",
    "Asiana Airlines": "🇰🇷 [OZ]",
    "Qantas": "🇦🇺 [QF]",
    "Jetstar": "🇦🇺 [JQ]",
    "Air New Zealand": "🇳🇿 [NZ]",
    "IndiGo": "🇮🇳 [6E]",
    "Air India": "🇮🇳 [AI]",
    "Vistara": "🇮🇳 [UK]",
    "United Airlines": "🇺🇸 [UA]",
    "American Airlines": "🇺🇸 [AA]",
    "Delta Air Lines": "🇺🇸 [DL]",
}

NORMAL_STATUSES = {"scheduled", "active", "landed", "departed"}


def get_airport_zone(code):
    tz_name = AIRPORT_TZ.get((code or "").upper())
    return ZoneInfo(tz_name) if tz_name else timezone.utc


def get_airport_tz_abbr(code, dt=None):
    zone = get_airport_zone(code)
    sample = dt.astimezone(zone) if dt else datetime.now(zone)
    return sample.strftime("%Z")


def parse_iso_raw(time_str):
    """Parse timestamp normally, respecting any embedded offset."""
    try:
        if not time_str:
            return None
        if "T" in str(time_str):
            return datetime.fromisoformat(str(time_str).replace("Z", "+00:00"))
        return None
    except Exception:
        return None


def parse_local_wall_time(time_str, airport_code):
    """
    Treat API timestamp as local wall-clock time for the airport,
    ignoring any embedded offset.
    This fixes routes where the API offset is wrong but the local clock time is right.
    """
    if not time_str:
        return None

    text = str(time_str).strip()
    try:
        # Take only YYYY-MM-DDTHH:MM:SS part, ignore timezone suffix if present
        base = text[:19]
        naive = datetime.fromisoformat(base)
        return naive.replace(tzinfo=get_airport_zone(airport_code))
    except Exception:
        return None


def best_airport_dt(time_str, airport_code):
    """
    Prefer local wall-time interpretation.
    Fall back to raw ISO if needed, then convert to airport timezone.
    """
    dt = parse_local_wall_time(time_str, airport_code)
    if dt:
        return dt

    raw = parse_iso_raw(time_str)
    if raw:
        if raw.tzinfo is None:
            raw = raw.replace(tzinfo=timezone.utc)
        return raw.astimezone(get_airport_zone(airport_code))

    return None


def format_time_with_label(time_str, airport_code):
    dt = best_airport_dt(time_str, airport_code)
    if not dt:
        return "N/A"
    return dt.strftime("%d-%b-%Y %H:%M %Z")


def format_date_only(time_str, airport_code):
    dt = best_airport_dt(time_str, airport_code)
    if dt:
        return dt.strftime("%d-%b-%Y")
    return "Unknown Date"


def format_duration_minutes(minutes):
    if minutes is None or minutes < 0:
        return "N/A"
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"


def get_aviationstack_schedule(origin, dest, api_key):
    base_url = "https://api.aviationstack.com/v1/flights"
    params = {
        "access_key": api_key,
        "dep_iata": origin,
        "arr_iata": dest,
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as e:
        print(f"API Error: HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"API Error: {e}", file=sys.stderr)
        return None


def remove_codeshares(flights):
    return [f for f in flights if f.get("flight", {}).get("codeshared") is None]


def get_flight_code(flight):
    flight_info = flight.get("flight", {})
    return (
        flight_info.get("iata")
        or flight_info.get("icao")
        or flight_info.get("number")
        or "N/A"
    )


def get_airline_name(flight):
    return flight.get("airline", {}).get("name", "Unknown")


def get_airline_display_name(flight):
    airline = get_airline_name(flight)
    badge = AIRLINE_BADGES.get(airline, "✈️")
    return f"{badge} {airline}"


def deduplicate_flights(flights):
    seen = set()
    unique = []
    for flight in flights:
        key = (
            get_airline_name(flight),
            get_flight_code(flight),
            flight.get("departure", {}).get("scheduled", "N/A"),
        )
        if key not in seen:
            seen.add(key)
            unique.append(flight)
    return unique


def sort_flights_by_departure(flights, origin):
    def sort_key(flight):
        dt = best_airport_dt(flight.get("departure", {}).get("scheduled"), origin)
        return (dt is None, dt or datetime.max.replace(tzinfo=get_airport_zone(origin)))
    return sorted(flights, key=sort_key)


def get_aircraft_display(flight):
    aircraft = flight.get("aircraft", {}) if isinstance(flight.get("aircraft"), dict) else {}
    live = flight.get("live", {}) if isinstance(flight.get("live"), dict) else {}

    for key in ("type", "iata", "icao"):
        val = aircraft.get(key)
        if val:
            return str(val).strip()

    val = live.get("aircraft")
    if val:
        return str(val).strip()

    reg = aircraft.get("registration") or live.get("registration")
    if reg:
        return f"Reg {str(reg).strip()}"

    icao24 = aircraft.get("icao24") or live.get("icao24")
    if icao24:
        return f"ICAO24 {str(icao24).strip()}"

    return "Unknown"


def get_delay_minutes(flight):
    dep_delay = flight.get("departure", {}).get("delay")
    arr_delay = flight.get("arrival", {}).get("delay")
    if isinstance(dep_delay, (int, float)):
        return int(dep_delay)
    if isinstance(arr_delay, (int, float)):
        return int(arr_delay)
    return None


def format_delay(delay_minutes):
    return f"{delay_minutes} min" if delay_minutes is not None else "N/A"


def choose_best_departure_dt(flight, origin):
    dep = flight.get("departure", {})
    return (
        best_airport_dt(dep.get("actual"), origin)
        or best_airport_dt(dep.get("estimated"), origin)
        or best_airport_dt(dep.get("scheduled"), origin)
    )


def choose_best_arrival_dt(flight, dest):
    arr = flight.get("arrival", {})
    return (
        best_airport_dt(arr.get("actual"), dest)
        or best_airport_dt(arr.get("estimated"), dest)
        or best_airport_dt(arr.get("scheduled"), dest)
    )


def get_flight_time(flight, origin, dest):
    """
    Real/latest operating duration.
    If arrival local time appears earlier than departure in absolute terms due to date weirdness,
    roll arrival forward by 1 day until sensible.
    """
    dep_dt = choose_best_departure_dt(flight, origin)
    arr_dt = choose_best_arrival_dt(flight, dest)

    if not dep_dt or not arr_dt:
        return "N/A"

    while arr_dt <= dep_dt:
        arr_dt += timedelta(days=1)

    minutes = int((arr_dt.astimezone(timezone.utc) - dep_dt.astimezone(timezone.utc)).total_seconds() // 60)
    return format_duration_minutes(minutes)


def get_scheduled_duration(flight, origin, dest):
    """
    Timetable duration using airport-local wall times.
    This is the key fix for routes like SIN-LAX where the API offset is unreliable.
    """
    dep_dt = best_airport_dt(flight.get("departure", {}).get("scheduled"), origin)
    arr_dt = best_airport_dt(flight.get("arrival", {}).get("scheduled"), dest)

    if not dep_dt or not arr_dt:
        return "N/A"

    while arr_dt <= dep_dt:
        arr_dt += timedelta(days=1)

    minutes = int((arr_dt.astimezone(timezone.utc) - dep_dt.astimezone(timezone.utc)).total_seconds() // 60)
    return format_duration_minutes(minutes)


def derive_display_status(flight, dest):
    raw_status = str(flight.get("flight_status", "")).strip().lower()

    dep_actual = parse_iso_raw(flight.get("departure", {}).get("actual"))
    arr_actual = parse_iso_raw(flight.get("arrival", {}).get("actual"))
    arr_est = best_airport_dt(flight.get("arrival", {}).get("estimated"), dest)
    now = datetime.now(get_airport_zone(dest))

    if arr_actual:
        return "Landed"

    if dep_actual:
        if arr_est and arr_est < now:
            return "Likely Landed"
        return "Departed"

    if raw_status:
        return raw_status.title()

    return "Unknown"


def format_status(status):
    raw = str(status).strip()
    if raw.lower() in NORMAL_STATUSES:
        return raw.title()
    return f"{RED_BOLD}{raw.title()}{RESET}"


def format_countdown(time_str, origin):
    dt = best_airport_dt(time_str, origin)
    if not dt:
        return "N/A"

    now = datetime.now(get_airport_zone(origin))
    diff = dt - now
    total_seconds = int(diff.total_seconds())

    if total_seconds < 0:
        mins_ago = abs(total_seconds) // 60
        hours = mins_ago // 60
        mins = mins_ago % 60
        return f"Departed {hours}h {mins}m ago" if hours > 0 else f"Departed {mins}m ago"

    mins_left = total_seconds // 60
    days = mins_left // (24 * 60)
    hours = (mins_left % (24 * 60)) // 60
    mins = mins_left % 60

    if days > 0:
        return f"In {days}d {hours}h {mins}m"
    if hours > 0:
        return f"In {hours}h {mins}m"
    return f"In {mins}m"


def group_flights_by_departure_date(flights, origin):
    grouped = {}
    for flight in flights:
        dep_time = flight.get("departure", {}).get("scheduled")
        key = format_date_only(dep_time, origin)
        grouped.setdefault(key, []).append(flight)
    return grouped


def print_time_block(label, scheduled, estimated, actual, airport_code):
    print(f"  {label} Scheduled: {format_time_with_label(scheduled, airport_code)}")
    if estimated:
        print(f"  {label} Estimated: {format_time_with_label(estimated, airport_code)}")
    if actual:
        print(f"  {label} Actual:    {format_time_with_label(actual, airport_code)}")


def print_flight_block(flight, origin, dest, show_countdown=False):
    dep = flight.get("departure", {})
    arr = flight.get("arrival", {})

    dep_sched = dep.get("scheduled")
    dep_est = dep.get("estimated")
    dep_actual = dep.get("actual")

    arr_sched = arr.get("scheduled")
    arr_est = arr.get("estimated")
    arr_actual = arr.get("actual")

    dep_terminal = dep.get("terminal", "")
    dep_gate = dep.get("gate", "")
    arr_terminal = arr.get("terminal", "")
    arr_gate = arr.get("gate", "")

    airline_display = get_airline_display_name(flight)
    flight_code = get_flight_code(flight)

    dep_tz = get_airport_tz_abbr(origin)
    arr_tz = get_airport_tz_abbr(dest)

    aircraft_display = get_aircraft_display(flight)
    delay_minutes = get_delay_minutes(flight)
    flight_time = get_flight_time(flight, origin, dest)
    scheduled_duration = get_scheduled_duration(flight, origin, dest)
    display_status = derive_display_status(flight, dest)

    print(f"\n{airline_display} {flight_code}")
    print(f"  Timezones:   {dep_tz} → {arr_tz}")

    print_time_block("Departure", dep_sched, dep_est, dep_actual, origin)
    if dep_terminal:
        gate_text = f", Gate {dep_gate}" if dep_gate else ""
        print(f"  Departure:   Terminal {dep_terminal}{gate_text}")

    print_time_block("Arrival", arr_sched, arr_est, arr_actual, dest)
    if arr_terminal:
        gate_text = f", Gate {arr_gate}" if arr_gate else ""
        print(f"  Arrival:     Terminal {arr_terminal}{gate_text}")

    print(f"  Flight Time:        {flight_time}")
    print(f"  Scheduled Duration: {scheduled_duration}")
    print(f"  Aircraft:           {aircraft_display}")
    print(f"  Delay:              {format_delay(delay_minutes)}")
    print(f"  Status:             {format_status(display_status)}")

    if show_countdown:
        print(f"  Countdown:          {format_countdown(dep_actual or dep_est or dep_sched, origin)}")


def print_aviationstack_results(data, origin, dest, show_countdown=False):
    if not data or "data" not in data:
        print("No flight data available.")
        return

    flights = data["data"]
    if not flights:
        print(f"No flights found from {origin} to {dest}.")
        return

    filtered = remove_codeshares(flights)
    if filtered:
        flights = filtered

    flights = deduplicate_flights(flights)
    flights = sort_flights_by_departure(flights, origin)

    origin_name = AIRPORTS.get(origin, origin)
    dest_name = AIRPORTS.get(dest, dest)

    print(f"\n✈️  Flight Search: {origin_name} ({origin}) → {dest_name} ({dest})")
    print(f"📊 Found {len(flights)} operating flight(s)\n")
    print("=" * 100)

    grouped = group_flights_by_departure_date(flights, origin)
    for group_date, group_flights in grouped.items():
        print(f"\n📅 {group_date}")
        print("-" * 100)
        for flight in group_flights:
            print_flight_block(flight, origin, dest, show_countdown=show_countdown)

    print("\n" + "=" * 100)


def show_manual_options(origin, dest):
    origin_name = AIRPORTS.get(origin, origin)
    dest_name = AIRPORTS.get(dest, dest)

    print(f"\n✈️  Flight Search: {origin_name} ({origin}) → {dest_name} ({dest})")
    print("\n⚠️  No API key configured.\n")

    google_url = f"https://www.google.com/travel/flights?q=Flights%20from%20{origin}%20to%20{dest}"
    print("Google Flights:")
    print(google_url)
    print()

    fr24_url = f"https://www.flightradar24.com/data/flights/{origin.lower()}-{dest.lower()}"
    print("FlightRadar24:")
    print(fr24_url)
    print()


def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Check flights between airports")
    parser.add_argument("origin", nargs="?", help="Origin airport (IATA code)")
    parser.add_argument("destination", nargs="?", help="Destination airport (IATA code)")
    parser.add_argument("--from", dest="from_airport", help="Origin airport")
    parser.add_argument("--to", dest="to_airport", help="Destination airport")
    parser.add_argument("--countdown", action="store_true", help="Show countdown to departure")

    args = parser.parse_args()

    origin = (args.origin or args.from_airport or "").upper()
    dest = (args.destination or args.to_airport or "").upper()

    if not origin or not dest:
        print("Usage:")
        print("  python3 schedule.py SIN HKG")
        print("  python3 schedule.py --from SIN --to HKG")
        print("  python3 schedule.py --from SIN --to TFU --countdown")
        print(f"\nSupported airports: {', '.join(sorted(AIRPORTS.keys()))}")
        sys.exit(1)

    api_key = os.environ.get("AVIATIONSTACK_API_KEY")

    if api_key:
        data = get_aviationstack_schedule(origin, dest, api_key)
        print_aviationstack_results(data, origin, dest, show_countdown=args.countdown)
    else:
        show_manual_options(origin, dest)


if __name__ == "__main__":
    main()
