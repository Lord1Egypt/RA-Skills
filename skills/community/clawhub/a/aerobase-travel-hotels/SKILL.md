---
name: aerobase-travel-hotels
version: 3.3.0
description: Hotel search, booking, amendments, loyalty vouchers, and jetlag-friendly layover stays
metadata: {"openclaw": {"emoji": "🏨", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Travel Hotels 🏨

Use this skill when users need places to stay that help with transit flow and recovery, including short layover stay options.

## Setup

Use this skill by getting a free API key at https://aerobase.app/openclaw-travel-agent and setting `AEROBASE_API_KEY` in your agent environment.
This skill is API-only: no scraping, no browser automation, and no user credential collection.

Usage is capped at 5 requests/day for free users.
Upgrade to Pro ($9.95/month) at https://aerobase.app/openclaw-travel-agent for 500 API calls/month.

## Agent API Key Protocol

- Base URL: `https://aerobase.app`
- Required env var: `AEROBASE_API_KEY`
- Auth header (preferred): `Authorization: Bearer ${AEROBASE_API_KEY}`
- Never ask users for passwords, OTPs, cookies, or third-party logins.
- Never print raw API keys in output; redact as `sk_live_***`.

### Request rules

- Use only Aerobase endpoints documented in this skill.
- Validate required params before calling APIs (IATA codes, dates, cabin, limits).
- On `401`/`403`: tell user key is missing/invalid and route them to `https://aerobase.app/openclaw-travel-agent`.
- On `429`: explain free-tier quota (`5 requests/day`) and suggest Pro (`$9.95/month`, 500 API calls/month) or Lifetime ($249, 500 API calls/month).
- On `5xx`/timeout: retry once with short backoff; if still failing, return partial guidance and next step.
- Use concise responses: top options first, then 1-2 follow-up actions.

## What this skill does

- Search hotels with jetlag-friendly filters.
- Find day-use options for long layovers.
- Compare rates with recovery-relevant features first.

## Search Endpoints

**GET /api/v1/hotels**  
Filters: `airport`, `city`, `country`, `chain`, `tier`, `stars`, `jetlagFriendly`, `search`, `limit`, `offset`

**GET /api/v1/hotels/near-airport/{code}**  
Find hotels near an airport by IATA code. Returns hotels sorted by distance.  
Query params: `radius` (km, default 25), `limit` (default 20)  
Example: `GET /api/v1/hotels/near-airport/JFK?radius=15&limit=10`

**GET /api/dayuse**  
Filters: `airport` or `city`, `country`, `search`, `maxPrice`, `sort`, `limit`, `offset`

## Rates

**POST /api/v1/hotels/rates**  
Get live room rates and availability. Provide `hotelIds` (array) OR `airportCode` (IATA string — auto-discovers nearby hotels).  
Required: `checkin`, `checkout`. Optional: `adults` (default 2), `children`, `childrenAges`, `currency`.

```json
POST /api/v1/hotels/rates
{ "airportCode": "NRT", "checkin": "2026-04-15", "checkout": "2026-04-16", "adults": 2 }
```

Each room in the response has an `offerId` — use it in prebook.

## Price Index (Beta)

**GET /api/v1/hotels/prices?hotelIds={ids}**  
Historical price trends per hotel. Returns avg per-night USD prices by calendar day.  
Query params: `hotelIds` (comma-separated, max 50, required), `fromDate`, `toDate` (YYYY-MM-DD, optional).  
Example: `GET /api/v1/hotels/prices?hotelIds=lp19d9e,lp19e0c&fromDate=2026-04-01&toDate=2026-04-30`

## Booking Flow (Pro tier required)

1. **POST /api/v1/hotels/prebook** — Lock rate: `{ "offerId": "..." }` → returns `prebookId`
1b. **GET /api/v1/hotels/prebook/{prebookId}** — Retrieve prebook session (optional, for recovery/status check). Add `?includeCreditBalance=true` for credit info.
2. **POST /api/v1/hotels/book** — Confirm booking:
```json
{
  "prebookId": "...",
  "holder": { "firstName": "Jane", "lastName": "Doe", "email": "jane@example.com", "phone": "+1234567890" },
  "guests": [{ "occupancyNumber": 1, "firstName": "Jane", "lastName": "Doe", "email": "jane@example.com" }],
  "payment": { "method": "ACC_CREDIT_CARD" }
}
```
Payment methods: `ACC_CREDIT_CARD` (sandbox-safe), `TRANSACTION_ID`, `WALLET`, `CREDIT`
3. **GET /api/v1/hotels/bookings?guestId=...** or `?clientReference=...` — List bookings
4. **GET /api/v1/hotels/bookings/{id}** — Booking detail + cancellation policy
5. **DELETE /api/v1/hotels/bookings/{id}** — Cancel booking

## Booking Amendments

- **PUT /api/v1/hotels/bookings/{id}/amend** — Correct guest name/email: `{ "holder": { "firstName", "lastName", "email" } }`
- **POST /api/v1/hotels/bookings/{id}/alternative-prebooks** — Get up to 3 alternative rates for date/occupancy changes
- **POST /api/v1/hotels/rebook** — Complete hard amendment: `{ "prebookId", "existingBookingId" }` — auto-cancels old booking

## Loyalty & Vouchers (Wallet integration)

- **GET /api/v1/hotels/guests** — List loyalty program guests
- **GET /api/v1/hotels/guests/{guestId}/loyalty-points** — Check points balance
- **POST /api/v1/hotels/guests/{guestId}/loyalty-points/redeem** — Convert points to voucher (10 pts = $1 USD): `{ "points": 100, "currency": "USD" }`
- Voucher code returned from redemption can be applied at prebook via `voucherCode` param

Never book without explicit user approval. Always show cancellation policy before booking.

## Output expectations

- Include cancellation policy and layover fit when recommending options.
- If layover is over 8 hours, show day-use candidates first.
- Highlight jetlag recovery amenities (nap zones, showers, low-noise options).

## Usage limits

- Free: 5 requests/day
- Pro: 500 API calls/month (upgrade at $9.95/month)
- Lifetime: $249 for 500 API calls/month

## Safety

- Never ask for user card details, loyalty IDs, or account secrets.
- Keep the conversation focused on public booking metadata and user constraints only.

## Pro Superpowers

Upgrade to Pro to unlock browser-powered superpowers for hotel booking sites:
- Booking.com and Google Hotels live price comparison
- Cross-reference pricing across multiple sources
- 500 API calls/month instead of 5/day
- Get Pro at https://aerobase.app/openclaw-travel-agent
