#!/usr/bin/env python3
"""
content_length_report.py — Word count and CTA count vs. open/click correlation.

Analyzes message bodies (text or HTML) for length and CTA presence,
correlates with the parent campaign's engagement.

Usage:
  python3 content_length_report.py
  python3 content_length_report.py --days 180 --format json
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from statistics import mean

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
    in_window = []
    for c in campaigns:
        d = _parse_iso(c.get("sdate") or c.get("ldate"))
        if d and d >= cutoff and _safe_int(c.get("send_amt")) > 0:
            in_window.append(c)
    messages = client.paginate("messages", "messages", max_items=5000)
    return {"campaigns": in_window, "messages": messages}


HTML_TAG = re.compile(r"<[^>]+>")
URL_RE = re.compile(r"https?://\S+")
CTA_PATTERNS = re.compile(r"\b(click here|learn more|sign up|get started|buy now|shop now|register|subscribe|download|read more|book now)\b", re.I)


def _strip_html(html: str) -> str:
    return HTML_TAG.sub(" ", html or "")


def analyze(data: dict) -> dict:
    msg_by_id = {m["id"]: m for m in data["messages"]}
    rows = []
    for c in data["campaigns"]:
        sent = _safe_int(c.get("send_amt"))
        if sent <= 0:
            continue
        # campaign references its messages via /campaignMessages or array on campaign
        m_ids = []
        m_field = c.get("messages") or []
        if isinstance(m_field, list):
            for x in m_field:
                if isinstance(x, dict):
                    m_ids.append(str(x.get("id")))
                else:
                    m_ids.append(str(x))
        if not m_ids:
            continue
        msg = msg_by_id.get(m_ids[0])
        if not msg:
            continue
        body = _strip_html(msg.get("html") or "") or (msg.get("text") or "")
        words = len(body.split())
        ctas = len(CTA_PATTERNS.findall(body))
        urls = len(URL_RE.findall(msg.get("html") or ""))
        rows.append({
            "campaign_id": c.get("id"),
            "subject": c.get("subject"),
            "word_count": words,
            "cta_count": ctas,
            "url_count": urls,
            "open_rate": _safe_int(c.get("uniqueopens")) / sent,
            "click_rate": _safe_int(c.get("uniquelinkclicks")) / sent,
        })

    if not rows:
        return {"rows": [], "summary": "No campaigns with messages in window"}

    short = [r["click_rate"] for r in rows if r["word_count"] < 100]
    medium = [r["click_rate"] for r in rows if 100 <= r["word_count"] < 300]
    long_ = [r["click_rate"] for r in rows if r["word_count"] >= 300]
    one_cta = [r["click_rate"] for r in rows if r["cta_count"] == 1]
    multi_cta = [r["click_rate"] for r in rows if r["cta_count"] > 1]
    return {
        "rows": rows,
        "click_rate_by_length": {
            "short_<100": mean(short) if short else None,
            "medium_100_300": mean(medium) if medium else None,
            "long_>=300": mean(long_) if long_ else None,
        },
        "click_rate_by_cta_count": {
            "single_cta": mean(one_cta) if one_cta else None,
            "multi_cta": mean(multi_cta) if multi_cta else None,
        },
    }


def render_markdown(r: dict) -> str:
    lines = ["# Content Length & CTA Analysis", ""]
    if not r["rows"]:
        lines.append("_No campaigns with linked messages in window._")
        return "\n".join(lines)
    lines.append(f"Campaigns analyzed: {len(r['rows'])}")
    lines.append("")
    lines.append("## Click rate by length bucket")
    for k, v in r["click_rate_by_length"].items():
        lines.append(f"- {k}: {v*100:.2f}%" if v is not None else f"- {k}: —")
    lines.append("")
    lines.append("## Click rate by CTA count")
    for k, v in r["click_rate_by_cta_count"].items():
        lines.append(f"- {k}: {v*100:.2f}%" if v is not None else f"- {k}: —")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--days", type=int, default=180)


def _fetch(client, args):
    return fetch(client, args.days)


def main():
    cli_main(
        description="Content length / CTA analysis",
        fetch_data=_fetch,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
