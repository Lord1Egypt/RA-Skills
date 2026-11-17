# Expected output skeleton — Fixture 12

## This fixture tests Silergy catalogue entry

If `references/semiconductor-vendor/Silergy/product_families.md` is missing or
the SY8120i / SY8089 / SY6280 entries are missing, this fixture fails.

## Required structural elements

### 1. Defaults-first

- [ ] Skill states assumptions inline (indoor consumer, 1k-10k volume, China-domestic)
- [ ] Skill does NOT ask 5 questions before recommending
- [ ] User's "Chinese DCDC" preference honoured — no overseas parts

### 2. Multi-function BOM (NOT single chip)

- [ ] 2 rails: 3.3V (1.5A main) + 1.8V (100mA sensor)
- [ ] 3.3V rail: Top 2 candidates (SY8120i vs SY8089)
- [ ] 1.8V rail: Top 1 candidate (SY6280 LDO)

### 3. 3.3V rail Top 2

| Slot | Chip | Current rating | Headroom | Why | Trade-off |
|------|------|----------------|----------|-----|-----------|
| A | **SY8120i** | 3A | 2x | industry best practice | slightly higher cost |
| B | **SY8089** | 2A | 1.3x | lower cost | tight if load peaks |

### 4. Recommendation shape

- [ ] **SY8120i** as primary pick (2x headroom principle)
- [ ] **SY8089** as cost-optimised alternative (if load is verified ≤1.5A continuous)
- [ ] **SY6280** for 1.8V LDO rail

### 5. Per-tier citation

- [ ] Tier 2: `references/semiconductor-vendor/Silergy/product_families.md` for each
- [ ] Tier 1: `specs/Silergy/SY*.yaml` (maintainer's private spec database, not shipped in public release) — placeholder
- [ ] Tier 3: LCSC + Mouser + Digi-Key URLs

### 6. Cross-reference

- [ ] Note that overseas alternatives exist (TI TPS62xxx, MPS MP2xxx) but not recommended given user's Chinese-DCDC preference

## Acceptance criteria

- [ ] All 3 candidates are Silergy (no overseas)
- [ ] Multi-function BOM (2 rails, not 1)
- [ ] Top 2 for main rail, Top 1 for sensor rail
- [ ] Headroom principle explained
- [ ] Cost framing as tier
- [ ] LCSC mentioned prominently
- [ ] Tier 1 + Tier 2 citations present

## Anti-patterns to fail

- ❌ Recommending TI TPS62xxx or overseas parts (ignores Chinese DCDC preference)
- ❌ Single rail only (ignores multi-function aspect)
- ❌ Single recommendation per rail (violates Top 3 default)
- ❌ Fabricating Vin / Vout / efficiency numbers
- ❌ Missing headroom principle (just picking cheapest)
- ❌ Forgetting LCSC
