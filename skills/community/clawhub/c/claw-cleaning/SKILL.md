---
name: apartment-cleaning
description: "Book a professional apartment cleaning in San Francisco via the claw.cleaning REST API. Use when someone wants to book, schedule, or inquire about apartment cleaning services, cleaning availability, cleaning prices, or cleaning appointments. Rate is $40/hour. Any day of the week on/after 2026-05-05; Saturdays and Sundays only before then. SF addresses only. No payment is collected up front — customers pay the cleaner in cash or card at the appointment. Handles the full flow: check availability, collect details, confirm booking."
metadata: {"openclaw":{"emoji":"🧹","api":{"baseUrl":"https://claw.cleaning","endpoints":[{"name":"check_availability","method":"GET","path":"/availability"},{"name":"initiate_booking","method":"POST","path":"/bookings/initiate"},{"name":"check_booking_status","method":"GET","path":"/bookings/status"}]}}}
---

# Apartment Cleaning Booking

## At a Glance
- **Service:** Professional apartment cleaning
- **Area:** San Francisco only
- **Rate:** $40/hour (1–8 hours)
- **Days:** Any day of the week on/after 2026-05-05. Before then, Saturdays and Sundays only.
- **Hours:** 8 AM – 6 PM PT
- **Payment:** No upfront payment. The customer pays the cleaner (cash or card) at the appointment.

## How This Skill Works

This skill calls the `claw.cleaning` REST API directly over HTTPS — no local CLI, no MCP server.

- **Base URL:** `https://claw.cleaning`
- **Auth:** None. All endpoints are public.
- **Content type:** `application/json`

Use the agent's HTTP/fetch capability (e.g. `curl`, `fetch`, `requests`) to call the endpoints below.

### Available Endpoints
- `GET /availability` — list open slots
- `POST /bookings/initiate` — reserve a slot (calendar invite sent immediately, customer pays the cleaner at the appointment)
- `GET /bookings/status` — list upcoming bookings by email

## Safety Rules
- Never `POST /bookings/initiate` without showing the full preview to the customer and getting explicit confirmation ("yes", "confirm", "book it", etc.).
- Always `GET /availability` before `POST /bookings/initiate` to confirm the slot is listed as available.
- Do not invent available times — only offer times returned by `GET /availability`.
- Make it clear to the customer that the total ($40/hour × hours) is paid in cash or card to the cleaner at the end of the session.

## Booking Workflow

### Step 1 — Check availability

`GET https://claw.cleaning/availability` returns the next 14 upcoming bookable days under a top-level `days` array. Pass `?date=YYYY-MM-DD` to check one specific day. Before 2026-05-05 the date must be a Saturday or Sunday; on or after, any day of the week is bookable.

Examples:
```
GET https://claw.cleaning/availability
GET https://claw.cleaning/availability?date=2026-05-06
```

Present the available slots clearly. Each slot shows `startTime` and `maxHours` available.

### Step 2 — Collect customer details
Ask the customer:
- Which date and start time?
- How many hours? (1–8, $40 each)
- Full SF address (street, city, state)
- Their name
- Their email (calendar invite goes here)

### Step 3 — Confirm before booking
Show the customer a summary (date, start time, hours, address, total, email) and remind them the total is paid to the cleaner at the appointment. Ask for explicit confirmation before posting the booking.

### Step 4 — Initiate booking

`POST https://claw.cleaning/bookings/initiate` with a JSON body:
```json
{
  "date": "YYYY-MM-DD",
  "startTime": "HH:MM",
  "hours": 1-8,
  "address": "... San Francisco, CA ...",
  "name": "Customer Name",
  "email": "customer@example.com"
}
```

Send `Content-Type: application/json`. On success returns `{ "status": "booked", "total": "$X", ... }`. The slot is reserved immediately and the calendar invite is sent.

### Step 5 — Deliver the outcome
Tell the customer the slot is booked, the calendar invite is on its way, and they owe the cleaner $40/hour at the end of the session (cash or card).

### Step 6 — Check status (optional)

`GET https://claw.cleaning/bookings/status?email=<url-encoded-email>` if the customer asks whether their booking went through. Returns upcoming bookings for that email.

## Key Details
- Working hours: 8 AM – 6 PM PT
- 30-min travel buffers are automatically blocked before and after each cleaning
- The calendar event blocks the slot immediately on booking
- Persistent no-shows may result in the email being blocked from future bookings

## Error Handling

All errors return a JSON body with an `error` field and a non-2xx HTTP status.

- `400` `"Address must be in San Francisco, CA."` → ask for a valid SF address
- `400` `"Hours must be between 1 and 8."` → correct the hours value
- `400` `"Weekdays before 2026-05-05 are not bookable..."` → pick a Saturday/Sunday, or any day on or after 2026-05-05
- `400` `"Cannot book a time in the past..."` → pick a future date and time
- `400` `"Invalid date format. Use YYYY-MM-DD."` / `"Invalid startTime format. Use HH:MM (24h)."` → fix the format
- `400` `"Invalid email address."` → ask for a valid email
- `403` `"This email is blocked from booking."` (`code: "email_blocked"`) → the operator has blocked this email due to prior no-shows. Customer should contact connor@getcolby.com.
- `409` `"That time slot is no longer available."` → call `GET /availability` and offer alternatives
- `500` `"Failed to fetch availability."` / `"Failed to initiate booking."` / `"Could not create calendar event."` → retry once; if it keeps failing, tell the customer to try again later

See `references/booking-flow.md` for a full example conversation flow with sample HTTP requests and responses.
