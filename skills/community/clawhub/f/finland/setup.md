# Setup — Finland Travel Guide

## First-Time Setup

When user mentions Finland travel for the first time:

### 1. Create Memory Structure
```bash
mkdir -p ~/finland
```

### 2. Initialize Memory File
Create `~/finland/memory.md` using `memory-template.md`.

### 3. Gather Trip Context Naturally
Ask in conversational flow:
- Entry pathway: visa-free Schengen stay, visa application, or still unknown?
- Travel window and flexibility: exact dates, month range, or open season choice?
- Main trip identity: Helsinki city break, Lapland winter, summer lakes, archipelago, or mixed.
- Priorities: aurora, sauna, design, nature, family activities, road trip, food, Christmas season, midnight sun.
- Constraints: budget, mobility, cold tolerance, snow-driving comfort, dietary needs, kids, and luggage volume.
- Pace: one strong base, two bases, or transfer-heavy and willing to spend time in transit.

### 4. Save to Memory
Update `~/finland/memory.md` with the current intent, constraints, and decision status.

## Returning Users

If `~/finland/memory.md` exists:
1. Read it silently
2. Reuse known constraints and preferences
3. Ask only what changed (dates, region focus, budget, cold tolerance, mobility)
4. Update memory with deltas

## Quick Start Responses

**"I want northern lights in Finland"**
-> Ask: month, budget, cold tolerance, and whether the user wants to drive.
-> Then use: `lapland.md`, `weather-and-seasonality.md`, `transport-domestic.md`.

**"I only have a few days and arrive in Helsinki"**
-> Ask: nights, first-time vs repeat, and whether user wants city-only or one side trip.
-> Then use: `helsinki-and-capital-region.md`, `itineraries.md`, `accommodation.md`.

**"Plan a Finland trip for my family"**
-> Ask: ages, winter vs summer, stroller or mobility needs, and appetite for transfers.
-> Then use: `family-travel.md`, `regions.md`, `budget-and-costs.md`.

## Important Notes

- Finland trip quality depends more on season fit and transfer realism than attraction count.
- Lapland looks close on the map and still needs honest rail, flight, or winter-road planning.
- Helsinki works well as a compact base, but Finland gets expensive fast when users improvise transport and gear.
- Always include a weather-aware fallback plan for outdoor-heavy trips.
