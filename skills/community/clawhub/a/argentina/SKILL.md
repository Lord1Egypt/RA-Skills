---
name: Argentina
slug: argentina
version: 1.0.0
homepage: https://clawic.com/skills/argentina
changelog: "Initial release with verified Argentina entry rules, regional route playbooks, money strategy, and practical travel logistics."
description: Plan Argentina trips with region-specific routing, money strategy, seasonal timing, and practical travel logistics.
metadata: {"clawdbot":{"emoji":"🇦🇷","requires":{"bins":[],"config":["~/argentina/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/argentina/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning an Argentina trip and needs practical guidance beyond generic inspiration: entry rules, money and payments, region choice, flight and road logic, park access, safety, and day-to-day execution.

## Architecture

Memory lives in `~/argentina/`. See `memory-template.md` for structure.

```
~/argentina/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

Use this map to jump into the right decision module before building the route.

| Topic | File |
|-------|------|
| **Entry, Border, and Money** | |
| Tourist entry, visa, stays, paperwork | `entry-and-documents.md` |
| Customs, cash limits, food, tax-free notes | `customs-and-border.md` |
| Cash, cards, exchange logic, VAT, tips | `money-payments-and-exchange.md` |
| **Planning Backbone** | |
| Region selection and route architecture | `regions.md` |
| Sample itineraries for 7-21 days | `itineraries.md` |
| Accommodation strategy by trip style | `accommodation.md` |
| Budget framing and cost traps | `budget-and-costs.md` |
| **Transport and Nature** | |
| Flights, buses, trains, airport buffers | `transport-domestic.md` |
| Self-drive, mountain roads, border paperwork | `road-trips-and-driving.md` |
| Parks, permits, tickets, outdoor logistics | `national-parks-and-nature.md` |
| Neighbor-country side trips and border hops | `border-hops-and-neighbor-countries.md` |
| **Major Regions and Cities** | |
| Buenos Aires playbook | `buenos-aires.md` |
| Mendoza and wine country playbook | `mendoza-and-wine-country.md` |
| Iguazu and Misiones playbook | `iguazu-and-misiones.md` |
| Patagonia Lakes playbook | `patagonia-lakes.md` |
| South Patagonia playbook | `patagonia-south.md` |
| Ushuaia and Tierra del Fuego playbook | `ushuaia-and-tierra-del-fuego.md` |
| Salta and Jujuy playbook | `salta-and-jujuy.md` |
| Peninsula Valdes and Puerto Madryn playbook | `peninsula-valdes-and-puerto-madryn.md` |
| Cordoba and central Argentina playbook | `cordoba-and-central-argentina.md` |
| Atlantic coast and Mar del Plata playbook | `atlantic-coast-and-mar-del-plata.md` |
| **Lifestyle and Execution** | |
| Food strategy by region and timing | `food-guide.md` |
| Nightlife by city type | `nightlife.md` |
| Traveling with children or mixed ages | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Emergencies, theft, weather alerts, disruptions | `safety-and-emergencies.md` |
| Climate and seasonality planning | `weather-and-seasonality.md` |
| Connectivity, transport cards, helpful apps | `telecoms-and-apps.md` |
| Research sources map | `sources.md` |

## Core Rules

### 1. Route by Macro-Region, Not by Map Fantasy
For short trips, pick one anchor cluster and one contrast region at most. Argentina is long enough that "just add Iguazu or Patagonia" can destroy the experience.

### 2. Lock Entry and Money Before Non-Refundables
Before buying flights, confirm the correct entry path, the length of stay, border-hop implications, and the payment strategy for cards, cash, and park tickets.

### 3. Ask for Month First
Argentina changes dramatically by season. Patagonia, Iguazu, Mendoza, and the northwest should never be planned with one generic weather assumption.

### 4. Treat Patagonia as Multiple Trips
Lake District, South Patagonia, and Ushuaia are different products with different transport and weather logic. Do not merge them casually.

### 5. Always Offer Two Transport Models
For each route, give at least two practical options with tradeoffs:
- Flight-heavy: faster, fewer overnight transfers, more airport friction
- Road/bus-heavy: slower, more scenery, more fatigue and weather sensitivity

### 6. Budget with Friction, Not Headlines
Argentina trip quality often depends more on transfer costs, excursion timing, airport changes, and card/cash execution than on the hotel sticker price.

### 7. Deliver Action Plans
Output should include:
- Base-city strategy
- Day-by-day flow with transfer buffers
- Booking deadlines or low-inventory warnings
- Weather fallback or alternate plan
- Safety, payment, and emergency notes

## Common Traps

- Buenos Aires + Mendoza + Iguazu + Patagonia in one short trip.
- Assuming Patagonia is one interchangeable region.
- Planning with old exchange-rate blog posts instead of current official references.
- Ignoring cross-border implications when adding the Brazilian side of Iguazu or Chile crossings.
- Using overnight buses or same-day airport changes without buffer.
- Choosing accommodation by nightly rate only and losing hours to transfers.
- Treating national park access as fully spontaneous in peak season.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/argentina/`

**This skill does NOT:** Access files outside `~/argentina/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `car-rental` — Better rental strategy and handoff logistics
- `booking` — Reservation workflows and confirmation hygiene
- `food` — Deeper restaurant and cuisine recommendations
- `spanish` — Language support for bookings, transport, and service interactions

## Feedback

- If useful: `clawhub star argentina`
- Stay updated: `clawhub sync`
