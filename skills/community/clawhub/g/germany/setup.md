# Setup — Germany Travel Guide

## First-Time Setup

When user mentions Germany travel for the first time:

### 1. Create Memory Structure
```bash
mkdir -p ~/germany
```

### 2. Initialize Memory File
Create `~/germany/memory.md` using `memory-template.md`.

### 3. Gather Trip Context Naturally
Ask in conversational flow:
- Entry path: nationality, Schengen familiarity, visa-free or visa still pending?
- Travel window: exact dates, month range, or season only?
- Scope preference: one region deep, city plus scenic contrast, or multi-city rail trip?
- Priorities: Berlin, Bavaria, castles, Christmas markets, wine, museums, family pace, nightlife, road trip, hiking.
- Constraints: budget band, kids, mobility, driving comfort, weather tolerance, luggage style.
- Movement style: rail-first, car-first, or flexible if tradeoffs are clear?

### 4. Save to Memory
Update `~/germany/memory.md` with the current intent, constraints, and decision status.

## Returning Users

If `~/germany/memory.md` exists:
1. Read it silently
2. Reuse known constraints and priorities
3. Ask only what changed (dates, region focus, event goals, budget, mobility)
4. Update memory with deltas

## Quick Start Responses

**"I want Berlin and Bavaria"**
→ Ask: total days, month, rail comfort, and whether user wants city depth or castles and Alpine scenery.
→ Then use: `regions.md`, `berlin.md`, `munich-and-upper-bavaria.md`, `transport-domestic.md`.

**"I want Christmas markets in Germany"**
→ Ask: late November or December dates, crowd tolerance, whether user wants big-city or smaller-market atmosphere, and whether they accept cold-weather rail travel.
→ Then use: `christmas-markets-and-festivals.md`, `weather-and-seasonality.md`, `regions.md`, `accommodation.md`.

**"I need a full Germany itinerary"**
→ Ask: exact days, month, rail versus car preference, and whether user values cities, castles, food and wine, family pace, or winter atmosphere most.
→ Then use: `regions.md`, `itineraries.md`, `budget-and-costs.md`, `payments-and-tipping.md`.

## Important Notes

- Germany planning quality depends heavily on cluster selection, event timing, and rail-versus-car discipline.
- Sunday closures and fair or festival dates can reshape otherwise good plans.
- Bavaria, the Rhine, Berlin, and the north should be treated as distinct products, not automatic add-ons.
- Rail is powerful, but not every scenic route or village-heavy plan should be built around it.
