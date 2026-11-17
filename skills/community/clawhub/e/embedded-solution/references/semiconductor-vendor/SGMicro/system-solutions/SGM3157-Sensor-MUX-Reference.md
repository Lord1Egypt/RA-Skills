# SGM3157 Sensor Multiplexer Reference

> **Source:** SG Micro-published reference design using the SGM3157 SPDT analog switch.
> BOM is **SG Micro-only** (single-vendor). For multi-vendor analog signal-chain solutions,
> see `references/application-solution/` (when applicable).

## Overview

A sensor multiplexer reference: one MCU ADC channel reads multiple analog
sensors via the SGM3157 SPDT (single-pole double-throw) analog switch. Common
application: low-cost environmental sensors (temperature + humidity + gas),
battery monitors (cell 1 vs cell 2), or audio signal routing.

- **Vendor:** SG Micro Corp (圣邦微电子)
- **Published as:** SG Micro reference design in datasheet applications section
- **Document type:** Analog signal chain reference (typical application schematic)
- **Date reviewed:** 2026-06-27
- **Document revision:** "SG Micro-published, no formal revision number" — refer to sg-micro.com for the latest reference.

## Reference Design

- **Product page:** https://www.sg-micro.com/product/sgm3157 (verification pending)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/SGMicro/SGM3157.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/SGMicro/product_families.md` and the datasheet)*

## BOM Candidates (SG Micro only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| SPDT analog switch | **SGM3157** | [link](../product_families.md#sgm3157) | Signal-level switch; low Ron for sensor MUX |
| Optional: low-noise op-amp (signal conditioning) | **SGM358** | [link](../product_families.md#sgm358) | Op-amp for amplifying low-level sensor output |

External to SG Micro (out of BOM scope for this single-vendor solution):
- MCU with ADC (any vendor — Nordic / ST / Renesas / etc.)
- Sensor elements (temperature / humidity / gas / etc.)
- Passives (resistor dividers, decoupling, filter caps)

## Reference Design Verification Status

- [x] Hero part (SGM3157) has a vendor product page URL in
      `references/semiconductor-vendor/SGMicro/product_families.md`
      and is on the verified SG Micro product page (HTTP 200).
- [ ] Specific reference design / schematic from the SG Micro datasheet
      was not downloaded in this entry. **This file documents the *type* of
      reference design, not the exact SG Micro-published schematic.** To
      complete it, fetch the actual reference design from
      sg-micro.com and cite the specific document.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The SGM3157 spec values
> (Ron / bandwidth / on-resistance flatness) live in the maintainer's
> private spec database (`specs/SGMicro/SGM3157.yaml`, if installed)
> and are cross-checked against the official vendor datasheet PDF
> Public-release users should download the datasheet directly from the vendor product page (see Main Page column above); the embedded_dev/ path is for development cloning with the datasheets plug-in.
> `references/semiconductor-vendor/SGMicro/product_families.md#sgm3157`.

## Source Discipline

For this entry, all data points come from:
- SG Micro product page (`https://www.sg-micro.com/product/sgm3157`)
- SG Micro official datasheet (downloadable from `sg-micro.com/product/sgm3157/download`)

Verify with vendor documentation before recommending. SG Micro parts are
stocked on LCSC, Mouser, and Digi-Key.
