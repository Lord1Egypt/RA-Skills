---
name: football-player-comparison
description: Compare football players using Crawlora FotMob profiles, player-specific season statistics, and bounded match samples. Use for role-aware form comparisons, statistical scouting briefs, or explaining differences with minutes, competition, season, and metric provenance preserved.
---

# Football player comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound pages and calls by the requested scope and credit budget.
Preserve source IDs, URLs, retrieval times, and source dates where supplied.

Produce a role- and period-aware statistical comparison of the selected players.
Establish the position/role, competition, season/date window, desired metrics,
and minimum playing-time criterion before selecting comparison rows.

## Resolve players and comparable observations

- Use `fotmob_search` and profile detail to verify numeric player IDs, team,
  position, and identity. Do not identify players by surname alone or reuse
  another provider's IDs. Keep current profile context separate from past teams.
- Discover each player's `statSeasons` from their profile, then pass that player's
  entryId to `fotmob_player_stats`. Player season IDs are player-specific: do not
  reuse a league ID, a year label, or another player's season entry.
- Verify competition, period, team, and supplied minutes/appearances for each row.
  Separate domestic league, cup, international, and other competitions. Keep
  goalkeeper-specific metrics apart from outfield metrics; shot/heat maps are
  provider observations rather than directly comparable totals.
- For recent form, follow player `matchFilters` league/team pairs and the upstream
  `before` cursor to collect a bounded match sample. Resolve match IDs and statuses
  before per-match player stats. Match-history appearance does not mean the player
  played 90 minutes or that a scheduled match has finished.
- Preserve provider stat keys, labels, units, and supplied rating/model context.
  Missing stats are unknown, not zero. An unavailable injury/profile field does
  not establish fitness or medical status.

```sh
scripts/crawlora.sh /fotmob/search term="Mohamed Salah"
# Select and verify the actual returned player ID first:
# scripts/crawlora.sh /fotmob/player id="$PLAYER_ID"
# scripts/crawlora.sh /fotmob/player-stats player_id="$PLAYER_ID" season_id="$PLAYER_SEASON_ID"
# scripts/crawlora.sh /fotmob/player-matches player_id="$PLAYER_ID"
```

## Normalize metrics and show uncertainty

Calculate a per-90 rate only when the numerator is a compatible count and actual
minutes for that same sample are supplied: `count / minutes × 90`. Do not divide
percentages, per-game averages, provider ratings, or already-normalized rates by
minutes again. Do not average match percentages when the correct event-weighted
denominator is missing. Show totals, rates, and minutes together and apply the
same minimum-minute criterion to each player; small samples remain visible.

Do not combine season totals with overlapping match totals. Compare recent form
under matched date/competition/role scopes; an equal number of games can span
different periods. Keep team strength, tactical role, opponent mix, and provider
model differences as limits rather than silently attributing every difference
to player ability. Market values are estimates, not offers or transfer fees.

Return an identity/scope ledger, metric comparison with formulas and denominators,
selected match evidence, role-specific strengths/uncertainties, and missing data.
An overall ranking needs the user's criteria and disclosed weights; unsupported
metrics must not silently become zero. Statistics alone do not prove future
performance, transfer suitability, or a completed scouting evaluation.
