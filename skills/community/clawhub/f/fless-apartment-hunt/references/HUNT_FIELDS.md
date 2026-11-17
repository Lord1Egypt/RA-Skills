# Hunt fields: exact rules

The hunt brief is validated server-side by Fless before a link is created.
This is the exact contract (source: `https://fless.io/hunt-how-to.md` +
`HuntCreate` schema at `https://fless.io/api/v1/openapi.json`).

## Required for a complete brief

| Field | Type | Rules |
|---|---|---|
| `city_id` | integer | Must be a LIVE city. Live cities: `GET https://fless.io/api/v1/cities/listing` (coming-soon cities are waitlist-only → error COMING_SOON_CITY). |
| `min_price` | number | Monthly USD, ≥ 0 |
| `max_price` | number | Monthly USD, must be > min_price (else PRICE_RANGE_INVALID) |
| `bedrooms` | string | One of: `"0"` (Studio), `"1"`, `"2"`, `"3"`, `"4"`, `"4+"` (4-or-more), `"studio"`. Matching is set-intersection with building options; Studio = 0. |
| `move_in_date` | string | `YYYY-MM-DD`, strictly in the future (else INVALID_MOVE_IN_DATE_PAST) |
| `proximity_criteria` | array | 1+ POIs the hunt centers on: `{name, address?, latitude, longitude, category?, max_distance}`; `max_distance` in miles, 0.1 to 10, default 0.2. Find POIs: `GET https://fless.io/api/v1/map/search?query=...&lat=...&lng=...&radius=...` |

## Optional fields

| Field | Notes |
|---|---|
| `name` | Free text; defaults to `Hunt - {City}` when omitted |
| `amenities` | Dict `{amenity_name: true}`; canonical keys below; unknown keys are auto-normalized when a synonym matches (e.g. `"gym"` → `"Fitness Center"`), flagged in `issues` |
| `additional_questions` | Free-text questions answered per building (3 free per hunt); the right place for pet-breed, parking-cost, income-limit questions |
| `tour_preference` | Subset of: `"Guided"`, `"Self-guided"`, `"Virtual"` |
| `policies` | Dict; rarely needed, prefer `additional_questions` |

## Canonical amenity keys (57)

Use these exact keys (substring matching applies, e.g. "Pool" matches
"Swimming Pool", but "Gym" does NOT match "Fitness Center"):

24/7 Security, Air Conditioning, Balcony/Patio, BBQ/Picnic Area, Bike Repair
Station, Bike Storage, Billiards Table, Business Center, Car Wash Bay,
Ceiling Fans, Clubhouse/Community Room, Coffee Bar, Community WiFi, Concierge,
Controlled Access Entry, Co-Working Spaces, Doorman, Dry Cleaning Service,
Elevator, EV Charging Stations, Fiber Optic Internet, Fire Pit, Fitness
Center, Game Room, Guest Parking, Guest Suites, Hardwood Floors, In-unit
Fireplace, Intercom System, Keyless Entry, Laundry (In-Unit), Laundry
(On-Site), On-Site Management, On-Site Maintenance, Outdoor Kitchen, Outdoor
Lounge, Package Lockers, Package Receiving, Parking Garage, Parking (Outdoor),
Pet-Friendly Policies, Pet Park, Pet Spa, Playground, Resident Lounge,
Rooftop Deck, Sauna, Security Cameras, Shuttle Service, Smart Home Features,
Storage Unit, Swimming Pool, Theater Room, Utilities Included, Walk-In
Closets, Window Coverings, Yoga Studio

Common safe synonyms that auto-normalize: gym → Fitness Center, pool →
Swimming Pool, dog park → Pet Park, in-unit laundry → Laundry (In-Unit).

## Binary restrictions: ask before building the link

Some criteria disqualify buildings outright. If any apply, make them part of
the brief (in `amenities`/`additional_questions`):

- **Age-qualified housing (55+/62+)**: excludes under-threshold residents.
  Ask: "Will every household member be 55+?" If no, add a question ruling out
  age-qualified communities; if yes and desired, say so explicitly.
- **Pets**: dogs/cats are commonly rejected or restricted by breed/weight
  (service animals exempt). Ask for animal type, breed, weight.
- **Smoking**: many buildings are entirely smoke-free.
- **Income limits**: some buildings are income-restricted (e.g. 80% AMI);
  surface as a question if budget is near the limit for the area.

## Credit pricing (state factually when asked)

New users get a 15 day free trial (unlimited hunts, no credit card). After
the trial: 30 credits included, hunts cost 5.

After your trial, per-item costs:

- First hunt free; signup grants 25 credits + 5/month; a hunt costs 5 credits.
- 5 building outreach emails per hunt free, extras 1 credit.
- Optional upgrades at creation: advanced matching (3), premium matching (5).
- Credits: $20/200, $40/450, $80/950, purchased by the human in the web app only.

## Error codes

`CITY_NOT_FOUND` · `COMING_SOON_CITY` · `INVALID_MOVE_IN_DATE_PAST` ·
`PRICE_RANGE_INVALID` · `INVALID_REQUEST` (bad enum/format; message names the
field) · `MISSING_FIELDS` · `RATE_LIMITED` (honor Retry-After) ·
`LINK_EXPIRED` (rebuild the link).
