# LPC55S69 TrustZone Example

> **Source:** NXP-published MCUXpresso SDK example demonstrating
> Armv8-M TrustZone-M on the LPC55S69 Cortex-M33 MCU. BOM is
> **NXP-only** (single-vendor).

## Overview
An NXP-published SDK example showing secure / non-secure partition
setup, SAU / IDAU configuration, and secure call gate usage on the
LPC55S69.

- **Vendor:** NXP Semiconductors
- **Published as:** MCUXpresso SDK `lpcxpresso55s69_trustzone_examples`
- **Document type:** SDK example (source code + readme)
- **EVK:** LPCXpresso55S69
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.nxp.com/design/development-boards/lpcxpresso55s69 (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/NXP/LPC55S69.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/NXP/product_families.md` and the datasheet)*

## BOM Candidates (NXP only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cortex-M33 MCU with TrustZone-M | **LPC55S69** | [link](../product_families.md) | TrustZone-M, PowerQuad DSP accelerator |
| EVK platform | **LPCXpresso55S69** | NXP product page | On-board LPC-Link2 debug probe |

External to NXP (out of BOM scope for this single-vendor solution):
- USB cable, host PC with MCUXpresso

## Reference Design Verification Status

- [ ] Original NXP product page URL HTTP 200 — verification pending.
- [ ] LPC55S69 datasheet not yet downloaded.
- [ ] Confirm SDK example path `lpcxpresso55s69_trustzone_examples`
      matches the latest MCUXpresso SDK release.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The LPC55S69 spec values
> live in the maintainer's private spec database (`specs/NXP/LPC55S69.yaml`, if installed). Datasheet PDF not yet
> downloaded.

## Source Discipline

- Original example published by NXP on nxp.com / in NXP MCUXpresso SDK.
- This entry only references NXP parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
