#!/usr/bin/env python3
"""
write_report.py — turn collect_stats.py JSON into a readable markdown report.

Stdlib only. No network. Reads the JSON on stdin (or a --in file) and writes a
plain-English weekly clinic activity report to stdout (or --out file).

This is the deterministic fallback so the skill produces a report even headless.
When run by an AI assistant, the assistant can add narrative interpretation on top
of (or instead of) this — see SKILL.md.

Usage:
    python3 collect_stats.py | python3 write_report.py --out output/ClinicReport.md
    python3 write_report.py --in stats.json
"""
import argparse
import json
import sys
from datetime import datetime, timezone

SILENCE_DAYS = 3  # flag a hardware device silent if no report in this many days


def fw_tuple(v):
    """Normalize a firmware string to a tuple of ints for comparison, so
    '0.8.13' and '0.8.13.0' compare equal (trailing zeros ignored)."""
    if not v:
        return ()
    parts = []
    for p in str(v).split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    while parts and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def iso_days_ago(iso):
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except (ValueError, AttributeError):
        return None


def bar(n, maxn, width=24):
    if not maxn:
        return ""
    return "█" * max(1, round(n / maxn * width)) if n else ""


def build(d):
    L = []
    org = d.get("organizationName") or "your clinic"
    w = d["window"]
    start, end = w["start"][:10], w["end"][:10]
    t = d["totals"]
    cur, prev, trend = t["recordings"], t["previousRecordings"], t.get("trendPct")

    L.append(f"# Clinic Activity Report — {org}")
    L.append("")
    L.append(f"**Window:** {start} → {end}  ·  {w['days']} days  ·  timezone {d['timezone']}")
    L.append(f"*Read-only snapshot — nothing was sent or changed.*")
    L.append("")

    # Headline
    L.append("## At a glance")
    L.append("")
    if trend is None:
        trend_txt = "(no prior-period data to compare)"
    elif trend > 0:
        trend_txt = f"↑ {trend}% vs the previous {w['days']} days"
    elif trend < 0:
        trend_txt = f"↓ {abs(trend)}% vs the previous {w['days']} days"
    else:
        trend_txt = "flat vs the previous period"
    L.append(f"- **{cur} recordings** this period  ·  {trend_txt}")
    L.append(f"- Previous period: {prev} recordings")
    hw = [x for x in d["devices"] if x.get("isHardware")]
    L.append(f"- {len(hw)} recording device(s) in the clinic")
    L.append("")

    # By device
    bd = d["breakdown"]["byDevice"]
    if bd:
        L.append("## Recordings by device")
        L.append("")
        maxn = max(bd.values())
        for name, n in bd.items():
            L.append(f"- **{name}** — {n}  `{bar(n, maxn)}`")
        L.append("")

    # By weekday
    bw = d["breakdown"]["byWeekday"]
    if any(bw.values()):
        L.append("## Busiest days")
        L.append("")
        maxn = max(bw.values())
        for day, n in bw.items():
            L.append(f"- {day} — {n}  `{bar(n, maxn, 20)}`")
        busiest = max(bw, key=bw.get)
        L.append("")
        L.append(f"Busiest day: **{busiest}**.")
        L.append("")

    # Busiest hours (top 3)
    bh = {int(k): v for k, v in d["breakdown"]["byHour"].items()}
    if any(bh.values()):
        top = sorted(bh.items(), key=lambda kv: kv[1], reverse=True)[:3]
        top = [(h, n) for h, n in top if n]
        if top:
            def hr(h):
                ap = "am" if h < 12 else "pm"
                hh = h % 12 or 12
                return f"{hh}{ap}"
            parts = ", ".join(f"{hr(h)} ({n})" for h, n in top)
            L.append(f"Busiest times of day: {parts}.")
            L.append("")

    # Health flags
    flags = []
    for dev in hw:
        age = iso_days_ago(dev.get("lastReport"))
        label = dev.get("name") or dev.get("serial")
        if age is None:
            flags.append(f"⚠️ **{label}** — no report time on record.")
        elif age >= SILENCE_DAYS:
            flags.append(f"⚠️ **{label}** — silent for {age} days (last report {dev['lastReport'][:10]}).")
        fw, tfw = dev.get("firmware"), dev.get("targetFirmware")
        if fw and tfw and fw_tuple(fw) != fw_tuple(tfw):
            flags.append(f"⚠️ **{label}** — firmware {fw} (target {tfw}); may need an update.")
    for wh in d.get("webhooks", []):
        if wh.get("recentFailures"):
            flags.append(f"⚠️ Webhook `{wh.get('url')}` — "
                         f"{wh['recentFailures']}/{wh['recentDeliveries']} recent deliveries failed.")

    L.append("## Health check")
    L.append("")
    if flags:
        L.extend(flags)
    else:
        L.append("✅ No device or webhook issues detected.")
    L.append("")

    L.append("---")
    L.append("*Generated locally by the NxVET clinic-activity-report skill. "
             "Figures come from your NxVET data via read-only API calls.*")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile")
    ap.add_argument("--out", dest="outfile")
    args = ap.parse_args()
    raw = open(args.infile).read() if args.infile else sys.stdin.read()
    d = json.loads(raw)
    report = build(d)
    if args.outfile:
        import os
        os.makedirs(os.path.dirname(args.outfile) or ".", exist_ok=True)
        with open(args.outfile, "w") as f:
            f.write(report)
        print(args.outfile)
    else:
        sys.stdout.write(report)


if __name__ == "__main__":
    main()
