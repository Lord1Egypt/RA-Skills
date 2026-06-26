---
name: Germany
slug: germany
version: 1.0.0
homepage: https://clawic.com/skills/germany
changelog: "Initial release with verified Germany entry rules, rail-vs-car planning, regional playbooks, and practical travel logistics."
description: Plan Germany trips with region-specific routing, rail-vs-car strategy, verified entry rules, and practical travel logistics.
metadata: {"clawdbot":{"emoji":"🇩🇪","requires":{"bins":[],"config":["~/germany/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/germany/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Germany trip and needs practical guidance beyond generic inspiration: Schengen entry checks, rail versus car decisions, region choice, seasonal tradeoffs, budgeting, and on-the-ground execution.

## Architecture

Memory lives in `~/germany/`. See `memory-template.md` for structure.

```
~/germany/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

Use this map to jump into the right decision module before building the route.

| Topic | File |
|-------|------|
| **Entry, Border, and Core Planning** | |
| Schengen, passport, visas, current border systems | `entry-and-documents.md` |
| Customs, allowances, restricted items, cash rules | `customs-and-border.md` |
| Region selection and route architecture | `regions.md` |
| Sample itineraries for 5-21 days | `itineraries.md` |
| Accommodation strategy by trip style | `accommodation.md` |
| Budget framing and cost traps | `budget-and-costs.md` |
| Cards, cash, tips, and payment friction | `payments-and-tipping.md` |
| **Transport and Movement** | |
| ICE, regional rail, airports, local transit | `transport-domestic.md` |
| Scenic driving, rental cars, low-emission zones | `road-trips-and-driving.md` |
| **Major Regions and Cities** | |
| Berlin playbook | `berlin.md` |
| Munich and Upper Bavaria playbook | `munich-and-upper-bavaria.md` |
| Franconia and Romantic Road playbook | `franconia-and-romantic-road.md` |
| Rhine, Moselle, Cologne, and west playbook | `rhine-moselle-and-west.md` |
| Hamburg and the north playbook | `hamburg-and-north.md` |
| Black Forest and southwest playbook | `black-forest-and-southwest.md` |
| Saxony and east playbook | `saxony-and-east.md` |
| **Lifestyle and Execution** | |
| Food strategy by region and timing | `food-guide.md` |
| Beer halls, wine regions, and drinking context | `beer-and-wine-regions.md` |
| Nightlife by city type | `nightlife.md` |
| Culture, etiquette, Sundays, and quiet hours | `culture-and-etiquette.md` |
| Traveling with children or mixed ages | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Christmas markets and major festival logic | `christmas-markets-and-festivals.md` |
| **Conditions and Tools** | |
| Emergencies, protests, weather alerts, disruptions | `safety-and-emergencies.md` |
| Climate and seasonality planning | `weather-and-seasonality.md` |
| Connectivity, rail apps, transport cards, useful tools | `telecoms-and-apps.md` |
| Research source map | `sources.md` |

## Core Rules

### 1. Route by Cluster, Not by Checkbox
For short trips, keep one anchor cluster per week: Berlin and nearby east, Bavaria, Rhine-west, or north Germany. Germany is efficient, but transfer churn still destroys trip quality.

### 2. Confirm Entry and Border Friction Before Booking
Use `entry-and-documents.md` first: Schengen stay limits, passport validity, visa pathway when relevant, and the current EES or ETIAS status before locking non-refundable plans.

### 3. Decide Rail vs Car Early
Germany works differently depending on route shape:
- Rail-first for Berlin, Hamburg, Munich, Cologne, and most intercity hops
- Car-first for the Black Forest, Alpine villages, Romantic Road detours, and some wine-country loops

### 4. Make Every Plan Season-Aware
Use `weather-and-seasonality.md` before promising Christmas markets, lake swimming, Alpine road loops, or shoulder-season castle routes. Winter closures, summer crowds, and shoulder weather matter.

### 5. Budget for Full Germany Math
Price the real trip, not the hotel headline:
- Rail reservations and local transit add-ons
- City tax, parking, and low-emission-zone friction
- Breakfast value versus station-area markups
- Cash-only or card-friction exposure in smaller venues

### 6. Protect Sundays, Holidays, and Event Windows
Germany rewards timing discipline. Sunday closures, trade-fair demand, Oktoberfest pressure, and Christmas market crowd waves can reshape where users should stay and when they should move.

### 7. Deliver Operational Plans
Output should include:
- Base-city strategy
- Day-by-day flow with transfer buffers
- Reservation deadlines or event-pressure warnings
- Rail and car alternative when relevant
- Safety, payment, and emergency quick notes

## Common Traps

- Treating Germany as a frictionless "add one more city" country.
- Using a car by default for Berlin, Munich, Hamburg, or Cologne city stays.
- Assuming every restaurant, kiosk, or market stall is card-friendly.
- Planning Sunday arrival with no food, pharmacy, or grocery strategy.
- Trying to combine Berlin, Bavaria, Rhine castles, and the Alps in one short trip.
- Treating Christmas markets, Oktoberfest, and major fair dates as normal-demand periods.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/germany/`

**This skill does NOT:** Access files outside `~/germany/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `booking` — Reservation workflows and confirmation hygiene
- `car-rental` — Better rental strategy and handoff logistics
- `food` — Deeper restaurant and cuisine recommendations
- `german` — Language support for bookings, transport, and service interactions

## Feedback

- If useful: `clawhub star germany`
- Stay updated: `clawhub sync`
