# gaming-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**35 endpoints across 3 platform group(s).**

## Steam (21)

### `steam_achievements`

- **HTTP:** `GET /steam/achievements`
- **What:** Get global achievement completion percentages for a Steam app. Returns the global unlock percentage for each of an app's achievements, sorted most-unlocked first. Apps without global achievement stats return an empty list.
- **Params:** `appid` (string, **required**) — Numeric Steam app id

### `steam_app`

- **HTTP:** `GET /steam/app`
- **What:** Get Steam store details for an app. Returns store metadata for a single Steam app (title, type, price, developers/publishers, platforms, genres, categories, release date, metacritic, recommendation and achievement counts). cc selects the store region (and price currency) and l the text language. filters is a comma-separated subset of allowed fields to shrink the payload.
- **Params:** `appid` (string, **required**) — Numeric Steam app id; `cc` (string, optional) — Store country code (ISO, selects currency); `filters` (string, optional) — Comma-separated fields: basic, price_overview, developers, publishers, categories, genres, release_date, platforms, metacritic, achievements, screenshots, movies, recommendations, controller_support, dlc, short_description, supported_languages, packages, package_groups, ratings, content_descriptors, background; `l` (string, optional) — Language code

### `steam_category`

- **HTTP:** `GET /steam/category/{slug}`
- **What:** Browse a store category (tag) with weighted community tags. Returns a catalog slice for a community tag / category, carrying each item's WEIGHTED community tags, review-score breakdown, developer/publisher credits, release date, platforms and price. The slug is a numeric tag id or a tag name (case- and separator-insensitive, e.g. rogue_like); resolve ids via /steam/tags/list. Ordering is Steam's default relevance — for sorted or os/price-faceted browse use /steam/tags.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `coming_soon_only` (boolean, optional) — Only unreleased / coming-soon titles; `count` (integer, optional) — Results per page (max 100); `free` (boolean, optional) — Only free titles; `l` (string, optional) — Steam store language name; `released_only` (boolean, optional) — Only already-released titles; `slug` (string, **required**) — Community tag id (numeric) or tag name slug; `start` (integer, optional) — Result offset for pagination

### `steam_charts_concurrent`

- **HTTP:** `GET /steam/charts/concurrent`
- **What:** Get Steam's live games-by-concurrent-players leaderboard. Returns the live leaderboard of games ranked by current concurrent players (rank, appid, current concurrent, peak). By default each row is enriched with the game name and review summary; pass enrich=false for raw ranked app ids.
- **Params:** `cc` (string, optional) — Store country code (ISO) for name enrichment; `enrich` (boolean, optional) — Attach game name and review summary to each rank; `l` (string, optional) — Steam store language name for name enrichment

### `steam_charts_most_played`

- **HTTP:** `GET /steam/charts/most-played`
- **What:** Get Steam's weekly most-played games chart. Returns Steam's weekly most-played chart: the top games ranked by peak concurrent players over the last week (rank, appid, previous-week rank, peak players). By default each row is enriched with the game name and review summary; pass enrich=false for the raw ranked app ids only.
- **Params:** `cc` (string, optional) — Store country code (ISO) for name enrichment; `enrich` (boolean, optional) — Attach game name and review summary to each rank; `l` (string, optional) — Steam store language name for name enrichment

### `steam_charts_top_releases`

- **HTTP:** `GET /steam/charts/top-releases`
- **What:** Get Steam's monthly best-new-releases index. Returns Steam's monthly top-releases index: one page per month, each listing that month's top-released app ids (with the month label and start date). The app-id lists are large and not name-enriched; resolve names via /steam/items.
- **Params:** _none_

### `steam_community_recommendations`

- **HTTP:** `GET /steam/community-recommendations`
- **What:** Get the store's community-recommended reviews feed. Returns a batch of recent, quality user reviews recommended across the whole store (author, playtime, helpful votes, and the recommended app). Filter by review kind/sort, reviewer playtime window, review language, and store region. The endpoint serves a fixed batch and does not support tag filtering or deep pagination.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code; `playtime_max` (integer, optional) — Maximum reviewer playtime in hours (0 = no maximum); `playtime_min` (integer, optional) — Minimum reviewer playtime in hours (0 = no minimum); `review_filter` (string, optional) — Review kind / sort; `review_language` (string, optional) — Review language: 'my_languages' or a Steam language name

### `steam_featured`

- **HTTP:** `GET /steam/featured`
- **What:** Get the Steam store featured capsules. Returns the storefront's featured capsules for a region (per-platform featured lists plus large spotlight capsules), including discount and price fields.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code

### `steam_featured_categories`

- **HTTP:** `GET /steam/featured-categories`
- **What:** Get Steam top sellers, new releases, specials and coming soon. Returns the storefront merchandising buckets for a region: specials, top_sellers, new_releases, and coming_soon, each with its item list.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code

### `steam_items`

- **HTTP:** `GET /steam/items`
- **What:** Resolve a batch of app ids to store items with weighted tags. Resolves up to 100 Steam app ids in one call to store items, each carrying its WEIGHTED community tags, review-score breakdown, developer/publisher credits, release date, platforms and price. The batch enrichment primitive for the community-tag taxonomy.
- **Params:** `appids` (string, **required**) — Comma-separated numeric app ids (max 100); `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Steam store language name

### `steam_news`

- **HTTP:** `GET /steam/news`
- **What:** Get recent news posts for a Steam app. Returns recent news and announcement posts for a Steam app by numeric `appid` (for example `570`). `count` sets the number of posts (default 10, max 50) and `maxlength` caps each post body in characters (default 300, `-1` for the full body). Each post has `gid`, title, URL, author, contents, feed label and name, `date`, `is_external_url` and `tags`.
- **Params:** `appid` (string, **required**) — Numeric Steam app id; `count` (integer, optional) — Number of posts (max 50); `maxlength` (integer, optional) — Max characters of each post body; default 300, set -1 for full content

### `steam_package`

- **HTTP:** `GET /steam/package`
- **What:** Get Steam store details for a package. Returns details for a Steam package (a purchasable bundle): name, the apps it contains, price, platforms, and release date. cc selects the store region and price currency.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code; `packageid` (string, **required**) — Numeric Steam package id

### `steam_players`

- **HTTP:** `GET /steam/players`
- **What:** Get the current concurrent-player count for a Steam app. Returns the current number of concurrent players for a Steam app, given its numeric `appid` such as `570`. The response has `appid`, `player_count` and a `source_url`. An app with no player-count data returns 404.
- **Params:** `appid` (string, **required**) — Numeric Steam app id

### `steam_reviews`

- **HTTP:** `GET /steam/reviews`
- **What:** List reviews for a Steam app. Returns a page of user reviews for an app with cursor pagination and an aggregate query_summary (score, positive/negative totals). Aggregate totals populate only on the first page (cursor=*). Pass the returned cursor back to page.
- **Params:** `appid` (string, **required**) — Numeric Steam app id; `cursor` (string, optional) — Pagination cursor from the previous page; `day_range` (integer, optional) — Look-back window in days (filter=all only, max 365); `filter` (string, optional) — Sort order; `language` (string, optional) — Steam language name or 'all'; `num_per_page` (integer, optional) — Reviews per page (max 100); `purchase_type` (string, optional) — Purchase source filter; `review_type` (string, optional) — Review sentiment filter

### `steam_reviews_histogram`

- **HTTP:** `GET /steam/reviews/histogram`
- **What:** Get the review up/down histogram for a Steam app. Returns the positive/negative recommendation counts over time (the store review graph): weekly/monthly rollups plus recent daily buckets.
- **Params:** `appid` (string, **required**) — Numeric Steam app id; `language` (string, optional) — Steam language name or 'all'

### `steam_search`

- **HTTP:** `GET /steam/search`
- **What:** Search the Steam store by title. Resolves a search term to Steam apps via the store typeahead (title, appid, price, platforms, metascore). Best for title -> appid lookup; returns roughly ten results. For faceted, paginated search use /steam/search/results.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code; `term` (string, **required**) — Search term

### `steam_search_results`

- **HTTP:** `GET /steam/search/results`
- **What:** Faceted, paginated Steam store search. Runs the Steam store search with pagination and sorting and returns the result rows (appid, title, release date, review summary, price, platforms). Supports start/count paging and sort_by.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `count` (integer, optional) — Results per page (max 100); `l` (string, optional) — Language code; `sort_by` (string, optional) — Sort order; `start` (integer, optional) — Result offset for pagination; `term` (string, **required**) — Search term

### `steam_steamspy`

- **HTTP:** `GET /steam/steamspy`
- **What:** Get SteamSpy third-party ownership and playtime estimates. Returns third-party ownership, concurrent-user, playtime, and review estimates for an app from SteamSpy. These are SteamSpy estimates, not official Steam figures.
- **Params:** `appid` (string, **required**) — Numeric Steam app id

### `steam_tags`

- **HTTP:** `GET /steam/tags`
- **What:** Browse the Steam store by community tag and store facets. Browses the store by the community-tag taxonomy (Roguelike, Metroidvania, Cozy...) and the store filter facets, with no free-text term. Filter by one or more tag ids, a store category id, platform (os), a maximum price, specials-only, and hide-free-to-play; sort and page the browse-rank rows. Each row includes its community tag ids (resolve names via /steam/tags/list). Pagination runs the full result set (total is the real, fully-pageable match count); paging past total returns an empty page.
- **Params:** `category1` (string, optional) — Numeric Steam store category id (e.g. 998 games, 21 dlc); `category2` (string, optional) — Additional numeric store category id (feature); `category3` (string, optional) — Additional numeric store category id (feature); `cc` (string, optional) — Store country code (ISO, selects currency); `count` (integer, optional) — Results per page (max 100); `deck_compatibility` (string, optional) — Steam Deck compatibility filter: 1 unsupported, 2 playable, 3 verified; `filter` (string, optional) — Curated preset applied within the other facets; `hidef2p` (boolean, optional) — Hide free-to-play titles; `l` (string, optional) — Language code; `maxprice` (string, optional) — Maximum price as whole cents in the cc currency, or the literal 'free'; `os` (string, optional) — Comma-separated platform filter subset of: win, mac, linux; `sort_by` (string, optional) — Sort order; `specials` (boolean, optional) — Only discounted titles; `start` (integer, optional) — Result offset for pagination; `supportedlang` (string, optional) — Only titles supporting this Steam language name; `tags` (string, optional) — Comma-separated numeric community tag ids (all must match); resolve ids via /steam/tags/list; `untags` (string, optional) — Comma-separated numeric community tag ids to EXCLUDE; `vrsupport` (string, optional) — Comma-separated VR-support filter ids (e.g. 401 seated, 402 standing, 403 roomscale)

### `steam_tags_list`

- **HTTP:** `GET /steam/tags/list`
- **What:** List Steam community tag ids and names. Returns Steam's popular community tags (numeric id + localized name) so callers can map a tag name to the id that /steam/tags and /steam/category expect.
- **Params:** `l` (string, optional) — Steam store language name for the tag labels

### `steam_top_sellers`

- **HTTP:** `GET /steam/top-sellers`
- **What:** Get Steam's weekly top-sellers chart for a country. Returns the store's weekly top-sellers chart for a country, each rank carrying the full store item (name, price, weighted community tags, review summary, platforms). cc selects the country whose sales ranking and currency are returned.
- **Params:** `cc` (string, optional) — Country code (ISO) whose weekly sales ranking is returned; `l` (string, optional) — Steam store language name

## PlayStation (10)

### `playstation_browse`

- **HTTP:** `GET /playstation/browse`
- **What:** Browse the PlayStation Store all-games grid. Returns a page of the PlayStation Store "all games" grid with per-item price, platforms, and media, plus the available filter facets (price, genre, platform, subscription, content type, etc.) with value counts. Pass page to advance; next_page is set when more results exist. cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code; `page` (integer, optional) — 1-based page number

### `playstation_category`

- **HTTP:** `GET /playstation/category`
- **What:** Browse a PlayStation Store category grid. Returns a page of a specific PlayStation Store category grid (by category UUID) with per-item price, platforms, and media, plus the available filter facets with value counts. Pass page to advance; next_page is set when more results exist. cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `id` (string, **required**) — Category UUID; `l` (string, optional) — Language code; `page` (integer, optional) — 1-based page number

### `playstation_concept`

- **HTTP:** `GET /playstation/concept`
- **What:** Get PlayStation Store details for a concept (game hub). Returns store metadata for a PlayStation concept: title, publisher, release date, platforms, genres, description, content rating, aggregate star rating, the default product's purchase price, media, and the full lists of purchasable editions and add-ons. cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `id` (string, **required**) — Numeric PlayStation concept id; `l` (string, optional) — Language code

### `playstation_concept_reviews`

- **HTTP:** `GET /playstation/concept/reviews`
- **What:** Get PlayStation concept reviews. Returns one page of written PlayStation Store reviews for a concept (game hub), each with its title, body, rating, helpful count, spoiler flag, the edition the reviewer owned, and reviewer identity (online id, PS Plus subscriber status, verified-purchase status, avatar). Also includes the concept's aggregate star rating (including its rating distribution). page/page_size page through the full review list (total_count reports the true upstream review count, has_next_page whether a later page has more), sort controls ordering, and rating optionally filters to one star value. Reviews are region-scoped: cc selects the store region whose reviews are returned (and the price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO); `id` (string, **required**) — Numeric PlayStation concept id; `l` (string, optional) — Language code; `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Reviews per page; `rating` (integer, optional) — Filter to one star rating (1-5); `sort` (string, optional) — Sort order

### `playstation_deals`

- **HTTP:** `GET /playstation/deals`
- **What:** Get PlayStation Store deals shelves. Returns the PlayStation Store deals landing page as a list of merchandising shelves (sections), each with its titles and per-item price, plus a flattened, de-duplicated item list across all shelves. cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code

### `playstation_latest`

- **HTTP:** `GET /playstation/latest`
- **What:** Get PlayStation Store latest-release shelves. Returns the PlayStation Store latest-releases landing page as a list of merchandising shelves (sections), each with its titles and per-item price, plus a flattened, de-duplicated item list across all shelves. cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code

### `playstation_page`

- **HTTP:** `GET /playstation/page`
- **What:** Get a PlayStation Store merchandising page by alias. Reads any PlayStation Store merchandising page by alias (e.g. collections, subscriptions, or a promotional alias) and returns its shelves (sections) plus the curated collection links found on the page. Each collection link carries a category_id (UUID) you can pass to /playstation/category to fetch that collection's full, paginated title grid. Known aliases: collections, subscriptions, deals, latest. cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `alias` (string, **required**) — Merchandising page alias; `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code

### `playstation_product`

- **HTTP:** `GET /playstation/product`
- **What:** Get PlayStation Store details for a single product. Returns store metadata for a single PlayStation product/edition: title, np title id, parent concept id, product type and store classification, edition name, publisher, release date, platforms, genres, spoken/screen languages, content rating, aggregate star rating, purchase price, and media. cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `id` (string, **required**) — PlayStation product id; `l` (string, optional) — Language code

### `playstation_search`

- **HTTP:** `GET /playstation/search`
- **What:** Search the PlayStation Store. Returns a page of PlayStation Store search results (concepts and products) for a term, with pagination and per-item price, platforms, classification, and media. Pass page to advance; next_page is set when more results exist. cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code; `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Results per page (max 48); `term` (string, **required**) — Search term

### `playstation_suggest`

- **HTTP:** `GET /playstation/suggest`
- **What:** Get PlayStation Store search suggestions for a term. Returns typeahead-style PlayStation Store search suggestions for a partial or full term: id, name, classification, platforms, publisher, release date, price, a representative image, and a direct store URL per match. Matching is upstream-ordered and loose (it may include titles that only loosely relate to the term), not a ranked exact-substring search. limit caps how many suggestions are returned (max 20; the upstream API does not honor a higher value). cc selects the store region (and price currency); l accepts a language code or locale such as en or en-US, with the locale's primary language used for text.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code; `limit` (integer, optional) — Maximum number of suggestions to return (max 20); `term` (string, **required**) — Search term (partial or full)

## Roblox (4)

### `roblox_badges`

- **HTTP:** `GET /roblox/badges`
- **What:** List Roblox experience badges. Returns one cursor-paginated page of public badge metadata for a Roblox experience. Pass next_cursor back unchanged as cursor. No user-awarded badge data is returned.
- **Params:** `cursor` (string, optional) — Opaque cursor returned by a previous response; `universe_id` (integer, **required**) — Positive Roblox universe id

### `roblox_game`

- **HTTP:** `GET /roblox/game`
- **What:** Get a Roblox experience. Returns public catalog detail for one Roblox experience, including aggregate votes and its public icon. This endpoint does not return player, account, purchase, or server data.
- **Params:** `universe_id` (integer, **required**) — Positive Roblox universe id

### `roblox_rankings`

- **HTTP:** `GET /roblox/rankings`
- **What:** List Roblox game rankings. Returns one Roblox game ranking shelf, chosen by `sort_id`: `top-trending` (default), `up-and-coming`, `top-playing-now`, `fun-with-friends` or `top-revisited`. Each experience has its name, creator, genre, player count, up and down votes, maturity label, minimum age and URL. Shelves are global, not personalised.
- **Params:** `sort_id` (string, optional) — Ranking shelf: top-trending, up-and-coming, top-playing-now, fun-with-friends, top-revisited

### `roblox_search`

- **HTTP:** `GET /roblox/search`
- **What:** Search Roblox experiences. Searches Roblox experiences for `q` (1 to 256 characters). Each result has its universe and place ids, name, creator, genre, `player_count`, up and down votes, maturity and URL. Pass `next_page` back unchanged as `page_token` for the next page. No account, friend, purchase or inventory data is included.
- **Params:** `page_token` (string, optional) — Opaque page token returned by a previous search; `q` (string, **required**) — Experience search query
