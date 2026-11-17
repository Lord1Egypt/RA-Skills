# Fixture 05 — Startup founder asking pet-tracker minimum BOM cost

**User persona:** Founder (extreme cost focus, business reality check)
**Source conversation:** 2026-06-27 simulated user query

## Input prompt (verbatim)

> 宠物定位器（GPS+BLE），我要把 BOM 成本压到最低，能做到多少？

## What the skill should do

1. **Step 1**: Pet tracker — GPS + BLE, battery powered, cost-optimised.
   Two design tracks: active GPS (real-time) vs passive GPS (on-demand).
2. **Step 2**: No pet-tracker application-solution in INDEX.
3. **Step 4**: BLE SoC candidates in catalogue (nRF52832 / CC2640R2F / DA1470x).
   **GPS module is OUT of catalogue** — must trigger Step 7.
4. **Step 5**: ASK — "active GPS (real-time, more battery) or passive GPS
   (BLE-query-triggered, much cheaper)?" + battery life target.
5. **Step 6**: TWO BOMs side by side (Track 1: active GPS, Track 2: passive GPS).
   For each, top 3 candidate chips per function + comparison table.
6. **Step 7 — External lookup**: GPS modules (Quectel L76K, AT6558R, u-blox)
   are not in catalogue — skill must trigger Step 7 and provide vendor URLs,
   not invented part numbers.

## Acceptance criteria

- [ ] Skill acknowledges the BOM cost question and provides two design tracks
      (active vs passive GPS) with very different cost/battery profiles
- [ ] Top 3 candidates per function (BLE SoC / charger / battery) with
      catalogue entries and verification status
- [ ] GPS module clearly marked as **out of catalogue**, with Step 7 lookup
      for vendor URLs (Quectel, Airoha, u-blox)
- [ ] Total BOM cost estimate given as a RANGE (e.g. "$6-8 passive / $11-15
      active"), not a single number — cost depends on negotiated volume
- [ ] Honest "cost floor reality check" — sub-$5 BOM requires single-chip
      GPS+BLE which is NOT in catalogue; treat as aspirational
- [ ] Does NOT invent part numbers for GPS modules — uses Step 7 + vendor URLs
