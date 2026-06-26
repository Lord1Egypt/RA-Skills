---
name: Bulgaria
slug: bulgaria
version: 1.0.0
homepage: https://clawic.com/skills/bulgaria
description: Plan Bulgaria with local context on Sofia, Plovdiv, the Black Sea, mountain routes, food, and tourist-trap avoidance.
changelog: Added a Bulgaria travel guide covering cities, coast, mountains, food, and practical trip planning.
metadata: {"clawdbot":{"emoji":"🇧🇬","requires":{"bins":[],"config":["~/bulgaria/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/bulgaria/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a trip to Bulgaria or needs local context on cities, beaches, mountain trips, food, transport, winter resorts, or practical travel logistics.

## Architecture

Memory lives in `~/bulgaria/`. If `~/bulgaria/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```
~/bulgaria/
└── memory.md     # Trip context and learned preferences
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| **Cities** | |
| Sofia complete guide | `sofia.md` |
| Plovdiv complete guide | `plovdiv.md` |
| Varna complete guide | `varna.md` |
| Bansko complete guide | `bansko.md` |
| **Planning** | |
| Sample itineraries | `itineraries.md` |
| Where to stay by style | `accommodation.md` |
| Useful apps | `apps.md` |
| **Food & Drink** | |
| Dishes, markets, ordering norms | `food-guide.md` |
| Wine regions and grape varieties | `wine.md` |
| **Experiences** | |
| Day trips and standout experiences | `experiences.md` |
| Black Sea beach guide | `beaches.md` |
| Hiking and mountain routes | `hiking.md` |
| Nightlife by city and season | `nightlife.md` |
| **Reference** | |
| Regional differences | `regions.md` |
| Customs, timing, etiquette | `culture.md` |
| Traveling with children | `with-kids.md` |
| **Practical** | |
| Flights, rail, buses, driving | `transport.md` |
| SIMs, roaming, coverage | `telecoms.md` |
| Emergencies and safety | `emergencies.md` |

## Core Rules

### 1. Specific Beats Generic
Do not say "try Bulgarian food". Say "banitsa for breakfast, shopska salad with rakia before dinner, and grilled fish on the coast instead of beach-strip menus."

### 2. Distinguish Bulgaria's Travel Modes
Match the plan to what the user actually wants:
- Sofia and Plovdiv for city + history
- Varna, Sozopol, and Sinemorets for coast
- Bansko, Rila, and Rhodopes for mountains
- Melnik and Thracian Valley for wine

### 3. Call Out Seasonal Reality
Timing changes the answer:
- Ski towns peak in winter and hiking peaks in summer
- Black Sea resorts feel best in June and September
- Sofia and Plovdiv are easier than the coast in deep winter
- Mountain weather turns fast even in warm months

### 4. Flag Tourist Traps Early
Warn about the common misses:
- Sunny Beach if the user wants quiet or local Bulgaria
- all-inclusive beach strips if they want food or culture
- driving mountain roads in winter without preparation
- assuming every "traditional" restaurant is actually good

### 5. Explain Practical Friction
Bulgaria is easy once the frictions are named:
- intercity buses are often more useful than trains
- cards work in cities, but some rural spots still prefer cash
- English is common in tourist areas, weaker in small towns
- prices and opening hours should be checked before booking

### 6. Match Traveler Style

| Traveler | Focus on |
|----------|----------|
| Foodie | `food-guide.md`, `wine.md`, `plovdiv.md` |
| Beach | `beaches.md`, `varna.md`, `regions.md` |
| Culture | `sofia.md`, `plovdiv.md`, `experiences.md` |
| Hiking | `hiking.md`, `bansko.md`, `regions.md` |
| Family | `with-kids.md`, `beaches.md`, `itineraries.md` |
| Nightlife | `nightlife.md`, `sofia.md`, `varna.md` |

## Common Traps

- Treating Bulgaria as "just cheap" instead of planning by region and season
- Booking Sunny Beach when the user actually wants calm beaches or culture
- Assuming trains are always the best option between cities
- Underestimating mountain weather and lift closures
- Expecting dinner timing or service style to match Italy or Spain
- Relying only on head gestures for yes/no instead of listening carefully

## Security & Privacy

**Data that stays local:**
- Trip preferences in `~/bulgaria/`
- Saved notes on cities, budget, pace, and dislikes

**This skill does NOT:**
- Access files outside `~/bulgaria/`
- Make network requests on its own
- Book or purchase anything without user direction

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - General trip planning and logistics
- `food` - Restaurant thinking, dishes, and meal planning
- `bulgarian` - Bulgarian language help for phrases, menus, and messaging

## Feedback

- If useful: `clawhub star bulgaria`
- Stay updated: `clawhub sync`
