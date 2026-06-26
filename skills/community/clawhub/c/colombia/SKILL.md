---
name: Colombia
slug: colombia
version: 1.0.0
homepage: https://clawic.com/skills/colombia
changelog: "Initial release with verified Colombia entry rules, region playbooks, and practical tourist logistics."
description: Plan Colombia trips with region-specific routing, verified entry rules, weather-aware logistics, and practical tourist safety.
metadata: {"clawdbot":{"emoji":"🇨🇴","requires":{"bins":[],"config":["~/colombia/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/colombia/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Colombia trip and needs practical guidance beyond generic advice: entry requirements, region choice, route design, altitude and climate fit, transport tradeoffs, and on-the-ground execution.

## Architecture

Memory lives in `~/colombia/`. See `memory-template.md` for structure.

```
~/colombia/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

| Topic | File |
|-------|------|
| **Entry and Border** | |
| Visa, Check-Mig, stay limits, health docs | `entry-and-documents.md` |
| Customs, cash declarations, island and border notes | `customs-and-border.md` |
| **Planning Backbone** | |
| Regions and route strategy | `regions.md` |
| Sample itineraries (7-21 days) | `itineraries.md` |
| Accommodation strategy | `accommodation.md` |
| Budget and cost planning | `budget-and-costs.md` |
| Payments, cards, and cash norms | `tipping-and-payments.md` |
| **Transport** | |
| Flights, buses, boats, and urban systems | `transport-domestic.md` |
| Driving and road trips | `road-trips-and-driving.md` |
| **Nature and Parks** | |
| Parks, permits, closures, and jungle planning | `national-parks.md` |
| **Major Regions and Cities** | |
| Bogota playbook | `bogota.md` |
| Medellin and Antioquia playbook | `medellin-and-antioquia.md` |
| Cartagena and Caribbean coast playbook | `cartagena-and-caribbean.md` |
| Coffee Region playbook | `coffee-region.md` |
| Cali and Pacific playbook | `cali-and-pacific.md` |
| Santander and eastern Andes playbook | `santander-and-eastern-andes.md` |
| Colonial cities and Boyaca playbook | `colonial-cities-and-boyaca.md` |
| Amazon and Llanos playbook | `amazon-and-llanos.md` |
| San Andres and Providencia playbook | `san-andres-and-providencia.md` |
| **Lifestyle and Execution** | |
| Food by region and style | `food-guide.md` |
| Nightlife strategy by city type | `nightlife.md` |
| Traveling with children | `family-travel.md` |
| Accessibility strategy | `accessibility.md` |
| **Safety and Conditions** | |
| Emergencies, protests, health, and scams | `safety-and-emergencies.md` |
| Climate, rain cycles, altitude, and surf windows | `weather-and-seasonality.md` |
| **Tools** | |
| Connectivity and useful apps | `telecoms-and-apps.md` |
| Research sources map | `sources.md` |

## Core Rules

### 1. Route by Geography and Altitude, Not by Hype
Anchor around one macro-region per week. Colombia looks compact on the map, but mountain transfers, flight reliability, and altitude shifts shape trip quality more than attraction count.

### 2. Clear Entry and Health Risk Before Itinerary Work
Use `entry-and-documents.md` first: visa-free vs visa-needed, Check-Mig timing, stay length, onward proof, and yellow-fever exposure if Amazon, Llanos, jungle Caribbean, or certain parks are in scope.

### 3. Choose Transport by Terrain
Always offer at least two route models when relevant:
- Flight-heavy for cross-country jumps or island/Amazon segments
- Bus or road-heavy for one region where scenery and stop control matter

### 4. Make Every Plan Microclimate-Aware
Use `weather-and-seasonality.md` and `national-parks.md` before locking outdoor days. Bogota cold, Caribbean heat, Pacific rain, Andean landslides, and Amazon river conditions can break a naive plan.

### 5. Price the Real Colombia Trip
Budget with actual trip math: airport transfers, baggage, cash-only moments, tolls, island and jungle logistics, park or boat surcharges, and higher costs in holiday peaks.

### 6. Flag Tourist Traps Proactively
Call out common mistakes before users commit:
- Bogota, Medellin, and Cartagena in 4-5 rushed days
- Long overnight road legs in rainy mountain corridors
- Beach-first plans with no heat or humidity tolerance
- Amazon or island planning without vaccine and weather checks

### 7. Deliver Actionable Plans
Output should include:
- Base city strategy
- Day-by-day flow with realistic transfer windows
- Booking deadlines for flights, boats, parks, or islands
- Backup plan for rain, landslides, or protests
- Safety and emergency quick notes

## Common Traps

- Treating Colombia like a fast country-hop instead of a terrain-driven trip.
- Ignoring altitude, humidity, or yellow-fever planning until after bookings.
- Assuming buses are always the budget winner when a short domestic flight saves a full day.
- Booking beach or island stays without sea and weather buffers.
- Choosing accommodation by nightly rate only, ignoring neighborhood safety and airport friction.
- Overpacking regions instead of building two or three strong bases.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/colombia/`

**This skill does NOT:** Access files outside `~/colombia/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `booking` — Reservation workflows and confirmation hygiene
- `food` — Deeper culinary planning for each destination
- `esim` — Better mobile-data setup before arrival
- `spanish` — Language support for bookings, transport, and daily interactions

## Feedback

- If useful: `clawhub star colombia`
- Stay updated: `clawhub sync`
