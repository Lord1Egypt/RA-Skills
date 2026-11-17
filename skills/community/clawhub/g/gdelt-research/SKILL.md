---
name: gdelt-research
description: Researches global news and US television coverage via the Crawlora API — GDELT web-news search/context/timeline/sentiment, plus GDELT Television 2.0 AI's index of US TV transcripts, captions, on-screen text, and visual labels — returning clean JSON. Use when the user wants coverage-volume or sentiment trends over time, cross-outlet news search, sentence-level co-occurrence search, or what US TV news said/showed about a topic — OSINT, media-monitoring, and political/social-science research.
---

# News & TV coverage research (GDELT)

Search and chart global news coverage and US television news via the GDELT
Project's own indexes — full-text search, sentence-level context search,
coverage/tone timelines, and (for TV) transcripts, captions, on-screen text,
and computer-vision labels — all as normalized JSON from the Crawlora API,
no scraping.

## When to use this skill

- "What's the recent news coverage of X?" / "Search global news for X."
- "How has coverage of X trended over time?" / "Is coverage of X positive
  or negative?" (timeline + tone/sentiment).
- "What sentences mention X near Y?" (sentence-level co-occurrence, last 72
  hours only).
- "What did US TV news say/show about X?" (transcripts, captions,
  on-screen text).
- "Which TV stations/shows covered X the most?" / "What's trending on TV
  right now?" (word cloud, station/show comparisons).
- OSINT, media-monitoring, or political/social-science research needing a
  free, no-auth global news/TV corpus.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

**Web news:**

1. **Search** — `/gdelt/search` (`query`, required; optional `country`,
   `domain`, `language`, `from`/`to`/`timespan`, `sort`, `maxrecords`)
   searches GDELT's continuously updated global news index.
2. **Context** — `/gdelt/context` (`query`, required; `is_quote` to scope
   to quoted text) does sentence-level co-occurrence search — **last 72
   hours of coverage only**.
3. **Timeline** — `/gdelt/timeline` (`query`, `metric` for volume vs. tone,
   `smooth`) returns how coverage volume or tone has trended over time.
4. **Tone chart** — `/gdelt/tonechart` (`query`) returns a sentiment
   histogram for a query's matching coverage.

**US television (GDELT Television 2.0 AI):**

5. **Search** — `/gdelt/tv-search` (`station`, required; optional `show`,
   `caption`/`transcript`/`onscreen_text`/`visual`/`concept` text filters
   and matching `exclude_*` negations, `day_of_week`) searches transcripts,
   captions, OCR text, and computer-vision visual labels.
6. **Timeline / comparisons** — `/gdelt/tv-timeline` (airtime volume over
   time), `/gdelt/tv-showchart` (top shows by coverage share),
   `/gdelt/tv-stationchart` (cross-station comparison) — same filter params
   as search, `station` required.
7. **Word cloud** — `/gdelt/tv-wordcloud` (`station`+`channel`, both
   required) returns a frequency-ranked word/label cloud for one match.
8. **Reference lists** — `/gdelt/tv-stationdetails` (no params) lists
   current stations; `/gdelt/tv-concept-entities` and
   `/gdelt/tv-visual-entities` (`limit`) list GDELT's own Knowledge-Graph
   concept and computer-vision label catalogs, useful for building valid
   `concept`/`visual` filter values.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Global news search:
scripts/crawlora.sh /gdelt/search query="semiconductor export controls" | jq '.'

# Coverage volume trend over time:
scripts/crawlora.sh /gdelt/timeline query="semiconductor export controls" metric=timelinevol | jq '.'

# Sentiment histogram:
scripts/crawlora.sh /gdelt/tonechart query="semiconductor export controls" | jq '.'

# US TV: search one station's coverage:
scripts/crawlora.sh /gdelt/tv-search station=CNN show="Erin Burnett OutFront" | jq '.'

# US TV: current station list:
scripts/crawlora.sh /gdelt/tv-stationdetails | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every GDELT
web-news and Television 2.0 AI endpoint this skill uses.

## Examples

- **Media narrative tracking:** `/gdelt/timeline` (volume) +
  `/gdelt/tonechart` (sentiment) for the same query to see both how much
  and how favorably a topic is covered over time.
- **Cross-medium check:** the same query through `/gdelt/search` (web news)
  and `/gdelt/tv-search` (TV) to compare print/online vs. broadcast
  framing.
- **Breaking-story monitoring:** `/gdelt/context` for sentence-level
  co-occurrence in the last 72 hours — catches emerging framing before a
  full-timeline trend is visible.
- **TV coverage-share research:** `/gdelt/tv-showchart` or
  `/gdelt/tv-stationchart` to see which shows/stations are driving
  coverage of a topic.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — GDELT's own public indexes; no authentication
  possible or needed upstream.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **`/gdelt/context` only covers the last 72 hours** — use `/gdelt/search`
  or the timeline/tone endpoints for anything further back.
- **Every TV endpoint requires `station`** (`/gdelt/tv-wordcloud` also
  requires `channel`) — list valid values via `/gdelt/tv-stationdetails`
  first if unsure.
- `timespan` and `from`/`to` are alternative ways to scope a date range —
  don't mix them; pick one.
