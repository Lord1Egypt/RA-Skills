---
name: apple-maps-research
description: Researches places, categories, guides, routes, transit, and travel times through Apple Maps via the Crawlora API, returning clean JSON. Use when the user wants local-business discovery, directions, nearby places, an Apple Guide, reverse geocoding, or ETA estimates without browser automation.
---

# Apple Maps research

Search Apple Maps and its public place/guide surfaces for local intelligence,
directions, transit, and travel-time estimates as normalized JSON from the
Crawlora API.

## When to use this skill

- Find businesses or places near a coordinate, address, or category.
- Autocomplete a place search or reverse-geocode coordinates.
- Get driving, walking, or cycling directions and ETA estimates.
- Browse Apple Guides and the places inside them.
- Pull a place's details or photos.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`.

## How it works

1. Resolve a partial query with `/apple-maps/autocomplete`, or coordinates
   with `/apple-maps/reverse-geocode`.
2. Search `/apple-maps/search` or `/apple-maps/category-search`; use
   `/apple-maps/place` and `/apple-maps/place/photos` for detail.
3. Use `/apple-maps/directions`, `/apple-maps/eta`, or
   `/apple-maps/transit-departures` for travel planning.
4. Discover and inspect curated guides with `/apple-maps/guides` and the
   `/apple-maps/guides/*` endpoints.

Full endpoint list: [`reference/endpoints.md`](reference/endpoints.md).

## Example

```sh
scripts/crawlora.sh /apple-maps/search query="coffee" latitude=37.7749 longitude=-122.4194 | jq '.'
scripts/crawlora.sh /apple-maps/directions origin_latitude=37.7749 origin_longitude=-122.4194 destination_latitude=37.7849 destination_longitude=-122.4094 mode=driving | jq '.'
```
