# STM32U5 Ultra-Low-Power Demo

> **Source:** ST-published reference design for the STM32U5 ultra-low-
> power Cortex-M33 MCU, demonstrating stop-to-active currents in the
> sub-µA range. BOM is **ST-only** (single-vendor).

## Overview
An ST-published application note walking through low-power mode
selection (Stop 0/1/2, Standby, Shutdown), RTC wake, and SRAM
retention sizing on the STM32U5 series.

- **Vendor:** STMicroelectronics
- **Published as:** Application Note + STM32CubeU5 examples
- **Document type:** Reference design (pro-forma bring-up + power-profile recipe)
- **EVK:** NUCLEO-U575ZI-Q
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.st.com/en/evaluation-tools/nucleo-u575zi-q.html (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/ST/STM32U5.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/ST/product_families.md` and the datasheet)*

## BOM Candidates (ST only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Ultra-low-power Cortex-M33 MCU | **STM32U5** | [link](../product_families.md) | Multiple SKUs (U575 / U585 / etc.) — cite exact SKU |
| EVK platform | **NUCLEO-U575ZI-Q** | ST product page | Arduino headers, on-board ST-LINK |

External to ST (out of BOM scope for this single-vendor solution):
- USB cable, host PC, optional current meter

## Reference Design Verification Status

- [ ] Original ST product page URL HTTP 200 — verification pending.
- [ ] STM32U5 datasheet not yet downloaded.
- [ ] Pin down the exact STM32U5 SKU cited in the reference design
      (U575 vs U585 vs others — they differ on security peripherals).
- [ ] Confirm the low-power numbers are cited from the datasheet and
      **not** measured on the EVK only — those two values can differ
      by 2-3x at Stop2 entry.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The STM32U5 spec values
> live in the maintainer's private spec database (`specs/ST/STM32U5.yaml`, if installed). Datasheet PDF not yet downloaded.

## Source Discipline

- Original reference design published by ST on st.com.
- This entry only references ST parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
