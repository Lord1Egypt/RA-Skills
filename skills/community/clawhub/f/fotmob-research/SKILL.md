---
name: fotmob-research
description: Research football fixtures, match reports, player form, transfers, standings, and broadcast listings through Crawlora FotMob tools. Use for a football match brief, team or player comparison, league leaders, transfer coverage, or where a match is shown.
---

# FotMob football research

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Build a source-attributed football brief from FotMob's public match, team,
player, league, transfer, and broadcast surfaces.

## Discover identities before retrieving detail

- Resolve teams and players with `fotmob_search`; use `fotmob_leagues` and
  `fotmob_seasons` for league/season choices. Keep numeric FotMob IDs separate
  from another provider's IDs. Use `fotmob_matches` for a date in `YYYYMMDD`
  and an explicit IANA timezone, then select returned match IDs.
- Fetch match detail and, when relevant, player-match stats and match media.
  Record scheduled time, status, competition, and observation time before
  comparing scores. A future fixture has no completed-match statistics.
- Get team/player details before following pagination. Team fixture cursors
  come from the previous-fixture URL; player `before` comes from the upstream
  previous URL. Copy these opaque values unchanged rather than synthesizing them.
- Player season stats require that player's `statSeasons` entryId, not a league
  season label. League leaders use `fotmob_stats_categories` for the selected
  league, season, and subject (`players` or `teams`) before `fotmob_stats`.
- Discover FIFA ranking periods for the requested gender before requesting a
  ranking. Discover TV-guide countries and channels before using a market code;
  guide availability describes a market listing, not access to a video stream.

```sh
scripts/crawlora.sh /fotmob/search term="Arsenal"
scripts/crawlora.sh /fotmob/leagues
scripts/crawlora.sh /fotmob/matches date=20261005 timezone=Europe/London
# Use returned IDs, for example:
# scripts/crawlora.sh /fotmob/match id="$MATCH_ID"
# scripts/crawlora.sh /fotmob/stats-categories league_id="$LEAGUE_ID" type=players
scripts/crawlora.sh /fotmob/tv-guide-countries
```

## Interpret and deliver

Compare like competitions, seasons, minutes, and positions; show sample size
and per-match versus total denominators. FotMob ratings and market values are
provider estimates. Transfers distinguish completed moves, extensions, and
rumours; a likely rumour is not a confirmed transfer. Separate editorial news
from match statistics. Return an evidence table and a concise match/team/player
brief with source links and timestamps. Missing lineups, events, or statistics
remain unknown; no result does not establish that a fixture or player is absent.
