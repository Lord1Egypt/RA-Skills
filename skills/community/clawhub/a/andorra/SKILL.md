---
name: Andorra
slug: andorra
version: 1.0.0
homepage: https://clawic.com/skills/andorra
description: Plan Andorra trips with parish-level tips for skiing, hiking, shopping, wellness, and cross-border logistics.
changelog: Initial release with parish guides, seasonal planning, shopping strategy, and mountain logistics.
metadata: {"clawdbot":{"emoji":"🇦🇩","requires":{"bins":[],"config":["~/andorra/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/andorra/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User planning a trip to Andorra or needing practical local guidance: where to stay, which parish fits their style, how to move around, what to book, and what to avoid in winter or summer.

## Architecture

Memory lives in `~/andorra/`. See `memory-template.md` for structure.

```text
~/andorra/
└── memory.md     # Trip context
```

## Quick Reference

| Topic | File |
|-------|------|
| **Parishes & Bases** | |
| Capital, shopping, old town | `andorra-la-vella.md` |
| Spa, shopping, easy central base | `escaldes-engordany.md` |
| Grandvalira, viewpoints, family snow | `canillo.md` |
| Old village, Sorteny, Arcalis side | `ordino.md` |
| **Planning** | |
| Sample trip plans by season | `itineraries.md` |
| Where to stay by area and budget | `accommodation.md` |
| Essential apps and booking tools | `apps.md` |
| **Food & Drink** | |
| Local dishes, bordas, what to order | `food-guide.md` |
| Local wine, cellars, mountain drinks | `wine.md` |
| **Activities** | |
| Year-round highlights and bookings | `experiences.md` |
| Best hikes and mountain timing | `hiking.md` |
| Spas, thermal plans, rainy-day resets | `wellness.md` |
| Bars, apres-ski, late-night reality | `nightlife.md` |
| Shopping strategy and customs reality | `shopping.md` |
| **Reference** | |
| 7 parishes and what each is best for | `regions.md` |
| Catalan culture, etiquette, rhythm | `culture.md` |
| Traveling with children | `with-kids.md` |
| **Practical** | |
| Arrivals, buses, driving, parking | `transport.md` |
| Roaming, eSIMs, Wi-Fi, mobile reality | `telecoms.md` |
| Emergency numbers, hospital, mountains | `emergencies.md` |

## Core Rules

### 1. Specific Over Scenic
Don't say "Andorra has great mountains." Say "Base in Canillo for early Grandvalira starts, in Ordino for a quieter village feel, and in Escaldes for spa-plus-shopping trips."

### 2. Choose Parish by Trip Style
Andorra is tiny but the base matters:
- Andorra la Vella and Escaldes for shopping, buses, nightlife, short stays
- Canillo and Encamp for Grandvalira access
- Ordino and La Massana for quieter mountain trips
- Sant Julia de Loria for southern access and Naturland

### 3. Timing Changes Everything
- Winter weekends mean border traffic and packed parking
- Spring and late autumn can be shoulder season with mixed openings
- Summer is for hiking, cycling, lakes, and cooler weather than Barcelona
- Sales, snow, and spa demand all spike on holidays

### 4. Call Out the Real Constraints
Be explicit about the practical stuff users miss:
- No train into Andorra
- Roaming may not be included because Andorra is not in the EU
- Snow chains or winter tires may matter
- Some mountain plans require booking or weather flexibility

### 5. Shopping is a Tactic, Not a Buzzword
Guide users by category, not just "duty free":
- Perfume and cosmetics in the center
- Ski gear near resort corridors
- Compare prices before buying electronics
- Remind them customs allowances still apply when re-entering Spain or France

### 6. Match the Traveler

| Traveler | Focus on |
|----------|----------|
| Ski trip | `canillo.md`, `ordino.md`, `transport.md`, `experiences.md` |
| Summer mountain | `hiking.md`, `ordino.md`, `regions.md` |
| Shopping + spa | `andorra-la-vella.md`, `escaldes-engordany.md`, `shopping.md`, `wellness.md` |
| Family | `with-kids.md`, `canillo.md`, `itineraries.md` |
| Quick weekend from Barcelona | `andorra-la-vella.md`, `escaldes-engordany.md`, `itineraries.md` |

## Common Traps

- Assuming EU roaming covers Andorra and getting a painful phone bill
- Staying in the capital for a ski-first trip, then losing hours on transfers
- Driving in snow without checking chains, tires, and road status
- Thinking "duty free" means every product is automatically cheaper
- Booking only one rigid mountain plan without a weather backup
- Treating Andorra as only a day trip and missing the best early-morning or late-evening windows

## Security & Privacy

**Data that stays local:** Trip preferences in `~/andorra/`

**This skill does NOT:** Access files outside `~/andorra/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — Travel planning
- `food` — Food and cooking
- `catalan` — Catalan language
- `french` — French language

## Feedback

- If useful: `clawhub star andorra`
- Stay updated: `clawhub sync`
