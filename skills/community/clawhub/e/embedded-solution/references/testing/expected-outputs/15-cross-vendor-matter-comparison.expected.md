# Expected output skeleton — Fixture 15

## This fixture tests cross-vendor comparison quality

Skill must represent ST / Nordic / Silicon Labs **fairly** — not biased toward
any single vendor, but showing real trade-offs.

## Required structural elements

### 1. Defaults-first

- [ ] Skill states assumptions inline (indoor consumer, 1k-10k production, mainstream overseas)
- [ ] User did not specify "domestic" → skill defaults to mainstream overseas
- [ ] Skill does NOT ask 5 questions before comparing

### 2. Recognition of Matter Border Router

- [ ] Skill distinguishes MBR (gateway, needs Thread + WiFi + BLE) from End Device (Thread + BLE only)
- [ ] User's "border router" wording is honoured — not downgraded to End Device

### 3. Cross-vendor comparison

| Vendor | Thread+BLE SoC | WiFi strategy | Single-chip Thread+BLE? | Ecosystem |
|--------|----------------|---------------|------------------------|-----------|
| ST | **STM32WBA** | external companion | ✅ (no WiFi integrated) | STM32Cube, mature |
| Nordic | **nRF52840** | nRF7002 companion | ❌ split | nRF Connect, very mature |
| Silicon Labs | **EFR32MG24** | external companion | ✅ (no WiFi integrated) | Simplicity Studio, GSDK |

### 4. Per-vendor "when to pick"

- [ ] Silicon Labs EFR32MG24 — Thread+BLE single chip
- [ ] Nordic nRF52840 + nRF7002 — ecosystem maturity (split BOM)
- [ ] ST STM32WBA — SESIP Level 3 secure element certification

### 5. Per-tier citation

- [ ] Tier 2: `references/semiconductor-vendor/ST/product_families.md#stm32wba`
- [ ] Tier 2: `references/semiconductor-vendor/Nordic/product_families.md#nrf52840`
- [ ] Tier 2: `references/semiconductor-vendor/SiliconLabs/product_families.md#efr32mg24`
- [ ] Tier 1: each YAML placeholder mentioned with maintainer context disclaimer
- [ ] Tier 3 mirror per region: Mouser for ST / Alldatasheet for Nordic / Alcom for Silicon Labs

## Acceptance criteria

- [ ] All 3 vendors fairly represented
- [ ] MBR vs End Device distinction
- [ ] Single-chip vs split distinction
- [ ] WiFi strategy noted
- [ ] Tier 3 mirror differentiation
- [ ] No fabricated spec numbers
- [ ] Defaults stated inline

## Anti-patterns to fail

- ❌ Picking only 1 vendor (violates "compare" request)
- ❌ Adding ESP32-C6 (not a Matter BR)
- ❌ Recommending nRF52840 alone (no WiFi)
- ❌ Missing single-chip vs split distinction
- ❌ Missing Tier 3 mirror differentiation
