# Setup - Brazil Travel Guide

## First-Time Setup

When user mentions Brazil travel for the first time:

### 1. Create Memory Structure
```bash
mkdir -p ~/brazil
```

### 2. Initialize Memory File
Create `~/brazil/memory.md` using `memory-template.md`.

### 3. Gather Trip Context Naturally
Ask in conversational flow:
- Passport and nationality, because Brazil entry rules vary by passport.
- Dates or month range, plus whether Carnival, New Year, or school holidays are acceptable.
- Trip style: city, beach, food, wildlife, road trip, family, nightlife, or mixed.
- Comfort with flights, ferries, long buses, and self-drive.
- Budget band and whether premium islands or lodges are realistic.
- Pace: one region deep or two-block contrast trip.
- Constraints: kids, mobility, dietary needs, heat tolerance, mosquito sensitivity, swimming confidence.

### 4. Save to Memory
Update `~/brazil/memory.md` with current intent, priorities, constraints, and open decisions.

## Returning Users

If `~/brazil/memory.md` exists:
1. Read it silently.
2. Reuse known constraints and preferences.
3. Ask only what changed: dates, passport status, region focus, budget, mobility, or weather tolerance.
4. Update memory with deltas.

## Quick Start Responses

**"I want Rio"**
-> Ask: number of nights, beach versus city mix, nightlife comfort, budget, first time versus repeat.
-> Then use: `rio-de-janeiro.md`, `accommodation.md`, `safety-and-emergencies.md`.

**"I want Brazil beaches"**
-> Ask: calm family beach, urban beach, surf, diving, or premium island.
-> Then use: `regions.md`, `salvador-and-bahia-coast.md`, `florianopolis-and-santa-catarina.md`, `fernando-de-noronha-and-recife.md`.

**"I want wildlife or Amazon"**
-> Ask: Amazon lodge, Pantanal wildlife, or waterfall and river focus.
-> Then use: `manaus-and-amazon.md`, `pantanal-and-bonito.md`, `national-parks-and-nature.md`.

## Important Notes

- Entry rules should be confirmed before non-refundable bookings, especially for passports that need visas.
- Brazil routing quality depends on keeping transfer friction under control.
- Payment and booking friction can come from foreign-card limits, PIX-only flows, and CPF prompts.
- Safety advice should be operational and neighborhood-specific, not generic.
