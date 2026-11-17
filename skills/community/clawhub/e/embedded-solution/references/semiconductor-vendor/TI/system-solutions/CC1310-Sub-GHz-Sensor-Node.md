# CC1310 Sub-GHz Sensor Node

> **Source:** TI-published reference design for the CC1310 sub-GHz
> wireless MCU, targeting long-range / low-power sensor nodes
> (Sub-1 GHz proprietary or Wireless M-Bus). BOM is **TI-only**
> (single-vendor).

## Overview
A TI-published reference design demonstrating sub-GHz sensor-node
deployment on the CC1310 Cortex-M3 wireless MCU, including wake-on-
radio, security, and a battery-profile current budget.

- **Vendor:** Texas Instruments
- **Published as:** SimpleLink CC13x0 SDK examples
- **Document type:** Reference design (pro-forma bring-up + RF settings)
- **EVK:** LAUNCHXL-CC1310 (or LAUNCHXL-CC1312R1 for the refreshed line)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.ti.com/tool/LAUNCHXL-CC1310 (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/TI/CC1310.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/TI/product_families.md` and the datasheet)*

## BOM Candidates (TI only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Sub-1 GHz wireless MCU | **CC1310** | [link](../product_families.md) | Cortex-M3, integrated sub-GHz radio, low-power sensor controller |
| EVK platform | **LAUNCHXL-CC1310** | TI product page | On-board XDS110, SMA antenna, BoosterPack headers |

External to TI (out of BOM scope for this single-vendor solution):
- USB cable, host PC, batteries

## Reference Design Verification Status

- [ ] Original TI product page URL HTTP 200 — verification pending.
- [ ] CC1310 datasheet not yet downloaded.
- [ ] Confirm whether to cite the original CC1310 or the refreshed
      CC1310R / CC1312R line. TI strongly prefers CC1312R1 for new
      designs; the legacy CC1310 is mature but not recommended.
- [ ] Confirm the sub-GHz band (315 / 433 / 868 / 915 MHz) matches
      the regional regulatory settings in the cited example.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The CC1310 spec values
> live in the maintainer's private spec database (`specs/TI/CC1310.yaml`, if installed). Datasheet PDF not yet downloaded.

## Source Discipline

- Original reference design published by TI on ti.com.
- This entry only references TI parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
