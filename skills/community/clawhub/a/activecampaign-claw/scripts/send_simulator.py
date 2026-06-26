#!/usr/bin/env python3
"""
send_simulator.py — Predict send outcomes for a planned audience.

Uses calibrated baselines (from state.json) plus the audience size from
AC to estimate opens, clicks, unsubs, bounces.

Usage:
  python3 send_simulator.py --list <id>
  python3 send_simulator.py --tag <id>
  python3 send_simulator.py --segment <id>
  python3 send_simulator.py --recipients 12000   # plain count
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _ac_client import ACClient, ACClientError, load_state


def fetch_audience_size(client: ACClient, list_id, tag_id, segment_id, plain_count) -> int | None:
    if plain_count is not None:
        return plain_count
    if list_id:
        resp = client.get("contactLists", params={"filters[list]": list_id, "filters[status]": 1, "limit": 1})
        return int((resp.get("meta") or {}).get("total", 0))
    if tag_id:
        resp = client.get("contactTags", params={"filters[tag]": tag_id, "limit": 1})
        return int((resp.get("meta") or {}).get("total", 0))
    if segment_id:
        try:
            resp = client.get("contacts", params={"segmentid": segment_id, "limit": 1})
            return int((resp.get("meta") or {}).get("total", 0))
        except ACClientError:
            return 0
    # Caller didn't pass an audience scope. Surface a friendly message and
    # return a sentinel so the main flow can print + exit cleanly.
    return None


def simulate(audience: int, baseline: dict) -> dict:
    base_open = baseline.get("open_rate_p50", 0.25)
    base_click = baseline.get("click_rate_p50", 0.03)
    base_unsub = baseline.get("unsub_rate", 0.003)
    base_bounce = baseline.get("bounce_rate", 0.005)
    return {
        "audience": audience,
        "estimated_opens": int(audience * base_open),
        "estimated_clicks": int(audience * base_click),
        "estimated_unsubs": int(audience * base_unsub),
        "estimated_bounces": int(audience * base_bounce),
        "baseline_used": baseline,
    }


def render_markdown(r: dict) -> str:
    return "\n".join([
        "# Send Simulation",
        "",
        f"- Audience size: **{r['audience']:,}**",
        f"- Estimated opens: {r['estimated_opens']:,}",
        f"- Estimated clicks: {r['estimated_clicks']:,}",
        f"- Estimated unsubs: {r['estimated_unsubs']:,}",
        f"- Estimated bounces: {r['estimated_bounces']:,}",
        "",
        "_Estimates use calibrated 90-day baselines from state.json._",
    ])


def main():
    parser = argparse.ArgumentParser(description="Send outcome simulator")
    parser.add_argument("--list", dest="list_id")
    parser.add_argument("--tag", dest="tag_id")
    parser.add_argument("--segment", dest="segment_id")
    parser.add_argument("--recipients", type=int, default=None)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    state = load_state() or {}
    baseline = state.get("baselines", {})
    client = ACClient()
    audience = fetch_audience_size(client, args.list_id, args.tag_id, args.segment_id, args.recipients)
    if audience is None:
        print(
            "# Send Simulation\n\n"
            "This report needs an audience to simulate against — pass exactly one of:\n\n"
            "- `--list <id>` to simulate a send to a list\n"
            "- `--tag <id>` to simulate a send to everyone with a tag\n"
            "- `--segment <id>` to simulate a send to a saved segment\n"
            "- `--recipients <n>` to simulate against an explicit headcount\n\n"
            "Look up the id from `state.json` (run `calibrate.py` if needed) or "
            "from `scripts/list_audit.py` / `scripts/tag_audit.py` / "
            "`scripts/segment_audit.py`.\n"
        )
        return
    r = simulate(audience, baseline)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
