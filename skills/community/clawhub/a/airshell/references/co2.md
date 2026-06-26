# CO₂ — Domain Knowledge

## What it measures
Carbon dioxide concentration in parts per million (ppm). Indoors, CO₂ rises as people breathe in enclosed spaces. It is the primary proxy for ventilation quality — not a direct pollutant at normal indoor levels.

**Outdoor baseline:** ~420 ppm (2024)

## Thresholds — multi-standard comparison

| Level | Range | Source | Notes |
|-------|-------|--------|-------|
| Excellent | <600 ppm | Harvard COGfx "Green+" | Enhanced ventilation target |
| Good | 600–800 ppm | Harvard COGfx "Green" | Well-ventilated room |
| ⚠️ Caution | 800–1,000 ppm | WELL v2 precondition (≤900), RESET acceptable (≤1,000) | Stuffiness begins, mild cognitive impact |
| ❗ High | 1,000–1,500 ppm | ASHRAE de facto limit | Clear cognitive impact, reduced concentration |
| 🚨 Very High | >1,500 ppm | — | Significant impairment, poor sleep |

**Key standards:**
- **ASHRAE 62.1:** No absolute CO₂ limit (removed ~1999). CO₂ is used as a ventilation proxy only.
- **WELL v2:** ≤900 ppm (precondition via sensor pathway) or ≤750 ppm (2-point optimization)
- **RESET Air:** ≤1,000 ppm (Acceptable) / ≤600 ppm (High Performance)
- **EN 16798-1 Cat I** (for children/sensitive groups): outdoor + 550 ppm ≈ ~970 ppm total
- **Harvard COGfx study:** No safe lower threshold — cognitive improvement is linear. +500 ppm CO₂ = 1.4–1.8% slower response times, 2.1–2.4% lower throughput (302-person global study, 2021)
- **Sleep study** (Strøm-Tejsen 2016): rooms with 660–835 ppm showed significantly better sleep quality, reduced next-day sleepiness, better logical thinking vs rooms at 2,395–2,585 ppm

## Cognitive impact reference (COGfx, Satish et al.)

| CO₂ level | Effect |
|-----------|--------|
| ~550 ppm | Baseline cognitive performance (+61–101% vs conventional office) |
| ~950 ppm | Performance begins to decline |
| ~1,000 ppm | ~15% decline in cognitive scores |
| ~1,400 ppm | ~50% decline in cognitive scores |
| >2,500 ppm | Severe impairment across all domains |

## For a nursery / infant context
- **No WHO or EPA CO₂ health standard** — CO₂ is not classified as a pollutant at indoor levels
- **Recommended: <800 ppm** — aligns with Harvard "Green" building target, WELL v2 optimization, and infant sleep safety research
- **Critical infant caveat:** CO₂ concentration *inside a closed crib* can be **up to 4× higher** than the background room level (Braun & Zeiler, 2021, TU Eindhoven). CO₂ rebreathing from soft bedding is linked to SIDS risk via failure of respiratory arousal. Keeping room CO₂ low reduces baseline CO₂ burden.
- **Infants breathe ~40x/min** vs adults 12–20x/min — they cycle through stale air faster and are more exposed to poor ventilation
- Study of 500 children's bedrooms (Klausen et al., 2023): >50% exceeded 1,000 ppm overnight with doors and windows closed; many reached 2,500 ppm by morning

## Recommended AirShell alarm thresholds

| Occupant | Raise | Clear | Smoothing | Rationale |
|----------|-------|-------|-----------|-----------|
| Infant / nursery | 800 ppm | 700 ppm | 5 min | Harvard "Green" target; crib micro-environment can be 4× room level |
| Child / sensitive adult | 900 ppm | 750 ppm | 5 min | WELL v2 precondition |
| General adult | 1,000 ppm | 800 ppm | 5 min | ASHRAE de facto comfort limit |
| Office / productivity | 800 ppm | 700 ppm | 5 min | Harvard COGfx — cognitive impact starts here |

## Common causes of spikes
- Door/windows closed with multiple people in the room
- Poor ventilation in small rooms
- Overnight accumulation in sealed rooms (especially critical for infants)
- Cooking (CO₂ is a combustion byproduct)

## Advice to give
- Open a window or door slightly (CO₂ drops quickly — typically 10–15 min to clear)
- If consistently high overnight: leave door ajar or crack a window
- If spike is accompanied by elevated PM2.5: identify source before deciding whether to ventilate (outdoor PM may be worse)
- CO₂ and PM2.5 don't always move together — CO₂ high + PM normal = ventilation issue; PM high + CO₂ normal = particle source (cooking, etc.)

## Sensor note (SEN63C)
- Sensor: Sensirion SCD41 (inside SEN63C) — photoacoustic NDIR CO₂, very accurate
- Warmup: ~15s after start_measurement before valid readings
- Sentinel value (not ready): 32767 ppm — always ignore/filter
- Factory calibrated; no field calibration needed
- Self-calibration assumes exposure to outdoor air (420 ppm) periodically — relevant for long-term drift
