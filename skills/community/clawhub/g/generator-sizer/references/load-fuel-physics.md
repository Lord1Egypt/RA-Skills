# Generator Sizing — Load & Fuel Physics (Reference)

## 1. The two watts: running vs starting

Every load has:

- **Running (continuous) watts** — what the nameplate says, what it draws
  in steady state.
- **Starting (surge) watts** — the extra inrush for 1–3 seconds when a
  motor starts. Resistance-split phase motors (fridge compressors, well
  pumps, furnace blowers) need 2–3× running; some deep-well pumps with
  pressure tanks hit 3× for up to 5 seconds.

| Load | Running W | Surge × | Tier |
|---|---|---|---|
| Refrigerator (18 cu ft) | 150–250 | 3.0 | 1 |
| Chest freezer | 150–250 | 3.0 | 1 |
| Sump pump ½ HP | 800–1050 | 3.0 | 1 |
| Well pump ½ HP (240 V) | 1000 | 3.0 | 1 |
| Furnace blower (gas) ½ HP | 600 | 3.0 | 1 |
| Medical: CPAP | 50–120 | 1.0 | 1 |
| Medical: oxygen concentrator | 300–550 | 1.5 | 1 |
| Pellet stove | 400 | 1.5 | 1 |
| Microwave | 1000–1500 | 1.0 | 2 |
| Coffee maker | 900–1200 | 1.0 | 2 |
| Electric water heater | 4500 | 1.0 | 3 (rarely worth it) |
| Window AC 10k BTU | 900–1200 | 3.0 | 2 |
| Lights (10 × LED) | 100 | 1.0 | 1 |
| Router + modem + phone charging | 50–80 | 1.1 | 1 |
| TV 55" | 120 | 1.1 | 2 |
| Laptop | 65 | 1.0 | 2 |
| Garage door opener ½ HP | 600 | 2.5 | 3 |

## 2. The sizing equation

Sizing rule used by the script:

```
required_continuous = sum(running_watts)          # everything you'll run
surge_event = base_nonmotor + max_motor_surge
              + running of other motors
required_surge_capacity ≥ surge_event
```

Buy to: `generator_continuous ≥ required_continuous × 1.15` (15% headroom,
motor aging, altitude) and surge rating ≥ surge_event.

## 3. Generator classes and what they honestly run

| Class | Continuous (real) | Runs |
|---|---|---|
| 2,000 W inverter | 1,600–1,700 W | Fridge + lights + router + CPAP. Nothing else. |
| 3,500 W | 3,000 W | + sump pump OR furnace blower (not both starting together) |
| 7,500 W | 6,000 W | + well pump, microwave, window AC, TV — a real house's outage kit |
| 10–13,500 W | 8–11,000 W | Most of a house minus range/dryer/water heater |
| 22 kW standby + ATS | whole home | Everything (with load-shed controller) |

Altitude derate: −3% per 1,000 ft above sea level (gasoline).

## 4. Fuel physics

Gasoline (typical open-frame unit, loaded):

```
gal/h ≈ 0.05 + 0.095 × delivered_kW
```

- 7,500 W class at 50% load (3 kW) ≈ 0.34 gal/h → ~5.5 h on a 1.9-gal
  tank, ~15 gal/day.
- Inverter class at ¼ load throttles down: 2,000 W class ≈ 0.10–0.15
  gal/h → 10+ h on 1.1 gal.

Propane: ≈ 2× the gallons of gasoline for the same energy (91,500 BTU/gal
vs 114,000), and a 20 lb tank holds 4.7 gal. Derate output ~10% on propane.

Storage reality: gasoline stale in 3–6 months (use stabilizer, rotate
yearly); propane stores indefinitely — the strongest argument for
tri-fuel.

## 5. Safety gates (non-negotiable)

1. **CO:** outdoors, 20+ ft from windows/doors/vents, exhaust pointed
   away. Never garage/porch/deck/crawl space. Battery CO alarm indoors on
   the floor where people sleep. CO is the #1 storm-death mechanism after
   the storm itself.
2. **No backfeed.** Power into home wiring ONLY via transfer switch or
   listed breaker interlock. Backfeeding a 240 V dryer outlet can
   energize the line side and kill a lineman.
3. **Cords:** outdoor-rated, gauge for length and amps, no coiled cords
   under anything.
4. **Dry hands / dry ground** when connecting; generator bonded neutral
   matters with a transfer switch (consult electrician).
5. **Sensitive electronics:** non-inverter gensets run 15–25% THD; CPAP,
   oxygen concentrators, modern furnaces prefer inverter-class power.

## 6. Staggered-start doctrine

Sequence motors so no two surges overlap:

1. Start generator, let stabilize 5 min.
2. Largest motor first (well pump / furnace blower) — the hardest start.
3. Then sump, then fridge, then freezer (their cycles will interleave
   naturally; that's fine — cycles aren't starts).
4. Non-motor loads last.

## 7. Storm-duration fuel planning

Plan = (gal/h at your load fraction) × storm hours × 1.25 reserve.
Ice storms and hurricanes both trend to 48–96 h outages in bad years:
that's 30–60 gal of gasoline or 60–120 gal of propane for a 7,500 W
class at mixed load. This is the number that decides tri-fuel.
