# Fixture 12 — Silergy power tree (catalog regression test)

**User persona:** Power-tree designer for IoT node evaluating Chinese DCDC alternatives
**Source conversation:** 2026-06-27 (added after Silergy added to catalogue)

## Input prompt (verbatim)

> "I'm designing a 5V-powered IoT sensor node. Need 3.3V at 1.5A for the main rail, and 1.8V at 100mA for a sensor. Prefer Chinese DCDC vendors."

## What the skill should do

1. **Trigger check** — power tree design, BOM = triggers.
2. **Step 4 — Search Priority**:
   - Tier 2: read `references/semiconductor-vendor/Silergy/product_families.md` for SY8089 (2A), SY8120i (3A), SY6280 (LDO)
   - Tier 2: read `specs/Silergy/SY8089.yaml`, `specs/Silergy/SY8120i.yaml`, `specs/Silergy/SY6970.yaml` (maintainer's private spec database, not shipped in public release; if installed)
   - Tier 3: fetch Silergy product pages (no Cloudflare gating) for current specs
3. **Step 5 — defaults-first**:
   - Default: indoor consumer, 1k-10k production, China-domestic preference (user explicit)
   - 1.5A at 3.3V → SY8120i (3A part) or SY8089 (2A part) — close to spec, verify with datasheet
   - 100mA at 1.8V → LDO (Silergy SY6280 or similar)
4. **Step 6 — Top 3 components**:
   - Slot A: **SY8120i** (Silergy) — 3A synchronous buck, headroom for 1.5A load
   - Slot B: **SY8089** (Silergy) — 2A synchronous buck, slightly smaller / cheaper if load is verified ≤ 1.5A continuous
   - Slot C: SY6280 LDO for the 1.8V rail
5. **Skill should call out**:
   - 2A vs 3A selection depends on continuous vs peak load (verify with datasheet)
   - Headroom principle: pick the higher-current part for thermal margin
   - Tier 3 mirror: LCSC, Mouser, Digi-Key all carry Silergy

## Expected behaviour (defaults-first)

Skill produces a Top 3 + comparison table where:
- 2 candidates for the main 3.3V rail (SY8120i vs SY8089)
- 1 candidate for the 1.8V rail (LDO)
- All 3 candidates are Silergy (user said "Chinese DCDC vendors")
- Cost framing given as tier
- Headroom principle explained

### Example acceptable response structure

> ## Top 3 — 5V → 3.3V (1.5A) + 1.8V (100mA) power tree (Silergy, Chinese DCDC)
>
> *[Assumed: indoor consumer IoT, 1k-10k volume, China-domestic preference. Tell me if outdoor or industrial.]*
>
> ### 3.3V main rail (1.5A continuous)
>
> | Slot | Chip | Current rating | Why | Trade-off |
> |------|------|----------------|-----|-----------|
> | A | **SY8120i** | 3A | Headroom for 1.5A load (2x margin), better thermal | slightly higher cost |
> | B | **SY8089** | 2A | lower cost, smaller package | tight margin if load peaks |
>
> Recommendation: **SY8120i** — 2x current headroom is industry best practice.
>
> ### 1.8V sensor rail (100mA)
>
> | Slot | Chip | Function | Notes |
> |------|------|----------|-------|
> | C | **SY6280** | LDO | low quiescent current, sufficient for 100mA |
>
> ### Sources
> - references/semiconductor-vendor/Silergy/product_families.md#sy8120i
> - references/semiconductor-vendor/Silergy/product_families.md#sy8089
> - references/semiconductor-vendor/Silergy/product_families.md#sy6280

## Acceptance criteria

- [ ] All 3 candidates are **Silergy** (respect user's "Chinese DCDC" preference)
- [ ] Main rail Top 2 (SY8120i vs SY8089)
- [ ] Secondary rail Top 1 (SY6280 LDO)
- [ ] Current ratings vs load explained
- [ ] Headroom principle mentioned (2x margin for current)
- [ ] Citation to `references/semiconductor-vendor/Silergy/product_families.md` present
- [ ] Citation to `specs/Silergy/SY8120i.yaml`, `specs/Silergy/SY8089.yaml`, `specs/Silergy/SY6970.yaml` (Tier 1 placeholder, maintainer's private spec database, not shipped in public release) present
- [ ] LCSC mentioned as Tier 3 mirror
- [ ] No fabricated spec numbers

## Anti-patterns to fail

- ❌ Recommending TI TPS62xxx or other overseas (ignores "Chinese DCDC" preference)
- ❌ Recommending only 1 chip per rail (violates Top 3 default at function level)
- ❌ Missing the 1.8V LDO function (treats design as single-rail)
- ❌ Fabricating Vin/Vout/efficiency numbers
- ❌ Recommending SY8120i without comparing to SY8089 (only 1 candidate)
- ❌ Forgetting headroom principle (just picking the cheapest)

## How this fixture tests the catalogue

This fixture **only passes if Silergy is in the catalogue** — regression test for the
2026-06-27 catalog expansion (commit `6a0ec69`). Also tests multi-function BOM
(2 rails, not 1).
