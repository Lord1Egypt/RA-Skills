"""
AEGIS Incident Tracker — Prevents spam by grouping related alerts.

An "incident" is a cluster of CRITICAL/HIGH threats about the same 
topic+location within a time window. Once an incident is alerted,
subsequent updates about the SAME incident are suppressed from the channel.

Only genuinely NEW incidents (different location, different attack type,
or >6 hours later) trigger new channel posts.
"""

import json, os, re, time, hashlib
from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path(os.environ.get("AEGIS_DATA_DIR", os.path.expanduser("~/.openclaw/aegis-data")))
INCIDENTS_FILE = DATA_DIR / "active_incidents.json"

# Incident window: threats within this period about the same topic = same incident
INCIDENT_WINDOW_HOURS = 6

# Keywords for incident fingerprinting (extract topic signature)
LOCATION_KEYWORDS = [
    "dubai", "abu dhabi", "dxb", "auh", "fujairah", "sharjah", "ajman",
    "ras al", "umm al", "jebel ali", "khalifa", "al dhafra", "minhad",
    "airport", "port", "base", "embassy", "consulate", "tower", "hotel"
]

ATTACK_KEYWORDS = [
    "drone", "missile", "ballistic", "cruise", "rocket", "projectile",
    "strike", "attack", "bomb", "fire", "explosion", "intercept",
    "shelling", "barrage"
]


def _extract_fingerprint(text: str) -> str:
    """Extract a normalized incident fingerprint from threat text.
    Groups by: primary location + broad category. Very coarse — 
    'DXB airport drone fire' and 'DXB airport flights suspended' = SAME incident."""
    text_lower = text.lower()
    
    # Extract PRIMARY location (most specific match wins)
    location = "unknown"
    location_priority = [
        ("dxb", "dxb"), ("dubai airport", "dxb"), ("dubai international airport", "dxb"),
        ("auh", "auh"), ("abu dhabi airport", "auh"),
        ("fujairah port", "fujairah-port"), ("port of fujairah", "fujairah-port"),
        ("jebel ali", "jebel-ali"), ("khalifa port", "khalifa-port"),
        ("al dhafra", "al-dhafra"), ("minhad", "minhad"),
        ("dubai", "dubai"), ("abu dhabi", "abudhabi"),
        ("fujairah", "fujairah"), ("sharjah", "sharjah"),
        ("uae", "uae"), ("emirates", "uae"),
    ]
    for keyword, loc_id in location_priority:
        if keyword in text_lower:
            location = loc_id
            break
    
    # Upgrade: if location is generic "dubai" but "airport" is in text, it's DXB
    if location == "dubai" and "airport" in text_lower:
        location = "dxb"
    if location == "abudhabi" and "airport" in text_lower:
        location = "auh"
    
    # Broad category (NOT specific attack type — too granular)
    category = "general"
    if any(w in text_lower for w in ["airport", "flight", "airspace", "runway", "landing", "holding pattern", "airfield", "aviation", "airliner"]):
        category = "aviation"
    elif any(w in text_lower for w in ["port", "oil", "fuel", "tanker", "shipping"]):
        category = "maritime-energy"
    elif any(w in text_lower for w in ["embassy", "consulate", "diplomatic"]):
        category = "diplomatic"
    elif any(w in text_lower for w in ["tower", "building", "residential", "hotel"]):
        category = "urban"
    elif any(w in text_lower for w in ["base", "military", "thaad", "patriot", "radar"]):
        category = "military"
    
    fp_text = f"{location}|{category}"
    return hashlib.md5(fp_text.encode()).hexdigest()[:12]


def load_incidents() -> dict:
    """Load active incidents."""
    try:
        if INCIDENTS_FILE.exists():
            return json.loads(INCIDENTS_FILE.read_text())
    except:
        pass
    return {}


def save_incidents(incidents: dict):
    """Save active incidents."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    INCIDENTS_FILE.write_text(json.dumps(incidents, indent=2))


def is_new_incident(threat_title: str) -> bool:
    """Check if this threat represents a NEW incident (not yet alerted)."""
    incidents = load_incidents()
    fp = _extract_fingerprint(threat_title)
    now = time.time()
    
    # Clean expired incidents
    expired = [k for k, v in incidents.items() 
               if now - v.get("first_seen", 0) > INCIDENT_WINDOW_HOURS * 3600]
    for k in expired:
        del incidents[k]
    
    if fp in incidents:
        # Same incident — update count but DON'T alert again
        incidents[fp]["updates"] = incidents[fp].get("updates", 0) + 1
        incidents[fp]["last_seen"] = now
        save_incidents(incidents)
        return False
    else:
        # New incident — record it and allow alert
        incidents[fp] = {
            "first_seen": now,
            "last_seen": now,
            "fingerprint": fp,
            "sample_title": threat_title[:200],
            "updates": 0
        }
        save_incidents(incidents)
        return True


def filter_new_incidents(threats: list) -> list:
    """Filter a list of threats to only truly NEW incidents."""
    new = []
    for t in threats:
        title = t.get("title", "")
        if is_new_incident(title):
            new.append(t)
    return new
