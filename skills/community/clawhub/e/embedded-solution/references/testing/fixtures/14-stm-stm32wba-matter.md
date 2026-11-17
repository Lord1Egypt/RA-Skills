# Fixture 14 — ST STM32WBA Matter single-chip (catalogue regression)

**User persona:** Smart home engineer migrating from STM32WB55 to newer Matter-ready chip
**Source conversation:** 2026-06-27 (added after STM32WBA added to catalogue)

## Input prompt (verbatim)

> "I designed a Matter sensor with STM32WB55 last year. Now I want to migrate to a newer chip with built-in secure element. What should I use?"

## What the skill should do

1. **Trigger check** — migration / chip selection = triggers.
2. **Step 4 — Search Priority**:
   - Tier 2: read `references/semiconductor-vendor/ST/product_families.md` for STM32WBA entry
   - Tier 2: read `specs/ST/STM32WBA.yaml` (maintainer's private spec database, not shipped in public release; placeholder, if installed)
   - Tier 3: fetch ST product page (Cloudflare-gated — use Mouser mirror)
3. **Step 5 — defaults-first**:
   - Migration scenario: user already has STM32WB55 firmware/SDK experience
   - Default: indoor consumer Matter sensor, battery-powered
   - "Newer chip with built-in secure element" → user is asking specifically for SESIP-class security
4. **Step 6 — Top 3 migration candidates**:
   - Slot A: **STM32WBA** (ST) — direct successor with SESIP Level 3 secure element ⭐
   - Slot B: **STM32WB55** (ST, current) — keep using it, migration optional
   - Slot C: **EFR32MG24** (Silicon Labs) — alternative vendor with MVP
5. **Skill should call out**:
   - STM32WBA is the obvious direct successor (same ST family, same SDK base, added SESIP)
   - STM32WB55 is still active — migration is optional, not forced
   - EFR32MG24 is the alternative if you want to switch vendors (but loses STM32 ecosystem familiarity)

## Expected behaviour (defaults-first)

Skill produces a Top 3 + comparison table where:
- STM32WBA is clearly the primary recommendation (direct successor + user's specific request)
- STM32WB55 retained as "still good" (migration is optional)
- Migration effort assessment (firmware portability from STM32WB55 → STM32WBA)

### Example acceptable response structure

> ## Top 3 — STM32WB55 → STM32WBA migration (Matter sensor, with SESIP)
>
> *[Assumed: indoor Matter sensor, battery-powered, 1k-10k volume, ST ecosystem familiarity.]*
>
> ### Comparison
>
> | Slot | Chip | Migration effort | Secure element | Why |
> |------|------|-------------------|----------------|-----|
> | A | **STM32WBA** | Low (same ST family + SDK base) | ✅ SESIP Level 3 | Direct successor, you asked for built-in secure element |
> | B | **STM32WB55** | None (keep current) | ❌ external needed | Still active; migration is optional |
> | C | **EFR32MG24** | High (different vendor / SDK) | (verify) | Cross-vendor alternative, but loses ST ecosystem |
>
> ### Recommendation
>
> **STM32WBA** — fits your exact ask. STM32WB55 → STM32WBA is mostly a recompile + driver update; SDK base is similar.
>
> **Stay on STM32WB55** if Matter certification is already done — no need to migrate.
>
> **EFR32MG24** only if you want to explore Silicon Labs ecosystem.

## Acceptance criteria

- [ ] STM32WBA as primary pick (direct successor + user explicit ask for secure element)
- [ ] STM32WB55 retained as "still active, migration optional"
- [ ] EFR32MG24 noted as cross-vendor alternative with explicit migration cost
- [ ] SESIP Level 3 mentioned as STM32WBA's key differentiator
- [ ] Citation to `references/semiconductor-vendor/ST/product_families.md#stm32wba` present
- [ ] Citation to `specs/ST/STM32WBA.yaml` (Tier 1 placeholder, maintainer's private spec database, not shipped in public release) present
- [ ] Tier 3 mirror: **Mouser mirror** mentioned (st.com Cloudflare-gated)
- [ ] Migration effort assessed (low / none / high)
- [ ] No fabricated spec numbers

## Anti-patterns to fail

- ❌ Recommending nRF52840 + nRF7002 (split, doesn't match user's "single-chip successor" need)
- ❌ Forcing migration (STM32WB55 still active — should be mentioned as option)
- ❌ Missing SESIP Level 3 mention (user's explicit ask)
- ❌ Fabricating secure-element certification level
- ❌ Missing the "stay on STM32WB55" option (user might not actually need to migrate)
- ❌ Missing Mouser mirror for ST datasheet (Cloudflare-gated)
- ❌ Saying "all three are equivalent" (STM32WB55 vs STM32WBA vs EFR32MG24 are very different)

## How this fixture tests the catalogue

This fixture **only passes if STM32WBA is in the catalogue** — regression test for the 2026-06-27 catalog expansion (commit `6a0ec69`). Tests migration scenario (different from greenfield design).
