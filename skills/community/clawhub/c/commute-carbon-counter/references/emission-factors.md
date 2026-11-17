# Emission Factors — Sources, Ranges, and Honesty

## What the numbers are

All factors are **grams of CO2 per passenger-kilometre** (well-to-wheel where the source
provides it), representing fleet/occupancy **averages**, not any specific vehicle. They
are planning-grade: right for comparing modes and tracking your own trend, wrong for
certified carbon accounting.

## The table used by `commute_carbon.py`

| Mode | g/pkm | Basis |
|---|---|---|
| car (ICE, solo) | 192 | ~170 g/km tailpipe for average fleet + upstream fuel, × low occupancy (1.2–1.5) |
| carpool | 192 ÷ passengers | same car, split per head — a 3-person carpool ≈ 64 g/pkm |
| ev | 53 | ~180 Wh/km consumption × grid intensity ~300 g/kWh average grids; hydro grids → ~10, coal grids → ~150 |
| motorcycle | 103 | smaller engine, worse everything else |
| bus (urban) | 97 | diesel urban bus at ~10–15 pax average load |
| coach (intercity) | 27 | full-ish express buses are among the best land modes |
| metro | 35 | electric heavy rail, includes station/aux loads |
| tram | 30 | light rail, similar logic |
| train (regional) | 41 | diesel+electric mix, moderate occupancy |
| bike / walk | 0 | no fuel; food-cycle emissions treated as diet-neutral here |
| e-bike | 5 | ~1 Wh/km charging losses included |
| e-scooter (shared) | 8 | charging + rebalancing/collect vans included |
| plane (short-haul) | 255 | per economy passenger-km, no RFI multiplier |

## Why ranges in sources are wide

- **Occupancy is everything for shared modes.** A near-empty diesel bus can exceed a
  solo car per passenger; a full one beats a bike courier. The numbers above assume
  real-world average loads.
- **Grid carbon intensity** swings EV/e-rail/tram factors by 10× between Norway and
  Poland. If you know your local grid g/kWh, scale electric modes by
  `factor × (your_g_per_kWh / 300)`.
- **Manufacturing** (especially battery production) is excluded from day-to-day factors
  by convention — it's a one-time amortized cost, not a per-trip decision variable. For
  an EV it adds roughly 5–15 t CO2 upfront, amortizing to ~10–20 g/pkm over vehicle life.
- **Radiative forcing** from aviation (contrails, NOx at altitude) is excluded; with a
  ~1.9× multiplier the short-haul figure would approach 480 g/pkm. Planes remain the
  worst mode either way.

## Personal budget framing

The default budget (1000 kg CO2/yr for personal transport) roughly reflects the
"1.5°C lifestyle" literature for mobility in developed economies (total personal
footprint target ~2.5 t/yr by 2030, of which transport is a large slice). It is a
deliberately ambitious anchor, not a scientific allocation. Set your own with `--budget`.

Tree equivalence uses ~21 kg CO2 per urban tree per year — a commonly cited range is
20–25 kg for a mature street tree. It's a communication device, not a sequestration plan.

## Source synthesis

Factors are triangulated from: UK DEFRA/BEIS GHG conversion factors (company
reporting), European Environment Agency rail/road averages, US EPA automotive trends,
and peer-reviewed LCA meta-analyses for e-scooters/e-bikes. Individual sources differ
by ±30% on any single mode; the *ordering* of modes (walk < bike < rail < bus < car <
plane) is robust across all of them.

## What this tool deliberately does NOT do

- No Scope 1/2/3 accounting or GHG Protocol alignment
- No offset calculation you should buy credits against
- No per-vehicle lookup (your 2010 V8 differs from the fleet average)
- No flight-class differentiation (first class ≈ 2× economy per pkm)

If a decision needs certified numbers — regulatory reporting, offsets, corporate
commute programs with money attached — get measured data. If a decision is "should I
take the metro two days a week" — this is exactly the right tool.
