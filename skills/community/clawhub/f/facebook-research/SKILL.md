---
name: facebook-research
description: Searches Facebook Marketplace listings and looks up public Facebook Page details (name, follower/like counts, category, contact info) via the Crawlora API, returning clean JSON. Use when the user wants Marketplace listing data for a location/category or a public Page's profile info — instead of scraping Facebook directly.
---

# Facebook research

Search Facebook Marketplace and look up public Facebook Page details — all
as normalized JSON from the Crawlora API, no browser automation or logged-in
session required.

## When to use this skill

- "Find Marketplace listings for <item> near <location>."
- "What's on the Marketplace browse feed for <location>/<category>?"
- "Get <Facebook Page>'s follower count / category / contact info."
- "Does this Facebook Page list a phone number or website?"
- Local-market price research or lead-gen sweeps of a Page's public About tab.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Marketplace search / browse** — `GET /facebook/marketplace/search` with a
   required `location` (Marketplace vanity slug) plus an optional `query` or
   `category`; omit both `query` and `category` to get the location's browse
   feed instead of a search. `min_price`, `max_price`, `sort_by`,
   `days_since_listed`, and `condition` only take effect alongside a `query`
   or `category`.
2. **Page lookup** — `GET /facebook/{page}` where `page` is a vanity name,
   handle, `profile.php` id, or full Facebook URL; returns name, follower/like
   counts, intro, category, business hours/price range, review count, and any
   public contact details on the Page's About tab.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Marketplace search / browse:
scripts/crawlora.sh /facebook/marketplace/search location=chicago-il query="dining table" | jq '.'
scripts/crawlora.sh /facebook/marketplace/search location=chicago-il category=vehicles min_price=5000 | jq '.'

# Page lookup:
scripts/crawlora.sh /facebook/nike | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for both Facebook
endpoints this skill uses.

## Examples

- **Local resale price check:** `/facebook/marketplace/search` with
  `location` + `query` for an item, compare listed prices/conditions across
  the first page of results.
- **Business lead enrichment:** `/facebook/{page}` for a prospect's Facebook
  Page to pull follower count, category, and any public phone/email/website
  from the About tab before outreach.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Marketplace listings and public Page info; no
  login, no private content. Respect Facebook's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Marketplace search is single-page only**: Facebook's own further
  pagination requires a logged-in session and is out of scope — only the
  first page of server-rendered results is returned.
- **`property_rentals` category is always filtered** — it has its own
  listing page and ignores the `min_price`/`max_price`/`sort_by`/etc. filters
  the same way the plain browse feed does.
- **Marketplace search can be slow** — up to roughly a minute in the slowest
  case, since it retries past an intermittent upstream condition; priced
  accordingly.
