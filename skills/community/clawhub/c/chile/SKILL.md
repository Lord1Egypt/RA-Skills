---
name: Chile
slug: chile
version: 1.0.0
homepage: https://clawic.com/skills/chile
changelog: "Initial release with verified Chile entry rules, macro-region routing, and practical travel logistics from desert to Patagonia."
description: Plan Chile trips with macro-region triage, verified entry rules, long-distance logistics, and practical safety for cities, desert, lakes, and Patagonia.
metadata: {"clawdbot":{"emoji":"🇨🇱","requires":{"bins":[],"config":["~/chile/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/chile/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Chile trip and needs more than generic sightseeing advice: which macro-region to choose, how to route huge distances, what to reserve early, and how to handle entry, SAG declaration, weather, transport, and safety on the ground.

## Architecture

Memory lives in `~/chile/`. See `memory-template.md` for structure.

```
~/chile/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

Use this map to load only the Chile subtopic that changes the decision in front of you.

| Topic | File |
|-------|------|
| **Entry and Compliance** | |
| Entry pathway, tourist stay, Rapa Nui rules | `entry-and-documents.md` |
| SAG declaration, customs, restricted items | `customs-and-biosecurity.md` |
| **Planning Backbone** | |
| Macro-regions and route logic | `regions.md` |
| Sample itineraries (5-21 days) | `itineraries.md` |
| Domestic flights, buses, airport moves | `transport-domestic.md` |
| Self-drive and road-trip reality | `road-trips-and-driving.md` |
| National parks, reservations, permits | `national-parks.md` |
| Climate and seasonality | `weather-and-seasonality.md` |
| Budget, cards, cash, and tipping | `budget-and-payments.md` |
| Apps, eSIM, and connectivity | `telecoms-and-apps.md` |
| **Major Regions and Bases** | |
| Santiago and central base strategy | `santiago.md` |
| Valparaiso and Vina del Mar strategy | `valparaiso-and-vina.md` |
| San Pedro de Atacama and the north | `atacama.md` |
| Puerto Varas, Chiloe, and the lake district | `lake-district-and-chiloe.md` |
| Puerto Natales, Punta Arenas, and Torres | `patagonia-and-torres-del-paine.md` |
| Aysen and Carretera Austral | `carretera-austral-and-aysen.md` |
| Rapa Nui entry and visit design | `rapa-nui.md` |
| **Lifestyle and Execution** | |
| Food, markets, seafood, and wine | `food-and-wine.md` |
| Nightlife and evening strategy | `nightlife.md` |
| Traveling with children | `family-travel.md` |
| Accessibility planning | `accessibility.md` |
| **Safety and Verification** | |
| Emergencies, protests, earthquakes, alerts | `safety-and-emergencies.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Latitude, Not by FOMO
Chile is long, transfer-heavy, and season-sensitive. For short trips, lock one macro-region plus Santiago/central coast at most.

### 2. Solve Entry and SAG First
Before building routes, confirm the traveler's entry pathway in `entry-and-documents.md` and declaration obligations in `customs-and-biosecurity.md`. Chile is strict about undeclared animal and plant products.

### 3. Treat Atacama Altitude and Patagonia Weather as Trip-Shaping
Use `atacama.md`, `patagonia-and-torres-del-paine.md`, and `weather-and-seasonality.md` before promising ambitious days. Altitude, wind, rain, park closures, and ferry timing can break a pretty itinerary.

### 4. Always Offer Two Logistics Models
For each plan provide:
- A faster flight-heavy version
- A slower bus/road-heavy version

Explain the tradeoff in cost, scenery, fatigue, reservation pressure, and weather resilience.

### 5. Price the Full Chain, Not the Headline Fare
Budget using complete Chile trip math: domestic flights, Calama/Puerto Natales transfers, park tickets, refugios or tours, baggage, tolls, and card-vs-cash friction in smaller towns.

### 6. Flag Incompatible Combos Early
Call out mistakes before the user books:
- Atacama plus Torres del Paine in a short trip
- Carretera Austral in bad season without slack
- Rapa Nui planned without the extra entry requirements
- Dense city stays in Valparaiso hill areas without mobility review

### 7. Deliver Operational Plans
Output should include:
- Best base or base pair
- Day-by-day flow with transfer windows
- Reservation deadlines and risk points
- Weather and altitude notes
- Backup plan for delays, strikes, or closures

## Common Traps

- Treating Chile like a compact destination instead of a north-south corridor.
- Trying to do Atacama, lakes, and Patagonia in one short trip.
- Ignoring Calama, Puerto Natales, and ferry transfer overhead.
- Arriving to San Pedro and doing the highest-altitude day immediately.
- Leaving Torres del Paine reservations until the last minute in high season.
- Assuming cards, signal, and transport frequency are equally easy everywhere.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/chile/`

**This skill does NOT:** Access files outside `~/chile/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `booking` — Reservation workflows and confirmation hygiene
- `car-rental` — Better self-drive strategy and handoff logistics
- `food` — Deeper restaurant and cuisine planning
- `spanish` — Language support for bookings, menus, and practical interactions

## Feedback

- If useful: `clawhub star chile`
- Stay updated: `clawhub sync`
