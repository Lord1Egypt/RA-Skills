# Fixture 11 — WCH cost-sensitive MCU (catalog regression test)

**User persona:** Cost-sensitive hardware designer in China exploring domestic alternatives
**Source conversation:** 2026-06-27 (added after WCH added to catalogue)

## Input prompt (verbatim)

> "I need a microcontroller for a USB-to-serial bridge. Cost is the top priority. Prefer domestic suppliers."

## What the skill should do

1. **Trigger check** — embedded system design, chip selection = triggers.
2. **Step 4 — Search Priority**:
   - Tier 2: read `references/semiconductor-vendor/WCH/product_families.md` for CH32V103 entry
   - Tier 2: read `specs/WCH/CH32V103R8T6.yaml` (maintainer's private spec database, not shipped in public release; if installed) for placeholder fields
   - Tier 3: fetch WCH product page (no Cloudflare gating observed) for current specs
3. **Step 5 — defaults-first**:
   - Default: USB-to-serial bridge (consumer-grade, indoor, low-cost)
   - User already specified "cost top priority" + "domestic suppliers" → these are explicit overrides
4. **Step 6 — Top 3**:
   - Slot A: **CH32V103R8T6** (WCH) — built-in USB device, RISC-V, lowest cost, domestic ⭐
   - Slot B: **CH32F103C8T6** (WCH) — ARM Cortex-M3 variant if user prefers ARM over RISC-V
   - Slot C: **CH340N** (WCH) — dedicated USB-serial IC (no MCU needed) for simpler designs
5. **Skill should call out**:
   - WCH has 3 viable options depending on architecture preference (RISC-V vs ARM vs dedicated IC)
   - All three are stocked on LCSC, Mouser, Digi-Key (Tier 3 vendor)
   - Cross-reference: GD32VF103 (GigaDevice RISC-V) as second-source alternative

## Expected behaviour (defaults-first)

Skill produces a Top 3 + comparison table where:
- All 3 candidates are WCH (user said "domestic" + "cost")
- Skill distinguishes RISC-V (CH32V) vs ARM (CH32F) vs dedicated IC (CH340N)
- Cost framing: CH340N < CH32F103 < CH32V103 (verify with vendor)
- Tier 3 mirror list mentions LCSC prominently (Chinese-vendor parts)

### Example acceptable response structure

> ## Top 3 — USB-to-serial bridge MCU (WCH, cost-optimised)
>
> *[Assumed: USB CDC device class, indoor consumer, <$1 BOM cost target. Tell me if industrial or other bridge protocol.]*
>
> ### Comparison
>
> | Slot | Chip | Architecture | USB | Best for | Cost tier |
> |------|------|--------------|-----|----------|-----------|
> | A | **CH32V103R8T6** | RISC-V (QingKe V2) | built-in device | "real" MCU + USB, future firmware expansion | low |
> | B | **CH32F103C8T6** | ARM Cortex-M3 | built-in device | STM32F103 firmware portability | low |
> | C | **CH340N** | dedicated USB-serial IC | built-in | dedicated bridge, no MCU logic needed | lowest |
>
> ### Recommendation
>
> **CH32V103R8T6** — best balance of cost + flexibility for a USB-serial bridge with room to grow.
>
> **CH32F103C8T6** — if you already have STM32F103 firmware / toolchain.
>
> **CH340N** — if you just need a dumb USB-serial bridge and have no MCU-side logic.

## Acceptance criteria

- [ ] All 3 candidates are **WCH** (respect user's "domestic suppliers" preference)
- [ ] Comparison distinguishes RISC-V vs ARM vs dedicated IC
- [ ] Cost framing given as tier (not single number)
- [ ] Tier 3 mirror list: **LCSC** mentioned prominently (WCH parts stocked there)
- [ ] Citation to `references/semiconductor-vendor/WCH/product_families.md#ch32v103r8t6` present
- [ ] Citation to `specs/WCH/CH32V103R8T6.yaml` (Tier 1 placeholder, maintainer's private spec database, not shipped in public release) present
- [ ] Defaults stated inline
- [ ] No fabricated spec numbers (per Tier 1 placeholder YAML)

## Anti-patterns to fail

- ❌ Recommending STM32F103 (overseas, ignores "domestic" preference)
- ❌ Recommending only 1 chip (violates Top 3 default)
- ❌ Missing the CH340N option for "dedicated IC" use case
- ❌ Fabricating clock/RAM/flash numbers (placeholder YAML marks `unverified: [all]`)
- ❌ Forgetting LCSC as Tier 3 mirror for Chinese vendor
- ❌ Saying "all three are equivalent" (they serve different use cases)

## How this fixture tests the catalogue

This fixture **only passes if WCH is in the catalogue** — regression test for the
2026-06-27 catalog expansion (commit `6a0ec69`). If WCH gets removed, this fixture
breaks (skill can't find the candidate to recommend).
