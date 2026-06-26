#!/usr/bin/env python3
"""
automation_lookup.py — Resolve an automation id by name.

Checks `state.json` first; falls back to /automations search.

Usage:
  python3 automation_lookup.py --name "Welcome Series"
  python3 automation_lookup.py --name welcome --format json
"""

from __future__ import annotations

from _ac_client import ACClient, cli_main, load_state, sanitize


def _add_args(parser):
    parser.add_argument("--name", required=True,
                        help="Automation name (case-insensitive, partial OK)")


def _lookup_in_state(name: str) -> list[dict]:
    state = load_state() or {}
    autos = state.get("taxonomy", {}).get("automations", []) or []
    needle = name.lower().strip()
    exact = []
    partial = []
    for a in autos:
        aname = (a.get("name") or "").lower()
        if not aname:
            continue
        if aname == needle:
            exact.append(a)
        elif needle in aname:
            partial.append(a)
    return exact or partial


def fetch_data(client: ACClient, args) -> dict:
    local = _lookup_in_state(args.name)
    if local:
        return {"source": "state", "automations": local, "query": args.name}
    res = client.get("automations", params={"search": args.name})
    return {
        "source": "live",
        "automations": res.get("automations") or [],
        "query": args.name,
    }


def analyze(data: dict) -> dict:
    return {
        "source": data["source"],
        "query": data["query"],
        "matches": [
            {
                "id": a.get("id"),
                "name": sanitize(a.get("name", "")),
                "status": a.get("status"),
                "entered": a.get("entered"),
                "exited": a.get("exited"),
            }
            for a in data["automations"]
        ],
    }


def render_markdown(r: dict) -> str:
    lines = [
        f"# Automation lookup: `{r['query']}`",
        "",
        f"_Source: {r['source']} ({'local cache' if r['source'] == 'state' else 'live API'})_",
        "",
    ]
    if not r["matches"]:
        lines.append("No matching automations.")
        return "\n".join(lines) + "\n"
    lines.append("| ID | Name | Status | Entered | Exited |")
    lines.append("|---|---|---|---:|---:|")
    for m in r["matches"]:
        status = {"0": "draft", "1": "active", "2": "paused"}.get(
            str(m["status"]), m["status"],
        )
        lines.append(
            f"| {m['id']} | `{m['name']}` | {status} | "
            f"{m['entered'] or '—'} | {m['exited'] or '—'} |"
        )
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="Look up an automation id by name",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
