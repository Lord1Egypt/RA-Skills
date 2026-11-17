---
name: fiverr-research
description: Researches Fiverr gigs and sellers via the Crawlora API — search gigs by keyword, pull a gig's full detail (packages, pricing tiers, rating, seller summary), and look up a seller's profile — returning clean JSON. Use when the user wants to find freelance gigs, compare gig pricing/packages, or vet a Fiverr seller.
---

# Fiverr research

Search Fiverr gigs, pull a gig's full pricing/package/rating detail, and look
up a seller's profile — all as normalized JSON from the Crawlora API, no
scraping Fiverr pages by hand.

## When to use this skill

- "Find Fiverr gigs for <skill/service>." — keyword gig search.
- "Compare pricing/packages for these gigs." — pull full gig detail for each.
- "Who is this Fiverr seller? Are they legit?" — seller profile lookup.
- "What else does this seller offer?" — seller profile's gig list, then
  gig detail on the ones that matter.
- "What's the going rate for <service> on Fiverr?" — search + collect
  starting prices across results.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search** — `/fiverr/search` takes a free-text keyword (`q`) and returns
   normalized gig summaries: title, seller username, seller level, rating,
   review count, starting price, category, thumbnail. Paginate with `page`.
2. **Gig detail** — take a result's seller username and gig slug and call
   `/fiverr/gig/{username}/{slug}` for the full page: description, pricing
   packages (basic/standard/premium with price and delivery time), rating,
   review count, orders in queue, tags, gallery images, and a seller summary
   (level, rating, response time, languages).
3. **Seller profile** — `/fiverr/seller/{username}` returns the seller's
   display name, one-liner title, description, country, seller level,
   verification status, hourly rate, spoken languages, join date, and the
   seller's gig ids — useful for due diligence or listing everything a
   seller offers.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search gigs:
scripts/crawlora.sh /fiverr/search q="logo design" | jq '.'

# Pull one gig's full detail (username + slug from a search result):
scripts/crawlora.sh /fiverr/gig/johndoe/i-will-design-a-modern-logo | jq '.'

# Look up the seller behind a gig:
scripts/crawlora.sh /fiverr/seller/johndoe | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Fiverr
endpoint this skill uses.

## Examples

- **Gig comparison:** `/fiverr/search` for a service, then `/fiverr/gig/{username}/{slug}`
  on the top results to compare package pricing, delivery time, and rating
  side by side before recommending one.
- **Seller due diligence:** `/fiverr/seller/{username}` to check seller
  level, verification status, join date, and languages, then `/fiverr/gig/{username}/{slug}`
  on their listed gigs to see review counts and orders in queue.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public gig/seller pages; respect Fiverr's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Gig detail needs both `username` and `slug`** — the trailing path segment
  after the username in a gig URL, not just a gig ID; get both from a
  `/fiverr/search` result (`seller_username` field) rather than guessing.
- Results are paginated on `/fiverr/search` — pass `page` to walk the full list.
