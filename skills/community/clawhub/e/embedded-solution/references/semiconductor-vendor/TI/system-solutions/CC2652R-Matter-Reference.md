# CC2652R Matter Reference

> **Source:** TI-published SimpleLink SDK Matter reference design
> for the CC2652R multiprotocol wireless MCU. BOM is **TI-only**
> (single-vendor).

## Overview
A TI-published reference design demonstrating Matter-over-Thread
device commissioning, Cluster / Attribute server design, and
multi-protocol coexistence on the CC2652R SoC.

- **Vendor:** Texas Instruments
- **Published as:** SimpleLink CC13x2 / CC26x2 SDK Matter examples
- **Document type:** Reference design (pro-forma Matter node + ICD support)
- **EVK:** LAUNCHXL-CC26X2R1
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.ti.com/tool/LAUNCHXL-CC26X2R1 (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/TI/CC2652R.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/TI/product_families.md` and the datasheet)*

## BOM Candidates (TI only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Multiprotocol 2.4-GHz wireless MCU | **CC2652R** | [link](../product_families.md) | Cortex-M4F, Thread / Zigbee / BLE 5 / Matter |
| EVK platform | **LAUNCHXL-CC26X2R1** | TI product page | On-board XDS110 debug probe, BoosterPack headers |

External to TI (out of BOM scope for this single-vendor solution):
- USB cable, host PC, Thread border router for testing

## Reference Design Verification Status

- [ ] Original TI product page URL HTTP 200 — verification pending.
- [ ] CC2652R datasheet not yet downloaded.
- [ ] Confirm which Matter SDK release is being cited — Matter
      evolved rapidly; pin a specific tag.
- [ ] Confirm ICD (Intermittently Connected Device) support is
      enabled in the cited example if that's a selling point.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The CC2652R spec values
> live in the maintainer's private spec database (`specs/TI/CC2652R.yaml`, if installed). Datasheet PDF not yet
> downloaded.

## Source Discipline

- Original reference design published by TI on ti.com.
- This entry only references TI parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
