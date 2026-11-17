---
name: gaming-research
description: Researches video games via the Crawlora API — Steam (store pages, pricing, reviews, player counts, charts, tags, achievements) and PlayStation Store (products, categories, deals) — returning clean JSON. Use when the user wants a game's price/reviews/player count, what's trending or on sale, or a store listing's details.
---

# Gaming research

Look up game store listings, pricing, reviews, and player counts across
Steam and the PlayStation Store as normalized JSON from the Crawlora API —
no scraping storefront pages.

## When to use this skill

- "What does <game> cost / how is it rated?"
- "How many people are playing <game> right now?" (Steam player counts)
- "What's trending / most played / top sellers right now?"
- "What's on sale?" (Steam or PlayStation deals)
- "Find games in <genre/tag>" or "similar to <game>."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Steam** — `/steam/search` (`term`) to find an `appid`, then
   `/steam/app` for the store page, `/steam/reviews` (+ `/reviews/histogram`)
   for review data, `/steam/players` for the current concurrent player
   count, `/steam/news` for updates, `/steam/achievements` for the
   achievement list. `/steam/charts/most-played`, `/steam/charts/concurrent`,
   `/steam/charts/top-releases`, `/steam/top-sellers`, and `/steam/featured`
   cover trending/what's-hot; `/steam/tags` and `/steam/category/{slug}`
   filter by genre/tag.
2. **PlayStation** — `/playstation/search` (`term`) to find a product `id`,
   then `/playstation/product` for detail, `/playstation/concept` for a
   game's overall franchise/concept page, `/playstation/category` to browse
   a category, `/playstation/deals` for current discounts,
   `/playstation/latest` for new releases.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Steam:
scripts/crawlora.sh /steam/search term="Hades" | jq '.'
scripts/crawlora.sh /steam/app appid=1145360 | jq '.'
scripts/crawlora.sh /steam/players appid=1145360 | jq '.'

# PlayStation:
scripts/crawlora.sh /playstation/search term="Spider-Man" | jq '.'
scripts/crawlora.sh /playstation/deals | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Steam and
PlayStation endpoint this skill uses.

## Examples

- **Buy-decision brief:** `/steam/app` (price, tags) + `/steam/reviews/histogram`
  (rating distribution) + `/steam/players` (is it still active) in one pass.
- **What's hot right now:** `/steam/charts/most-played` + `/steam/top-sellers`
  cross-checked against `/playstation/latest` for console releases.
- **Sale-hunting:** `/steam/featured` (specials) + `/playstation/deals` for
  the same title across both storefronts.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public store/review pages.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Steam pricing/availability is region-specific** — pass `cc` (country
  code) and `l` (language) where supported to match a specific storefront.
- Resolve names to platform ids via `.../search` before calling a detail
  endpoint.
