---
name: work-meetup
description: >-
  Find professional venues — restaurants for client dinners, quiet cafés for
  meetings, bars for after-work drinks, and spaces for team offsites — via
  natural-language search. Use when the user is planning something
  work-related ("restaurant for a client dinner", "quiet café to meet a
  colleague", "venue for a small team offsite", "networking spots"). Powered
  by Outgoing (https://outgoing.world), which connects AI agents to a huge
  catalog of quality, engaging activities worldwide, including arts,
  concerts, restaurants, popups, workshops, and more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "💼"
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

# Work & networking — powered by Outgoing

Find venues that work for business: client dinners, meetings, after-work drinks,
and team offsites.

## When to use

The user is planning something professional. Triggers: "client dinner",
"business lunch", "meeting spot", "after-work drinks", "team offsite",
"networking", "somewhere quiet to talk shop".

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

Lead with the professional context, then add the must-haves: noise level
(quiet enough to talk), group size, formality, and budget/expense-friendliness.

- "quiet, upscale restaurant for a 4-person client dinner — easy to talk"
- "café with good wifi and tables for an informal 1:1 meeting"
- "lively but not loud bar for after-work drinks with the team"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=upscale but quiet restaurant for a client dinner downtown" \
  --data-urlencode "city=new_york"
```

- `city` — an optional hint to ground the search if the query doesn't say
  where. Prefer putting the location right in the prompt, as specific as
  needed (e.g. "jazz tonight in Pigalle") — the query overrides `city`.
- Returns `{ message, activities[] }`; each activity has `activity_id`, `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search near the office or a landmark.

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price
`label` when `is_bookable`. Render `picture_url` where supported. Only
report what the API returns — never invent venues, prices, or availability.

## Booking (optional)

To buy tickets, use the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific occasions — see the **activity-discovery-and-booking** skill for the full list.
