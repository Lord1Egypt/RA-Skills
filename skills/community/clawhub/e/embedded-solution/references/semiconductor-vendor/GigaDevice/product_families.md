# GigaDevice — Product Families

GigaDevice (Beijing, China) is a fabless semiconductor company best
known for its GD32 line of ARM Cortex-M (and emerging RISC-V) 32-bit
microcontrollers. GD32 MCUs are popular as pin-compatible alternatives
to STM32 in cost-sensitive designs.

This document lists every GigaDevice chip referenced in this skill's
specs/GigaDevice/*.yaml files.

| Part | Family | Status | Datasheet | Link |
|------|--------|--------|-----------|------|
| **GD32F303xx** | ARM Cortex-M4 mainstream MCU | ✅ | [link](https://www.gigadevice.com/product/mcu/main-stream-mcus/gd32f30x-series) | [datasheet](product page → Documents & Downloads) |
| **GD32F450xx** | ARM Cortex-M4 high-performance MCU | ✅ | [link](https://www.gigadevice.com/product/mcu/high-performance-mcus/gd32f4xx-series) | [datasheet](product page → Documents & Downloads) |
| **GD32E230xx** | ARM Cortex-M23 low-power MCU | ⚠️ product page removed (404 on gigadevice.com) | [link](https://www.gigadevice.com/product/mcu/entry-level-mcus) | [datasheet](product page → Documents & Downloads) |

## Status Legend

- ✅  Product page reachable (HTTP 200)
- ⚠️  Product page removed (HTTP 404); part still recommended via datasheet
- ❌  Part has been removed/renamed/relocated — do NOT use
- ⏳  Verification pending — recheck before recommending

## Pin Compatibility Note

GD32F103 is a drop-in upgrade for STM32F103 in many designs. GD32F303
adds more peripherals and faster clocks. GD32F4 / F450 / F470 / H7
series compete with STM32F4 / H7. GD32E series target low-power
Cortex-M23 (compete with STM32L0).


## GD32VF103 Series — RISC-V MCU

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **GD32VF103** | ⚠️ product page removed (404 on gigadevice.com) | https://www.gigadevice.com/product/mcu/low-power-mcus/gd32vf103-series | product page → Documents & Downloads |

---

## Status Notes

- **2026-06-29 v0.4.0 firecrawl pass**: 4 GigaDevice product family pages attempted.
  2 returned real content (GD32F303 28KB, GD32F450 52KB). 2 returned 404
  (GD32E230, GD32VF103) — gigadevice.com appears to have dropped these series
  pages. Snapshots saved to
  `references/semiconductor-vendor/GigaDevice/firecrawl-snapshots/`. 4 credits
  consumed. All 4 GigaDevice yamls (GD32F303xx, GD32F450xx, GD32E230xx,
  GD32VF103) already verified via datasheet extraction — datasheet PDFs
  still in catalog even though product pages are gone.
