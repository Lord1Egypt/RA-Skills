# Fixture 18 — Without-skill baseline (MCU comparison)

**Purpose**: Companion to fixture 17. Demonstrates the structural
quality difference on a different query type — *general MCU comparison*
(rather than BLE-specific). The baseline exhibits a similar set of
failure modes to fixture 17 but with MCU-specific extras (price
fabrication, missing modern silicon, conflating internal vs external
flash).

**User persona**: Engineer / student asking a broad catalog question
without project constraints.

## Input prompt (verbatim)

> Provide comparison table of commonly used MCUs in the industry

## What a generic LLM (no skill) typically produces

See `expected-outputs/18-without-skill-mcu-baseline.expected.md` for
the canonical baseline. Common failure modes the baseline exhibits:

1. **Fabricated prices** — model adds "$1.5 / $4-6 / $8-15" entries
   without any distributor data. SKILL.md explicitly bans price
   fabrication ("always mark as 'depends on quote / distributor'").
2. **Inflated coverage** — every cell is filled, no "not verified"
   markers anywhere.
3. **Single recommendation per row** — the "application" column
   shows Top-1 picks (e.g. "入门选 STM32F103") instead of Top 3 +
   single comparison table per scenario.
4. **Missing modern silicon** — the baseline mentions STM32F1/F4
   (legacy) but not STM32G0/U5/H7/WB55/WL55; mentions nRF52840 but
   not nRF5340/nRF54L15; does not include any Series 2 EFR32; no
   Chinese domestic MCUs (GD32 / WCH) at all.
5. **Conflated specs** — ESP32's "4 MB flash" is external SPI flash
   not internal; STM32F407's "192 KB RAM" mixes CCM and SRAM.
6. **No source citation** — every number is ungrounded; no tier, no
   URL, no verification date.
7. **Missing vendors** — Microchip PIC and TI MSP430 are not in the
   skill's catalog scope but are mentioned anyway; the model would
   have been better served by flagging "outside catalog scope — fetch
   vendor URL for spec verification".

## Why this fixture exists

Pair with fixture 17 to demonstrate that the skill's value is
**consistent across query types** (BLE-specific and general MCU),
not a one-off. Both fixtures show the same anti-pattern categories
appearing in the baseline (price fabrication, missing modern parts,
inflated confidence, no citations) and being systematically prevented
by the skill's structural constraints.

## Acceptance criteria for the WITH-SKILL answer

The with-skill answer to the same prompt must:

- [ ] Group candidates by use-case scenario (entry-level / general /
      high-performance) since "commonly used" is not a single archetype
- [ ] Top 3 per scenario, with a single comparison table per scenario
- [ ] Each cell cited with tier + URL + verification date
- [ ] "not verified" markers on any field not in Tier 1 YAML
- [ ] Explicit "outside catalog scope" note for Microchip / MSP430 /
      RP2040 if mentioned (rather than fabricating data for them)
- [ ] No price fabrication — the with-skill answer should redirect
      to distributor URLs instead
- [ ] Catch MCU parts released in the last 2-3 years (STM32U5,
      nRF54L15, EFR32BG24) that the baseline misses

## Test methodology

Same as fixture 17:

1. Without-skill response: capture as the canonical baseline.
2. With-skill response: produce against the rubric.
3. Compare scores.

Expected scores:
- Without skill: 3-5 / 25 (similar to fixture 17)
- With skill: ≥ 19 / 25

## Maintenance

Same as fixture 17. The "modern silicon released after training
cutoff" category is especially important to track — newer LLM
training data should narrow this gap over time.