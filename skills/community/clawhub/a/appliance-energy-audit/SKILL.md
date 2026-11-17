---
name: appliance-energy-audit
description: "Use when you want to know which appliances actually drive your electric bill, whether a bill spike is explained by your usage, if standby/vampire draw is worth addressing, whether replacing an old fridge/dryer/AC pays back, or when modeling tiered utility rates — builds a ranked cost-per-appliance table from watts, duty cycle, and usage hours, reconciles it against your real bill, and computes replacement payback."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [energy, electricity, appliances, utility-bill, audit, savings, home]
---

# Appliance Energy Audit

## Overview

Your utility bill says you used 850 kWh last month — but says nothing about *which* device used them. This skill turns a walk-through inventory of your home ("fridge from 2012, gaming PC, window AC…") into a ranked cost table: what each appliance consumes per month and year, what share of the bill it represents, how much pure standby ("vampire") draw is costing, and — when you feed in your actual bill kWh — whether the model matches reality or something is running more than you think.

It also answers the eternal appliance-store question: *is the new efficient model actually worth it?* The `replace` command computes monthly/yearly savings and payback months for any old-vs-new pair at your electricity rate.

## When to Use

- "Which appliances are costing me the most?" / "Why is my electric bill so high?"
- "Is it worth replacing my 15-year-old fridge / electric dryer / AC?"
- "How much do all these always-on devices (router, console, smart speakers) cost me?"
- "My bill jumped — does my usage actually explain it?"
- "I have tiered rates — how does that change the picture?"
- Don't use for: gas appliance costs, whole-house heat-loss modeling, or real-time monitoring (this is an analytical model, not a meter).

## The Model

Each appliance is characterized by four numbers (all have sensible library defaults):

| Field | Meaning | Example |
|---|---|---|
| `watts` | draw when active | 150 W fridge compressor |
| `duty` | fraction of active time it actually draws (compressors cycle) | 0.35 |
| `hours_day` | hours/day it's on | 24 for a fridge, 0.5 for a dryer |
| `standby_w` | idle draw the other hours | 3 W for a TV |

```
monthly_kWh = (watts × hours_day × 30 × duty  +  standby_w × (24 − hours_day) × 30) × qty ÷ 1000
cost        = kWh × rate        (flat)
            = tiered_cost(kWh)  (tiered rate plans)
```

Vampire draw is the standby term summed across appliances. Full derivation and the tiered-rate marginal-cost approximation are in `references/energy-model.md`.

## Commands

```bash
# Browse the 44-appliance preset library (watts, duty, default hours, standby)
python3 scripts/energy_audit.py library

# Quick single-appliance estimate
python3 scripts/energy_audit.py estimate "my dryer,electric-dryer,0.5" --rate 0.25

# Full audit — repeat -a for each appliance, ranked by monthly cost
python3 scripts/energy_audit.py audit -a "fridge,fridge" -a "tv,tv-oled-55,5" \
    -a "bulbs,led-bulb,4,8" -a "gaming pc,gaming-pc,3" --rate 0.17

# From a JSON inventory file, with tiered rates and bill reconciliation
python3 scripts/energy_audit.py audit -f home.json --tiers "0.12:500,0.15:1000,0.20:" --calibrate-to 850

# Model vs actual bill only
python3 scripts/energy_audit.py calibrate -f home.json --bill-kwh 620

# Replacement math: old fridge vs $800 efficient model
python3 scripts/energy_audit.py replace --old "old fridge,fridge" \
    --new "efficient fridge,120,0.3,24" --price 800 --rate 0.17

# See everything at once on sample data
python3 scripts/energy_audit.py example
```

Appliance shorthand: `name[,preset|watts][,hours_day][,qty][,standby_w]` — with a preset, numbers mean hours/qty/standby; without one, the first number is watts. JSON spec files are lists of the same fields in long form (`{"name": ..., "preset": ...}` or `{"name": ..., "watts": ...}`).

## Workflow

1. Inventory your home: walk room to room; for each device run `library` to find its preset or read the nameplate watts.
2. First pass: `audit` with defaults — the preset library already encodes realistic duty cycles.
3. Calibrate: get your bill's monthly kWh, run with `--calibrate-to`. If the model says "undercounted", your heating/cooling or an aging compressor is running harder than rated — raise those `hours_day`/`duty` values and re-run.
4. Act: attack the top of the table. Use `replace` on any aging big-ticket row to get payback months; put high-standby devices (flagged automatically) on switched power strips.
5. Re-check quarterly or after any bill spike — the diff between runs is the story.

## Common Pitfalls

1. **Forgetting duty cycle for compressor appliances.** A fridge is "on" 24 h/day but its compressor runs ~35% of the time. Using duty 1.0 triples the estimate. The presets encode this — prefer them over nameplate watts.
2. **Using nameplate watts as typical draw.** Ratings are peak/startup, not average. A desktop PSU rated 600 W averages ~200 W. Use measured or library values; nameplate only as a last resort.
3. **Ignoring tiered rates when you have them.** On tiered plans the *next* kWh can cost 60% more than the first — flattening to one rate distorts which appliance matters. Pass `--tiers`.
4. **Trusting the model over the bill.** If `calibrate` shows a big gap, the model is wrong somewhere — not your meter. Find the missing/underestimated device (almost always HVAC run-time or water heating) before making purchase decisions.
5. **Double-counting qty.** `-a "bulbs,led-bulb,4,8"` means 8 bulbs at 4 h/day. If you also list bulbs individually you'll count them twice.

## Verification Checklist

- [ ] `python3 scripts/test_energy_audit.py` → ALL TESTS PASSED (63 assertions)
- [ ] `python3 scripts/energy_audit.py library` prints the preset table
- [ ] `python3 scripts/energy_audit.py example` renders a ranked audit + calibration + replace verdict
- [ ] `audit --calibrate-to <bill kWh>` gap is under ±10% before trusting per-appliance numbers
