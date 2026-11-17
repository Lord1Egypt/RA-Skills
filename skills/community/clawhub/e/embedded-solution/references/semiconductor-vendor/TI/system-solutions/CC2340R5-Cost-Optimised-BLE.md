# CC2340R5 Cost-Optimised BLE

> **Source:** TI-published SimpleLink CC2340R5 SDK BLE peripheral
> example for the cost-optimised CC2340R5 BLE 5.3 MCU. BOM is
> **TI-only** (single-vendor).

## Overview
A TI-published SDK example demonstrating low-cost BLE peripheral
designs on the CC2340R5 Cortex-M0+ wireless MCU, targeting
disposable medical sensors, beacons, and appliance connectivity.

- **Vendor:** Texas Instruments
- **Published as:** SimpleLink CC2340R5 SDK
  `examples/rtos/LP_EM_CC2340R5/blestack/basic_ble`
- **Document type:** SDK example (source code + readme)
- **EVK:** LP-EM-CC2340R5
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.ti.com/tool/LP-EM-CC2340R5 (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/TI/CC2340R5.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/TI/product_families.md` and the datasheet)*

## BOM Candidates (TI only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cost-optimised BLE 5.3 MCU | **CC2340R5** | [link](../product_families.md) | Cortex-M0+, 512 KB flash, integrated DCDC |
| EVK platform | **LP-EM-CC2340R5** | TI product page | BoosterPack-compatible daughterboard form factor |

External to TI (out of BOM scope for this single-vendor solution):
- USB cable, host PC with CCS, smartphone for BLE testing

## Reference Design Verification Status

- [ ] Original TI product page URL HTTP 200 — verification pending.
- [ ] CC2340R5 datasheet not yet downloaded.
- [ ] Confirm SDK example path matches the latest SimpleLink SDK
      release — TI consolidated CC2340 SDK under one bundle; double-
      check it exists in the cited location.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The CC2340R5 spec values
> live in the maintainer's private spec database (`specs/TI/CC2340R5.yaml`, if installed). Datasheet PDF not yet
> downloaded.

## Source Discipline

- Original example published by TI on ti.com / in TI GitHub repos.
- This entry only references TI parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
