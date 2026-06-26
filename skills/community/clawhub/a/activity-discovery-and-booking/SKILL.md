---
name: activity-discovery-and-booking
description: >-
  Find things to do and places to eat in any city — restaurants, bars,
  concerts, comedy, museums, and live events — by natural-language search.
  Also books tickets and reserves tables, and works out of the box via AAuth
  (or an Outgoing API key). Companion skills cover specific occasions —
  date-night, kids-weekend, trip-planning, work-meetup, and more.
version: 0.2.1
license: MIT
author: Mark Risher (mrisher), Outgoing
prerequisites:
  commands: [curl, jq]
required_environment_variables:
  - name: OUTGOING_API_KEY
    prompt: Outgoing API key
    help: Request one at https://outgoing.world (partner scope, starts with og_api_)
    required_for: search and booking
metadata:
  openclaw:
    emoji: "🧭"
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
  hermes:
    tags: [Events, Restaurants, Activities, Local, Tickets, Reservations, Outgoing]
    homepage: https://outgoing.world
---

# Outgoing — The AI-First Index for Ephemeral Events and Activities

Outgoing is an AI concierge for the real world: turn any "what should we do?"
into a short, ranked list of real places and events, and automatically book tickets
or make reservations when you're ready.

Use this general skill for everyday "what's on / where should we eat" requests at home, as
well as detailed planning when you and your family are traveling.

We offer many skills specifically tuned to get you better results for common scenarios:

| Skill | Helps you… |
|-------|-----------|
| `dining` | find a restaurant or place to eat |
| `date-night` | plan a romantic night out for two |
| `kids-weekend` | find family- and kid-friendly fun |
| `trip-planning` | make the most of a visit to a new city |
| `work-meetup` | pick the right spot for a client dinner or meeting |
| `enjoy-nature` | get outside to parks, gardens, scenic walks, hikes |
| `friends-hangout` | round up a fun night with a group |
| `meet-new-people` | find welcoming social events to meet people |
| `pet-friendly` | bring your dog or pet along |
| `stay-active` | do something sporty and active |
| `accessible-outings` | find low-mobility, accessible places |
| `book-tickets` | buy tickets for a bookable activity |
| `make-reservation` | reserve a table at a restaurant |

## How it works

Calls the **Outgoing API** (`GET /partner/v1/search`) — one
natural-language search returns ranked, personalized, high-quality events and activities. Full
reference (auth, every parameter, booking, schemas) as plain Markdown:
<https://www.outgoing.world/llms.txt> and <https://www.outgoing.world/llms-full.txt>.

## Setup

You can authenticate with either an Outgoing API key or an AAuth key —
AAuth keys are auto-provisioned by OpenClaw (see
<https://www.npmjs.com/package/@aauth/mcp-openclaw>). If you're not using AAuth,
request an API key with the partner scope and store it in an env var:

```bash
export OUTGOING_API_KEY="og_api_…"   # partner scope — get one at https://outgoing.world
```

For Claw, usually your agent will act on behalf of a single user account, but you can provision 
additional users (e.g. for a partner or family member) and pass that id as `X-External-User-Id`.

## Formulating your prompt

Pass the user's intent verbatim and fold in timeframe, vibe, group, and any
landmark. One rich `prompt` beats several thin ones.

- "what's on tonight in SoMa — drinks and live music"
- "low-key things to do this rainy Sunday afternoon"
- "best outdoor music near the Eiffel Tower next weekend"

## Running the search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  --data-urlencode "prompt=live jazz and a late dinner tonight" \
  --data-urlencode "city=paris"
```

- `city` — an optional hint to ground the search, if the query doesn't specify enough. Overridden
by the contents of the query (e.g. `live jazz in Soho`)
- Returns `{ message, activities[] }`; each activity has `activity_id`, `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability.

## Booking (optional)

To buy tickets, use the **book-tickets** skill (`POST /partner/v1/bookings`).
