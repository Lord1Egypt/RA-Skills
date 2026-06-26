#!/usr/bin/env python3
"""
baseline_drift.py — Detect when current 30-day metrics drift from the 90-day baseline.

Reads ~/.activecampaign-skill/state.json (calibrated baseline). Pulls last
30 days of campaigns, compares aggregates, flags drift > 1σ.

Usage:
  python3 baseline_drift.py
  python3 baseline_drift.py --window-days 30 --format json
"""

from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

from _ac_client import ACClient, load_state
from _ac_client import safe_int as _safe_int


def _parse_iso(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def fetch_recent(client: ACClient, days: int) -> list:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    campaigns = client.paginate("campaigns", "campaigns", max_items=5000)
    return [c for c in campaigns if _parse_iso(c.get("sdate") or c.get("ldate")) and (_parse_iso(c.get("sdate") or c.get("ldate")) >= cutoff)]


def aggregate(campaigns: list) -> dict:
    open_rates = []
    click_rates = []
    unsub_rates = []
    for c in campaigns:
        sent = _safe_int(c.get("send_amt"))
        if sent <= 0:
            continue
        open_rates.append(_safe_int(c.get("uniqueopens")) / sent)
        click_rates.append(_safe_int(c.get("uniquelinkclicks")) / sent)
        unsub_rates.append(_safe_int(c.get("unsubscribes")) / sent)
    return {
        "campaigns": len(campaigns),
        "open_rate_mean": statistics.mean(open_rates) if open_rates else None,
        "click_rate_mean": statistics.mean(click_rates) if click_rates else None,
        "unsub_rate_mean": statistics.mean(unsub_rates) if unsub_rates else None,
    }


def analyze(current: dict, baseline: dict) -> dict:
    drifts = []
    for metric, base_key in [
        ("open_rate_mean", "open_rate_p50"),
        ("click_rate_mean", "click_rate_p50"),
        ("unsub_rate_mean", "unsub_rate"),
    ]:
        cur = current.get(metric)
        base = baseline.get(base_key)
        if cur is None or base is None:
            continue
        delta_pp = (cur - base) * 100
        drifts.append({
            "metric": metric,
            "current": cur,
            "baseline": base,
            "delta_pp": delta_pp,
            "significant": abs(delta_pp) >= 5,
        })
    return {"current": current, "baseline_used": baseline, "drifts": drifts}


def render_markdown(r: dict) -> str:
    lines = [
        "# Baseline Drift Check",
        "",
        f"Campaigns in current window: {r['current']['campaigns']}",
        "",
        "| Metric | Current | Baseline | Δ pp | Significant? |",
        "|---|---|---|---|---|",
    ]
    for d in r["drifts"]:
        cur = d["current"] * 100 if d["current"] is not None else None
        base = d["baseline"] * 100 if d["baseline"] is not None else None
        lines.append(
            f"| {d['metric']} | "
            f"{f'{cur:.2f}%' if cur is not None else '—'} | "
            f"{f'{base:.2f}%' if base is not None else '—'} | "
            f"{d['delta_pp']:+.2f} | {'⚠ yes' if d['significant'] else 'no'} |"
        )
    if not r["drifts"]:
        lines.append("_(Insufficient current-window data to compute drift.)_")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Detect baseline drift")
    parser.add_argument("--window-days", type=int, default=30)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    state = load_state() or {}
    baseline = state.get("baselines", {})
    client = ACClient()
    campaigns = fetch_recent(client, args.window_days)
    cur = aggregate(campaigns)
    r = analyze(cur, baseline)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
