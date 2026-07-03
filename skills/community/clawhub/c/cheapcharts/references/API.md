# CheapCharts API Reference

> Full endpoint, parameter, enum, and field documentation. Load this when you
> need exact parameter names, valid enum values, or response field semantics.
> The literal `curl` commands live in [RECIPES.md](../RECIPES.md); the
> empirically-discovered gotchas live in [PITFALLS.md](PITFALLS.md).

**API Base URL:** `https://buster.cheapcharts.de/v1/gptapi/`
**All-time-low (ATL) check:** `https://buster.cheapcharts.de/v1/DetailData.php` (unofficial internal endpoint - see [Pitfall #17](PITFALLS.md#17-detaildata-is-unofficial))

> **Common parameters:** Charts, Deals, Prices, and Recommendations share common parameters (`action`, `store`, `country`, `itemType`, `imdbRating`, `rottenTomatoesRating`). Search and Topseller have their own parameter sets (see their sections below).

## 1. Search - `Search.php`

Find items by title. Use this FIRST when you only have a title and need the IMDb ID.

**Required:** `action=search`, `query=<title>` (or `searchTerm=<title>` - alias, per vendor's llms.txt)
**Optional:** `store=itunes` (default), `country=us` (default), `itemType=all` (default), `limit=20` (default 20, max 20), `offset=0` (paging offset for results beyond limit)

Returns flat list: `{"status":"success","results":[...items...]}`. Each item includes `imdbId` (if available), `mediaType`, `itemType`, `priceFollowUpItemType`, `store`, `country`, `cheapChartsProductPageUrl`, `title`, `artist`, `releaseDate`, `releaseYear`, `currency`, `price`, `currentPrice`, `has4K`, `hdrFormat`, `imdbRating`, `rottenTomatoesRating` (see Common Item Fields below).

## 2. Charts - `Charts.php`

Current chart rankings for movies or TV seasons.

**Required:** `action=getCharts`, `store`, `country`, `itemType` (buymovies or seasons)
**Optional:** `genre=All`, `quality=hd4k`, `limit`, `imdbRating` (min), `rottenTomatoesRating` (min), `releaseYear` (e.g. `2025-2025`)

Returns: `{"status":"success","results":{"buymovies":[...]}}`. Items include `rank` field.

## 3. Deals - `Deals.php`

Current deals and price drops. Best for bargain hunting.

**Required:** `action=getDeals`, `store`, `country`, `itemType` (buymovies or seasons)
**Optional:** `genre=All`, `quality=hd4k`, `sort=latestPricechange`, `maxPrice`, `releaseYear` (format: `2020-2025` - single year like `2026-2026` works too; default: all years), `limit`, `imdbRating` (min rating 0-10, default 0 = no filter, e.g. `imdbRating=7`), `rottenTomatoesRating` (min score 0-100, default 0 = no filter, e.g. `rottenTomatoesRating=80`), `has4K=1` (DOES NOT WORK - ignored, filter client-side instead, [Pitfall #16](PITFALLS.md#16-has4k1-filter-does-not-work-on-dealscharts))

**Sort options:** `latestPricechange` (default), `price`, `greatestSavings`, `greatestPercentageSavings`, `popularity`, `alphabetical`, `releaseDate` (ascending only - see [Pitfall #11](PITFALLS.md#11-sortreleasedate-is-ascending-only))

**Date filter:** `releaseYear=YYYY-YYYY` accepts both single-year (`2026-2026`) and ranges (`2024-2026`). Works on Deals and Charts endpoints. NOT supported on Recommendations, Prices, or Search.

Returns: `{"status":"success","results":{"buymovies":[...]}}`. Items include `price`, `priceBefore`, `imdbRating`, `rottenTomatoesRating`.

## 4. Prices - `Prices.php`

Look up current prices for specific titles by IMDb ID.

**Required:** `action=getPrices`, `store`, `country`, `itemType=buymovies`, `imdbIDs` (comma-separated, e.g. `tt0468569,tt2911666`)

Note: llms.txt Common Parameters list `seasons` as valid for Prices, but the Prices-specific param table and empirical testing confirm only `buymovies` works - see [Pitfall #7](PITFALLS.md#7-seasonsbundles-lack-imdb-ids---prices-api-explicitly-rejects-seasons). `rentalmovies` also works for rental prices (empirically discovered).

Returns: `{"status":"success","results":{"buymovies":[...]}}`. Same item shape as Deals.

## 5. Recommendations - `Recommendations.php`

Curated recommendations, filtered by genre and quality.

**Required:** `action=getRecommendations`, `store`, `country`, `itemType` (buymovies or seasons)
**Optional:** `genre=All`, `quality=hd4k`, `limit`, `imdbRating`, `rottenTomatoesRating`

**Note:** llms.txt lists `imdbRating`/`rottenTomatoesRating` as supported here, but empirical testing shows they are silently ignored on Recommendations ([Pitfall #23](PITFALLS.md#23-imdbrating-and-rottentomatoesrating-filters-work-on-dealscharts-but-not-on-recommendations)). Use Deals with `sort=greatestSavings` + rating filters instead.

Returns: `{"status":"success","results":{"buymovies":[...]}}`. Items may include `description` field.

## 6. Topseller - `Topseller.php`

Top sellers across multiple stores. Does NOT require `itemType`, `imdbRating`, or `rottenTomatoesRating` (unlike other endpoints).

**Required:** `action=getTopsellerForStartpage`, `country`, `store` (comma-separated, e.g. `itunes,amazon,vudu,googlePlay`)
**Optional:** `maxItemCount=5` (default 5, per store per category)

Returns: `{"status":"success","results":{"itunes":{"movies":[...],"seasons":[...]},"amazon":{...}}}`. Grouped by store, then by movies/seasons. Field availability varies by store - `has4K`, `hasAtmos`, `hdrFormat`, `isMovieBundle` only appear for iTunes items ([Pitfall #3](PITFALLS.md#3-expecting-all-fields-on-all-stores)).

## 7. DetailData (Internal) - `DetailData.php`

**Not in the official gptapi docs.** Discovered by inspecting the CheapCharts website's network calls. Returns full item details including current prices, complete price history, and child seasons (for bundles). Works for both movies and seasons. **This is the reliable way to get season/bundle prices without a browser.**

**Required:** `store`, `country`, `itemType` (`movies` or `seasons` - NOT `buymovies`, [Pitfall #13](PITFALLS.md#13-detaildata-itemtype-is-movies-or-seasons---not-buymovies)), `idInStore` (the iTunes store ID from Search results)

Returns: `{"results":{"seasons":{...}}}` (key matches the `itemType` you passed).

**Key fields (movies and seasons):**

| Field | Description |
|---|---|
| `priceSd` / `priceHd` | Current SD/HD price |
| `priceSdBefore` / `priceHdBefore` | Previous price before last change |
| `priceSdLastChangeDate` / `priceHdLastChangeDate` | Date of last price change |
| `priceSdEvolution` / `priceHdEvolution` | Full price history as `date:[+/-]price~...` string, newest first. Each value is the ABSOLUTE price effective from that date; the sign is only the change direction. See "Parsing priceHdEvolution" below. Absent on some titles/tiers (e.g. SD-only items have no HD evolution). |
| `priceSdIsLowest` / `priceHdIsLowest` | `1` if current SD/HD price equals the all-time low across CheapCharts' tracked history for this title, else `0`. **This is the canonical ATL check - use it instead of parsing `priceHdEvolution`.** |
| `priceSdIsBest` / `priceHdIsBest` | `1` if current SD/HD price equals the best (lowest) price within the current sale window (i.e. current ongoing sale's floor), else `0`. Distinct from `IsLowest` - `IsBest=1, IsLowest=0` means "lowest of THIS sale but a previous sale went lower." |
| `priceSdDropIndicator` / `priceHdDropIndicator` | `1` if price rose at last change, `-1` if it dropped, `0` if unchanged. Useful for filtering "real drops" without comparing to `priceBefore`. |
| `isBundle` / `isSeasonBundle` | Whether this is a season bundle |
| `isSeasonComplete` | Whether all seasons are included |
| `childSeasonsCount` | Number of child seasons in the bundle. **May be null even on genuine complete-series bundles** (verified 2026-07-02: Tom & Jerry Kids Show Complete Series returns `isSeasonBundle=1` but `childSeasonsCount=null`) |
| `bundleSavings` / `bundleSavingsHd` | Savings vs buying seasons individually at regular price. **May be null on bundles** - treat as optional |
| `saveOpportunity` / `saveOpportunityHd` | Same as bundleSavings |
| `episodeCount` | Total episodes |
| `advisoryRating` | Content rating (e.g. TV-14) |
| `summary` | Full synopsis |
| `seasonFamily` | Array of child seasons, each with `idInStore`, `title`, `priceSd`, `priceHd`, `priceSdEvolution`, `priceHdEvolution`, `cheapChartsProductPageUrl`. **May be empty even on complete-series bundles** - don't rely on it for child-season pricing |
| `productPageUrl` | Direct Apple TV / iTunes store URL |
| `iTunesUrl` | iTunes URL |
| `imageSmallUrl` / `imageMediumUrl` / `imageLargeUrl` | Cover art URLs |
| `appleTvId` | Apple TV internal ID |

**Parsing `priceHdEvolution`:** Split on `~`, each segment is `YYYY-MM-DD:[+|-]price`, newest first. **Each value is the absolute price in effect from that date** - `+` means the price rose to that value, `-` means it dropped to it, and the rightmost (earliest) segment carries no sign because it's the initial tracked price. Real example (Bernie, verified live 2026-07-02):

```
2026-06-23:-4.99~2026-05-06:+12.99~2026-05-01:-5.99~2026-04-14:+12.99~2026-04-10:-4.99~2026-03-20:+12.99~2026-03-13:-8.99~2026-02-17:12.99
```

reads oldest-to-newest: listed at $12.99 (2026-02-17), dropped to $8.99, back to $12.99, dropped to $4.99, back to $12.99, dropped to $5.99, back to $12.99, dropped to $4.99 (current). The values are NEVER deltas - summing them produces garbage ([Pitfall #26](PITFALLS.md#26-pricehdevolution--pricesdevolution-values-are-absolute-prices-not-deltas)). Validation invariant: the newest segment equals the current `priceHd`/`priceSd` (the weekly CI canary checks this). For "is it at ATL" questions, prefer the `IsLowest` flags; for history timelines, use `python scripts/deals.py --title "<name>" --history`, which parses this format.

## Enum Values

### Store

| Value | Countries Supported |
|---|---|
| `itunes` | us, de, gb, fr, au, ca, at, ch, es, pt, ru, jp, tr, pl, in, cn |
| `amazon` | us, de |
| `vudu` | us |
| `googlePlay` | us |

**Default to `itunes`** if user doesn't specify a store - it has the broadest country support.

### ItemType

| Value | Meaning | Used by |
|---|---|---|
| `buymovies` | Movies (purchase prices) | Charts, Deals, Prices, Recommendations |
| `rentalmovies` | Movies (rental prices, ~30 days to start, 48h to finish) | Charts, Deals, Prices (empirically discovered) |
| `seasons` | TV show seasons | Charts, Deals, Recommendations, DetailData |
| `movies` | Movies (metadata in Search; price detail in DetailData) | Search, DetailData |
| `all` | All media types (movies, seasons, ebooks, audiobooks, albums) | Search only |

**Purchase vs rental (empirically discovered, NOT in current llms.txt):** The Prices endpoint's `itemType` parameter accepts `buymovies` (purchase price) or `rentalmovies` (rental price). Rentals are typically 30 days to start watching and 48 hours to finish once started. The Search endpoint can return either type - the `priceFollowUpItemType` field tells you which one to use in the follow-up Prices call. The `deals.py` script supports `--type rentalmovies` for batch rental deals. Note: the official llms.txt only documents `buymovies` and `seasons` as valid itemType values - `rentalmovies` was discovered empirically and works on Deals and Prices endpoints.

### Genre

**Movies (`itemType=buymovies`)** - these values actually filter (tested 2026-06-21):

`All` (no filter), `ActionAdventure`, `Comedy`, `Docus` (iTunes only), `Drama`, `MadeForTV`, `Horror`, `Classical`, `Romance`, `Independent`, `KidsFamily`, `MusicDocumentation`, `SciFiFantasy`, `Sport`, `Thriller`, `Western`, `Anime`, `Musicals`

Unknown values silently fall back to "All" - they do NOT error ([Pitfall #22](PITFALLS.md#22-genre-filter-silently-falls-back-to-all-for-unknown-values-on-buymovies)). Not all genres are available for all stores - non-iTunes stores may silently ignore unsupported genre values.

**TV Seasons (`itemType=seasons`)** - the `genre` parameter is broken on Deals, Charts, and Recommendations ([Pitfall #21](PITFALLS.md#21-genre-filter-is-broken-for-seasons-on-deals-charts-and-recommendations)). Omit it and filter by title client-side.

### Quality

| Value | Meaning |
|---|---|
| `hd4k` | HD and 4K (default) |
| `hd` | HD only |
| `sd` | SD only |
| `4k` | 4K only |
| `sdOnly` | SD only (strict) |

## Common Item Fields

| Field | Always Present | Description |
|---|---|---|
| `title` | yes | Movie or TV season title |
| `artist` | yes | Director (movies) or creator (TV) - may be empty string |
| `cheapChartsProductPageUrl` | yes | Direct link to CheapCharts page - **always include this when showing results** |
| `currency` | yes | Currency code (USD, EUR, etc.) |
| `price` | yes | Current HD purchase price (reflects quality parameter default; per llms.txt) |
| `priceBefore` | no | Previous price before last change |
| `releaseDate` | yes | Original release date |
| `genre` | yes | Primary genre name (human-readable, e.g. "Action & Adventure") |
| `imdbId` | no | IMDb identifier (e.g. `tt0468569`) |
| `imdbRating` | no | IMDb rating 0-10 |
| `rottenTomatoesRating` | no | Rotten Tomatoes score 0-100 |
| `has4K` | no | iTunes only - may be boolean or 1/0 |
| `hasAtmos` | no | iTunes only - Dolby Atmos available |
| `hdrFormat` | no | iTunes only - `No HDR`, `Dolby Vision`, `HDR10+`, `HDR10` |
| `isMovieBundle` | no | iTunes only - is this a movie bundle/collection |
| `isBundle` | no | Whether this is a season/collection bundle (Topseller seasons, DetailData) |
| `description` | no | Short synopsis (if available) |
| `rank` | no | Chart rank position (Charts endpoint only) |
| `mediaType` | Search only | movies, seasons, ebooks, audiobooks, albums |
| `itemType` | Search only | Same media category repeated for agent compatibility |
| `store` | Search only | Store used for the search |
| `country` | Search only | Country used for the search |
| `priceFollowUpItemType` | Search only | Use this as itemType for Prices API follow-up. Can be `buymovies` OR `rentalmovies` (rentalmovies empirically discovered, NOT in current llms.txt) |
| `currentPrice` | Search only | Alias for `price` in Search responses |
| `releaseYear` | no | Release year, derived from releaseDate when available (Search responses) |

## Source

- API docs: https://www.cheapcharts.com/us/ai (llms.txt)
- Website: https://www.cheapcharts.com
- The API is free and public, designed for AI agents. No auth headers needed.
