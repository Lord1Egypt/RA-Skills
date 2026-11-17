# Battery Cold-Start Physics & Failure Signatures (Reference)

## 1. Resting voltage → State of Charge (12 V lead-acid, 25 °C)

| Resting V | SOC | Field meaning |
|---|---|---|
| ≥12.7 | 100% | healthy full |
| 12.5 | ~80% | fine |
| 12.4 | 75% | acceptable, charge soon |
| 12.2 | 50% | sulfate risk if left |
| 12.0 | 25% | will struggle < 0 °C |
| 11.9–11.4 | near-empty | deep discharge damage begins |
| ~10.5 or stable-low | — | **shorted/dead cell → replace** |

Voltage drops ~0.01 V per °C below 25 °C — minor vs SOC effect, included
in the script.

## 2. Cold derate (available cranking power)

Empirical curve (SAE-style approximation used by the script):

```
factor(T) = 0.55 + 0.45 / (1 + exp(-(T + 5) / 8))
```

| T (°C) | Available power |
|---|---|
| +27 | 100% |
| 0 | ~65% |
| −18 | ~40% |
| −30 | ~30% |

## 3. Cranking demand vs temperature

Thick cold oil raises cranking torque/current:

```
demand_mult(T) = 1 + 0.8 * max(0, (18 - T) / 36)   # 1.0 at 18°C → 2.0 at -18°C
```

Engine-class baseline CCA need (warm):

| Engine | Baseline warm CCA need |
|---|---|
| 4-cyl gas | 150–200 |
| 6-cyl gas | 200–280 |
| 8-cyl / full-size truck | 280–400 |
| 4-cyl diesel (unheated) | 400–600 |

## 4. Age fade

Average-climate fade ≈ 6%/yr; hot-climate (parked outdoors, southern
summers) 8–10%/yr; garage-kept gentle use 4–5%/yr. Most batteries that
"die suddenly" actually crossed the demand line on the first cold
morning — the curve was approaching all summer.

## 5. The no-start line

The battery fails to start the engine when:

```
CCA_rated × age_factor × cold_factor(T) < baseline_CCA × demand_mult(T)
```

The script solves for T numerically (bisect −45…+30 °C). A 4-year-old
550 CCA battery in a 6-cyl gas car stops starting around −20 °C on paper
— but real-world margin (oil state, wiring resistance, 3 s vs 0.5 s
crank) eats 5–8 °C of that. Treat the computed line as optimistic.

## 6. Failure signatures (no tools)

| Observation | Points to |
|---|---|
| Nothing at all, no lights | cables/terminals/ground, or fully dead battery |
| One click, headlights BRIGHT | starter solenoid/circuit — not battery |
| Click-click-click, lights DIM | battery low or high-resistance connection |
| Cranks strong, won't fire | fuel/ignition/engine — battery is fine |
| Cranks slow → slows → stops | battery exhausted (or alternator never charging) |
| Starts fine hot, slow cold AM | battery capacity loss (classic age fade) |
| Fine daily, dead after 3 days sitting | parasitic drain (>50 mA overnight norm) |

## 7. Alternator quick check (dash or cheap meter)

- Engine running: 13.8–14.6 V = charging correctly.
- Running < 13.0 V = alternator/regulator problem (battery is victim).
- Running > 15.0 V = overcharge — regulator failing, cooking battery.

## 8. Jump-start order (never let clamps touch)

1. Red → dead battery positive.
2. Red → donor battery positive.
3. Black → donor battery negative.
4. Black → UNPAINTED METAL on dead engine block (NOT the dead negative
   post — spark safety near venting hydrogen).
5. Donor engine running 1–2 min, then start the dead car.
6. Remove in reverse order. Drive 30+ min (not idle) or put on a charger.

Modern cars: key fob electronics are safe; do not disconnect the dead
battery while running. EV/hybrid 12 V systems: use the designated jump
posts, not the traction pack area.

## 9. Cold-start protocol

1. All electrical loads off (blower, lights, heated screens, seat
   heaters — heated rear window is a 10 A thief).
2. Key on 3–5 s (fuel pump prime on many cars), key off, repeat once.
3. Crank 5 s max, rest 30 s, max 3 attempts.
4. Starts: let idle 10–30 s, drive gently; alternator recharges better
   with RPM than idle.
5. No start after 3 attempts: stop — triage with the signature table,
   don't grind the starter.

## 10. Buying guidance

- Match OEM group size; meet or exceed OEM CCA (never below).
- Cold climate: +15–20% CCA headroom over OEM.
- Date code on case: buy batteries < 3 months old (shelf discharge +
  sulfation starts immediately). Letter = month (A=Jan), digit = year.
- Warranty math: free-replacement period matters more than total years.
