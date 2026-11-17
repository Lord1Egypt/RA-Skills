# Expected output skeleton — Fixture 14

## This fixture tests STM32WBA catalogue + migration scenario

If `references/semiconductor-vendor/ST/product_families.md` or
`specs/ST/STM32WBA.yaml` (maintainer's private spec database, not shipped in public release) placeholder is missing, this fixture fails.
Also tests that the skill recognises **migration** as a different scenario
from greenfield design.

## Required structural elements

### 1. Recognition of migration scenario

- [ ] Skill recognises this is a **migration** question, not greenfield
- [ ] Skill notes that STM32WB55 is **still active** (migration is optional)
- [ ] Skill does NOT force migration

### 2. Top 3 migration candidates

| Slot | Chip | Migration effort | Secure element | Why |
|------|------|-------------------|----------------|-----|
| A | **STM32WBA** | Low (same ST family) | ✅ SESIP Level 3 | Direct successor, user asked for SESIP |
| B | **STM32WB55** | None (keep current) | ❌ external | Still active, no need to migrate |
| C | **EFR32MG24** | High (different vendor) | (verify) | Cross-vendor alternative |

### 3. Recommendation shape

- [ ] **STM32WBA** as primary (matches user's "newer chip with built-in secure element" ask)
- [ ] **STM32WB55** as "still good" option (migration optional)
- [ ] **EFR32MG24** as cross-vendor alternative with explicit high migration cost

### 4. Per-tier citation

- [ ] Tier 2: `references/semiconductor-vendor/ST/product_families.md#stm32wba`
- [ ] Tier 1: `specs/ST/STM32WBA.yaml` (maintainer's private spec database, not shipped in public release)
- [ ] Tier 3: Mouser mirror for ST (Cloudflare-gated)

### 5. Migration effort assessment

- [ ] STM32WB55 → STM32WBA = "mostly a recompile + driver update" (same ST SDK base)
- [ ] STM32WB55 keep = no migration cost
- [ ] EFR32MG24 = high (different vendor / SDK)

## Acceptance criteria

- [ ] STM32WBA as primary pick
- [ ] STM32WB55 retained as option
- [ ] SESIP Level 3 mentioned
- [ ] Migration effort assessed for each option
- [ ] Mouser mirror mentioned
- [ ] Tier 1 + Tier 2 citations present
- [ ] No fabricated spec numbers

## Anti-patterns to fail

- ❌ Recommending split nRF52840 + nRF7002
- ❌ Forcing migration (STM32WB55 still active — should be option)
- ❌ Missing SESIP mention
- ❌ Fabricating secure-element certification
- ❌ Missing "stay on STM32WB55" option
- ❌ Missing Mouser mirror
- ❌ "All three are equivalent"
