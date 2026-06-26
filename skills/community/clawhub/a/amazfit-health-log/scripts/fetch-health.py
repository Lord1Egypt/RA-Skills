#!/usr/bin/env python3
"""
HCGateway → Obsidian Health Log
Fetches Amazfit GTR3 data for a given date and writes a daily note.
"""

import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# ── Config ────────────────────────────────────────────────────────────────────
SKILL_DIR   = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
LOCALES_DIR = SKILL_DIR / "locales"

# VAULT_PATH and LOG_DIR are loaded from config.json at runtime (see main())

def load_locale(language: str) -> dict:
    """Load locale strings, falling back to 'en' if the requested locale is missing."""
    locale_file = LOCALES_DIR / f"{language}.json"
    if not locale_file.exists():
        print(f"⚠ Locale '{language}' not found, falling back to 'en'")
        locale_file = LOCALES_DIR / "en.json"
    with open(locale_file, encoding="utf-8") as f:
        return json.load(f)

# ── HTTP helpers ───────────────────────────────────────────────────────────────
def api_post(url, payload, token=None):
    data = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def login(base_url, username, password):
    resp = api_post(f"{base_url}/api/v2/login", {"username": username, "password": password})
    return resp["token"]

def fetch(base_url, token, method):
    return api_post(f"{base_url}/api/v2/fetch/{method}", {}, token=token)

# ── Data processing ────────────────────────────────────────────────────────────
def to_local(iso_str, tz):
    """Parse ISO UTC string → local datetime."""
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return dt.astimezone(tz)

def is_on_date(iso_str, target_date, tz):
    return to_local(iso_str, tz).date() == target_date

def process_steps(records, target_date, tz):
    total = sum(
        r["data"].get("count", 0)
        for r in records
        if is_on_date(r["start"], target_date, tz)
    )
    return total

def process_sleep(records, target_date, tz):
    """Find sleep session that ends on target_date (morning wake-up)."""
    sessions = [r for r in records if to_local(r["end"], tz).date() == target_date]
    if not sessions:
        return None
    # take the longest session if multiple
    session = max(sessions, key=lambda r: (
        datetime.fromisoformat(r["end"].replace("Z", "+00:00")) -
        datetime.fromisoformat(r["start"].replace("Z", "+00:00"))
    ))
    start = to_local(session["start"], tz)
    end   = to_local(session["end"], tz)
    total_min = int((end - start).total_seconds() / 60)

    stage_mins = {1: 0, 4: 0, 5: 0, 6: 0}
    for s in session["data"].get("stages", []):
        stage = s.get("stage")
        if stage in stage_mins:
            s_start = datetime.fromisoformat(s["startTime"].replace("Z", "+00:00"))
            s_end   = datetime.fromisoformat(s["endTime"].replace("Z", "+00:00"))
            stage_mins[stage] += int((s_end - s_start).total_seconds() / 60)

    return {
        "start": start.strftime("%H:%M"),
        "end":   end.strftime("%H:%M"),
        "total_h": total_min // 60,
        "total_m": total_min % 60,
        "wach":   stage_mins[1],
        "leicht": stage_mins[4],
        "tief":   stage_mins[5],
        "rem":    stage_mins[6],
    }

def process_hr(records, target_date, tz):
    samples = []
    for r in records:
        if is_on_date(r["start"], target_date, tz):
            for s in r["data"].get("samples", []):
                bpm = s.get("beatsPerMinute")
                if bpm:
                    samples.append(bpm)
    if not samples:
        return None
    return {"avg": round(sum(samples)/len(samples)), "min": min(samples), "max": max(samples)}

def process_rhr(records, target_date, tz):
    vals = [r["data"].get("beatsPerMinute") for r in records
            if is_on_date(r["start"], target_date, tz) and r["data"].get("beatsPerMinute")]
    return round(sum(vals)/len(vals)) if vals else None

def process_spo2(records, target_date, tz):
    vals = [r["data"].get("percentage") for r in records
            if is_on_date(r["start"], target_date, tz) and r["data"].get("percentage")]
    return round(sum(vals)/len(vals), 1) if vals else None

def process_distance(records, target_date, tz):
    total = 0.0
    for r in records:
        if is_on_date(r["start"], target_date, tz):
            d = r["data"].get("distance", 0)
            # distance can be a dict with units or a plain number (meters)
            if isinstance(d, dict):
                total += d.get("inMeters", 0)
            else:
                total += d
    return round(total / 1000, 2) if total else None  # meters → km

# ── Note generation ────────────────────────────────────────────────────────────
def fmt(val, unit="", fallback="--"):
    return f"{val} {unit}".strip() if val is not None else fallback

def generate_note(date, steps, sleep, hr, rhr, spo2, distance_km, t: dict, tz):
    wday      = t["weekdays"][date.weekday()]
    date_str  = date.strftime("%Y-%m-%d")
    date_disp = date.strftime("%d.%m.%Y")

    # Sleep section
    if sleep:
        sleep_dur   = f"{sleep['total_h']}h {sleep['total_m']}m"
        sleep_block = f"""\
### 😴 {t['sleep_heading']}
- **{t['sleep_period']}:** {sleep['start']} – {sleep['end']}
- **{t['sleep_duration']}:** {sleep_dur}

| {t['col_stage']}  | {t['col_minutes']} |
|--------|---------|
| {t['stage_deep']}   | {sleep['tief']} min |
| {t['stage_rem']}    | {sleep['rem']} min |
| {t['stage_light']}  | {sleep['leicht']} min |
| {t['stage_awake']}  | {sleep['wach']} min |"""
    else:
        sleep_block = f"### 😴 {t['sleep_heading']}\n*{t['sleep_no_data']}*"

    # HR section
    if hr:
        hr_block = f"### ❤️ {t['hr_heading']}\n- **{t['hr_avg']}** {hr['avg']} bpm · Min {hr['min']} · Max {hr['max']} bpm"
    else:
        hr_block = f"### ❤️ {t['hr_heading']}\n- **{t['hr_resting']}:** {fmt(rhr, 'bpm')}"

    if rhr and hr:
        hr_block += f"\n- **{t['hr_resting']}:** {rhr} bpm"

    sleep_dur_summary = f"{sleep['total_h']}h {sleep['total_m']}m" if sleep else '--'

    return f"""\
---
date: {date_str}
{t['fm_weekday_key']}: {wday}
tags: ["{t['tag_health']}", gtr3, log, "{t['tag_auto']}"]
source: {t['fm_source']}
created: {datetime.now(tz).strftime("%Y-%m-%dT%H:%M")}
---

# 🏃 {t['note_title']} — {wday}, {date_disp}

> [!info] {t['callout_title']}
> {t['callout_body']}

---

## 📊 {t['summary_heading']}

| {t['col_metric']} | {t['col_value']} |
|--------|-------|
| 👟 {t['row_steps']} | {fmt(steps)} |
| 📏 {t['row_distance']} | {fmt(distance_km, 'km')} |
| 😴 {t['row_sleep_dur']} | {sleep_dur_summary} |
| ❤️ {t['row_resting_hr']} | {fmt(rhr, 'bpm')} |
| 🩸 {t['row_spo2']} | {fmt(spo2, '%')} |

---

{sleep_block}

---

{hr_block}

---

### 🩸 {t['spo2_heading']}
- **{t['spo2_avg']}:** {fmt(spo2, '%')}

---

*← [[{date.replace(day=date.day-1).strftime("%Y-%m-%d") if date.day > 1 else ""}|{t['nav_yesterday']}]]  |  [[30 Bereiche/Gesundheit/Logs/GTR3/{(date + timedelta(days=1)).strftime("%Y-%m-%d")}|{t['nav_tomorrow']}]] →*
"""

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    # Load config and locale
    with open(CONFIG_FILE) as f:
        cfg = json.load(f)
    tz      = ZoneInfo(cfg.get("timezone", "UTC"))
    t       = load_locale(cfg.get("language", "en"))
    log_dir = Path(cfg["vault_path"]) / cfg.get("log_dir", "Health/GTR3")

    # Target date: yesterday by default, or pass YYYY-MM-DD as arg
    if len(sys.argv) > 1:
        target_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    else:
        target_date = (datetime.now(tz) - timedelta(days=1)).date()

    print(f"Fetching health data for {target_date}...")

    # Auth
    token = login(cfg["base_url"], cfg["username"], cfg["password"])
    print("✓ Authenticated")

    # Fetch all relevant data types
    raw_steps    = fetch(cfg["base_url"], token, "steps")
    raw_sleep    = fetch(cfg["base_url"], token, "sleepSession")
    raw_hr       = fetch(cfg["base_url"], token, "heartRate")
    raw_rhr      = fetch(cfg["base_url"], token, "restingHeartRate")
    raw_spo2     = fetch(cfg["base_url"], token, "oxygenSaturation")
    raw_distance = fetch(cfg["base_url"], token, "distance")
    print("✓ Data fetched")

    # Process
    steps       = process_steps(raw_steps, target_date, tz)
    sleep       = process_sleep(raw_sleep, target_date, tz)
    hr          = process_hr(raw_hr, target_date, tz)
    rhr         = process_rhr(raw_rhr, target_date, tz)
    spo2        = process_spo2(raw_spo2, target_date, tz)
    distance_km = process_distance(raw_distance, target_date, tz)

    # Generate note
    note = generate_note(target_date, steps, sleep, hr, rhr, spo2, distance_km, t, tz)

    # Write to vault
    log_dir.mkdir(parents=True, exist_ok=True)
    out_path = log_dir / f"{target_date}.md"
    out_path.write_text(note, encoding="utf-8")
    print(f"✓ Note written: {out_path}")

    # Summary output
    print(f"\n📊 {target_date}")
    print(f"   Steps:      {steps or '--'}")
    print(f"   Distance:   {distance_km or '--'} km")
    sleep_str = f"{sleep['total_h']}h {sleep['total_m']}m" if sleep else '--'
    print(f"   Sleep:      {sleep_str}")
    print(f"   Resting HR: {rhr or '--'} bpm")
    print(f"   SpO2:       {spo2 or '--'} %")

if __name__ == "__main__":
    main()
