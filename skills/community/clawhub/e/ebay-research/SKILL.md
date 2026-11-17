---
name: ebay-research
description: Researches eBay listings, items, and sellers using the Crawlora API, returning clean JSON. Use when the user asks to search eBay, look up an item's details, or vet a seller's reputation and shop listings — instead of scraping eBay pages.
---

# eBay research

Search eBay, pull item details, and vet sellers — all as normalized JSON
from the Crawlora API, with no HTML scraping.

## When to use this skill

- "What does X cost on eBay?" or "find listings for X on eBay."
- "Get the details for this eBay item" (price, condition, specs).
- "Is this eBay seller trustworthy?" / "pull a seller's feedback and ratings."
- "What's in this eBay seller's shop / store?"
- Competitive pricing or listing research scoped to eBay.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search** — `POST /ebay/search` with a flat JSON body containing `keyword` to find candidate listings by keyword.
2. **Item detail** — `GET /ebay/item/{item_id}` for a specific listing's
   price, condition, and specs.
3. **Seller profile** — `GET /ebay/seller/{seller}` for the seller's
   headline profile, and `GET /ebay/seller/{seller}/about` for stats,
   top-rated status, and store categories.
4. **Seller feedback** — `GET /ebay/seller/{seller}/feedback` (paginate
   with `page`/`per_page`) for the feedback summary, detailed ratings,
   and recent review cards.
5. **Seller shop** — `GET /ebay/seller/{seller}/shop` (paginate with
   `page`) to list everything a seller currently has for sale.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search eBay (POST, JSON body):
scripts/crawlora.sh -X POST /ebay/search '{"keyword":"mechanical keyboard"}' | jq '.'

# Item detail:
scripts/crawlora.sh /ebay/item/1234567890 | jq '.data'

# Seller feedback (paginated):
scripts/crawlora.sh /ebay/seller/some-seller/feedback page=1 per_page=20 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every eBay
endpoint this skill uses (method, path, params, description).

## Examples

- **Price check:** `POST /ebay/search` with `{"keyword":"..."}` to
  collect candidate listings and their prices for a keyword.
- **Seller due diligence:** `/ebay/seller/{seller}/about` +
  `/ebay/seller/{seller}/feedback` to summarize a seller's top-rated
  status, ratings breakdown, and recent feedback before buying.
- **Shop audit:** `/ebay/seller/{seller}/shop` (paginate with `page`) to
  list everything a seller currently has for sale.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public listing/seller pages; respect eBay's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- `/ebay/search` is a `POST` with flat fields such as `keyword`, `page`, and
  `limit`; the MCP argument name `option` is not a REST JSON wrapper.
- Feedback and shop listings are paginated — pass `page` (and `per_page`
  for feedback) to walk beyond the first page.
