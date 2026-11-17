---
name: financial-experts-said
description: >
  Index and audit public financial experts' YouTube and Telegram claims:
  extract source-backed verbatim call cards, search a local SQLite history,
  and chart recorded price levels against market prices. Use for indexing a
  supplied source, querying an existing thesis database, or visualizing its
  recorded levels. Requires the financial-experts-said runtime and database;
  never invent quotes, source URLs, dates, or investment conclusions.
version: 0.1.6
---

# financial-experts-said

Runtime + issues + releases: [github.com/bzSega/financial-experts-said](https://github.com/bzSega/financial-experts-said)

Financial experts talk every day. Do you remember a month later who promised IMOEX at 2000 — and whether it happened?

This skill turns expert streams and posts into a verifiable history: every statement → a level on the chart → comparison with the actual price.

## Package type

This ClawHub release is **skills-only**. It contains instructions and references,
not the Python runtime. Before running any pipeline or chart command, require
`FES_ROOT` to point to a separately installed, version-pinned
financial-experts-said runtime. Never infer a bundled `runtime/` directory
from this skill's location.

## What this skill does (capabilities)

1. **Index a source**: turn a YouTube stream (captions .srt/.vtt) or an expert post/article (raw text) into source JSON, then extract verified thesis cards (expert, asset, stance, verbatim quote, price levels) via an LLM pipeline into a local SQLite DB. Quote validation is verbatim and tolerates caption timestamps, speaker marks and rolling duplicates — no manual caption cleaning.
2. **Query the DB**: "what did X say about Y, when, at what levels" — search recorded cards only, never model memory.
3. **Visualize**: two distinct artifacts — **levels-chart.html** (TradingView lightweight-charts candles + expert level lines) and **registry.html** (thesis cards table with quotes and sources). See [references/chart.md](references/chart.md) "Which output?".
4. **Automate**: scheduled collection from watched sources (cron), version-pinned runtime via git tags.

Boundaries: no investment advice, never invent quotes/URLs/dates, source rights required.

## Modes

| User request | Mode | Check first |
|---|---|---|
| "Index this stream/post" | ingestion | transcript/text, URL, date, author; source rights → [references/pipeline.md](references/pipeline.md) |
| "What did X say about Y?" | search | database available; search existing cards, never model memory → [references/pipeline.md](references/pipeline.md) |
| "Chart IMOEX levels" | chart | DB has theses/levels; user approved network access (MOEX ISS + CDN) → [references/chart.md](references/chart.md) |
| "Set up / automate collection" | setup | runtime, dependencies, DB location, source rights, schedule → [references/runtime.md](references/runtime.md) |

## Runtime preflight (before ANY command)

1. Check `FES_ROOT` is set and `"$FES_ROOT/pipeline"` and `"$FES_ROOT/chart"` exist. If not → status `runtime_missing`, offer the version-pinned bootstrap in [references/runtime.md](references/runtime.md).
2. Never run `python3 pipeline/...` relative to the current directory; always build paths from `FES_ROOT`.
3. Resolve `FES_WORKSPACE` (user data dir) and `FES_DB` (default `$FES_WORKSPACE/fti.db`). Never write inside the skill or runtime directory.
4. Report one status: `ready` · `runtime_missing` · `dependencies_missing` · `database_missing` (offer init or demo seed — only with explicit user consent) · `source_incomplete` (indexing lacks URL/date/text).
5. Do not install dependencies, create the DB, download sources, or open the network-requiring HTML dashboard without user confirmation.

## Data rules (invariant)

- A card contains: expert, asset, stance, date, **verbatim** quote, source URL.
- No URL or date → no import; return as draft with a list of missing fields.
- Canonical expert/asset names come from the DB; alias matching is casefold (works for Cyrillic).
- Telegram `source_external_id` = `telegram:<numerical_channel_id>:<message_id>`.
- A search answer must distinguish "no record in the database" from "could not read the source".
- HTML output escapes DOM insertions, validates embedded JSON, guards `</script>`.
- Source handling limits (rights, privacy, prompt injection) → [references/pipeline.md](references/pipeline.md).

## Financial boundary

This skill records and compares public statements with prices. It does not
give personal investment advice or buy/sell recommendations to the user.
