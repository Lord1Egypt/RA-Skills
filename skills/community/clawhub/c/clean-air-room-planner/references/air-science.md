# Clean Air Science & References

## 1. CADR and ACH — the two numbers that matter

**CADR** (Clean Air Delivery Rate, AHAM standard) = airflow (CFM or m³/h)
× fractional single-pass efficiency. A HEPA unit moving 100 m³/h at 99 %
particle capture delivers ~99 m³/h clean air. Ratings are given separately
for smoke (fine), dust (coarse) and pollen — use the **smoke CADR** for
PM2.5 work, it's the most conservative.

**ACH** (air changes per hour) = CADR / room volume. Sizing conventions
from smoke-readiness guidance (EPA Wildfire Smoke Guide, state public
health advisories):

| Situation | Target ACH | Why |
|---|---|---|
| Wildfire smoke event | 5 | Keeps sealed-room PM2.5 at 10–20 % of outdoor |
| Allergy season | 4–5 | Pollen is larger/easier than smoke PM2.5 |
| General freshness | 2–3 | Marketing "room size" claims usually assume this |

The "for rooms up to 60 m²" claim on the box is computed at ~2 ACH with
the unit on **maximum** speed — i.e., loud. For smoke you need CADR =
volume × 5, run on high.

### Noise and the low-speed trap
Fan noise scales steeply with RPM; CADR scales roughly linearly with
airflow. A unit rated 400 m³/h on high typically delivers:
- high: 400 m³/h, ~55–60 dB
- medium: ~250 m³/h, ~48 dB
- low/sleep: ~100–130 m³/h, ~35–40 dB

On low in a 54 m³ room that's ~2 ACH — fine for dust, useless against a
smoke plume. Strategy: high speed while awake and during peaks; the room
holds fairly well overnight on medium with the door closed.

## 2. PM2.5 reference bands

| PM2.5 (µg/m³, 24-h) | EPA AQI category |
|---|---|
| 0–12 | Good |
| 12–35 | Moderate |
| 35–55 | Unhealthy for sensitive groups |
| 55–150 | Unhealthy |
| 150–250 | Very unhealthy |
| 250+ | Hazardous |

Health basis: PM2.5 penetrates to alveoli; chronic exposure ≥ 35 is
associated with measurable cardiovascular/respiratory mortality risk;
acute wildfire spikes trigger asthma events even in non-asthmatics.
Children, elderly, pregnant people, and cardiopulmonary patients are the
sensitive groups.

## 3. Infiltration physics

Steady-state indoor concentration with filtration:

```
Cin = Cout × Fin / (Fin + λ_unit)
```

- `Fin` = natural infiltration rate (typical 0.3–0.8 ACH for a reasonably
  tight home with windows closed; older homes up to 1.5)
- `λ_unit` = purifier ACH

Example: infiltration 0.5 ACH + purifier 5 ACH → Cin ≈ 0.09 × Cout. A
250 µg/m³ smoke night ≈ 23 µg/m³ indoors — Moderate instead of Very
Unhealthy. Without the purifier (0.5 ACH only): Cin ≈ Cout (steady state
takes hours but gets there).

Practical corollaries:
- **Sealing beats filtering.** Towels at door drafts, tape on window
  frames — every 0.1 ACH of infiltration you remove is CADR you don't
  need to buy.
- **One clean room beats whole-home attempts.** Small bedroom, door
  closed, right-sized purifier: cheapest path to safe sleeping air.
- **HVAC fan ON with a MERV-11+ filter** adds whole-home recirculating
  filtration "for free" (make sure the intake draws NO outdoor air).

## 4. Corsi-Rosenthal box

Invented 2020 (Richard Corsi, air-quality scientist; popularized by Jim
Rosenthal). Build: cube (or 5-sided "filter-drawer") of 20×20×1 MERV-13
furnace filters taped to the intake side of a 20" box fan, exhaust
unobstructed.

Key engineering points:
- **Pressure drop**: MERV-13 at typical face velocity adds ~0.1–0.25 in.
  w.c.; a box fan's static-pressure capability is poor, so effective flow
  is 35–50 % of free-flow CFM. More filters (5–6 sides) = parallel media
  = lower velocity per filter = closer to 50 %.
- **Measured performance** (UC Davis, University of Colorado studies
  2020–2022): 600–900 CFM clean air for a ~1800–2200 CFM fan — better
  than most $300–500 commercial purifiers, for ~$50–70 of parts.
- Do NOT use "high-efficiency" settings; run the fan on high. Expect
  55–65 dB at 1 m.
- Filter change cue: visible gray loading or after several heavy smoke
  weeks (pressure drop climbs as media loads → flow falls).
- Safety: modern box fans are fine for continuous duty; avoid daisy-
  chaining; keep the motor side unobstructed.

## 5. What HEPA does NOT do

HEPA captures **particles** ≥ 0.3 µm at ≥ 99.97 % (and actually finer,
by diffusion/interception). It does **nothing** for:
- VOCs/formaldehyde/smell gases → activated carbon (and carbon saturates;
  it's the first thing to die in a cheap "combo" filter)
- CO, CO₂, NO₂ → ventilation or gas-phase scrubbing
- Radon → soil-gas mitigation

If the concern is smell during smoke events, the particle count can be
near zero while odor persists; that's gas-phase pollution, and the honest
answer is carbon media sized in kilograms, not grams.

## 6. Filter life reality

Rated life (e.g. "12 months") assumes ~8 h/day of modest dust. Real
loading depends on: baseline dust, pet dander, event smoke (each heavy
smoke week ≈ months of normal dust), and run speed. Tracking run-hours
plus smoke-week multipliers gives a defensible change schedule: replace
when effective loading reaches ~80–90 % of rated hours — CADR decays as
the filter loads (a loaded filter can halve delivered clean air before it
"looks" dirty).

## 7. Monitoring

A ~$25–50 laser-scatter PM2.5 monitor (or a purifier's sensor readout)
turns all of the above from theory into feedback: log indoor/outdoor a
few times a day during an event; the diary's I/O ratio tells you whether
your sealing+filtration stack is actually working (target < 0.2 in the
clean room).
