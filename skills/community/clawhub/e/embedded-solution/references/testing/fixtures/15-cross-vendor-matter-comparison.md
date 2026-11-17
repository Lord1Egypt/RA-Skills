# Fixture 15 — Cross-vendor Matter Thread comparison (uses all 3 vendors)

**User persona:** Smart home architect evaluating Matter Thread ecosystem across vendors
**Source conversation:** 2026-06-27 (added after catalogue coverage reaches 11 vendors)

## Input prompt (verbatim)

> "I'm designing a Matter over Thread border router for a smart home gateway. Compare what ST, Nordic, and Silicon Labs each offer."

## What the skill should do

1. **Trigger check** — chip selection for Matter BR = triggers.
2. **Step 1 — Understand application**:
   - Matter Border Router (gateway), not End Device
   - Needs: Thread + WiFi + BLE (gateway connects Thread devices to WiFi home network)
   - Production-scale design (not hobby)
3. **Step 4 — Run Search Priority**:
   - Tier 2 + Tier 1 for each vendor:
     - ST: STM32WBA (Thread + BLE single chip, no WiFi) → need WiFi companion
     - Nordic: nRF52840 + nRF7002 (split architecture, Thread + BLE + WiFi)
     - Silicon Labs: EFR32MG24 (Thread + BLE single chip, no WiFi) → need WiFi companion
   - Tier 3: fetch vendor product pages (Tier 3 mirror list per region)
4. **Step 5 — defaults-first**:
   - Default: indoor consumer, 1k-10k production, mainstream overseas (user didn't specify domestic)
   - "Matter border router" is a specific role — skill should distinguish from End Device
5. **Step 6 — Cross-vendor comparison**:
   - For each vendor, show: (a) Thread support, (b) BLE support, (c) WiFi capability (built-in or companion), (d) single-chip vs split, (e) ecosystem maturity
   - Top 3 picks should be 1 per vendor OR cross-vendor ranking depending on use case

## Expected behaviour (defaults-first)

Skill produces a comparison where each vendor is fairly represented. The "right" answer is genuinely vendor-dependent:
- **Silicon Labs EFR32MG24 + external WiFi** if Thread + BLE single-chip is the priority
- **Nordic nRF52840 + nRF7002** if ecosystem maturity + Nordic SDK matters
- **ST STM32WBA + external WiFi** if Matter certification via SESIP is required

### Example acceptable response structure

> ## Matter border router — vendor comparison (ST / Nordic / Silicon Labs)
>
> *[Assumed: indoor consumer gateway, 1k-10k production, mainstream overseas (you didn't say domestic). Tell me if you need domestic or automotive.]*
>
> ### Architecture options
>
> | Vendor | Thread+BLE SoC | WiFi strategy | Single-chip Thread+BLE? | Ecosystem |
> |--------|----------------|---------------|------------------------|-----------|
> | ST | **STM32WBA** | external companion | ✅ (no WiFi integrated) | STM32Cube ecosystem, mature |
> | Nordic | **nRF52840** | nRF7002 companion | ❌ split (Thread+BLE + WiFi separate) | nRF Connect SDK, very mature |
> | Silicon Labs | **EFR32MG24** | external companion | ✅ (no WiFi integrated) | Simplicity Studio, GSDK |
>
> ### When to pick each
>
> **Silicon Labs EFR32MG24** — best if you want Thread+BLE in one chip and don't need a tight Nordic-ecosystem lock-in.
>
> **Nordic nRF52840 + nRF7002** — best if your team already uses Nordic SDK / nRF Connect; split adds BOM complexity but ecosystem is the strongest.
>
> **ST STM32WBA** — best if you need Matter SESIP Level 3 secure element certification (ST is the only one with built-in SE).

## Acceptance criteria

- [ ] All 3 vendors fairly represented (not biased toward any one)
- [ ] Each vendor's SoC cited with `product_families.md#<chip>` anchor
- [ ] Matter Border Router distinguished from End Device
- [ ] Single-chip vs split distinction made explicit
- [ ] WiFi strategy (built-in vs companion) noted for each
- [ ] Tier 3 mirror list: ST Mouser mirror, Nordic alldatasheet, Silicon Labs alcom mirror
- [ ] No fabricated spec numbers (placeholder YAMLs mark `unverified: [all]`)
- [ ] Defaults stated inline

## Anti-patterns to fail

- ❌ Picking only one vendor (violates the user's "compare" request)
- ❌ Adding ESP32-C6 to the comparison (WiFi+Thread but **not** a MBR — needs Matter Border Router profile)
- ❌ Recommending nRF52840 alone (no WiFi — would not satisfy user's "WiFi" implicit need)
- ❌ Missing the single-chip vs split distinction (architectural trade-off)
- ❌ Fabricating WiFi chip model numbers
- ❌ Missing Tier 3 mirror differentiation (different vendor = different mirror)

## How this fixture tests the catalogue

This fixture tests **3 vendors simultaneously** — ensures the catalogue is
internally consistent and the skill can compare across vendors fairly. If any
of ST / Nordic / Silicon Labs is missing, this fixture breaks.
