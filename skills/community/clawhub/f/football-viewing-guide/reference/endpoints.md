# football-viewing-guide — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**9 endpoints across 2 platform group(s).**

## FotMob (6)

### `fotmob_match`

- **HTTP:** `GET /fotmob/match`
- **What:** FotMob match details. Returns FotMob's public match-details payload, including available facts, events, statistics, lineups, shot map, momentum, table and head-to-head sections. The data field preserves the upstream JSON shape; individual sections may be absent for a match.
- **Params:** `id` (string, **required**) — Numeric FotMob match id

### `fotmob_matches`

- **HTTP:** `GET /fotmob/matches`
- **What:** FotMob matches for a date. Returns FotMob's public match payload for a calendar date and IANA timezone. The data field preserves the upstream JSON shape.
- **Params:** `date` (string, **required**) — Date in YYYYMMDD format; `timezone` (string, optional) — IANA timezone; defaults to UTC

### `fotmob_search`

- **HTTP:** `GET /fotmob/search`
- **What:** Search FotMob entities. Returns public search suggestions for FotMob leagues, teams, players, and matches. term must contain 1 to 50 characters. Suggestions preserve the upstream JSON shape.
- **Params:** `term` (string, **required**) — Search phrase, 1 to 50 characters

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

## Flashscore (3)

### `flashscore_match_tv`

- **HTTP:** `GET /flashscore/match-tv`
- **What:** Flashscore match TV and streaming broadcasters. Returns the TV channels and streaming services listed for a match in one viewer market, with provider ids, names and website links. Listings are country specific, so pick geo from flashscore-odds-geos; an empty list means no broadcaster is listed for that market. Bookmaker promotions are not included.
- **Params:** `geo` (string, optional) — Viewer market country code from flashscore-odds-geos; defaults to GB; `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_odds_geos`

- **HTTP:** `GET /flashscore/odds-geos`
- **What:** Flashscore odds markets, subdivisions and odds enums. Lists every country code accepted by flashscore-match-odds and flashscore-match-tv (with whether bookmakers were found for it when verified), the US states and Canadian provinces that change the bookmaker list, and every betting type, scope and handicap type that can appear in odds responses.
- **Params:** _none_

### `flashscore_search`

- **HTTP:** `GET /flashscore/search`
- **What:** Flashscore search. Searches the same public entity index used by Flashscore's search box. Results can include teams, players, and tournament templates across supported sports.
- **Params:** `q` (string, **required**) — Search phrase (2 to 80 characters)
