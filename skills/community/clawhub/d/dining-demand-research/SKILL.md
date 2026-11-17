---
name: dining-demand-research
description: Research public Resy and OpenTable restaurant discovery, profiles, and time-specific availability snapshots. Use for dining shortlists or reservation-demand comparisons, not booking or ordering.
---

# Dining demand research

Research public restaurant discovery and the availability currently displayed by
Resy and OpenTable. Produce a dated snapshot and a shortlist; these surfaces
do not create, hold, modify, or cancel reservations, purchase event tickets, or
guarantee a table remains available.

## Resolve the restaurant and request context

1. Establish the requested place, party size, local dining date/time, and any
   cuisine, price, or accessibility preferences. Resolve ambiguous venues by
   provider ID first, then name plus street address/neighborhood; never mix a
   Resy `restaurant_id` with an OpenTable `restaurant_id`.
2. For Resy, discover a city with `GET /resy/locations` (`q`, `country`), then
   use returned location codes/IDs for `GET /resy/cuisines` (`location`) and
   `GET /resy/events` (`location`, optional `date`, `limit`, `offset`). Search
   venues with `GET /resy/search` (`latitude`, `longitude`, optional `term`,
   `date`, `party_size`, `size`); `date` adds current slots to the results.
3. For OpenTable, use `GET /opentable/search` with required `term`, `latitude`,
   and `longitude`, plus optional `date_time`, `party_size`, and `size`. Use a
   returned ID with `GET /opentable/restaurant` (`restaurant_id`, optional
   `date_time`, `party_size`) to refresh that venue's profile and slots.
4. Fetch provider-specific detail when it improves the decision: `GET
   /resy/restaurant` or `GET /resy/availability` (`restaurant_id`, `date`,
   optional `party_size`); `GET /opentable/restaurant/menus` or `GET
   /opentable/restaurant/reviews` (`restaurant_id`, optional `page`, `size`).
   Menu and review data support discovery; they do not prove a table is
   available.

## Time, availability, and pricing

- Resy dates are `YYYY-MM-DD`; OpenTable `date_time` is RFC3339-minute local
  format. Normalize the requested moment to the restaurant's verified local
  time zone before the call, retain the original local date/time and zone in
  the output, and do not label an offset-free local time as UTC.
- Capture `retrieved_at` immediately for every availability call, alongside
  source, provider ID, requested date/time, party size, and canonical URL when
  returned. Treat returned slots as an observed snapshot: they can change
  between calls and do not hold inventory.
- Party size defaults to 2 on availability/search/detail calls when omitted.
  Request the user's actual party size; a result for one party size cannot be
  generalized to another. Search result limits default to 10 for Resy and
  OpenTable; Resy's event list also defaults to 10, while OpenTable reviews
  default to page 1 with 20 reviews. Do not imply undocumented maximums.
- A venue price tier/band is an affordability signal, not a menu total. Use
  actual menu prices only where returned, preserve currency and scope, and do
  not infer taxes, fees, deposits, minimums, or reservation cost.

## Keep regular reservations distinct from events

Resy `GET /resy/events` lists ticketed, fixed-price/fixed-capacity dining
events, not ordinary reservation slots. For one event, call `GET /resy/event`
with the event result's `event_url_slug`, `restaurant_url_slug`, and the same
`location` (optional `party_size`) to inspect ticket packages and their live
availability. Report event availability, tier price, inclusions, and event-day
instructions separately from restaurant reservation availability. This is
read-only research, never a ticket purchase.

## Deliverable and bounds

Return a comparison with venue name, provider and provider ID, verified
address/neighborhood, cuisine, price signal, requested local date/time/zone,
party size, observed slots or explicit lack of slots, source URL, and
`retrieved_at`. State which facts are discovery/profile data versus a
time-specific availability snapshot. Compare only like-for-like party sizes
and local times; a missing slot is not proof of a sellout, closure, or lack of
demand. Keep sources separate unless venue identity is independently verified.
