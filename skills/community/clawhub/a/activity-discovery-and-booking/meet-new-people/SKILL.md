---
name: meet-new-people
description: >-
  Find social events to meet new people — mixers, meetups, classes,
  workshops, community events, and solo-friendly outings — via
  natural-language search. Use when the user is new in town or wants to
  expand their circle ("ways to meet people", "social events this week",
  "beginner classes to meet others", "I'm new here, what should I do").
  Powered by Outgoing (https://outgoing.world), which connects AI agents to a
  huge catalog of quality, engaging activities worldwide, including arts,
  concerts, restaurants, popups, workshops, and more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🫂"
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

# Meet new people — powered by Outgoing

Find social, welcoming events where it's easy to meet others.

## When to use

The user wants to meet people or is new in town. Triggers: "meet new people",
"make friends", "social events", "mixers", "meetups", "classes/workshops to
meet others", "new in the city", "solo but social".

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

Lead with the social-connection frame and favor group, interactive formats
(classes, workshops, mixers, clubs) over passive ones. Note any interests to
match like-minded people.

- "welcoming social events this week where it's easy to talk to strangers"
- "beginner-friendly group classes or workshops to meet people"
- "community meetups around hiking, board games, or language exchange"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=social events and beginner classes to meet new people this week" \
  --data-urlencode "city=berlin"
```

- `city` — an optional hint to ground the search if the query doesn't say
  where. Prefer putting the location right in the prompt, as specific as
  needed (e.g. "jazz tonight in Pigalle") — the query overrides `city`.
- Returns `{ message, activities[] }`; each activity has `activity_id`, `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a neighborhood.

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price
`label` when `is_bookable`. Render `picture_url` where supported. Only
report what the API returns — never invent venues, prices, or availability.

## Booking (optional)

To buy tickets, use the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific occasions — see the **activity-discovery-and-booking** skill for the full list.
