# Generator Sizer

**The "7500 watts" on the box is not what you can run.** It's surge
rating; the honest continuous number is ~20% lower, and the appliances
that matter in an outage are motors that need 2–3× their running watts
just to start.

## The Problem

- A fridge drawing 200 W needs 600 W for two seconds when the compressor
  kicks in. A ½ HP well pump at 1,000 W running needs 3,000 W to start.
- Size the generator by running watts alone and it stalls the first time
  the sump pump and fridge start in the same second.
- Runtime quotes are at 25% load. Real plans burn 2–3× that; a 48-hour
  outage on a 7,500 W unit needs ~20 gallons of gasoline nobody has.
- Any 240 V load (well pump, furnace) connected to house wiring without
  a transfer switch is a backfeed hazard that kills line workers.

## What This Skill Does

`scripts/generator_sizer.py` — appliance-by-appliance load sheet with
starting-surge multipliers, priority tiers, worst-case surge event,
generator class verdict (2k inverter → 22 kW standby), fuel burn per
hour and per storm at your real load fraction, elevation derate, and
safety gates (transfer-switch flag, CO rules, medical-grade power):

```bash
python3 scripts/generator_sizer.py \
  --appliances fridge freezer sump-pump furnace-blower lights-10 router \
  --storm-hours 48

python3 scripts/generator_sizer.py \
  --appliances fridge well-pump furnace-blower lights-10 \
  --generator-watts 3500 --check-only   # will my 3.5kW carry this?
```

## Who Needs This

- Storm-belt households (ice, hurricanes) planning backup power
- Rural homes on well pumps — the load that forces a generator class jump
- Anyone buying a generator who doesn't want to discover the surge trap
  mid-outage
- People with CPAP/oxygen concentrators needing clean inverter power

## Example

Fridge + freezer + sump + furnace blower + 10 LED lights + router =
2,060 W running. But the worst surge event (sump starting while the
fridge/freezer/blower run) is 3,560 W → required continuous ≈ 2,370 W
→ a 3,500 W class unit fits with margin *only if* starts are staggered;
add a well pump and you're in 7,500 W territory. At 30% load on that
unit: ~0.19 gal/h → 11–12 gal for a 48 h storm. The script prints
exactly this.

## Safety

Generators kill more people after storms than the storms do — almost all
from carbon monoxide. Outdoors, 20+ ft from any opening, battery CO
alarm indoors. Transfer switch or interlock for anything wired into the
house. Never backfeed.

## License

MIT — see LICENSE.
