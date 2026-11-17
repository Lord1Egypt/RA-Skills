---
name: charlotteonthecheap-mcp
description: Find free and cheap things to do in Charlotte, NC — daily event listings with times, prices and venues, plus searchable deals, festivals, kids activities and local guides from Charlotte On The Cheap. Use when the user asks what's happening in Charlotte, wants free or cheap local events on a date or weekend, or asks about Charlotte-area deals, festivals, or family activities.
---

# Charlotte On The Cheap

Reads [Charlotte On The Cheap](https://www.charlotteonthecheap.com), a local
guide to free and cheap things to do in the Charlotte, NC area. Everything is
read-only and needs no credentials.

## Picking the right tool

- **What's on for a date** → `cotc_list_events` with an ISO `date`
  (defaults to today). Each listing has its time, price and venue. Add
  `free_only: true` for no-cost listings only.
- **Scan or compare a whole month** → `cotc_events_month_overview`.
- **Find articles by topic, place or text** → `cotc_search_posts`
  (`query`, `category`, `location`, `after`/`before`).
- **Read one article in full** → `cotc_get_post` with an id, slug, or URL.
- **Discover filter ids** → `cotc_list_categories`, `cotc_list_locations`.

## Typical flow

For "what's free this weekend?", call `cotc_list_events` once per date with
`free_only: true` — the events calendar is per-day, so a weekend is two calls
(three over a long weekend). Give the user the title, time and venue, and offer
`cotc_get_post` on anything they want details for.

For a topic ("free museum days", "kids stuff in Lake Norman"), search instead:
resolve the category or location id first if you need to filter, then
`cotc_search_posts`.

## Two behaviours to get right

**Month overviews are previews.** The site's calendar renders at most four
listings per day. In `cotc_events_month_overview`, each day's `events` is a
*preview* while `total` is the day's real count — for August 2026 that's 124
previewed against 510 actual. Use `total` when telling the user how much is on,
and call `cotc_list_events` for a date to get that day's full schedule. Never
present the preview as the complete list.

**Expired deals are hidden by default.** Retired offers are recategorised into
an `expired` category and excluded from searches, so results reflect things
still available. Only pass `include_expired: true` when the user is explicitly
researching past deals or history — and say so when those results are shown,
since the offers no longer stand.

## Dates

Pass dates as ISO `YYYY-MM-DD` (and months as `YYYY-MM`). The tools convert to
whatever the site expects and reject a malformed date rather than guessing.
Resolve relative dates ("this Saturday") against today before calling.
