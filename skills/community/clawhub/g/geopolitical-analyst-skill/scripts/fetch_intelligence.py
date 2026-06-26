#!/usr/bin/env python3
"""
geopolitical-analyst: Full Intelligence Data Fetcher
Fetches GDELT (articles, tone, volume, language, divergence), ACLED, ReliefWeb, and economic data.

Usage:
  python fetch_intelligence.py --topic "Sudan conflict" --country Sudan --country-code SD \
    [--currency SDG] [--acled-key KEY --acled-email EMAIL] [--appname YOUR_APP]
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path


GDELT_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"
ACLED_BASE = "https://api.acleddata.com/acled/read/"
RELIEFWEB_BASE = "https://api.reliefweb.int/v2/reports"
FRANKFURTER_BASE = "https://api.frankfurter.app"


def _get(url: str, timeout: int = 15) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "geopolitical-analyst/2.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e), "url": url}


def _post(url: str, payload: dict, timeout: int = 15) -> dict:
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data, method="POST",
                                      headers={"Content-Type": "application/json",
                                               "User-Agent": "geopolitical-analyst/2.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e), "url": url}


def gdelt_articles(query: str, max_records: int = 25, country_code: str = None) -> dict:
    p = {"query": query, "mode": "artlist", "maxrecords": max_records, "format": "json"}
    if country_code:
        p["sourcecountry"] = country_code
    time.sleep(5)
    return _get(f"{GDELT_BASE}?{urllib.parse.urlencode(p)}")


def gdelt_tone(query: str, country_code: str = None, smooth: int = 3) -> dict:
    p = {"query": query, "mode": "timelinetone", "format": "json", "TIMELINESMOOTH": smooth}
    if country_code:
        p["sourcecountry"] = country_code
    time.sleep(5)
    return _get(f"{GDELT_BASE}?{urllib.parse.urlencode(p)}")


def gdelt_volume(query: str, country_code: str = None) -> dict:
    p = {"query": query, "mode": "timelinevol", "format": "json"}
    if country_code:
        p["sourcecountry"] = country_code
    time.sleep(5)
    return _get(f"{GDELT_BASE}?{urllib.parse.urlencode(p)}")


def gdelt_lang_dist(query: str) -> dict:
    p = {"query": query, "mode": "timelinelang", "format": "json"}
    time.sleep(5)
    return _get(f"{GDELT_BASE}?{urllib.parse.urlencode(p)}")


def parse_tone_series(raw: dict) -> dict:
    try:
        series = raw.get("timeline", [{}])[0].get("data", [])
        if not series:
            return {"error": "No data"}
        values = [pt["value"] for pt in series if "value" in pt]
        if not values:
            return {"error": "No values"}
        current = values[-1]
        avg7 = sum(values[-7:]) / min(7, len(values))
        trend = values[-1] - values[max(0, len(values) - 7)]
        return {
            "current": round(current, 2),
            "avg_7d": round(avg7, 2),
            "trend_7d": round(trend, 2),
            "direction": "deteriorating" if trend < -0.5 else "improving" if trend > 0.5 else "stable",
            "level": (
                "ACTIVE_CRISIS" if current < -10 else
                "PRE_CRISIS" if current < -8 else
                "HIGH_TENSION" if current < -5 else
                "ELEVATED_FRICTION" if current < -2 else
                "NEUTRAL"
            ),
        }
    except Exception as e:
        return {"error": str(e)}


def compute_nds(global_tone: dict, local_tone: dict) -> dict:
    """Narrative Divergence Score."""
    try:
        g = global_tone.get("current", 0)
        l = local_tone.get("current", 0)
        nds = abs(g - l)
        return {
            "score": round(nds, 2),
            "global_tone": g,
            "local_tone": l,
            "interpretation": (
                "ACTIVE_INFO_OPS" if nds > 8 else
                "SIGNIFICANT_DIVERGENCE" if nds > 5 else
                "MODERATE_DIVERGENCE" if nds > 2 else
                "CONSISTENT_NARRATIVE"
            ),
            "flag": nds > 5,
        }
    except Exception as e:
        return {"error": str(e)}


def fetch_currency(currency_code: str) -> dict:
    """Exchange rate trend from Frankfurter (ECB-backed, free)."""
    try:
        # Latest rate vs USD
        latest = _get(f"{FRANKFURTER_BASE}/latest?from={currency_code}&to=USD")

        # 90-day history
        start = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
        history = _get(f"{FRANKFURTER_BASE}/{start}..?from={currency_code}&to=USD")

        rates = list(history.get("rates", {}).values())
        usd_rates = [r.get("USD", 0) for r in rates if isinstance(r, dict)]

        if len(usd_rates) >= 2:
            change_90d = ((usd_rates[-1] - usd_rates[0]) / usd_rates[0]) * 100
            trend = "depreciating" if change_90d < -5 else "appreciating" if change_90d > 5 else "stable"
        else:
            change_90d = 0
            trend = "unknown"

        return {
            "currency": currency_code,
            "current_vs_usd": latest.get("rates", {}).get("USD"),
            "change_90d_pct": round(change_90d, 2),
            "trend": trend,
            "pressure_signal": (
                "CRISIS" if abs(change_90d) > 30 else
                "HIGH" if abs(change_90d) > 15 else
                "MODERATE" if abs(change_90d) > 5 else
                "LOW"
            ),
        }
    except Exception as e:
        return {"error": str(e), "currency": currency_code}


def acled_events(country: str, api_key: str, email: str, limit: int = 20) -> dict:
    p = {
        "key": api_key, "email": email, "country": country, "limit": limit,
        "fields": "event_date|event_type|sub_event_type|actor1|actor2|location|admin1|fatalities|notes|source",
        "format": "json",
    }
    return _get(f"{ACLED_BASE}?{urllib.parse.urlencode(p)}")


def reliefweb_reports(keyword: str, country: str = None, appname: str = "geopolitical-analyst") -> dict:
    url = f"{RELIEFWEB_BASE}?appname={urllib.parse.quote(appname)}"
    payload = {
        "query": {"value": keyword},
        "limit": 10,
        "sort": ["date:desc"],
        "fields": {"include": ["title", "date", "source", "url", "body"]},
    }
    if country:
        payload["filter"] = {"field": "country.name", "value": country}
    return _post(url, payload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--country", default=None)
    parser.add_argument("--country-code", default=None, help="ISO 3166-1 alpha-2 (e.g. SD, IR, UA)")
    parser.add_argument("--currency", default=None, help="ISO 4217 currency code (e.g. IRR, UAH, SDG)")
    parser.add_argument("--acled-key", default=None)
    parser.add_argument("--acled-email", default=None)
    parser.add_argument("--appname", default="geopolitical-analyst")
    args = parser.parse_args()

    results = {
        "query": args.topic,
        "country": args.country,
        "country_code": args.country_code,
        "fetched_at": datetime.utcnow().isoformat(),
        "sources": {},
    }

    print(f"[1/8] GDELT articles (global)...", file=sys.stderr)
    results["sources"]["gdelt_articles"] = gdelt_articles(args.topic)

    print(f"[2/8] GDELT tone (global)...", file=sys.stderr)
    tone_global_raw = gdelt_tone(args.topic)
    results["sources"]["gdelt_tone_global"] = parse_tone_series(tone_global_raw)

    if args.country_code:
        print(f"[3/8] GDELT tone (local: {args.country_code})...", file=sys.stderr)
        tone_local_raw = gdelt_tone(args.topic, country_code=args.country_code)
        results["sources"]["gdelt_tone_local"] = parse_tone_series(tone_local_raw)

        print(f"[4/8] Narrative Divergence Score...", file=sys.stderr)
        results["sources"]["narrative_divergence"] = compute_nds(
            results["sources"]["gdelt_tone_global"],
            results["sources"]["gdelt_tone_local"],
        )
    else:
        results["sources"]["gdelt_tone_local"] = {"status": "skipped", "reason": "No country_code"}
        results["sources"]["narrative_divergence"] = {"status": "skipped"}

    print(f"[5/8] GDELT language distribution...", file=sys.stderr)
    results["sources"]["gdelt_lang_dist"] = gdelt_lang_dist(args.topic)

    print(f"[6/8] ACLED events...", file=sys.stderr)
    if args.acled_key and args.acled_email and args.country:
        results["sources"]["acled"] = acled_events(args.country, args.acled_key, args.acled_email)
    else:
        results["sources"]["acled"] = {"status": "skipped", "reason": "No key/email/country"}

    print(f"[7/8] ReliefWeb reports...", file=sys.stderr)
    results["sources"]["reliefweb"] = reliefweb_reports(args.topic, args.country, args.appname)

    print(f"[8/8] Economic indicators...", file=sys.stderr)
    if args.currency:
        results["sources"]["currency"] = fetch_currency(args.currency)
    else:
        results["sources"]["currency"] = {"status": "skipped", "reason": "No --currency provided"}

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
