#!/usr/bin/env python3
"""
webhook_audit.py — Inventory configured webhooks and reachability-check their URLs.

AC does not expose webhook delivery logs, so this script only verifies that
each configured target URL responds to a HEAD/OPTIONS probe.

Usage:
  python3 webhook_audit.py
  python3 webhook_audit.py --skip-probe   # config inventory only
  python3 webhook_audit.py --format json
"""

from __future__ import annotations

import argparse
import json
import socket
import urllib.error
import urllib.request
from pathlib import Path

from _ac_client import ACClient


def probe_url(url: str, timeout: int = 5) -> dict:
    if not url or not url.startswith(("http://", "https://")):
        return {"reachable": False, "error": "invalid url"}
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"reachable": True, "status": resp.status}
    except urllib.error.HTTPError as e:
        # 405 method not allowed often means the URL exists but rejects HEAD; that's fine
        return {"reachable": e.code in (200, 204, 301, 302, 401, 403, 405), "status": e.code}
    except (urllib.error.URLError, socket.timeout) as e:
        return {"reachable": False, "error": str(e)}
    except Exception as e:
        return {"reachable": False, "error": str(e)}


def fetch(client: ACClient) -> list:
    return client.paginate("webhooks", "webhooks", max_items=2000)


def analyze(webhooks: list, skip_probe: bool) -> dict:
    rows = []
    for w in webhooks:
        url = w.get("url")
        events = w.get("events") or []
        sources = w.get("sources") or []
        probe = {"reachable": None, "status": None} if skip_probe else probe_url(url)
        rows.append({
            "id": w.get("id"),
            "name": w.get("name"),
            "url": url,
            "events": events,
            "sources": sources,
            "listid": w.get("listid"),
            "init": w.get("init"),
            "probe": probe,
        })
    unreachable = [r for r in rows if r["probe"]["reachable"] is False]
    return {"total": len(rows), "webhooks": rows, "unreachable": unreachable}


def render_markdown(r: dict) -> str:
    lines = [
        "# Webhook Audit",
        "",
        f"- Total webhooks: {r['total']}",
        f"- Unreachable URLs: **{len(r['unreachable'])}**",
        "",
    ]
    if r["unreachable"]:
        lines.append("## Unreachable")
        for w in r["unreachable"]:
            err = w["probe"].get("error", w["probe"].get("status"))
            lines.append(f"- `{w['name']}` → {w['url']} ({err})")
        lines.append("")
    lines.append("## All webhooks")
    lines.append("| ID | Name | URL | Events | Reachable |")
    lines.append("|---|---|---|---|---|")
    for w in r["webhooks"]:
        events = ",".join(w["events"]) if isinstance(w["events"], list) else str(w["events"])
        reach = w["probe"]["reachable"]
        reach_s = "—" if reach is None else ("✓" if reach else "✗")
        lines.append(f"| {w['id']} | {w['name']} | {w['url']} | {events} | {reach_s} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit webhooks")
    parser.add_argument("--skip-probe", action="store_true")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    webhooks = fetch(client)
    r = analyze(webhooks, args.skip_probe)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
