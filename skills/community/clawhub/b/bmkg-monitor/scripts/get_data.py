#!/usr/bin/env python3
import requests
import sys
import json
import xml.etree.ElementTree as ET

BASE_URL = "https://data.bmkg.go.id/DataMKG/TEWS/"
SHAKEMAP_BASE = "https://data.bmkg.go.id/DataMKG/TEWS/"
WEATHER_API = "https://api.bmkg.go.id/publik/prakiraan-cuaca"
WARNINGS_URL = "https://www.bmkg.go.id/alerts/nowcast/id"


def error_exit(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def fetch_json(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_exit(str(e))


def fetch_text(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        error_exit(str(e))


def fetch_bmkg(endpoint):
    return fetch_json(BASE_URL + endpoint)


def format_gempa(g):
    lines = [
        f"Time: {g.get('Tanggal')} {g.get('Jam')}",
        f"Magnitude: {g.get('Magnitude')}",
        f"Depth: {g.get('Kedalaman')}",
        f"Location: {g.get('Wilayah')}",
        f"Coords: {g.get('Coordinates')}",
        f"Potensi: {g.get('Potensi', 'N/A')}",
        f"Felt: {g.get('Dirasakan', 'N/A')}",
    ]
    shakemap = g.get("Shakemap")
    if shakemap:
        lines.append(f"Shakemap: {SHAKEMAP_BASE}{shakemap}")
    return "\n".join(lines)


def cmd_latest(raw_json):
    data = fetch_bmkg("autogempa.json")
    g = data.get("Infogempa", {}).get("gempa", {})
    if raw_json:
        print(json.dumps(g, indent=2, ensure_ascii=False))
        return
    print("--- LATEST SIGNIFICANT EARTHQUAKE (M5.0+) ---")
    print(format_gempa(g))
    dt = g.get("DateTime", "")
    if dt:
        print("\n[TIP] Check detailed static reports if available:")
        print("- History: https://static.bmkg.go.id/history.<EVENT_ID>.txt")
        print("- Moment Tensor: https://static.bmkg.go.id/mt.<EVENT_ID>.txt")


def cmd_detail(args, raw_json):
    if not args:
        error_exit("Usage: get_data.py detail <EVENT_ID>")
    eid = args[0]
    if raw_json:
        history = fetch_text(f"https://static.bmkg.go.id/history.{eid}.txt")
        mt = fetch_text(f"https://static.bmkg.go.id/mt.{eid}.txt")
        print(json.dumps({"event_id": eid, "moment_tensor": mt, "history": history}, indent=2, ensure_ascii=False))
        return
    history = fetch_text(f"https://static.bmkg.go.id/history.{eid}.txt")
    mt = fetch_text(f"https://static.bmkg.go.id/mt.{eid}.txt")
    print(f"--- DETAILED DATA FOR EVENT: {eid} ---")
    print("\n[MOMENT TENSOR]")
    print(mt)
    print("\n[HISTORY/PHASES]")
    print(history)


def cmd_felt(raw_json):
    data = fetch_bmkg("gempadirasakan.json")
    list_g = data.get("Infogempa", {}).get("gempa", [])
    if raw_json:
        print(json.dumps(list_g[:5], indent=2, ensure_ascii=False))
        return
    print("--- LATEST FELT EARTHQUAKES ---")
    for g in list_g[:5]:
        print(format_gempa(g))
        print("-" * 40)


def cmd_recent(raw_json):
    data = fetch_bmkg("gempaterkini.json")
    list_g = data.get("Infogempa", {}).get("gempa", [])
    if raw_json:
        print(json.dumps(list_g[:5], indent=2, ensure_ascii=False))
        return
    print("--- RECENT EARTHQUAKES (M5.0+) ---")
    for g in list_g[:5]:
        print(format_gempa(g))
        print("-" * 40)


def cmd_weather(args, raw_json):
    if not args:
        error_exit("Usage: get_data.py weather <adm4_code>")
    adm4_code = args[0]
    data = fetch_json(f"{WEATHER_API}?adm4={adm4_code}")

    if raw_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    lokasi = data.get("lokasi", {})
    loc_parts = [lokasi.get("desa"), lokasi.get("kecamatan"), lokasi.get("kotkab"), lokasi.get("provinsi")]
    loc_name = ", ".join(p for p in loc_parts if p)

    print(f"--- WEATHER FORECAST: {loc_name or adm4_code} ---")

    cuaca_list = data.get("data", [])
    forecasts_shown = 0
    for group in cuaca_list:
        for entry in group.get("cuaca", []):
            for fc in entry:
                if forecasts_shown >= 3:
                    break
                local_time = fc.get("local_datetime", fc.get("datetime", "N/A"))
                temp = fc.get("t", "N/A")
                humidity = fc.get("hu", "N/A")
                condition = fc.get("weather_desc_id", fc.get("weather_desc", "N/A"))
                wind_speed = fc.get("ws", "N/A")
                wind_dir = fc.get("wd_to", fc.get("wd", "N/A"))
                visibility = fc.get("vs_text", fc.get("vs", "N/A"))

                print(f"\n  Time: {local_time}")
                print(f"  Temperature: {temp}°C")
                print(f"  Humidity: {humidity}%")
                print(f"  Condition: {condition}")
                print(f"  Wind: {wind_speed} km/h {wind_dir}")
                print(f"  Visibility: {visibility}")
                print("-" * 40)
                forecasts_shown += 1
            if forecasts_shown >= 3:
                break
        if forecasts_shown >= 3:
            break

    if forecasts_shown == 0:
        print("No forecast data available.")


def cmd_warnings(raw_json):
    text = fetch_text(WARNINGS_URL)
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        error_exit(f"Failed to parse warnings XML: {e}")

    channel = root.find("channel")
    if channel is None:
        channel = root

    items = channel.findall("item")
    if not items:
        if raw_json:
            print(json.dumps([], indent=2))
        else:
            print("--- ACTIVE WEATHER WARNINGS ---")
            print("No active warnings.")
        return

    warnings = []
    for item in items[:10]:
        title = item.findtext("title", "N/A")
        desc = item.findtext("description", "N/A")
        pub_date = item.findtext("pubDate", "N/A")
        warnings.append({"title": title, "description": desc, "pubDate": pub_date})

    if raw_json:
        print(json.dumps(warnings, indent=2, ensure_ascii=False))
        return

    print("--- ACTIVE WEATHER WARNINGS ---")
    for w in warnings:
        print(f"\n  Title: {w['title']}")
        print(f"  Date: {w['pubDate']}")
        print(f"  Description: {w['description']}")
        print("-" * 40)


def cmd_tsunami(raw_json):
    auto = fetch_bmkg("autogempa.json")
    recent = fetch_bmkg("gempaterkini.json")

    latest = auto.get("Infogempa", {}).get("gempa", {})
    recent_list = recent.get("Infogempa", {}).get("gempa", [])

    def has_tsunami_potential(potensi):
        p = (potensi or "").lower()
        return "tsunami" in p and "tidak" not in p

    results = []
    if latest and has_tsunami_potential(latest.get("Potensi")):
        results.append(latest)
    for g in recent_list:
        if has_tsunami_potential(g.get("Potensi")):
            results.append(g)

    if raw_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    print("--- EARTHQUAKES WITH TSUNAMI POTENTIAL ---")
    if not results:
        print("No earthquakes with tsunami potential found.")
        return
    for g in results:
        print(format_gempa(g))
        print("-" * 40)


def cmd_shakemap(raw_json):
    data = fetch_bmkg("autogempa.json")
    g = data.get("Infogempa", {}).get("gempa", {})
    shakemap = g.get("Shakemap")

    if raw_json:
        result = {
            "shakemap_file": shakemap,
            "shakemap_url": f"{SHAKEMAP_BASE}{shakemap}" if shakemap else None,
            "earthquake": g,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("--- SHAKEMAP (LATEST EARTHQUAKE) ---")
    print(format_gempa(g))
    if shakemap:
        print(f"\nShakemap URL: {SHAKEMAP_BASE}{shakemap}")
    else:
        print("\nNo shakemap available for this event.")


def cmd_help():
    print("""BMKG Monitor - Indonesian Meteorology & Geophysics Data

Usage: get_data.py <command> [args] [--json]

Commands:
  latest              Latest significant earthquake (M5.0+)
  felt                Recent earthquakes felt by people
  recent              Recent M5.0+ earthquakes
  detail <EVENT_ID>   Detailed moment tensor & phase data for an event
  weather <ADM4_CODE> Weather forecast for a location (next 3 periods)
  warnings            Active weather warnings (top 10)
  tsunami             Earthquakes with tsunami potential
  shakemap            Shakemap URL for the latest earthquake
  help                Show this help message

Options:
  --json              Output raw JSON (append as last argument)

Examples:
  get_data.py latest
  get_data.py weather 35.07.01.1001
  get_data.py felt --json
  get_data.py detail 20250101_EVENT_ID""")


def main():
    argv = sys.argv[1:]

    raw_json = False
    if argv and argv[-1] == "--json":
        raw_json = True
        argv = argv[:-1]

    mode = argv[0] if argv else "help"
    args = argv[1:]

    if mode == "help":
        cmd_help()
    elif mode == "latest":
        cmd_latest(raw_json)
    elif mode == "detail":
        cmd_detail(args, raw_json)
    elif mode == "felt":
        cmd_felt(raw_json)
    elif mode == "recent":
        cmd_recent(raw_json)
    elif mode == "weather":
        cmd_weather(args, raw_json)
    elif mode == "warnings":
        cmd_warnings(raw_json)
    elif mode == "tsunami":
        cmd_tsunami(raw_json)
    elif mode == "shakemap":
        cmd_shakemap(raw_json)
    else:
        print(f"Unknown command: {mode}", file=sys.stderr)
        cmd_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
