# RA6M5 EK-RA6M5 Quick Start

> **Source:** Renesas-published EK-RA6M5 evaluation kit quick-start
> guide and FSP (Flexible Software Package) example set. BOM is
> **Renesas-only** (single-vendor). For multi-vendor teardown-
> derived solutions see `references/application-solution/`.

## Overview
A Renesas-published getting-started guide for the RA6M5 Cortex-M33
MCU on the EK-RA6M5 evaluation kit, demonstrating FSP project
creation, peripheral bring-up, and FreeRTOS / Azure RTOS support.

- **Vendor:** Renesas Electronics
- **Published as:** EK-RA6M5 Quick Start Guide + FSP example
  projects
- **Document type:** Eval kit guide (vendor-published)
- **EVK:** EK-RA6M5 (RTK7EKA6M5S00001BE)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.renesas.com/en/products/microcontrollers-microprocessors/ra-cortex-m-mcus/ek-ra6m5-evaluation-kit-ra6m5-mcu-group (verification pending)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Renesas/RA6M5.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Renesas/product_families.md` and the datasheet)*

## BOM Candidates (Renesas only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cortex-M33 general-purpose MCU | **RA6M5** | [link](../product_families.md#ra6m5) | Cortex-M33 @ 200 MHz, integrated DCDC, Ethernet |
| EVK platform | **EK-RA6M5** | Renesas product page | Arduino-compatible headers, on-board J-Link OB |

External to Renesas (out of BOM scope for this single-vendor solution):
- USB cable, host PC with e² studio / IAR / Keil

## Reference Design Verification Status

- [ ] Original Renesas product page URL HTTP 200 — verification pending.
- [x] Datasheet already present at
      product page → Documents & Downloads.
- [ ] Confirm FSP version pinned in the cited example (Renesas ships
      FSP releases quarterly; example paths drift across versions).
- [ ] Pin the exact RA6M5 part number — the family includes R7FA6M5
      variants with different pin counts and peripherals.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The RA6M5 spec values
> live in the maintainer's private spec database (`specs/Renesas/RA6M5.yaml`, if installed) and are cited to the datasheet
> PDF under product page → Documents & Downloads.
> See that YAML for verified values.

## Source Discipline

- Original guide published by Renesas on renesas.com / in FSP
  example projects.
- This entry only references Renesas parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
