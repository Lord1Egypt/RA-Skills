# EV Road-Trip Charging — Model and Field Notes

Reference for `scripts/evroadtrip.py`.

## 1. Where the energy goes (highway)

At 110–130 km/h the battery feeds, roughly:
- **Aero drag**: 55–65% of energy, growing with the SQUARE of speed
  (power ~v³ per km: +18% speed ≈ +35% energy per km).
- **Rolling resistance + drivetrain losses**: 20–25%.
- **HVAC**: 0 in a warm cabin at 20°C ambient; up to 4–7 kW sustained at
  −10°C (resistive) or 2–3 kW (heat pump).
- **Elevation**: 1% SoC per ~12 m of climb for a 2-ton car (regen recovers
  ~60% of it on the way down).

Practical per-class highway consumption at 20°C, 115 km/h (Wh/km):
compact 140–155 · sedan 155–175 · SUV/crossover 185–210 · truck/large-van
215–240. Cold derates add: heat pump +0.6%/°C below 18°C, resistive
+1.4%/°C. So the same SUV: 195 at +20°C, ~226 at −8°C with heat pump,
~270 resistive.

## 2. DC fast-charge reality

- Nameplate kW is a **peak** at ideal SoC/temperature. Average 10→80% power
  ≈ 0.70–0.80 × min(station, vehicle) after taper and thermal derates.
- Taper: most 400V cars hold peak to ~30–40% then taper; above 80% expect
  ≤ half of peak; above 90% often <30 kW. Hence the 80% doctrine.
- **Paired stalls**: two cables on one cabinet share power — parking at a
  paired stall with a neighbor already charging can halve your rate.
- **Cold gate**: below ~5°C pack temp, DC rate collapses until the pack
  warms; preconditioning while driving to the charger is the fix (start
  20–30 min out when the charger is the active nav target on most brands).
- Plug formats: CCS1 (NA non-Tesla), CCS2 (EU), NACS/Tesla (NA + growing),
  CHAdeMO (dying, adapters). Adapter rules: NACS→CCS1 works for most
  2023+ cars at Tesla Superchargers (Magic Dock / adapter programs);
  check your car's approval list — charging speed via adapter can be capped.

## 3. Planning doctrine

- **Buffer floors**: arrive ≥10% SoC at every DC stop; ≥15–20% at the last
  stop of the day; +5% to all floors when temp < 0°C or mountain grades.
- **Charge windows**: 10→80% is the fast zone. 80%+ only when the next leg
  is long AND the stop is a meal anyway (overlap wasted time with needed
  time).
- **Stop cadence**: 2.5–3 h driving ≈ one 20–30 min stop matches human
  comfort anyway; EV plans that fight biology lose.
- **Night rule**: arrive at hotel < 20% is fine ONLY with confirmed L2
  (7–11 kW = full by morning). Confirm the EVSE in photos/reviews, bring a
  portable 2–5 kW fallback cable for emergency top-ups.
- **Cost**: DC at $0.40–0.60/kWh ≈ 2–3× home charging but still ~$0.11–0.14
  per km for an efficient EV — comparable to a 40 MPG gas car at $4/gal.
  Apps: plan around one wallet per network (NA: Tesla, EA, EVgo, ChargePoint,
  Shell Recharge; EU: various — check roaming).

## 4. Route selection heuristics

- Prefer corridors with 2+ networks even if slightly longer — redundancy
  beats a broken lone charger.
- 150 kW minimum useful DC on a road trip; 50 kW stalls only as emergency.
- Urban chargers = congestion and idle fees; highway-adjacent = clean in/out.
- Check the charger's LAST status (apps show 24–48 h): a dead stall list
  beats a star rating.

## 5. Emergency margins

- If arrival SoC would breach the floor: slow down 10–15 km/h (−10–15%
  consumption), drop HVAC to seat heaters only (−1–2 kW), draft nothing,
  and take the earlier charger.
- Tow coverage: many roadside plans now include EV tow-to-charger; know
  your program before the trip.
