---
name: cheapcharts
description: "Use when looking up digital movie/TV show prices, deals, charts, or recommendations across iTunes, Amazon, Vudu, and Google Play. Free public API, no auth required."
version: 2.2.0
author: tracerman (built with love and coffee)
license: MIT
metadata:
  hermes:
    tags: [movies, tv-shows, deals, price-tracking, cheapcharts, api, atl, all-time-low]
    required_commands: [python]
    related_skills: [publishing-agent-skills]
---

# CheapCharts API Skill

> A free, public-API price tracker for digital movies and TV shows across iTunes (Apple TV), Amazon Prime Video, Vudu, and Google Play. No authentication, no rate limits. Parallel calls are safe - the `atl_check.py` script uses 8 concurrent DetailData workers.

**Repo:** https://github.com/tracerman/cheapcharts-skill
**API Base URL:** `https://buster.cheapcharts.de/v1/gptapi/`
**All-time-low (ATL) check:** `https://buster.cheapcharts.de/v1/DetailData.php` (unofficial internal endpoint - see Pitfall #17)


## Default Workflow (canonical pattern)

When a user asks anything about deals, drops, prices, or "what's cheap right now", follow this flow:

1. **Decide the store.** Default to `itunes` (US), or use `itunes,amazon,vudu,googlePlay` for multi-store.
2. **Decide the item type.** `buymovies` for movies, `seasons` for TV, `all` for Search only.
3. **Pull Deals with `sort=latestPricechange`** for "latest" / "today's drops" / "what just changed" questions. Use `sort=greatestSavings` for "best deals" or `sort=releaseDate` for "newest releases".
4. **Verify "today" claims by hitting DetailData** for each candidate and checking `priceHdLastChangeDate` (or `priceSdLastChangeDate`). **Always check the response `status` field first** - `status=error` means your call failed silently otherwise (see Pitfall #15).
5. **Filter out fake drops** (`priceBefore - price <= $1`) and bundle placeholder dates when sorting by `releaseDate`.
6. **Enrich with the ATL flag** (`priceHdIsLowest` / `priceSdIsLowest`) from DetailData so every report can show whether each drop is at the historical floor. CheapCharts makes one extra call per item - see the standard report template in Presentation Guidelines.

The full "today's drops" recipe with Python verification is in the Workflow Recipes section.

## When to Use

- User asks about movie/TV show prices on digital stores
- User wants to find deals or discounts on digital movies
- User wants to browse charts (what's popular/trending)
- User wants recommendations in a genre
- User wants to compare prices across stores (iTunes, Amazon, Vudu, Google Play)
- User wants to check price history or lowest historical price
- User mentions CheapCharts directly

**Don't use for:** Physical media (Blu-ray/DVD), streaming subscription catalogs (Netflix/Disney+), movie reviews/criticism (use web search instead).

## Quick Decision Guide

| User says... | Use endpoint | Why |
|---|---|---|
| "Latest deals" / "today's drops" / "what just changed" | **Deals + DetailData** | Default workflow: sort=latestPricechange, then verify each item's priceHdLastChangeDate matches today (see Recipe: "Today's price drops") |
| "Find deals under $X" | Deals | Filter by maxPrice + sort=greatestSavings |
| "Best highly-rated deals" / "critically-acclaimed under $X" | Deals | Filter by imdbRating + maxPrice (both server-side filters, see Recipe) |
| "4K / Dolby Vision / Atmos movies" | Deals + client filter | has4K=1 server filter doesn't work (Pitfall #16) - fetch then filter client-side |
| "Newest releases on sale" | Deals | sort=releaseDate + bundle placeholder filter (see Pitfall #12) |
| "What's popular right now" / "what's selling" | Charts or Topseller | Charts for one store, Topseller for cross-store |
| "How much is [title]" | Search then Prices | Search to get imdbId, then Prices across stores (Pitfall #19: iTunes = Apple TV) |
| "Best complete series deals" | Deals (seasons) | Filter isBundle=1 client-side (Recipe) |
| "Recommend me a [genre] movie" | Recommendations | Pass specific genre + imdbRating (Pitfall #18: with no genre, returns chart data) |
| "What's selling the most" | Topseller | Cross-store top sellers |
| "Search for [title]" | Search | Title-based search, returns metadata |
| "Is [title] at its all-time low?" / "deals at ATL" / "lowest price ever" | **Deals + DetailData** | DetailData exposes `priceHdIsLowest` / `priceSdIsLowest` flags - no need to parse `priceHdEvolution` (see Recipe: "All-time low (ATL) deals"). Use `priceHdEvolution` only if you need the actual historical low dollar amount or change-date of the prior ATL. |

## API Endpoints

> **Common parameters:** Charts, Deals, Prices, and Recommendations share common parameters (`action`, `store`, `country`, `itemType`, `imdbRating`, `rottenTomatoesRating`). Search and Topseller have their own parameter sets (see their sections below).

### 1. Search - `Search.php`

Find items by title. Use this FIRST when you only have a title and need the IMDb ID.

**Required:** `action=search`, `query=<title>` (or `searchTerm=<title>` - alias, per vendor's llms.txt)
**Optional:** `store=itunes` (default), `country=us` (default), `itemType=all` (default), `limit=20` (default 20, max 20), `offset=0 (paging offset for results beyond limit)`

*(see [RECIPES.md](RECIPES.md))*

Returns flat list: `{"status":"success","results":[...items...]}`. Each item includes `imdbId` (if available), `mediaType`, `itemType`, `priceFollowUpItemType`, `store`, `country`, `cheapChartsProductPageUrl`, `title`, `artist`, `releaseDate`, `releaseYear`, `currency`, `price`, `currentPrice`, `has4K`, `hdrFormat`, `imdbRating`, `rottenTomatoesRating` (see Common Item Fields table for full details).

### 2. Charts - `Charts.php`

Current chart rankings for movies or TV seasons.

**Required:** `action=getCharts`, `store`, `country`, `itemType` (buymovies or seasons)
**Optional:** `genre=All`, `quality=hd4k`, `limit`, `imdbRating` (min), `rottenTomatoesRating` (min), `releaseYear` (e.g. `2025-2025`)

*(see [RECIPES.md](RECIPES.md))*

Returns: `{"status":"success","results":{"buymovies":[...]}}`. Items include `rank` field.

### 3. Deals - `Deals.php`

Current deals and price drops. Best for bargain hunting.

**Required:** `action=getDeals`, `store`, `country`, `itemType` (buymovies or seasons)
**Optional:** `genre=All`, `quality=hd4k`, `sort=latestPricechange`, `maxPrice`, `releaseYear` (format: `2020-2025` - single year like `2026-2026` works too; default: all years), `limit`, `imdbRating` (min rating 0-10, default 0 = no filter, e.g. `imdbRating=7`), `rottenTomatoesRating` (min score 0-100, default 0 = no filter, e.g. `rottenTomatoesRating=80`), `has4K=1` (DOES NOT WORK - ignored, filter client-side instead)

**Sort options:** `latestPricechange` (default), `price`, `greatestSavings`, `greatestPercentageSavings`, `popularity`, `alphabetical`, `releaseDate` (ascending only - see Pitfall #11)

**Date filter:** `releaseYear=YYYY-YYYY` accepts both single-year (`2026-2026`) and ranges (`2024-2026`). Works on Deals and Charts endpoints. NOT supported on Recommendations, Prices, or Search.

*(see [RECIPES.md](RECIPES.md))*

Returns: `{"status":"success","results":{"buymovies":[...]}}`. Items include `price`, `priceBefore`, `imdbRating`, `rottenTomatoesRating`.

### 4. Prices - `Prices.php`

Look up current prices for specific titles by IMDb ID.

**Required:** `action=getPrices`, `store`, `country`, `itemType=buymovies`, `imdbIDs` (note: llms.txt Common Parameters list `seasons` as valid for Prices, but the Prices-specific param table and empirical testing confirm only `buymovies` works - see Pitfall #7) (comma-separated, e.g. `tt0468569,tt2911666`)

*(see [RECIPES.md](RECIPES.md))*

Returns: `{"status":"success","results":{"buymovies":[...]}}`. Same item shape as Deals.

### 5. Recommendations - `Recommendations.php`

Curated recommendations, filtered by genre and quality.

**Required:** `action=getRecommendations`, `store`, `country`, `itemType` (buymovies or seasons)
**Optional:** `genre=All`, `quality=hd4k`, `limit`, `imdbRating`, `rottenTomatoesRating`

**Note:** llms.txt lists `imdbRating`/`rottenTomatoesRating` as supported here, but empirical testing shows they are silently ignored on Recommendations (Pitfall #23). Use Deals with `sort=greatestSavings` + rating filters instead.

*(see [RECIPES.md](RECIPES.md))*

Returns: `{"status":"success","results":{"buymovies":[...]}}`. Items may include `description` field.

### 6. Topseller - `Topseller.php`

Top sellers across multiple stores. Does NOT require `itemType`, `imdbRating`, or `rottenTomatoesRating` (unlike other endpoints).

**Required:** `action=getTopsellerForStartpage`, `country`, `store` (comma-separated, e.g. `itunes,amazon,vudu,googlePlay`)
**Optional:** `maxItemCount=5` (default 5, per store per category)

*(see [RECIPES.md](RECIPES.md))*

Returns: `{"status":"success","results":{"itunes":{"movies":[...],"seasons":[...]},"amazon":{...}}}`. Grouped by store, then by movies/seasons. Field availability varies by store - `has4K`, `hasAtmos`, `hdrFormat`, `isMovieBundle` only appear for iTunes items (see Pitfall #3).

### 7. DetailData (Internal) - `DetailData.php`

**Not in the official gptapi docs.** Discovered by inspecting the CheapCharts website's network calls. Returns full item details including current prices, complete price history, and child seasons (for bundles). Works for both movies and seasons. **This is the reliable way to get season/bundle prices without a browser.**

**Required:** `store`, `country`, `itemType` (`movies` or `seasons` - NOT `buymovies`), `idInStore` (the iTunes store ID from Search results)

*(see [RECIPES.md](RECIPES.md))*

Returns: `{"results":{"seasons":{...}}}` (key matches the `itemType` you passed).

**Key fields (seasons):**

| Field | Description |
|---|---|
| `priceSd` / `priceHd` | Current SD/HD price |
| `priceSdBefore` / `priceHdBefore` | Previous price before last change |
| `priceSdLastChangeDate` / `priceHdLastChangeDate` | Date of last price change |
| `priceSdEvolution` / `priceHdEvolution` | Full price history as `date:+/-price~date:+/-price~...` string. `+` = price went up, `-` = price went down. See "Parsing priceHdEvolution" below - the delta convention is unreliable for reconstructing absolute prices; prefer the `IsLowest` flag. |
| `priceSdIsLowest` / `priceHdIsLowest` | `1` if current SD/HD price equals the all-time low across CheapCharts' tracked history for this title, else `0`. **This is the canonical ATL check - use it instead of parsing `priceHdEvolution`.** |
| `priceSdIsBest` / `priceHdIsBest` | `1` if current SD/HD price equals the best (lowest) price within the current sale window (i.e. current ongoing sale's floor), else `0`. Distinct from `IsLowest` - `IsBest=1, IsLowest=0` means "lowest of THIS sale but a previous sale went lower." |
| `priceSdDropIndicator` / `priceHdDropIndicator` | `1` if price rose at last change, `-1` if it dropped, `0` if unchanged. Useful for filtering "real drops" without comparing to `priceBefore`. |
| `isBundle` / `isSeasonBundle` | Whether this is a season bundle |
| `isSeasonComplete` | Whether all seasons are included |
| `childSeasonsCount` | Number of child seasons in the bundle |
| `bundleSavings` / `bundleSavingsHd` | Savings vs buying seasons individually at regular price |
| `saveOpportunity` / `saveOpportunityHd` | Same as bundleSavings |
| `episodeCount` | Total episodes |
| `advisoryRating` | Content rating (e.g. TV-14) |
| `summary` | Full synopsis |
| `seasonFamily` | Array of child seasons, each with `idInStore`, `title`, `priceSd`, `priceHd`, `priceSdEvolution`, `priceHdEvolution`, `cheapChartsProductPageUrl` |
| `productPageUrl` | Direct Apple TV / iTunes store URL |
| `iTunesUrl` | iTunes URL |
| `imageSmallUrl` / `imageMediumUrl` / `imageLargeUrl` | Cover art URLs |
| `appleTvId` | Apple TV internal ID |

**Parsing `priceHdEvolution` (low priority - prefer `priceHdIsLowest`):** Split on `~`, each segment is `YYYY-MM-DD:[+/-]price`. The last segment (rightmost) is the earliest historical price; the first segment is the most recent price change. Example:

```
2026-05-20:+89.99~2026-05-12:-69.99~2026-04-01:-49.99~2022-02-09:89.99
```

**Caveat:** the delta convention is inconsistent across titles - for some, the last segment is an absolute starting price (`2022-02-09:89.99` with no sign); for others, the deltas don't accumulate cleanly to the current price. Empirically, walking deltas from the oldest segment does NOT always reproduce `priceHd`/`priceSd`. **For ATL detection, use the `priceHdIsLowest` / `priceSdIsLowest` flags instead - they are authoritative.** Only fall back to parsing `priceHdEvolution` if you need the absolute dollar amount of the historical low or the date it occurred, and validate the result against `priceHd` before trusting it.

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
| `rentalmovies` | Movies (rental prices, ~30 days to start, 48h to finish) | Charts, Deals, Prices (per official llms.txt) |
| `seasons` | TV show seasons | Charts, Deals, Recommendations, DetailData |
| `movies` | Movie metadata only | Search only |
| `seasons` | Season metadata only | Search only |
| `all` | All media types (movies, seasons, ebooks, audiobooks, albums) | Search only |

**Purchase vs rental (empirically discovered, NOT in current llms.txt):** The Prices endpoint's `itemType` parameter accepts `buymovies` (purchase price) or `rentalmovies` (rental price). Rentals are typically 30 days to start watching and 48 hours to finish once started. The Search endpoint can return either type — the `priceFollowUpItemType` field tells you which one to use in the follow-up Prices call. The `atl_check.py` script supports `--type rentalmovies` for batch ATL checks on rental deals. Note: the official llms.txt only documents `buymovies` and `seasons` as valid itemType values — `rentalmovies` was discovered empirically and works on Deals and Prices endpoints.

### Genre

**Movies (`itemType=buymovies`)** - these values actually filter (tested 2026-06-21):

`All` (no filter), `ActionAdventure`, `Comedy`, `Docus` (iTunes only), `Drama`, `MadeForTV`, `Horror`, `Classical`, `Romance`, `Independent`, `KidsFamily`, `MusicDocumentation`, `SciFiFantasy`, `Sport`, `Thriller`, `Western`, `Anime`, `Musicals`

Unknown values silently fall back to "All" - they do NOT error (Pitfall #22). Not all genres are available for all stores - non-iTunes stores may silently ignore unsupported genre values.

**TV Seasons (`itemType=seasons`)** - the `genre` parameter is broken on Deals, Charts, and Recommendations (Pitfall #21). Omit it and filter by title client-side.

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

## Endpoint Decision Tree

When a user asks about prices, deals, or discovery, this is the canonical flow:

| User question | First call | Why |
|---|---|---|
| "How much is [title]?" | `Search.php` to get IMDb ID, then `Prices.php` | Search resolves the title; Prices returns current numbers per store |
| "What are the current deals?" | `Deals.php` with `sort=latestPricechange` | Returns price drops in chronological order |
| "What are the best deals under $X?" | `Deals.php` with `maxPrice=X&sort=greatestSavings` | Server-side filter for price cap; sort by savings |
| "What's the price of a [rental/buy] of [title]?" | `Search.php` first, then `Prices.php` with `itemType=rentalmovies` or `itemType=buymovies` | Use the `priceFollowUpItemType` from Search to pick the right one |
| "What's popular / what's selling?" | `Topseller.php` with `store=itunes,amazon,vudu,googlePlay` | Cross-store top sellers; only endpoint that batches all 4 stores in one call |
| "What's the #1 chart in [genre]?" | `Charts.php` with `genre=X&limit=10` | Ranked chart per store/genre/quality |
| "Recommend a good [genre] movie" | `Recommendations.php` with `genre=X&imdbRating=7` | Curated, not just chart |
| "Compare [title] across all 4 stores" | `Search.php` -> get IMDb ID -> 4x `Prices.php` calls in parallel | One IMDb ID, four store prices |
| "What was the all-time low for [title]?" | `Search.php` -> get `idInStore` -> `DetailData.php` | Only DetailData exposes `priceHdIsLowest` |
| "What just dropped in price today?" | `Deals.php` with `sort=latestPricechange` + `DetailData.php` to verify the `priceHdLastChangeDate` | Deals doesn't tell you the actual change date; DetailData does |

**Topseller is the only endpoint that does cross-store batching.** Deals/Charts/Recommendations all require a single `store` parameter. If a user wants "what's selling across all four stores," Topseller is the answer; otherwise query each store separately.

## Workflow Recipes

### "Find deals on 4K action movies under $5" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "Highly-rated deals under $X" (IMDb + maxPrice both filter server-side) _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "4K Dolby Vision + Atmos movies on sale" (filter client-side - see Pitfall #16) _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "Search a specific title, then compare prices across all 4 stores" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "Complete TV series on sale" (filter to bundle deals, avoid per-season noise) _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "Cross-store top sellers today" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "What's the price of [specific movie]?" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

Step 1 - Search to get IMDb ID:
*(see [RECIPES.md](RECIPES.md))*

Step 2 - Prices using IMDb ID from search results:
*(see [RECIPES.md](RECIPES.md))*

### "Today's price drops on Apple TV/iTunes" (DEFAULT for "latest deals") _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

**When user asks "what's the latest on cheapcharts", "latest Apple TV deals", "today's price drops", or any "what just changed" question, use this workflow.** Steps:

1. Pull Deals with `sort=latestPricechange` (default sort order is most recent change first).
2. For each item, hit DetailData to get the actual `priceHdLastChangeDate` (or `priceSdLastChangeDate`).
3. Filter to items where the change date matches today. Report those as today's drops; fall back to "last 3 days" if nothing changed today.

*(see [RECIPES.md](RECIPES.md))*

**Note:** CheapCharts data lags Apple's store by hours-to-a-day. If `latestPricechange` returns items but none have today's `priceHdLastChangeDate`, that's a real "no drops today yet" - not a bug. Show the last 3 days of changes as a fallback and note the lag.

**Architecture note - why this recipe makes N+1 calls:** DetailData is the ONLY endpoint that exposes the `priceHdIsLowest` / `priceSdIsLowest` flags (verified 2026-06-23: Deals.php returns 14 fields with no ATL data, Search.php returns 10 metadata fields, Prices.php with multiple imdbIDs works but returns the same 15 fields as Deals - none of them ATL-related). There is no batch DetailData endpoint - tested with `idInStore=A&idInStore=B`, `idInStore=A,B`, `ids=A,B`, `idInStores=A,B`: all variants return empty `{}`. So populating the ATL column requires 1 Deals call + 1 DetailData per item.

**Use the bundled script** `scripts/atl_check.py` (parallel `ThreadPoolExecutor` with 8 workers) to make the N DetailData calls concurrent - empirically ~12s for 50 items vs ~150s for the inline sequential recipe below. The script also supports single-title lookup via `--title`, min-savings filtering, and JSON output.

### "All-time low (ATL) deals" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

**When user asks "is [title] at its lowest ever?" / "what's at ATL right now?" / "deals at the lowest price ever" - use this workflow.** DetailData exposes a built-in `priceHdIsLowest` / `priceSdIsLowest` flag. `1` means the current price equals the all-time low across CheapCharts' tracked price history for that title.

**Recommended: run the bundled parallel script** (preferred over the inline recipes below - much faster):

*(see [RECIPES.md](RECIPES.md))*

**For a runnable script** that does batch ATL filtering or single-title ATL lookup with proper exit codes, see `scripts/atl_check.py` (supports `--title`, `--type buymovies|seasons`, `--limit`, `--min-savings`, `--json`). This is the recommended path for cron jobs and one-off lookups - invoke with `python scripts/atl_check.py` (or the absolute path from your environment). The script is `currently at ATL` only - it does NOT filter by `priceHdLastChangeDate`; for date-bounded checks (e.g. "hit ATL in the last 24 hours") use the inline workflow in the Cron section.

### "Latest new-release movies on sale" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "Movies released this year that are on sale" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "TV season releases from a specific year range" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "Charts for new releases only" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "Best sci-fi recommendations on Amazon with IMDb 7+" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "What's trending across all stores?" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

### "Highly-rated horror movies on sale" _(see [RECIPES.md](RECIPES.md) for the literal curl commands)_

*(see [RECIPES.md](RECIPES.md))*

## Gift Card Stacking Strategy

CheapCharts tracks Apple gift card discounts at **https://www.cheapcharts.com/us/gift-card-deals** - retailers like Target, Best Buy, PayPal, Amazon, and Costco regularly sell $100 Apple gift cards for $80-$90 (10-25% off).

**Compound savings:** Buy a discounted Apple gift card -> use it to purchase an already-discounted movie on iTunes/Apple TV. A $4.99 movie bought with a 20%-off gift card effectively costs **$3.99**.

**Known patterns (from CheapCharts gift card deal history):**

| Retailer | Typical Deal | Stacking Tip |
|---|---|---|
| Target | $10-$15 bonus GC with $100 Apple GC | Use Target Circle Card for extra 5% off |
| Best Buy | $10-$15 bonus GC with $100 Apple GC | Stack with PayPal 5% off Best Buy |
| Amazon | $15 credit with $100 Apple GC | Use promo codes (e.g. `APPLEBF`, `APPLEGIFT`) |
| Costco | 10-20% off Apple GC (members only) | Check Costco warehouse + online |

These promotions rotate every few months, peaking around Black Friday and holidays. **Always check the gift card deals page before recommending a purchase** - if an active gift card deal exists, mention it as a way to stack savings.

## Movies Anywhere Compatibility

Many digital movie purchases on iTunes/Apple TV, Amazon, Vudu, and Google Play are **Movies Anywhere (MA) compatible**. MA-compatible titles sync across all four stores - buy on iTunes, watch on Vudu/Amazon/Google Play and vice versa.

**Important:** CheapCharts does NOT expose MA compatibility in any endpoint. There is no `isMoviesAnywhere` field, no MA filter, and no MA endpoint. The Movies Anywhere website itself does not have a stable public API (returns JS-rendered HTML only - no JSON-LD).

**Detection strategy (programmatic):** Use a studio-based heuristic. MA compatibility is determined by studio participation in the Movies Anywhere consortium:

| MA-Compatible Studios | NOT MA-Compatible (major) |
|---|---|
| Walt Disney Studios (Disney, Pixar, Marvel, Lucasfilm, 20th Century Studios, Searchlight) | Paramount (incl. Republic, Miramax) |
| Warner Bros. (New Line, Castle Rock, HBO theatrical) | MGM |
| Universal (DreamWorks, Focus, Illumination) | Lionsgate (incl. Summit, Starz) |
| Sony Pictures (Columbia, TriStar, Screen Gems, AFFIRM, Crunchyroll theat.) | The Weinstein Company (defunct) |
| 20th Century Studios (now under Disney but historically Fox) | Some A24 titles (varies) |

**Recipe: Look up a title's studio via IMDb**

*(see [RECIPES.md](RECIPES.md))*

**Implications for cross-store comparison:**
- For MA-compatible titles, the cheapest store wins regardless of where the user watches
- For NOT MA-compatible titles, the user should buy from the store they actually wants to watch on
- For unknown studios, suggest verifying at moviesanywhere.com or the Movies Anywhere app

## Seasonal Sales Calendar (iTunes / Apple TV)

iTunes/Apple TV deals follow predictable annual patterns. Use this to set expectations and proactively suggest checking deals during these windows:

| Period | Sale Type | Typical Discount |
|---|---|---|
| Jan-Feb | Oscar season | Best Picture contenders 30-50% off |
| Mar-Apr | Spring sale | Wide catalog discounts, often $4.99 |
| May-Jul | Summer blockbuster sales | Tied to theatrical releases |
| Oct | Horror month | *Get Out*, *Hereditary*, etc. at $3.99-$4.99 |
| Nov-Dec | Black Friday -> New Year | Biggest window: $0.99 rentals, $4.99 purchases |
| Tuesdays | Weekly spotlight deals | 8-30+ titles drop, $0.99 rentals to $4.99 buys |

**Studio promotions** (Warner Bros., Universal, Disney) run independently of seasonal sales - flash drops with no announcement, lasting 24-72 hours.

## Cron / Monitoring Recipe

For automated deal monitoring, set up a Hermes cron job that checks the Deals API daily and alerts on real price drops. Use the new "latest price change" workflow (sort=latestPricechange + DetailData verification) rather than `greatestSavings` - the latter is dominated by fake drops and bundles with manipulated baselines.

```
Schedule: daily at 9am (0 9 * * *)
Prompt: |
  Query the CheapCharts Deals API for iTunes US movies sorted by latestPricechange.
  Pull the top 30 items. For each, call DetailData (itemType=movies) to get priceHdLastChangeDate.
  Filter to items where priceHdLastChangeDate == today AND priceBefore - price > $3 (skip fake drops).
  Report the top 5 deals with title, price, priceBefore, savings %, IMDb rating, and the cheapChartsProductPageUrl.
  If fewer than 3 items changed today, fall back to the last 3 days of changes.
  If no items meet the threshold, stay silent.
  Use the documented endpoints (see RECIPES.md).
```

**For "currently at ATL" monitoring** (titles that are at their all-time low right now, regardless of when they got there), use the bundled script:

```
Schedule: daily at 9am (0 9 * * *)
Prompt: |
  Run: python scripts/atl_check.py --type buymovies --min-savings 5
  Report the top 5 ATL titles with title, current price, prior price, savings $, savings %, IMDb rating, and cheapChartsProductPageUrl.
  If no titles meet the threshold, stay silent.
  The script does parallel DetailData fetches via ThreadPoolExecutor (~12s for 50 items).
```

**For "just hit ATL" monitoring** (titles that REACHED their all-time low in the last 24 hours specifically), the script does NOT have a `--changed-since` filter - use the inline workflow with the date check:

```
Schedule: daily at 9am (0 9 * * *)
Prompt: |
  Query CheapCharts Deals for iTunes US movies sorted by latestPricechange, limit 50.
  For each, hit DetailData (itemType=movies) and check BOTH priceHdLastChangeDate == today
  AND priceHdIsLowest == 1 (or priceSdIsLowest == 1).
  Report the top 5 titles that hit ATL today, with title, current price, prior price (priceHdBefore),
  savings $, savings %, IMDb rating, and cheapChartsProductPageUrl.
  If no titles hit ATL today, stay silent.
  This uses the IsLowest flag exposed by DetailData - no need to parse priceHdEvolution.
```

## Support Files

- `scripts/atl_check.py` - runnable Python script for batch ATL filtering (`--type`, `--limit`, `--min-savings`, `--json`) and single-title ATL lookup (`--title`). Uses parallel DetailData fetches. Suitable for cron jobs and one-off checks.

## Related Resources

## CheapCharts Games (related but not in scope)

CheapCharts also tracks video game prices at **games.cheapcharts.com** (Xbox, PlayStation, Nintendo Switch). It is a separate product: separate website, separate iOS/Android apps, and **no public API** (verified 2026-06-23 — all four GPT API endpoints and DetailData only serve movies/TV/books, not games).

**If a user asks about game deals:** point them to the website and the mobile apps:
- Website: https://games.cheapcharts.com
- iOS app: id1622193150
- Android app: com.cheapcharts.cheapcharts_games

The `atl_check.py` script returns a clear error message if you pass `--store games` (it checks for the literal string and exits with code 2 + a redirect message). This is honest UX, not silent failure.

If CheapCharts ever releases a games API, add it as a separate script (e.g., `scripts/games_atl_check.py`) rather than overloading this one — the data shapes, store codes, and item taxonomies are different.

## Related Resources

- **Mobile apps:** CheapCharts Movie & TV Deals (iOS: id772046134, Android: com.lollipapp.cc), CheapCharts Games (iOS: id1622193150, Android: com.cheapcharts.cheapcharts_games)
- **JSON-LD hints:** Key CheapCharts website pages expose JSON-LD `potentialAction` hints that link directly to the GPT API endpoints with pre-filled parameters. Use as a browser-based fallback if the API doesn't cover a specific query.
- **Apple TV app gap:** The Apple TV app uses a different catalog index than iTunes. Many deals (boxsets, complete series bundles, older catalog titles) appear on CheapCharts/iTunes but are invisible in the Apple TV app. If a user can't find a deal in Apple TV, direct them to the iTunes purchase link (`productPageUrl` or `iTunesUrl` from DetailData).

## Presentation Guidelines

1. **Always include `cheapChartsProductPageUrl`** when showing results to users - they can click through for full price history and details.
2. **Show savings** - calculate `priceBefore - price` and percentage off when `priceBefore` is present.
3. **Highlight 4K/Atmos/HDR** info for iTunes items when relevant.
4. **Show ratings** - IMDb and Rotten Tomatoes scores help users decide.
5. **Filter noise** - Search with `itemType=all` returns ebooks, audiobooks, albums. Filter to `mediaType == "movies"` or `mediaType == "seasons"` unless user explicitly wants other media.
6. **Multi-store comparison** - use Topseller or call Prices with different `store` values to compare the same title across stores. Note Movies Anywhere compatibility (see dedicated section) - for MA-compatible titles, cheapest store wins regardless of where the user watches.

7. **Mention gift card stacking** - when recommending an iTunes/Apple TV purchase, check if there's an active Apple gift card deal at `https://www.cheapcharts.com/us/gift-card-deals`. If so, mention the compound savings opportunity (discounted gift card + discounted movie).

8. **Note seasonal context** - if the current date falls within a known sale window (see Seasonal Sales Calendar), proactively mention it (e.g., "We're in Oscar season - Best Picture contenders typically drop 30-50% off right now").

9. **Always include an `ATL` column in deal tables** when the data has been enriched with DetailData. `ATL` is the standard shorthand for "all-time low" - derived from `priceHdIsLowest` / `priceSdIsLowest`. This tells the user whether the current price equals the historical floor or just a typical sale. Use one of:
   - `ATL` - current price equals the all-time low (best possible time to buy)
   - `-` (plain hyphen) - current price is on sale but not at the historical floor
   - omit the column entirely only if the data wasn't enriched with DetailData

   **Standard deal-report table template (when DetailData has been hit):**

   | Title | Genre | Now | Was | Save | IMDb | ATL | Changed |
   |---|---|---:|---:|---:|---:|:-:|---|
   | [Title](cheapChartsProductPageUrl) | Genre | $X.XX | $Y.YY | $Z.ZZ (N%) | N.N | ATL | YYYY-MM-DD |

   For multi-store comparisons, add a `Store` column between Title and Now. For seasonal/limited drops where change date is the same day for every row, drop the `Changed` column to save width on Telegram.

   When a row's `ATL` cell is `ATL`, consider prefixing the row with `**` (bold) in your message body - Telegram renders this and it visually flags the rare "lowest ever" deals among typical sales.

## Common Pitfalls

1. **Using wrong `itemType` for Prices.** Prices requires `buymovies` (not `movies`). Search returns `priceFollowUpItemType` - use that value for the Prices follow-up call.

2. **Forgetting to URL-encode the query.** Use `%20` for spaces in `query` parameter, not literal spaces.

3. **Expecting all fields on all stores.** `has4K`, `hasAtmos`, `hdrFormat`, `isMovieBundle` are iTunes-only. Amazon/Vudu/Google Play items won't have these fields.

4. **Search returns mixed media types.** `itemType=all` returns movies, seasons, ebooks, audiobooks, and albums. Filter by `mediaType` in your processing if the user only wants movies/TV.

5. **Topseller `has4K` is numeric.** Topseller may return `1`/`0` instead of `true`/`false` for `has4K`/`hasAtmos`. Handle both.

6. **`artist` may be empty string.** Not all stores provide director/creator names. Don't rely on it being populated.

7. **Seasons/bundles lack IMDb IDs - Prices API explicitly rejects seasons.** The Prices endpoint returns an error: "Prices API supports ONLY movies (buymovies), not seasons." The Search endpoint returns `idInStore` but no price for seasons. **Solution: use the internal `DetailData.php` endpoint** (see Endpoint #7 above) with the `idInStore` from Search results. This returns current prices, full price history, and child seasons - all via HTTP, no browser needed. Workflow: Search (get idInStore) -> DetailData (get prices + history).

8. **Bundle vs individual season pricing.** When a user asks about a "complete series" bundle, always check the individual season prices too. Seasons go on sale independently, and buying them individually can be cheaper than the bundle (even when the bundle claims to save money vs regular individual prices). The product page shows "Other Seasons" with current sale prices for each season.

9. **Fake drops / manipulated `priceBefore`.** Some deals show a large `priceBefore -> price` drop that isn't real. Detect fake drops by: (a) checking if `priceBefore` equals `price` (no actual change - just the field is populated), (b) using DetailData's `priceHdEvolution` / `priceSdEvolution` to verify a genuine historical price change occurred, (c) filtering to `priceBefore > price` strictly (some items appear in Deals with no actual discount). When reporting deals, always calculate actual savings (`priceBefore - price`) and skip items where savings <= $0. If `priceBefore` looks suspiciously high compared to the price evolution history, flag it as a potentially inflated baseline.

10. **Amazon/Vudu/Google Play Deals endpoint instability.** The Deals endpoint for non-iTunes stores has been observed returning HTTP 500 errors server-side (noted June 2026). If Deals fails for a non-iTunes store, fall back to Topseller for that store, or retry later. iTunes Deals is the most reliable endpoint.

11. **`sort=releaseDate` is ASCENDING only - no descending variant.** The API accepts `releaseDate` (oldest first) but rejects `releaseDate_desc`, `newest`, `dateAdded`, `releaseDate_asc`, and every other date-sort variant tested (returns empty results). To get newest-first order, request with `sort=releaseDate&limit=500` and reverse client-side (Python/JS), OR narrow with `releaseYear=YYYY-YYYY` first and then pick what you need from the smaller result set.

12. **Bundle placeholder dates pollute `releaseDate` sort.** Many movie bundles have `releaseDate=2030-12-31` or `2026-12-31` - obvious placeholder values, not real release dates. They cluster at the top of `releaseDate` ascending results and look like "the newest" if you don't filter. Strip them client-side (e.g. `if not releaseDate.startswith('2030')`) before reporting "newest releases." Single-movie titles almost always have real dates; the issue is specifically with multi-film bundles.

13. **DetailData `itemType` is `movies` or `seasons` - NOT `buymovies`.** The Deals endpoint uses `itemType=buymovies` for movies, but DetailData uses a DIFFERENT vocabulary. Valid DetailData itemType values are: `singles, albums, movies, seasons, audiobooks, ebooks, apps, macapps, games`. Passing `itemType=buymovies` to DetailData returns an error: `Expected value for <itemType> not set or invalid`. This silently fails in scripts that don't check the `status` field, making it look like there's no price-change data when there actually is. **Always use `movies` for movies and `seasons` for TV when calling DetailData.**

14. **CheapCharts data lags Apple's store.** Apple's price changes can take hours to a full day to propagate to the CheapCharts API. If `sort=latestPricechange` returns items but none have a `priceHdLastChangeDate` matching today, that is a legitimate "no drops detected today yet" - re-query in a few hours. Don't treat an empty today-list as a bug.

15. **Always check `response.status` before iterating results.** Every endpoint returns `{"status":"success", ...}` on success or `{"status":"error", "message":"..."}` on failure. If you iterate `results` without checking status, a 400 error with empty `results: {}` silently yields no data - which looks identical to "no deals found." This is how the 2026-06-21 "no drops today" bug happened: passing `itemType=buymovies` to DetailData returned a status=error, the script iterated an empty dict, and reported "nothing today" when The Harvest had actually just dropped. **Pattern: `if response.get('status') != 'success': print(response.get('message')); return`.**

16. **`has4K=1` filter does NOT work on Deals/Charts.** Tested with iTunes US: passing `has4K=1` returns the same items with `has4K=0` in the response - the parameter is silently ignored. To filter to 4K-only deals, filter client-side after the API call (`if item.get('has4K') in (1, True): ...`). The field exists in item data (as `has4K`, `hasAtmos`, `hdrFormat`) but is not honored as a query parameter.

17. **DetailData is unofficial.** Only Search, Charts, Deals, Prices, Recommendations, and Topseller are in the official gptapi docs. DetailData.php was discovered by inspecting CheapCharts' website network calls and is not promised to stay stable. If it starts returning errors, fall back to Prices (movies only) or just present the current Deals data without history verification.

18. **`Recommendations.php` may return chart data when no genre filter is set.** Tested: calling Recommendations with `genre=All` returns items with `rank` fields and matches the Charts endpoint output. The underlying API uses `OfferList.php?listType=charts`. If you want curated recommendations rather than just top-of-charts, pass a specific `genre` (e.g. `SciFiFantasy`) and an `imdbRating` filter.

19. **Apple TV / iTunes terminology.** Official CheapCharts docs confirm: "iTunes" and "Apple TV" are used interchangeably. When the user says "Apple TV deal" or "iTunes deal" or "buy on Apple", treat them all as `store=itunes`. Apple rebranded iTunes Movies & TV Shows to the Apple TV app in 2019; the underlying purchase catalog is the same.

20. **JSON-LD fallback for unsupported queries.** Key CheapCharts website pages (search results, deal list pages, movie detail pages) embed JSON-LD `potentialAction` hints that link directly to the GPT API endpoints with pre-filled parameters. If a user asks for something the API doesn't support directly (e.g., browsing a specific store page), browse the relevant cheapcharts.com page and parse the JSON-LD to discover the right API call.

21. **`genre` filter is broken for `seasons` on Deals, Charts, AND Recommendations.** Tested 2026-06-21: every `genre` value (`Drama`, `Comedy`, `Horror`, `ActionAdventure`, `KidsFamily`, `Anime`, `MadeForTV`, etc.) returns the exact same list of items - the parameter is silently ignored. The default sort/limit just returns the top of the unfiltered deals list. **For TV series filtering, omit the `genre` parameter entirely and filter by series name client-side (e.g., `if 'archie' in item['title'].lower()`).** Only `itemType=buymovies` honors the genre filter reliably.

22. **`genre` filter silently falls back to "All" for unknown values on `buymovies`.** Tested 2026-06-21: passing `genre=Latino`, `genre=Faith`, `genre=War`, `genre=asdfgarbage123`, etc. all return the same unfiltered deals list as `genre=All`. The API does NOT error - it just gives you everything. **If you pass a non-standard genre and get a large mixed-genre result set, that's a signal your genre value isn't recognized.** Stick to the documented Genre enum below.

23. **`imdbRating` and `rottenTomatoesRating` filters work on Deals/Charts but NOT on Recommendations.** Tested 2026-06-21: on `Deals?itemType=buymovies&imdbRating=8`, returned items with min rating 8.0 (works). On `Recommendations?itemType=buymovies&genre=Drama&imdbRating=8`, returned items with ratings 6.8, 7.3, 7.5 - the filter was silently ignored. **For rating-filtered recommendations, use Deals with `sort=greatestSavings` and the rating filter, NOT Recommendations.**

24. **Movies Anywhere compatibility is NOT exposed by any CheapCharts endpoint.** Tested 2026-06-21: no `isMoviesAnywhere` field exists in any of Search, Deals, Charts, Prices, Recommendations, Topseller, or DetailData responses. The Movies Anywhere website has no stable public API (returns JS-rendered HTML, no JSON-LD). Use the studio-based heuristic in the Movies Anywhere Compatibility section, or browse the MA website for definitive verification.

25. **`releaseYear` works on Charts for both buymovies and seasons.** Tested: `Charts?itemType=seasons&releaseYear=2025-2026` correctly returns seasons with release dates in that range. Confirms releaseYear is supported on Deals and Charts (already documented) but worth restating since the seasons endpoint's other filters are broken (Pitfall #21).

26. **`priceHdEvolution` / `priceSdEvolution` deltas do NOT reliably reconstruct absolute price history.** The evolution string is documented as "date:[+/-]price" with the rightmost segment as the starting absolute price and earlier segments as deltas. Empirically (tested 2026-06-23): walking the deltas from the rightmost segment frequently produces a final price that does NOT match `priceHd` / `priceSd`. For example, Bernie (iTunes id 1875049429) has `priceHdEvolution=2026-06-23:-4.99~...~2026-02-17:12.99` and current `priceHd=4.99`, but summing the deltas from $12.99 forward gives $27.00 - not $4.99. The delta magnitudes/signs appear to be inconsistent across titles. **For ATL detection, always use `priceHdIsLowest` / `priceSdIsLowest` flags (authoritative).** Only fall back to parsing the evolution string if you also need the dollar amount or date of the historical low, and validate your reconstructed final price against `priceHd` / `priceSd` before reporting it. The previous SKILL example interpreting the evolution string as cumulative deltas is misleading - see the updated "Parsing priceHdEvolution" section.

27. **`priceHdIsLowest` / `priceSdIsLowest` is the canonical ATL flag - different from `priceHdIsBest` / `priceSdIsBest`.** `IsLowest=1` means current price equals the all-time low across CheapCharts' tracked history. `IsBest=1` means current price is the floor of the CURRENT sale window - a previous sale may have gone lower (`IsLowest=0, IsBest=1` is common). Check `IsLowest` for "lowest ever" questions; check `IsBest` for "is this a good price right now" questions.

28. **There is no batch DetailData endpoint - N+1 calls is the only way to enrich a Deals list with ATL data.** Verified 2026-06-23: `DetailData.php` only accepts a single `idInStore` per call. Tested alternative param shapes (`idInStore=A&idInStore=B`, comma-separated `idInStore=A,B`, `ids=A,B`, `idInStores=A,B`) - all return empty `{}`. None of the public gptapi endpoints (Deals, Search, Prices, Charts, Recommendations, Topseller) expose the ATL flags. Use the bundled `scripts/atl_check.py` (parallel `ThreadPoolExecutor`, 8 workers) to make the N DetailData calls concurrent - empirically ~12s for 50 items vs ~150s for sequential.

29. **Before adding a recipe to this skill, check `scripts/` for an existing tool that already does the workflow.** This skill ships with `scripts/atl_check.py` (parallel batch ATL checker with CLI flags, JSON output, proper exit codes). The skill's inline bash recipes for ATL filtering are 10-12x slower than the script (sequential DetailData calls vs parallel). Recipes should reference the script with a short invocation. When extending the skill: `ls scripts/` and `grep -n 'scripts/' SKILL.md` first, then add a one-line "run this script" recipe instead of inlining the workflow.

30. **iTunes is the only store with reliable batch + complete catalog coverage.** The script accepts `--store` for all four stores, and single-title lookups work on Amazon/Vudu/Google Play, but the underlying CheapCharts data is sparser on those stores and the Deals endpoint returns a server-side error (HTTP 500, "There was an error handling the request") for many batch queries. Verified 2026-06-23: `--store amazon --limit 10` exits with code 2, while `--store itunes --limit 10` returns 80+ deals. For non-iTunes stores, prefer `--title <name>` lookups over batch mode, or fall back to Topseller (`gptapi/Topseller.php` with `store=itunes,amazon,vudu,googlePlay`) if you need cross-store batch data. Don't promise "all four stores" in agent reports without verifying the data for the specific title or genre.

## Verification Checklist

- [ ] Correct endpoint selected for user intent (see Quick Decision Guide)
- [ ] "Latest deals" / "today's drops" / "what just changed" defaults to Deals sort=latestPricechange + DetailData verification (NOT releaseDate sort)
- [ ] `store` and `country` set appropriately (default: `itunes`, `us`)
- [ ] `itemType` correct (`buymovies` for Deals/Charts, `movies` for DetailData, `seasons` for both, `all` for Search only)
- [ ] Response `status` field checked as `"success"` before iterating `results` (Pitfall #15) - silent failures from wrong itemType or bad params look identical to empty result sets
- [ ] Query parameters URL-encoded (spaces as `%20`)
- [ ] `cheapChartsProductPageUrl` included in output shown to user
- [ ] Results filtered to relevant `mediaType` if user only wants movies/TV
- [ ] Fake drops filtered out (`priceBefore > price`, savings > $0)
- [ ] Bundle placeholder dates filtered out when sorting by `releaseDate` (`releaseDate` not starting with `2030`)
- [ ] For TV season queries: `genre` filter omitted (Pitfall #21) and filtered client-side by title/name
- [ ] For rating-filtered queries: used Deals endpoint, NOT Recommendations (Pitfall #23)
- [ ] Movies Anywhere compatibility noted in multi-store comparisons (using studio heuristic from Movies Anywhere Compatibility section, not assumed)
- [ ] Seasonal context mentioned if current date falls in a known sale window
- [ ] For ATL questions ("lowest ever", "all-time low"): used `priceHdIsLowest` / `priceSdIsLowest` from DetailData, NOT parsed `priceHdEvolution` (Pitfall #26)
- [ ] For cron / monitoring jobs that need ATL alerts: consider running `python scripts/atl_check.py --json` and parsing the output, instead of inlining the DetailData workflow
- [ ] For non-iTunes stores: prefer `--title` lookups over batch mode (Pitfall #30); don't claim "all four stores" coverage without per-title verification

## Source

- API docs: https://www.cheapcharts.com/us/ai (llms.txt)
- Website: https://www.cheapcharts.com
- The API is free, public, and specifically designed for AI agents. No auth headers needed.
