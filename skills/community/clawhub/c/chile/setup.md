# Setup — Chile Travel Guide

## First-Time Setup

When user mentions Chile travel for the first time:

### 1. Create Memory Structure
```bash
mkdir -p ~/chile
```

### 2. Initialize Memory File
Create `~/chile/memory.md` using `memory-template.md`.

### 3. Gather Trip Context Naturally
Ask in conversational flow:
- Travel window: exact dates, month range, or shoulder-season flexibility?
- Scope preference: central Chile plus one macro-region, or one region deep only?
- Priorities: cities, wine, food, desert, astronomy, lakes, trekking, wildlife, road trip, beaches, family.
- Constraints: budget, mobility, driving comfort, altitude tolerance, cold/wind tolerance.
- Transport preference: fly more, bus more, self-drive, or mixed.
- Reservation pressure: okay with fixed bookings, or prefers flexibility?

### 4. Save to Memory
Update `~/chile/memory.md` with the current intent, constraints, and decision status.

## Returning Users

If `~/chile/memory.md` exists:
1. Read it silently
2. Reuse known constraints and preferences
3. Ask only what changed: dates, region focus, budget, mobility, or trekking appetite
4. Update memory with deltas

## Quick Start Responses

**"I want Santiago and Valparaiso"**
-> Ask: total nights, first-time vs repeat, budget band, nightlife vs museums vs food.
-> Then use: `santiago.md`, `valparaiso-and-vina.md`, `budget-and-payments.md`.

**"I want Atacama"**
-> Ask: month, altitude tolerance, astronomy interest, rental-car comfort.
-> Then use: `atacama.md`, `weather-and-seasonality.md`, `transport-domestic.md`.

**"I want Patagonia"**
-> Ask: total days, trekking level, whether refugios/camps are acceptable, and if the trip is Torres-only or broader Patagonia.
-> Then use: `patagonia-and-torres-del-paine.md`, `national-parks.md`, `road-trips-and-driving.md`.

## Important Notes

- Chile trip quality depends heavily on picking the right latitude band for the available days.
- The two biggest planning breakers are altitude in the north and weather/reservation pressure in Patagonia.
- Many "cheap" routes become expensive after transfers, park tickets, and domestic baggage rules.
- Always include one backup option for weather, wind, closures, or transport disruption.
