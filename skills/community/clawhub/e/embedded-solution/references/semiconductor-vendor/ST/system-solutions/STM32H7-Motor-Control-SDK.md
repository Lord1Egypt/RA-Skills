# STM32H7 Motor-Control SDK

> **Source:** ST-published X-CUBE-MCSDK (STM32 Motor Control
> Software Development Kit) FOC example running on an STM32H7-based
> evaluation kit. BOM is **ST-only** (single-vendor). For multi-vendor
> teardown-derived solutions see `references/application-solution/`.

## Overview
An ST-published SDK example for sensorless FOC motor control on the
STM32H7 Cortex-M7 MCU, including current sensing, PWM generation,
and field-oriented control loops. Hero part is **STM32H7**, not the
G4 family that some motor-control EVKs use.

- **Vendor:** STMicroelectronics
- **Published as:** X-CUBE-MCSDK package example (`FOC` library,
  motor-control Workbench project)
- **Document type:** SDK example (source code + Workbench project)
- **EVK:** STEVAL-SPIN3202 (STM32F0-based low-voltage driver; for
  an STM32H7-class reference use a Nucleo-STM32H743ZI plus an
  STSPIN power stage such as STSPIN32F0B / STSPIN32G4, or the
  STEVAL-IHM07M1 dual-BLDC platform with H7 adapter). The exact
  EVK must be picked to match a real STM32H7 reference design —
  see Verification Status.
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.st.com/en/embedded-software/x-cube-mcsdk.html (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/ST/STM32H7.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/ST/product_families.md` and the datasheet)*

## BOM Candidates (ST only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cortex-M7 high-performance MCU | **STM32H7** | [link](../product_families.md) | Multiple SKUs (H743 / H750 / H7B3) — cite exact SKU |
| EVK platform (motor-control focused) | **STEVAL-IHM07M1** (or H7-paired equivalent) | ST product page | Dual 3-phase inverter; needs STM32H7 adapter board |

External to ST (out of BOM scope for this single-vendor solution):
- 3-phase BLDC / PMSM motor, USB cable, host PC with ST Motor
  Control Workbench

## Reference Design Verification Status

- [ ] Original ST product page URL HTTP 200 — verification pending.
- [ ] STM32H7 datasheet not yet downloaded.
- [ ] **Pick the right H7 EVK before publishing this entry.** The
      earlier draft cited B-G431B-ESC1, which actually uses
      **STM32G431** in production — that would mismatch the YAML
      hero part. ST's published STM32H7 motor-control path uses
      X-CUBE-MCSDK against a Nucleo-STM32H743ZI plus a power-stage
      board. Confirm the exact pairing before citing source code.
- [ ] Pin the exact STM32H7 SKU (H743 vs H750 vs H7B3) — they differ
      on RAM, peripherals, and crypto.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The STM32H7 spec values
> live in the maintainer's private spec database (`specs/ST/STM32H7.yaml`, if installed). Datasheet PDF not yet downloaded.

## Source Discipline

- Original example published by ST on st.com / in ST GitHub repos.
- This entry only references ST parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
