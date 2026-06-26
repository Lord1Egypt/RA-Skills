#!/usr/bin/env python3
"""feeds-digest CLI: Sammelt und filtert RSS/Atom-Feeds zu einem Digest.

Beispiele:
    feeds-digest --since 7d
    feeds-digest --since 3d --topics bc,fabric
    feeds-digest --llm --output report.md
    feeds-digest --test
    feeds-digest --list-feeds
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

# Make lib/ importable when called as `python3 feeds-digest.py`
sys.path.insert(0, str(Path(__file__).resolve().parent))

import click

from lib import config as cfg
from lib import cache, filter as filt, formatter
from lib import llm as llm_lib
from lib.models import FeedItem
from lib.sources import build_source


@click.command()
@click.option(
    "--since",
    "-s",
    default=None,
    help="Zeitraum: 3d, 1w, 2w, 1m (default aus config)",
)
@click.option(
    "--topics",
    "-t",
    default=None,
    help="Komma-getrennte Themen-Filter (z.B. bc,fabric)",
)
@click.option(
    "--config",
    "-c",
    default=None,
    help="Pfad zur Config-YAML (default: ~/.config/feeds-digest/config.yaml)",
)
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output-Datei (sonst stdout)",
)
@click.option(
    "--llm",
    "llm_flag",
    is_flag=True,
    help="LLM-Summary anhängen (Perplexity/OpenAI/Ollama)",
)
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="JSON statt Markdown ausgeben",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Nur Errors ausgeben (für Cron)",
)
@click.option(
    "--test",
    is_flag=True,
    help="Nur Feed-Erreichbarkeit testen, kein Digest",
)
@click.option(
    "--list-feeds",
    is_flag=True,
    help="Aktive Feeds aus Config anzeigen",
)
@click.option(
    "--history",
    is_flag=True,
    help="Cache-Verlauf anzeigen",
)
def main(
    since: str | None,
    topics: str | None,
    config: str | None,
    output: str | None,
    llm_flag: bool,
    json_output: bool,
    quiet: bool,
    test: bool,
    list_feeds: bool,
    history: bool,
):
    """feeds-digest: Multi-Source-RSS-Digest."""
    try:
        if history:
            _show_history()
            return

        # Load config
        try:
            config_data = cfg.load_config(config)
        except cfg.ConfigError as e:
            click.echo(f"❌ Config-Fehler: {e}", err=True)
            sys.exit(2)

        if list_feeds:
            _list_feeds(config_data)
            return

        if test:
            _test_feeds(config_data, quiet)
            return

        # Resolve options
        since_str = since or config_data["defaults"]["since"]
        since_td = cfg.parse_since(since_str)
        topics_list = _parse_topics(topics, config_data)
        max_per_source = config_data["defaults"]["max_per_source"]

        if not quiet:
            click.echo(f"📡 feeds-digest: lade Feeds (since={since_str})...", err=True)

        # Build sources
        sources = _build_sources(config_data)

        if not sources:
            click.echo("⚠️  Keine aktiven Feeds in Config.", err=True)
            sys.exit(1)

        # Fetch
        results = []
        for source in sources:
            result = source.fetch()
            results.append(result)
            if not quiet:
                if result.ok:
                    click.echo(
                        f"  ✅ {result.name}: {len(result.items)} items",
                        err=True,
                    )
                else:
                    click.echo(
                        f"  ⚠️  {result.name}: {result.error}",
                        err=True,
                    )

        # Aggregate items
        all_items: list[FeedItem] = []
        for r in results:
            all_items.extend(r.items)

        # Filter pipeline
        all_items = filt.filter_by_date(all_items, since_td)
        if topics_list:
            all_items = filt.filter_by_topics(all_items, topics_list)

        # Cache-Dedup: lade alle gesehenen GUIDs pro Quelle
        seen_guids: set[str] = set()
        for r in results:
            seen_guids.update(cache.load_seen_guids(r.name))

        # Filtere bereits gesehene Items raus
        new_items = [i for i in all_items if i.guid not in seen_guids]

        # In-Memory-Dedup für den Fall, dass zwei Quellen das gleiche Item liefern
        new_items = filt.deduplicate(new_items)
        new_items = filt.limit_per_source(new_items, max_per_source)

        # Update Cache: neue GUIDs speichern + History schreiben
        for r in results:
            source_new = [i for i in new_items if i.source == r.name]
            if source_new:
                existing_guids = list(cache.load_seen_guids(r.name))
                new_guids = existing_guids + [i.guid for i in source_new]
                cache.save_seen_guids(r.name, new_guids)
                cache.append_to_history(r.name, source_new)

        all_items = new_items

        if not quiet:
            click.echo(f"\n📋 {len(all_items)} Einträge nach Filterung", err=True)

        # Format
        if json_output:
            output_text = formatter.format_json(results, all_items)
        else:
            output_text = formatter.format_markdown(
                results, all_items, since_str, topics_list
            )

        # Optional LLM
        if llm_flag:
            if not quiet:
                click.echo("🤖 LLM-Summary wird generiert...", err=True)
            try:
                llm_cfg = config_data["llm"]
                prompt_template = llm_lib.load_prompt_template(llm_cfg["prompt_file"])
                summary = llm_lib.summarize(
                    digest_markdown=output_text,
                    provider=llm_cfg["provider"],
                    model=llm_cfg["model"],
                    prompt_template=prompt_template,
                    max_tokens=llm_cfg["max_tokens"],
                    temperature=llm_cfg["temperature"],
                )
                output_text += "\n\n---\n\n## 🤖 LLM-Summary\n\n" + summary
            except llm_lib.LLMSummaryError as e:
                click.echo(f"⚠️  LLM-Fehler: {e}", err=True)
                output_text += f"\n\n---\n\n⚠️  LLM-Summary fehlgeschlagen: {e}\n"

        # Write
        if output:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w", encoding="utf-8") as f:
                f.write(output_text)
            if not quiet:
                click.echo(f"💾 Geschrieben: {output}", err=True)
        else:
            click.echo(output_text)

    except KeyboardInterrupt:
        click.echo("\n⚠️  Abgebrochen.", err=True)
        sys.exit(130)


def _parse_topics(topics: str | None, config: dict) -> list[str]:
    """Parse --topics flag, fall back to config defaults."""
    if topics:
        return [t.strip() for t in topics.split(",") if t.strip()]
    return config["defaults"].get("topics", [])


def _build_sources(config: dict) -> list:
    """Build all enabled source instances from config."""
    sources = []
    for source_type, source_list in config.get("feeds", {}).items():
        if not isinstance(source_list, list):
            continue
        for source_config in source_list:
            if not source_config.get("enabled", True):
                continue
            name = source_config.get("name", f"<unnamed {source_type}>")
            instance = build_source(source_type, name, source_config)
            if instance:
                sources.append(instance)
    return sources


def _list_feeds(config: dict) -> None:
    """List all configured feeds with status."""
    click.echo("📋 Aktive Feeds:\n")
    for source_type, source_list in config.get("feeds", {}).items():
        if not isinstance(source_list, list) or not source_list:
            continue
        click.echo(f"  [{source_type}]")
        for source_config in source_list:
            name = source_config.get("name", "?")
            enabled = source_config.get("enabled", True)
            status = "✅" if enabled else "❌"
            topics = ", ".join(source_config.get("topics", []))
            click.echo(f"    {status} {name}  (topics: {topics or '-'})")
        click.echo("")


def _test_feeds(config: dict, quiet: bool) -> None:
    """Test reachability of all enabled feeds."""
    sources = _build_sources(config)
    if not sources:
        click.echo("⚠️  Keine aktiven Feeds.", err=True)
        return

    click.echo(f"🧪 Teste {len(sources)} Feeds...\n")
    for source in sources:
        result = source.fetch()
        if result.ok:
            click.echo(f"  ✅ {result.name} ({result.source_type}): {len(result.items)} items")
        else:
            click.echo(f"  ❌ {result.name} ({result.source_type}): {result.error}")


def _show_history() -> None:
    """Show cache history."""
    history_dir = cache.DEFAULT_CACHE_DIR / "history"
    if not history_dir.exists():
        click.echo("Kein Verlauf vorhanden.")
        return

    files = sorted(history_dir.glob("*.jsonl"), reverse=True)
    if not files:
        click.echo("Kein Verlauf vorhanden.")
        return

    click.echo(f"📚 Verlauf: {len(files)} Tag(e)\n")
    for path in files[:7]:  # last 7 days
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        click.echo(f"  {path.stem}: {len(lines)} Einträge")


if __name__ == "__main__":
    main()
