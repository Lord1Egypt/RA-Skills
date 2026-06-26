#!/usr/bin/env python3
"""
subject_line_report.py — Cluster subject lines by pattern, rank by lift.

Tags each subject for length, emoji, personalization, question/statement,
urgency words, all-caps. Computes mean open rate per pattern vs. baseline.

Usage:
  python3 subject_line_report.py
  python3 subject_line_report.py --days 90 --format json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean

from _ac_client import ACClient
from _ac_client import safe_int as _safe_int

URGENCY_WORDS = re.compile(r"\b(now|today|hurry|last\s+chance|ends|deadline|urgent|limited|expir)\b", re.I)
PERSONALIZATION = re.compile(r"%[A-Z_]+%|\{\{[^}]+\}\}")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F600-\U0001F64F]")


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


def fetch(client: ACClient, days: int) -> list:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    campaigns = client.paginate("campaigns", "campaigns", max_items=5000)
    out = []
    for c in campaigns:
        d = _parse_iso(c.get("sdate") or c.get("ldate"))
        if d and d >= cutoff and _safe_int(c.get("send_amt")) > 0:
            out.append(c)
    return out


def features(subject: str) -> dict:
    s = subject or ""
    return {
        "length": len(s),
        "word_count": len(s.split()),
        "has_emoji": bool(EMOJI_RE.search(s)),
        "has_question": "?" in s,
        "has_personalization": bool(PERSONALIZATION.search(s)),
        "has_urgency": bool(URGENCY_WORDS.search(s)),
        "is_caps": s.isupper() and len(s) > 5,
    }


def analyze(campaigns: list) -> dict:
    rows = []
    overall_open = []
    for c in campaigns:
        sent = _safe_int(c.get("send_amt"))
        if sent <= 0:
            continue
        ouroboros = _safe_int(c.get("uniqueopens"))
        open_rate = ouroboros / sent
        overall_open.append(open_rate)
        f = features(c.get("subject") or "")
        rows.append({"open_rate": open_rate, "sent": sent, **f, "subject": c.get("subject")})

    baseline = mean(overall_open) if overall_open else 0
    patterns = {}
    for tag in ["has_emoji", "has_question", "has_personalization", "has_urgency", "is_caps"]:
        with_tag = [r["open_rate"] for r in rows if r[tag]]
        without_tag = [r["open_rate"] for r in rows if not r[tag]]
        patterns[tag] = {
            "n_with": len(with_tag),
            "n_without": len(without_tag),
            "open_rate_with": mean(with_tag) if with_tag else None,
            "open_rate_without": mean(without_tag) if without_tag else None,
            "lift_pp": (mean(with_tag) - mean(without_tag)) * 100 if with_tag and without_tag else None,
        }

    # length buckets
    short = [r["open_rate"] for r in rows if r["length"] <= 30]
    medium = [r["open_rate"] for r in rows if 30 < r["length"] <= 60]
    long_ = [r["open_rate"] for r in rows if r["length"] > 60]
    length_buckets = {
        "<=30": (mean(short) if short else None, len(short)),
        "31-60": (mean(medium) if medium else None, len(medium)),
        ">60": (mean(long_) if long_ else None, len(long_)),
    }

    return {
        "campaigns_analyzed": len(rows),
        "baseline_open_rate": baseline,
        "patterns": patterns,
        "length_buckets": length_buckets,
        "all_subjects": [{"subject": r["subject"], "open_rate": r["open_rate"]} for r in rows][:50],
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Subject Line Report",
        "",
        f"- Campaigns analyzed: {r['campaigns_analyzed']}",
        f"- Baseline open rate (this window): {r['baseline_open_rate']*100:.1f}%",
        "",
        "## Pattern lift",
        "| Pattern | n with | n w/o | Open w/ | Open w/o | Lift |",
        "|---|---|---|---|---|---|",
    ]
    for k, p in r["patterns"].items():
        ow = f"{p['open_rate_with']*100:.1f}%" if p["open_rate_with"] is not None else "—"
        owt = f"{p['open_rate_without']*100:.1f}%" if p["open_rate_without"] is not None else "—"
        lift = f"{p['lift_pp']:+.1f}pp" if p["lift_pp"] is not None else "—"
        lines.append(f"| {k} | {p['n_with']} | {p['n_without']} | {ow} | {owt} | {lift} |")
    lines.append("")
    lines.append("## Length buckets")
    for label, (rate, n) in r["length_buckets"].items():
        rate_s = f"{rate*100:.1f}%" if rate is not None else "—"
        lines.append(f"- {label} chars: {rate_s} ({n} sends)")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Subject line pattern analysis")
    parser.add_argument("--days", type=int, default=90)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    campaigns = fetch(client, args.days)
    r = analyze(campaigns)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
