---
name: concrete-contractors-estimator
description: "Concrete contractors estimator: work out cubic yards for a slab, driveway, patio, footing, round column or steps with a waste allowance, the ready-mix order quantity, 80/60/40 lb bag counts, rebar or wire-mesh quantities, a rough installed cost range, and a hot-weather pour plan (start time, tips, cure schedule). Use when someone asks how much concrete or how many bags they need, how much rebar to buy, what a slab might cost, or when and how to pour in the heat."
version: 1.0.0
homepage: https://concretecontractorsphoenix.net/
metadata:
  openclaw:
    emoji: "🏗️"
    homepage: https://concretecontractorsphoenix.net/
---

# Concrete Contractors Estimator

Instruction-only: no commands, installs or network access. Collect the measurements, do the arithmetic
below yourself and show the working so the user can check it.

## Purpose

Give homeowners, DIYers and small crews the same take-off concrete contractors do before a pour: how much
concrete to order, how many bags that is, how much steel, a rough price and how to plan the pour day in heat.

## When to use

- "How many yards of concrete for a 24 x 12 ft driveway, 4 inches thick?"
- "How many 80 lb bags for four 12 inch sonotubes, 4 ft deep?"
- "How much rebar do I need for a 20 x 10 patio at 18 inches on center?"
- "What would a 400 sq ft stamped patio roughly cost?"
- "It will be 108 F on Saturday in July. Should we still pour, and when?"

## Inputs

Ask only for what is missing. Defaults in brackets.

- Shape: slab / driveway / patio, footing, round column, or steps
- Slab: length ft, width ft, thickness in [4; driveways 4-6]
- Footing: total length ft, width in, depth in
- Column: diameter in, height ft, count [1]
- Steps: number of steps, rise in [7], run in [11], width ft
- Waste allowance [10 %]
- Slab extras: rebar spacing in [18], finish broom / colored / exposed / stamped [broom], removing old concrete? [no]
- Pour day: forecast high in F, month

## Procedure

1. Volume in cubic feet:
   - slab: L x W x T / 12
   - footing: L x (W / 12) x (D / 12)
   - column: 3.14159 x (D / 24)^2 x H x count
   - steps (solid, on grade): W x (run / 12) x (rise / 12) x n(n+1)/2
2. With waste: V = volume x (1 + waste). Cubic yards = V / 27, rounded to 2 decimals.
   Order quantity = yards rounded **up** to the next 0.25 yd.
3. Bags (round up): 80 lb = V / 0.60, 60 lb = V / 0.45, 40 lb = V / 0.30.
   Under 1 cubic yard suggest bags; 1 cubic yard or more suggest ready-mix.
4. Rebar grid for a slab at spacing S inches: bars along the length = floor(W x 12 / S) + 1, each L ft;
   bars along the width = floor(L x 12 / S) + 1, each W ft. Linear feet = sum. 20 ft sticks = ceil(LF x 1.10 / 20).
   Welded-wire alternative: ceil(area x 1.10 / 50) sheets of 5 x 10 ft.
5. Rough installed cost (USD per sq ft): broom 6-10, colored 8-13, exposed aggregate 9-14, stamped 12-20.
   Above 4 in thick multiply by 1 + 0.10 x (T - 4). Removing old concrete adds 2-4 per sq ft. Round to whole dollars
   and say it is a planning range, not a quote.
6. Pour day from the forecast high:
   - under 90 F: low risk, any time, finish before the afternoon peak
   - 90-99 F: moderate, start by 7:00 am
   - 100-109 F: high, start 5:00-6:00 am and finish by 10:00 am
   - 110 F and up: extreme, reschedule if possible; otherwise start at first light and finish by 9:00 am
   Tips build with the heat: never add water at the truck; at 90+ pre-wet subgrade and forms and have the crew ready;
   at 100+ ask for a set retarder, keep the mix under 90 F, use shade or windbreaks; at 110+ split the pour.
   Always start curing right after finishing (curing compound, wet burlap or plastic, moist 7 days).
   June to September add a monsoon note: watch storm cells, keep plastic on site, route runoff away.
   Cure schedule: foot traffic after 2 days, vehicles after 7, design strength at 28.

## Outputs

A short answer with: cubic feet and yards (with waste), order yards, bag counts, the bags vs ready-mix call,
rebar or mesh (slabs), the cost range (slabs), and the pour-day plan if a forecast was given. Show each formula
with the user's numbers.

Worked example: 20 x 10 ft slab, 4 in, 10 % waste -> 66.67 ft3 x 1.10 = 73.33 ft3 = 2.72 yd3, order 2.75 yd3;
123 x 80 lb bags; rebar 7 + 14 bars = 280 ft = 16 sticks; broom finish $1,200-$2,000.

## Reference

The same formulas ship as packages (npm, PyPI, crates.io, pub.dev, NuGet, RubyGems, Packagist):
https://github.com/nbkdevs/concrete-contractors-phoenix

## Links

- Concrete driveways, patios, stamped concrete and repairs planned for desert heat: [Concrete Contractors Phoenix](https://concretecontractorsphoenix.net/)
