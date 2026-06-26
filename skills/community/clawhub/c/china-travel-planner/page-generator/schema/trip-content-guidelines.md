# Trip Content Guidelines

Use this guide when generating structured trip content for the travel-page-framework.

## Goal

Produce travel output in two layers:

1. **Human-readable plan** for direct chat replies
2. **Structured page data** for rendering in a reusable web template

The structured layer should follow `schema/trip-schema.json`.

## Writing principles

- Prefer reusable fields over custom one-off paragraphs.
- Put destination-specific wording in JSON values, not in the page template.
- Keep each card focused on one job.
- Use short, concrete text that still reads naturally on a card.
- Avoid long essay paragraphs inside cards.

## Recommended output flow

When planning a trip, think in this order:

1. constraints
2. itinerary logic
3. hotel logic
4. transport / metro / rail logic
5. attraction shortlist
6. practical reminders
7. structured JSON population

## Section rules

### meta
- `title`: full page title
- `subtitle`: compact trip summary
- `description`: search/share summary

### hero
- keep summary under 90 Chinese characters when possible
- tags should be short and scannable

### stats
- use concise dashboard-style values
- avoid full sentences

### hotels
Each hotel card should answer:
- why this phase
- why this area
- why this hotel / option

`highlights` should be short bullets, not prose paragraphs.

### metroCoverage
Use for:
- line coverage goals
- route constraints
- day allocation for lines

### days
Each day should have:
- a clear theme
- realistic morning/afternoon/evening chunks
- explicit city target
- explicit metro line list if relevant
- a short operational note

### sideTrips
Use for nearby cities or side destinations.
The `role` field should explain why the side trip exists in the overall plan.

### attractions
Attraction cards should be short and web-friendly.
Recommended fields:
- why it matters
- where it fits in the itinerary
- what kind of traveler it suits

### tips
Use short operational reminders.
Avoid generic travel advice unless directly relevant.

## Reusability rules

### Do
- keep dates, hotels, attractions, and route logic in JSON
- keep card field names stable across destinations
- keep component structure destination-agnostic

### Don't
- hardcode Changsha-specific wording into reusable templates
- embed giant HTML blobs inside JSON
- mix presentation class names into data fields

## Suggested future extensions

Potential fields that can be added later without breaking the core schema:
- `budget`
- `food`
- `transport`
- `mapLinks`
- `bookingLinks`
- `gallery`
- `status` for completed/live trip tracking
