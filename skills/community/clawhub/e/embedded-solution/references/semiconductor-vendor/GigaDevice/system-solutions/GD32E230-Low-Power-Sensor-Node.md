# GD32E230 Low-Power Sensor Node

> **Source:** GigaDevice-published reference design for a coin-cell
> powered sensor node on the GD32E230 Cortex-M23 MCU. BOM is
> **GigaDevice-only** (single-vendor).

## Overview
A GigaDevice-published reference design demonstrating deep-sleep
modes, RTC wake, and battery-friendly ADC sampling on the GD32E230
Cortex-M23 MCU. Targets applications like remote sensors, building
automation, and metering.

- **Vendor:** GigaDevice
- **Published as:** GD32 firmware library example + AN113
  application note (Low-power design with GD32E230)
- **Document type:** Reference design (pro-forma BOM + low-power
  profile)
- **EVK:** GD32E230C-START or GD32E230K-START
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.gigadevice.com/product/mcu/low-power-mcus/gd32e230xx-series (verification pending)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/GigaDevice/GD32E230xx.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/GigaDevice/product_families.md` and the datasheet)*

## BOM Candidates (GigaDevice only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cortex-M23 low-power MCU | **GD32E230** | [link](../product_families.md#gd32e230xx) | ARM Cortex-M23 @ 72 MHz, 64 KB flash, 8 KB SRAM |
| EVK platform | **GD32E230C-START** | GigaDevice product page | On-board J-Link, Arduino-compatible headers |

External to GigaDevice (out of BOM scope for this single-vendor solution):
- CR2032 coin cell or 2xAA battery holder
- External sensor (temperature, humidity, accelerometer, etc.)
- Optional debug probe (J-Link / GD-Link)

## Reference Design Verification Status

- [ ] Original GigaDevice product page URL HTTP 200 — verification pending.
- [x] Datasheet already present at
      product page → Documents & Downloads (Rev 1.4).
- [ ] Pin the exact GD32E230 part number (GD32E230C8T6 for 64 KB /
      LQFP48, GD32E230K8T6 for 64 KB / LQFP32).
- [ ] Document the cited deep-sleep current value (typically
      < 1 µA with RTC running, but datasheet should be cited).

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The GD32E230 spec values
> (clock, flash, SRAM, supply voltage) live in
> `specs/GigaDevice/GD32E230xx.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet
> PDF under product page → Documents & Downloads.

## Source Discipline

- Original reference design published by GigaDevice on gd32mcu.com.
- This entry only references GigaDevice parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.

## Architecture Note

GD32E230 uses **ARM Cortex-M23** — the smallest, most energy-efficient
ARMv8-M core. It is architecturally similar to STM32L0 (also
Cortex-M23 + M0-compatible Thumb-2 subset). Code written for STM32L0
can usually be ported with minor register-level changes; the GD32 SPL
API mirrors the STM32 Standard Peripheral Library naming.
