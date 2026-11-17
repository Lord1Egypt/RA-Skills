---
name: game-price-history-research
description: Research observed Steam price history and compare current game editions or PlayStation offers using Crawlora. Use for a dated discount brief, observed price-range analysis, or game offer comparison with currency, SKU, subscription, and history coverage preserved.
---

# Game price history research

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Explain observed game prices and discounts for a title or matched edition set.
Establish storefront, edition/base-game/add-on scope, desired platforms, currency,
region, observation window, and whether the task is historical or a current offer check.

## Resolve title, edition, and history scope

- Discover Steam titles/tags or PlayStation category/region/classification facets,
  then resolve exact `appid`, product SKU, and concept/title grouping. A base
  game, bundle, DLC, virtual currency, and premium edition are different offers.
  Shared names or concept IDs are grouping leads, not identical entitlements.
- Steam dataset histories use `app_id`; live Steam app detail uses `appid` and
  optional `cc`. The history endpoint has no country filter: do not pass `cc`
  or claim a live regional quote retroactively describes the stored series.
- `datasets_steam_prices_search` stores daily app/day price observations for
  priced games, with `snapshot_date`, `crawled_at`, currency, integer cents,
  initial cents, discount percentage, and free flag. Dates with no row are
  unobserved, not zero price or proven unchanged. The first stored day is not
  necessarily the original launch price, and a stored minimum is not an all-time low.
- PlayStation stored rows are current/crawled product SKUs with region, minor-unit
  price fields, and subscription/add-on flags. No historical SKU-price endpoint
  is provided here. Compare current PlayStation offers separately from Steam
  history rather than inventing a cross-platform daily time series.

```sh
scripts/crawlora.sh /datasets/steam-games/search q="The Witcher 3" type=game page=1 page_size=5
scripts/crawlora.sh /datasets/playstation-games/facets facet=region
# Use a verified returned app ID before its history/current detail:
# scripts/crawlora.sh /datasets/steam-prices/search app_id="$APP_ID" sort=date_asc page=1 page_size=100
# scripts/crawlora.sh /steam/app appid="$APP_ID" cc=us
```

## Calculate and present comparable prices

Convert explicitly declared `*_cents` using their cents scale, preserving raw
values; PlayStation minor-unit fields need the row's currency/scale. Never apply
one assumed currency or conversion factor to unlike sources. Keep initial/list,
discounted, per-edition, bundle, and subscription-qualified prices separate.
An included-with-subscription label is not proof the user owns the necessary plan.
A price of zero needs source/free/context evidence; a missing price is unknown.

For compatible positive prices compute `later − earlier` and the percentage
change against the earlier observed price. A displayed markdown is relative to
its displayed base price, not automatically relative to the historical maximum.
Bound pages to the 10,000-result window and show actual covered days, gaps,
currency, and crawl dates. Report observed range/minimum, dated discounts,
current-versus-stored conflicts, and edition/region assumptions. Prices do not
establish sales, revenue, availability, or savings until checkout; do not purchase,
subscribe, redeem keys, or schedule price alerts unless requested.
