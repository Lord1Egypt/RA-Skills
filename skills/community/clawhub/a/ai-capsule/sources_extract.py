#!/usr/bin/env python3
"""
Extract data source info from sources/{industry}.yaml

Usage:
  python3 sources_extract.py --type rss --industry ai
  python3 sources_extract.py --type webfetch --industry ai
  python3 sources_extract.py --type tavily --industry ai
  python3 sources_extract.py --list
  python3 sources_extract.py --markdown --industry ai
  python3 sources_extract.py --for-claude --industry ai   # fetch task list for the agent
"""

import argparse
import sys
from pathlib import Path

import yaml

SOURCES_DIR = Path(__file__).parent / "sources"


def load_sources(industry: str) -> list[dict]:
    path = SOURCES_DIR / f"{industry}.yaml"
    if not path.exists():
        print(f"[ERROR] source file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sources") or []


def list_industries() -> list[str]:
    return [p.stem for p in sorted(SOURCES_DIR.glob("*.yaml")) if p.stem != "README"]


def filter_by_type(sources: list[dict], type_: str) -> list[dict]:
    return [s for s in sources if s.get("type") == type_]


def to_markdown_table(sources: list[dict]) -> str:
    rows = []
    rows.append("| Source | Type | URL / Params |")
    rows.append("|--------|------|--------------|")
    for s in sources:
        name = s.get("name", "")
        type_ = s.get("type", "")
        if type_ == "tavily":
            detail = f'query=`{s.get("query","")}`, time_range={s.get("time_range","")}, limit={s.get("limit",5)}'
        else:
            url = s.get("url", "")
            note = s.get("note", "")
            detail = f"`{url}`" + (f" ({note})" if note else "")
        rows.append(f"| {name} | {type_} | {detail} |")
    return "\n".join(rows)


def to_claude_instructions(sources: list[dict], cutoff_days: int = 3) -> str:
    """Generate fetch task list for the agent to execute."""
    from datetime import datetime, timedelta
    cutoff = (datetime.now() - timedelta(days=cutoff_days)).strftime("%Y-%m-%d")

    lines = [
        f"Only include articles published after {cutoff}. Skip older ones immediately.",
        "",
    ]

    webfetch = [s for s in sources if s.get("type") == "webfetch"]
    tavily = [s for s in sources if s.get("type") == "tavily"]
    twitter = [s for s in sources if s.get("type") == "twitter"]

    if webfetch:
        lines.append("## URL fetch sources (fetch each, skip on failure)")
        lines.append("")
        lines.append("> Fetch tool: Claude Code → `WebFetch` | Codex/shell → `curl` + parse | Tavily agents → `tavily_extract`")
        lines.append("")
        for i, s in enumerate(webfetch, 1):
            url = s.get("url", "")
            note = s.get("note", "")
            limit = s.get("limit", 5)
            line = f"{i}. **{s['name']}** → `{url}` (take latest {limit})"
            if note:
                line += f"  \n   _{note}_"
            lines.append(line)

    if tavily:
        lines.append("")
        lines.append("## Tavily search sources")
        lines.append("")
        for i, s in enumerate(tavily, 1):
            domains = ", ".join(s.get("include_domains") or [])
            lines.append(
                f"{i}. **{s['name']}** → query=`{s.get('query','')}`, "
                f"include_domains=`{domains}`, "
                f"time_range={s.get('time_range','day')}, "
                f"limit={s.get('limit',5)}"
            )

    if twitter:
        lines.append("")
        lines.append("## X/Twitter sources (already handled by fetch.py)")
        lines.append("")
        lines.append("These are pre-fetched by fetch.py (Step 1). No action needed here.")
        for i, s in enumerate(twitter, 1):
            accounts = ", ".join(f"@{a}" for a in s.get("accounts", []))
            limit = s.get("limit", 5)
            lines.append(f"{i}. **{s['name']}** → accounts: {accounts}, limit: {limit}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Data source extraction tool")
    parser.add_argument("--industry", default="ai", help="Industry name (maps to sources/{industry}.yaml)")
    parser.add_argument("--type", dest="type_", choices=["rss", "webfetch", "tavily", "twitter"], help="Filter by source type")
    parser.add_argument("--list", action="store_true", help="List all available industries")
    parser.add_argument("--markdown", action="store_true", help="Output as Markdown table")
    parser.add_argument("--for-claude", action="store_true", help="Output fetch task list for the agent")
    parser.add_argument("--cutoff-days", type=int, default=3, help="Recency filter in days (default: 3)")
    args = parser.parse_args()

    if args.list:
        for ind in list_industries():
            print(ind)
        return

    sources = load_sources(args.industry)

    if args.for_claude:
        print(to_claude_instructions(sources, cutoff_days=args.cutoff_days))
        return

    if args.type_:
        sources = filter_by_type(sources, args.type_)

    if args.markdown:
        print(to_markdown_table(sources))
        return

    import json
    print(json.dumps(sources, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
