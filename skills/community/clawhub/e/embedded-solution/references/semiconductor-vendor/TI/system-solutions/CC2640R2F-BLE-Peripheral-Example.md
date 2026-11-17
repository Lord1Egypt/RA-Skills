# CC2640R2F BLE Peripheral Example

> **Source:** TI-published SimpleLink CC2640R2 SDK BLE peripheral
> example running on the LAUNCHXL-CC2640R2 evaluation board. BOM is
> **TI-only** (single-vendor). For multi-vendor teardown-derived
> solutions see `references/application-solution/`.

## Overview
A TI-published SDK example demonstrating BLE peripheral role
(advertising + GATT + connection) on the CC2640R2F wireless MCU,
using the LAUNCHXL-CC2640R2 LaunchPad.

- **Vendor:** Texas Instruments
- **Published as:** SimpleLink CC2640R2 SDK
  `examples/rtos/CC2640R2_LAUNCHXL/blestack/simple_peripheral`
- **Document type:** SDK example (source code + readme)
- **EVK:** LAUNCHXL-CC2640R2
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.ti.com/tool/LAUNCHXL-CC2640R2 (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/TI/CC2640R2F.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/TI/product_families.md` and the datasheet)*

## BOM Candidates (TI only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| BLE 5.x wireless MCU ⚠️ | **CC2640R2F** ⚠️ | [link](../product_families.md) | Cortex-M3 + Cortex-M0 sensor controller. **TI discontinued new CC2640R2F production in 2024 for several SKUs — verify active status on ti.com before new designs. TI's recommended migration paths are CC2640R2L (lower-cost variant) for cost-sensitive redesigns, or the CC2340R5 / CC2642R families for new product lines.** |
| EVK platform | **LAUNCHXL-CC2640R2** | TI product page | On-board XDS110 debug probe, BoosterPack headers |

External to TI (out of BOM scope for this single-vendor solution):
- USB cable, host PC with CCS / IAR, smartphone for BLE testing

## Reference Design Verification Status

- [ ] Original TI product page URL HTTP 200 — verification pending.
- [ ] CC2640R2F datasheet not yet downloaded.
- [ ] Confirm SimpleLink SDK example path matches the latest SDK
      release (TI rebrands the CC2640R2 SDK to CC26x2 / CC13x2 lines
      over time — verify the right repo is being cited).
- [x] **Discontinued-parts warning added to BOM row.** TI ended
      new CC2640R2F production for several SKUs in 2024. For new
      designs, prefer CC2340R5 (cost-optimised) or CC2642R
      (BLE 5.2 multi-protocol) per TI's official migration guidance.
      For learning or maintaining legacy CC2640R2F designs, the
      SimpleLink CC2640R2 SDK continues to ship.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The CC2640R2F spec values
> live in the maintainer's private spec database (`specs/TI/CC2640R2F.yaml`, if installed). Datasheet PDF not yet
> downloaded.

## Source Discipline

- Original example published by TI on ti.com / in TI GitHub repos.
- This entry only references TI parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
