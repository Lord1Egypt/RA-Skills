---
name: bike-theft-shield
description: "Use when a bike might be stolen (locking up in a city, buying a lock) or HAS been stolen. Grades lock setups against theft-area risk, builds a serial/photo registry BEFORE theft, and prints the first-72-hours stolen-bike playbook: police report, registry flags, marketplace sting searches, insurance claim."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [bike, security, theft, urban, insurance, recovery]
---

# Bike Theft Shield

## Overview

Roughly **2 million bikes are stolen every year in North America alone**, and the recovery rate is dismal (<3% for unregistered bikes) — not because bikes vanish, but because owners can't produce a serial number in the first hour, and stolen bikes are resold within 48 hours on marketplace apps. Prevention and recovery are both *systems*, not products: a lock graded for the parking location, a registry entry that survives the theft, and a pre-built playbook that fires in the first 72 hours while the bike is still local.

This skill has three modes: **harden** (lock audit + locking protocol + registration), **register** (serial + photo evidence file, stored locally as JSON), and **stolen** (the 72-hour recovery playbook with report templates and sting-search setup).

## When to Use

- Moving to / commuting in a city, or parking a bike outside overnight anywhere
- Buying a lock or judging whether the current lock survives the parking spot
- Buying a used bike (check it isn't stolen — serial + registry check)
- **A bike was just stolen** — run `stolen` immediately
- Don't use for: motorbike/scooter theft (different registries and locks), inside-home storage audits only.

## Quick Start

```bash
# 1. Is my lock good enough for where I park?
python3 scripts/bikeshield.py audit --bike-value 1400 --area-risk 4 \
  --locks "kryptonite evolution u-lock; cable"

# 2. Register the bike BEFORE anything happens (serial + photo checklist)
python3 scripts/bikeshield.py register add --make "Trek" --model "Marlin 7" \
  --year 2023 --color "Black" --value 1400 --serial "WTU123A4567"
python3 scripts/bikeshield.py register photos trek-marlin     # what to photograph

# 3. THEFT: first 72 hours playbook
python3 scripts/bikeshield.py stolen --bike-file bikes.json --hours-ago 2

# 4. Used-bike purchase check
python3 scripts/bikeshield.py check --serial "WTU123A4567"
```

## Lock Grading Model

| Rating (Sold Secure / ART) | Resists | Fails to | Suitable area risk |
|---|---|---|---|
| Diamond | 60s+ angle grinder attack, all hand attacks | sustained cordless grinder x2 | 4–5 (city cores, overnight) |
| Gold (≈ART 4) | bolt croppers to 42", leverage, hammers | 1 grinder ~1–2 min | 3–4 (commuter parking, daytime) |
| Silver (≈ART 2–3) | basic hand attacks, small croppers | big croppers, grinders | 2 (campus, short stops) |
| Bronze / cable / combo | opportunistic tugs only | literally everything else | 1 (in-sight only) |

Spending doctrine: **lock budget ≈ 10–15% of bike value** in risk 3+, always as a *pair* (primary U/chain + secondary for wheels), because a single lock leaves a quick-release wheel or seatpost as the cheap win.

## Locking Protocol (what the audit prints)

1. **Object test**: street signs (unbolt-able), scaffolding, chain-link, trees = NO; ground-anchored rack, bike hoop, fence post capped = YES.
2. **Sheldon method**: U-lock around rear wheel + seat tube inside the rear triangle — wheel+frame secured with a small lock. Fill the shackle space (leave no room for a jack).
3. Quick releases: replace skewers with locking ones or take the seat/light with you.
4. Lock high (off the ground = no bottle-jack leverage), keyway facing down.
5. Never lock overnight outside in risk 4–5 — no lock survives a night grinder attack.

## Stolen-Bike 72-Hour Playbook (summary)

- **Hour 0–1**: file the police report (a case number unlocks everything else: insurance, registry flag, marketplace takedowns). Flag stolen on BikeIndex + Project 529 + national registry if applicable.
- **Hour 1–24**: create saved searches on Facebook Marketplace, Craigslist, OfferUp/eBay with the model name + city + 40 km radius. Stolen bikes surface locally within 48 h. Set alerts for "bike" + your frame size as well (thieves strip details).
- **Day 1–3**: print QR flyers for bike shops, pawn shops, co-ops (they all check serials); post in local cycling Facebook/Reddit/WhatsApp groups with the registry link — these communities recover more bikes than police do.
- **Recovery sting**: never meet alone; agree on inspecting "your" bike by serial under a pretext (buying), bring the police case number and one friend; if serial matches, call the non-emergency line instead of confronting.
- **Insurance**: homeowners/renters covers bikes often with a sublimit (~$500–1500) — file within the policy window; check if the policy needs the police report within 24–72 h.

## Common Pitfalls

1. **Cable lock as the only lock.** Every cable falls to 24" bolt croppers in seconds. Cables are wheel-accessories, never primary.
2. **Serial number unknown until after the theft.** It's stamped on the frame (bottom bracket shell mostly — per-brand locations in the script); the police report needs it and marketplace takedowns require it.
3. **Locking the top tube to a sign post.** Lift the bike over the post — gone. Object test first, always.
4. **Photos of the drive side only.** Registry photos: both sides, drivetrain close-up, serial close-up, distinctive scratches, components (wheelset, saddle) — these identify stripped frames.
5. **Meeting a "seller" who has your bike.** Confrontations go badly; use the serial + police case number + non-emergency line, or bring a uniformed officer to the meeting (many departments do this gladly).

## Verification Checklist

- [ ] Audit verdict names the weakest link (lock, wheel, or object) — not just a grade
- [ ] Registry JSON has: serial, 6+ photos checklist, distinct marks, purchase proof
- [ ] Serial location guidance matches the bike's brand
- [ ] Stolen playbook step 1 = police report with case number before anything else
- [ ] Insurance sublimit and claim deadline checked against the policy

## Example Session

```
$ python3 scripts/bikeshield.py audit --bike-value 1400 --area-risk 4 \
    --locks "kryptonite evolution u-lock; cable"

LOCK AUDIT — bike $1400, area risk 4/5
══════════════════════════════════════
[1] kryptonite evolution u-lock → Gold (≈ART 4)
    Resists croppers/leverage; falls to a cordless grinder in 1–2 min.
    OK for daytime commuter parking; NOT for overnight in risk 4.
[2] cable → NOT A LOCK (opportunistic-tug class only)
    24" bolt croppers cut it in seconds — demote to wheel duty.

VERDICT: PARTIAL — frame protected by day logic only.
WEAKEST LINK: front wheel (quick-release) + overnight exposure.
FIX:  • Add locking skewers or a secondary Gold mini-U for the front wheel.
      • Lock budget check: $140–210 recommended — currently ~$80 → underinvested.
      • Overnight rule: bike goes inside; no lock survives a night grinder run.
```
