# Fixture 10 — ESP32-C6 single-chip Matter (uses new catalogue entry)

**User persona:** Smart home product designer evaluating single-chip Matter options
**Source conversation:** 2026-06-27 (added after ESP32-C6 + STM32WBA + nRF7002 added to catalogue)

## Input prompt (verbatim)

> "I want to make a Matter light bulb. It needs WiFi, BLE for commissioning, and Thread as fallback. Which single-chip SoC should I use?"

## What the skill should do

1. **Trigger check** — embedded system design, chip selection, BOM = triggers.
2. **Step 1** — application: Matter device (light bulb); constraints: WiFi + BLE + Thread; user wants **single chip** (explicit).
3. **Step 4 — Run Search Priority**:
   - Tier 1: read `specs/Espressif/ESP32-C6.yaml` (maintainer's private spec database, newly added 2026-06-27; placeholder, not shipped in public release) for verified fields
   - Tier 2: read `references/semiconductor-vendor/Espressif/product_families.md#esp32-c6` for vendor URL + lifecycle status
   - Tier 3: fetch Espressif product page if needed for current specs
4. **Step 5 — defaults-first**:
   - Default: indoor consumer (0-40°C), 1k-10k production volume, cost-sensitive but Matter compliance matters
   - One medium-cost flag: production volume affects whether single-chip or split makes sense
5. **Step 6 — Top 3**:
   - Slot A: **ESP32-C6** (Espressif) — RISC-V + WiFi 6 + BLE 5 + Thread 1.3 single chip ⭐
   - Slot B: **STM32WBA** (ST) — BLE 5.3 + 802.15.4 single chip with secure element (no WiFi — needs companion or Thread-only)
   - Slot C: **nRF52840 + nRF7002** (Nordic split) — 2-chip solution, more flexibility but more complex
6. **Skill should call out**:
   - ESP32-C6 is the obvious single-chip answer
   - STM32WBA lacks WiFi → would need Thread-only commissioning or external WiFi
   - nRF7002 split is the "more flexible" alternative

## Expected behaviour (defaults-first)

Skill produces a Top 3 + comparison table where:
- ESP32-C6 is clearly the recommended pick (it fits the user's "single chip" requirement perfectly)
- Comparison table has verified spec values for ESP32-C6 (per the new YAML placeholder)
- Honest about STM32WBA missing WiFi
- nRF52840+nRF7002 noted as the 2-chip alternative

### Example acceptable response structure

> ## Top 3 — Matter light bulb (single-chip WiFi+BLE+Thread)
>
> *[Assumed: indoor consumer, 1k-10k volume, cost-sensitive. Tell me if outdoor or automotive.]*
>
> ### Comparison
>
> | Slot | Chip | Architecture | WiFi | BLE | Thread | Single chip? |
> |------|------|--------------|------|-----|--------|--------------|
> | A | **ESP32-C6** | RISC-V | ✅ WiFi 6 | ✅ BLE 5.3 | ✅ Thread 1.3 | ✅ |
> | B | **STM32WBA** | Cortex-M33 + M0+ | ❌ | ✅ BLE 5.3 | ✅ 802.15.4 | ✅ (no WiFi) |
> | C | **nRF52840 + nRF7002** | Cortex-M4 + WiFi companion | ✅ via companion | ✅ | ✅ via companion | ❌ split |
>
> ### Recommendation
>
> **ESP32-C6** — single-chip solution that matches your exact requirement (WiFi + BLE + Thread in one SoC).
>
> **STM32WBA** — only if you don't need WiFi (Thread + BLE commissioning via Thread Border Router). Adds a separate WiFi chip if needed.
>
> **nRF52840 + nRF7002** — if you want to split concerns (BLE/Thread on nRF52840, WiFi on nRF7002). More flexible but more complex.

## Acceptance criteria

- [ ] Skill recommends **ESP32-C6** as the primary pick (single chip matches user requirement)
- [ ] Comparison table has 3 candidates
- [ ] ESP32-C6 row has **WiFi 6 + BLE 5.3 + Thread 1.3** marked (new catalogue data)
- [ ] STM32WBA row notes **no WiFi** honestly (not "full Matter" — would need companion)
- [ ] nRF52840+nRF7002 noted as split (2-chip) alternative
- [ ] Citation to `references/semiconductor-vendor/Espressif/product_families.md#esp32-c6` present
- [ ] Citation to `specs/Espressif/ESP32-C6.yaml` present (Tier 1 placeholder; maintainer's private spec database, not shipped in public release)
- [ ] Defaults stated inline (indoor consumer, 1k-10k volume)
- [ ] No fabricated spec numbers (per Tier 1 placeholder YAML)

## Anti-patterns to fail

- ❌ Recommending nRF52840+nRF7002 over ESP32-C6 (nRF is split, doesn't fit user's "single chip")
- ❌ Saying "all three are equivalent" when ESP32-C6 is clearly the best fit
- ❌ Missing the WiFi column for STM32WBA (must be explicit: STM32WBA has no WiFi)
- ❌ Fabricating ESP32-C6 specs from memory (use Tier 1 placeholder YAML or "not verified")
- ❌ Recommending the original ESP32 (no WiFi 6, no Thread 1.3)
- ❌ Long lecture on Matter architecture when user wants a chip pick

## How this fixture tests the catalogue

This fixture **only passes if ESP32-C6 is in the catalogue** — it's a regression test for the 2026-06-27 catalog expansion (commit `6a0ec69`). If the catalogue regression breaks, this fixture breaks too.
