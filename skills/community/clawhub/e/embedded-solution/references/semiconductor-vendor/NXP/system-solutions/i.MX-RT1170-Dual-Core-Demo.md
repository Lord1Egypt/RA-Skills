# i.MX RT1170 Dual-Core Demo

> **Source:** NXP-published reference design for the i.MX RT1170
> crossover MCU dual-core heterogeneous architecture (Cortex-M7 +
> Cortex-M4). BOM is **NXP-only** (single-vendor).

## Overview
An NXP-published application note demonstrating the dual-core boot,
inter-core messaging (RPMsg / MU), and shared-memory partitioning
patterns on the i.MX RT1170 SoC.

- **Vendor:** NXP Semiconductors
- **Published as:** Application Note + MCUXpresso SDK dual-core examples
- **Document type:** Reference design (pro-forma architecture + driver config)
- **EVK:** MIMXRT1170-EVK
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.nxp.com/design/development-boards/i-mx-rt1170-evk (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/NXP/i.MX_RT1170.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/NXP/product_families.md` and the datasheet)*

## BOM Candidates (NXP only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Heterogeneous dual-core MCU | **i.MX RT1170** | [link](../product_families.md) | Cortex-M7 @ 1 GHz + Cortex-M4 @ 400 MHz |
| EVK platform | **MIMXRT1170-EVK** | NXP product page | Large DRAM, parallel LCD, dual-core bring-up firmware |

External to NXP (out of BOM scope for this single-vendor solution):
- USB-C cable, display panel, host PC

## Reference Design Verification Status

- [ ] Original NXP product page URL HTTP 200 — verification pending.
- [ ] i.MX RT1170 datasheet not yet downloaded — see placeholder note.
- [ ] Confirm dual-core boot sequence is the **published** NXP example
      (vs a community port). Cite the exact SDK example path.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The i.MX RT1170 spec values
> live in the maintainer's private spec database (`specs/NXP/i.MX_RT1170.yaml`, if installed). Datasheet PDF not yet
> downloaded.

## Source Discipline

- Original reference design published by NXP on nxp.com.
- This entry only references NXP parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
