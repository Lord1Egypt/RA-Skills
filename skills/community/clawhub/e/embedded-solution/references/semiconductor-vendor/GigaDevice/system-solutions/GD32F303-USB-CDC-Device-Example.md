# GD32F303 USB-CDC Device Example

> **Source:** GigaDevice-published GD32 firmware library example for
> a USB Full-Speed CDC (virtual COM port) device running on the
> GD32F303 Cortex-M4 MCU. BOM is **GigaDevice-only** (single-vendor).

## Overview
A GigaDevice-published firmware example showing a USB device-mode
CDC ACM class driver on the GD32F303 mainstream MCU, paired with the
GD32F303R-START evaluation kit. Useful as a starting point for any
USB-to-serial bridge or virtual COM port design based on GD32.

- **Vendor:** GigaDevice
- **Published as:** GD32 firmware library example
  `Examples/USB/USBFS/USB_Device/CDC_ACM`
- **Document type:** SDK example (source code + readme)
- **EVK:** GD32F303R-START (with on-board USB-FS connector)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.gigadevice.com/product/mcu/main-stream-mcus/gd32f30x-series (verification pending; site reachable via browser, datasheet PDF on gd32mcu.com)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/GigaDevice/GD32F303xx.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/GigaDevice/product_families.md` and the datasheet)*

## BOM Candidates (GigaDevice only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cortex-M4 mainstream MCU with USB FS | **GD32F303** | [link](../product_families.md#gd32f303xx) | ARM Cortex-M4 @ 120 MHz, up to 3072 KB flash, 96 KB SRAM |
| EVK platform | **GD32F303R-START** | GigaDevice product page | On-board USB-FS connector, Arduino-compatible headers |

External to GigaDevice (out of BOM scope for this single-vendor solution):
- USB cable (to host PC)
- Host PC with terminal program (PuTTY, minicom, screen)
- Optional: terminal-side driver that opens the VCP as a serial port

## Reference Design Verification Status

- [ ] Original GigaDevice product page URL HTTP 200 — verification pending.
- [x] Datasheet already present at
      product page → Documents & Downloads (Rev 1.9).
- [ ] Pin the exact GD32F303 part number (GD32F303RCT6 vs other
      package / flash combinations on the R-START board).
- [ ] Confirm firmware library version (GD32F30x Firmware Library
      rev) — different revs use slightly different USB driver APIs.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The GD32F303 spec values
> (clock, flash, SRAM, supply voltage) live in
> `specs/GigaDevice/GD32F303xx.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet
> PDF under product page → Documents & Downloads.

## Source Discipline

- Original example published by GigaDevice on gd32mcu.com / in the
  GD32 firmware library GitHub repository.
- This entry only references GigaDevice parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.

## Migration Note

GD32F303 is a popular **drop-in upgrade for STM32F103** in many
designs — pin-compatibility on the LQFP48 package and similar
peripheral layout (USB, USART, SPI, I2C, CAN). Firmware libraries
are NOT binary-compatible with STM32, but the GD32 SPL (Standard
Peripheral Library) follows a very similar API surface, so most
STM32F103 firmware can be ported with mechanical search-and-replace.
