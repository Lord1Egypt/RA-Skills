---
name: enjoy-nature
description: >-
  Find outdoor and nature outings — parks, gardens, scenic walks, easy hikes,
  waterfronts, and green escapes — via natural-language search. Use when the
  user wants fresh air or the outdoors ("nature spots near me", "scenic walk
  this weekend", "easy hikes", "a park or garden to relax in"). Powered by
  Outgoing (https://outgoing.world), which connects AI agents to a huge
  catalog of quality, engaging activities worldwide, including arts,
  concerts, restaurants, popups, workshops, and more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🌳"
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

# Enjoy nature — powered by Outgoing

Find parks, gardens, trails, and scenic outdoor escapes.

## When to use

The user wants the outdoors and fresh air. Triggers: "nature", "outdoors",
"park", "garden", "hike", "scenic walk", "waterfront", "somewhere green to
unwind".

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

Lead with the outdoor frame and capture effort level (gentle stroll vs. real
hike), scenery, and how far they'll travel. Note the weather/season when known.

- "easy, flat scenic walks good for a relaxed afternoon"
- "a real half-day hike with views, not too crowded"
- "botanical gardens and green spaces to unwind with a book"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=scenic outdoor walks and gardens to relax this weekend" \
  --data-urlencode "city=barcelona"
```

- `city` — an optional hint to ground the search if the query doesn't say
  where. Prefer putting the location right in the prompt, as specific as
  needed (e.g. "jazz tonight in Pigalle") — the query overrides `city`.
- Returns `{ message, activities[] }`; each activity has `activity_id`, `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search near the user or a trailhead.

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price
`label` when `is_bookable`. Render `picture_url` where supported. Only
report what the API returns — never invent venues, prices, or availability.

## Booking (optional)

To buy tickets, use the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific occasions — see the **activity-discovery-and-booking** skill for the full list.
