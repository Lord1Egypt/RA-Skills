# CheapCharts API Pitfalls

> The empirically-discovered API behaviors this skill is built around. Each
> entry was verified against the live API on the date noted. Load this file
> when a call misbehaves or before building a new workflow.
>
> **Maintenance rule: append only - never renumber.** Cross-references to
> pitfall numbers exist in SKILL.md, RECIPES.md, and `scripts/deals.py`.
> The weekly CI canary (`.github/scripts/canary_pitfalls.py`) re-tests the
> load-bearing entries (#13, #16, #21, #23, #26, #28) and opens an issue on drift.

The six pitfalls most likely to silently break a workflow: [#13](#13-detaildata-itemtype-is-movies-or-seasons---not-buymovies) (DetailData vocabulary), [#15](#15-always-check-responsestatus-before-iterating-results) (status check), [#16](#16-has4k1-filter-does-not-work-on-dealscharts) (has4K broken), [#21](#21-genre-filter-is-broken-for-seasons-on-deals-charts-and-recommendations) (seasons genre), [#26](#26-pricehdevolution--pricesdevolution-values-are-absolute-prices-not-deltas) (evolution semantics), [#28](#28-there-is-no-batch-detaildata-endpoint) (no batch DetailData).

### 1. Using wrong itemType for Prices

Prices requires `buymovies` (not `movies`). Search returns `priceFollowUpItemType` - use that value for the Prices follow-up call.

### 2. Forgetting to URL-encode the query

Use `%20` for spaces in `query` parameter, not literal spaces.

### 3. Expecting all fields on all stores

`has4K`, `hasAtmos`, `hdrFormat`, `isMovieBundle` are iTunes-only. Amazon/Vudu/Google Play items won't have these fields.

### 4. Search returns mixed media types

`itemType=all` returns movies, seasons, ebooks, audiobooks, and albums. Filter by `mediaType` in your processing if the user only wants movies/TV.

### 5. Topseller has4K is numeric

Topseller may return `1`/`0` instead of `true`/`false` for `has4K`/`hasAtmos`. Handle both.

### 6. artist may be empty string

Not all stores provide director/creator names. Don't rely on it being populated.

### 7. Seasons/bundles lack IMDb IDs - Prices API explicitly rejects seasons

The Prices endpoint returns an error: "Prices API supports ONLY movies (buymovies), not seasons." The Search endpoint returns `idInStore` but no price for seasons. **Solution: use the internal `DetailData.php` endpoint** (see [API.md](API.md#7-detaildata-internal---detaildataphp)) with the `idInStore` from Search results. This returns current prices, full price history, and child seasons - all via HTTP, no browser needed. Workflow: Search (get idInStore) -> DetailData (get prices + history).

### 8. Bundle vs individual season pricing

When a user asks about a "complete series" bundle, always check the individual season prices too. Seasons go on sale independently, and buying them individually can be cheaper than the bundle (even when the bundle claims to save money vs regular individual prices). The product page shows "Other Seasons" with current sale prices for each season.

### 9. Fake drops / manipulated priceBefore

Some deals show a large `priceBefore -> price` drop that isn't real. Detect fake drops by: (a) checking if `priceBefore` equals `price` (no actual change - just the field is populated), (b) using DetailData's `priceHdEvolution` / `priceSdEvolution` to verify a genuine historical price change occurred, (c) filtering to `priceBefore > price` strictly (some items appear in Deals with no actual discount). When reporting deals, always calculate actual savings (`priceBefore - price`) and skip items where savings <= $0. If `priceBefore` looks suspiciously high compared to the price evolution history, flag it as a potentially inflated baseline.

### 10. Amazon/Vudu/Google Play Deals endpoint instability

The Deals endpoint for non-iTunes stores has been observed returning HTTP 500 errors server-side (noted June 2026). If Deals fails for a non-iTunes store, fall back to Topseller for that store, or retry later. iTunes Deals is the most reliable endpoint.

### 11. sort=releaseDate is ASCENDING only

The API accepts `releaseDate` (oldest first) but rejects `releaseDate_desc`, `newest`, `dateAdded`, `releaseDate_asc`, and every other date-sort variant tested (returns empty results). To get newest-first order, request with `sort=releaseDate&limit=500` and reverse client-side (Python/JS), OR narrow with `releaseYear=YYYY-YYYY` first and then pick what you need from the smaller result set.

### 12. Bundle placeholder dates pollute releaseDate sort

Many movie bundles have `releaseDate=2030-12-31` or `2026-12-31` - obvious placeholder values, not real release dates. They cluster at the top of `releaseDate` ascending results and look like "the newest" if you don't filter. Strip them client-side (e.g. `if not releaseDate.startswith('2030')`) before reporting "newest releases." Single-movie titles almost always have real dates; the issue is specifically with multi-film bundles.

### 13. DetailData itemType is movies or seasons - NOT buymovies

The Deals endpoint uses `itemType=buymovies` for movies, but DetailData uses a DIFFERENT vocabulary. Valid DetailData itemType values are: `singles, albums, movies, seasons, audiobooks, ebooks, apps, macapps, games`. Passing `itemType=buymovies` to DetailData returns an error: `Expected value for <itemType> not set or invalid`. This silently fails in scripts that don't check the `status` field, making it look like there's no price-change data when there actually is. **Always use `movies` for movies and `seasons` for TV when calling DetailData.**

### 14. CheapCharts data lags Apple's store

Apple's price changes can take hours to a full day to propagate to the CheapCharts API. If `sort=latestPricechange` returns items but none have a `priceHdLastChangeDate` matching today, that is a legitimate "no drops detected today yet" - re-query in a few hours. Don't treat an empty today-list as a bug.

### 15. Always check response.status before iterating results

Every endpoint returns `{"status":"success", ...}` on success or `{"status":"error", "message":"..."}` on failure. If you iterate `results` without checking status, a 400 error with empty `results: {}` silently yields no data - which looks identical to "no deals found." This is how the 2026-06-21 "no drops today" bug happened: passing `itemType=buymovies` to DetailData returned a status=error, the script iterated an empty dict, and reported "nothing today" when The Harvest had actually just dropped. **Pattern: `if response.get('status') != 'success': print(response.get('message')); return`.**

### 16. has4K=1 filter does NOT work on Deals/Charts

Tested with iTunes US: passing `has4K=1` returns the same items with `has4K=0` in the response - the parameter is silently ignored. To filter to 4K-only deals, filter client-side after the API call (`if item.get('has4K') in (1, True): ...`). The field exists in item data (as `has4K`, `hasAtmos`, `hdrFormat`) but is not honored as a query parameter.

### 17. DetailData is unofficial

Only Search, Charts, Deals, Prices, Recommendations, and Topseller are in the official gptapi docs. DetailData.php was discovered by inspecting CheapCharts' website network calls and is not promised to stay stable. If it starts returning errors, fall back to Prices (movies only) or just present the current Deals data without history verification.

### 18. Recommendations.php may return chart data when no genre filter is set

Tested: calling Recommendations with `genre=All` returns items with `rank` fields and matches the Charts endpoint output. The underlying API uses `OfferList.php?listType=charts`. If you want curated recommendations rather than just top-of-charts, pass a specific `genre` (e.g. `SciFiFantasy`) and an `imdbRating` filter.

### 19. Apple TV / iTunes terminology

Official CheapCharts docs confirm: "iTunes" and "Apple TV" are used interchangeably. When the user says "Apple TV deal" or "iTunes deal" or "buy on Apple", treat them all as `store=itunes`. Apple rebranded iTunes Movies & TV Shows to the Apple TV app in 2019; the underlying purchase catalog is the same.

### 20. JSON-LD fallback for unsupported queries

Key CheapCharts website pages (search results, deal list pages, movie detail pages) embed JSON-LD `potentialAction` hints that link directly to the GPT API endpoints with pre-filled parameters. If a user asks for something the API doesn't support directly (e.g., browsing a specific store page), browse the relevant cheapcharts.com page and parse the JSON-LD to discover the right API call.

### 21. genre filter is broken for seasons on Deals, Charts, AND Recommendations

Tested 2026-06-21: every `genre` value (`Drama`, `Comedy`, `Horror`, `ActionAdventure`, `KidsFamily`, `Anime`, `MadeForTV`, etc.) returns the exact same list of items - the parameter is silently ignored. The default sort/limit just returns the top of the unfiltered deals list. **For TV series filtering, omit the `genre` parameter entirely and filter by series name client-side (e.g., `if 'archie' in item['title'].lower()`).** Only `itemType=buymovies` honors the genre filter reliably.

### 22. genre filter silently falls back to "All" for unknown values on buymovies

Tested 2026-06-21: passing `genre=Latino`, `genre=Faith`, `genre=War`, `genre=asdfgarbage123`, etc. all return the same unfiltered deals list as `genre=All`. The API does NOT error - it just gives you everything. **If you pass a non-standard genre and get a large mixed-genre result set, that's a signal your genre value isn't recognized.** Stick to the documented Genre enum in [API.md](API.md#genre). (The bundled `deals.py` validates `--genre` case-insensitively against the enum for exactly this reason.)

### 23. imdbRating and rottenTomatoesRating filters work on Deals/Charts but NOT on Recommendations

Tested 2026-06-21: on `Deals?itemType=buymovies&imdbRating=8`, returned items with min rating 8.0 (works). On `Recommendations?itemType=buymovies&genre=Drama&imdbRating=8`, returned items with ratings 6.8, 7.3, 7.5 - the filter was silently ignored. **For rating-filtered recommendations, use Deals with `sort=greatestSavings` and the rating filter, NOT Recommendations.**

### 24. Movies Anywhere compatibility is NOT exposed by any CheapCharts endpoint

Tested 2026-06-21: no `isMoviesAnywhere` field exists in any of Search, Deals, Charts, Prices, Recommendations, Topseller, or DetailData responses. The Movies Anywhere website has no stable public API (returns JS-rendered HTML, no JSON-LD). Use the studio-based heuristic in [EXTRAS.md](EXTRAS.md#movies-anywhere-compatibility), or browse the MA website for definitive verification.

### 25. releaseYear works on Charts for both buymovies and seasons

Tested: `Charts?itemType=seasons&releaseYear=2025-2026` correctly returns seasons with release dates in that range. Confirms releaseYear is supported on Deals and Charts (already documented) but worth restating since the seasons endpoint's other filters are broken ([#21](#21-genre-filter-is-broken-for-seasons-on-deals-charts-and-recommendations)).

### 26. priceHdEvolution / priceSdEvolution values are absolute prices, not deltas

Format: `YYYY-MM-DD:[+|-]price~...`, newest segment first. **Each value is the ABSOLUTE price in effect from that date** - the `+`/`-` sign only marks the direction of the change (`+` rose to, `-` dropped to), and the rightmost segment (no sign) is the initial tracked price. Verified 2026-07-02 on Bernie (movies id 1875049429: `2026-06-23:-4.99~...~2026-02-17:12.99` reads "listed $12.99, ... dropped to $4.99" and reconciles exactly with `priceHd=4.99`, `priceHdBefore=12.99`) and on Tom & Jerry Kids Show: The Complete Series (seasons id 1550380051, 14 segments, all reconcile).

**History of this pitfall:** an earlier version (tested 2026-06-23) claimed the values were per-change deltas that "don't accumulate" - summing Bernie's values gave $27.00 instead of $4.99. That was a misdiagnosis: summing absolute prices as if they were deltas produces exactly that garbage. The data was consistent all along; the mental model was wrong.

Practical guidance:
- **For "is it at ATL right now":** still use `priceHdIsLowest` / `priceSdIsLowest` - a single authoritative flag beats parsing.
- **For "when was it on sale / what's the price history":** parse the evolution string with absolute-price semantics. The bundled script does this: `python scripts/deals.py --title "<name>" --history`.
- **Validation invariant:** the newest segment's value must equal the current `priceHd`/`priceSd`. The weekly CI canary checks this on live data and opens an issue if the semantics ever drift.

### 27. IsLowest vs IsBest

`priceHdIsLowest` / `priceSdIsLowest` is the canonical ATL flag - different from `priceHdIsBest` / `priceSdIsBest`. `IsLowest=1` means current price equals the all-time low across CheapCharts' tracked history. `IsBest=1` means current price is the floor of the CURRENT sale window - a previous sale may have gone lower (`IsLowest=0, IsBest=1` is common). Check `IsLowest` for "lowest ever" questions; check `IsBest` for "is this a good price right now" questions.

### 28. There is no batch DetailData endpoint

N+1 calls is the only way to enrich a Deals list with ATL data. Verified 2026-06-23: `DetailData.php` only accepts a single `idInStore` per call. Tested alternative param shapes (`idInStore=A&idInStore=B`, comma-separated `idInStore=A,B`, `ids=A,B`, `idInStores=A,B`) - all return empty `{}`. None of the public gptapi endpoints (Deals, Search, Prices, Charts, Recommendations, Topseller) expose the ATL flags. Use the bundled `scripts/deals.py` (parallel `ThreadPoolExecutor`, 8 workers) to make the N DetailData calls concurrent - empirically ~12s for 50 items vs ~150s for sequential.

### 29. Check scripts/ before adding a recipe

Before adding a recipe to this skill, check `scripts/` for an existing tool that already does the workflow. This skill ships with `scripts/deals.py` (parallel batch ATL checker with CLI flags, JSON output, proper exit codes). The skill's inline bash recipes for ATL filtering are 10-12x slower than the script (sequential DetailData calls vs parallel). Recipes should reference the script with a short invocation. When extending the skill: `ls scripts/` and `grep -n 'scripts/' SKILL.md` first, then add a one-line "run this script" recipe instead of inlining the workflow.

### 30. iTunes is the only store with reliable batch + complete catalog coverage

The script accepts `--store` for all four stores, and single-title lookups work on Amazon/Vudu/Google Play, but the underlying CheapCharts data is sparser on those stores and the Deals endpoint returns a server-side error (HTTP 500, "There was an error handling the request") for many batch queries. Verified 2026-06-23: `--store amazon --limit 10` exits with code 2, while `--store itunes --limit 10` returns 80+ deals. For non-iTunes stores, prefer `--title <name>` lookups over batch mode, or fall back to Topseller (`gptapi/Topseller.php` with `store=itunes,amazon,vudu,googlePlay`) if you need cross-store batch data. Don't promise "all four stores" in agent reports without verifying the data for the specific title or genre.

### 31. priceBefore < price is signal, not noise - it means the sale just ended

Verified 2026-06-24: on 20 classic-noir titles, 13 had `priceBefore < current price` (e.g. `now=$9.99, was=$4.99`) - the price went *up* at the last change, meaning the title was at $4.99 recently and the sale just expired. This is exactly the kind of title a user wants flagged as a "next drop target." **Do not render these rows as "-/--/--"** (treating absence of active savings as absence of useful info). The standard deal-report table (Presentation Guidelines in SKILL.md) needs a status column - "sale ended" with the prior low price shown in the `Was` column - alongside "on sale" and "small sale." When you filter the Deals list down to "currently on sale," mention the sale-ended cohort separately so the user can decide whether to set an alert. The `priceHdDropIndicator` field tells you the direction without comparing `priceBefore` yourself: `1` = went up, `-1` = went down, `0` = unchanged.

### 32. Never fabricate store-direct URLs - the response always has them

CheapCharts' DetailData response includes `productPageUrl` and `iTunesUrl` (the direct Apple TV purchase link) for every title, and `cheapChartsProductPageUrl` for the CheapCharts price-history page. These are emitted as full URLs - do not pattern-match or reconstruct them from `idInStore`. Verified 2026-06-24: a session attempted to reconstruct 20 plausible-looking Apple TV slugs by extending `idInStore` with a guessed `umc.cmc.<hash>` pattern; every one was a 404. The real URLs are in the response. If the field is missing from the response, render the link as the title in plain text (no link) and note "store URL unavailable" rather than guessing.

### 33. v3.0 reframed the script from "ATL-only" to "deals with ATL flag" - old defaults no longer apply

Prior to v3.0, `atl_check.py` (now renamed `deals.py`) filtered to ATL-only deals by default. As of v3.0.0 (2026-06-24), the default is to show all current deals with an ATL column flag (`ATL` or `-`), and the ATL-only behavior moved behind the `--atl-only` flag. If a user asks "show me all the deals," they expect the v3.0 default (all deals, ATL as a column). If they ask "what's at its all-time low," that's `--atl-only`. If they ask "show me today's drops," use `--since 1` (v3.1+) or the default `latestPricechange` sort. When in doubt, the user's question word "just" or "only" is a strong signal for `--atl-only`.

### 34. --min-savings is a threshold, not a category filter - it can return the same titles as a different threshold

The script has no `--bundle-only` flag. Bundles have larger regular prices (e.g. $99.99 -> $14.99) so high savings thresholds (e.g. `--min-savings 30`) *correlate* with bundles, but don't *define* them. Verified 2026-06-24 building the v2.3.2 demo panels: `--type buymovies --min-savings 5 --limit 12` and `--min-savings 30 --limit 12` against the same iTunes US feed returned the same 5 titles in the same order (all happened to be 14-25 film collections). The second run was labeled "bundle deals" in the panel but was actually just a stricter savings threshold. To get a true bundle-only list, fetch each candidate's `isMovieBundle` from DetailData and filter client-side. Don't label a savings-threshold run as "bundle deals" (or "season deals", or "individual movies") unless you've actually filtered for that category - and if you have, mention the filter in the panel caption so a reader doesn't take it at face value.

### 35. sort=greatestSavings puts bundles at the top; sort=latestPricechange puts individual movies at the top

Verified 2026-06-24: with iTunes US Deals, `sort=greatestSavings --limit 30` returned 30/30 bundles (because $99.99 -> $14.99 beats any single-movie deal in absolute savings). `sort=latestPricechange --limit 30` returned 1/30 bundles and 29/30 individual movies. When you need individual movies with ratings (e.g. for a demo panel showing IMDb scores), use `--sort latestPricechange` and consider also `--exclude-bundles` to be sure. Conversely, when you actually want bundles, use `--sort greatestSavings` without `--exclude-bundles` to get the full bundle list. The sort choice *is* the category filter for movie-vs-bundle dominance on this endpoint.

### 36. isMovieBundle is the canonical bundle-marker for Deals items, not mediaType

Verified 2026-06-24: Deals items return `isMovieBundle: 0` or `1` (an int), but `mediaType` and `itemType` are `None` on the same items. Search items return `mediaType` (e.g. `"movies"`, `"seasons"`) but not `isMovieBundle`. The two endpoints use different field conventions. **For Deals / DetailData flows: check `isMovieBundle`. For Search-then-Prices flows: check `mediaType`.** The script's `--exclude-bundles` flag uses `isMovieBundle` because it operates on Deals candidates, not Search results. Don't try to use `--exclude-bundles` after a Search call - the field won't be there.

### 37. imdbRating and rottenTomatoesRating are Deals candidate fields, not DetailData fields

Verified 2026-06-24: Deals items have `imdbRating` and `rottenTomatoesRating` populated (e.g. *Django Unchained* returns `imdbRating: 8.5, rottenTomatoesRating: 87`); DetailData items do NOT (DetailData's node is price/history only). The script copies these into the output at the candidate-merge step. When building the report, render ratings for individual movies (where `isMovieBundle == 0`); for bundles and TV seasons, render `-` because the field is absent on the source data, not because of a script bug. Same applies to `imdbId`.
