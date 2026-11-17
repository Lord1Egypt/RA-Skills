# nRF54L15 Power-Profile Sample

> **Source:** Nordic Semiconductor-published nRF Connect SDK power-
> profiling sample for the nRF54L15 ultra-low-power wireless SoC.
> BOM is **Nordic-only** (single-vendor).

## Overview
A Nordic-published SDK example demonstrating the nRF54L15's Global
RTC wake architecture, MRAM power-mode transitions, and current
profile measurements (sub-µA standby). Targets battery-powered
sensor / beacon nodes.

- **Vendor:** Nordic Semiconductor
- **Published as:** nRF Connect SDK power-profiler samples
- **Document type:** SDK example (power-profile measurement)
- **EVK:** nRF54L15 DK (PCA10156)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.nordicsemi.com/Products/Development-hardware/nRF54L15-DK (verification pending)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Nordic/nRF54L15.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Nordic/product_families.md` and the datasheet)*

## BOM Candidates (Nordic only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Ultra-low-power wireless SoC | **nRF54L15** | [link](../product_families.md#nrf54l15) | Cortex-M33, MRAM, Global RTC for sub-µA standby |
| EVK platform | **nRF54L15 DK (PCA10156)** | Nordic product page | On-board Power Profiler Kit II headers, debug |

External to Nordic (out of BOM scope for this single-vendor solution):
- USB cable, Power Profiler Kit II (PPK2), host PC with nRF Connect
  for Desktop

## Reference Design Verification Status

- [ ] Original Nordic product page URL HTTP 200 — verification pending.
- [x] Datasheet already present at
      product page → Documents & Downloads.
- [ ] nRF54L15 is a recent (2024-2025 era) part; verify the SDK
      release tag matches the cited sample path.
- [ ] Distinguish **datasheet typical** vs **measured on the DK**
      power numbers — Nordic's app note publishes both. For
      certification work, cite the datasheet, not the SDK readout.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The nRF54L15 spec values
> live in the maintainer's private spec database (`specs/Nordic/nRF54L15.yaml`, if installed) and are cited to the datasheet
> PDF under product page → Documents & Downloads.
> See that YAML for verified values.

## Source Discipline

- Original example published by Nordic in nRF Connect SDK.
- This entry only references Nordic parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
