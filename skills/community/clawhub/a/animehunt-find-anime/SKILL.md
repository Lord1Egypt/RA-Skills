---
name: find-anime
description: Find anime, manga or webtoons to watch or read next - search by title, browse by genre/year/season, webtoons (manhwa, manhua) by genre and reading platform, see what is airing this week, with page links.
version: 1.1.0
author: AnimeHunt
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["curl"]
  hermes:
    tags: ["anime", "manga", "entertainment", "recommendations"]
---

# Find anime and manga

Use this skill when someone asks what anime or manga to watch or read, wants details about a title, asks
"what is airing this week / this season", or wants the best titles of a genre or year. The catalog covers
about 55k anime and manga plus independent series, with community scores. It never lists explicit (18+) content.

## Endpoint

Base URL: `https://animehunt.co` (replace with the real domain; MCP endpoint is `/api/mcp`).
Every tool is also a plain HTTP call, no key needed:

```
GET  /api/tools/search_titles?query=<text>&media_type=anime|manga&limit=10
GET  /api/tools/get_title?title=<slug or title>&media_type=anime|manga
GET  /api/tools/discover_titles?media_type=anime&genres=romance,drama&year=2024&sort=score&limit=12
GET  /api/tools/list_genres
GET  /api/tools/season_titles?year=2026&season=fall&limit=20
GET  /api/tools/airing_this_week?limit=20
POST /api/tools/suggest_feature   {"title": "...", "details": "..."}   (feedback or a feature wish for the site team)
```

Responses are JSON: `{ "ok": true, "text": "<markdown summary>", "data": { ... } }`. The `text` field is
ready to show; `data.items[]` has `title`, `year`, `format`, `score` (0-100), `contentRating`, `url`.

## How to work

1. Specific title asked for: call `search_titles`, then `get_title` with the slug for synopsis, status and
   links to where it can be watched or read.
2. "Best <genre> anime", "new manga from 2025": call `list_genres` once if unsure of a slug, then
   `discover_titles` with `sort=score` for quality or `sort=popular` for mainstream picks.
3. "What is airing": `airing_this_week`; "what is coming in winter 2027": `season_titles`.
4. Webtoons, manhwa, manhua ("best action manhwa", "romance webtoons like True Beauty"): `discover_titles` with
   `media_type: "manga"`, `webtoon_only: true`, a genre slug and `sort: "score"`; add `platform: "webtoon"` or
   `"tapas"` when the person wants one app. Link the hub `https://animehunt.co/webtoons` for browsing.
5. Present 5-8 picks with one line each on why it fits, and always include the `url` so the person can
   open the page, track it or import their list.
6. Mark titles with `contentRating: "mature"` as such when the person may be a minor.

## Example

```bash
curl -s "https://animehunt.co/api/tools/discover_titles?media_type=anime&genres=mystery,psychological&sort=score&limit=8" | jq -r .text
```
