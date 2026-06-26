# Apartment Cleaning — Full Example Booking Flow

All interactions go through the `claw.cleaning` REST API at `https://claw.cleaning`. The agent makes plain HTTPS requests — no local CLI, no MCP server.

No payment is collected up front. The customer pays the cleaner (cash or card) at the appointment.

## Customer starts

**Customer:** "Hey, I want to book an apartment cleaning"

**Agent:** "Great! Let me check what's available."

HTTP request:
```
GET https://claw.cleaning/availability
```

Response (`200 OK`):
```json
{
  "days": [
    {
      "date": "2026-04-18",
      "slots": [
        { "startTime": "09:00", "maxHours": 5 },
        { "startTime": "10:00", "maxHours": 4 },
        { "startTime": "14:00", "maxHours": 3 }
      ]
    },
    {
      "date": "2026-04-19",
      "slots": [
        { "startTime": "09:00", "maxHours": 8 }
      ]
    }
  ]
}
```

**Agent:** "Here's what's open:

**Saturday, April 18:**
- 9:00 AM (up to 5 hours, max $200)
- 10:00 AM (up to 4 hours, max $160)
- 2:00 PM (up to 3 hours, max $120)

**Sunday, April 19:**
- 9:00 AM (up to 8 hours, max $320)

Rate is $40/hour, paid to the cleaner at the appointment. Which time works for you?"

---

## Customer selects a slot

**Customer:** "Saturday at 10, I need 3 hours"

**Agent:** "Got it — 3 hours at $120 total, paid to the cleaner. A few more things:
- What's the full address? (Must be in San Francisco)
- Your name?
- Your email for the calendar invite?"

**Customer:** "456 Castro St, San Francisco, CA 94114. Jane Smith, jane@example.com."

---

## Agent confirms before booking

**Agent:** "Here's your booking summary before I confirm:

- **Date:** Saturday, April 18, 2026
- **Time:** 10:00 AM – 1:00 PM (3 hours)
- **Address:** 456 Castro St, San Francisco, CA 94114
- **Name:** Jane Smith
- **Email:** jane@example.com
- **Total:** $120 (cash or card to the cleaner at the appointment)

Shall I proceed?"

**Customer:** "Yes, book it!"

---

## Agent initiates booking

HTTP request:
```
POST https://claw.cleaning/bookings/initiate
Content-Type: application/json

{
  "date": "2026-04-18",
  "startTime": "10:00",
  "hours": 3,
  "address": "456 Castro St, San Francisco, CA 94114",
  "name": "Jane Smith",
  "email": "jane@example.com"
}
```

Response (`200 OK`):
```json
{
  "status": "booked",
  "total": "$120",
  "date": "2026-04-18",
  "startTime": "10:00",
  "hours": 3,
  "address": "456 Castro St, San Francisco, CA 94114",
  "email": "jane@example.com",
  "message": "Cleaning confirmed for 2026-04-18 at 10:00 (3h). Calendar invite sent to jane@example.com. Pay $120 cash or card to the cleaner at the appointment."
}
```

**Agent:** "You're booked! The calendar invite is on its way to jane@example.com. Please have $120 ready for the cleaner at the end of the session — they take cash or card."

---

## Status check

**Customer:** "Did that go through?"

HTTP request:
```
GET https://claw.cleaning/bookings/status?email=jane%40example.com
```

Response (`200 OK`):
```json
{
  "email": "jane@example.com",
  "bookings": [
    {
      "date": "2026-04-18",
      "startTime": "10:00",
      "hours": 3,
      "address": "456 Castro St, San Francisco, CA 94114",
      "eventId": "..."
    }
  ]
}
```

**Agent:** "You're all set! Your cleaning is confirmed for April 18th at 10:00 AM. Check your email for the calendar invite."

---

## Edge cases

### Address not in SF
`POST /bookings/initiate` returns `400` with `{ "error": "Address must be in San Francisco, CA." }`.
**Agent:** "Sorry, the cleaning service is only available in San Francisco. Do you have an SF address?"

### Slot unavailable
`POST /bookings/initiate` returns `409` with `{ "error": "That time slot is no longer available. Please check availability and choose another time." }`.
**Agent:** "That slot was just taken. Let me check what else is available..." — then `GET /availability?date=<same-date>` for the same date.

### Email blocked
`POST /bookings/initiate` returns `403` with `{ "error": "This email is blocked from booking. Contact the operator at connor@getcolby.com.", "code": "email_blocked" }`.
**Agent:** "Your email has been blocked from booking through this service, usually because of a past no-show. Please contact the operator at connor@getcolby.com."

### No-show policy
If the customer asks to cancel, they can email **connor@getcolby.com** at least 24 hours before the slot. Persistent no-shows may result in the email being blocked from future bookings.

---

## Quick `curl` reference

```sh
# Upcoming availability (next 14 bookable days)
curl https://claw.cleaning/availability

# One specific day (before 2026-05-05, must be Saturday or Sunday)
curl "https://claw.cleaning/availability?date=2026-04-18"

# Book a slot
curl -X POST https://claw.cleaning/bookings/initiate \
  -H 'Content-Type: application/json' \
  -d '{
    "date": "2026-04-18",
    "startTime": "10:00",
    "hours": 3,
    "address": "456 Castro St, San Francisco, CA 94114",
    "name": "Jane Smith",
    "email": "jane@example.com"
  }'

# Check status for an email
curl "https://claw.cleaning/bookings/status?email=jane%40example.com"
```
