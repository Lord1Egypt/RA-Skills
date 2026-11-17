# fotmob-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**31 endpoints across 1 platform group(s).**

## FotMob (31)

### `fotmob_audio_matches`

- **HTTP:** `GET /fotmob/audio-matches`
- **What:** FotMob matches with audio commentary. Returns FotMob's current match-to-audio-language availability index. Match ids are open-ended and can be passed to /fotmob/match. The list is independent of a selected match date and may include matches outside the current fixtures feed.
- **Params:** _none_

### `fotmob_fifa_ranking_periods`

- **HTTP:** `GET /fotmob/fifa-ranking-periods`
- **What:** FotMob FIFA ranking period directory. Lists the FIFA ranking periods FotMob currently offers for the required `gender` (`men` or `women`). Each period has a `periodId` and a `periodName` date label. Pass a `periodId` to the FotMob FIFA rankings endpoint; the ids change over time and are not a fixed set.
- **Params:** `gender` (string, **required**) — Ranking gender

### `fotmob_fifa_rankings`

- **HTTP:** `GET /fotmob/fifa-rankings`
- **What:** FotMob FIFA national-team rankings. Returns ranked national-team points and rank changes for one period. Discover valid periodId values for the selected gender from /fotmob/fifa-ranking-periods.
- **Params:** `gender` (string, **required**) — Ranking gender; `period_id` (string, **required**) — Period id returned for this gender by /fotmob/fifa-ranking-periods

### `fotmob_latest_news`

- **HTTP:** `GET /fotmob/latest-news`
- **What:** FotMob latest football news. Returns the global English latest-news feed. Items are article previews; the upstream response contains up to 20 items per offset. Use start_index increments of 20 to page without overlap.
- **Params:** `start_index` (integer, optional) — Zero-based news offset; defaults to 0

### `fotmob_league`

- **HTTP:** `GET /fotmob/league`
- **What:** FotMob league details and sections. Returns FotMob's public league page payload, including available tabs, overview, table, fixtures, statistics, transfers, and seasons where supplied by the league. Discover valid season values with /fotmob/seasons. shotmap=true includes the optional, larger overview shot-map payload.
- **Params:** `league_id` (integer, **required**) — Numeric FotMob league id from /fotmob/leagues; `season` (string, optional) — Optional season value from /fotmob/seasons for this league; `shotmap` (boolean, optional) — Include the optional overview shot map; increases response size

### `fotmob_leagues`

- **HTTP:** `GET /fotmob/leagues`
- **What:** FotMob competition directory. Returns FotMob's full public league directory grouped into popular, international, and country collections. Use league ids with other FotMob endpoints.
- **Params:** _none_

### `fotmob_lineup_builder_players`

- **HTTP:** `GET /fotmob/lineup-builder-players`
- **What:** FotMob lineup builder player metadata. Returns public metadata for 1 to 11 selected lineup players. Player ids are open-ended and can be discovered through /fotmob/search or /fotmob/lineup-builder-team. Unknown ids without complete public metadata return 404.
- **Params:** `player_ids` (string, **required**) — Comma-separated list of 1 to 11 numeric FotMob player ids

### `fotmob_lineup_builder_team`

- **HTTP:** `GET /fotmob/lineup-builder-team`
- **What:** FotMob lineup builder team data. Returns the public lineup builder's prefilled formation, starting lineup, and squad for a team id. Discover open-ended team ids with /fotmob/search. Some teams legitimately have no squad list.
- **Params:** `team_id` (string, **required**) — Numeric FotMob team id discoverable through /fotmob/search

### `fotmob_match`

- **HTTP:** `GET /fotmob/match`
- **What:** FotMob match details. Returns FotMob's public match-details payload, including available facts, events, statistics, lineups, shot map, momentum, table and head-to-head sections. The data field preserves the upstream JSON shape; individual sections may be absent for a match.
- **Params:** `id` (string, **required**) — Numeric FotMob match id

### `fotmob_match_media`

- **HTTP:** `GET /fotmob/match-media`
- **What:** FotMob match videos and media metadata. Returns the public highlight-video and media metadata for one match. The request uses FotMob's English United States variant; unavailable media is represented by null source fields.
- **Params:** `id` (string, **required**) — Numeric FotMob match id, discoverable from /fotmob/matches or /fotmob/search

### `fotmob_matches`

- **HTTP:** `GET /fotmob/matches`
- **What:** FotMob matches for a date. Returns FotMob's public match payload for a calendar date and IANA timezone. The data field preserves the upstream JSON shape.
- **Params:** `date` (string, **required**) — Date in YYYYMMDD format; `timezone` (string, optional) — IANA timezone; defaults to UTC

### `fotmob_news`

- **HTTP:** `GET /fotmob/news`
- **What:** FotMob league news. Returns a page of FotMob news items for one league. League ids are discoverable from /fotmob/leagues; start_index is a zero-based offset.
- **Params:** `league_id` (string, **required**) — Numeric FotMob league id; `start_index` (integer, optional) — Zero-based news offset; defaults to 0

### `fotmob_news_article`

- **HTTP:** `GET /fotmob/news-article`
- **What:** FotMob full top-news article. Returns the full article body for a FotMob-authored top-news story. Pass the complete id-and-slug value from the public /topnews/<id> URL. News previews from external publishers remain external and are not fetched.
- **Params:** `id` (string, **required**) — Complete FotMob top-news article id and slug from the public article URL

### `fotmob_player`

- **HTTP:** `GET /fotmob/player`
- **What:** FotMob player profile. Returns a public FotMob player profile, including current team, injuries, recent matches, career history, trophies, market values, and the player-specific season identifiers needed for deeper statistics. Discover player ids through /fotmob/search. Market values are included by default.
- **Params:** `id` (string, **required**) — Numeric FotMob player id from fotmob/search; `include_market_values` (boolean, optional) — Include market-value history; defaults to true

### `fotmob_player_match_stats`

- **HTTP:** `GET /fotmob/player-match-stats`
- **What:** FotMob player match stats. Returns the public per-match stat rows for one player, including the available stat key, value, and translated label. Discover player ids through fotmob/search and match ids through fotmob/match or fotmob/player-matches.
- **Params:** `match_id` (string, **required**) — Numeric FotMob match id; `player_id` (string, **required**) — Numeric FotMob player id

### `fotmob_player_matches`

- **HTTP:** `GET /fotmob/player-matches`
- **What:** FotMob player match history. Returns one page of player match history. The player's matchFilters and permitted league/team pairs are discovered from /fotmob/player. For another page, copy the numeric before timestamp from the upstream previous URL.
- **Params:** `before` (string, optional) — Numeric before timestamp from the upstream previous URL; omit for the newest page; `league_id` (string, optional) — all, or a numeric league id from fotmob/player matchFilters; `player_id` (string, **required**) — Numeric FotMob player id from fotmob/search; `team_id` (string, optional) — all, or a numeric team id paired with league_id in fotmob/player matchFilters

### `fotmob_player_stats`

- **HTTP:** `GET /fotmob/player-stats`
- **What:** FotMob player season statistics. Returns deep statistics, shot map, heatmap, and goalkeeper shot map for one player-specific season entry. Discover valid season_id values and hasDeepStats from /fotmob/player statSeasons; entry ids vary by player and season.
- **Params:** `player_id` (string, **required**) — Numeric FotMob player id from fotmob/search; `season_id` (string, **required**) — Player-specific entryId from fotmob/player statSeasons

### `fotmob_search`

- **HTTP:** `GET /fotmob/search`
- **What:** Search FotMob entities. Returns public search suggestions for FotMob leagues, teams, players, and matches. term must contain 1 to 50 characters. Suggestions preserve the upstream JSON shape.
- **Params:** `term` (string, **required**) — Search phrase, 1 to 50 characters

### `fotmob_seasons`

- **HTTP:** `GET /fotmob/seasons`
- **What:** FotMob league season discovery. Lists the season values FotMob offers for one league, identified by the required numeric `league_id` (from the FotMob leagues endpoint). The response has the league id, name and a `seasons` list such as `2026/2027`. Pass a season to the FotMob league endpoint; the list varies by league.
- **Params:** `league_id` (integer, **required**) — Numeric FotMob league id from /fotmob/leagues

### `fotmob_stats`

- **HTTP:** `GET /fotmob/stats`
- **What:** FotMob league player or team statistics. Returns ranked player or team statistics for a stat id discovered from /fotmob/stats-categories. The accepted stat ids vary by league, season, and type. team_id optionally restricts player statistics to one team. position filters player results client-side.
- **Params:** `league_id` (string, **required**) — Numeric FotMob league id; `position` (string, optional) — Optional client-side player position filter; `season_id` (string, optional) — Numeric season id from /fotmob/stats-categories; defaults to the newest season; `stat` (string, **required**) — Stat id returned by /fotmob/stats-categories for this league, season, and type; `team_id` (string, optional) — Optional numeric team id to filter player stats; `type` (string, **required**) — Stats subject

### `fotmob_stats_categories`

- **HTTP:** `GET /fotmob/stats-categories`
- **What:** FotMob league stat categories and seasons. Returns FotMob's current stat catalog and available seasons for a league. With season_id omitted, the response exposes the season list and initial top-stat choices; pass a returned season id to retrieve that season's full player or team stat catalog.
- **Params:** `league_id` (string, **required**) — Numeric FotMob league id; `season_id` (string, optional) — Numeric season id; omit to discover seasons; `type` (string, **required**) — Stats subject

### `fotmob_table`

- **HTTP:** `GET /fotmob/table`
- **What:** FotMob league table. Returns the league standings and the upstream table views, including all, home, away, form, and expected-goals tables. League ids are discoverable from /fotmob/leagues.
- **Params:** `league_id` (string, **required**) — Numeric FotMob league id

### `fotmob_team`

- **HTTP:** `GET /fotmob/team`
- **What:** FotMob team details. Returns public team data and the sections currently available for that team, such as overview, table, fixtures, squad, stats, transfers, and history. Team ids can be found with /fotmob/search. The upstream section set varies by team. For older fixtures, pass fixtures.previousFixturesUrl to /fotmob/team-fixtures.
- **Params:** `id` (string, **required**) — Numeric FotMob team id

### `fotmob_team_fixtures`

- **HTTP:** `GET /fotmob/team-fixtures`
- **What:** FotMob paginated team fixtures. Returns one page of older team matches. Start with the fixtures.previousFixturesUrl cursor from /fotmob/team, then pass each response's previous value as cursor until it is empty or null. Team ids are open-ended numeric ids discoverable through /fotmob/search.
- **Params:** `cursor` (string, **required**) — Opaque cursor copied from fixtures.previousFixturesUrl in /fotmob/team or previous in the preceding response; `team_id` (string, **required**) — Numeric FotMob team id

### `fotmob_team_news`

- **HTTP:** `GET /fotmob/team-news`
- **What:** FotMob team news. Returns the paginated article feed shown on a public FotMob team news page. Team ids can be found with /fotmob/search or /fotmob/team.
- **Params:** `start_index` (integer, optional) — Zero-based news offset from 0 through 10000; `team_id` (integer, **required**) — Numeric FotMob team id

### `fotmob_transfers`

- **HTTP:** `GET /fotmob/transfers`
- **What:** FotMob transfer center. Returns confirmed transfers, rumours, or popular transfers with the public transfer-center filters. Fee values are in EUR. Use fotmob/leagues and fotmob/search to discover league and team ids. The upstream returns 50 rows per page and caps its hit count at 10,000.
- **Params:** `direction` (string, optional) — Transfer direction; applied when league_ids or team_ids is supplied; `exclude_extensions` (boolean, optional) — Exclude contract-extension records; `last` (string, optional) — Time window; `league_ids` (string, optional) — Comma-separated numeric FotMob league ids, up to 50; discover with /fotmob/leagues; `likely_only` (boolean, optional) — Return only likely rumours; mode must be rumours; `max_fee` (integer, optional) — Maximum transfer fee in EUR; `min_fee` (integer, optional) — Minimum transfer fee in EUR; `mode` (string, optional) — Feed mode; `order_by` (string, optional) — Sort column; `page` (integer, optional) — One-based result page; 50 rows per page; `team_ids` (string, optional) — Comma-separated numeric FotMob team ids, up to 50; discover with /fotmob/search

### `fotmob_trending_news`

- **HTTP:** `GET /fotmob/trending-news`
- **What:** FotMob trending football news. Returns the five-story Trending shelf shown on FotMob's public News page. Items are curated previews and may overlap the global latest-news feed; the upstream list is dynamic. No locale or country parameter is exposed because the complete accepted value space is not pinned.
- **Params:** _none_

### `fotmob_trending_searches`

- **HTTP:** `GET /fotmob/trending-searches`
- **What:** FotMob trending search suggestions. Returns FotMob's current grouped trending suggestions for all entities, players, teams, and leagues. The feed is dynamic and may vary by the upstream's inferred region; no region or category parameter is exposed.
- **Params:** _none_

### `fotmob_tv_guide`

- **HTTP:** `GET /fotmob/tv-guide`
- **What:** FotMob football TV guide. Returns the public seven-day football broadcast schedule for a country, with local schedule times. Discover all accepted country codes from /fotmob/tv-guide-countries. Timezone defaults to UTC.
- **Params:** `country` (string, **required**) — Market code from /fotmob/tv-guide-countries; `timezone` (string, optional) — IANA timezone for local times

### `fotmob_tv_guide_channels`

- **HTTP:** `GET /fotmob/tv-guide-channels`
- **What:** FotMob TV guide channels. Discovers channels attached to matches in the selected country's current seven-day public TV guide window. Use the country directory to discover the complete country code set.
- **Params:** `country` (string, **required**) — Market code from /fotmob/tv-guide-countries

### `fotmob_tv_guide_countries`

- **HTTP:** `GET /fotmob/tv-guide-countries`
- **What:** FotMob TV guide country directory. Lists the countries in FotMob's football TV guide country selector, each with a country `code` (such as `us`, `gb`, `de` or `jp`) and a name. Use a code with the FotMob TV guide and TV guide channels endpoints. It takes no parameters.
- **Params:** _none_
