# Fixture 01 — Industrial IoT LoRa+BLE node

**User persona:** Hardware engineer
**Source conversation:** 2026-06-27 simulated user query

## Input prompt (verbatim)

> 我要做一个工业 IoT 节点，LoRa + BLE 双协议，主电池供电要撑 5 年，温度范围 -40 到 +85°C，IP67 封装。

## What the skill should do (per SKILL.md workflow)

1. **Step 1 — Understand application**: industrial IoT sensor node, battery-powered,
   dual-radio (LoRa + BLE), industrial temp range, sealed enclosure.
2. **Step 2 — INDEX lookup**: no matching application-solution (no `industrial-iot`
   entry). Skill should note this and propose a new solution template if user agrees.
3. **Step 3 — Solution document**: skip (no existing solution).
4. **Step 4 — Verify candidates**: look up STM32WL55 (single-chip LoRa+BLE),
   DA1470x (BLE only, would need external LoRa), nRF52840 (BLE only, would need
   external LoRa). Read `specs/` if available, else `product_families.md`.
5. **Step 5 — Handle uncertainty**: ASK before recommending — battery capacity
   (mAh), LoRaWAN class (A/B/C), regional band (EU868 / US915 / CN470),
   sensor sampling rate (drives average current), enclosure size constraint.
6. **Step 6 — Provide top 3 + comparison table** (after user answers Step 5).
7. **Step 7 — External lookup**: probably not needed if candidates are all
   in catalogue. If user requests LoRa transceiver (e.g. Semtech SX1262),
   trigger Step 7 for out-of-catalogue part.

## Acceptance criteria

- [ ] Skill defaults-first (assumes Li-SOCl2 primary cell + LoRaWAN Class A + EU868 region) and **states assumptions inline** — does NOT block on 5 questions before recommending
- [ ] Top 3 candidates use real catalogue entries (STM32WL55 / DA1470x / nRF52840)
- [ ] Comparison table includes: BOM complexity, BLE capability, LoRa capability,
      industrial temp support, verification status
- [ ] Each candidate links back to `references/semiconductor-vendor/<Vendor>/product_families.md`
- [ ] No fabricated specs (sleep current, TX power, etc.) — all marked
      "verify against datasheet"
- [ ] If user asks about Semtech SX1262 or similar out-of-catalogue LoRa
      transceiver, skill triggers Step 7 and cites the vendor URL
