# ISL9238 NVDC Charger Reference

> **Source:** Renesas-published reference design for the ISL9238
> buck + boost Narrow-VDC charger controller with SMBus / I²C
> configuration. BOM is **Renesas-only** (single-vendor).

## Overview
A Renesas-published reference design for a USB-C PD / Narrow-VDC
battery charger using the ISL9238 controller. Includes schematic
blocks for adapter detection, system rail regulation, and SMBus
programming.

- **Vendor:** Renesas Electronics
- **Published as:** ISL9238 datasheet + reference design note
- **Document type:** Reference design (pro-forma schematic + BOM)
- **EVK:** ISL9238 evaluation board (ISL9238EVAL1Z or successor)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.renesas.com/en/products/power-management/battery-management/battery-charger-ics/isl9238 (verification pending)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Renesas/ISL9238.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Renesas/product_families.md` and the datasheet)*

## BOM Candidates (Renesas only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Buck + boost NVDC charger controller | **ISL9238** | [link](../product_families.md#isl9238) | USB-C PD + legacy adapter detection, SMBus / I²C |
| Companion USB-C PD controller (Renesas) | **R9A02G011** or **RAJ240090** (variant-dependent) | [link](../product_families.md) | Renesas USB-PD controller — pin exact part against the cited ISL9238 design note |

External to Renesas (out of BOM scope for this single-vendor solution):
- USB-C cable, host PC, MOSFETs / passives (Renesas design notes
  suggest specific Renesas MOSFETs where applicable — extend the
  BOM to those if used)

## Reference Design Verification Status

- [ ] Original Renesas product page URL HTTP 200 — verification pending.
- [x] Datasheet already present at
      product page → Documents & Downloads.
- [ ] Confirm ISL9238 variant (A / B / C) cited — each variant adds
      features and changes pinout in subtle ways.
- [ ] Confirm exact companion USB-PD controller — the ISL9238 design
      notes pair with several Renesas PD controllers; the BOM must
      pick one and not switch silently.
- [ ] Mark whether the design supports **NVDC** (narrow-VDC) or
      **HPBB** (hybrid power buck boost) topology — the ISL9238
      family supports both via firmware.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The ISL9238 spec values
> live in the maintainer's private spec database (`specs/Renesas/ISL9238.yaml`, if installed) and are cited to the datasheet
> PDF under product page → Documents & Downloads.
> See that YAML for verified values.

## Source Discipline

- Original reference design published by Renesas on renesas.com.
- This entry only references Renesas parts (single-vendor rule).
  Passives and connectors are **out of scope** for this BOM and
  belong in the full schematic, not the system-solution table.
- For multi-vendor teardowns, see `references/application-solution/`.
