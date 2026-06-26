# Setup — Argentina Travel Guide

## First-Time Setup

When user mentions Argentina travel for the first time:

### 1. Create Memory Structure
```bash
mkdir -p ~/argentina
```

### 2. Initialize Memory File
Create `~/argentina/memory.md` using `memory-template.md`.

### 3. Gather Trip Context Naturally
Ask in conversational flow:
- Entry path: nationality, visa-free or visa still pending, any side trip to Brazil or Chile?
- Travel window: exact dates, month range, or season only?
- Scope preference: one region deep or city plus nature contrast?
- Priorities: Buenos Aires, Patagonia, wine, waterfalls, food, family pace, wildlife, road trip, hiking.
- Constraints: budget band, kids, mobility, altitude tolerance, driving comfort, weather tolerance.
- Money style: comfortable with mixed card/cash strategy or prefers minimum cash handling?

### 4. Save to Memory
Update `~/argentina/memory.md` with the current intent, constraints, and decision status.

## Returning Users

If `~/argentina/memory.md` exists:
1. Read it silently
2. Reuse known constraints and priorities
3. Ask only what changed (dates, region focus, budget, border plans, mobility)
4. Update memory with deltas

## Quick Start Responses

**"I want Buenos Aires and Patagonia"**
→ Ask: total days, month, which Patagonia style fits best (lakes, glaciers, or Ushuaia), and whether user accepts internal flights.
→ Then use: `regions.md`, `buenos-aires.md`, one Patagonia playbook, `transport-domestic.md`.

**"I want wine and mountains"**
→ Ask: Mendoza only or Mendoza plus high Andes, self-drive comfort, winery style, and altitude tolerance.
→ Then use: `mendoza-and-wine-country.md`, `road-trips-and-driving.md`, `weather-and-seasonality.md`.

**"I need a full Argentina itinerary"**
→ Ask: exact days, month, and whether user values city, wine, waterfalls, wildlife, or hiking most.
→ Then use: `regions.md`, `itineraries.md`, `budget-and-costs.md`, `money-payments-and-exchange.md`.

## Important Notes

- Argentina planning quality depends heavily on month, region selection, and transfer discipline.
- Money strategy is part of trip design, not a final detail.
- Patagonia should be narrowed before flights are priced.
- Border hops to Brazil or Chile should never be treated as frictionless add-ons.
