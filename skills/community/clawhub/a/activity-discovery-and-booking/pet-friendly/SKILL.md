---
name: pet-friendly
description: >-
  Find dog- and pet-friendly outings — patios, cafés, parks, breweries, and
  trails that welcome pets — via natural-language search. Use when the user
  wants to bring their pet along ("dog-friendly cafés", "where can I bring my
  dog", "pet-friendly patios", "places that allow dogs this weekend").
  Powered by Outgoing (https://outgoing.world), which connects AI agents to a
  huge catalog of quality, engaging activities worldwide, including arts,
  concerts, restaurants, popups, workshops, and more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🐾"
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

# Pet-friendly outings — powered by Outgoing

Find places that welcome dogs and other pets.

## When to use

The user wants to bring a pet. Triggers: "dog-friendly", "pet-friendly", "can I
bring my dog", "patio that allows dogs", "dog park", "somewhere with my pet".

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

Always state the pet need explicitly in the `prompt` so results actually allow
pets. Add the type of outing (café, patio, park, trail) and the pet's size/needs
when relevant.

- "dog-friendly patios for brunch where a large dog is welcome"
- "off-leash dog parks and pet-friendly trails nearby"
- "breweries or cafés that allow dogs inside"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=dog-friendly cafés and patios where I can bring my dog this weekend" \
  --data-urlencode "city=london"
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
report what the API returns — never invent venues, prices, availability, or
pet policies.

## Booking (optional)

To buy tickets, use the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific occasions — see the **activity-discovery-and-booking** skill for the full list.
