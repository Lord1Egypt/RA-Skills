#!/usr/bin/env python3
"""
GA Insights - AI-Powered Google Analytics Assistant
OpenClaw Skill v0.3.0

Enhanced with:
- Richer natural language understanding
- Bounce rate, page performance, device, geo, hourly/daily trends
- Actionable insights & recommendations
- In-memory caching (5-10 min TTL)
- Better error handling and setup guidance
"""

import os
import sys
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

# ─── Optional GA SDK ──────────────────────────────────────────────────────────
try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta import (
        RunReportRequest, RunRealtimeReportRequest,
        DateRange, Dimension, Metric, OrderBy, FilterExpression, Filter
    )
    GA_SDK_AVAILABLE = True
except ImportError:
    GA_SDK_AVAILABLE = False

# ─── Paths ────────────────────────────────────────────────────────────────────
CONFIG_DIR  = Path.home() / ".openclaw" / "ga-insights"
CONFIG_FILE = CONFIG_DIR / "config.json"
CACHE_FILE  = CONFIG_DIR / "cache.json"
DEFAULT_CREDENTIALS = str(Path.home() / ".openclaw" / "ga-insights-key.json")
SERVICE_ACCOUNT_EMAIL = "ga-insights@plucky-engine-488015-d4.iam.gserviceaccount.com"

CACHE_TTL   = 300   # 5 minutes default
CACHE_TTL_REALTIME = 30  # 30s for realtime


# ══════════════════════════════════════════════════════════════════════════════
# CACHE
# ══════════════════════════════════════════════════════════════════════════════

def _load_cache() -> dict:
    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _save_cache(cache: dict):
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except Exception:
        pass

def cache_get(key: str, ttl: int = CACHE_TTL):
    cache = _load_cache()
    entry = cache.get(key)
    if entry and (time.time() - entry["ts"]) < ttl:
        return entry["data"]
    return None

def cache_set(key: str, data):
    cache = _load_cache()
    cache[key] = {"ts": time.time(), "data": data}
    # Keep cache lean – drop entries older than 1h
    now = time.time()
    cache = {k: v for k, v in cache.items() if now - v["ts"] < 3600}
    _save_cache(cache)

def cache_clear():
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
    return {"message": "Cache cleared."}


# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════

def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"property_id": None, "connected": False}

def save_config(config: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_client():
    """Return initialised GA Data API client or None."""
    if not GA_SDK_AVAILABLE:
        return None
    config = load_config()
    creds = config.get("credentials_path") or DEFAULT_CREDENTIALS
    if os.path.exists(creds):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds
    try:
        return BetaAnalyticsDataClient()
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════════════════

def setup_guide() -> dict:
    config = load_config()
    if config.get("connected"):
        return {
            "status": "already_connected",
            "property_id": config.get("property_id"),
            "message": f"✅ Already connected to GA4 property {config.get('property_id')}."
        }
    return {
        "status": "setup_needed",
        "service_account_email": SERVICE_ACCOUNT_EMAIL,
        "steps": [
            "1. Go to https://analytics.google.com/",
            "2. Admin (⚙) → Property Access Management",
            "3. Click + → Add users",
            f"4. Enter: {SERVICE_ACCOUNT_EMAIL}",
            "5. Role: Viewer → Save",
            "6. Admin → Property Settings → copy the numeric Property ID",
            "7. Tell me: 'ga connect <Property ID>'"
        ],
        "note": "The service account only has read access — your data stays private."
    }

def complete_setup(property_id: str) -> dict:
    pid = property_id.strip().lstrip("properties/")
    config = load_config()
    config.update({"property_id": pid, "credentials_path": DEFAULT_CREDENTIALS, "connected": True})
    save_config(config)

    try:
        client = get_client()
        if client:
            client.run_report(RunReportRequest(
                property=f"properties/{pid}",
                date_ranges=[DateRange(start_date="today", end_date="today")],
                metrics=[Metric(name="screenPageViews")]
            ))
        return {"status": "success", "property_id": pid,
                "message": f"✅ Connected! Property {pid} is now linked."}
    except Exception as e:
        err = str(e)
        if "not found" in err.lower() or "permission" in err.lower():
            hint = ("Double-check you added the service account email in "
                    "GA4 Admin → Property Access Management.")
        elif "credentials" in err.lower():
            hint = "Service account key file not found. Contact support."
        else:
            hint = "Check your network and try again."
        return {"status": "error", "message": f"Connection failed: {err}", "hint": hint}


# ══════════════════════════════════════════════════════════════════════════════
# LOW-LEVEL QUERY HELPER
# ══════════════════════════════════════════════════════════════════════════════

def _not_connected() -> dict:
    return {
        "error": "Not connected to GA4.",
        "fix": "Run 'ga setup' for instructions, then 'ga connect <Property ID>'."
    }

def _sdk_missing() -> dict:
    return {
        "error": "Google Analytics SDK not installed.",
        "fix": "Run: pip install google-analytics-data"
    }

def _api_error(e: Exception, context: str = "") -> dict:
    err = str(e)
    if "quota" in err.lower():
        msg = "GA4 API quota exceeded. Try again later."
    elif "permission" in err.lower() or "403" in err:
        msg = "Permission denied. Make sure the service account has Viewer access in GA4."
    elif "not found" in err.lower() or "404" in err:
        msg = "Property not found. Check your Property ID in GA4 Admin → Property Settings."
    elif "credentials" in err.lower() or "authentication" in err.lower():
        msg = "Authentication failed. Service account key may be missing or invalid."
    else:
        msg = f"GA4 API error: {err}"
    return {"error": msg, "context": context}

def run_report(metrics: list, dimensions: list = None,
               date_ranges: list = None, days: int = 7,
               order_by: list = None, limit: int = 20,
               cache_key: str = None, cache_ttl: int = CACHE_TTL) -> dict:
    """
    Thin wrapper around RunReportRequest with caching.
    Returns {"rows": [...], "days": int} or {"error": ...}
    """
    if cache_key:
        cached = cache_get(cache_key, cache_ttl)
        if cached is not None:
            return cached

    config = load_config()
    if not config.get("connected"):
        return _not_connected()
    if not GA_SDK_AVAILABLE:
        return _sdk_missing()

    client = get_client()
    if not client:
        return {"error": "Could not initialise GA4 client. Check credentials."}

    pid = config["property_id"]

    if date_ranges is None:
        end = datetime.now()
        start = end - timedelta(days=days - 1)
        date_ranges = [DateRange(
            start_date=start.strftime('%Y-%m-%d'),
            end_date=end.strftime('%Y-%m-%d')
        )]

    kwargs = {
        "property": f"properties/{pid}",
        "date_ranges": date_ranges,
        "metrics": [Metric(name=m) for m in metrics],
        "limit": limit,
    }
    if dimensions:
        kwargs["dimensions"] = [Dimension(name=d) for d in dimensions]
    if order_by:
        kwargs["order_bys"] = order_by

    try:
        response = client.run_report(RunReportRequest(**kwargs))
        result = {"rows": response.rows, "days": days, "raw": response}
        if cache_key:
            cache_set(cache_key, result)
        return result
    except Exception as e:
        return _api_error(e, f"metrics={metrics} dims={dimensions}")


# ══════════════════════════════════════════════════════════════════════════════
# INSIGHT HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _pct_change(new: float, old: float) -> float:
    if old == 0:
        return 0.0
    return round((new - old) / old * 100, 1)

def _trend_label(pct: float) -> str:
    if pct > 20:   return "📈 significantly up"
    if pct > 5:    return "↑ up"
    if pct < -20:  return "📉 significantly down"
    if pct < -5:   return "↓ down"
    return "→ roughly flat"

def _bounce_insight(rate: float) -> str:
    if rate < 30:
        return "Excellent bounce rate — users are very engaged."
    if rate < 50:
        return "Good bounce rate — solid engagement."
    if rate < 70:
        return "Moderate bounce rate. Consider improving page load speed, content relevance, and clear CTAs."
    return ("High bounce rate ⚠️  — many visitors leave without interacting. "
            "Check page load speed (aim <3s), above-the-fold content, and mobile experience.")

def _session_duration_insight(seconds: float) -> str:
    mins = seconds / 60
    if mins < 1:
        return "Very short sessions — users aren't finding what they need."
    if mins < 2:
        return "Short sessions — content may not be engaging enough."
    if mins < 5:
        return "Decent session length — users are spending some time."
    return "Great session duration — users are deeply engaged."

def _traffic_drop_insight(pct: float, period: str = "vs last week") -> str:
    if pct < -30:
        return (f"⚠️  Traffic is {abs(pct):.0f}% lower {period}. Investigate: "
                "check for crawl errors in Google Search Console, recent deployments, "
                "or marketing campaign pauses.")
    if pct < -10:
        return (f"Traffic is {abs(pct):.0f}% lower {period}. Worth investigating — "
                "check referral sources and any recent site changes.")
    if pct > 30:
        return f"🎉 Traffic is {abs(pct):.0f}% higher {period}! Check which sources drove the spike."
    return f"Traffic is {abs(pct):.0f}% {'higher' if pct > 0 else 'lower'} {period} — within normal range."


# ══════════════════════════════════════════════════════════════════════════════
# QUERY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_traffic_summary(days: int = 7) -> dict:
    """Overall traffic overview with daily trend."""
    result = run_report(
        metrics=["screenPageViews", "totalUsers", "sessions",
                 "averageSessionDuration", "bounceRate"],
        dimensions=["date"],
        days=days,
        cache_key=f"traffic_summary_{days}",
    )
    if "error" in result:
        return result

    rows = result["rows"]
    if not rows:
        return {"message": "No data found for this period.", "days": days}

    total_views    = sum(int(r.metric_values[0].value) for r in rows)
    total_users    = sum(int(r.metric_values[1].value) for r in rows)
    total_sessions = sum(int(r.metric_values[2].value) for r in rows)
    avg_duration   = sum(float(r.metric_values[3].value) for r in rows) / len(rows)
    avg_bounce     = sum(float(r.metric_values[4].value) for r in rows) / len(rows) * 100

    # Daily breakdown (sorted by date)
    daily = sorted([{
        "date": r.dimension_values[0].value,
        "views": int(r.metric_values[0].value),
        "users": int(r.metric_values[1].value),
    } for r in rows], key=lambda x: x["date"])

    # Find best/worst day
    best  = max(daily, key=lambda x: x["views"])
    worst = min(daily, key=lambda x: x["views"])

    return {
        "period": f"Last {days} days",
        "page_views": total_views,
        "users": total_users,
        "sessions": total_sessions,
        "avg_session_duration_sec": round(avg_duration, 0),
        "bounce_rate_pct": round(avg_bounce, 1),
        "daily": daily,
        "best_day": best,
        "worst_day": worst,
        "insights": [
            f"📊 {total_users:,} users · {total_sessions:,} sessions · {total_views:,} page views over {days} days.",
            f"⏱  Average session: {avg_duration/60:.1f} min — {_session_duration_insight(avg_duration)}",
            f"🏆 Best day: {best['date']} ({best['views']:,} views) | "
            f"Slowest: {worst['date']} ({worst['views']:,} views).",
            _bounce_insight(avg_bounce),
        ]
    }

def get_traffic_sources(days: int = 7) -> dict:
    """Traffic breakdown by source/medium."""
    result = run_report(
        metrics=["sessions", "totalUsers", "bounceRate"],
        dimensions=["sessionSource", "sessionMedium"],
        days=days,
        limit=15,
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        cache_key=f"traffic_sources_{days}",
    )
    if "error" in result:
        return result

    sources = [{
        "source": r.dimension_values[0].value,
        "medium": r.dimension_values[1].value,
        "sessions": int(r.metric_values[0].value),
        "users": int(r.metric_values[1].value),
        "bounce_pct": round(float(r.metric_values[2].value) * 100, 1),
    } for r in result["rows"]]

    total_sessions = sum(s["sessions"] for s in sources)
    for s in sources:
        s["share_pct"] = round(s["sessions"] / total_sessions * 100, 1) if total_sessions else 0

    top = sources[0] if sources else {}
    insights = [
        f"Top source: {top.get('source','?')}/{top.get('medium','?')} "
        f"({top.get('share_pct',0):.0f}% of sessions)." if top else "No source data.",
    ]
    # Flag heavy bounce sources
    high_bounce = [s for s in sources if s["bounce_pct"] > 70 and s["sessions"] > 10]
    if high_bounce:
        insights.append("⚠️  High-bounce sources (>70%): " +
                        ", ".join(f"{s['source']}/{s['medium']}" for s in high_bounce[:3]) +
                        ". Review landing pages for these channels.")

    return {"period": f"Last {days} days", "sources": sources, "insights": insights}

def get_realtime_users() -> dict:
    """Current active users."""
    config = load_config()
    if not config.get("connected"):
        return _not_connected()
    if not GA_SDK_AVAILABLE:
        return _sdk_missing()

    cached = cache_get("realtime", CACHE_TTL_REALTIME)
    if cached:
        return cached

    client = get_client()
    try:
        resp = client.run_realtime_report(RunRealtimeReportRequest(
            property=f"properties/{config['property_id']}",
            dimensions=[Dimension(name="country"), Dimension(name="deviceCategory")],
            metrics=[Metric(name="activeUsers")]
        ))
        breakdown = [{
            "country": r.dimension_values[0].value,
            "device": r.dimension_values[1].value,
            "users": int(r.metric_values[0].value),
        } for r in resp.rows]
        total = sum(b["users"] for b in breakdown)
        result = {
            "active_users": total,
            "breakdown": breakdown[:10],
            "status": "live",
            "insight": (f"🟢 {total} user{'s' if total != 1 else ''} on your site right now." if total
                        else "No active users at this moment.")
        }
        cache_set("realtime", result)
        return result
    except Exception as e:
        return _api_error(e, "realtime")

def get_bounce_rate(days: int = 7) -> dict:
    """Bounce rate by page."""
    result = run_report(
        metrics=["bounceRate", "screenPageViews", "averageSessionDuration"],
        dimensions=["pagePath"],
        days=days,
        limit=20,
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
        cache_key=f"bounce_rate_{days}",
    )
    if "error" in result:
        return result

    pages = [{
        "page": r.dimension_values[0].value,
        "bounce_pct": round(float(r.metric_values[0].value) * 100, 1),
        "views": int(r.metric_values[1].value),
        "avg_duration_sec": round(float(r.metric_values[2].value), 0),
    } for r in result["rows"]]

    high = sorted([p for p in pages if p["bounce_pct"] > 60], key=lambda x: x["bounce_pct"], reverse=True)
    low  = sorted([p for p in pages if p["bounce_pct"] < 40], key=lambda x: x["bounce_pct"])
    overall = sum(p["bounce_pct"] * p["views"] for p in pages) / max(sum(p["views"] for p in pages), 1)

    insights = [_bounce_insight(overall)]
    if high:
        insights.append(f"Pages needing attention: {', '.join(p['page'] for p in high[:3])} — bounce >60%.")
    if low:
        insights.append(f"Best-performing pages: {', '.join(p['page'] for p in low[:3])} — excellent engagement.")

    return {
        "period": f"Last {days} days",
        "overall_bounce_pct": round(overall, 1),
        "pages": pages,
        "high_bounce_pages": high[:5],
        "low_bounce_pages": low[:5],
        "insights": insights,
    }

def get_page_performance(days: int = 7, sort_by: str = "views") -> dict:
    """Best and worst performing pages."""
    order_metric = "screenPageViews" if sort_by == "views" else "averageSessionDuration"
    result = run_report(
        metrics=["screenPageViews", "totalUsers", "averageSessionDuration",
                 "bounceRate", "engagementRate"],
        dimensions=["pagePath", "pageTitle"],
        days=days,
        limit=25,
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_metric), desc=True)],
        cache_key=f"page_perf_{days}_{sort_by}",
    )
    if "error" in result:
        return result

    pages = [{
        "path": r.dimension_values[0].value,
        "title": r.dimension_values[1].value,
        "views": int(r.metric_values[0].value),
        "users": int(r.metric_values[1].value),
        "avg_duration_sec": round(float(r.metric_values[2].value), 0),
        "bounce_pct": round(float(r.metric_values[3].value) * 100, 1),
        "engagement_pct": round(float(r.metric_values[4].value) * 100, 1),
    } for r in result["rows"]]

    top5    = pages[:5]
    bottom5 = sorted(pages, key=lambda x: x["views"])[:5]

    return {
        "period": f"Last {days} days",
        "top_pages": top5,
        "bottom_pages": bottom5,
        "total_pages_analysed": len(pages),
        "insights": [
            f"Top page: {top5[0]['path']} — {top5[0]['views']:,} views." if top5 else "",
            (f"Most engaging: {max(pages, key=lambda x: x['engagement_pct'])['path']} "
             f"({max(pages, key=lambda x: x['engagement_pct'])['engagement_pct']:.0f}% engagement rate).")
            if pages else "",
        ]
    }

def get_device_breakdown(days: int = 7) -> dict:
    """Traffic by device category."""
    result = run_report(
        metrics=["sessions", "totalUsers", "bounceRate", "averageSessionDuration"],
        dimensions=["deviceCategory"],
        days=days,
        cache_key=f"devices_{days}",
    )
    if "error" in result:
        return result

    devices = [{
        "device": r.dimension_values[0].value.capitalize(),
        "sessions": int(r.metric_values[0].value),
        "users": int(r.metric_values[1].value),
        "bounce_pct": round(float(r.metric_values[2].value) * 100, 1),
        "avg_duration_sec": round(float(r.metric_values[3].value), 0),
    } for r in result["rows"]]

    total = sum(d["sessions"] for d in devices)
    for d in devices:
        d["share_pct"] = round(d["sessions"] / total * 100, 1) if total else 0

    mobile = next((d for d in devices if "mobile" in d["device"].lower()), None)
    desktop = next((d for d in devices if "desktop" in d["device"].lower()), None)

    insights = []
    if mobile and desktop:
        if mobile["share_pct"] > 60:
            insights.append(f"📱 {mobile['share_pct']:.0f}% mobile — ensure your site is fully mobile-optimised.")
        elif desktop["share_pct"] > 70:
            insights.append(f"🖥  {desktop['share_pct']:.0f}% desktop — mobile still worth optimising for growth.")
        if mobile and mobile["bounce_pct"] > desktop["bounce_pct"] + 15:
            insights.append("Mobile bounce rate is significantly higher than desktop — check mobile UX & load speed.")

    return {"period": f"Last {days} days", "devices": devices, "insights": insights}

def get_geo_data(days: int = 7) -> dict:
    """Traffic by country."""
    result = run_report(
        metrics=["sessions", "totalUsers", "bounceRate"],
        dimensions=["country"],
        days=days,
        limit=15,
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        cache_key=f"geo_{days}",
    )
    if "error" in result:
        return result

    countries = [{
        "country": r.dimension_values[0].value,
        "sessions": int(r.metric_values[0].value),
        "users": int(r.metric_values[1].value),
        "bounce_pct": round(float(r.metric_values[2].value) * 100, 1),
    } for r in result["rows"]]

    total = sum(c["sessions"] for c in countries)
    for c in countries:
        c["share_pct"] = round(c["sessions"] / total * 100, 1) if total else 0

    top = countries[0] if countries else {}
    return {
        "period": f"Last {days} days",
        "countries": countries,
        "insights": [
            f"🌍 Top country: {top.get('country','?')} ({top.get('share_pct',0):.0f}% of sessions)." if top else "",
            f"Audience spans {len(countries)} countries." if countries else "",
        ]
    }

def get_hourly_trends(days: int = 1) -> dict:
    """Hourly traffic distribution."""
    result = run_report(
        metrics=["sessions", "totalUsers"],
        dimensions=["hour"],
        days=days,
        order_by=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="hour"))],
        cache_key=f"hourly_{days}",
    )
    if "error" in result:
        return result

    hours = [{
        "hour": int(r.dimension_values[0].value),
        "sessions": int(r.metric_values[0].value),
        "users": int(r.metric_values[1].value),
    } for r in result["rows"]]

    if not hours:
        return {"message": "No hourly data available."}

    peak = max(hours, key=lambda x: x["sessions"])
    low  = min(hours, key=lambda x: x["sessions"])

    return {
        "period": f"Last {days} day(s)",
        "hours": hours,
        "peak_hour": peak,
        "low_hour": low,
        "insights": [
            f"🕐 Peak traffic at {peak['hour']:02d}:00 ({peak['sessions']} sessions).",
            f"Quietest at {low['hour']:02d}:00 ({low['sessions']} sessions) — good time for maintenance.",
        ]
    }

def get_daily_trends(days: int = 30) -> dict:
    """Day-by-day traffic with week-over-week comparison."""
    result = run_report(
        metrics=["sessions", "totalUsers", "screenPageViews"],
        dimensions=["date"],
        days=days,
        order_by=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))],
        cache_key=f"daily_trends_{days}",
    )
    if "error" in result:
        return result

    daily = [{
        "date": r.dimension_values[0].value,
        "sessions": int(r.metric_values[0].value),
        "users": int(r.metric_values[1].value),
        "views": int(r.metric_values[2].value),
    } for r in result["rows"]]

    if not daily:
        return {"message": "No daily data available."}

    # Week-over-week if enough data
    insights = []
    if len(daily) >= 14:
        this_week = daily[-7:]
        last_week = daily[-14:-7]
        tw_sessions = sum(d["sessions"] for d in this_week)
        lw_sessions = sum(d["sessions"] for d in last_week)
        pct = _pct_change(tw_sessions, lw_sessions)
        insights.append(f"This week vs last week: {_trend_label(pct)} ({pct:+.0f}%). "
                        + _traffic_drop_insight(pct, "vs last week"))

    avg = sum(d["sessions"] for d in daily) / len(daily)
    anomalies = [d for d in daily if d["sessions"] < avg * 0.5]
    if anomalies:
        dates = [d["date"] for d in anomalies]
        insights.append(f"⚠️  Unusually low traffic on: {', '.join(dates)}. Check for site issues or algorithm changes.")

    return {"period": f"Last {days} days", "daily": daily, "insights": insights}

def get_conversions(days: int = 7) -> dict:
    """Conversion events with rate analysis."""
    # Total users for rate calculation
    traffic_result = run_report(
        metrics=["totalUsers"],
        days=days,
        cache_key=f"total_users_{days}",
    )

    result = run_report(
        metrics=["eventCount", "totalUsers", "eventCountPerUser"],
        dimensions=["eventName"],
        days=days,
        limit=20,
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="eventCount"), desc=True)],
        cache_key=f"conversions_{days}",
    )
    if "error" in result:
        return result

    events = [{
        "event": r.dimension_values[0].value,
        "count": int(r.metric_values[0].value),
        "users": int(r.metric_values[1].value),
        "per_user": round(float(r.metric_values[2].value), 2),
    } for r in result["rows"]]

    total_users = 0
    if "rows" in traffic_result and traffic_result["rows"]:
        total_users = int(traffic_result["rows"][0].metric_values[0].value)

    # Likely conversion events (not standard GA noise)
    conversion_keywords = ["purchase", "sign_up", "subscribe", "lead", "submit", "register",
                          "checkout", "add_to_cart", "complete", "goal"]

    likely_conversions = [e for e in events if any(k in e["event"].lower() for k in conversion_keywords)]
    other_events = [e for e in events if not any(k in e["event"].lower() for k in conversion_keywords)]

    insights = []
    if likely_conversions:
        conv = likely_conversions[0]
        rate = (conv["users"] / total_users * 100) if total_users else 0
        insights.append(f"🎯 Top conversion: {conv['event']} — {conv['users']:,} completions "
                        f"({rate:.1f}% conversion rate).")
    else:
        insights.append("No standard conversion events detected. "
                        "Track purchases, signups, or goals via GA4 events.")

    return {
        "period": f"Last {days} days",
        "total_users": total_users,
        "conversion_events": likely_conversions[:10],
        "other_events": other_events[:10],
        "insights": insights
    }

def get_funnel_analysis(days: int = 7) -> dict:
    """Simple conversion funnel analysis."""
    result = run_report(
        metrics=["totalUsers", "sessions", "conversions"],
        dimensions=["date"],
        days=days,
        cache_key=f"funnel_{days}",
    )
    if "error" in result:
        return result

    rows = result["rows"]
    if not rows:
        return {"message": "Not enough data for funnel analysis."}

    total_users = sum(int(r.metric_values[0].value) for r in rows)
    total_sessions = sum(int(r.metric_values[1].value) for r in rows)
    total_conversions = sum(int(r.metric_values[2].value) for r in rows)

    # Calculate rates
    visitor_to_session = (total_sessions / total_users * 100) if total_users else 0
    session_to_conv = (total_conversions / total_sessions * 100) if total_sessions else 0
    overall_conv = (total_conversions / total_users * 100) if total_users else 0

    return {
        "period": f"Last {days} days",
        "visitors": total_users,
        "sessions": total_sessions,
        "conversions": total_conversions,
        "rates": {
            "visitor_to_session_pct": round(visitor_to_session, 1),
            "session_to_conversion_pct": round(session_to_conv, 2),
            "overall_conversion_pct": round(overall_conv, 2),
        },
        "insights": [
            f"📊 {visitor_to_session:.1f}% of visitors start a session.",
            f"🎯 {session_to_conv:.2f}% of sessions convert.",
            f"📈 Overall conversion rate: {overall_conv:.2f}%.",
            "Funnel tip: Focus on the biggest drop-off step for biggest impact."
        ]
    }

def compare_periods(period1_days: int = 7, period2_days: int = 7) -> dict:
    """Compare two time periods."""
    # Get data for period 1 (more recent)
    p1 = run_report(
        metrics=["sessions", "totalUsers", "screenPageViews", "bounceRate"],
        days=period1_days,
        cache_key=f"compare_p1_{period1_days}",
    )
    # Get data for period 2 (older)
    p2 = run_report(
        metrics=["sessions", "totalUsers", "screenPageViews", "bounceRate"],
        days=period2_days,
        cache_key=f"compare_p2_{period2_days}",
    )

    if "error" in p1:
        return p1
    if "error" in p2:
        return p2

    # Extract totals
    def extract_totals(r):
        return {
            "sessions": sum(int(row.metric_values[0].value) for row in r["rows"]),
            "users": sum(int(row.metric_values[1].value) for row in r["rows"]),
            "views": sum(int(row.metric_values[2].value) for row in r["rows"]),
            "bounce": sum(float(row.metric_values[3].value) * int(row.metric_values[0].value) for row in r["rows"]) /
                      max(sum(int(row.metric_values[0].value) for row in r["rows"]), 1) * 100,
        }

    d1 = extract_totals(p1)
    d2 = extract_totals(p2)

    def diff_label(current, previous, metric):
        pct = _pct_change(current, previous)
        return {
            "metric": metric,
            "current": current,
            "previous": previous,
            "change_pct": pct,
            "label": _trend_label(pct),
        }

    return {
        "period_1": f"Last {period1_days} days",
        "period_2": f"Previous {period2_days} days",
        "comparison": {
            "sessions": diff_label(d1["sessions"], d2["sessions"], "sessions"),
            "users": diff_label(d1["users"], d2["users"], "users"),
            "page_views": diff_label(d1["views"], d2["views"], "page views"),
            "bounce_rate": diff_label(d1["bounce"], d2["bounce"], "bounce rate"),
        },
        "summary": (
            f"Traffic {diff_label(d1['sessions'], d2['sessions'], 'sessions')['label']} "
            f"({diff_label(d1['sessions'], d2['sessions'], 'sessions')['change_pct']:+.0f}%) "
            f"compared to the previous period."
        )
    }

def analyze_traffic_drop(days: int = 7) -> dict:
    """Compare recent period with same period earlier."""
    return compare_periods(days, days)


# ══════════════════════════════════════════════════════════════════════════════
# NATURAL LANGUAGE PARSER
# ══════════════════════════════════════════════════════════════════════════════

def _parse_period(text: str) -> int:
    """Extract day count from natural language."""
    text = text.lower()
    numbers = re.findall(r'(\d+)', text)
    if numbers:
        num = int(numbers[0])
        if 'hour' in text:
            return min(num // 24 + 1, 30)
        if 'day' in text:
            return min(num, 365)
        if 'week' in text:
            return min(num * 7, 90)
        if 'month' in text:
            return min(num * 30, 365)
    # Default: 7 days
    return 7

def _extract_intent(text: str) -> tuple:
    """Return (intent, params) tuple."""
    text = text.lower().strip()

    # Realtime
    if any(w in text for w in ['realtime', 'right now', 'current', 'live', 'active', 'online']):
        return ('realtime', {})

    # Bounce rate
    if any(w in text for w in ['bounce', 'bouncing']):
        days = _parse_period(text)
        return ('bounce', {'days': days})

    # Pages / page performance
    if any(w in text for w in ['page', 'pages', 'best page', 'worst page', 'top page']):
        days = _parse_period(text)
        sort = 'duration' if 'engag' in text or 'time' in text else 'views'
        return ('pages', {'days': days, 'sort_by': sort})

    # Devices
    if any(w in text for w in ['device', 'mobile', 'desktop', 'tablet', 'phone']):
        days = _parse_period(text)
        return ('devices', {'days': days})

    # Geography / countries / location
    if any(w in text for w in ['country', 'countries', 'geo', 'location', 'where', 'nation']):
        days = _parse_period(text)
        return ('geo', {'days': days})

    # Hourly
    if any(w in text for w in ['hour', 'hourly', 'time of day', 'when']):
        days = _parse_period(text)
        return ('hourly', {'days': days})

    # Daily trends / over time
    if any(w in text for w in ['trend', 'daily', 'over time', 'history', 'past']):
        days = _parse_period(text)
        return ('daily', {'days': days})

    # Conversions / goals / events
    if any(w in text for w in ['convert', 'conversion', 'goal', 'purchase', 'sign up', 'signup',
                                'event', 'complete', 'submit', 'funnel']):
        days = _parse_period(text)
        if 'funnel' in text:
            return ('funnel', {'days': days})
        return ('conversions', {'days': days})

    # Traffic drop / why / decrease
    if any(w in text for w in ['drop', 'down', 'decrease', 'lower', 'less', 'why', 'dropped']):
        days = _parse_period(text)
        return ('drop', {'days': days})

    # Compare periods
    if any(w in text for w in ['compare', 'vs', 'versus', 'difference', 'change']):
        # Try to extract two periods
        periods = re.findall(r'(\d+)\s*(day|week|month)', text)
        if len(periods) >= 2:
            p1 = periods[0][0]
            p2 = periods[1][0]
            unit = periods[0][1]
            mult = 1 if unit == 'day' else 7 if unit == 'week' else 30
            p2_mult = 1 if periods[1][1] == 'day' else 7 if periods[1][1] == 'week' else 30
            return ('compare', {'period1': int(p1)*mult, 'period2': int(p2)*p2_mult})
        return ('compare', {'period1': 7, 'period2': 7})

    # Sources / traffic source / where from
    if any(w in text for w in ['source', 'sources', 'referral', 'medium', 'channel', 'where from']):
        days = _parse_period(text)
        return ('sources', {'days': days})

    # Default: traffic summary
    days = _parse_period(text)
    return ('traffic', {'days': days})


# ══════════════════════════════════════════════════════════════════════════════
# MAIN HANDLER
# ══════════════════════════════════════════════════════════════════════════════

def handle_query(user_input: str) -> dict:
    """
    Main entry point for natural language queries.
    Returns a dict with structured data and actionable insights.
    """
    if not user_input or not user_input.strip():
        return {"message": "Ask me about your analytics! Try: 'how's traffic?', "
                          "'what's my bounce rate?', or 'compare last week to the week before.'"}

    intent, params = _extract_intent(user_input)
    days = params.get('days', 7)

    try:
        if intent == 'realtime':
            return get_realtime_users()

        if intent == 'bounce':
            return get_bounce_rate(days)

        if intent == 'pages':
            return get_page_performance(days, params.get('sort_by', 'views'))

        if intent == 'devices':
            return get_device_breakdown(days)

        if intent == 'geo':
            return get_geo_data(days)

        if intent == 'hourly':
            return get_hourly_trends(days)

        if intent == 'daily':
            return get_daily_trends(days)

        if intent == 'conversions':
            return get_conversions(days)

        if intent == 'funnel':
            return get_funnel_analysis(days)

        if intent == 'drop':
            return analyze_traffic_drop(days)

        if intent == 'compare':
            return compare_periods(params.get('period1', 7), params.get('period2', 7))

        if intent == 'sources':
            return get_traffic_sources(days)

        # Default: traffic summary
        return get_traffic_summary(days)

    except Exception as e:
        return _api_error(e, f"intent={intent}")


# ══════════════════════════════════════════════════════════════════════════════
# CLI / MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GA Insights CLI")
    sub = parser.add_subparsers(dest="command", help="Commands")

    # Setup
    sub.add_parser("setup", help="Show setup guide")
    sub.add_parser("status", help="Check connection status")

    # Queries
    p = sub.add_parser("traffic", help="Traffic summary")
    p.add_argument("--days", type=int, default=7)

    p = sub.add_parser("sources", help="Traffic sources")
    p.add_argument("--days", type=int, default=7)

    p = sub.add_parser("realtime", help="Active users now")
    sub.add_parser("bounce", help="Bounce rate analysis")
    sub.add_parser("pages", help="Page performance")
    sub.add_parser("devices", help="Device breakdown")
    sub.add_parser("geo", help="Geographic data")
    sub.add_parser("hourly", help="Hourly trends")
    sub.add_parser("daily", help="Daily trends")
    sub.add_parser("conversions", help="Conversion events")
    sub.add_parser("funnel", help="Funnel analysis")

    p = sub.add_parser("compare", help="Compare periods")
    p.add_argument("--period1", type=int, default=7, help="Recent period days")
    p.add_argument("--period2", type=int, default=7, help="Previous period days")

    p = sub.add_parser("drop", help="Traffic drop analysis")
    p.add_argument("--days", type=int, default=7)

    sub.add_parser("cache", help="Clear cache")

    # Query mode
    sub.add_parser("query", help="Natural language query")
    sub.add_argument("query", nargs="...", help="Query string")

    args = parser.parse_args()

    # Helper to print JSON
    def out(data):
        print(json.dumps(data, indent=2, default=str))

    if args.command == "setup":
        out(setup_guide())

    elif args.command == "status":
        out(load_config())

    elif args.command == "traffic":
        out(get_traffic_summary(args.days))

    elif args.command == "sources":
        out(get_traffic_sources(args.days))

    elif args.command == "realtime":
        out(get_realtime_users())

    elif args.command == "bounce":
        out(get_bounce_rate())

    elif args.command == "pages":
        out(get_page_performance())

    elif args.command == "devices":
        out(get_device_breakdown())

    elif args.command == "geo":
        out(get_geo_data())

    elif args.command == "hourly":
        out(get_hourly_trends())

    elif args.command == "daily":
        out(get_daily_trends())

    elif args.command == "conversions":
        out(get_conversions())

    elif args.command == "funnel":
        out(get_funnel_analysis())

    elif args.command == "compare":
        out(compare_periods(args.period1, args.period2))

    elif args.command == "drop":
        out(analyze_traffic_drop(args.days))

    elif args.command == "cache":
        out(cache_clear())

    elif args.command == "query":
        # Join remaining args into query string
        query = " ".join(args.query)
        out(handle_query(query))

    else:
        parser.print_help()
