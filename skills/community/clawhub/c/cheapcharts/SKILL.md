---
name: cheapcharts
description: "Look up digital movie and TV deals, prices, charts, and recommendations on iTunes/Apple TV, Amazon, Vudu, and Google Play via the free CheapCharts public API (no auth or API key). Produces a markdown deal table with an all-time-low (ATL) flag per title using the bundled parallel script. Use when the user asks about movie/TV prices, sales, price drops, price history, all-time lows, or what's cheap to buy or rent right now."
version: 3.2.0
license: MIT
metadata:
  author: tracerman
  tags: movies, tv-shows, deals, price-tracking, cheapcharts, atl, all-time-low
  required-commands: python
---

# CheapCharts API Skill

> A free, public-API price tracker for digital movies and TV shows across iTunes (Apple TV), Amazon Prime Video, Vudu, and Google Play. No authentication. Parallel calls are safe - the bundled `deals.py` script uses 8 concurrent DetailData workers.

**Repo:** https://github.com/tracerman/cheapcharts-skill
**API Base URL:** `https://buster.cheapcharts.de/v1/gptapi/`
**ATL check:** `https://buster.cheapcharts.de/v1/DetailData.php` (unofficial internal endpoint - [Pitfall #17](references/PITFALLS.md#17-detaildata-is-unofficial))

## When to Use

- Movie/TV prices, deals, or discounts on digital stores (iTunes/Apple TV, Amazon, Vudu, Google Play)
- Charts (what's popular), recommendations by genre, cross-store price comparison
- Price history / "has it ever been cheaper?" / all-time-low questions
- User mentions CheapCharts directly

**Don't use for:** physical media (Blu-ray/DVD), streaming subscription catalogs (Netflix/Disney+), movie reviews (web search instead), video games (no public API - see [EXTRAS.md](references/EXTRAS.md#cheapcharts-games-related-but-not-in-scope)).

## The Bundled Script (use this first)

`scripts/deals.py` (stdlib-only, Python 3.9+) pulls Deals, enriches every candidate with the authoritative ATL flag from DetailData in parallel (8 workers, ~12s for 50 items), preserves the API's sort order, and emits a markdown table or JSON. It handles the pitfalls (status checks, DetailData vocabulary, genre validation) so you don't have to.

```
python scripts/deals.py                        # all current deals (iTunes US), ATL column
python scripts/deals.py --since 1              # only items whose price changed today
python scripts/deals.py --atl-only             # only rows at their all-time low
python scripts/deals.py --title "Fight Club"   # single-title ATL check
python scripts/deals.py --title "Fight Club" --history   # + full price-history timeline (sale windows, floor)
python scripts/deals.py --type seasons         # TV seasons (also: rentalmovies)
python scripts/deals.py --genre horror         # genre filter (case-insensitive, validated)
python scripts/deals.py --max-price 4.99 --min-savings 3 --limit 30
python scripts/deals.py --sort greatestSavings # bundles dominate this sort (Pitfall #35)
python scripts/deals.py --exclude-bundles      # individual movies only (they carry ratings)
python scripts/deals.py --store amazon --title "Heat"   # non-iTunes: prefer --title (Pitfall #30)
python scripts/deals.py --json                 # machine-readable output for pipelines
```

**Exit codes:** `0` deals found, `1` no deals matched (legitimate empty result), `2` API or usage error. Failed DetailData lookups are counted and reported in the table header; if all fail, exit is 2.

Default sort is `latestPricechange` (freshest drops first). Output columns: Title (links to Apple TV) | Fmt | Now | Was | Save | IMDb | RT | Date | ATL | Buy | History.

## Default Workflow

1. **"Latest deals" / "today's drops" / "what just changed"** -> `python scripts/deals.py --since 1` (fall back to `--since 3` if empty; CheapCharts lags Apple by hours-to-a-day, [Pitfall #14](references/PITFALLS.md#14-cheapcharts-data-lags-apples-store)).
2. **"What's at its all-time low?"** -> `python scripts/deals.py --atl-only`.
3. **"Is [title] at its lowest ever?"** -> `python scripts/deals.py --title "<name>"`.
4. **Anything the script doesn't cover** (charts, recommendations, cross-store, search) -> call the API directly per the decision table below; literal curl commands in [RECIPES.md](RECIPES.md).
5. **Always check the response `status` field first** - `status=error` fails silently otherwise ([Pitfall #15](references/PITFALLS.md#15-always-check-responsestatus-before-iterating-results)).

## Decision Table

| User asks... | Do this | Why |
|---|---|---|
| "Latest deals" / "today's drops" | `deals.py --since 1` | latestPricechange sort + DetailData date verification |
| "Deals under $X" | `deals.py --max-price X` | maxPrice filters server-side |
| "Highly-rated deals" | Deals API with `imdbRating`/`rottenTomatoesRating` | Both filter server-side on Deals (NOT Recommendations, [Pitfall #23](references/PITFALLS.md#23-imdbrating-and-rottentomatoesrating-filters-work-on-dealscharts-but-not-on-recommendations)) |
| "4K / Dolby Vision / Atmos on sale" | Deals API, then filter client-side | `has4K=1` param is ignored ([Pitfall #16](references/PITFALLS.md#16-has4k1-filter-does-not-work-on-dealscharts)) |
| "Newest releases on sale" | Deals `sort=releaseDate` + strip placeholder dates | Ascending only ([#11](references/PITFALLS.md#11-sortreleasedate-is-ascending-only)); bundles carry fake 2030 dates ([#12](references/PITFALLS.md#12-bundle-placeholder-dates-pollute-releasedate-sort)) |
| "What's popular / selling?" | Charts (one store) or Topseller (cross-store) | Topseller is the only multi-store batch endpoint |
| "How much is [title]?" | Search -> Prices (use `priceFollowUpItemType`) | Search resolves the IMDb ID; iTunes = Apple TV ([#19](references/PITFALLS.md#19-apple-tv--itunes-terminology)) |
| "Rental price of [title]?" | Search -> Prices with `itemType=rentalmovies` | Rental vocabulary is empirically discovered, works on Deals/Prices |
| "Complete series deals" | Deals `itemType=seasons`, filter `isBundle=1` client-side | Season genre filter is broken ([#21](references/PITFALLS.md#21-genre-filter-is-broken-for-seasons-on-deals-charts-and-recommendations)) |
| "Recommend a [genre] movie" | Recommendations with a specific genre | With `genre=All` it returns chart data ([#18](references/PITFALLS.md#18-recommendationsphp-may-return-chart-data-when-no-genre-filter-is-set)) |
| "Is [title] at its ATL?" / "lowest ever?" | `deals.py --title` or DetailData `IsLowest` flags | Only DetailData exposes ATL; the flags beat parsing ([#26](references/PITFALLS.md#26-pricehdevolution--pricesdevolution-values-are-absolute-prices-not-deltas)) |
| "When was [title] on sale?" / "price history" / "when will it be on sale again?" | `deals.py --title "<name>" --history` | Renders the full timeline with sale windows + historical floor; predict the next window from the cadence + the seasonal calendar in [EXTRAS.md](references/EXTRAS.md#seasonal-sales-calendar-itunes--apple-tv) |
| "What just came off a sale?" | DetailData on candidates; report `priceBefore < price` rows | Sale-ended rows are "next drop target" signal ([#31](references/PITFALLS.md#31-pricebefore--price-is-signal-not-noise---it-means-the-sale-just-ended)) |
| Compare across all 4 stores | Search -> 4x Prices calls, or Topseller | Note Movies Anywhere implications ([EXTRAS.md](references/EXTRAS.md#movies-anywhere-compatibility)) |

## Critical Pitfalls (the ones that silently break workflows)

Full list of 37 with evidence and dates: [references/PITFALLS.md](references/PITFALLS.md).

1. **DetailData speaks a different vocabulary:** `itemType=movies` or `seasons`, NOT `buymovies` - the wrong value errors, and looks like "no data" if you skip the status check ([#13](references/PITFALLS.md#13-detaildata-itemtype-is-movies-or-seasons---not-buymovies)).
2. **Always check `status` before iterating `results`** - errors return `{"status":"error"}` with an empty result shape that mimics "no deals" ([#15](references/PITFALLS.md#15-always-check-responsestatus-before-iterating-results)).
3. **`has4K=1` is silently ignored** on Deals/Charts - filter client-side ([#16](references/PITFALLS.md#16-has4k1-filter-does-not-work-on-dealscharts)).
4. **`genre` is broken for seasons** everywhere, and unknown genre values on movies silently return EVERYTHING ([#21](references/PITFALLS.md#21-genre-filter-is-broken-for-seasons-on-deals-charts-and-recommendations), [#22](references/PITFALLS.md#22-genre-filter-silently-falls-back-to-all-for-unknown-values-on-buymovies)).
5. **`priceHdEvolution` values are absolute prices, NOT deltas** - the sign is only the change direction; summing them produces garbage. For "at ATL now?" use the `IsLowest` flags; for timelines use `--history`, which parses it correctly ([#26](references/PITFALLS.md#26-pricehdevolution--pricesdevolution-values-are-absolute-prices-not-deltas)).
6. **No batch DetailData** - ATL enrichment is N+1 by design; use the parallel script ([#28](references/PITFALLS.md#28-there-is-no-batch-detaildata-endpoint)).
7. **Never fabricate store URLs** - `productPageUrl`/`iTunesUrl`/`cheapChartsProductPageUrl` are in the response; guessed Apple TV slugs 404 ([#32](references/PITFALLS.md#32-never-fabricate-store-direct-urls---the-response-always-has-them)).
8. **Sort choice = category filter:** `greatestSavings` surfaces bundles, `latestPricechange` surfaces individual movies ([#35](references/PITFALLS.md#35-sortgreatestsavings-puts-bundles-at-the-top-sortlatestpricechange-puts-individual-movies-at-the-top)).

## Presentation Guidelines

1. **Always include `cheapChartsProductPageUrl`** (price-history page) and the store buy link (`productPageUrl`/`iTunesUrl` from DetailData). Never guess URLs; if a field is missing, show plain text and say "store URL unavailable".
2. **Show savings** (`priceBefore - price`, and %) and skip rows where savings <= $0 unless reporting them as "sale ended".
3. **Always include an ATL column** when data was enriched with DetailData: `ATL` = at the historical floor, `-` = ordinary sale. Standard table:

   | Title | Genre | Now | Was | Save | IMDb | ATL | Changed |
   |---|---|---:|---:|---:|---:|:-:|---|
   | [Title](cheapChartsProductPageUrl) | Genre | $X.XX | $Y.YY | $Z.ZZ (N%) | N.N | ATL | YYYY-MM-DD |

4. **"Sale ended" rows are reportable signal** ([Pitfall #31](references/PITFALLS.md#31-pricebefore--price-is-signal-not-noise---it-means-the-sale-just-ended)): when `priceBefore < price`, add a `Status` column (`on sale` / `sale ended` / `stable`) instead of rendering empty cells - these are the user's "set an alert" candidates.
5. **Ratings come from Deals candidates, not DetailData** - render IMDb/RT only for individual movies (`isMovieBundle == 0`); bundles and seasons legitimately have none ([#37](references/PITFALLS.md#37-imdbrating-and-rottentomatoesrating-are-deals-candidate-fields-not-detaildata-fields)).
6. **Filter noise:** Search with `itemType=all` returns ebooks/audiobooks/albums too - filter by `mediaType` unless asked otherwise.
7. **Mention compounding savings when relevant:** gift-card stacking and seasonal sale windows are in [EXTRAS.md](references/EXTRAS.md).

## Verification Checklist

- [ ] Correct endpoint for the intent (Decision Table above)
- [ ] Response `status == "success"` checked before iterating (Pitfall #15)
- [ ] `itemType` vocabulary correct: `buymovies` for Deals/Charts/Prices, `movies`/`seasons` for DetailData (Pitfall #13)
- [ ] Genre values from the enum only; omitted entirely for seasons (Pitfalls #21, #22)
- [ ] ATL claims based on `priceHdIsLowest`/`priceSdIsLowest`, not parsed evolution strings (Pitfall #26)
- [ ] Fake drops filtered (`priceBefore > price`, savings > $0) and sale-ended rows reported as such (Pitfalls #9, #31)
- [ ] Buy/history links taken verbatim from the response (Pitfall #32)
- [ ] For non-iTunes stores: single-title lookups preferred over batch (Pitfall #30)
- [ ] `cheapChartsProductPageUrl` included in anything shown to the user

## Files in This Skill

- [`scripts/deals.py`](scripts/deals.py) - the parallel deal/ATL finder (primary tool; unit-tested, CI-canaried)
- [`RECIPES.md`](RECIPES.md) - literal curl commands for every workflow + cron prompt templates
- [`references/API.md`](references/API.md) - full endpoint/parameter/enum/field reference
- [`references/PITFALLS.md`](references/PITFALLS.md) - all 37 empirically-verified API pitfalls
- [`references/EXTRAS.md`](references/EXTRAS.md) - gift-card stacking, Movies Anywhere, seasonal sale calendar, CheapCharts Games
- [`examples/`](examples/) - real output screenshots

## Source

- API docs: https://www.cheapcharts.com/us/ai (llms.txt) - when llms.txt and this skill disagree, llms.txt wins, then verify empirically
- Website: https://www.cheapcharts.com
- The API is free and public, designed for AI agents. No auth headers needed.
