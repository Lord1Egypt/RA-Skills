#!/usr/bin/env python3
"""
notes_analysis.py — Content analysis of contact + deal notes.

Pulls /notes (per-AC-v3 docs the response key is `notes` and per-item
`reltype` is the string class name: `Deal`, `Subscriber` (i.e. contact),
or `Activity`). Surfaces:

  - total notes by reltype, by user
  - median note length per user (depth proxy)
  - notes with action-item language ("follow up", "next step", "send",
    "call back", etc.)
  - top recurring vocabulary across notes (lightweight word frequency)
  - stale-note flag: deals whose most-recent note is older than N days

No NLP — frequency + keyword matching only. The script is read-only.

Usage:
  python3 notes_analysis.py
  python3 notes_analysis.py --stale-days 30
  python3 notes_analysis.py --format json --output notes_analysis.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from _ac_client import ACClient, ACClientError, emit_files, render_feature_unavailable
from _ac_client import parse_date as _parse_date

ACTION_PATTERNS = (
    r"\bfollow ?up\b",
    r"\bnext step\b",
    r"\bcall back\b",
    r"\bcall (?:them|him|her|on)\b",
    r"\bsend (?:over|the|them)?\b",
    r"\bemail (?:them|him|her)?\b",
    r"\bschedule\b",
    r"\bbook\b",
    r"\bremind(?:er)?\b",
    r"\btodo\b",
    r"\bto[- ]do\b",
)
ACTION_RE = re.compile("|".join(ACTION_PATTERNS), re.IGNORECASE)

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "for", "in", "on",
    "with", "is", "was", "are", "be", "been", "being", "this", "that",
    "these", "those", "i", "you", "we", "they", "he", "she", "it",
    "have", "has", "had", "will", "would", "could", "should", "may",
    "might", "do", "does", "did", "at", "by", "from", "as", "so",
    "if", "then", "than", "not", "no", "yes", "ok", "okay", "https",
    "http", "com", "www",
}


def fetch_data(client: ACClient, max_items: int = 50000) -> dict:
    notes = client.paginate("notes", "notes", max_items=max_items)
    users = client.paginate("users", "users", max_items=500)
    return {"notes": notes, "users": users}


def _tokenize(text: str) -> list[str]:
    if not text:
        return []
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]{2,}", text.lower())
    return [w for w in words if w not in STOP_WORDS]


def analyze(data: dict, stale_days: int = 30, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    notes = data.get("notes", [])
    users = data.get("users", [])

    user_by_id = {str(u["id"]): u for u in users}

    by_reltype = Counter()
    per_user = defaultdict(lambda: {"count": 0, "lengths": [], "name": "", "email": ""})
    action_items = []
    word_counter = Counter()
    latest_note_per_deal = {}

    for n in notes:
        text = n.get("note") or ""
        reltype = str(n.get("reltype", "")) or "Unknown"
        by_reltype[reltype] += 1

        uid = str(n.get("userid") or "unassigned")
        bucket = per_user[uid]
        bucket["count"] += 1
        bucket["lengths"].append(len(text))
        if uid in user_by_id:
            u = user_by_id[uid]
            bucket["name"] = f"{u.get('firstName', '')} {u.get('lastName', '')}".strip() or u.get("username", "")
            bucket["email"] = u.get("email", "")
        elif uid == "unassigned":
            bucket["name"] = "(no user)"

        if ACTION_RE.search(text):
            action_items.append({
                "id": n.get("id"),
                "reltype": reltype,
                "relid": n.get("relid"),
                "userid": uid,
                "preview": text[:200].replace("\n", " "),
                "cdate": n.get("cdate"),
            })

        word_counter.update(_tokenize(text))

        if reltype == "Deal":
            relid = str(n.get("relid", ""))
            cdate = _parse_date(n.get("cdate") or n.get("mdate"))
            if relid and cdate:
                if relid not in latest_note_per_deal or cdate > latest_note_per_deal[relid]:
                    latest_note_per_deal[relid] = cdate

    user_rows = []
    for uid, bucket in per_user.items():
        lengths = bucket["lengths"]
        median_len = sorted(lengths)[len(lengths) // 2] if lengths else 0
        user_rows.append({
            "userid": uid,
            "name": bucket["name"] or f"user-{uid}",
            "email": bucket["email"],
            "count": bucket["count"],
            "median_length": median_len,
        })
    user_rows.sort(key=lambda r: -r["count"])

    stale_deals = [
        {"deal_id": did, "last_note_age_days": (now - dt).days}
        for did, dt in latest_note_per_deal.items()
        if (now - dt).days >= stale_days
    ]
    stale_deals.sort(key=lambda r: -r["last_note_age_days"])

    return {
        "total_notes": len(notes),
        "by_reltype": dict(by_reltype),
        "users": user_rows,
        "action_items_count": len(action_items),
        "action_items": action_items[:50],
        "top_words": word_counter.most_common(30),
        "stale_deals": stale_deals[:50],
        "stale_days_threshold": stale_days,
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Notes Analysis",
        "",
        f"- Total notes: **{r['total_notes']}**",
        f"- Breakdown by reltype: {r['by_reltype']}",
        f"- Notes containing action-item language: **{r['action_items_count']}**",
        f"- Deals whose latest note is ≥{r['stale_days_threshold']} days old: **{len(r['stale_deals'])}**",
        "",
    ]
    if r["users"]:
        lines.append("## Notes by user")
        lines.append("")
        lines.append("| User | Count | Median length |")
        lines.append("|---|---:|---:|")
        for u in r["users"][:15]:
            lines.append(
                f"| {u['name']} | {u['count']} | {u['median_length']} chars |"
            )
        lines.append("")
    if r["action_items"]:
        lines.append("## Notes containing action-item language (sample)")
        lines.append("")
        for a in r["action_items"][:15]:
            lines.append(
                f"- {a['reltype']} {a['relid']} (user {a['userid']}, {a['cdate']}): "
                f"{a['preview']}"
            )
        lines.append("")
    if r["top_words"]:
        lines.append("## Top recurring words")
        lines.append("")
        lines.append(", ".join(f"`{w}` ({c})" for w, c in r["top_words"]))
        lines.append("")
    if r["stale_deals"]:
        lines.append("## Deals with stale notes")
        lines.append("")
        for d in r["stale_deals"][:25]:
            lines.append(f"- Deal {d['deal_id']} — last note {d['last_note_age_days']}d ago")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze contact + deal notes")
    parser.add_argument("--stale-days", type=int, default=30)
    parser.add_argument("--max-items", type=int, default=20000,
                        help="Cap /notes stream (default 20000)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    try:
        data = fetch_data(client, max_items=args.max_items)
    except ACClientError as e:
        if e.status_code == 403:
            print(render_feature_unavailable(
                "Notes (CRM)", "Plus",
                "Notes analysis needs the /notes endpoint.",
            ))
            return
        raise
    report = analyze(data, stale_days=args.stale_days)
    out = json.dumps(report, indent=2) if args.format == "json" else render_markdown(report)

    if args.output:
        path = Path(args.output)
        path.write_text(out)
        print(f"Wrote {path}")
        emit_files(path)
    else:
        print(out)


if __name__ == "__main__":
    main()
