# cricket-player-team-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**10 endpoints across 1 platform group(s).**

## Cricinfo (10)

### `cricinfo_match`

- **HTTP:** `GET /cricinfo/match`
- **What:** Get a Cricinfo match scorecard. Returns a public Cricinfo match scorecard with match state, team scores, and available innings totals and batter/bowler lines. Upcoming matches return an empty innings list. `url` must be a canonical `https://www.cricinfo.com/series/.../(full-scorecard|live-cricket-score)` URL; live-score URLs are normalized to the paired scorecard.
- **Params:** `url` (string, **required**) — Canonical Cricinfo full-scorecard or live-cricket-score URL

### `cricinfo_rankings`

- **HTTP:** `GET /cricinfo/rankings`
- **What:** Get ICC rankings from Cricinfo. Returns ICC rankings (team or player) from a Cricinfo rankings page, given as the required `url`, which must be a canonical `https://www.cricinfo.com/rankings/...` address. Each entry has its rank, name, country, rating, points, matches and format, plus a team or player id.
- **Params:** `url` (string, **required**) — Canonical Cricinfo rankings URL

### `cricinfo_records`

- **HTTP:** `GET /cricinfo/records`
- **What:** Get a Cricinfo record table. Returns a bounded table from a Cricinfo records page. `record` is a relative Statsguru record path such as `batting/most_runs_career.html`. `class` must be one of `1`, `2`, `3`, `4`, `5`, `6`, `8`, `9`, `10`, `11`, `12`, `20`, `21`, `22`, or `23`.
- **Params:** `class` (integer, **required**) — Record match-class. Allowed values: 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 20, 21, 22, 23; `current` (string, optional) — Record currentness selector; `id` (string, optional) — Numeric record subject identifier; `record` (string, **required**) — Relative Statsguru record path; `type` (string, optional) — Record subject type

### `cricinfo_records_index`

- **HTTP:** `GET /cricinfo/records/index`
- **What:** List Cricinfo records catalog. Returns the public Cricinfo records catalog, including match classes, record categories, selectable teams or entities, and example suggestions. Use the existing records endpoint to retrieve a specific table.
- **Params:** _none_

### `cricinfo_series`

- **HTTP:** `GET /cricinfo/series`
- **What:** Get a Cricinfo series schedule and standings. Returns a series's match schedule and standings from its dedicated page. `series_id` must be the slug-and-ID portion of a canonical Cricinfo series URL, such as `indian-premier-league-2024-1410320`.
- **Params:** `series_id` (string, **required**) — Slug-and-ID portion of a canonical series URL

### `cricinfo_squads`

- **HTTP:** `GET /cricinfo/squads`
- **What:** Get a Cricinfo team squad. Returns recent public squad announcements and player rosters from a Cricinfo team profile, including player roles and withdrawal or overseas markers when published.
- **Params:** `url` (string, **required**) — Canonical Cricinfo team profile URL

### `cricinfo_stats`

- **HTTP:** `GET /cricinfo/stats`
- **What:** Query Cricinfo Statsguru. Returns a bounded Statsguru table. `class` must be one of `1`, `2`, `3`, `4`, `5`, `6`, `8`, `9`, `10`, `11`, `12`, `20`, `21`, `22`, or `23`; `type` must be one of `batting`, `bowling`, `fielding`, `allround`, `fow`, `team`, `official`, or `aggregate`; `view` may be `innings`, `match`, `series`, `ground`, `host`, `opposition`, `year`, or `season`.
- **Params:** `class` (integer, **required**) — Statsguru match-class. Allowed values: 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 20, 21, 22, 23; `ground` (string, optional) — Numeric ground identifier; `host` (string, optional) — Numeric host-country identifier; `limit` (integer, optional) — Maximum rows returned, from 1 to 100; `opposition` (string, optional) — Numeric opposition team identifier; `orderby` (string, optional) — Statsguru sort column; `orderby_desc` (boolean, optional) — Sort descending when true; `player` (string, optional) — Numeric Cricinfo player identifier; `season` (string, optional) — Season formatted as YYYY or YYYY/YY; `span_max` (string, optional) — Statsguru ending date; `span_min` (string, optional) — Statsguru starting date; `team` (string, optional) — Numeric Cricinfo team identifier; `type` (string, **required**) — Statsguru statistic family; `view` (string, optional) — Statsguru table view

### `cricinfo_team`

- **HTTP:** `GET /cricinfo/team`
- **What:** Get a Cricinfo team profile. Returns public team identity, profile text, recent fixtures and results, and the rolling batting and bowling leaders shown on a Cricinfo team page.
- **Params:** `url` (string, **required**) — Canonical Cricinfo team profile URL

### `cricinfo_team_schedule`

- **HTTP:** `GET /cricinfo/team/schedule`
- **What:** Get a Cricinfo team match schedule. Returns a cricket team's recent fixtures and results from its Cricinfo team page, given as the required `url`, which must be a canonical `https://www.cricinfo.com/team/...` address. The response has the team's id, name and slug, and matches with series, format, state, status text, team scores and scorecard URL.
- **Params:** `url` (string, **required**) — Canonical Cricinfo team URL

### `cricinfo_teams`

- **HTTP:** `GET /cricinfo/teams`
- **What:** List Cricinfo teams. Returns Cricinfo's team directory with no parameters, organised into titled groups such as popular international teams. Each team has its id, name, slug, abbreviation, country, logo URL and primary colour where Cricinfo gives them, and whether it is a national side.
- **Params:** _none_
