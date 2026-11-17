# The Energy Model

This document explains every formula in `energy_audit.py`, where the library numbers come from, and the limits of the model.

## 1. The core consumption equation

An appliance has two regimes:

- **Active**: it is switched on / in use. It draws `watts`, but — for cycling loads like refrigerator compressors, water heater elements, or thermostated heaters — only for a fraction `duty` of that time.
- **Idle**: it is off or in standby but still plugged in. It draws `standby_w` (0 for simple resistive devices, 1–8 W for anything with a power supply or remote receiver).

Over a 30-day month:

```
active_hours = hours_day × 30 × duty
idle_hours   = max(0, 24 − hours_day) × 30
monthly_kWh  = (watts × active_hours + standby_w × idle_hours) × qty / 1000
```

Worked example — a fridge preset (150 W, duty 0.35, 24 h/day):

```
active = 150 W × 720 h × 0.35 = 37,800 Wh = 37.8 kWh/month
```

That matches real-world Energy Star data for a modern 18-cu-ft top-freezer (~30–40 kWh/mo). An early-2000s unit would be 2× that — model old fridges by raising watts and duty (e.g. 250 W, duty 0.5 → 90 kWh/mo).

Worked example — LED bulbs, qty 8, 4 h/day:

```
8 × 9 W × 120 h = 8,640 Wh = 8.6 kWh/mo  ≈ $1.46/mo @ $0.17
```

## 2. Duty cycles: why nameplate watts lie

| Load type | Duty | Reason |
|---|---|---|
| Fridge/freezer compressor | 0.30–0.45 | Thermostat cycles the compressor |
| Water heater element | 0.15–0.25 | Element heats in bursts |
| Electric oven | 0.5–0.7 | Elements cycle to hold temperature |
| Window/central AC | 0.5–0.65 (cooling season) | Compressor cycles on thermostat |
| Resistive heater | 0.6–0.8 | Thermostat |
| Everything else (TV, PC, bulbs, dryer motor) | 1.0 | Draws continuously while on |

The library ships mid-range values. Duty varies with ambient temperature, door openings, and appliance age — this is the single biggest source of model error, and the reason `calibrate` exists.

## 3. Costs: flat and tiered rates

**Flat rate:** `cost = kWh × rate`.

**Tiered rate** (e.g. California PG&E-style), tiers = [(limit₁, rate₁), (limit₂, rate₂), …, (None, rateₙ)]:

```
cost(kWh) = Σᵢ rateᵢ × kWh falling between limitᵢ₋₁ and limitᵢ
```

Example — 700 kWh under [(500, 0.12), (None, 0.20)]:

```
500 × 0.12 + 200 × 0.20 = $60 + $40 = $100   (avg $0.1429/kWh)
```

**Per-appliance attribution under tiers.** Assigning each appliance its marginal rate would make attribution order-dependent (whose kWh is "first"?). The audit instead attributes everyone the *average* rate of the whole month:

```
avg_rate = tiered_cost(total_kWh) / total_kWh
```

This conserves money exactly (per-appliance costs sum to the bill) and is neutral. It slightly under-weights the appliances you could actually shed (their true marginal rate is the top tier), so treat top-tier-driven rankings as lower bounds on savings.

## 4. Vampire (standby) draw

```
vampire_kWh = standby_w × (24 − hours_day) × 30 / 1000 × qty
```

Typical standby offenders: game consoles 8 W (instant-on), desktop PCs 3 W, TVs 1 W, routers/modems run 24/7 so they have no idle hours and zero vampire share by definition — they're just always-on loads. A home with a console, PC, TV, and microwave clock easily carries 15–25 kWh/mo of pure standby ($2.50–4/mo at $0.17) — a switched power strip pays for itself in a few months.

## 5. Calibration

`calibrate(audit, bill_kWh)` computes `gap = bill − model`:

- **matched** (|gap| < 5%): trust the breakdown.
- **undercounted** (gap > 0): the bill exceeds the model — look for HVAC run-time above assumed hours, an aging compressor, or an unlisted device (dehumidifier, garage freezer, space heater).
- **overcounted** (gap < 0): the model over-estimates — lower `hours_day` on the biggest rows.

Iterate: adjust the top 2–3 rows, re-run, stop when within ±10%. Since every other conclusion (rankings, replace verdicts) flows down from this total, calibration is the step that makes the audit *yours* rather than a generic estimate.

## 6. Replacement analysis

```
saved_kWh/month = old_kWh − new_kWh
saved_$/month   = saved_kWh × marginal_rate        (marginal ≈ average here)
payback_months  = price / saved_$/month
worth_it        = payback ≤ 120 months (10 years)
```

The 120-month cutoff is a heuristic for appliances with 10+ year lifespans (fridges, dryers, AC). For cheaper devices (lamps, smart plugs) you'll see paybacks under 24 months.

## 7. Where the library numbers come from

Presets are mid-range values synthesized from public sources: EPA Energy Star appliance energy reports, EU EPREL database ranges, and typical nameplate/measure values (a 55" LED TV ≈ 100 W, a modern game console ≈ 160 W active / 8 W instant-on standby, etc.). They are starting points for calibration, not measurements of your specific unit — your actual fridge varies ±40% with age, size, and door habits. That variance is exactly why the skill insists on bill calibration before trusting rankings.
