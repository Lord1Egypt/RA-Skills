---
name: trip-planning
description: >-
  Plan what to do on a trip — must-see sights, local gems, neighborhoods to
  explore, and half-day itineraries for visitors — via natural-language
  search. Use when the user is visiting a city or planning a trip ("what to
  do on my first visit to Paris", "things to see this weekend as a tourist",
  "plan my afternoon near the Eiffel Tower"). Powered by Outgoing
  (https://outgoing.world), which connects AI agents to a huge catalog of
  quality, engaging activities worldwide, including arts, concerts,
  restaurants, popups, workshops, and more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🧳"
    homepage: https://www.outgoing.world/developers
    primaryEnv: OUTGOING_API_KEY
    requires:
      env:
        - OUTGOING_API_KEY
      anyBins:
        - curl
    envVars:
      - name: OUTGOING_API_KEY
        required: true
        description: >-
          Outgoing API key with the partner scope (og_api_…). Request one at https://outgoing.world.
---

# Trip planning — powered by Outgoing

Help a visitor make the most of a city.

## When to use

The user is a tourist or trip-planner: a first visit, a few days in town, or
building an itinerary. Triggers: "visiting", "in town for the weekend", "first
time in", "what should I see", "itinerary", "things to do near my hotel".

## How it works

Calls the **Outgoing API** (`GET /partner/v1/search`) — one
natural-language search returns a ranked list of real venues/events. The same
API powers every Outgoing skill; full reference (auth, every parameter, booking,
schemas) as plain Markdown: <https://www.outgoing.world/llms.txt> and
<https://www.outgoing.world/llms-full.txt>.

## Setup

```bash
export OUTGOING_API_KEY="og_api_…"   # partner scope — get one at https://outgoing.world
```

Authenticate with your API key (or an AAuth token). By default, calls act as
the user bound to your key — no provisioning needed. To act for a specific
user (e.g. a partner or family member), provision them once (`POST
/partner/v1/users`) and pass their id as `X-External-User-Id` (details in
llms.txt).

## Formulating your prompt

Capture trip length, interests, and pace; mix iconic sights with local gems.
Anchor on where they're staying when known (pass `lat`/`lng`).

- "a half-day of must-see sights plus one neighborhood worth wandering"
- "local, non-touristy food and culture near my hotel in Shibuya"
- "what to do with one free evening — something memorable and walkable"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=must-see things to do for a first visit, plus a few local gems" \
  --data-urlencode "city=tokyo"
```

- `city` — an optional hint to ground the search if the query doesn't say
  where. Prefer putting the location right in the prompt, as specific as
  needed (e.g. "jazz tonight in Pigalle") — the query overrides `city`.
- Returns `{ message, activities[] }`; each activity has `activity_id`, `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Use `lat`/`lng` to anchor the search near the traveler's hotel or a landmark.

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price
`label` when `is_bookable`. Render `picture_url` where supported. Only
report what the API returns — never invent venues, prices, or availability.

## Booking (optional)

To buy tickets, use the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific occasions — see the **activity-discovery-and-booking** skill for the full list.
