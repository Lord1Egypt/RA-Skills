---
name: Dominican Republic
slug: dominican-republic
version: 1.0.0
homepage: https://clawic.com/skills/dominican-republic
changelog: "Initial release with verified entry guidance, resort-vs-independent routing, and practical beach, transport, and safety playbooks."
description: Plan Dominican Republic trips with beach-region routing, verified entry steps, off-resort logistics, and practical local safety.
metadata: {"clawdbot":{"emoji":"🇩🇴","requires":{"bins":[],"config":["~/dominican-republic/"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User is planning a Dominican Republic trip and needs execution help beyond generic resort marketing: entry rules, which coast fits the trip, resort vs independent travel tradeoffs, city and beach base strategy, transport reality, weather timing, and practical local safety.

## Architecture

Memory lives in `~/dominican-republic/`. If `~/dominican-republic/` does not exist or is empty, run `setup.md`. See `memory-template.md` for structure.

```text
~/dominican-republic/
└── memory.md     # Trip context, route logic, and evolving constraints
```

## Data Storage

- `~/dominican-republic/memory.md` stores durable trip context, route decisions, and constraints for future Dominican Republic planning.
- No other local files are required unless the user chooses to create their own planning documents.

## Quick Reference

Use this map to load only the decision module that changes the plan in front of you.

| Topic | File |
|-------|------|
| **Entry and Compliance** | |
| Entry flow, passport logic, e-ticket, onward proof | `entry-and-documents.md` |
| Official source map for re-checking moving parts | `sources.md` |
| **Planning Backbone** | |
| Coast and region choice | `regions.md` |
| Sample itineraries for 4-12 days | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Budget framing | `budget-and-costs.md` |
| Cards, cash, taxes, tipping, and payment reality | `payments-and-money.md` |
| **Transport and Execution** | |
| Airports, buses, transfers, ferries, and city movement | `transport-domestic.md` |
| Rental-car fit, toll roads, and driving risk | `road-trips-and-driving.md` |
| Connectivity, ride-hailing, maps, and booking tools | `telecoms-and-apps.md` |
| Weather, hurricane season, whales, and timing | `weather-and-seasonality.md` |
| **Major Bases and Regions** | |
| Santo Domingo city strategy | `santo-domingo.md` |
| Punta Cana, Bavaro, and Cap Cana | `punta-cana-and-bavaro.md` |
| Samana, Las Terrenas, and Las Galeras logic | `samana-and-las-terrenas.md` |
| Puerto Plata, Sosua, and Cabarete | `puerto-plata-cabarete-and-sosua.md` |
| Bayahibe, La Romana, Saona, and diving fit | `bayahibe-and-la-romana.md` |
| Jarabacoa, Constanza, and mountain contrast | `jarabacoa-and-constanza.md` |
| **Lifestyle and Trip Style** | |
| Food strategy and local dishes | `food-guide.md` |
| Beaches by water fit, vibe, and coast | `beaches.md` |
| Signature activities and experience selection | `experiences.md` |
| Family pacing and mixed-age planning | `family-travel.md` |
| Nightlife and evening tradeoffs | `nightlife.md` |
| Etiquette, language, and social rhythm | `culture.md` |
| Emergencies, water safety, and street risk | `safety-and-emergencies.md` |

## Core Rules

### 1. Route by Coast, Not by Resort Ads
The right Dominican Republic trip depends first on which coast matches the goal:
- Punta Cana and Bavaro for easiest resort execution
- Bayahibe and La Romana for calmer southeast water and island-day logic
- Samana and Las Terrenas for independent beach-plus-nature travel
- Puerto Plata and Cabarete for north-coast wind, surfing, and mixed town energy
- Santo Domingo for city, history, food, and nightlife

### 2. Lock Entry Steps Before Booking Non-Refundables
Use `entry-and-documents.md` early to confirm:
- passport and nationality logic
- official e-ticket completion for air arrival and departure
- onward-proof issues for one-way or unusual itineraries
- whether the trip is resort-only, multi-stop, or includes onward international travel

### 3. Resort Trips and Independent Trips Need Different Advice
Do not plan Punta Cana, Santo Domingo, Samana, Bayahibe, and Cabarete with the same assumptions.
- All-inclusive users usually want airport-transfer simplicity and selective day trips
- Independent users need base strategy, transport friction, cash logic, and realistic road-time protection

### 4. Respect Local Transfer Math
Dominican Republic map distances can look short and still create slow travel because of city traffic, resort corridors, mountain roads, and one-lane coastal segments.
- Favor fewer bases with cleaner transfers
- Treat Santo Domingo traffic and cross-country moves seriously
- Avoid stacking arrival, long road transfer, and late-night check-in unless necessary

### 5. Match the Water to the User
Beach advice must separate:
- calm Caribbean swim water
- Atlantic surf and wind
- day-trip islands
- family-safe resort beaches
- photography beaches that are less ideal for casual swimming

### 6. Protect the User From Avoidable Friction
Flag common failures early:
- airport transfer confusion
- paying resort-zone prices for basic errands
- driving at night in unfamiliar areas
- assuming every beach is swimmable in every season
- booking a remote villa without transport, groceries, or weather backup

### 7. Deliver Operational Plans
Output should include:
- best base or base pair
- transfer logic with realistic buffers
- area-level stay recommendation, not just a city name
- budget and payment notes
- water, weather, and safety caveats for that exact route

## Common Traps

- Treating Punta Cana as representative of the whole country.
- Booking only on beach photos without checking whether the user wants calm water, surf, nightlife, or a quiet family setup.
- Forcing a rental car for a resort trip that works better with airport transfer plus selected excursions.
- Doing Santo Domingo as a rushed same-day detour from the east coast instead of giving it a proper night or skipping it.
- Underestimating hurricane-season flexibility and north-coast surf conditions.
- Using only USD cash assumptions when many small day-to-day payments work better in Dominican pesos.
- Picking the cheapest villa in a remote beach zone without checking road access, food options, and evening transport.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/dominican-republic/`

**This skill does NOT:** Access files outside `~/dominican-republic/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `booking` — Reservation workflows and confirmation hygiene
- `car-rental` — Better self-drive strategy and handoff logistics
- `food` — Deeper restaurant and cuisine planning
- `spanish` — Language support for bookings, menus, and practical interactions

## Feedback

- If useful: `clawhub star dominican-republic`
- Stay updated: `clawhub sync`
