#!/usr/bin/env python3
"""
collect_stats.py — gather a clinic's weekly activity stats from the NxVET API.

Read-only. Stdlib only (no pip installs). The only network calls are authenticated
GETs to https://app.nx.vet. Never prints the full API key.

It fetches, for a date window (default: the last 7 days in the clinic's timezone):
  * total recordings (labels) and a per-device / per-weekday / per-hour breakdown
  * the previous window's total, for a week-over-week trend
  * the device fleet with last-seen times (to flag silent devices)
  * webhook delivery health (recent failures), if any webhooks exist

Output: a single JSON object on stdout that the report writer (Claude, or
write_report.py) turns into a plain-English report. Nothing is sent anywhere.

Usage:
    python3 collect_stats.py                     # last 7 days, tz from config.json
    python3 collect_stats.py --days 7
    python3 collect_stats.py --end 2026-07-20    # window ending on this date (inclusive)
    python3 collect_stats.py --tz America/New_York
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None

BASE_URL = "https://app.nx.vet"
PROJECT = os.getcwd()
CONFIG_PATH = os.path.join(PROJECT, "config.json")

# Label types that represent an actual clinic recording/consult. NxHubBatch =
# NxHUB device recordings; the others are app/dictation/button captures. We count
# these and ignore derived/aggregate types so the total reflects real activity.
RECORDING_TYPES = [
    "NxHubBatch", "ClinicConversation", "ButtonRecording",
    "AudioButtonRecording", "DictationAudio", "PhoneCallAudio", "NxMIC",
]


def load_env_key():
    key = os.environ.get("NXVET_API_KEY")
    if key:
        return key.strip()
    env_path = os.path.join(PROJECT, ".env")
    fallback = None
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("NXVET_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
                if "=" in line and not line.startswith("#"):
                    v = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if v.startswith("nxvet_sk_"):
                        fallback = v
    if fallback:
        return fallback
    sys.exit("ERROR: NXVET_API_KEY not found in environment or ./.env")


def mask(key):
    return f"nxvet_sk_…{key[-4:]}" if key and len(key) >= 4 else "nxvet_sk_…"


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


CACHE_DIR = os.path.join(PROJECT, "state", "http_cache")
# The NxVET API does not send ETag/Cache-Control headers, so conditional (304)
# requests aren't possible. Instead we use a short client-side TTL cache: a
# repeat request for the same URL within CACHE_TTL_S reuses the local copy and
# makes NO API call at all. This is what keeps re-runs cheap. TTL is short so a
# scheduled weekly run always gets fresh data. Override with CACHE_TTL_S env.
CACHE_TTL_S = int(os.environ.get("CACHE_TTL_S", "600"))  # 10 minutes default


def _cache_path(url):
    import hashlib
    return os.path.join(CACHE_DIR, hashlib.sha1(url.encode()).hexdigest() + ".json")


def _cache_get(url, now_s):
    p = _cache_path(url)
    if not os.path.exists(p):
        return None
    if now_s - os.path.getmtime(p) > CACHE_TTL_S:
        return None  # stale
    try:
        with open(p) as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return None


def _cache_put(url, body_obj):
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = _cache_path(url) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(body_obj, f)
    os.replace(tmp, _cache_path(url))


def api_get(path, key, params=None, tries=5, use_cache=True):
    """GET returning (json_or_none, headers). Backs off on 429/5xx.

    TTL cache (opt-in via use_cache): a repeat request for the same URL within
    CACHE_TTL_S reuses the local copy and skips the API call entirely. Used
    because the NxVET API sends no ETag/Cache-Control, so 304 revalidation isn't
    available. Keeps re-runs (and the overlapping prior-period fetch) cheap.
    """
    url = BASE_URL + path
    if params:
        parts = []
        for k, v in params.items():
            if isinstance(v, (list, tuple)):
                for item in v:
                    parts.append(f"{k}={urllib.request.quote(str(item))}")
            else:
                parts.append(f"{k}={urllib.request.quote(str(v))}")
        url += "?" + "&".join(parts)

    if use_cache:
        hit = _cache_get(url, time.time())
        if hit is not None:
            return hit, {"x-cache": "HIT"}

    backoff = 1.0
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {key}", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                obj = json.loads(body) if body else None
                if use_cache:
                    _cache_put(url, obj)
                return obj, dict(resp.headers)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                ra = e.headers.get("Retry-After")
                time.sleep(min(float(ra) if ra else backoff, 60))
                backoff *= 2
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < tries - 1:
                time.sleep(min(backoff, 60))
                backoff *= 2
                continue
            raise
    raise RuntimeError("exhausted retries")


def uuid7_ms(uid):
    """Label ids are UUIDv7 — first 48 bits are epoch-ms creation time."""
    try:
        return int(uid.replace("-", "")[:12], 16)
    except (ValueError, AttributeError):
        return None


def label_ms(row):
    """Best timestamp for a label row: fromTime (epoch ms) else the id's time."""
    return row.get("fromTime") or uuid7_ms(row.get("id", ""))


def fetch_labels_between(org, key, start_ms, end_ms):
    """All recording labels with a timestamp in [start_ms, end_ms). Newest-first;
    stop paging once we're older than start_ms."""
    rows, offset, limit = [], 0, 100
    while True:
        listing, _ = api_get(
            f"/api/organizations/{org}/labels", key,
            {"types": RECORDING_TYPES, "limit": limit, "offset": offset})
        page = listing if isinstance(listing, list) else listing.get("data", [])
        if not page:
            break
        stop = False
        for r in page:
            ms = label_ms(r)
            if ms is None:
                continue
            if ms < start_ms:
                stop = True
                break
            if ms < end_ms:
                rows.append(r)
        if stop or len(page) < limit:
            break
        offset += limit
    return rows


def summarize(rows, tz):
    """Per-device / per-weekday / per-hour counts for a set of label rows."""
    by_device, by_weekday, by_hour = Counter(), Counter(), Counter()
    WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for r in rows:
        ms = label_ms(r)
        dev = r.get("friendlyName") or r.get("deviceSerial") or "Unknown device"
        by_device[dev] += 1
        if ms is not None:
            dt = datetime.fromtimestamp(ms / 1000, tz)
            by_weekday[WD[dt.weekday()]] += 1
            by_hour[dt.hour] += 1
    return {
        "byDevice": dict(by_device.most_common()),
        "byWeekday": {d: by_weekday.get(d, 0) for d in WD},
        "byHour": {str(h): by_hour.get(h, 0) for h in range(24)},
    }


def fetch_devices(org, key):
    listing, _ = api_get("/api/devices", key, {"organizationId": org})
    rows = listing if isinstance(listing, list) else listing.get("data", [])
    out = []
    for d in rows:
        serial = d.get("serial") or ""
        # Only NxHUB hardware heartbeats (has a lastReport / nxhub-* serial).
        # App/web/iOS "devices" are login sessions — never flag them as "silent".
        is_hardware = serial.lower().startswith("nxhub-") or bool(d.get("nxHubLastReportTime"))
        out.append({
            "id": d.get("id"),
            "serial": serial,
            "name": d.get("friendlyName"),
            "isHardware": is_hardware,
            "lastReport": d.get("nxHubLastReportTime"),
            "firmware": d.get("nxHubCurrentFirmwareVersion"),
            "targetFirmware": d.get("nxHubTargetFirmwareVersion"),
        })
    return out


def fetch_webhook_health(org, key):
    """Return webhook failure counts over recent deliveries, best-effort.
    Webhooks are optional — any error here is non-fatal (returns [])."""
    try:
        listing, _ = api_get(f"/api/organizations/{org}/webhooks", key)
    except Exception:
        return []
    hooks = listing if isinstance(listing, list) else (listing or {}).get("data", [])
    health = []
    for h in hooks or []:
        hid = h.get("id")
        entry = {"id": hid, "url": h.get("url"), "enabled": h.get("enabled"),
                 "recentDeliveries": 0, "recentFailures": 0}
        try:
            deliveries, _ = api_get(
                f"/api/organizations/{org}/webhooks/{hid}/deliveries", key,
                {"limit": 50})
            dl = deliveries if isinstance(deliveries, list) else (deliveries or {}).get("data", [])
            for d in dl or []:
                entry["recentDeliveries"] += 1
                status = d.get("statusCode") or d.get("responseStatus")
                ok = d.get("success")
                if ok is False or (isinstance(status, int) and status >= 400):
                    entry["recentFailures"] += 1
        except Exception:
            pass
        health.append(entry)
    return health


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--end", help="window end date YYYY-MM-DD (inclusive); default today")
    ap.add_argument("--tz", help="IANA timezone; overrides config.json")
    args = ap.parse_args()

    if ZoneInfo is None:
        sys.exit("ERROR: Python 3.9+ required (zoneinfo).")

    key = load_env_key()
    cfg = load_config()
    org = cfg.get("organizationId")
    if not org:
        # discover it
        me, _ = api_get("/api/auth/me", key)
        org = me.get("organizationId")
    tzname = args.tz or cfg.get("timezone") or "America/New_York"
    tz = ZoneInfo(tzname)

    # window: [start, end) as local midnights
    if args.end:
        end_local = datetime.fromisoformat(args.end).replace(tzinfo=tz) + timedelta(days=1)
    else:
        now = datetime.now(tz)
        end_local = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    start_local = end_local - timedelta(days=args.days)
    prev_start_local = start_local - timedelta(days=args.days)

    to_ms = lambda dt: int(dt.timestamp() * 1000)
    end_ms, start_ms, prev_ms = to_ms(end_local), to_ms(start_local), to_ms(prev_start_local)

    this_rows = fetch_labels_between(org, key, start_ms, end_ms)
    prev_rows = fetch_labels_between(org, key, prev_ms, start_ms)
    devices = fetch_devices(org, key)
    webhooks = fetch_webhook_health(org, key)

    out = {
        "organizationId": org,
        "organizationName": cfg.get("organizationName"),
        "timezone": tzname,
        "window": {
            "start": start_local.isoformat(),
            "end": (end_local - timedelta(days=0)).isoformat(),
            "days": args.days,
        },
        "totals": {
            "recordings": len(this_rows),
            "previousRecordings": len(prev_rows),
        },
        "breakdown": summarize(this_rows, tz),
        "devices": devices,
        "webhooks": webhooks,
        "generatedNote": "read-only snapshot; nothing was sent or modified",
    }
    # trend
    prev = out["totals"]["previousRecordings"]
    cur = out["totals"]["recordings"]
    out["totals"]["trendPct"] = (round((cur - prev) / prev * 100) if prev else None)

    sys.stderr.write(f"[collect_stats] org={org} window={args.days}d "
                     f"recordings={cur} prev={prev} devices={len(devices)} "
                     f"key={mask(key)}\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
