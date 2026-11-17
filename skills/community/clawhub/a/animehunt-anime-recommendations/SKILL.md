---
name: anime-recommendations
description: Personal anime/manga recommendations from titles someone liked - "I loved A and B, what next?" - with reasons and page links.
version: 1.0.0
author: AnimeHunt
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["curl"]
  hermes:
    tags: ["anime", "manga", "recommendations", "entertainment"]
---

# Anime and manga recommendations

Use this skill when someone names anime or manga they enjoyed and wants more like it, or asks for titles
similar to one show. Recommendations combine "people who liked X also liked Y" community pairs and
theme/genre similarity, and they come with the reason ("because you liked ...").

## Endpoint

Base URL: `https://animehunt.co` (replace with the real domain; MCP endpoint is `/api/mcp`). No key needed.

```
POST /api/tools/recommend_from_liked
     {"liked": ["Cowboy Bebop", "Samurai Champloo"], "exclude": ["Trigun"], "media_type": "anime", "limit": 10}
GET  /api/tools/similar_titles?title=cowboy-bebop&limit=8
```

Responses are JSON: `{ "ok": true, "text": "<markdown>", "data": { "items": [...] } }`. Each item has
`title`, `year`, `format`, `score`, `url`, and for `recommend_from_liked` a `because` list of the seed
titles it matches.

## How to work

1. Collect the titles the person liked (1-10) and anything they already watched (put those in `exclude`).
2. Call `recommend_from_liked`. If a seed title cannot be found, run `search_titles` (find-anime skill)
   to get the right slug and retry.
3. Show 5-8 picks, each with the `because` reason in one sentence and the `url`.
4. For "something like <one title>" use `similar_titles` instead.

## Example

```bash
curl -s -X POST "https://animehunt.co/api/tools/recommend_from_liked" \
  -H "content-type: application/json" \
  -d '{"liked":["Cowboy Bebop","Samurai Champloo"],"limit":8}' | jq -r .text
```
