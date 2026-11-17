# Cal.com Calendar Integration Skill

## Metadata

- **name**: cal-com
- **description**: Integrate with Cal.com calendar: list event types, create/cancel bookings, get available slots, and manage availability schedules via the Cal.com REST API.
- **version**: 1.0.0
- **author**: OpenClaw CCD Team
- **platform**: OpenClaw (ClawHub Skill)

---

## Trigger Phrases

1. "list my Cal.com event types"
2. "show available Cal.com bookings"
3. "book a meeting on Cal.com"
4. "cancel my Cal.com reservation"
5. "get open slots on Cal.com"
6. "what event types do I have on Cal.com"
7. "create a Cal.com booking for"
8. "remove my Cal.com booking"
9. "sync Cal.com availability"
10. "check my Cal.com schedule"
11. "set up Cal.com availability"
12. "update my Cal.com working hours"
13. "Cal.com integration"
14. "connect to my Cal.com account"
15. "get my Cal.com user info"

---

## Capabilities

This skill enables the following operations against the Cal.com REST API (v2):

1. **List Event Types** — Retrieve all event types defined in your Cal.com account, including slug, title, duration, and description.
2. **Create a Booking** — Book a time slot for a specific event type on behalf of a user.
3. **Cancel a Booking** — Cancel an existing booking by its unique UID.
4. **List Bookings** — Fetch upcoming and/or past bookings for the authenticated user.
5. **Get Available Slots** — Query available time slots for a given event type and date range.
6. **Create / Update Availability Schedule** — Define or modify weekly availability rules (working hours, date overrides).
7. **Get User Info** — Retrieve the authenticated user's profile, timezone, and default settings.

All API calls target `https://api.cal.com/v1`. Authentication uses a Bearer token (API key).

---

## Prerequisites

Before using this skill, you must have:

- A **Cal.com account** (self-hosted or on cal.com)
- A **Cal.com API Key** (v2 format) with appropriate read/write scopes
- Your Cal.com **username or user ID** (e.g., `johnsmith` or `123456`)

### Environment Variables

Store these in your OpenClaw environment or skill config:

```
CAL_COM_API_KEY=your_calcom_api_key_here
CAL_COM_USERNAME=your_calcom_username_here
```

---

## Detailed Steps

### 1 — List Event Types

**Endpoint:** `GET /event-types`

**Headers:**
```
Authorization: Bearer {CAL_COM_API_KEY}
Content-Type: application/json
```

**Example cURL:**
```bash
curl -s "https://api.cal.com/v1/event-types" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}"
```

**Example Response (success):**
```json
{
  "event_types": [
    {
      "id": "evt_abc123",
      "slug": "30-min-meeting",
      "title": "30 Minute Meeting",
      "duration": 30,
      "description": "A quick 30-minute call",
      "active": true
    },
    {
      "id": "evt_def456",
      "slug": "60-min-consultation",
      "title": "60 Minute Consultation",
      "duration": 60,
      "description": "Deep dive session",
      "active": true
    }
  ]
}
```

**Failure Response:**
```json
{
  "error": "unauthorized",
  "message": "Invalid or expired API key."
}
```

---

### 2 — Create a Booking

**Endpoint:** `POST /bookings`

**Headers:**
```
Authorization: Bearer {CAL_COM_API_KEY}
Content-Type: application/json
```

**Request Body:**
```json
{
  "eventTypeId": "evt_abc123",
  "startTime": "2026-07-10T14:00:00Z",
  "endTime": "2026-07-10T14:30:00Z",
  "attendee": {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "timezone": "Asia/Shanghai"
  },
  "notes": "Looking forward to the call"
}
```

**Example cURL:**
```bash
curl -s -X POST "https://api.cal.com/v1/bookings" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "eventTypeId": "evt_abc123",
    "startTime": "2026-07-10T14:00:00Z",
    "endTime": "2026-07-10T14:30:00Z",
    "attendee": {
      "name": "Jane Doe",
      "email": "jane.doe@example.com",
      "timezone": "Asia/Shanghai"
    }
  }'
```

**Example Response (success):**
```json
{
  "booking": {
    "id": "bk_xyz789",
    "uid": "bk_xyz789",
    "eventTypeId": "evt_abc123",
    "title": "30 Minute Meeting",
    "startTime": "2026-07-10T14:00:00Z",
    "endTime": "2026-07-10T14:30:00Z",
    "status": "accepted",
    "attendees": [
      {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
      }
    ]
  }
}
```

**Failure Response:**
```json
{
  "error": "booking_conflict",
  "message": "The requested time slot is no longer available."
}
```

---

### 3 — Cancel a Booking

**Endpoint:** `DELETE /bookings/{uid}`

**Headers:**
```
Authorization: Bearer {CAL_COM_API_KEY}
```

**Example cURL:**
```bash
curl -s -X DELETE "https://api.cal.com/v1/bookings/bk_xyz789" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}"
```

**Example Response (success):**
```json
{
  "booking": {
    "id": "bk_xyz789",
    "status": "cancelled"
  },
  "message": "Booking cancelled successfully."
}
```

**Failure Response:**
```json
{
  "error": "not_found",
  "message": "Booking with UID bk_xyz789 not found."
}
```

---

### 4 — List Bookings

**Endpoint:** `GET /bookings`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status: `upcoming`, `past`, `cancelled` |
| `limit` | integer | Max results (default: 20, max: 100) |
| `cursor` | string | Pagination cursor |

**Example cURL:**
```bash
curl -s "https://api.cal.com/v1/bookings?status=upcoming&limit=10" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}"
```

**Example Response (success):**
```json
{
  "bookings": [
    {
      "id": "bk_xyz789",
      "uid": "bk_xyz789",
      "title": "30 Minute Meeting",
      "startTime": "2026-07-10T14:00:00Z",
      "endTime": "2026-07-10T14:30:00Z",
      "status": "accepted",
      "eventType": {
        "slug": "30-min-meeting",
        "title": "30 Minute Meeting"
      },
      "attendees": [
        {
          "name": "Jane Doe",
          "email": "jane.doe@example.com"
        }
      ]
    }
  ],
  "nextPageCursor": null
}
```

---

### 5 — Get Available Slots

**Endpoint:** `GET /slots`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `eventTypeId` | string | The event type ID to check |
| `startTime` | ISO 8601 | Range start (e.g., `2026-07-10T00:00:00Z`) |
| `endTime` | ISO 8601 | Range end (e.g., `2026-07-15T23:59:59Z`) |

**Example cURL:**
```bash
curl -s "https://api.cal.com/v1/slots?eventTypeId=evt_abc123&startTime=2026-07-10T00:00:00Z&endTime=2026-07-15T23:59:59Z" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}"
```

**Example Response (success):**
```json
{
  "slots": [
    {
      "startTime": "2026-07-10T09:00:00Z",
      "endTime": "2026-07-10T09:30:00Z",
      "available": true
    },
    {
      "startTime": "2026-07-10T10:00:00Z",
      "endTime": "2026-07-10T10:30:00Z",
      "available": true
    },
    {
      "startTime": "2026-07-10T10:30:00Z",
      "endTime": "2026-07-10T11:00:00Z",
      "available": false
    }
  ]
}
```

---

### 6 — Create / Update Availability Schedule

**Endpoint:** `POST /schedules` (create) or `PATCH /schedules/{id}` (update)

**Headers:**
```
Authorization: Bearer {CAL_COM_API_KEY}
Content-Type: application/json
```

**Request Body (create):**
```json
{
  "name": "My Working Hours",
  "timezone": "Asia/Shanghai",
  "weeklyAvailability": [
    {
      "day": "Monday",
      "startTime": "09:00",
      "endTime": "18:00"
    },
    {
      "day": "Tuesday",
      "startTime": "09:00",
      "endTime": "18:00"
    },
    {
      "day": "Wednesday",
      "startTime": "09:00",
      "endTime": "18:00"
    },
    {
      "day": "Thursday",
      "startTime": "09:00",
      "endTime": "18:00"
    },
    {
      "day": "Friday",
      "startTime": "09:00",
      "endTime": "17:00"
    }
  ],
  "dateOverrides": [
    {
      "date": "2026-07-04",
      "startTime": "10:00",
      "endTime": "14:00"
    }
  ]
}
```

**Example cURL:**
```bash
curl -s -X POST "https://api.cal.com/v1/schedules" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Working Hours",
    "timezone": "Asia/Shanghai",
    "weeklyAvailability": [
      {"day": "Monday", "startTime": "09:00", "endTime": "18:00"},
      {"day": "Tuesday", "startTime": "09:00", "endTime": "18:00"},
      {"day": "Wednesday", "startTime": "09:00", "endTime": "18:00"},
      {"day": "Thursday", "startTime": "09:00", "endTime": "18:00"},
      {"day": "Friday", "startTime": "09:00", "endTime": "17:00"}
    ]
  }'
```

**Example Response (success):**
```json
{
  "schedule": {
    "id": "sc_abc123",
    "name": "My Working Hours",
    "timezone": "Asia/Shanghai",
    "weeklyAvailability": [
      {"day": "Monday", "startTime": "09:00", "endTime": "18:00"}
    ],
    "dateOverrides": []
  }
}
```

---

### 7 — Get User Info

**Endpoint:** `GET /users/me`

**Example cURL:**
```bash
curl -s "https://api.cal.com/v1/users/me" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}"
```

**Example Response (success):**
```json
{
  "user": {
    "id": "123456",
    "username": "johnsmith",
    "email": "john.smith@example.com",
    "timezone": "Asia/Shanghai",
    "weekStart": "Monday",
    "defaultEventDuration": 30,
    "locale": "en"
  }
}
```

---

## Output Format

### Success Output

Always returns a structured JSON block with a `status` field set to `"success"`:

```json
{
  "status": "success",
  "action": "list_event_types",
  "data": { ... }
}
```

### Failure Output

Always returns a structured JSON block with a `status` field set to `"error"`:

```json
{
  "status": "error",
  "action": "create_booking",
  "error": "booking_conflict",
  "message": "The requested time slot is no longer available."
}
```

---

## Example Conversations

### Example 1 — List Event Types

**User:** "What event types do I have set up on Cal.com?"

**Agent:**
I'll list your Cal.com event types now.

```bash
curl -s "https://api.cal.com/v1/event-types" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}"
```

**Parsed Response:**

```json
{
  "status": "success",
  "action": "list_event_types",
  "data": {
    "event_types": [
      {"id": "evt_abc123", "slug": "30-min-meeting", "title": "30 Minute Meeting", "duration": 30},
      {"id": "evt_def456", "slug": "60-min-consultation", "title": "60 Minute Consultation", "duration": 60},
      {"id": "evt_ghi789", "slug": "15-min-intro", "title": "15 Minute Intro Call", "duration": 15}
    ]
  }
}
```

**Summary for User:**
You have **3 active event types** on Cal.com:

| Title | Duration | Slug |
|-------|----------|------|
| 15 Minute Intro Call | 15 min | 15-min-intro |
| 30 Minute Meeting | 30 min | 30-min-meeting |
| 60 Minute Consultation | 60 min | 60-min-consultation |

---

### Example 2 — Book a Meeting

**User:** "Book a 30-minute meeting with Jane Doe at jane.doe@example.com for July 10th at 2 PM Shanghai time."

**Agent:**
Creating a booking for July 10, 2026 at 14:00 Shanghai time (UTC+8).

```bash
curl -s -X POST "https://api.cal.com/v1/bookings" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "eventTypeId": "evt_abc123",
    "startTime": "2026-07-10T06:00:00Z",
    "endTime": "2026-07-10T06:30:00Z",
    "attendee": {
      "name": "Jane Doe",
      "email": "jane.doe@example.com",
      "timezone": "Asia/Shanghai"
    }
  }'
```

**Parsed Response:**

```json
{
  "status": "success",
  "action": "create_booking",
  "data": {
    "booking": {
      "id": "bk_xyz789",
      "title": "30 Minute Meeting",
      "startTime": "2026-07-10T06:00:00Z",
      "endTime": "2026-07-10T06:30:00Z",
      "status": "accepted",
      "attendees": [{"name": "Jane Doe", "email": "jane.doe@example.com"}]
    }
  }
}
```

**Summary for User:**
✅ Booking confirmed!

- **Title:** 30 Minute Meeting
- **Date:** July 10, 2026 at 2:00 PM (Shanghai / UTC+8)
- **Attendee:** Jane Doe (jane.doe@example.com)
- **Booking ID:** `bk_xyz789`

---

### Example 3 — Check Available Slots

**User:** "What slots are available next week for the 60-minute consultation?"

**Agent:**
Checking available slots for your 60-minute consultation from July 13–17, 2026.

```bash
curl -s "https://api.cal.com/v1/slots?eventTypeId=evt_def456&startTime=2026-07-13T00:00:00Z&endTime=2026-07-17T23:59:59Z" \
  -H "Authorization: Bearer ${CAL_COM_API_KEY}"
```

**Parsed Response:**

```json
{
  "status": "success",
  "action": "get_available_slots",
  "data": {
    "slots": [
      {"startTime": "2026-07-13T02:00:00Z", "endTime": "2026-07-13T03:00:00Z", "available": true},
      {"startTime": "2026-07-13T03:00:00Z", "endTime": "2026-07-13T04:00:00Z", "available": true},
      {"startTime": "2026-07-14T02:00:00Z", "endTime": "2026-07-14T03:00:00Z", "available": true},
      {"startTime": "2026-07-14T04:00:00Z", "endTime": "2026-07-14T05:00:00Z", "available": false},
      {"startTime": "2026-07-15T02:00:00Z", "endTime": "2026-07-15T03:00:00Z", "available": true}
    ]
  }
}
```

**Summary for User:**
Available 60-minute slots next week (Shanghai timezone):

- **Mon Jul 13:** 10:00 AM, 11:00 AM
- **Tue Jul 14:** 10:00 AM only (11:00 AM is booked)
- **Wed Jul 15:** 10:00 AM

(UTC times shown; subtract 8 hours for Shanghai local time.)

---

## Installation Guide

### Step 1 — Get Your Cal.com API Key

1. Log in to your Cal.com account at [cal.com](https://cal.com) (or your self-hosted instance).
2. Navigate to **Settings → Developer → API Keys**.
3. Click **New API Key**.
4. Give it a descriptive name (e.g., `OpenClaw Integration`).
5. Select the required scopes: `bookings:read`, `bookings:write`, `event-types:read`, `schedules:read`, `schedules:write`.
6. Click **Create** and copy the generated key immediately — it is shown only once.
7. Store it securely; do not share it publicly.

### Step 2 — Find Your Username

- Your Cal.com username appears in your profile URL: `cal.com/{username}`.
- Alternatively, after creating the API key, the user ID is visible in **Settings → Profile**.

### Step 3 — Configure the Skill

Set the following environment variables or OpenClaw config entries:

```bash
CAL_COM_API_KEY=cal_v2_your_generated_key_here
CAL_COM_USERNAME=your_username_here
```

### Step 4 — Verify Connectivity

Test your setup by asking:
> "Get my Cal.com user info"

If successful, you'll see your profile returned. If you get an `unauthorized` error, double-check that your API key is valid and has not expired.

---

## Caveats

### Rate Limiting

- Cal.com API v2 enforces rate limits per API key (typically **60 requests/minute** for standard plans).
- Implement exponential backoff on `429 Too Many Requests` responses.
- Check the `Retry-After` header for the exact wait time.
- Avoid polling slots or bookings in tight loops; cache results where possible.

### Webhook Support

- This skill does **not** handle Cal.com Webhooks directly.
- If you need real-time booking notifications, pair this skill with an OpenClaw webhook receiver or an external middleware (e.g., a small Express server) that forwards events to OpenClaw.
- Ensure your webhook endpoint is HTTPS and reachable from the internet for Cal.com to deliver events.

### Timezone Handling

- **Always use ISO 8601 format with UTC offsets** (e.g., `2026-07-10T14:00:00+08:00`) or pure UTC (`Z`).
- The Cal.com API internally normalizes all times to UTC.
- When displaying times to the user, always convert back to their local timezone (fetchable from `/users/me`).
- Daylight Saving Time (DST) transitions can shift slots by ±1 hour; verify schedule results after DST changes.
- For multi-timezone teams, clarify whose timezone is being used when creating bookings.

### Event Type IDs vs. Slugs

- Use **event type IDs** (`evt_abc123`) in API calls, not slugs, for reliability.
- IDs are stable; slugs can be changed by the user and may cause `404` errors.
- Fetch the ID from the `/event-types` list before creating a booking.

### Cancellation and Rescheduling

- Cancelled bookings are marked with `status: "cancelled"` but are **not deleted** from the system.
- Rescheduling is not directly supported via this skill; cancel the existing booking and create a new one.
- Ensure you check `status` before attempting cancellation to avoid a `not_found` error.

### Availability Schedules

- The `PATCH /schedules/{id}` endpoint performs a **full replace**, not a merge.
- Always fetch the current schedule first, modify the fields you need, then submit the complete object.
- Missing required fields (e.g., `timezone`) in an update will reset them to Cal.com defaults.

### Self-Hosted Instances

- If using a self-hosted Cal.com instance, replace the base URL:
  ```
  https://api.cal.com/v1
  ```
  with your self-hosted API endpoint, e.g.:
  ```
  https://your-calcom-instance.com/api/v1
  ```
- Some features (e.g., certain event type fields) may vary between Cal.com versions. Check your instance's OpenAPI spec at `/api/v2/docs`.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-07-04 | Initial ClawHub release |

---

*Skill ID: `cal-com` | Compatible with Cal.com API v2*
