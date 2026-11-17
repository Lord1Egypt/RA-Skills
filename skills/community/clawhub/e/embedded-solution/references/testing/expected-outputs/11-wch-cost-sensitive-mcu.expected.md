# Expected output skeleton — Fixture 11

## This fixture tests WCH catalogue entry

If `references/semiconductor-vendor/WCH/product_families.md` is missing or
`specs/WCH/CH32V103R8T6.yaml` (maintainer's private spec database, not shipped in public release) placeholder is missing, this fixture fails.

## Required structural elements

### 1. Defaults-first

- [ ] Skill states assumptions inline (USB CDC device class, indoor consumer, <$1 BOM target)
- [ ] Skill does NOT ask 5 questions before recommending
- [ ] User's "domestic suppliers" preference is honoured — no overseas chips recommended

### 2. Top 3 WCH candidates

| Slot | Chip | Architecture | USB | Use case |
|------|------|--------------|-----|----------|
| A | **CH32V103R8T6** | RISC-V (QingKe V2) | built-in | real MCU + USB, future-proof |
| B | **CH32F103C8T6** | ARM Cortex-M3 | built-in | STM32F103 firmware portability |
| C | **CH340N** | dedicated USB-serial IC | built-in | dumb bridge, no MCU logic |

### 3. Recommendation shape

- [ ] **CH32V103R8T6** as primary pick (RISC-V + flexibility)
- [ ] **CH32F103C8T6** as ARM-compatibility alternative
- [ ] **CH340N** as dedicated-IC alternative (lowest cost)
- [ ] All three serve different use cases — skill must explain when to pick each

### 4. Tier 3 mirror emphasis

- [ ] **LCSC** mentioned prominently (WCH parts are stocked there)
- [ ] Mouser / Digi-Key also mentioned as fallback

### 5. Per-tier citation

- [ ] Tier 2: `references/semiconductor-vendor/WCH/product_families.md#ch32v103r8t6`
- [ ] Tier 1: `specs/WCH/CH32V103R8T6.yaml` (maintainer's private spec database, not shipped in public release) — placeholder
- [ ] Tier 3: LCSC search URL provided

### 6. Cross-reference to second-source

- [ ] Mention **GD32VF103** (GigaDevice RISC-V MCU) as second-source alternative

## Acceptance criteria

- [ ] All 3 candidates are WCH (no STM32 / NXP / etc.)
- [ ] Comparison distinguishes RISC-V / ARM / dedicated IC
- [ ] Cost framing given as tier (low / lowest)
- [ ] LCSC mentioned
- [ ] Tier 1 + Tier 2 citations present
- [ ] Defaults stated inline

## Anti-patterns to fail

- ❌ Recommending STM32F103 (overseas, ignores domestic preference)
- ❌ Single recommendation (violates Top 3 default)
- ❌ Missing CH340N option
- ❌ Fabricating clock / RAM / flash numbers
- ❌ Forgetting LCSC as Tier 3 mirror
- ❌ Saying "all three are equivalent"
