# Gear Derivation Tables — Conditions to Loadout

## Sleep system detail

### Bag ratings decoded (EN 13537 / ISO 23537)

| Rating | Meaning | Plan on it when |
|---|---|---|
| **Comfort** | a cold-side sleeper (woman-standard) sleeps 8h curled normally | ALWAYS — this is the planning number |
| **Limit** | a warm-side sleeper (man-standard) curls up but manages | only as extra margin info |
| Extreme | survival, hypothermia territory | never |

Derived rule used by the script: **required bag comfort = forecast low − 5°F** (radiative
+ forecast-err margin). Convert: °F = °C × 9/5 + 32.

### Pad R-value bands (ASTM F3340-18, additive when stacked)

| R-value | Ground feel | Season use |
|---|---|---|
| < 2.0 | cold by 3 AM below 50°F | summer only |
| 2.0–3.9 | fine to ~40°F nights | 3-season default |
| 4.0–5.9 | fine at freezing | cold 3-season / early winter |
| 6.0+ | snow camping base | winter |

R-values stack additively (R1+R2 = R1+R2) — a cheap foam (R 2.2) under an air pad (R 3.0)
gives R 5.2 and saves the expensive winter pad purchase.

### Liner & clothing boosts (approximate, stackable)

- Fleece/silk liner: +8–10°F
- Wearing your puffy + beanie + socks to bed: +5–10°F (the cheapest upgrade — it's already
  in the pack)
- Vapor barrier socks at freezing: keeps feet dry-warm
- The stack is a chain: sleepwear dry → bag dry → pad adequate. Any wet link loses 30%+

## Insulation layering by static camp hours

Camp is colder than the trail: no movement furnace. For evening static hours at forecast low:

| Forecast low | Core layers while static |
|---|---|
| > 55°F | base tee |
| 45–55°F | base + light fleece |
| 35–45°F | base + fleece + light puffy |
| 25–35°F | base + fleece + mid puffy + beanie + gloves |
| < 25°F | full puff + insulated pants consideration (ditch cotton sleepwear) |

## Water plan by terrain

| Terrain | Sources | Carry capacity | Daily consumption |
|---|---|---|---|
| Wet mountains (streams frequent) | every 1–3 mi | 1.5–2 L | 2.5–3.5 L/day |
| Rolling forest (seasonal) | every 3–6 mi | 2–3 L | 2.5–3 L/day |
| Arid/desert | every 6–12 mi | 4–6 L + electrolytes | 4–6 L/day |
| Snow (winter) | melt from snow | 2 L + stove + fuel | 2–3 L/day + fuel penalty |

Rules: treat everything (filter/purifier + backup chemical tabs), know the next TWO
sources, and cache nothing you can't afford to lose. In deserts, carry capacity for the
longest gap + 1 L reserve, and start walking cool.

## Fuel & food math (script implements)

- Canister stove: ~10–12 g fuel / person-day (2 boils + coffee). A 230 g canister ≈ 18–20
  person-days; 110 g ≈ 8–9. Group of 4 for 2 nights: ~100 g — one 110 g canister is right.
- Liquid-fuel (white gas): ~40–50 ml / person-day, plus priming. Cold-weather winner.
- Cold-soak: 0 g fuel, jars instead of pots — UL lunch strategy, not dinner for most.
- Food: 1.5 lb/person-day easy miles → 2.0–2.5 lb/person-day big mileage / cold weather.
  100–125 kcal per mile hiked beyond baseline is the backpacker's rule.

## Bear-country food storage by region

| Region | Method | Notes |
|---|---|---|
| Black bear, general | hang (counterbalance or PCT method, 12 ft up / 6 ft out) or ursack | canisters not usually required |
| Grizzly country (GTNP/Yellowstone/Glacier/Alaska) | **IGBC-approved canister** often mandatory | check the park's current order — fines + real risk |
| Sierra (Yosemite/SEKI) | canister mandatory (Garcia/Bearikade/etc.) | hangs are illegal and don't work there |
| Eastern US (Adirondacks) | canisters required in Eastern High Peaks | bears defeat hangs routinely |
| Car camping | hard-sided vehicle or locker | coolers are bear toys |

Also: cook 100 yd from sleep, nothing scented in the tent (toothpaste counts), and in
grizzly country travel noisily in low visibility.

## Shared-gear division math (groups)

- 1 stove per 3–4 people (boil throughput)
- 1 filter per 2–3 (bottleneck is patience, not flow rate)
- 1 first-aid kit per group + 1 minor solo kit each
- Tents paired 2-person = half the shelter weight per head vs solos
- Weight balancing: heavier items (water on day 1, stove, tent body) to the strongest
  backs, not even splits — the manifest should show per-person totals

## Condition flags the planner should surface

- Forecast older than 48h → refetch
- Clear skies + calm + dry air → subtract 3–5°F from the forecast low (radiative cooling)
- Above 8,000 ft → subtract ~3.5°F per 1,000 ft from the valley forecast (lapse rate)
- River fords / snowfields on route → trekking poles + camp shoes, stakes that hold in
  snow (deadman/snow stakes)
- Fire ban → stove-only meal plan, no ember-dependent recipes
