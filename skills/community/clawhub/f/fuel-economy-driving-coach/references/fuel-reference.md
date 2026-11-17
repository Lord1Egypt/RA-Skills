# Fuel Economy — Reference & Sources

## Where the bands come from

- **Aggressive driving 10-40% city / ~15% highway**: US DOE fueleconomy.gov "Driving More Efficiently" ranges.
- **Aero v³**: drag power P = ½ρ·CdA·v³. Between 65 and 75 mph the fuel-speed exponent empirically lands 2.0-2.5 (not pure 3.0, because rolling resistance and engine efficiency shift with operating point). The script uses 2.2 as the empirical midband.
- **Idle 0.3-0.6 gal/h**: EPA; larger engines toward the top.
- **Roof box +10-25%**: DOE/SAE studies of roof-mounted cargo; the drag penalty dwarfs the weight.
- **1 psi low ≈ +0.4%**: NHTSA/DOE rule of thumb; additionally wears shoulders and raises heat.
- **AC 3-10%** (compressor load), **open windows at speed 2-5%**: crossover ~45-55 mph depending on car aero.
- **Winter penalty 8-12%**: winter-blend gasoline (butane %, lower energy density), longer warm-up enrichment, cold-air density, tire rolling resistance at low temp.
- **Tank-to-wheel 20-25%** (spark ignition), 30-35% diesel; hybrids stretch effective efficiency via Atkinson cycle + regen, especially city.

## Honest expectations

| Car class | Typical combined | Physics-floor multiple |
|---|---|---|
| Midsize sedan | 30 | ~1.6-1.9x |
| Compact hatch | 34 | ~1.5-1.8x |
| Body-on-frame SUV | 20 | ~1.4-1.7x |
| Full-size pickup | 18 | ~1.4-1.6x |
| Hybrid compact | 52 | ~2.2-2.6x (floor model unfair to hybrids: regen) |

If your logged 3-tank average sits inside your class band, the car is fine and only habits/maintenance can move it. If it's 25%+ worse than class, route the diagnosis list.

## Maintenance items with REAL mpg effects (vs mythology)

| Item | Real effect | Myth status |
|---|---|---|
| Tire pressure | +3-4% when 8 psi low | Real, free |
| Oxygen sensor (aged) | 10-15% | Real; often silent |
| Dragging brake | 5-25% | Real; hub heat test |
| Thermostat stuck open | 5-12% | Real; temp gauge barely mid-band |
| Air filter | ~0% on modern EFI (flow-metered) | Mostly myth post-1996 |
| Fuel additives | 0% | Myth, full stop |
| "Premium clean" treatments | 0% | Myth |
| Oil viscosity vs manual | 0.5-1.5% | Marginal; follow manual |

## The speed-minutes table (400-mile day, 34 MPG car @65)

| Speed | Time | Fuel @ $3.50 | Effective $/hr of going faster |
|---|---|---|---|
| 60 | 6h40 | $38.9 | — |
| 65 | 6h09 | $41.2 | $8.4/hr (60→65) |
| 70 | 5h43 | $43.8 | $11.7/hr (65→70) |
| 75 | 5h20 | $46.6 | $14.9/hr (70→75) |
| 80 | 5h00 | $49.7 | $19.3/hr (75→80) |

Read: if your time is worth more than ~$15/hr, driving 70-75 is rational; if not, it's burning money. Ticket risk is a separate column.

## Trip logging template

Per tank (or per trip): date, odometer, gallons (same pump, same cutoff), miles, notes (route / load / weather / trailer / new tires). Compute MPG per entry; keep a 3-entry rolling average. Any change evaluated against that average — not against a memory.

## Hybrid/EV notes (out of core scope)

- Hybrids reward smooth anticipation because regen recaptures braking; aggressive driving hurts them LESS on highway, MORE in city (relatively).
- EVs: habits move range 20-30% (speed, climate, cold), but "fuel" cost per mile is 3-5x cheaper — coach economics don't transfer.
- PHEV drivers: the payoff is all in charge discipline; treat gas mode as failure mode.

## Fuel purchase strategy (minor, real)

- Wholesale clubs / cash discounts: $0.05-0.15/gal typical = $25-75/yr at 500 gal/yr. Real but small; don't drive extra miles for cheaper gas (a 2-mile detour burns the saving).
- App-based price check before fillups (GasBuddy etc.) saves ~$0.08/gal with zero detours.
-_octane_: follow the manual. "Premium recommended" usually tolerates regular at slight power cost; "premium required" means it.
