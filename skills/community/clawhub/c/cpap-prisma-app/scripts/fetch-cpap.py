#!/usr/bin/env python3
"""
PrismaAPP → Obsidian CPAP Log
Fetches Löwenstein CPAP therapy data and writes a structured daily note.

Usage:
  fetch-cpap.py                     # yesterday (default)
  fetch-cpap.py 2026-04-06          # specific date
  fetch-cpap.py --all               # backfill all data since first sync
  fetch-cpap.py --from=2026-03-01   # backfill from a specific date
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import date, timedelta, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# ── Paths ──────────────────────────────────────────────────────────────────────
SKILL_DIR   = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
LOCALES_DIR = SKILL_DIR / "locales"

THERAPY_MODE = {1: "APAP", 2: "CPAP", 3: "BiLevel", None: "—"}

# ── Config & Locale ────────────────────────────────────────────────────────────
def load_locale(language: str) -> dict:
    locale_file = LOCALES_DIR / f"{language}.json"
    if not locale_file.exists():
        print(f"⚠ Locale '{language}' not found, falling back to 'en'")
        locale_file = LOCALES_DIR / "en.json"
    with open(locale_file, encoding="utf-8") as f:
        return json.load(f)

# ── HTTP helpers ───────────────────────────────────────────────────────────────
def http_post_form(url: str, fields: dict) -> dict:
    data = urllib.parse.urlencode(fields).encode()
    req  = urllib.request.Request(url, data=data,
           headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def http_get(url: str, token: str) -> dict:
    req = urllib.request.Request(url,
          headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

# ── Auth ───────────────────────────────────────────────────────────────────────
def login(email: str, password: str, api_base: str) -> str:
    resp = http_post_form(f"{api_base}/connect/token", {
        "grant_type":  "password",
        "username":    email,
        "password":    password,
        "scope":       "profile offline_access",
        "tenant":      "patientapp",
        "client_id":   "patient-app-client",
    })
    return resp["access_token"]

# ── API ────────────────────────────────────────────────────────────────────────
def get_dashboard(token: str, api_base: str) -> dict:
    return http_get(f"{api_base}/api/Dashboard", token)

def get_week(token: str, date_in_week: str, api_base: str) -> list[dict]:
    data = http_get(f"{api_base}/api/Dashboard/week?dateInWeek={date_in_week}", token)
    return data.get("days", [])

def get_all_days(token: str, min_date_str: str, api_base: str) -> dict[str, dict]:
    """Load all days with data from min_date to today. Returns dict[date_str → day]."""
    min_date = date.fromisoformat(min_date_str)
    today    = date.today()
    by_date  = {}
    current  = min_date
    while current <= today:
        for day in get_week(token, current.isoformat(), api_base):
            if day.get("isDataReceived") and day["date"] not in by_date:
                by_date[day["date"]] = day
        current += timedelta(weeks=1)
    return dict(sorted(by_date.items()))

def get_day(token: str, target: date, api_base: str) -> dict | None:
    """Load data for exactly one day."""
    for d in get_week(token, target.isoformat(), api_base):
        if d["date"] == target.isoformat() and d.get("isDataReceived"):
            return d
    return None

# ── Formatting ─────────────────────────────────────────────────────────────────
def fmt_min(mins: int | None) -> str:
    if not mins:
        return "—"
    h, m = divmod(mins, 60)
    return f"{h}h {m:02d}m"

def fmt_f(v: float | None, digits: int = 1) -> str:
    return f"{v:.{digits}f}" if v is not None else "—"

def quality_label(q: int, t: dict) -> str:
    return t.get(f"q_{q}", "—")

def ahi_info(q: int, t: dict) -> str:
    return t.get(f"ahi_{q}", "—")

def overall_quality(day: dict, t: dict) -> tuple[str, str]:
    scores = [day.get("ahiQuality", 4), day.get("leakageQuality", 4), day.get("deepSleepQuality", 4)]
    valid  = [s for s in scores if s < 4]
    if not valid:
        return t["overall_none"], t["tag_none"]
    avg = sum(valid) / len(valid)
    if avg <= 0.3:   return t["overall_great"],  t["tag_great"]
    if avg <= 1.0:   return t["overall_good"],   t["tag_good"]
    if avg <= 1.5:   return t["overall_ok"],     t["tag_ok"]
    if avg <= 2.2:   return t["overall_border"], t["tag_border"]
    return                  t["overall_bad"],    t["tag_bad"]

def mask_label(mask: int | None, t: dict) -> str:
    if mask is None:    return "—"
    if mask == 100:     return t["mask_perfect"]
    if mask >= 90:      return t["mask_ok"]
    return                     t["mask_bad"]

# ── Note generation ────────────────────────────────────────────────────────────
def make_note(day: dict, all_dates: list[str], t: dict, tz: ZoneInfo) -> str:
    d       = day["date"]
    dt      = date.fromisoformat(d)
    weekday = t["weekdays"][dt.weekday()]

    ahi     = day["ahi"]
    ahi_q   = day.get("ahiQuality", 4)
    leak    = day["leakage"]
    leak_q  = day.get("leakageQuality", 4)
    sleep   = day["sleepTimeInMinutes"]
    deep    = day["deepSleepInMinutes"]
    deep_q  = day.get("deepSleepQuality", 4)
    snore   = day["snoringPercent"]
    snore_q = day.get("snoringQuality", 4)
    mask    = day.get("maskFitPercentage")
    pmin    = day.get("apapMinPressure", 0)
    pmax    = day.get("apapMaxPressure", 0)
    mode    = THERAPY_MODE.get(day.get("therapyMode"), "—")
    goal    = day.get("goalValueInMinutes", 360)
    goal_ok = day.get("isGoalReached", False)
    created = datetime.now(tz).strftime("%Y-%m-%dT%H:%M")

    # Navigation
    base    = "30 Bereiche/Gesundheit/CPAP/Logs"
    idx     = all_dates.index(d) if d in all_dates else -1
    prev_d  = all_dates[idx - 1] if idx > 0 else None
    next_d  = all_dates[idx + 1] if idx >= 0 and idx < len(all_dates) - 1 else None
    nav_prev = f"[[{base}/{prev_d}|← {prev_d}]]" if prev_d else "—"
    nav_next = f"[[{base}/{next_d}|{next_d} →]]" if next_d else "—"

    # Derived values
    druck       = f"{pmin} hPa" if pmin == pmax else f"{pmin}–{pmax} hPa"
    gesamt, tag = overall_quality(day, t)
    goal_str    = t["goal_reached"] if goal_ok else f"{t['goal_not_reached']} ({fmt_min(goal)})"

    return (
        f"---\n"
        f"date: {d}\n"
        f"{t['fm_weekday_key']}: {weekday}\n"
        f'tags: ["{t["tag_health"]}", "cpap", "{t["tag_auto"]}", "{tag}"]\n'
        f"source: {t['fm_source']}\n"
        f"created: {created}\n"
        f"---\n"
        f"\n"
        f"# 😴 {t['note_title']} — {weekday}, {dt.strftime('%d.%m.%Y')}\n"
        f"\n"
        f"> [!info] {t['callout_title']}\n"
        f"> {t['callout_body']}\n"
        f"\n"
        f"---\n"
        f"\n"
        f"## 📊 {t['summary_heading']}\n"
        f"\n"
        f"| {t['col_metric']} | {t['col_value']} | {t['col_rating']} |\n"
        f"|--------|------|-----------|\n"
        f"| 😴 {t['row_sleep']} | {fmt_min(sleep)} | {goal_str} |\n"
        f"| 🧠 {t['row_deepsleep']} | {fmt_min(deep)} | {quality_label(deep_q, t)} |\n"
        f"| 💨 {t['row_ahi']} | {fmt_f(ahi)} | {quality_label(ahi_q, t)} |\n"
        f"| 💧 {t['row_leakage']} | {fmt_f(leak)} L/min | {quality_label(leak_q, t)} |\n"
        f"| 🔊 {t['row_snoring']} | {snore} % | {quality_label(snore_q, t)} |\n"
        f"| 😷 {t['row_mask']} | {mask if mask is not None else '—'} % | {mask_label(mask, t)} |\n"
        f"| ⚙️ {t['row_therapy']} | {mode} | {t['pressure_label']}: {druck} |\n"
        f"\n"
        f"**{t['overall_prefix']}: {gesamt}**\n"
        f"\n"
        f"---\n"
        f"\n"
        f"## 😴 {t['sleep_heading']}\n"
        f"\n"
        f"- **{t['sleep_duration']}:** {fmt_min(sleep)}  \n"
        f"- **{t['sleep_deepsleep']}:** {fmt_min(deep)} ({quality_label(deep_q, t)})\n"
        f"- **{t['sleep_goal']}:** {fmt_min(goal)} — {t['goal_reached'] if goal_ok else t['goal_not_reached']}\n"
        f"\n"
        f"---\n"
        f"\n"
        f"## 💨 {t['therapy_heading']}\n"
        f"\n"
        f"- **{t['row_ahi']}:** {fmt_f(ahi)} — {ahi_info(ahi_q, t)}  \n"
        f"  {t['therapy_rating']}: {quality_label(ahi_q, t)}\n"
        f"- **{t['row_leakage']}:** {fmt_f(leak)} L/min — {quality_label(leak_q, t)}\n"
        f"- **{t['therapy_mode']}:** {mode}\n"
        f"- **{t['pressure_label']}:** {druck}\n"
        f"\n"
        f"---\n"
        f"\n"
        f"## 🔊 {t['snoring_heading']}\n"
        f"\n"
        f"- **{t['row_snoring']}:** {snore} % {t['snoring_of_time']} — {quality_label(snore_q, t)}\n"
        f"- **{t['mask_label']}:** {mask if mask is not None else '—'} %\n"
        f"\n"
        f"---\n"
        f"\n"
        f"*{nav_prev}  |  {nav_next}*\n"
    )

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        cfg = json.load(f)

    tz       = ZoneInfo(cfg.get("timezone", "Europe/Berlin"))
    t        = load_locale(cfg.get("language", "en"))
    api_base = cfg.get("api_base", "https://my.prismacloud.com").rstrip("/")
    log_dir  = Path(cfg["vault_path"]) / cfg.get("log_dir", "30 Bereiche/Gesundheit/CPAP/Logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    args     = sys.argv[1:]
    do_all   = "--all" in args
    from_arg = next((a for a in args if a.startswith("--from=")), None)
    date_arg = next((a for a in args if not a.startswith("--")), None)

    print("Logging in ...")
    token = login(cfg["email"], cfg["password"], api_base)
    print("✓ Authenticated")

    # ── Single day mode ───────────────────────────────────────────────────────
    if not do_all and not from_arg:
        if date_arg:
            target = date.fromisoformat(date_arg)
        else:
            target = (datetime.now(tz) - timedelta(days=1)).date()

        print(f"Loading data for {target} ...")
        day = get_day(token, target, api_base)

        if not day:
            print(f"⚠ {t['no_data_msg']}")
            sys.exit(0)

        week_dates = sorted(d["date"] for d in get_week(token, target.isoformat(), api_base)
                            if d.get("isDataReceived"))
        note = make_note(day, week_dates, t, tz)

        out = log_dir / f"{target}.md"
        out.write_text(note, encoding="utf-8")
        print(f"✓ Note written: {out}")
        _print_summary(day, t)
        return

    # ── Backfill mode ─────────────────────────────────────────────────────────
    print("Loading dashboard ...")
    dashboard = get_dashboard(token, api_base)
    api_min   = dashboard.get("minDate", str(date.today()))

    start_date = from_arg.split("=", 1)[1] if from_arg else api_min
    if start_date < api_min:
        start_date = api_min

    print(f"Loading all days from {start_date} ...")
    days  = get_all_days(token, start_date, api_base)
    dates = list(days.keys())
    print(f"  {len(days)} days with data found.")

    created = skipped = 0
    for d_str, day in days.items():
        out = log_dir / f"{d_str}.md"
        if out.exists():
            skipped += 1
            continue
        note = make_note(day, dates, t, tz)
        out.write_text(note, encoding="utf-8")
        print(f"  ✓ {d_str}")
        created += 1

    print(f"\nDone: {created} created, {skipped} already existed.")

def _print_summary(day: dict, t: dict):
    gesamt, _ = overall_quality(day, t)
    print(f"\n📊 {day['date']}")
    print(f"   {t['row_sleep']:15} {fmt_min(day.get('sleepTimeInMinutes'))}")
    print(f"   {t['row_deepsleep']:15} {fmt_min(day.get('deepSleepInMinutes'))}")
    print(f"   {t['row_ahi']:15} {fmt_f(day.get('ahi'))}")
    print(f"   {t['row_leakage']:15} {fmt_f(day.get('leakage'))} L/min")
    print(f"   {t['row_snoring']:15} {day.get('snoringPercent', '—')} %")
    print(f"   {t['row_mask']:15} {day.get('maskFitPercentage', '—')} %")
    print(f"   {t['overall_prefix']:15} {gesamt}")

if __name__ == "__main__":
    main()
