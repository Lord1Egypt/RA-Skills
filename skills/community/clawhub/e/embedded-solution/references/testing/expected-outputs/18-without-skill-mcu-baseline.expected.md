# Expected output skeleton — Fixture 18 (without-skill MCU baseline)

## What this file is

Canonical baseline that a generic LLM produces **without** the
embedded-solution skill loaded, answering "provide comparison table of
commonly used MCUs in the industry". Stored as a regression fixture.

Use it to:
1. Score any model-without-skill response against the rubric
2. Pair with fixture 17 to show the skill's value is consistent
   across query types
3. Re-run when the catalog adds new vendors / parts to verify the
   baseline still misses them

## Canonical baseline (2026-06-28)

Modern LLM (no skill) typically produces a single flat table covering
~10 widely-known MCUs:

### Industry common MCU comparison

| Vendor | Model | Core | Clock | Flash | RAM | Price (USD) | Application |
|--------|-------|------|-------|-------|-----|-------------|-------------|
| ST | STM32F103 | Cortex-M3 | 72 MHz | 64-128 KB | 20 KB | $1.5 | Entry classic |
| ST | STM32F407 | Cortex-M4F | 168 MHz | 1 MB | 192 KB | $4-6 | High-performance |
| ST | STM32H743 | Cortex-M7 | 480 MHz | 1-2 MB | 1 MB | $8-15 | Flagship |
| NXP | LPC1768 | Cortex-M3 | 100 MHz | 512 KB | 64 KB | $3-5 | Industrial |
| NXP | i.MX RT1064 | Cortex-M7 | 600 MHz | 1-4 MB | 1 MB | $5-8 | Crossover MCU |
| Nordic | nRF52840 | Cortex-M4F | 64 MHz | 1 MB | 256 KB | $5 | BLE |
| Espressif | ESP32 | Xtensa LX6 | 240 MHz | 4 MB | 520 KB | $2 | WiFi+BLE |
| Microchip | PIC16F877A | PIC16 | 20 MHz | 14 KB | 368 B | $2 | 8-bit entry |
| Renesas | RX72N | RXv3 | 240 MHz | 4 MB | 1 MB | $10 | Motor control |
| TI | MSP430G2553 | MSP430 | 16 MHz | 16 KB | 512 B | $1.5 | Ultra-low-power |

### Summary recommendations

- Entry: STM32F103 / PIC16F877A
- High-performance: STM32H743 / i.MX RT1064
- IoT: nRF52840 / ESP32
- Industrial: LPC1768 / RX72N
- Ultra-low-power: MSP430G2553

## 7 documented failure modes of this baseline

| # | Failure mode | Concrete example from baseline | Skill fix |
|---|--------------|--------------------------------|-----------|
| 1 | **Fabricated prices** | "$1.5 / $4-6 / $8-15" all unsourced | SKILL.md: "❌ Pricing (always mark as 'depends on quote / distributor')" |
| 2 | **Inflated confidence** | Every cell filled, no "not verified" anywhere | Anti-patterns list bans fabrication explicitly |
| 3 | **Top-1 per row** | "Application" column = one chip per use case | Step 6 forces Top 3 + single comparison table |
| 4 | **Missing modern silicon** | STM32F1/F4 mentioned; STM32G0/U5/H7/WB55/WL55 absent | Tier 1 catalog scan surfaces every part |
| 5 | **Conflated specs** | ESP32 "4 MB flash" is external SPI; STM32F407 "192 KB RAM" mixes CCM+SRAM | YAML stores internal / external / CCM as separate fields |
| 6 | **No source citation** | Every number ungrounded; no URL, no date, no tier | Step 6 + Step 7 cite tier + URL + timestamp |
| 7 | **Out-of-catalog vendors** | Microchip PIC + TI MSP430 mentioned even though not in skill scope | With-skill: "outside catalog scope — fetch vendor URL" |

## Coverage gap analysis

The skill catalog (as of v0.3.0) contains **45 MCU parts** across 11
vendors. The baseline lists 10 MCUs across 7 vendors.

| Catalog vendor | Parts in catalog | In baseline? |
|----------------|------------------|--------------|
| ST | 9 (G0/U5/U575/U585/H7/WB55/WL55/WBA + MP157) | ⚠️ 3 of 9 (only F1/F4/H7 family names) |
| NXP | 5 (K66/KW45/LPC55S69/i.MX-RT1064/RT1170) | ⚠️ 2 of 5 (only LPC1768/RT1064) |
| Nordic | 6 (nRF52832/840/5340/54L15/7002/9160) | ⚠️ 1 of 6 (only nRF52840) |
| Espressif | 4 (ESP32/C3/C6/S3) | ⚠️ 1 of 4 (only ESP32) |
| Renesas | 18 MCU-related (RA4/RA6/RL78/RX + DA BLE SoCs) | ⚠️ 1 of 18 (only RX72N) |
| TI | 4 MCU (CC1310/CC2640R2F/CC2652R/MSPM0G3507) | ⚠️ 1 of 4 (CC2640R2F family), 1 outside catalog (MSP430) |
| Silicon Labs | 5 (EFR32BG22/BG24/BG27/MG21/MG24) | ❌ 0 of 5 |
| GigaDevice | 4 (GD32E230/F303/F450/VF103) | ❌ 0 of 4 (no Chinese vendor coverage) |
| WCH | 3 (CH32V003/103/307) | ❌ 0 of 3 (no Chinese vendor coverage) |
| Silergy | (power ICs only — not MCU) | — |
| SGMicro | (analog ICs only — not MCU) | — |

**Total: baseline mentions 8 of 45 catalog MCUs (18% coverage)**.
The 37 missing ones include:
- All ST modern silicon (G0/U5/H7/WB55/WL55 + their derivatives)
- All Silicon Labs EFR32 Series 2 (5 parts)
- All Chinese domestic (GigaDevice + WCH = 7 parts)
- Nordic dual-core (nRF5340) and Series 5 (nRF54L15)
- TI MSPM0 (newer Cortex-M0+ replacement for MSP430)

## How to score this baseline against the rubric

Use `evaluation-rubric.md` 5 axes × 5 pts each = 25 max.

| Axis | Expected score (without skill) | Why |
|------|-------------------------------|-----|
| Factual accuracy | 1-2 / 5 | ESP32 flash conflates internal/external; STM32F407 RAM conflation; price fabrication |
| Top-3 discipline | 1 / 5 | Application column is Top-1 per row, not Top 3 + compare |
| No fabrication | 0-1 / 5 | Price column fabricated entirely; "not verified" absent |
| Search priority | 0 / 5 | No tier / URL / date anywhere |
| Source citation | 0 / 5 | No source anchors at all |

**Expected total: 2-4 / 25.**

Note: fixture 17 (BLE) and fixture 18 (MCU) should produce similar
without-skill scores (2-4 / 25), demonstrating the skill's value-add
is structural and consistent across query types.

## How to verify the with-skill version is meaningfully better

The with-skill version should score ≥ 19 / 25 on the same rubric.
The delta (15+ points) should be even larger than fixture 17 because
the catalog has 45 MCU parts vs 14 BLE parts — the catalog scan
benefit is bigger for MCU queries.

## Maintenance

Same as fixture 17. Re-run when:
- The catalog adds new MCU vendors or parts (verify the baseline
  still misses them)
- The evaluation rubric changes
- Newer LLMs score higher on factual accuracy (they may include
  more modern parts) — adjust the expected score ceiling but the
  structural axes (Top-3, no fabrication, search priority, source
  citation) should remain near zero without the skill.