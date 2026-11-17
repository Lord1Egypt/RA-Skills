---
name: cricket-player-team-comparison
description: Compare cricket player or team records through Crawlora Cricinfo Statsguru, records, matches, and discovery. Use for format-specific batting/bowling/fielding comparisons with class, innings, dates, opposition, overs notation, and source table definitions preserved.
---

# Cricket player and team comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare a defined player/team cohort under an explicit match format, season or
date window, statistic family, and role. Separate international/domestic and
men's/women's or age-group contexts rather than treating every record as comparable.

## Discover class, entity, and table scope

1. Use the records index and team/match/series sources to obtain supported match
   classes and verified numeric team/player/opposition/ground IDs. A class code
   selects a format/competition scope; do not infer it from a similar league name.
   There is no general free-text player-search parameter on Statsguru here.
2. Statsguru requires `class` and `type`. Use only the documented families
   (`batting`, `bowling`, `fielding`, `allround`, `fow`, `team`, `official`,
   `aggregate`) and view values. Retain each exact filter, season/date bounds,
   opposition/host/ground context, source URL, and observation time.
3. Source tables have variable `headers`/row fields. Interpret displayed labels
   for that table, not a fixed universal schema. Missing/dash values remain unknown.
   A player selector changes the table scope; do not assign global rows to that
   player simply because the request included an identifier.
4. A Statsguru result is bounded by `limit` (up to 100), without an exposed
   arbitrary page argument. Record table coverage. Record paths come from public
   record discovery; IDs/paths are not interchangeable with canonical match URLs.
   If rankings are used, preserve their source URL, date, format, and ranking scope.

```sh
scripts/crawlora.sh /cricinfo/records/index
scripts/crawlora.sh /cricinfo/teams
scripts/crawlora.sh /cricinfo/stats class=1 type=batting view=year limit=10
# Use returned/verified entity IDs before player/team-specific comparisons.
```

## Normalize rates without changing cricket notation

Compare runs, wickets, matches, innings, balls, not-outs, and opportunities on
matching bases. Batting average uses dismissals rather than appearances; bowling
average and economy use different numerators/denominators. Calculate rates only
when compatible raw counts and table definitions are available, retaining the
provider's own rate and rounding separately.

Overs notation is not decimal time: its final component represents balls in an
incomplete over. Verify the applicable balls-per-over rule before converting
overs into balls or computing economy; do not treat displayed `5.3` as 5.3 decimal
overs. Team innings, player batting innings, and bowling spells are different
exposures. Do not sum unlike format records, average percentages without event
weights, or compare complete-career totals with a recent selected sample.

Return an entity/class/filter ledger, comparison table with denominators and
units, selected match/context evidence, truncation and unknown fields, and a
role-specific interpretation. Rankings/records are descriptive source observations,
not forecasts, injury assessments, or betting recommendations. Strong aggregate
figures do not establish performance against unobserved opposition or conditions.
