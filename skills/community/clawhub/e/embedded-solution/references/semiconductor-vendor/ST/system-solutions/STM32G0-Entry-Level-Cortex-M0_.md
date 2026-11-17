# STM32G0 Entry-Level Cortex-M0+

> **Source:** ST-published reference design using the STM32G0 ST entry-level Cortex-M0+ MCU.
> BOM is **ST-only** (single-vendor). For multi-vendor st entry-level cortex-m0+ mcu solutions, see
> `references/application-solution/` (when applicable).

## Overview

An ST entry-level reference design using the STM32G0 as the modern replacement for STM32F0 / STM32F1 in cost-sensitive consumer designs.

Common application: typical ST reference design example using the STM32G0.

- **Vendor:** ST
- **Published as:** ST reference design in datasheet / SDK example
- **Document type:** Reference design (typical application schematic)
- **Date reviewed:** 2026-06-27
- **Document revision:** "ST-published, no formal revision number" — refer to vendor product page for the latest reference.

## Reference Design

- **Product page:** See `references/semiconductor-vendor/ST/product_families.md#stm32g0`
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/ST/STM32G0.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/ST/product_families.md` and the datasheet)*

## BOM Candidates (ST only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Hero part (MCU / SoC) | **STM32G0** | [link](../product_families.md#stm32g0) | ST entry-level Cortex-M0+ MCU (modern STM32F103 replacement) |
| Decoupling / passives | (external) | — | 100 nF per VDD + bulk caps |
| Crystal (if external) | (external) | — | Verify frequency with datasheet |

External to ST (out of BOM scope for this single-vendor solution):
- Decoupling capacitors
- Crystal or resonator (if not internal)
- Antenna matching network (for wireless parts)
- Sensors / actuators (application-dependent)

## Reference Design Verification Status

- [x] Hero part (STM32G0) has a vendor product page URL in
      `references/semiconductor-vendor/ST/product_families.md`
- [ ] Specific reference design / schematic from ST documentation
      was not downloaded in this entry. **This file documents the *type* of
      reference design, not the exact ST-published schematic.**

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The STM32G0 spec values
> live in the maintainer's private spec database (`specs/ST/STM32G0.yaml`, if installed)
> and are cross-checked against the official vendor datasheet PDF
> Public-release users should download the datasheet directly from the vendor product page (see Main Page column above); the embedded_dev/ path is for development cloning with the datasheets plug-in.
> `references/semiconductor-vendor/ST/product_families.md#stm32g0`.
