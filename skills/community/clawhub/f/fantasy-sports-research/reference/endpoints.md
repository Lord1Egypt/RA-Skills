# fantasy-sports-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 3 platform group(s).**

## DraftKings Daily Fantasy Sports (5)

### `draftkings_dfs_glossary`

- **HTTP:** `GET /draftkings/dfs/glossary`
- **What:** DraftKings Daily Fantasy glossary. Returns the public Daily Fantasy glossary terms and definitions from DraftKings' How to Play page. It does not access the contest lobby, player pool, or account data.
- **Params:** _none_

### `draftkings_dfs_guide`

- **HTTP:** `GET /draftkings/dfs/guide`
- **What:** DraftKings Daily Fantasy guide. Returns public contest-type summaries and sport landing-page links from DraftKings' Daily Fantasy Sports guide. Use draftkings_dfs_glossary for the page's public terminology definitions. This is a read-only guide directory; it does not access contests, lineups, player pools, or accounts. Availability and age limits vary by location.
- **Params:** _none_

### `draftkings_dfs_nfl_best_ball_featured_contests`

- **HTTP:** `GET /draftkings/dfs/nfl-best-ball/featured-contests`
- **What:** DraftKings NFL Best Ball featured contests. Lists the contest cards currently shown in DraftKings' public NFL Best Ball Featured Contests section, including displayed entry-fee and top-prize amounts and maximum entries. This is the landing-page selection, not the full contest lobby or a guarantee that a contest remains open. It does not follow tournament-detail links or return promotions, entries, lineups, or account data.
- **Params:** _none_

### `draftkings_dfs_rules_and_scoring`

- **HTTP:** `GET /draftkings/dfs/rules-and-scoring`
- **What:** DraftKings DFS Rules & Scoring. Returns the public Daily Fantasy rules and scoring overview plus visible sports and contest-style rules. Each rule includes upstream game-type IDs and sanitized scoring content. Hidden records, including XFL rules, are omitted; contests, players, prizes, lineups, and account data are not returned.
- **Params:** _none_

### `draftkings_dfs_sports`

- **HTTP:** `GET /draftkings/dfs/sports`
- **What:** DraftKings Daily Fantasy sports catalog. Returns the public US-DK sport catalog with exact sport codes and DraftKings' enabled/public-contests flags. The flags describe the source catalog, not caller-specific location eligibility. This endpoint does not access contests, lineups, prizes, or account data.
- **Params:** _none_

## DraftKings Pick6 (3)

### `draftkings_pick6_rule_page`

- **HTTP:** `GET /draftkings/pick6/rules/{slug}`
- **What:** DraftKings Pick6 sport-specific rules. Returns public scoring and rule sections for one supported Pick6 sport/format page. Discover supported slugs with draftkings_pick6_rules. This endpoint does not return player picks, projections, user entries, or location tokens.
- **Params:** `slug` (string, **required**) — Sport/format slug listed by draftkings_pick6_rules

### `draftkings_pick6_rules`

- **HTTP:** `GET /draftkings/pick6/rules`
- **What:** DraftKings Pick6 rules. Returns public rule sections from the DraftKings Pick6 Rules and Scoring page plus child pages with verified detail routes. Unverified upstream links are omitted from the slug directory. It does not return player picks, projections, user entries, or location tokens.
- **Params:** _none_

### `draftkings_pick6_sports`

- **HTTP:** `GET /draftkings/pick6/sports`
- **What:** DraftKings Pick6 sport directory. Returns the dated public Help Center snapshot of Pick6 sports and contest formats, with exact sport codes and links published by the Help Center, plus the CFB/CBB jurisdiction restriction. Product-page reachability is not verified. This directory does not return picks or projections and does not imply availability in the caller's location.
- **Params:** _none_

## FanDuel (3)

### `fanduel_research_projection_slates`

- **HTTP:** `GET /fanduel/research/projection-slates`
- **What:** FanDuel Research projection slates. Lists the daily-fantasy slates (the contest pools such as `Main`, `All Day` or a single game) of a sport, which the DAILY projections need as `slate_id`. Defaults to today; pass `date` for MLB, NBA and NHL, or `week` and `season` for the NFL, to read another day (past days list their slates too; a day with no games returns an empty list). Golf also returns the current events whose `id` is the projections' `event_id`.
- **Params:** `date` (string, optional) — Day as `YYYY-MM-DD`; MLB, NBA and NHL only; cannot be combined with `week` or `season`; `season` (integer, optional) — NFL season year such as `2026`; NFL only; `sport` (string, **required**) — Sport; `week` (integer, optional) — NFL week, 1 to 30; NFL only, usually with `season`

### `fanduel_research_projection_tables`

- **HTTP:** `GET /fanduel/research/projection-tables`
- **What:** FanDuel Research projection tables. Lists the 17 fantasy projection tables of FanDuel Research (numberFire) for MLB, NBA, NFL, NHL and golf: each table's sport, projection type, the position tabs it offers (with the player positions each tab keeps), whether it takes a scope, a slate or a golf event. Use it to find the valid `type`, `position` and `scope` values for the projections route.
- **Params:** `sport` (string, optional) — Keep only this sport's tables

### `fanduel_research_projections`

- **HTTP:** `GET /fanduel/research/projections`
- **What:** FanDuel Research fantasy projections. Returns numberFire's fantasy projections for MLB, NBA, NFL, NHL and golf in the service's rank order: each row has the player, team, game, FanDuel DFS salary and value (daily projections), and the stat columns of the player kind (points, rebounds and assists for the NBA; passing, rushing and receiving for NFL skill players; kicker, defense and individual defensive player columns; skater, goalie, batter and pitcher columns; golf finish odds). `type` picks the table: `DAILY` (needs `slate_id`), `WEEKLY`, `YEARLY`, `REMAINING`, `PPR` or `SEASON_STATS`; not every sport has every type, and `position` and `scope` depend on the table, so read them from the projection-tables route. An unknown slate is refused instead of silently returning other projections. Weekly NBA and MLB tables are empty outside their weeks. A player id can appear more than once in a yearly table.
- **Params:** `date` (string, optional) — Day of the slate as `YYYY-MM-DD` when `slate_id` is not from today; MLB, NBA and NHL DAILY only; `event_id` (string, optional) — Golf event id from the projection-slates route; golf only, defaults to the only current event; `limit` (integer, optional) — Rows per page, 1 to 200; default 50; `page` (integer, optional) — Page number, from 1; default 1, at most 10000; `position` (string, optional) — Position tab of the table; default is the table's default tab. Allowed values: `batters`, `pitchers`, `c`, `1b`, `2b`, `3b`, `ss`, `of`, `sp`, `rp` (MLB); `qb`, `rb`, `wr`, `te`, `flex`, `k`, `defense`, `idp` (NFL); `all`, `pg`, `sg`, `guards`, `sf`, `pf`, `forwards`, `centers` (NBA); `skaters`, `goalies`, `forwards`, `wingers`, `centers`, `d` (NHL); `all` (golf). Which of them a table offers is listed by projection-tables; `scope` (string, optional) — `TOTAL` or `PER_GAME`; only NBA WEEKLY, YEARLY, REMAINING and SEASON_STATS take it, default `TOTAL`; other tables return `400`; `season` (integer, optional) — NFL season of the slate; NFL DAILY only; `slate_id` (string, optional) — Slate id from the projection-slates route; required for DAILY (golf defaults to its only slate); other types return `400`; `sport` (string, **required**) — Sport; `type` (string, **required**) — Projection type; `week` (integer, optional) — NFL week of the slate when `slate_id` is not from this week; NFL DAILY only
