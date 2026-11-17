---
name: football-viewing-guide
description: Build a dated, country-specific football broadcast guide using FotMob schedules or Flashscore match-level TV listings. Use for listed channels and market comparisons without promising streaming access.
---

# Football viewing guide

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound pages and calls by the requested scope and credit budget.
Preserve source IDs, URLs, retrieval times, and source dates where supplied.

Find the publicly listed football broadcasts for the requested market and dates.
Start with the viewer's country/market, IANA timezone, preferred teams or
competitions, and date window. A country-specific channel listing does not
establish that the user can watch it with their subscriptions or device.

## Discover the market and schedule

1. Call `fotmob_tv_guide_countries` for valid market codes. These are provider
   codes, not an ISO-code transformation: some values differ from a country's
   expected abbreviation. Use the returned code instead of inventing one.
2. Request `fotmob_tv_guide` for that country and explicit timezone. It exposes
   the current seven-day window, without an arbitrary past/future date argument.
   If requested dates lie outside the returned window, report them uncovered;
   do not shift dates or claim a longer schedule exists.
3. Channels discovery lists channels attached to that same market's current
   seven-day window; it is not a complete national channel or rights-holder
   directory. Request it only for channel matching or a channel-specific guide.
4. Filter the actual schedule locally by date, team, competition, or listed channel.
   Preserve match IDs, UTC time, returned local times, competition, teams, and
   all returned channel names. Channels are not interchangeable across markets.
   Verify a same-named team/fixture via search, matches, or match detail if needed.
5. For a specific Flashscore fixture, resolve the exact match with
   `/flashscore/search` or a previously verified Flashscore ID. Discover the
   viewer market with `/flashscore/odds-geos`, then call
   `/flashscore/match-tv` with that event ID and geo. Flashscore provides a
   match-level snapshot, not the FotMob seven-day schedule; keep the provider
   and its market code explicit.

```sh
scripts/crawlora.sh /fotmob/tv-guide-countries
# Select a discovered market code and the viewer's timezone:
scripts/crawlora.sh /fotmob/tv-guide country=gb timezone=Europe/London
scripts/crawlora.sh /fotmob/tv-guide-channels country=gb
scripts/crawlora.sh /flashscore/search q="Arsenal"
scripts/crawlora.sh /flashscore/odds-geos
scripts/crawlora.sh /flashscore/match-tv id=example-match-id geo=GB
```

## Deliver a practical schedule with boundaries

Return one row per fixture with local date/time and timezone, teams, competition,
market, listed channels, match/source link when returned, and collection time.
Retain UTC time for joins and daylight-saving transitions; do not reuse a fixed
UTC offset across the requested window. Deduplicate by match ID plus market,
preserving multiple listed channels rather than counting them as separate games.
If guide time and refreshed match time disagree, show the discrepancy and timestamp
instead of silently reconciling it. Broadcast listings and fixtures may change.

Separate a supported market with an empty current schedule from a failed fetch.
Missing channel listings do not prove a match is untelevised elsewhere. Returned
public affiliate metadata is not guaranteed free streaming, a playable video,
subscription inclusion, device compatibility, or permission to bypass geographic
restrictions. Link an actually returned public page when useful; never fabricate
stream URLs. Do not sign up, purchase subscriptions, or schedule notifications
unless the user requests those actions.
