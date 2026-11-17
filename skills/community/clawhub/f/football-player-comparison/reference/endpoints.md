# football-player-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 1 platform group(s).**

## FotMob (6)

### `fotmob_match`

- **HTTP:** `GET /fotmob/match`
- **What:** FotMob match details. Returns FotMob's public match-details payload, including available facts, events, statistics, lineups, shot map, momentum, table and head-to-head sections. The data field preserves the upstream JSON shape; individual sections may be absent for a match.
- **Params:** `id` (string, **required**) — Numeric FotMob match id

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
