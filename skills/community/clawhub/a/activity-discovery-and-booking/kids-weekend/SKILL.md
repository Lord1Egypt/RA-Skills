---
name: kids-weekend
description: >-
  Find family-friendly things to do with kids — interactive museums, parks,
  workshops, shows, and rainy-day activities — via natural-language search.
  Use when the user wants ideas for children or the whole family ("things to
  do with the kids this weekend", "indoor activities for a toddler", "family
  fun Saturday"). Powered by Outgoing (https://outgoing.world), which
  connects AI agents to a huge catalog of quality, engaging activities
  worldwide, including arts, concerts, restaurants, popups, workshops, and
  more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🧸"
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

# Kids & family — powered by Outgoing

Find things to do with children and the whole family.

## When to use

The user is planning for kids or a family outing. Triggers: "with the kids",
"family-friendly", "toddler", "rainy-day activities", "something for a
4-year-old", "school holiday plans".

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

Lead with the family frame and capture the kids' ages, indoor vs. outdoor,
weather, and timing — these dramatically change good picks.

- "interactive, hands-on activities for a curious 4- and 7-year-old Saturday morning"
- "indoor rainy-day ideas for toddlers — somewhere they can run around"
- "something artistic to do with my kids this weekend"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=family-friendly things to do with two young kids this Saturday" \
  --data-urlencode "city=san_francisco"
```

- `city` — an optional hint to ground the search if the query doesn't say
  where. Prefer putting the location right in the prompt, as specific as
  needed (e.g. "jazz tonight in Pigalle") — the query overrides `city`.
- Returns `{ message, activities[] }`; each activity has `activity_id`, `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a landmark or neighborhood.

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price
`label` when `is_bookable`. Render `picture_url` where supported. Only
report what the API returns — never invent venues, prices, or availability.

## Booking (optional)

To buy tickets, use the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific occasions — see the **activity-discovery-and-booking** skill for the full list.
