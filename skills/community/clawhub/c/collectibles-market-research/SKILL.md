---
name: collectibles-market-research
description: Researches public trading-card and sports-collectible markets through the Crawlora API — card identity, PSA certification and price-guide evidence, live listings, auctions, sold items, and market trends. Use when the user wants a sourced collector or buying brief, not authentication, appraisal guarantees, or a purchase action.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Collectibles market research

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Build evidence-backed briefs for trading cards and sports collectibles from
public marketplace and PSA reference data. Keep identity, condition, grade,
listing status, sale status, and source platform separate: an asking price is
not a sale, and a PSA guide value is not a guaranteed market price.

## When to use this skill

- Identify a card, set, subject, or certification and check PSA reference data.
- Compare live listings or auction lots across COMC, Fanatics Collect, ALT,
  Goldin, and Pristine Auction.
- Review sold-item evidence, auction history, market trends, or live-break
  inventory for a bounded collecting question.
- Build a short list of cards or lots with provenance, grade/condition, price,
  status, and the exact source URL.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests
  to `https://api.crawlora.net/api/v1`.

## Research workflow

1. Normalize the target before searching: player/subject, year, brand/set,
   card number, parallel/language, grade, and whether the user wants live,
   sold, or auction evidence.
2. Use PSA discovery routes for categories, sets, checklists, and price-guide
   search. Use `psa_cert_lookup` only with a certification number; a cert
   result describes that cert and grade, not every copy of the card.
3. Search marketplaces with the narrowest supported terms and follow returned
   identifiers into listing/detail routes. Preserve the platform, listing type,
   asking/current bid/realized price, currency, condition, grade, and status.
4. Compare like with like: same card identity, grade, parallel, language,
   sale type, and time window. Deduplicate cross-posted items by source URL or
   platform id, but do not merge different sellers or platforms silently.
5. Report observed ranges and evidence counts. Separate PSA guide values,
   active asks, current bids, sold prices, and market-trend signals; do not
   claim a fair value, profit, rarity, authenticity, or investment return from
   a bounded sample.

## Examples

```sh
scripts/crawlora.sh /psa/price-guide/search query="1986 Topps Jordan" | jq '.'
scripts/crawlora.sh /psa/cert-lookup cert_number=12345678 | jq '.'
scripts/crawlora.sh /comc/search query="1986 Topps Jordan" | jq '.'
scripts/crawlora.sh /fanaticscollect/sold-items title="Jordan" | jq '.'
scripts/crawlora.sh /goldin/auctions query="Mantle" | jq '.'
scripts/crawlora.sh /alt/market-trends | jq '.'
```

## Limits

- Public data only; no account, purchase, bid, submission, authentication, or
  grading action is performed.
- Coverage, pagination, condition labels, fees, shipping, currency, and update
  times differ by platform. Say when a comparison is not apples-to-apples.
- PSA price-guide and population fields are source-specific reference signals;
  they do not establish a card's current sale value or guarantee authenticity.

## Retail catalog context

PSAStore and PristineMarketplace expose storefront products and collections;
Fanatics exposes sports-merchandise search and category/product detail. These
are retail catalogs, distinct from PSA certification/price-guide evidence,
Pristine Auction lots, and Fanatics Collect sold items. Discover collection
handles or category URLs before retrieving products, and keep price, variant,
stock status, and product condition separate from realized auction prices.
PristineMarketplace search uses a fixed grid of at most 16 products per page
even when a larger `limit` is requested. Do not infer complete coverage from a
large requested limit. Reviews may describe the storefront, rather than the
individual collectible. Merchandise availability does not prove authenticity
or card rarity.

```sh
scripts/crawlora.sh /psastore/collections limit=10 page=1
scripts/crawlora.sh /pristine-marketplace/search q="signed jersey" limit=16 page=1
scripts/crawlora.sh /fanatics/categories
```
