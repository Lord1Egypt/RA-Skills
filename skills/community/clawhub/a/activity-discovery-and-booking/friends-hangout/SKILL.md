---
name: friends-hangout
description: >-
  Find casual group outings — fun bars, breweries, games and activities,
  lively happy hours, and group-friendly spots — via natural-language search.
  Use when the user is going out with friends ("fun bars for a group Saturday
  night", "where to hang with friends", "something fun for 6 of us", "good
  happy hour"). Powered by Outgoing (https://outgoing.world), which connects
  AI agents to a huge catalog of quality, engaging activities worldwide,
  including arts, concerts, restaurants, popups, workshops, and more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🍻"
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

# Friends hangout — powered by Outgoing

Find fun, casual spots for a group of friends.

## When to use

The user is going out with friends. Triggers: "with friends", "group hangout",
"fun bars", "happy hour", "something for a group of 6", "lively night out",
"games and drinks".

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

Lead with the group frame and capture size, vibe (chill vs. rowdy), and whether
they want an activity (games, bowling, karaoke) or just drinks/food.

- "lively bars with space for a group of 8 to stand and talk"
- "fun activity for friends — think arcade, bowling, or karaoke"
- "laid-back brewery or beer garden for a Sunday afternoon hang"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=fun, lively bars for a group of six on Saturday night" \
  --data-urlencode "city=chicago"
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
