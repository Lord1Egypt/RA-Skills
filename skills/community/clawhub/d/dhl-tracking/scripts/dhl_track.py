#!/usr/bin/env python3
"""DHL Sendungsverfolgung - parse tracking JSON into human-readable summary.

Usage: 
  ./dhl_track.sh <TRACKING_NUMBER> | python3 dhl_track.py
  python3 dhl_track.py <TRACKING_NUMBER>
"""
import sys, json, subprocess
from datetime import datetime

def fetch_tracking(tracking_number: str, lang: str = "de") -> dict:
    """Fetch tracking data from DHL nolp API."""
    import urllib.request
    url = f"https://www.dhl.de/int-verfolgen/data/search?piececode={tracking_number}&language={lang}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def parse_tracking(data: dict) -> dict:
    """Parse DHL tracking JSON into a clean summary."""
    if not data.get("sendungen"):
        return {"error": "Keine Sendung gefunden", "raw": data}
    
    s = data["sendungen"][0]
    details = s.get("sendungsdetails", {})
    verlauf = details.get("sendungsverlauf", {})
    zustellung = details.get("zustellung", {})
    
    events = []
    for e in verlauf.get("events", []):
        events.append({
            "time": e.get("datum", ""),
            "status": e.get("status", ""),
            "return": e.get("ruecksendung", False)
        })
    
    return {
        "tracking_number": s.get("id"),
        "status": verlauf.get("status", "Unbekannt"),
        "progress": f"{verlauf.get('fortschritt', '?')}/{verlauf.get('maximalFortschritt', '?')}",
        "last_update": verlauf.get("datumAktuellerStatus", ""),
        "delivered": details.get("istZugestellt", False),
        "country": details.get("zielland", ""),
        "delivery_window": {
            "from": zustellung.get("zustellzeitfensterVon", ""),
            "to": zustellung.get("zustellzeitfensterBis", "")
        },
        "events": events
    }

def format_summary(parsed: dict) -> str:
    """Format parsed tracking into readable text."""
    if "error" in parsed:
        return f"❌ {parsed['error']}"
    
    progress_num = int(parsed["progress"].split("/")[0]) if "/" in parsed["progress"] else 0
    progress_max = int(parsed["progress"].split("/")[1]) if "/" in parsed["progress"] else 5
    bar = "●" * progress_num + "○" * (progress_max - progress_num)
    
    lines = [
        f"📦 DHL Tracking: {parsed['tracking_number']}",
        f"📊 Fortschritt: [{bar}] {parsed['progress']}",
        f"📍 Status: {parsed['status']}",
        f"🏳️ Zielland: {parsed['country']}",
        f"✅ Zugestellt: {'Ja' if parsed['delivered'] else 'Nein'}",
        "",
        "📋 Sendungsverlauf:"
    ]
    
    for e in parsed["events"]:
        try:
            dt = datetime.fromisoformat(e["time"])
            time_str = dt.strftime("%d.%m. %H:%M")
        except:
            time_str = e["time"]
        lines.append(f"  {time_str} — {e['status']}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = fetch_tracking(sys.argv[1])
    else:
        data = json.load(sys.stdin)
    
    parsed = parse_tracking(data)
    print(format_summary(parsed))
    
    # Also output JSON to stderr for programmatic use
    print(json.dumps(parsed, indent=2, ensure_ascii=False), file=sys.stderr)
