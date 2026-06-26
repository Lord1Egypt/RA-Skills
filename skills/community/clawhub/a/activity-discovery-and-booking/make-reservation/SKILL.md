---
name: make-reservation
description: >-
  Reserve a table at a restaurant through Outgoing. Use after discovering a
  restaurant (one with is_bookable true) when the user wants to book a table
  or make a dining reservation ("book us a table for 2 Friday at 8", "reserve
  dinner Saturday night", "get a reservation at that place"). Reservations are
  async and resolve via webhook. Powered by Outgoing (https://outgoing.world),
  which connects AI agents to a huge catalog of quality, engaging activities
  worldwide, including arts, concerts, restaurants, popups, workshops, and
  more.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🍽️"
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

# Make a reservation — powered by Outgoing

Reserve a table at a restaurant. Reservations are **asynchronous**: you `POST` a
request, get a `202 Accepted` with a `booking_id`, and the outcome (confirmed /
failed) arrives at your **webhook** — there is no polling endpoint.

This is the **second step**. Find the restaurant first with one of the Outgoing
discovery skills (date-night, work-meetup, … or the general
**activity-discovery-and-booking**) — you need its `activity_id` and the exact seating
option, date, and time from `ticket_price`. Only restaurants with
**`is_bookable: true`** can be reserved.

Reservations and ticket purchases share the same endpoint
(`POST /partner/v1/bookings`); for a table, each `tickets[]` row is a seating —
`num_tickets` is the party size and `session_date`/`session_time` is the slot.
Full reference (every field, schemas, `GET /partner/v1/orders`) as plain
Markdown: <https://www.outgoing.world/llms.txt> and
<https://www.outgoing.world/llms-full.txt>.

## Prerequisites

```bash
export OUTGOING_API_KEY="og_api_…"   # partner scope — get one at https://outgoing.world
```

- `Authorization: Bearer $OUTGOING_API_KEY` on every call (or an AAuth token). By
  default the reservation is made for the user bound to your key; pass
  `X-External-User-Id: <user>` only to act for a specific provisioned user.
- A **webhook URL** you control (HTTPS in production) to receive the result.
- A **payment token** pre-authorizing any deposit or no-show hold. For testing
  use `DRYRUN_SUCCESS` or `DRYRUN_FAIL` — no card is charged. Many restaurants
  take no deposit; confirm from `ticket_price`.

> **Test first.** Always validate the flow with `DRYRUN_SUCCESS`/`DRYRUN_FAIL`
> before using a real `payment_token` — a real token authorizes a real charge.

## Create a reservation — `POST /partner/v1/bookings`

```bash
curl -sS -X POST https://api.outgoing.world/partner/v1/bookings \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "activity_id": "550e8400-e29b-41d4-a716-446655440000",
    "tickets": [
      { "ticket_type_name": "Dinner reservation", "num_tickets": 2,
        "session_date": "2026-04-25", "session_time": "20:00" }
    ],
    "authorization_amount_cents": 0,
    "idempotency_key": "01929f3b-7c2a-7000-8d3f-1b2c3d4e5f60",
    "webhook_url": "https://partner.example.com/webhooks/outgoing-booking",
    "payment_token": "DRYRUN_SUCCESS"
  }'
```

| Field | Required | Notes |
|-------|----------|-------|
| `activity_id` | yes | The restaurant, from discovery; must be `is_bookable: true`. |
| `tickets[]` | yes (1 row) | `ticket_type_name` (exact, from `ticket_price.sessions[].tickets[].name`), `num_tickets` = party size, and `session_date`/`session_time` = the reservation slot. |
| `authorization_amount_cents` | yes | Pre-authorized deposit/hold in USD cents; treated as a max ceiling. Use `0` when the restaurant takes no deposit. |
| `idempotency_key` | yes | Unique per attempt; replaying returns the original `booking_id` (no duplicate). |
| `webhook_url` | yes | HTTPS in prod; receives the result payload. |
| `payment_token` | yes | Real token, or `DRYRUN_SUCCESS` / `DRYRUN_FAIL`. |
| `external_user_id` | no | Reserve for a specific provisioned user instead of the default user bound to your key. |

Returns `202 { booking_id, idempotency_key, status: "accepted" }` — processing
continues in the background.

## Webhook result

Outgoing `POST`s your `webhook_url` when the reservation resolves (retried up to
3×). `status` is one of `confirmed`, `failed`, `cancelled`, `pending`,
`user_input_required`, `deliverable_ready`. On `confirmed` you also get
`purchase_amount_cents`, `booking_fee_cents`, `total_charged_cents`, and
`ticket_details` (`confirmation_code`, `download_urls`, `notes`). On `failed`,
`error_message`. You can also list past reservations via `GET /partner/v1/orders`.

## Workflow

1. Get the restaurant (discovery skill). Confirm `is_bookable: true`; read
   `ticket_price` (seating options, available dates/times, any deposit).
2. **Confirm the party size, date, time, and any deposit with the user before
   submitting** — a real `payment_token` authorizes a real charge.
3. Generate a fresh `idempotency_key` (UUID) per intended reservation; reuse the
   same key only when retrying the *same* reservation.
4. POST the reservation (DRYRUN first when validating).
5. Tell the user it's submitted; resolve via webhook (or `GET /orders`). On
   `confirmed`, share the `confirmation_code` and any `notes`. On `failed`,
   relay `error_message` and offer a retry with a new key.

## Errors

`400` validation (seating/slot mismatch — message lists valid options; fully
booked; non-HTTPS webhook). `401` bad key/scope. `402` invalid/expired
`payment_token`. `404` user not provisioned or restaurant not found. `429` rate
limit. Relay `{ "error": "…" }` messages; never fabricate a result.

> Looking for a restaurant to reserve? Find one first with the
> **activity-discovery-and-booking** skill (or **date-night** / **work-meetup**).
