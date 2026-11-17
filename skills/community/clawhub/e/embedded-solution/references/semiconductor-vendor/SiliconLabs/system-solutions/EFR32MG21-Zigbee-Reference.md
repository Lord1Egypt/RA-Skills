# EFR32MG21 Zigbee Reference

> **Source:** Silicon Labs-published reference design using the EFR32MG21 Silicon Labs Series 2 Multiprotocol SoC.
> BOM is **Silicon Labs-only** (single-vendor). For multi-vendor silicon labs series 2 multiprotocol soc solutions, see
> `references/application-solution/` (when applicable).

## Overview

A Silicon Labs multiprotocol reference design using the EFR32MG21 for Zigbee 3.0 mesh networking with concurrent BLE commissioning.

Common application: typical Silicon Labs reference design example using the EFR32MG21.

- **Vendor:** Silicon Labs
- **Published as:** Silicon Labs reference design in datasheet / SDK example
- **Document type:** Reference design (typical application schematic)
- **Date reviewed:** 2026-06-27
- **Document revision:** "Silicon Labs-published, no formal revision number" — refer to vendor product page for the latest reference.

## Reference Design

- **Product page:** See `references/semiconductor-vendor/Silicon Labs/product_families.md#efr32mg21`
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/SiliconLabs/EFR32MG21.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Silicon Labs/product_families.md` and the datasheet)*

## BOM Candidates (Silicon Labs only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Hero part (MCU / SoC) | **EFR32MG21** | [link](../product_families.md#efr32mg21) | Silicon Labs Series 2 Multiprotocol SoC (Zigbee + BLE) |
| Decoupling / passives | (external) | — | 100 nF per VDD + bulk caps |
| Crystal (if external) | (external) | — | Verify frequency with datasheet |

External to Silicon Labs (out of BOM scope for this single-vendor solution):
- Decoupling capacitors
- Crystal or resonator (if not internal)
- Antenna matching network (for wireless parts)
- Sensors / actuators (application-dependent)

## Reference Design Verification Status

- [x] Hero part (EFR32MG21) has a vendor product page URL in
      `references/semiconductor-vendor/Silicon Labs/product_families.md`
- [ ] Specific reference design / schematic from Silicon Labs documentation
      was not downloaded in this entry. **This file documents the *type* of
      reference design, not the exact Silicon Labs-published schematic.**

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The EFR32MG21 spec values
> live in the maintainer's private spec database (`specs/SiliconLabs/EFR32MG21.yaml`, if installed)
> and are cross-checked against the official vendor datasheet PDF
> Public-release users should download the datasheet directly from the vendor product page (see Main Page column above); the embedded_dev/ path is for development cloning with the datasheets plug-in.
> `references/semiconductor-vendor/Silicon Labs/product_families.md#efr32mg21`.
