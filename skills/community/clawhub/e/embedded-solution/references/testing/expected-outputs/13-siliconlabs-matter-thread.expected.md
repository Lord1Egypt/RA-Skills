# Expected output skeleton — Fixture 13

## This fixture tests Silicon Labs catalogue + Matter Thread selection

If `references/semiconductor-vendor/SiliconLabs/product_families.md` or
`specs/SiliconLabs/EFR32MG24.yaml` / `STM32WBA.yaml` / `EFR32MG21.yaml` (all maintainer's private spec databases, not shipped in public release)
(maintainer's private spec databases, not shipped in public release) placeholders are missing, this fixture fails.

## Required structural elements

### 1. Defaults-first

- [ ] Skill states assumptions inline (indoor consumer, battery-powered, Matter 1.3 compliant)
- [ ] Skill does NOT ask 5 questions before recommending
- [ ] User's "Thread + BLE" requirement is honoured — no WiFi-only candidates

### 2. Top 3 Matter Thread candidates

| Slot | Chip | Architecture | Thread | BLE | Differentiator |
|------|------|--------------|--------|-----|----------------|
| A | **EFR32MG24** | Cortex-M33 + M0+ | ✅ 1.3 | ✅ 5.3 | AI/ML MVP |
| B | **STM32WBA** | Cortex-M33 + M0+ | ✅ | ✅ 5.3 | SESIP Level 3 secure element |
| C | **EFR32MG21** | Cortex-M33 + M0+ | ✅ | ✅ | cost-down, no MVP |

### 3. Recommendation shape

- [ ] **EFR32MG24** for AI/ML edge inference + newest Series 2
- [ ] **STM32WBA** for SESIP certification
- [ ] **EFR32MG21** for cost-down without MVP

### 4. Per-tier citation

- [ ] Tier 2: `references/semiconductor-vendor/SiliconLabs/product_families.md#efr32mg24`
- [ ] Tier 2: `references/semiconductor-vendor/ST/product_families.md#stm32wba`
- [ ] Tier 1: `specs/SiliconLabs/EFR32MG24.yaml` (maintainer's private spec database, not shipped in public release)
- [ ] Tier 1: `specs/ST/STM32WBA.yaml` (maintainer's private spec database, not shipped in public release)
- [ ] Tier 3: alcom.be mirror for Silicon Labs (Cloudflare-gated)

### 5. Flash size discipline

- [ ] Flash size NOT fabricated (placeholder YAML marks `unverified: [all]`)
- [ ] "verify against datasheet" explicit for flash size
- [ ] If user's "enough flash for OTA" constraint can't be met → mark as not verified

## Acceptance criteria

- [ ] All 3 candidates support Thread + BLE
- [ ] AI/ML MVP mentioned
- [ ] SESIP mentioned
- [ ] No fabricated flash size
- [ ] alcom.be mirror mentioned
- [ ] Tier 1 + Tier 2 citations present
- [ ] Defaults stated inline

## Anti-patterns to fail

- ❌ Recommending split nRF52840 + nRF7002
- ❌ Recommending ESP32-C6 (WiFi+Thread — user wanted Thread-only Matter)
- ❌ Fabricating flash size
- ❌ Missing EFR32MG24 → EFR32MG21 differentiation
- ❌ Forgetting alcom.be mirror
- ❌ "All three are equivalent"
