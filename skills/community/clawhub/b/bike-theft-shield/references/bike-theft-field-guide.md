# Bike Theft: Hardening, Registry, Recovery — Field Guide

Reference for `scripts/bikeshield.py`. Sources: Sold Secure and ART rating
criteria, published theft surveys (registration vs recovery rates), police
guidance on stolen property reports, and marketplace-resale patterns.

## 1. Where serial numbers hide (by brand class)

| Brand family | Typical serial location |
|---|---|
| Most generic / older steel | Bottom bracket shell (underside, flip the bike) |
| Trek | Bottom of the bottom bracket shell, starts "WTU" |
| Specialized | Front of seat tube or dropout, often "WSBC/ABCDE" |
| Giant | Under the bottom bracket or seat tube |
| Cannondale | Left dropout or BB, "GM" prefix |
| Santa Cruz / carbon frames | Under the BB shell or rear dropout |
| Brompton | On the frame plate + BB |
| E-bikes (Bosch etc.) | Motor housing + frame; record BOTH |

Also record: motor/frame numbers for e-bikes, fork steerer stamps on some
suspension forks, and wheel hub serials for expensive wheelsets.

## 2. Lock standards, honestly

- **Sold Secure (UK)**: Bronze < Silver < Gold < Diamond. Diamond ≈ resists a
  cordless angle grinder for ~1 minute (published test standard since 2021).
- **ART (NL)**: 1–4+ stars; ≥4 needed for some city insurance programs.
- Practical truth: **no portable lock defeats two grinders**. The game is
  (a) making your bike slower to steal than the one next to it, (b) time-of-day
  discipline, (c) recoverability (registry + serial + photos).

### Lock-type physics
- 13–16 mm hardened steel shackle: defeats hand croppers; grinder takes 40–90 s.
- 12+ mm chain: same class, heavier, flexible for awkward objects.
- Folding locks: mid cut-resistance, weak at the rivets vs grinders.
- Cable of ANY thickness: croppers food. Never primary above risk 1.

## 3. Area risk scoring (the script's 1–5 scale)

5 = NYC/SF/Chicago/London/Paris cores, any university district with theft
news; 4 = dense city, transit-hub parking; 3 = inner suburb, campus daytime;
2 = residential street, garage-adjacent; 1 = rural, in-sight-only stops.
When torn between two scores, take the higher one — locks are cheaper than
deductibles.

## 4. Registration map

- **BikeIndex.org** — free, global, widely checked by shops and police.
- **Project 529** — app with photo + bike "shields"; strong in US/Canada.
- **National cycle databases**: UK (BikeRegister), NL (art-marked frames),
  Germany (Code 247 etching).
- Local: university campus police registries.
- Home registry file (this script): JSON you control, survives app shutdowns —
  include purchase receipt scan path + insurance policy line.

## 5. Insurance reality

- Homeowners/renters: bikes usually covered off-premises at a sublimit
  ($500–1500 typical); scheduled personal property endorsement ("rider") for
  expensive bikes (~1–2% of value/yr, no deductible sometimes).
- Standalone bike insurance (velosurance-style): theft + crash + liability.
- Claim needs: police report number, photos, proof of ownership, sometimes
  proof the lock was rated (keep the lock receipt/box photo!).
- E-bikes: many policies treat >750 W or throttle bikes differently — check.

## 6. Marketplace sting search setup

Saved searches to create the hour the bike is stolen:
- `<model> bike` within 40 km, sorted by newest.
- `<brand> <size>` (thieves list wrong model, right frame).
- `bike <color>` in bike-parts categories (stripping sign).
- Alert on your wheelset/saddle/groupset part numbers (stripped parts have
  less listing variety than frames).
- Check pawn shops and cash-converters in person with a flyer + serial.

## 7. Recovery meeting safety

- Never say "stolen" in the first message — arrange to "inspect and buy".
- Meet in a public place, bring one friend, have the police case number open.
- Match the serial BEFORE any money talk; photograph it.
- If confirmed: call the non-emergency line and wait; do not grab-and-run
  (you can be charged, and sellers of stolen bikes aren't always calm).
