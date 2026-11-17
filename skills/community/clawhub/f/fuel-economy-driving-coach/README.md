# Fuel Economy Driving Coach

**"Drive gentler, save gas" is true and useless.** The useful form is arithmetic: every driving habit has a dollar price for *your* mileage and gas price — and the ranking flips depending on your numbers. This tool computes it.

## The Problem

Generic fuel-saving lists treat all drivers the same. But a roof box costs a 25k-mile/year highway commuter **$300+/yr**, while the same box on a Sunday errand car costs pocket lint. Meanwhile people pour fuel additives into tanks (0% effect, proven repeatedly) while driving on tires 8 psi low (+3-4%, free to fix). Without pricing habits at *your* numbers, the advice is noise.

## What It Does

```bash
python3 scripts/fuel_coach.py audit --mpg 30 --price 3.50 --miles 15000
# Ranked $/yr for every habit: aggressive driving, 75-vs-65 mph, roof box,
# idling, underinflation, cold starts, trunk weight, AC discipline...

python3 scripts/fuel_coach.py floor --weight-lb 3400 --cd 0.30 --frontal 24 --mpg 30
# Physics floor from aero (½ρCdA v³) + rolling resistance at 22% tank-to-wheel.
# Shows how far above the physics minimum you run — 1.5-2.5x is normal life.

python3 scripts/fuel_coach.py trip --miles 400 --mpg-high 34 --speed-a 65 --speed-b 75
# "Is it worth driving faster?" -> $/hour of going faster. If your time is
# worth more than that number, floor it; otherwise you're burning cash.

python3 scripts/fuel_coach.py diagnose --was 32 --now 27.5
# Sustained MPG drop routed through 8 causes ranked by likelihood × cheapness.
```

## Example Output

```
YOUR BASELINE: 15000 mi/yr @ 30 MPG, $3.50/gal = 500 gal = $1750/yr

Aggressive driving (jack-rabbit + hard braking)   $175-$700/yr
Highway 75 instead of 65 mph                      $ 70-$131/yr
Roof box/cargo box mounted (unused)               $ 88-$219/yr
...
Top-3 realistic capture: ~$577/yr
```

## The Honest Physics

- Aero drag rises with the **cube** of speed — 75 vs 65 mph costs 8-15% of highway fuel; minutes saved are linear, fuel is cubic.
- Idling burns 0.3-0.6 gal/h for zero miles. 10 min/day = $110-220/yr.
- Every 1 psi under placard = +0.4% consumption; 8 psi low also destroys tire shoulders.
- Winter MPG drops 8-12% from fuel blend + warm-up — that's normal, not a broken car.
- **No bottled additive has ever survived an EPA test.** Fix the free stuff first.

## Who Needs This

Commuters pricing a route/schedule change, road-trippers deciding cruise speed, families deciding roof box vs hitch rack, anyone with a sudden MPG drop wanting the ranked cause list before a shop upsells them, and hybrid/EV-curious drivers running honest payback math at their real mileage.

## License

MIT © Denis Voronin
