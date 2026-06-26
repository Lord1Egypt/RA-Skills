---
name: airport-pickups-london
description: Book UK airport and cruise port transfers via Airport Pickups London. Get instant fixed-price quotes, validate flights, create bookings, amend, cancel, and track drivers live. TfL-licensed, 24/7 service. Requires API key (free instant registration).
homepage: https://www.airport-pickups-london.com
metadata:
  clawdbot:
    emoji: "🚖"
---

# Airport Pickups London — Transfer Booking Skill

This skill connects your agent to Airport Pickups London's booking API via MCP, giving it full transfer management — quotes, bookings, amendments, cancellations, and live driver tracking.

## Authentication Required

**This skill requires an API key** via the `x-api-key` header. No environment variables are needed.

**Get a key instantly** (free, no approval):

```bash
curl -X POST https://mcp.airport-pickups-london.com/a2a/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Your Agent Name", "email": "you@example.com"}'
```

## Setup

Add the APL MCP server to your config:

```json
{
  "mcpServers": {
    "airport-pickups-london": {
      "url": "https://mcp.airport-pickups-london.com/mcp",
      "headers": {
        "x-api-key": "YOUR_API_KEY"
      }
    }
  }
}
```

## Available Tools (8)

### `get_quote` — Get Transfer Prices
Get prices for any UK transfer route. Returns all car types with prices, capacity, and luggage allowance.

**Example prompts:**
- "How much is a taxi from Heathrow to central London?"
- "Get me a quote from Gatwick to Brighton for 4 passengers"
- "What's the price from Southampton cruise port to London?"

### `validate_flight` — Flight Validation
Verify a flight number and get terminal, airline, arrival time, and meeting point.

**Example prompts:**
- "Check flight BA2534 arriving on April 15th"
- "What terminal does EK007 arrive at?"

### `book_transfer` — Create Booking
Create a confirmed transfer booking. Returns booking reference, manage URL, meeting point.

**Example prompts:**
- "Book a People Carrier from Heathrow to W1K 1LN for John Smith, flight BA2534, April 15th at 3pm"

### `lookup_booking` — Check Booking Status
Look up booking details by reference number. Returns status, driver info, and manage URL.

**Example prompts:**
- "What's the status of booking APL-CJ5KDJ?"

### `amend_booking` — Modify Booking
Change passenger name, phone, email, flight number, date/time, or special requests.

**Example prompts:**
- "Change the flight on APL-CJ5KDJ to BA2590"
- "Update the passenger name to Jane Doe"

### `cancel_booking` — Cancel Booking
Cancel a booking. Free cancellation 12+ hours before pickup.

**Example prompts:**
- "Cancel booking APL-CJ5KDJ"

### `track_driver` — Live Driver Tracking
Get the driver's live GPS position, vehicle details, photo, and ETA.

**Example prompts:**
- "Where is my driver for APL-CJ5KDJ?"

### `get_service_info` — FAQ & Policies
Get info about cancellation policy, payment methods, vehicles, child seats, pets, accessibility, meet and greet, cruise ports, corporate accounts.

**Example prompts:**
- "What's the cancellation policy?"
- "Do you provide child seats?"

## Data & Privacy

This skill sends the following data to the APL booking API:
- Pickup and dropoff locations
- Passenger name, phone, email
- Flight numbers

All data is transmitted over HTTPS (TLS 1.2+) and stored by Airport Pickups London for service delivery. GDPR compliant. The API key authenticates the agent, not the end user.

## Pricing Negotiation (A2A Extension)

Agents can request a discount by including `requestedDiscountPercent` in the quote request. Maximum discount is **5%**. Non-negotiable: peak surcharges, event pricing, child seats.

## Pricing Info

- All prices in GBP, per vehicle (not per person)
- Fixed prices — no surge, no hidden charges
- Includes meet & greet, waiting time, parking, tolls
- Free cancellation 12+ hours before pickup

## Vehicle Types

| Car Type | Passengers | Suitcases | From |
|----------|-----------|-----------|------|
| Saloon | Up to 3 | 3 | ~£33 |
| People Carrier | Up to 5 | 5 | ~£45 |
| 8 Seater | Up to 8 | 8 | ~£55 |
| Executive Saloon | Up to 3 | 3 | ~£65 |
| Executive MPV | Up to 7 | 7 | ~£85 |

## Important Rules for Agents

1. **ALWAYS call get_quote before booking** — never guess prices
2. **NEVER call book_transfer without user confirmation** — always show the price and get a "yes" first
3. Flight validation is optional and never blocks a booking
4. For airport pickups, recommend clearance: domestic 15min, European 45min, international 60min after landing

## Support

- 24/7 Phone: +44 208 688 7744
- WhatsApp: +44 7538 989360
- Website: www.airport-pickups-london.com
- Email: info@aplcars.com

## Ratings

TripAdvisor 4.7/5 | Trustpilot 4.9/5 | Reviews.io 4.9/5
