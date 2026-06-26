---
name: Austria
slug: austria
version: 1.0.0
homepage: https://clawic.com/skills/austria
changelog: "Initial release with verified Austria entry rules, rail-first routing, alpine season planning, and practical regional playbooks."
description: Plan Austria trips with rail and road logic, alpine season timing, region-specific routing, and practical local execution.
metadata: {"clawdbot":{"emoji":"🇦🇹","requires":{"bins":[],"config":["~/austria/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/austria/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning an Austria trip and needs practical guidance beyond generic inspiration: entry rules, region choice, rail vs car tradeoffs, mountain timing, city sequencing, food and culture context, and on-the-ground execution.

## Architecture

Memory lives in `~/austria/`. See `memory-template.md` for structure.

```
~/austria/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

Use this map to choose the right decision module before building the route.

| Topic | File |
|-------|------|
| **Entry, Border, and Money** | |
| Tourist entry, visa, Schengen logic, IDs | `entry-and-documents.md` |
| Customs, cash, food restrictions, border habits | `customs-and-border.md` |
| Budget framing and hidden costs | `budget-and-costs.md` |
| Cards, cash, tipping, tax-free basics | `tipping-and-payments.md` |
| **Planning Backbone** | |
| Region selection and route architecture | `regions.md` |
| Sample itineraries for 4-14 days | `itineraries.md` |
| Accommodation strategy by trip style | `accommodation.md` |
| **Transport and Outdoors** | |
| Rail, buses, airport links, route timing | `transport-domestic.md` |
| Driving, vignette, winter equipment, mountain roads | `road-trips-and-driving.md` |
| Alpine, lake, hiking, hut, and cable-car logic | `alps-lakes-and-outdoors.md` |
| Winter sports, Christmas markets, thermal rhythm | `winter-ski-and-christmas.md` |
| Border hops and nearby add-ons | `border-hops-and-day-trips.md` |
| **Regions and Cities** | |
| Vienna playbook | `vienna.md` |
| Salzburg and Salzkammergut playbook | `salzburg-and-salzburgerland.md` |
| Innsbruck and Tyrol playbook | `innsbruck-and-tyrol.md` |
| Graz and Styria playbook | `graz-and-styria.md` |
| Carinthia and lake districts playbook | `carinthia-and-lakes.md` |
| Danube, Linz, and Wachau playbook | `danube-linz-and-wachau.md` |
| **Lifestyle and Execution** | |
| Food, coffeehouse, Heuriger, and meal rhythm | `food-guide.md` |
| Family pacing and mixed-age planning | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Emergencies, mountain risk, and disruption logic | `safety-and-emergencies.md` |
| Climate and seasonality planning | `weather-and-seasonality.md` |
| Connectivity, apps, roaming, and tickets | `telecoms-and-apps.md` |
| Research sources map | `sources.md` |

## Core Rules

### 1. Route by Corridor, Not by Province Count
Austria is compact enough for ambitious plans and mountainous enough to punish them. Anchor each trip around one rail corridor or one driving loop, then add only the contrast region that still preserves easy transfers.

### 2. Lock Entry and Season Before Reservations
Before itinerary work, confirm the correct entry path in `entry-and-documents.md`, then validate whether the user's month aligns with lakes, cities, alpine hiking, skiing, or Christmas-market demand.

### 3. Default to Rail Unless the Route Truly Needs a Car
Vienna, Salzburg, Linz, Graz, and Innsbruck link well by rail. Car value appears when the trip is built around lake districts, small alpine villages, scenic roads, or family gear that makes transfers costly.

### 4. Treat Mountains as Logistics, Not Background
Use `alps-lakes-and-outdoors.md`, `weather-and-seasonality.md`, and `winter-ski-and-christmas.md` before promising huts, panoramas, or ski days. Storms, snow line, cable-car closures, avalanche risk, and fog inversion can change the entire plan.

### 5. Austria Rewards Pace
Trip quality improves when users sleep multiple nights per base, book key trains and mountain hotels early, and leave daylight margins for weather, spa time, café rhythm, and scenic detours.

### 6. Budget With Real Friction
Price with actual Austria trip math: rail reservations, airport transfers, vignettes, tunnel tolls, parking in historic cores, mountain lift costs, ski rental, and higher peak-season hotel pressure in lake and alpine regions.

### 7. Deliver Operational Plans
Output should include:
- Base-city strategy
- Day-by-day flow with transfer windows
- Reservation deadlines and weather-sensitive items
- Rail-first and car-first variants when relevant
- Safety, payment, and emergency notes

## Common Traps

- Treating Austria like a quick checkbox between larger European stops.
- Combining Vienna, Salzburg, Hallstatt, Innsbruck, and multiple ski or lake regions in too few days.
- Using a car inside Vienna or central Salzburg where parking cost and traffic destroy value.
- Assuming alpine routes, lifts, huts, or scenic roads behave the same in June, September, January, and March.
- Planning Hallstatt or Christmas markets without crowd timing and overnight logic.
- Underestimating Sunday closures and early dinner timing outside the biggest tourist zones.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/austria/`

**This skill does NOT:** Access files outside `~/austria/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `car-rental` — Better rental strategy and handoff logistics
- `booking` — Reservation workflows and confirmation hygiene
- `food` — Deeper restaurant and cuisine recommendations
- `german` — Language support for bookings, transport, and service interactions

## Feedback

- If useful: `clawhub star austria`
- Stay updated: `clawhub sync`
