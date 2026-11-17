---
name: battery-bank-travel-allocator
description: Use when planning battery power for a day out (travel, hiking, festival, conference, photography) — realistic deliverable Wh from power banks after voltage-conversion, heat, age, and cycle derating; per-device demand from screen hours × activity multipliers (navigation, photos, hotspot); stop-charge ceilings; over/under-provisioned verdicts and solar-panel yield reality check.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [power-bank, battery, travel, packing, usb-c, energy-budget, hiking]
---

# Battery Bank Travel Allocator

The "20000 mAh" printed on a power bank is cell capacity at 3.7 V —
your phone charges at 5 V, conversion and cable heat eat 10–15%, the
bank has aged 4%/year, and fast-charge protocols waste more. Realistic
delivery is ~60–65% of the sticker, worse on old banks. Meanwhile the
demand side is equally misunderstood: 5 hours of navigation drains a
phone 3.5× faster than 5 hours of light use, and charging a phone to
100% from a bank spends its least efficient energy on your least
needed percent.

This skill runs the honest budget both ways: what your banks can
actually deliver today, what your devices will actually consume given
the day's plan, and the verdict — with the counter-intuitive calls
included (leave the big bank home; the small one clears the day).

## When to Use

- Packing for a long day away from outlets: travel, hike, festival,
  conference, photo shoot, flight with connections
- "Will this bank keep my phone alive all day?" — the canonical
  question, answered with the real math
- Choosing which bank(s) to bring (or buying a first one — the
  real-capacity table shows what each size actually delivers)
- Deciding if a solar panel is a real solution or backpack jewelry
- Diagnosing why an old bank "doesn't hold anything anymore" — age +
  cycle derating math

**Don't use for:** laptop sizing over USB-PD for multi-day work trips
(the laptop model here is coarse); UPS/battery-backup sizing for home
electronics — different chemistry, different duty cycle.

## The Physics

| Factor | Model |
|---|---|
| Voltage conversion | rating at 3.7 V cell → delivered at 5 V: × 3.7/5 = ×0.74 |
| Conversion + cable + heat | × 0.85 |
| Age | −4% per year of design capacity |
| Cycles | ~8% per 500 cycles, capped at 20% |
| Net realistic transfer | ≈ 60–65% of rated mAh for a new bank |
| Screen-on drain | phone ≈ 7–9%/h baseline |
| Activity multipliers | navigation ×3.5, video ×2.5, hotspot ×2.8, photos ×1.6, gaming ×4, offline-maps ×1.8 |
| Idle/background | ≈ 1%/h radios on (airplane mode cuts to ~0.3) |
| Stop-charge ceilings | phone 85%, tablet/watch 90% — charging past wastes bank Wh at the worst efficiency |

## Commands

```bash
# day plan: banks, then devices with hours/activity/starting charge
python3 scripts/power_budget.py plan \
  --banks 20000:2 10000:0 \
  --devices phone:5:80:navigation phone-big:3:100:photos earbuds:0:40 \
  --hours 12

# what sizes actually deliver
python3 scripts/power_budget.py banks

# solar reality
python3 scripts/power_budget.py solar --watts 21 --sun-hours 4
```

Device syntax: `device[:screen-hours:start-pct:activity]`. Supported:
phone, phone-small, phone-big, tablet, camera, earbuds, watch,
laptop-usb, drone.

## Reading the Verdict

- **OVER-PROVISIONED** — banks ≥ 1.2× demand: leave the biggest bank
  home, pocket space is the scarce resource
- **FITS** — margin exists but thin: charge priority device first,
  expect ~15% protocol waste beyond the model
- **SHORTFALL** — named fixes: airplane mode + offline maps (−60%
  phone drain), lunch-stop wall plug, or cut the lowest-priority
  device from the charge list

## Common Pitfalls

1. **Believing rated mAh is delivered mAh.** The 0.74 voltage factor
   alone means a "20000" bank tops out near 14800 mAh at 5 V before
   any other loss.
2. **Ignoring bank age.** A 3-year-old daily-cycled 20000 delivers
   about what a new 10000 does. Model it: `--banks 20000:3`.
3. **Charging devices to 100%.** The last 15% of a phone charge is
   the slowest and least efficient transfer; when the bank is the
   source, 85% is the rational ceiling.
4. **Forgetting idle drain.** 12 hours away with radios on costs
   ~12% of the phone by itself; a full day conference with poor
   signal (radio hunting) can double that.
5. **Solar sticker faith.** A 21 W panel yields its rating only
   midday-and-perpendicular; backpack-hanging averages 10–25% over a
   day. The `solar` subcommand derates by 50% even in the optimistic
   case.
6. **Cables as bottlenecks.** A worn cable can halve throughput and
   pad every charge with waste heat — the model assumes a healthy
   short cable; your mileage collapses with the tangled 2 m one.

## Verification Checklist

- [ ] Every device modeled with its real activity, not "light" for
      everything (navigation vs light is a 3.5× error)
- [ ] Bank ages included for anything over a year old
- [ ] Verdict read with the ×1.2 safety margin in mind
- [ ] Charge order set: priority device first, 85% ceilings
- [ ] Airplane-mode plan for stretch scenarios

## References

- `references/energy-model.md` — the full loss chain with numbers,
  device battery library, activity multipliers, airline rules for
  big banks, and cold-weather derating.
