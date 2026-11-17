# Basement Moisture: Physics, Diagnosis, Fixes

Reference for `scripts/dampdoctor.py`.

## 1. Dew point (Magnus formula)

```
γ = ln(RH/100) + (a·T)/(b+T)          a=17.62, b=243.12 °C
Td = b·γ / (a − γ)
```
Moisture condenses on any surface with T < Td. At 22°C/70% RH, Td ≈ 16.4°C —
exactly the temperature of a summer basement wall against cool soil, which is
why "the walls sweat in July" is an air problem, not a leak.

Dew-point quick table (T, RH → Td):

| T\RH | 50% | 60% | 70% | 80% |
|---|---|---|---|---|
| 18°C | 7.4 | 10.0 | 12.4 | 14.7 |
| 22°C | 11.1 | 13.9 | 16.4 | 18.7 |
| 26°C | 14.8 | 17.8 | 20.5 | 23.1 |

Rule of thumb: **keep basement RH ≤ 55% in summer** and the coldest wall stays
above dew point in most climates. Below 45% is unnecessary (and expensive).

## 2. Deep-soil temperature lag model

Soil below ~2 m tracks the annual mean air temperature with a 1–2 month lag
and heavily damped swing:

```
T_soil(t) ≈ T_mean + A·exp(−z/d)·cos(ω(t−t_peak))     d ≈ 2.5–3 m
```
Practical bands (northern temperate climate):
- Jan–Feb: soil 8–10°C (coldest walls in... spring, when warm humid air
  arrives before soil warms — April–June is peak condensation season)
- Apr–Jun: soil 10–13°C
- Jul–Sep: soil 14–17°C (walls warm but air is most humid)
- Oct–Dec: soil 14–16°C while outside air cools — condensation fades

If the user measures the actual wall temperature (cheap IR thermometer or
even a hand test), the measurement beats the model — the script uses
`--wall-t` over `--soil-t` whenever both are given.

## 3. Efflorescence vs mold vs staining decoder

| Sign | What it is | Problem class |
|---|---|---|
| White crystalline powder, streaks | Salts crystallized as water evaporates from concrete | LIQUID path (water moving through) |
| Black/green spots on organic matter, paint, cardboard | Colonies on wet dust/organics | Condensation or humidity ≥70% sustained |
| Tide mark / dark band at wall base, uniform | Capillary rise or hydrostatic seepage at the joint | LIQUID |
| Isolated dark patch trailing from a crack | Crack leak | LIQUID, localized |
| Uniform damp film, worst on cold walls/tank/pipes | Surface below dew point | CONDENSATION |
| Rust stains, musty smell near sump | Unsealed sump evaporating | INTERIOR source |

## 4. The 10-source ranking (cheap-first, as priced by the audit)

1. **Downspouts dumping at the foundation** — extenders/downspout drains,
   $10–50 per corner. The #1 cause of wet basements.
2. **Negative grading** — soil sloping toward the wall within 3 m; regrade,
   $0 (DIY topsoil) to $500.
3. **Clogged/short gutters** — overflow cascades at corners.
4. **Window wells without drains/covers** — $20 domes, gravel top-up.
5. **Dryer venting inside** — 2–4 L of water per load into the air; vent out
   ($30–100).
6. **Unsealed sump pit** — a lid converts a constant evaporator to a closed
   system ($30–80).
7. **Gas/water-service penetration gaps** — hydraulic cement, $10.
8. **Interior moisture sources** — drying laundry, firewood storage, humidifier
   drain leaks.
9. **Wall cracks (cold joints, shrinkage)** — injection epoxy/polyurethane,
   $15 DIY kit to $500 pro — only after outside water management.
10. **Hydrostatic pressure / high water table** — drain tile + sump (interior
    French drain $3k–10k) — LAST, and only if 1–9 are done and it still leaks.

## 5. Dehumidifier sizing details

- Test basis: AHAM at 27°C/60% RH. At 18°C (cool basement) the same unit
  extracts ~60% of nameplate — buy one class up for cold basements.
- Energy: Energy Star ≈ 1.6 L/kWh integrated factor. A 20 L/day unit cycling
  12 h/day at 300 W ≈ 3.6 kWh/day ≈ $11–14/mo at $0.12–0.35/kWh — the
  script prices it at your rate.
- Drain hose or condensate pump for anything ≥12 L/day; buckets are a
  behavior tax that leads to overflow and rust.
- Fan circulation matters: a $30 circulator moving air across cold walls
  raises the effective surface temperature and cuts condensation.

## 6. When to actually call a contractor

- Pooled water at the wall-floor joint during rain AFTER downspouts/grading
  were fixed → interior drain tile evaluation.
- Horizontal cracking + bowing walls → structural, not moisture.
- Efflorescence that returns within weeks of scrubbing → active liquid path;
  get two bids, expect $500 crack injection BEFORE anyone mentions $10k systems.
