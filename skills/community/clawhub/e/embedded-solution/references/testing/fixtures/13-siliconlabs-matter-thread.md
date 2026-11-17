# Fixture 13 — Silicon Labs Matter over Thread (catalogue regression)

**User persona:** Smart home engineer evaluating Matter Thread solutions
**Source conversation:** 2026-06-27 (added after EFR32MG24 added to catalogue)

## Input prompt (verbatim)

> "I need a Thread + BLE SoC for a Matter light switch. It must support Matter 1.3 and have enough flash for OTA updates."

## What the skill should do

1. **Trigger check** — embedded design, Matter SoC selection = triggers.
2. **Step 4 — Search Priority**:
   - Tier 2: read `references/semiconductor-vendor/SiliconLabs/product_families.md` for EFR32MG24 entry
   - Tier 2: read `specs/SiliconLabs/EFR32MG24.yaml` (placeholder, if installed)
   - Tier 3: fetch Silicon Labs product page (Cloudflare-gated — use alcom.be mirror)
3. **Step 5 — defaults-first**:
   - Default: indoor consumer (0-40°C), Matter 1.3 compliant, Thread + BLE for commissioning
   - "Light switch" implies battery-powered + low standby current
   - "Enough flash for OTA" — Tier 3 verify flash size from datasheet
4. **Step 6 — Top 3**:
   - Slot A: **EFR32MG24** (Silicon Labs) — Cortex-M33 + M0+ + Thread 1.3 + BLE 5.3 + AI/ML MVP ⭐
   - Slot B: **STM32WBA** (ST) — Cortex-M33 + M0+ + Thread + BLE + SESIP secure element (no WiFi)
   - Slot C: **EFR32MG21** (Silicon Labs) — older Series 2, lower cost, no AI/ML MVP
5. **Skill should call out**:
   - EFR32MG24 has the AI/ML MVP (Matrix Vector Processor) for on-device ML
   - STM32WBA has the integrated secure element (SESIP Level 3)
   - EFR32MG21 is the cost-down alternative for designs that don't need MVP

## Expected behaviour (defaults-first)

Skill produces a Top 3 + comparison table where:
- All 3 candidates support Thread 1.3 + BLE (the user's requirement)
- Flash size is mentioned as a key differentiator (verify in datasheet, not fabricated)
- AI/ML MVP mentioned as EFR32MG24 differentiator
- SESIP mentioned as STM32WBA differentiator

### Example acceptable response structure

> ## Top 3 — Matter light switch (Thread + BLE, OTA-capable)
>
> *[Assumed: indoor consumer, battery-powered (battery life unknown — tell me), 1k-10k volume. Tell me if outdoor or mains-powered.]*
>
> ### Comparison
>
> | Slot | Chip | Architecture | Thread | BLE | Flash (verify) | Differentiator |
> |------|------|--------------|--------|-----|----------------|----------------|
> | A | **EFR32MG24** | Cortex-M33 + M0+ | ✅ 1.3 | ✅ 5.3 | verify datasheet | AI/ML MVP, Thread 1.3 |
> | B | **STM32WBA** | Cortex-M33 + M0+ | ✅ | ✅ 5.3 | verify datasheet | SESIP Level 3 secure element |
> | C | **EFR32MG21** | Cortex-M33 + M0+ | ✅ | ✅ | verify datasheet | cost-down, no MVP |
>
> ### Recommendation
>
> **EFR32MG24** if you need AI/ML edge inference or want the newest Silicon Labs Series 2.
>
> **STM32WBA** if you need certified secure element for Matter compliance.
>
> **EFR32MG21** if MVP is not needed and you want to minimise cost.

## Acceptance criteria

- [ ] All 3 candidates support Thread + BLE (Matter requirement)
- [ ] EFR32MG24, STM32WBA, EFR32MG21 all in catalogue (regression test for catalogue expansion)
- [ ] Flash size NOT fabricated (placeholder YAML marks `unverified: [all]`)
- [ ] AI/ML MVP mentioned as EFR32MG24 differentiator
- [ ] SESIP mentioned as STM32WBA differentiator
- [ ] Citation to `references/semiconductor-vendor/SiliconLabs/product_families.md#efr32mg24` present
- [ ] Tier 3 mirror: **alcom.be** mentioned (Silicon Labs Cloudflare-gated)
- [ ] Defaults stated inline
- [ ] No fabricated spec numbers

## Anti-patterns to fail

- ❌ Recommending nRF52840 + nRF7002 (split, not single-chip SoC)
- ❌ Recommending ESP32-C6 (has WiFi 6 but the user asked for Thread-only Matter, not WiFi+Thread)
- ❌ Fabricating flash size (e.g., "1.5 MB flash" without "verify against datasheet")
- ❌ Missing the EFR32MG24 → EFR32MG21 differentiation (same vendor, different cost tier)
- ❌ Forgetting alcom.be mirror (Silicon Labs Cloudflare-gated)
- ❌ Saying "all three are equivalent"

## How this fixture tests the catalogue

This fixture **only passes if EFR32MG24 / STM32WBA / EFR32MG21 are all in the catalogue** — regression test for the 2026-06-27 catalog expansion (commit `6a0ec69`). Tests that the skill can compare multiple Thread+BLE SoCs and explain Matter compliance trade-offs.
