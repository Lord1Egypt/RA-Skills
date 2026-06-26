---
name: Denmark
slug: denmark
version: 1.0.0
homepage: https://clawic.com/skills/denmark
changelog: "Initial release with verified Denmark entry rules, compact route logic, island transport planning, and practical regional playbooks."
description: Plan Denmark trips with compact route logic, verified entry rules, island transport choices, and practical local execution.
metadata: {"clawdbot":{"emoji":"🇩🇰","requires":{"bins":[],"config":["~/denmark/"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User is planning a Denmark trip and needs operational guidance beyond generic city lists: Schengen entry checks, Copenhagen vs Jutland vs island routing, rail and ferry choices, weather-fit timing, budget reality, and on-the-ground execution.

## Architecture

Memory lives in `~/denmark/`. If `~/denmark/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/denmark/
└── memory.md     # Trip context, route logic, and evolving constraints
```

## Data Storage

- `~/denmark/memory.md` stores durable trip context, route decisions, and constraints for future Denmark planning.
- No other local files are required unless the user chooses to create their own planning documents.

## Quick Reference

Use this map to load only the Denmark subtopic that changes the decision in front of you.

| Topic | File |
|-------|------|
| **Entry and Compliance** | |
| Tourist entry, Schengen stays, passport checks | `entry-and-documents.md` |
| Customs, cash declarations, restricted goods | `customs-and-border.md` |
| **Planning Backbone** | |
| Macro-regions and route logic | `regions.md` |
| Sample itineraries for 3-14 days | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Budget framing and hidden costs | `budget-and-costs.md` |
| Cards, cash, tax-free, and payment habits | `payments-and-tax-free.md` |
| **Transport and Outdoors** | |
| Trains, buses, ferries, metro, and airport moves | `transport-domestic.md` |
| Driving, bridge tolls, parking, and EV logic | `road-trips-and-driving.md` |
| Bike-first, coast, and island travel logic | `cycling-coasts-and-islands.md` |
| **Major Regions and Bases** | |
| Copenhagen and capital-region base strategy | `copenhagen.md` |
| North Zealand, Roskilde, and Mons Klint logic | `north-zealand-and-south-zealand.md` |
| Funen, Odense, and archipelago pacing | `funen-and-odense.md` |
| Aarhus, Djursland, and east Jutland | `aarhus-and-east-jutland.md` |
| Aalborg, Skagen, Thy, and north Jutland | `north-jutland-and-skagen.md` |
| Ribe, Romo, and the Wadden Sea coast | `southwest-jutland-and-wadden-sea.md` |
| Bornholm planning and access strategy | `bornholm.md` |
| **Lifestyle and Execution** | |
| Food strategy, bakeries, and dining rhythm | `food-guide.md` |
| Traveling with children or mixed ages | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Emergencies, warnings, coast, and weather risk | `safety-and-emergencies.md` |
| Climate, daylight, and seasonality logic | `weather-and-seasonality.md` |
| Connectivity, ticketing apps, and digital tools | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Corridor, Not by Municipality Count
For short trips, choose one dominant shape: Copenhagen and capital region, Funen plus east Jutland, north Jutland coast, southwest Jutland, or Bornholm. Denmark is compact, but bridges, ferries, wind, and hotel changes still punish over-routing.

### 2. Ask for Month Before Naming the Best Region
The same Denmark trip changes meaning in February, May, July, and November. Daylight, coast time, cycling comfort, ferry value, event density, and island logistics all depend on season.

### 3. Confirm Entry and Schengen Friction Early
Before non-refundable bookings, use `entry-and-documents.md` to confirm passport validity, Schengen day-count logic, visa or visa-free status, and whether the trip also touches Sweden, Germany, or wider Schengen routing.

### 4. Always Offer Two Movement Models
For any multi-stop trip, give at least two workable movement patterns:
- Rail and city-transit heavy: easier in Copenhagen, Odense, Aarhus, and simple intercity routes
- Car, ferry, or bike-assisted: better for coasts, west Jutland, Mons Klint, Thy, and flexible island travel

### 5. Budget With Full Denmark Math
Do not price from hotel headlines alone. Include bridge tolls, parking, ferry bookings, airport transfers, museum passes, car-seat or bike-rental costs, and restaurant reality in high-demand areas.

### 6. Protect the User from Island and Coast Fantasy
Flag bad combos early:
- Copenhagen, Aarhus, Skagen, Wadden Sea, and Bornholm in one short trip
- Summer-island plans with no ferry or lodging buffer
- Winter beach or bike-heavy routes sold as if daylight and wind do not matter
- Car rental for city-only stays where parking and stress destroy value

### 7. Deliver Operational Plans
Output should include:
- Best base or base pair
- Day-by-day flow with realistic transfer windows
- Booking deadlines or low-inventory warnings
- Weather downgrade and indoor backup options
- Safety, payment, and emergency notes

## Common Traps

- Treating Denmark like a checkbox add-on instead of a route with real regional character.
- Building a "whole country" trip when the user only has 4-7 days.
- Assuming every island move is spontaneous in peak summer.
- Renting a car before checking whether rail plus one day rental solves the trip better.
- Underestimating wind, cool water, and shoulder-season daylight on coast-heavy trips.
- Forgetting that many small-town restaurants, attractions, and shops have tighter hours outside peak season.
- Planning by map distance instead of bridge, ferry, parking, and check-in friction.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/denmark/`

**This skill does NOT:** Access files outside `~/denmark/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `europe` — Better wider-Europe context when Denmark is part of a longer route
- `booking` — Reservation workflows and confirmation hygiene
- `food` — Deeper restaurant and cuisine planning
- `english` — Language support for bookings, transport, and service interactions

## Feedback

- If useful: `clawhub star denmark`
- Stay updated: `clawhub sync`
