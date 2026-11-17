# Charging Physics — Losses, Amperage, Panels, Batteries

## Wall-to-battery efficiency
Every kWh in the battery requires more from the meter:
- onboard charger conversion: ~92-95% efficient
- AC wiring + connector: ~98%
- battery internal resistance + thermal management: varies

Practical planning number: **0.90** (the tool's default). Cold batteries and
very low/high states of charge push losses higher.

Consequence: "electricity is $0.14/kWh and my car holds 60 kWh, so a fill
costs $8.40" is wrong — it's 66.7 kWh × $0.14 = **$9.33**. Over a year of
nightly partial charges the delta is real but modest; over a TOU decision it
can matter more than the spread itself.

## Volts, amps, kW
US Level 2 charging is 240V. Power: `kW = amps × V / 1000 = amps × 0.24`.

| Circuit breaker | Usable amps (80%) | kW | Miles/hour added* |
|---|---|---|---|
| 20A | 16A | 3.8 kW | ~13 mi/h |
| 30A | 24A | 5.8 kW | ~20 mi/h |
| 40A | 32A | 7.7 kW | ~26 mi/h |
| 50A | 40A | 9.6 kW | ~33 mi/h |
| 60A | 48A | 11.5 kW | ~39 mi/h |

*at 3.4 mi/kWh and 90% efficiency.

Level 1 (ordinary 120V outlet, 12A) delivers ~1.4 kW ≈ 4-5 miles/hour —
enough for ~40 miles of daily driving if plugged in 10h/night, which covers
most commutes, but never recovers a big deficit.

## The 80% rule and panel math
NEC requires continuous loads (anything >3h — EV charging qualifies) to stay
at ≤80% of the circuit's rating. Same discipline at the panel level:

```
safe_charger_kW = (panel_amps × 0.80 − baseline_house_amps) × 0.24
```

Example: 100A panel, 28A evening baseline (HVAC + cooking + normal life):
(100×0.8 − 28) × 0.24 = 15.4 kW of headroom — a 48A EVSE (11.5 kW) fits on
paper. But at -10°C with heat pump + aux strips + dryer + oven the baseline
can exceed 52A and breach 80%. Options, in order of preference:
1. **EVSE load management** (most wallboxes support CT-clamp meters that
   throttle charging when the panel approaches its limit).
2. Scheduled charging in the off-peak window — exactly when other house
   loads are lowest. This is why overnight charging is ALSO a panel-safety
   practice, not just a rate practice.
3. Lower amperage setting: 32A covers almost every overnight need.

## Battery care: the 20-80 protocol
Lithium batteries age faster at extreme states of charge, especially warm
and full:
- Daily target 80% (many cars have a "daily charge limit" — use it).
- 100% only before long trips, ideally timed to finish right before depart.
- Don't park for days at very low SoC; the 20% floor is a habit, not a joke.
- LFP batteries (some Teslas, others) are the exception: charge to 100%
regularly — the BMS needs full charges to calibrate.

## Cold weather
- Range drops 10-30% below ~0°C (cabin heat + battery chemistry).
- Charging is slower on a cold pack; preconditioning (warming while plugged
  in) restores both range and charge speed.
- Departure preconditioning runs off GRID power if plugged in — that's free
  range. The 30-min post-charge buffer in the TOU planner exists for this.

## Efficiency factors to apply to your mi/kWh
| Condition | Effect |
|---|---|
| Highway 75+ mph | −15-25% |
| Below freezing | −10-30% |
| Roof cargo box | −5-10% |
- Snow tires | −2-4% |
| Jackrabbit starts | −5-15% |
Use the dashboard's lifetime average as your baseline; adjust for trip type.

## Worked problem: the 5-to-8 deficit
60 kWh needed, 7.4 kW charger, window 00:00-06:00, depart 06:00, 30 min
buffer → 5.5h usable → 36.6 kWh fits. Deficit 23.4 kWh.

- Exit (a): a 12.1 kW charger would need a 60A circuit — panel question
  first, then ~$500-1500 installed delta.
- Exit (b): tonight 36.6 kWh = 124 miles — enough if tomorrow is a normal
  day; top up tomorrow.
- Exit (c): the 23.4 kWh tail at the $0.23 spread costs $5.97 extra —
  once a month that's noise; nightly it's $180/yr and you should fix the
  setup instead.

This is the actual decision architecture of home charging: power, window,
habit — in that order.
