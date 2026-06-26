# LifeClaw Skill API Reference

## Base URL

```
https://api-v2.lifeclaw.agentese.ai
```

## Authentication

All endpoints require: `Authorization: Bearer $LIFECLAW_API_TOKEN`

Set `LIFECLAW_API_TOKEN` as an environment variable. See [SKILL.md](../SKILL.md#authentication) for how to create tokens.

## Endpoints

### POST /skill/search

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | string | Yes | — | Search query (max 500 chars) |
| location | string | No | "" | Location hint (e.g. "Tokyo", "Singapore") |
| language | string | No | "en" | Result language |
| limit | int | No | 5 | Results to return (1-20) |

**Response:**
```json
{
  "results": [
    {
      "name": "Sushi Dai",
      "address": "5-2-1 Tsukiji, Chuo City",
      "rating": 4.6,
      "cid": "12345678901234567",
      "maps_url": "https://www.google.com/maps?cid=12345678901234567"
    }
  ]
}
```

### POST /skill/detail

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Business name (max 200 chars) |
| cid | string | Yes | Google Maps CID from search (max 200 chars) |
| language | string | No | Result language (default "en") |

**Response:**
```json
{
  "detail": {
    "phone": "+81312345678",
    "address": "5-2-1 Tsukiji, Chuo City",
    "website": "https://example.com",
    "hours": "Mon: 05:00-14:00, Tue: 05:00-14:00",
    "rating": 4.6,
    "rating_count": 1234,
    "price_level": "$$$$",
    "type": "Sushi restaurant",
    "menu": "https://example.com/menu",
    "booking_url": "https://...",
    "maps_url": "https://www.google.com/maps?cid=...",
    "thumbnail_url": "https://..."
  },
  "phone_ref": "eyJjaWQ...",
  "phone_ref_unavailable_reason": null
}
```

**Phone fields:**
- `detail.phone` — raw merchant phone number for **display only**
- `phone_ref` — signed token for `/skill/book/phone`. Present when phone booking is available.
- `phone_ref_unavailable_reason` — why `phone_ref` is null (e.g. `"calling this region is not currently supported"`, `"phone number not in international format"`)

### POST /skill/book/phone

One endpoint for all phone calls. The `action` field determines server behavior — it is the primary routing key.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action | string | No | **Routing key.** `book` (default), `cancel`, `reschedule`, `inquiry` |
| phone_ref | string | Conditional | Required for `book` and `inquiry` |
| booking_id | int | Conditional | Required for `cancel` and `reschedule` |
| call_plan | object | Yes | See below |

**`phone_ref` and `booking_id` are mutually exclusive.** Passing both returns 422.

**Preconditions for cancel/reschedule:**
- `booking_id` must exist and belong to the current token's user — 404 if not found.
- Booking must have status `confirmed` and a callable merchant phone — 422 otherwise.

**call_plan fields (new booking):**

| Field | Level | Description |
|-------|-------|-------------|
| purpose | Required | Natural-language prompt for the AI caller (does not affect routing). e.g. "Book a table at …" |
| merchant_name | Required | Business name |
| date, time, party_size, name | Required | Booking details |
| contact_phone | Recommended | E.164 format (e.g. "+6591234567") — auto-formatted for voice readability |
| special_requests | Optional | String array — passed to AI caller as-is |
| predicted_qa | Optional | Array of {question, answer} — helps AI caller handle merchant questions |
| fallback_instructions | Optional | Free-text fallback guidance for the AI caller |
| language | Ignored | Do not set — auto-inferred from merchant phone country |

**call_plan fields (cancel/reschedule):**

| Field | Required | Description |
|-------|----------|-------------|
| purpose | Yes | e.g. "Cancel reservation at Sushi Dai" |
| new_date | For reschedule | New date (provide if date is changing) |
| new_time | For reschedule | New time (provide if time is changing) |

At least one of `new_date` or `new_time` is required for reschedule. Only include the fields that are changing.

Server auto-fills: `language`, merchant phone, original booking details.

**call_plan fields (inquiry):**

| Field | Required | Description |
|-------|----------|-------------|
| purpose | Yes | e.g. "Ask about opening hours and dress code" |

Result contains the merchant's answer in `result.summary`. No booking record is created.

**Response (202):**
```json
{
  "task_id": 42,
  "status": "pending",
  "poll_url": "/skill/task/42"
}
```

### PATCH /skill/bookings/{booking_id}

Client-side write-back: update your booking record after confirming the call result. This is the caller's own record — the server does not auto-update bookings based on call outcomes.

| Field | Type | Description |
|-------|------|-------------|
| status | string | New status, e.g. "cancelled" |
| booking_time | string | New date+time for reschedule. Recommended format: `"YYYY-MM-DD HH:MM"` (merchant's local time, no timezone needed) |
| party_size | int | New party size |

Each field is individually optional, but the request must include **at least one** field. Sending an empty body returns 422.

```json
{"status": "cancelled"}
```
```json
{"booking_time": "2026-04-12 20:00"}
```

**422 — No fields to update:**
```json
{"detail": "No fields to update"}
```

### GET /skill/task/{task_id}

**Pending:**
```json
{
  "task_id": 42,
  "status": "pending",
  "created_at": "2026-04-04T10:00:00+00:00"
}
```

**Completed:**
```json
{
  "task_id": 42,
  "status": "completed",
  "result": {
    "status": "confirmed",
    "summary": "Table booked for 2 at 12pm on April 10th",
    "details": "Confirmed under name Alex",
    "conditions": ["Smart casual dress code"],
    "duration_seconds": 45
  },
  "completed_at": "2026-04-04T10:02:15+00:00"
}
```

### GET /skill/bookings

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| status | string | "" | Filter: "confirmed", "cancelled", or empty for both |
| limit | int | 20 | Max results (capped at 50) |

```json
{
  "bookings": [
    {
      "id": 3,
      "merchant_name": "Sushi Dai",
      "method": "phone",
      "status": "confirmed",
      "booking_time": "2026-04-07 18:00",
      "party_size": 4,
      "merchant_phone": "+81312345678",
      "created_at": "2026-04-06T10:00:00+00:00"
    }
  ]
}
```

### GET /skill/balance

```json
{
  "points_balance": 18500,
  "display_name": "Alex"
}
```

## Pricing

| Action | Cost |
|--------|------|
| Search | 5 points |
| Detail | 15 points |
| Phone call | 300 points/min (min 1 min) |

Top up: [t.me/lifeclaw_ai_bot?start=topup](https://t.me/lifeclaw_ai_bot?start=topup)

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Missing or invalid token |
| 402 | Insufficient points |
| 403 | Account inactive |
| 404 | Resource not found |
| 422 | Invalid request body |
| 429 | Too many pending tasks (max 10) |
| 502 | Voice service unavailable |

**Error response examples:**

402 Insufficient Points:
```json
{
  "detail": {
    "error": "Insufficient points (need 5, have 0)",
    "balance": 0,
    "required": 5,
    "topup_url": "https://t.me/lifeclaw_ai_bot?start=topup"
  }
}
```

422 Invalid Request:
```json
{
  "detail": "call_plan missing 'purpose'"
}
```

422 Tampered phone_ref:
```json
{
  "detail": "Invalid or tampered phone_ref"
}
```

## Limits

- 10 concurrent pending phone bookings per user
- 10 API tokens per user
