---
name: deal-discovery-research
description: Find and compare Slickdeals and RetailMeNot offers through Crawlora deal search, categories, advanced facets, deal detail, and community comments. Use to find discounts, assess a posted bargain, or build a current deal shortlist with eligibility and expiry caveats.
---

# Deal discovery research

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Find posted offers and check the conditions that make them comparable.
Slickdeals community posts are discovery evidence, not a merchant checkout quote.

## Discover and inspect offers

- Start with the product, exact model/variant, country, acceptable merchants,
  condition, budget, and any membership or coupon restrictions. Search a bounded
  result set, then fetch selected deals using a returned `thread_id` or deal URL.
  Although both fields are optional in the schema, supply one valid identifier.
- Discover category slugs, primary categories, forum IDs, and deal types through
  their own routes. For advanced search, take brand/store/category facet IDs
  from that query's returned facets; never guess them or reuse unrelated IDs.
- Keep simple category browse and primary-category browse separate. Use the
  endpoint reference for each route's pagination and filter names rather than
  assuming all Slickdeals surfaces share one search contract.
- Read a bounded comment sample for coupon exclusions, regional restrictions,
  stock changes, shipping costs, and product-condition reports. Community votes
  and comments are attributed observations, not verified merchant guarantees.

```sh
scripts/crawlora.sh /slickdeals/categories
scripts/crawlora.sh /slickdeals/search q="wireless headphones"
scripts/crawlora.sh /slickdeals/search/advanced q="wireless headphones" page=1
# Use a returned deal URL, for example:
# scripts/crawlora.sh /slickdeals/deal url="$DEAL_URL"
# scripts/crawlora.sh /slickdeals/comments url="$DEAL_URL"
```

## Normalize and report

Compare the same model, variant, pack quantity, condition, currency, and price
basis. Separate upfront price from rebates, coupon codes, membership-only rates,
subscriptions, trade-ins, and gift-card value. Keep shipping/tax or eligibility
unknown when not returned. A claimed markdown or crossed-out list price does not
prove an all-time low; a price-history claim requires comparable historical
evidence. Posted time, expired flags, and comment reports are not current stock
verification. Return a ranked shortlist by the user's criteria with merchant,
conditions, source link, observation time, and unresolved checkout questions.
A failed/empty search cannot prove no offers exist. Do not purchase or apply
coupons to a user's account from a research request.

## RetailMeNot merchant context

Discover RetailMeNot categories, stores, or autocomplete matches, then pass the
returned merchant domain to store detail. Keep `market=us` and `market=ca`
separate; Canadian domains must come from the Canadian store directory. Merchant
coupon and cashback snapshots are conditional offers, not verified redemption.
Keep codes, exclusions, expiry, minimum spend, membership, click-through tracking,
and cashback timing separate from upfront price. Do not add cashback to a coupon
saving without evidence that the offers stack. Deal events and blog posts give
editorial context; they do not establish current availability.

```sh
scripts/crawlora.sh /retailmenot/categories
scripts/crawlora.sh /retailmenot/cashback
# Resolve a returned merchant domain before:
# scripts/crawlora.sh /retailmenot/store domain="$MERCHANT_DOMAIN" market=us
```
