# Expected output skeleton — Fixture 10

## This fixture tests catalogue expansion regression

If `specs/Espressif/ESP32-C6.yaml` (maintainer's private spec database, not shipped in public release) is missing from the catalogue, this fixture
becomes impossible to pass — the skill can't cite Tier 1 data for the primary
recommendation.

## Required structural elements

### 1. Defaults-first behaviour

- [ ] Skill states assumptions inline (indoor consumer, 1k-10k volume, cost-sensitive)
- [ ] Skill does NOT ask 5 questions before recommending
- [ ] Skill may flag production volume as a confirm-once gate if cost/quality tradeoff matters

### 2. Top 3 comparison table

| Slot | Chip | Single chip? | WiFi | BLE | Thread | Citation |
|------|------|--------------|------|-----|--------|----------|
| A | **ESP32-C6** | ✅ | ✅ WiFi 6 | ✅ BLE 5.3 | ✅ Thread 1.3 | Espressif product_families.md#esp32-c6 + specs/Espressif/ESP32-C6.yaml (maintainer-only, not shipped in public release) |
| B | **STM32WBA** | ✅ (no WiFi) | ❌ | ✅ BLE 5.3 | ✅ 802.15.4 | ST product_families.md#stm32wba + specs/ST/STM32WBA.yaml (maintainer-only) |
| C | **nRF52840 + nRF7002** | ❌ split | ✅ via nRF7002 | ✅ | ✅ via nRF7002 | Nordic product_families.md#nrf52840 + product_families.md#nrf7002 |

### 3. Recommendation shape

- [ ] **ESP32-C6** is the clear primary pick — user said "single chip" and it is the only one with all 3 protocols single-chip
- [ ] STM32WBA noted honestly (no WiFi — only useful if user drops WiFi requirement)
- [ ] nRF52840 + nRF7002 noted as split alternative (more flexible but more complex)

### 4. Per-tier citation

- [ ] ESP32-C6 spec fields cite Tier 1 (YAML placeholder) explicitly
- [ ] STM32WBA spec fields cite Tier 1 (YAML placeholder) explicitly
- [ ] nRF52840 / nRF7002 spec fields cite Tier 2 (product_families.md) + Tier 3 if fetched
- [ ] No fabricated spec numbers (YAMLs are placeholder; spec values must be "not verified" or actual fetched)

### 5. Trade-off explanation

- [ ] ESP32-C6: best single-chip fit
- [ ] STM32WBA: only if you can drop WiFi
- [ ] nRF52840 + nRF7002: more flexible but more complex BOM

## Acceptance criteria

- [ ] ESP32-C6 is primary pick
- [ ] All 3 candidates have WiFi / BLE / Thread columns filled honestly
- [ ] STM32WBA row explicitly marks WiFi as ❌
- [ ] No fabricated ESP32-C6 specs (placeholder YAML marks `unverified: [all]`)
- [ ] Defaults stated inline
- [ ] Tier 1 + Tier 2 citations present

## Anti-patterns to fail

- ❌ Recommending nRF52840+nRF7002 over ESP32-C6 (split doesn't match user's "single chip" requirement)
- ❌ Saying "all three are equivalent"
- ❌ Missing the WiFi column for STM32WBA
- ❌ Fabricating ESP32-C6 spec values from memory
- ❌ Recommending original ESP32 (no WiFi 6, no Thread 1.3)
- ❌ Long lecture on Matter protocol stack when user wants a chip pick
