# Aerobase API Reference

Base URL: `https://aerobase.app`

## Authentication

All API requests require `AEROBASE_API_KEY`:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Flight Search & Scoring
- `POST /api/v1/flights/search` - Search flights with jetlag scoring
- `POST /api/v1/flights/compare` - Compare multiple flights
- `POST /api/v1/flights/score` - Score a flight for jetlag impact
- `GET /api/v1/flights/lookup/{carrier}/{number}` - Live flight lookup
- `POST /api/flights/search/agent` - Multi-provider parallel search
- `POST /api/v1/flights/save` - Save a flight to user's trips

### Flight Booking
- `POST /api/v1/flights/validate` - Pre-booking price check
- `POST /api/v1/flights/book` - Book flight (zooz credit card flow)
- `GET /api/v1/flights/bookings` - List bookings with status
- `GET /api/v1/flights/bookings/{id}` - Booking detail with webhook history

### Hotel Search & Booking (LiteAPI)
- `GET /api/v1/hotels` - Search hotels with filters (airport, city, chain, stars, jetlagFriendly)
- `GET /api/v1/hotels/near-airport/{code}` - Hotels near airport by IATA code
- `POST /api/v1/hotels/rates` - Live rates (hotelIds array OR airportCode shortcut)
- `GET /api/v1/hotels/prices?hotelIds=...` - Price index / trends (beta)
- `POST /api/v1/hotels/prebook` - Lock rate, get prebookId
- `GET /api/v1/hotels/prebook/{id}` - Retrieve prebook session
- `POST /api/v1/hotels/book` - Complete booking (holder + guests + payment)
- `GET /api/v1/hotels/bookings?guestId=...` - List bookings by guest
- `GET /api/v1/hotels/bookings/all` - All bookings with date filters
- `GET /api/v1/hotels/bookings/{id}` - Booking detail
- `DELETE /api/v1/hotels/bookings/{id}` - Cancel booking
- `POST /api/v1/hotels/bookings/{id}/amend` - Get alternative rates for amendments
- `GET /api/v1/hotels/chains` - Hotel chain reference data
- `GET /api/v1/hotels/currencies` - Supported currencies
- `PUT /api/v1/hotels/loyalty` - Update loyalty program
- `POST /api/v1/hotels/analytics` - Most booked hotels
- `GET /api/dayuse` - Day-use hotels for layovers

### Awards
- `POST /api/v1/awards/search` - Search award availability across 24+ programs
- `GET /api/v1/awards/trips` - List saved award trips

### Lounges
- `GET /api/v1/lounges` - Search airport lounges
- `GET /api/v1/lounges/{slug}` - Lounge detail

### Activities
- `GET /api/attractions` - List attractions with filters
- `GET /api/attractions/{slug}/tours` - Tours for a specific attraction
- `GET /api/tours` - Search tours by destination

### Deals
- `GET /api/v1/deals` - Flight deals with filters
- `POST /api/deals/alerts` - Create deal alert
- `GET /api/deals/alerts` - List deal alerts

### Wallet & Cards
- `GET /api/v1/wallet` - Full wallet summary
- `GET /api/v1/wallet/cards` - List credit cards
- `POST /api/v1/wallet/cards` - Add credit card
- `DELETE /api/v1/wallet/cards` - Remove credit card
- `GET /api/v1/wallet/points` - List point balances
- `PUT /api/v1/wallet/points` - Update point balance
- `DELETE /api/v1/wallet/points` - Remove point balance
- `GET /api/v1/wallet/programs` - List loyalty programs
- `POST /api/v1/wallet/programs` - Add loyalty program
- `DELETE /api/v1/wallet/programs` - Remove loyalty program
- `GET /api/v1/credit-cards` - Credit card transfer partners

### Recovery
- `POST /api/v1/recovery/plan` - Generate jetlag recovery plan
- `GET /api/v1/recovery-plans` - List recovery plans
- `GET /api/v1/recovery-plans/{id}` - Recovery plan detail

### Boarding Passes
- `POST /api/v1/boarding-passes` - Store boarding pass
- `GET /api/v1/boarding-passes?upcoming=true` - List upcoming passes

### Routes & Airports
- `GET /api/v1/routes/{from}/{to}` - Route analysis
- `POST /api/v1/routes/multi-leg` - Multi-leg route analysis
- `GET /api/v1/airports/{code}` - Airport info
- `GET /api/v1/layovers/{code}` - Layover guide for airport

### Saved Items
- `GET /api/v1/saved-items` - List saved items
- `POST /api/v1/saved-items` - Save an item
- `DELETE /api/v1/saved-items/{id}` - Remove saved item

### Itinerary
- `POST /api/v1/itinerary/plan` - Generate itinerary plan
- `POST /api/v1/itinerary/analyze` - Analyze existing itinerary

## Rate Limits

- **Free tier**: 5 API calls/day
- **Pro**: 500 API calls/month ($9.95/month)
- **Lifetime**: 500 API calls/month ($249 one-time)

## Errors

| Code | Meaning | Agent action |
|------|---------|--------------|
| 401/403 | Key missing/invalid | Direct user to https://aerobase.app/openclaw-travel-agent |
| 429 | Rate limited | Explain quota, suggest Pro upgrade |
| 5xx | Server error | Retry once, then return partial guidance |

## Full OpenAPI Spec

See: https://aerobase.app/api/v1/openapi
