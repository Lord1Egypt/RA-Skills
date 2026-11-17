# STM32WB55 Nucleo BLE Peripheral

> **Source:** ST-published STM32CubeWB BLE peripheral example running
> on the NUCLEO-WB55RG evaluation board. BOM is **ST-only**
> (single-vendor). For multi-vendor teardown-derived solutions see
> `references/application-solution/`.

## Overview
An ST-published STM32Cube example demonstrating a BLE peripheral
(advertising + GATT service + connection state) on the STM32WB55
dual-core Cortex-M4 / Cortex-M0+ SoC, using the NUCLEO-WB55RG
as the dev platform.

- **Vendor:** STMicroelectronics
- **Published as:** STM32CubeWB package example
  `Projects/NUCLEO-WB55RG/Applications/BLE/BLE_p2pServer`
- **Document type:** SDK example (source code + readme)
- **EVK:** NUCLEO-WB55RG
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.st.com/en/evaluation-tools/nucleo-wb55rg.html (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/ST/STM32WB55.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/ST/product_families.md` and the datasheet)*

## BOM Candidates (ST only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Dual-core BLE 5.x SoC | **STM32WB55** | [link](../product_families.md) | Cortex-M4 app core + Cortex-M0+ BLE core |
| EVK platform | **NUCLEO-WB55RG** | ST product page | Arduino headers, on-board ST-LINK, USB Type-C |

External to ST (out of BOM scope for this single-vendor solution):
- USB cable, host PC with STM32CubeIDE / STM32CubeProgrammer
- Smartphone for BLE testing

## Reference Design Verification Status

- [ ] Original ST product page URL HTTP 200 — verification pending.
- [ ] STM32WB55 datasheet not yet downloaded.
- [ ] Confirm `BLE_p2pServer` example path is the latest in the
      STM32CubeWB release referenced by the YAML.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The STM32WB55 spec values
> live in the maintainer's private spec database (`specs/ST/STM32WB55.yaml`, if installed). Datasheet PDF not yet downloaded.

## Source Discipline

- Original example published by ST on st.com / in ST GitHub repos.
- This entry only references ST parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
