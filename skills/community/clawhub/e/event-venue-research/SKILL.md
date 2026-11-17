---
name: event-venue-research
description: Build event shortlists, dated calendars, and venue comparisons through Crawlora's Ticketmaster and TicketWeb endpoints. Use for public event research with verified venue identity, timing, age restrictions, ticket fees, and availability caveats.
---

# Event and venue research

Build a dated event or venue comparison from public listings. Keep ticket
availability, venue visitor information, and private venue-booking availability
separate; an event calendar does not establish that a venue can be hired.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for
event/city/category discovery, event details, and venue lookups.

## Resolve, filter, and compare

1. Establish destination, date range, interests, party age/access requirements,
   and budget. Search `/ticketmaster/search-events` (`q`, zero-based `page`,
   `sort=date` or `relevance`) or `/ticketweb/search` (`q`, one-based `page`).
   Filter returned dates locally where an endpoint has no date-range parameter.
2. For city/category browsing, use `/ticketmaster/discover-cities` or
   `/ticketmaster/discover-categories`, then the returned `city` slug/country or
   `category_id` in their matching event feeds. Discovery destination groupings
   can include surrounding municipalities; inspect actual venue locations.
3. Retrieve `/ticketmaster/event?id=...` or `/ticketweb/event?id=...` for a
   selected event. Read the nested event object, exact status, timing, venue,
   age restrictions, and source URL. IDs are provider-specific. Deduplicate
   cross-provider events by verified performer, venue, date/time, and event type;
   preserve distinct performances, ticket offers, and VIP/parking add-ons.
4. Preserve local time and timezone. TicketWeb search times have no UTC offset;
   detail can provide an offset and venue zone. Do not append `Z` to a local time.
   Keep TBD/TBA times unknown and distinguish doors, show start, and on-sale time.
5. Resolve venue details and upcoming events with `/ticketmaster/venue`,
   `/ticketmaster/venue-events`, or `/ticketweb/venue`. Artist/team attraction
   IDs are not venue IDs. Verify street address and public accessibility/visitor
   information; missing capacity or access details are unknown, not negative findings.
6. For TicketWeb prices, compare `sections[].prices[].total` and currency, keeping
   base price, fees, tier restrictions, and sale status. Do not add fees again to
   `total` or compare one provider's base price with another's fee-inclusive total.
   Ticketmaster prices, when absent, remain unknown; do not invent a price range.
7. Recheck shortlisted events close to delivery when current availability matters.
   Preserve canceled/postponed/rescheduled status and collection time. A successful
   data response does not reserve seats or lock prices.

```sh
scripts/crawlora.sh /ticketweb/search q=comedy page=1
scripts/crawlora.sh /ticketmaster/search-events q=jazz sort=date page=0
```

## Deliverable and bounds

Return a table/calendar with event and provider IDs, canonical links, venue/address,
local start time and zone, status, applicable age/access information, dated ticket
price scope, availability, and fit rationale. Group venue comparisons separately
from individual event offers. Create calendar entries or buy tickets only if asked.

- TicketWeb `has_tickets=false` with empty sections is ambiguous: free/RSVP,
  sold out, or access-code-gated can share this state. Cross-check explicit search
  availability (`in_stock`, `sold_out`, `unknown`) without guessing a cause.
- Ticketmaster event `410` means concluded/permanently removed; `404` means unknown.
  TicketWeb invalid IDs can surface as `503`; recheck the discovered ID before retrying.
- Ticketmaster event-feed pages are 0–49; TicketWeb search pages are 1–50.
  Stop at no progress, source end, or the requested date/sample bound. Back off
  on `429`, retry transient `5xx` once, stop on `401`/`403`, and check application `code`.
