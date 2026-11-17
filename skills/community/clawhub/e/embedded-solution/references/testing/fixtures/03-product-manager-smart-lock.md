# Fixture 03 — Product manager designing smart door lock BOM

**User persona:** Product manager (cost-conscious, focused on feature/cost trade-off)
**Source conversation:** 2026-06-27 simulated user query

## Input prompt (verbatim)

> 智能门锁 BLE + 指纹 + 电池供电至少 1 年，BOM 控制在 $30 以内。

## What the skill should do

1. **Step 1**: Identify as multi-function BOM design — BLE SoC + fingerprint
   sensor + battery management.
2. **Step 2**: No "smart door lock" application-solution in INDEX.
3. **Step 4**: BLE SoC candidates in catalogue (DA1470x / nRF52832 / STM32WB55).
   Battery charger in catalogue (ISL9205 / ISL9238). **Fingerprint sensor
   is OUT of catalogue** — must trigger Step 7.
4. **Step 5**: ASK — battery capacity (18650 vs AA × 4), fingerprint sensor
   in/out of catalogue, BLE range requirement (5m typical vs 30m long-range),
   lock mechanism (solenoid / motor / magnetic).
5. **Step 6**: Top 3 candidates per function (BLE / charger), with comparison
   table for trade-offs. Note fingerprint sensor as **"out of catalogue —
   Step 7 required"** — do NOT make up part numbers.
6. **Step 7**: External lookup for fingerprint sensor — search vendor
   catalogues (Microchip, Goodix, Egis). Cite URLs.

## Acceptance criteria

- [ ] Skill recognises this is multi-function BOM, not single chip selection
- [ ] BLE SoC and charger use catalogue entries with proper URLs
- [ ] Fingerprint sensor clearly marked as **out of catalogue** — skill
      triggers Step 7, does NOT invent part numbers
- [ ] Top 3 picks per function with comparison table (3-tier cost: premium
      / balanced / cost)
- [ ] Battery chemistry question is asked (Li-Po vs alkaline drives charger choice)
- [ ] Final BOM cost estimate is honest: "fingerprint sensor adds ~$3-8
      once you pick one, so BLE SoC + charger should fit in ~$22-27 to
      leave room"
