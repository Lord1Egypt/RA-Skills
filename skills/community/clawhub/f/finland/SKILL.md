---
name: Finland
slug: finland
version: 1.0.0
homepage: https://clawic.com/skills/finland
changelog: "Initial release with verified Finland entry rules, seasonal routing, and practical travel logistics."
description: Plan Finland trips with verified entry rules, season-aware routing, rail-and-Lapland logistics, and practical tourist safety.
metadata: {"clawdbot":{"emoji":"🇫🇮","requires":{"bins":[],"config":["~/finland/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/finland/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Finland trip and needs operational guidance beyond generic Nordic inspiration: Schengen entry checks, Helsinki vs Lapland route choice, rail-flight-car tradeoffs, winter or summer season fit, cost reality, and on-the-ground execution.

## Architecture

Memory lives in `~/finland/`. If `~/finland/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/finland/
└── memory.md     # Trip context, route logic, and evolving constraints
```

## Quick Reference

Use this map to load only the Finland subtopic that changes the decision in front of you.

| Topic | File |
|-------|------|
| **Entry and Compliance** | |
| Schengen stays, visas, EES/ETIAS watchouts | `entry-and-documents.md` |
| Customs, food, cash, alcohol, border realities | `customs-and-border.md` |
| **Planning Backbone** | |
| Macro-regions and route logic | `regions.md` |
| Sample itineraries for 4-14 days | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Budget framing and hidden costs | `budget-and-costs.md` |
| Cards, cash, tax-free, tipping | `payments-and-tax-free.md` |
| **Transport and Outdoors** | |
| Flights, trains, buses, ferries, airport moves | `transport-domestic.md` |
| Self-drive, winter roads, parking, licenses | `road-trips-and-driving.md` |
| Parks, cabins, trails, and outdoors logic | `nature-and-national-parks.md` |
| **Major Regions and Bases** | |
| Helsinki and capital-region base strategy | `helsinki-and-capital-region.md` |
| Lapland route logic and winter fit | `lapland.md` |
| Lakeland and Tampere balance | `lakeland-and-tampere.md` |
| Turku and the archipelago | `turku-and-archipelago.md` |
| **Lifestyle and Execution** | |
| Food strategy and local specialties | `food-guide.md` |
| Sauna etiquette, social rhythm, and culture | `sauna-and-culture.md` |
| Nightlife by city style and season | `nightlife.md` |
| Traveling with children or mixed ages | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Emergencies, alerts, and outdoor risk | `safety-and-emergencies.md` |
| Climate, aurora, darkness, and daylight logic | `weather-and-seasonality.md` |
| Connectivity, apps, tickets, and payments | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Season and Daylight, Not by the Map
Finland is manageable only when the month is fixed first. July city-hopping, September foliage, January aurora, and March family snow trips are different products, not interchangeable versions of the same route.

### 2. Confirm Entry and Border Friction Before Non-Refundables
Before locking flights, cabins, or night trains, use `entry-and-documents.md` and `customs-and-border.md` to confirm Schengen stay rules, visa pathway, passport validity, evolving EES/ETIAS requirements, and any overland border assumptions.

### 3. One Main Corridor Wins Most Trips
For short trips, choose one primary Finland logic:
- Helsinki and the south for city, design, food, and easy transit
- Lapland for aurora, snow, and winter activities
- Lakeland or archipelago for slower summer nature

### 4. Always Offer Two Transport Models
For any route beyond Helsinki, provide at least two workable patterns:
- Rail or flight heavy: lower winter-driving risk, more timetable dependence
- Self-drive or bus-heavy: more flexibility, more weather and fatigue exposure

### 5. Budget the Real Finland
Do not price from hotel headlines alone. Include airport transfers, sleeper-train supplements, winter clothing rental, sauna or spa costs, checked bags, cabin groceries, and restaurant or alcohol pricing.

### 6. Never Sell Aurora or Winter Fantasy as Guaranteed
Aurora is probability management, not certainty. Snow conditions, cloud cover, daylight hours, and school-holiday crowds change what is smart, especially in Lapland.

### 7. Deliver Operational Plans
Output should include:
- Best base or base pair
- Day-by-day flow with realistic transfer windows
- Booking deadlines or sellout risks
- Weather downgrade options
- Safety and emergency quick notes

## Common Traps

- Treating Helsinki and Lapland as a casual add-on in a very short trip.
- Assuming winter is romantic by default without checking darkness, cold tolerance, and clothing strategy.
- Choosing a rental car before checking whether train, bus, or one guided base solves the trip better.
- Thinking summer midnight sun means infinite energy and no pacing consequences.
- Building archipelago or lake trips without checking ferry frequency and shoulder-season reductions.
- Carrying a U.S.-style tipping mindset into a mostly service-included culture.
- Promising border, visa, or EES/ETIAS details from memory instead of verifying current rules.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/finland/`

**This skill does NOT:** Access files outside `~/finland/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `booking` — Reservation workflows and confirmation hygiene
- `car-rental` — Better self-drive strategy and handoff logistics
- `food` — Deeper restaurant and cuisine planning
- `english` — Language support for bookings, menus, and practical interactions

## Feedback

- If useful: `clawhub star finland`
- Stay updated: `clawhub sync`
