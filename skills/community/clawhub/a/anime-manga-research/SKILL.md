---
name: anime-manga-research
description: Researches anime and manga titles via the Crawlora API — search, title detail, characters, staff, recommendations, rankings, and airing schedules — returning clean JSON. Use when the user wants an anime/manga's details, cast/staff, similar titles, seasonal rankings, or what's currently airing.
---

# Anime & manga research

Look up anime and manga titles, characters, staff, and rankings as
normalized JSON from the Crawlora API — no scraping fan-wiki or
tracker-site pages.

## When to use this skill

- "Tell me about this anime/manga" (synopsis, genres, status, score).
- "Who's in the cast / who worked on this?" (characters, staff).
- "What's airing this season?" / "top-ranked anime by genre/year."
- "Find titles similar to <title>."
- "Search for a character by name" across titles.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Anime** — `/anime/search` (`query`) to find a title id, then
   `/anime/title/{id}` for detail (accepts a raw id or `mal` for a
   MyAnimeList id), `/anime/title/{id}/characters`, `/anime/title/{id}/staff`,
   `/anime/title/{id}/recommendations`. `/anime/rankings` (filter by
   `season`, `season_year`, `genre`, `format`, `status`) and
   `/anime/airing-schedule` cover charts and what's currently airing.
   `/anime/character/{id}` and `/anime/character/search` (`query`) look up
   a character directly.
2. **Manga** — mirrors anime: `/manga/search` (`query`) → `/manga/title/{id}`
   (accepts `mal` too); `/manga/rankings` for charts.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Anime:
scripts/crawlora.sh /anime/search query="Frieren" | jq '.'
scripts/crawlora.sh /anime/title/154587 | jq '.'
scripts/crawlora.sh /anime/airing-schedule | jq '.'

# Manga:
scripts/crawlora.sh /manga/search query="Frieren" | jq '.'
scripts/crawlora.sh /manga/rankings | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Anime and
Manga endpoint this skill uses.

## Examples

- **Seasonal roundup:** `/anime/rankings` filtered by `season`+`season_year`
  for a ranked list of the season's titles.
- **Deep-dive:** `/anime/title/{id}` + `/characters` + `/staff` for a full
  profile of one show.
- **"What's next":** `/anime/title/{id}/recommendations` for similar titles
  to watch after finishing one.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public title/tracker pages.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Title/character detail needs the platform's own id — resolve via
  `.../search` first if you only have a name.
- List endpoints are paginated (`page`/`per_page`) — walk pages for full coverage.
