---
name: costco-research
description: Researches Costco products, categories, warehouse stock/availability, and reviews using the Crawlora API, returning clean JSON. Use when the user asks to find a Costco product, check delivery/warehouse availability, browse Costco categories, or pull Costco product reviews — instead of scraping Costco.com.
---

# Costco research

Look up and compare Costco products, categories, delivery availability,
nearby warehouses, and reviews — all as normalized JSON from the Crawlora
API, with no HTML scraping.

## When to use this skill

- "What does X cost on Costco?" or "find this product on Costco."
- "Is this Costco item in stock / when will it deliver to ZIP {postal_code}?"
- "What Costco categories match {keyword}?" / "browse Costco's {category}."
- "Pull reviews / ratings for this Costco product."
- "Find the nearest Costco warehouse to {latitude}, {longitude}."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Browse categories** — `/costco/categories` returns Costco category slugs
   and product counts, optionally scoped to a search term; each slug is usable
   directly as `/costco/search`'s `category` filter.
2. **Search** — `/costco/search` finds candidate products by `query` and/or
   `category` slug: title, brand, model, image, and rating for each result.
3. **Detail** — `/costco/product/{id}` fetches a specific product's title,
   description, manufacturer, image, price, stock status, and rating.
4. **Availability** — `/costco/product/{id}/availability` returns stock and
   estimated-delivery status for a `postal_code` + `state` destination.
5. **Reviews** — `/costco/product/{id}/reviews` returns a page of a product's
   reviews: title, text, rating, author, and recommendation.
6. **Warehouses** — `/costco/warehouses` finds nearby Costco warehouses by
   `latitude`/`longitude`, sorted by distance.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Browse categories matching a term:
scripts/crawlora.sh /costco/categories query="patio furniture" | jq '.'

# Search products by query and/or category slug:
scripts/crawlora.sh /costco/search query="robot vacuum" | jq '.'

# Product detail, then availability at a ZIP/state:
scripts/crawlora.sh /costco/product/1234567 | jq '.data'
scripts/crawlora.sh /costco/product/1234567/availability postal_code=98101 state=WA | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Costco
endpoint this skill uses (method, path, params, description).

## Examples

- **Warehouse stock check:** `/costco/search` to find a product's `id`, then
  `/costco/product/{id}/availability` with the shopper's `postal_code` and
  `state` to confirm it's deliverable before recommending it.
- **Category price sweep:** `/costco/categories` to resolve a category slug
  for a keyword, then `/costco/search` with that `category` to list matching
  products and compare prices/ratings.
- **Pre-purchase due diligence:** `/costco/product/{id}` for price and stock
  status plus `/costco/product/{id}/reviews` to summarize recent ratings and
  recommendations before buying.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Costco pages; respect Costco's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Availability is US-only** — `/costco/product/{id}/availability` requires a
  US `postal_code` and two-letter `state` code; there's no non-US delivery lookup.
- `/costco/warehouses` needs a `latitude`/`longitude` pair, not a free-text
  address or ZIP — geocode first if you only have a place name.
