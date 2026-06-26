"""Markdown and JSON formatters for feed digests."""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo
    _MESZ = ZoneInfo("Europe/Berlin")
except Exception:
    _MESZ = timezone.utc  # Fallback if tzdata missing
from typing import Any

from .models import FeedItem, SourceResult


SOURCE_EMOJI = {
    "youtube": "📺",
    "ms_techcommunity": "📰",
    "github_releases": "🐙",
    "generic_rss": "📡",
}


def format_markdown(
    results: list[SourceResult],
    items: list[FeedItem],
    since_label: str,
    topics_filter: list[str],
    prompt_file: str = "prompts/summary.md",
) -> str:
    """Format digest as Markdown."""
    # MESZ für Jens (Default); Fallback zu UTC wenn zoneinfo fehlt
    now_mesz = datetime.now(_MESZ).strftime("%Y-%m-%d %H:%M %Z")
    total = len(items)
    sources = len([r for r in results if r.ok and r.items])

    lines: list[str] = []
    lines.append(f"# 📡 Feeds Digest - {now_mesz} (letzte {since_label})")
    lines.append("")

    if topics_filter:
        lines.append(f"> {total} Einträge aus {sources} Quellen | Topics: {', '.join(topics_filter)}")
    else:
        lines.append(f"> {total} Einträge aus {sources} Quellen")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group items by source
    by_source: dict[str, list[FeedItem]] = defaultdict(list)
    for item in items:
        by_source[item.source].append(item)

    # Sort items within each source by date desc
    for source_name in by_source:
        by_source[source_name].sort(
            key=lambda i: i.published or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )

    # Render each source
    for result in results:
        if not result.ok:
            lines.append(f"## {SOURCE_EMOJI.get(result.source_type, '📄')} {result.name} ⚠️")
            lines.append(f"**Fehler:** {result.error}")
            lines.append("")
            continue

        source_items = by_source.get(result.name, [])
        if not source_items:
            continue

        emoji = SOURCE_EMOJI.get(result.source_type, "📄")
        lines.append(f"## {emoji} {result.name}")
        lines.append("")

        for item in source_items:
            date_str = item.published.strftime("%Y-%m-%d") if item.published else "?"
            title = _escape_md(item.title)
            link = item.link
            lines.append(f"- **{date_str}** - [{title}]({link})")
            if item.description:
                lines.append(f"  *{item.description}*")
        lines.append("")

    # Footer with LLM prompt suggestion
    lines.append("---")
    lines.append("")
    lines.append("## 🤖 LLM-Prompt-Vorschlag")
    lines.append("")
    lines.append("Zum Pasten in Perplexity/OpenAI/Claude:")
    lines.append("")
    lines.append("```")
    lines.append("Analysiere die Tech-Updates oben. Erstelle Executive Summary (3-5 Bullets)")
    lines.append("mit Business-Relevanz für ERP/BC/AI-Consulting. Ignoriere Marketing.")
    lines.append("Hebe technische Breaking Changes hervor. Strukturiere nach Prio.")
    lines.append("```")
    lines.append("")

    # Raw JSON
    lines.append("## 📊 Rohdaten (JSON)")
    lines.append("")
    lines.append("```json")
    lines.append(_to_json(results, items))
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def format_json(results: list[SourceResult], items: list[FeedItem]) -> str:
    """Format digest as JSON for piping."""
    return _to_json(results, items)


def _to_json(results: list[SourceResult], items: list[FeedItem]) -> str:
    """Serialize results + items to compact JSON."""
    data: dict[str, Any] = {
        "generated_at": datetime.now(_MESZ).isoformat(),
        "sources": [],
        "items": [],
    }

    for r in results:
        data["sources"].append(
            {
                "name": r.name,
                "type": r.source_type,
                "ok": r.ok,
                "error": r.error,
                "item_count": len(r.items),
            }
        )

    for item in items:
        data["items"].append(
            {
                "source": item.source,
                "type": item.source_type,
                "title": item.title,
                "link": item.link,
                "published": item.published.isoformat() if item.published else None,
                "description": item.description,
                "topics": item.topics,
            }
        )

    return json.dumps(data, indent=2, ensure_ascii=False)


def _escape_md(text: str) -> str:
    """Escape markdown special chars in titles."""
    return text.replace("[", "\\[").replace("]", "\\]").replace("**", "")
