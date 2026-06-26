---
name: book-anything
description: Searches for businesses (restaurants, salons, clinics, hotels) and books appointments via AI phone calls. Also cancels, reschedules, and makes merchant inquiries by phone. Use when a user says "find", "book", "reserve", "cancel", "reschedule", or asks about a local business. Supports any language — the AI caller matches the merchant's language automatically.
metadata:
  author: lifeclaw
  version: "1.4.2"
  homepage: https://lifeclaw.agentese.ai
  clawdbot:
    emoji: "📞"
    requires:
      env:
        - LIFECLAW_API_TOKEN
    primaryEnv: LIFECLAW_API_TOKEN
---

# Book Anything — Search + AI Phone Booking

Search for any business, get full details, and book via an AI-powered phone call — all through a REST API.

**Base URL:** `https://api-v2.lifeclaw.agentese.ai`

## Quick Start

```bash
BASE_URL="https://api-v2.lifeclaw.agentese.ai"

# 1. Search
curl -X POST "$BASE_URL/skill/search" \
  -H "Authorization: Bearer $LIFECLAW_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "sushi near Shibuya", "location": "Tokyo"}'

# 2. Get details + phone_ref
curl -X POST "$BASE_URL/skill/detail" \
  -H "Authorization: Bearer $LIFECLAW_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Sushi Dai", "cid": "12345678901234567"}'

# 3. Book by phone (only if phone_ref is not null)
curl -X POST "$BASE_URL/skill/book/phone" \
  -H "Authorization: Bearer $LIFECLAW_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"phone_ref": "<phone_ref from step 2>", "call_plan": {"purpose": "Book a table", "merchant_name": "Sushi Dai", "date": "2026-04-10", "time": "12:00", "party_size": 2, "name": "Alex"}}'

# 4. Poll until status != "pending" (use task_id from step 3 response)
curl "$BASE_URL/skill/task/{task_id}" \
  -H "Authorization: Bearer $LIFECLAW_API_TOKEN"
```

## When to Use

- User asks to **find a business** (restaurant, salon, clinic, hotel, etc.)
- User wants to **book / reserve** something by phone
- User wants to **cancel or reschedule** an existing reservation
- User wants to **ask a merchant** a question (hours, menu, dress code, etc.)
- User needs **business details** (phone number, hours, address, reviews)

## Authentication

All requests require `Authorization: Bearer <token>` header.

**Get a token:** Message `@lifeclaw_ai_bot` on Telegram:
```
/token_create <name>
```

**Store the token** as environment variable `LIFECLAW_API_TOKEN`. Token is shown once only — save it immediately. Lost tokens cannot be recovered; create a new one with `/token_create <name>`.

---

## Workflow: New Booking

Follow steps 1–4 in order. Do NOT skip steps.

### Step 1 — Search

```
POST {base_url}/skill/search
{"query": "sushi near Shibuya", "location": "Tokyo", "language": "en", "limit": 5}
```

Response: list of places with `cid` and `maps_url`.

### Step 2 — Get Details

```
POST {base_url}/skill/detail
{"name": "Sushi Dai", "cid": "12345678901234567", "language": "en"}
```

Key response fields:
- `phone_ref` — signed token for booking. **If `null`, phone booking is NOT available.** Check `phone_ref_unavailable_reason`.
- `detail.phone` — merchant phone for **display only**
- `booking_url` — online booking link (if available)

**When `phone_ref` is `null`:** Do NOT call `/skill/book/phone`. Show `detail.phone` and `booking_url` to the user instead.


### Step 3 — Book by Phone

**Only call this if `phone_ref` is not null.**

```
POST {base_url}/skill/book/phone
{
  "phone_ref": "<phone_ref from Step 2>",
  "call_plan": {
    "purpose": "Book a table at Sushi Dai",
    "merchant_name": "Sushi Dai",
    "date": "2026-04-10",
    "time": "12:00",
    "party_size": 2,
    "name": "Alex",
    "contact_phone": "+6591234567"
  }
}
```

The `action` field determines what the server does (`book`, `cancel`, `reschedule`, `inquiry`). `purpose` inside `call_plan` is a natural-language prompt for the AI caller — it does NOT affect routing.

**call_plan fields (new booking):**
- **Required:** `purpose`, `merchant_name`, `date`, `time`, `party_size`, `name`
- **Recommended:** `contact_phone` (E.164) — auto-formatted for voice readability
- **Optional:** `special_requests` (string array), `predicted_qa` (array of {question, answer}), `fallback_instructions`
- **Ignored:** `language` — do not set, auto-inferred from merchant phone

Returns `{"task_id": {id}, "status": "pending", "poll_url": "/skill/task/{id}"}`.

### Step 4 — Poll Result

```
GET {base_url}/skill/task/{task_id}
```

Poll every 10 seconds until top-level `status` is no longer `"pending"`. Do NOT use increasing delays — use a fixed 10-second interval. Timeout after 5 minutes.

**Two-layer status:** Top-level `status` (`pending` / `completed` / `failed`) indicates whether the task is still running. Inner `result.status` indicates the booking outcome. Only stop polling when top-level `status != "pending"`; only treat the operation as successful when `result.status == "confirmed"`.

**Result interpretation:**

| `result.status` | Meaning | Action |
|-----------------|---------|--------|
| `confirmed` | Booking succeeded | Show confirmation to user |
| `pending` | Merchant hasn't confirmed yet | Tell user to wait for callback |
| `rejected` | Merchant refused | Suggest alternatives |
| `failed` | Call failed (no answer, etc.) | Show merchant phone for manual action |

---

## Workflow: Cancel / Reschedule

Uses the same `/skill/book/phone` endpoint with `booking_id` instead of `phone_ref`. Server auto-fills merchant phone and original booking details.

### Step 1 — Get Booking History

```
GET {base_url}/skill/bookings?status=confirmed
```

### Step 2 — Make the Call

Use the `id` from Step 1 as `booking_id`.

**Cancel:**
```
POST {base_url}/skill/book/phone
{"action": "cancel", "booking_id": 3, "call_plan": {"purpose": "Cancel reservation at Sushi Dai"}}
```

**Reschedule:**
```
POST {base_url}/skill/book/phone
{"action": "reschedule", "booking_id": 3, "call_plan": {"purpose": "Reschedule reservation at Sushi Dai", "new_date": "2026-04-12", "new_time": "20:00"}}
```

Provide `new_date` and/or `new_time` — only include the fields that are changing. For example, to change only the time, omit `new_date`.

Poll with Step 4 from the new booking workflow.

### Step 3 — Update Booking Record

After polling completes and `result.status == "confirmed"`, update the record:

```
PATCH {base_url}/skill/bookings/{booking_id}
{"status": "cancelled"}          // for cancel
{"booking_time": "2026-04-12 20:00"}  // for reschedule
```

**Important:** Booking records are client-managed. The server does NOT auto-update them based on call outcomes — you must call PATCH to write back the confirmed result.

---

## Workflow: Inquiry

For general questions (hours, menu, dress code, parking) — no booking involved.

```
POST {base_url}/skill/book/phone
{"action": "inquiry", "phone_ref": "<phone_ref from /skill/detail>", "call_plan": {"purpose": "Ask about opening hours and dress code"}}
```

Poll with Step 4. Answer is in `result.summary`. No booking record is created.

---

## Other Endpoints

- **Check balance:** `GET {base_url}/skill/balance`
- **Booking history:** `GET {base_url}/skill/bookings?status=confirmed&limit=10`

## Edge Cases

- **`phone_ref` is `null`:** Do NOT call `/skill/book/phone`. Show phone + booking_url instead.
- **Insufficient points (402):** Response includes `topup_url` — direct user to top up.
- **Phone call fails:** Show merchant phone for manual calling. Suggest `booking_url` if available.
- **No search results:** Suggest broadening query or different location.
- **Polling > 5 min:** Task likely timed out.

## Privacy & Data Handling

This skill sends user-provided data (name, phone number, party size, special requests) to the LifeClaw API (`api-v2.lifeclaw.agentese.ai`) to perform bookings on the user's behalf. This data is:

- Used solely to complete the requested booking via phone call or online reservation
- Not shared with third parties beyond the merchant being called
- Not used for advertising or profiling
- Retained only as booking records accessible to the token owner

API tokens are scoped to the creating user and can be revoked at any time via `@lifeclaw_ai_bot` with `/token_revoke <name>`.

For questions about data handling, contact: [https://t.me/agenteseAI](https://t.me/agenteseAI)

## API Reference

See [references/api.md](references/api.md) for complete request/response schemas and error codes.
