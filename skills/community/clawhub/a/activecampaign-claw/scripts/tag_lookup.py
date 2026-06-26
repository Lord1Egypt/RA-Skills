#!/usr/bin/env python3
"""
tag_lookup.py — Resolve a tag id by name.

Checks `state.json` first (zero API calls if the taxonomy is fresh).
Falls back to `GET /tags?search=<name>` if not found locally.

Usage:
  python3 tag_lookup.py --name VIP
  python3 tag_lookup.py --name "Hot Lead" --format json
"""

from __future__ import annotations

from _ac_client import ACClient, cli_main, load_state, sanitize


def _add_args(parser):
    parser.add_argument("--name", required=True,
                        help="Tag name (case-insensitive, exact or partial)")


def _lookup_in_state(name: str) -> list[dict]:
    state = load_state() or {}
    tags = state.get("taxonomy", {}).get("tags", []) or []
    needle = name.lower().strip()
    exact = []
    partial = []
    for t in tags:
        tname = (t.get("name") or t.get("tag") or "").lower()
        if not tname:
            continue
        if tname == needle:
            exact.append(t)
        elif needle in tname:
            partial.append(t)
    return exact or partial


def fetch_data(client: ACClient, args) -> dict:
    # Try state.json first — zero API calls
    local = _lookup_in_state(args.name)
    if local:
        return {"source": "state", "tags": local, "query": args.name}
    # Fall back to live API
    res = client.get("tags", params={"search": args.name})
    return {
        "source": "live",
        "tags": res.get("tags") or [],
        "query": args.name,
    }


def analyze(data: dict) -> dict:
    return {
        "source": data["source"],
        "query": data["query"],
        "matches": [
            {
                "id": t.get("id"),
                "name": sanitize(t.get("name") or t.get("tag") or ""),
                "description": sanitize(t.get("description", "")),
                "tag_type": t.get("tagType"),
            }
            for t in data["tags"]
        ],
    }


def render_markdown(r: dict) -> str:
    lines = [f"# Tag lookup: `{r['query']}`", "",
             f"_Source: {r['source']} ({'local cache' if r['source'] == 'state' else 'live API'})_", ""]
    if not r["matches"]:
        lines.append("No matching tags.")
        return "\n".join(lines) + "\n"
    lines.append("| ID | Name | Type | Description |")
    lines.append("|---|---|---|---|")
    for m in r["matches"]:
        lines.append(
            f"| {m['id']} | `{m['name']}` | {m['tag_type'] or '—'} | "
            f"{m['description'] or '—'} |"
        )
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="Look up a tag id by name",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
