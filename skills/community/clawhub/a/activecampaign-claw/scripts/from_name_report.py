#!/usr/bin/env python3
"""
from_name_report.py — Performance grouped by from-name and reply-to address.

Marketers rotate from-names without measuring; this surfaces which gets opened most.

Usage:
  python3 from_name_report.py
  python3 from_name_report.py --days 365 --format json
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from _ac_client import ACClient, cli_main
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


def fetch(client: ACClient, days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    campaigns = client.paginate("campaigns", "campaigns", max_items=5000)
    in_window = [c for c in campaigns if _parse_iso(c.get("sdate") or c.get("ldate")) and _parse_iso(c.get("sdate") or c.get("ldate")) >= cutoff]
    messages = client.paginate("messages", "messages", max_items=5000)
    return {"campaigns": in_window, "messages": messages}


def analyze(data: dict) -> dict:
    msg_by_id = {m["id"]: m for m in data["messages"]}
    by_fromname = defaultdict(lambda: {"sends": 0, "recipients": 0, "uopens": 0, "uclicks": 0})
    by_fromemail = defaultdict(lambda: {"sends": 0, "recipients": 0, "uopens": 0, "uclicks": 0})

    for c in data["campaigns"]:
        sent = _safe_int(c.get("send_amt"))
        if sent <= 0:
            continue
        fromname = c.get("fromname")
        fromemail = c.get("fromemail")
        if not fromname or not fromemail:
            # try to pull from the message
            m_field = c.get("messages") or []
            if isinstance(m_field, list) and m_field:
                first = m_field[0]
                m_id = str(first.get("id") if isinstance(first, dict) else first)
                msg = msg_by_id.get(m_id) or {}
                fromname = fromname or msg.get("fromname")
                fromemail = fromemail or msg.get("fromemail")
        fromname = fromname or "(unknown)"
        fromemail = fromemail or "(unknown)"
        for bucket, key in ((by_fromname, fromname), (by_fromemail, fromemail)):
            b = bucket[key]
            b["sends"] += 1
            b["recipients"] += sent
            b["uopens"] += _safe_int(c.get("uniqueopens"))
            b["uclicks"] += _safe_int(c.get("uniquelinkclicks"))

    def _rows(bucket):
        out = []
        for k, v in bucket.items():
            recips = v["recipients"]
            out.append({
                "key": k,
                "sends": v["sends"],
                "recipients": recips,
                "open_rate": (v["uopens"] / recips) if recips else 0,
                "click_rate": (v["uclicks"] / recips) if recips else 0,
            })
        out.sort(key=lambda x: -x["recipients"])
        return out

    return {
        "by_from_name": _rows(by_fromname),
        "by_from_email": _rows(by_fromemail),
    }


def render_markdown(r: dict) -> str:
    lines = ["# From-Name & From-Email Performance", "", "## By from-name", "| From | Sends | Recipients | Open % | Click % |", "|---|---|---|---|---|"]
    for row in r["by_from_name"]:
        lines.append(f"| {row['key']} | {row['sends']} | {row['recipients']:,} | {row['open_rate']*100:.1f}% | {row['click_rate']*100:.2f}% |")
    lines.append("")
    lines.append("## By from-email")
    lines.append("| Email | Sends | Recipients | Open % | Click % |")
    lines.append("|---|---|---|---|---|")
    for row in r["by_from_email"]:
        lines.append(f"| {row['key']} | {row['sends']} | {row['recipients']:,} | {row['open_rate']*100:.1f}% | {row['click_rate']*100:.2f}% |")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--days", type=int, default=365)


def _fetch(client, args):
    return fetch(client, args.days)


def main():
    cli_main(
        description="Performance by from-name / from-email",
        fetch_data=_fetch,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
