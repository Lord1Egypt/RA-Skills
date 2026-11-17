# Appliance Energy Audit ⚡

**Your electric bill tells you how much you spent. This tells you *what did it* — and what to do about it.**

## The problem

The average home runs 30–60 electrical devices, and the utility bill lump-sums them into one opaque number. When the bill spikes, you have no way to know whether it was the summer AC hours, the ancient second fridge in the garage, or the new gaming PC. And every appliance showroom pushes "energy efficient" upgrades with payback claims you can't verify.

Real audits cost $100–400 when a professional walks your home with a clipboard. Smart plugs and home monitors ($150+) measure only the devices they're attached to, and need months of data before they say anything.

## The solution

A bottom-up physics model you can run in 10 minutes:

```bash
# What does my home actually spend, ranked?
python3 scripts/energy_audit.py audit -a "kitchen fridge,fridge" \
  -a "garage freezer,chest-freezer" -a "window AC,ac-window-12k,6" \
  -a "gaming PC,gaming-pc,3" --rate 0.17
```

```
appliance                        kWh/mo    $/mo    $/yr  share   qty
---------------------------------------------------------------
garage freezer                    45.4    7.71   92.52   27.9%     1
window AC                         44.6    7.58   91.00   27.4%     1
gaming PC                         43.2    7.34   88.08   26.5%     1
kitchen fridge                    37.8    6.43   77.16   23.2%     1
---------------------------------------------------------------
TOTAL                            171.0   29.06  348.72
```

- **44-appliance preset library** with realistic duty cycles — a fridge's compressor runs ~35% of the time, not 100%; models built from nameplate watts alone overstate 2–3×.
- **Calibration against your real bill** — feed in your monthly kWh and the tool tells you whether the model undercounts (something runs harder than you think) or overcounts, with concrete hints.
- **Vampire-draw detection** — standby load is computed per device and totals to the "always-on tax" a power strip would kill.
- **Tiered-rate support** — on tiered plans the tool prices the whole month through your actual rate structure, not a flat average.
- **Replacement payback** — old vs new appliance, savings per month/year, payback in months:

```bash
python3 scripts/energy_audit.py replace --old "old fridge,fridge" \
  --new "efficient fridge,120,0.3,24" --price 800
# saves 22.7 kWh/mo ≈ $46.31/yr → payback 172.7 months → NOT worth it for a working fridge
```

## Who needs this

- Anyone whose bill jumped and wants to know why before calling an electrician
- Households deciding whether the efficient model is worth the premium
- People hunting phantom loads from consoles, PCs, and always-on gear
- Landlords and tenants splitting or disputing utility costs
- Anyone on tiered rates trying to understand marginal kWh pricing

## Install & test

Stdlib-only Python 3, no dependencies:

```bash
python3 scripts/test_energy_audit.py   # 63 assertions
python3 scripts/energy_audit.py example
```

MIT © 2026 Denis Voronin
