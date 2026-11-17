# MSPM0G3507 LaunchPad Demo

> **Source:** TI-published MSPM0 SDK example running on the
> LP-MSPM0G3507 LaunchPad evaluation board. BOM is **TI-only**
> (single-vendor).

## Overview
A TI-published SDK example demonstrating peripheral bring-up
(GPIO, Timers, ADC, UART) on the MSPM0G3507 Cortex-M0+ general-
purpose MCU. Targets entry-level motor control, lighting, and
appliance applications.

- **Vendor:** Texas Instruments
- **Published as:** MSPM0 SDK `examples/nortos/LP_MSPM0G3507/`
- **Document type:** SDK example (source code + readme)
- **EVK:** LP-MSPM0G3507
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.ti.com/tool/LP-MSPM0G3507 (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/TI/MSPM0G3507.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/TI/product_families.md` and the datasheet)*

## BOM Candidates (TI only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cortex-M0+ general-purpose MCU | **MSPM0G3507** | [link](../product_families.md) | 80 MHz, 128 KB flash, integrated op-amps |
| EVK platform | **LP-MSPM0G3507** | TI product page | On-board XDS110 debug probe, BoosterPack headers |

External to TI (out of BOM scope for this single-vendor solution):
- USB cable, host PC with CCS

## Reference Design Verification Status

- [ ] Original TI product page URL HTTP 200 — verification pending.
- [ ] MSPM0G3507 datasheet not yet downloaded.
- [ ] Confirm MSPM0 SDK version matches the cited example path;
      TI ships this as a separate SDK (not the SimpleLink bundle).
- [ ] Confirm MSPM0G3507 vs MSPM0G3107 / other G-series SKUs — they
      differ on peripheral count.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The MSPM0G3507 spec values
> live in the maintainer's private spec database (`specs/TI/MSPM0G3507.yaml`, if installed). Datasheet PDF not yet
> downloaded.

## Source Discipline

- Original example published by TI on ti.com / in TI GitHub repos.
- This entry only references TI parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
