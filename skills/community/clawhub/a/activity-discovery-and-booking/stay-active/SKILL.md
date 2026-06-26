---
name: stay-active
description: >-
  Find active and sporty things to do — fitness classes, climbing, cycling,
  watersports, drop-in sports, and active outdoor outings — via
  natural-language search. Use when the user wants to move and stay active
  ("active things to do this weekend", "drop-in fitness class", "climbing or
  cycling", "something sporty"). Powered by Outgoing
  (https://outgoing.world), which connects AI agents to a huge catalog of
  quality, engaging activities worldwide, including arts, concerts,
  restaurants, popups, workshops, and more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🏃"
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

# Stay active — powered by Outgoing

Find sporty, energetic things to do.

## When to use

The user wants physical activity. Triggers: "active", "sporty", "fitness
class", "climbing", "cycling", "yoga", "watersports", "drop-in sports",
"something to get moving".

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

Lead with the active frame and capture the sport/activity type, intensity, skill
level, and whether they want drop-in (no commitment) vs. a course.

- "drop-in fitness or HIIT class I can join this evening, no membership"
- "beginner-friendly bouldering or rock climbing"
- "kayaking, paddleboarding, or cycling routes for the weekend"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=active things to do this weekend — climbing, cycling, or a drop-in class" \
  --data-urlencode "city=sydney"
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
