# nRF9160 Asset Tracker Reference

> **Source:** Nordic Semiconductor-published nRF Connect SDK / nRF
> Cloud location-services asset tracker reference design for the
> nRF9160 SiP (LTE-M / NB-IoT + GNSS). BOM is **Nordic-only**
> (single-vendor).

## Overview
A Nordic-published reference design for a battery-powered cellular
asset tracker, demonstrating LTE-M attach, GNSS acquisition,
nRF Cloud location-services integration, and power-profile
sizing for multi-week battery life.

- **Vendor:** Nordic Semiconductor
- **Published as:** nRF Connect SDK
  `samples/nrf9160/location_tracker` + nRF Cloud documentation
- **Document type:** Reference design (pro-forma bring-up + power
  budget)
- **EVK:** nRF9160 DK (PCA10090)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.nordicsemi.com/Products/Development-hardware/nRF9160-DK (verification pending)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Nordic/nRF9160.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Nordic/product_families.md` and the datasheet)*

## BOM Candidates (Nordic only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cellular IoT SiP (LTE-M / NB-IoT + GNSS) | **nRF9160** | [link](../product_families.md#nrf9160) | Integrated modem, Cortex-M33 app core |
| EVK platform | **nRF9160 DK (PCA10090)** | Nordic product page | On-board SIM slot, GNSS antenna, sensors |

External to Nordic (out of BOM scope for this single-vendor solution):
- USB cable, Li-Po battery, host PC with nRF Connect for Desktop

## Reference Design Verification Status

- [ ] Original Nordic product page URL HTTP 200 — verification pending.
- [x] Datasheet already present at
      product page → Documents & Downloads.
- [ ] Confirm LTE-M / NB-IoT band lock — band classes differ by
      region (Cat-M1 in US/EU, NB-IoT with specific band masks in
      APAC). The reference design should pin one band class.
- [ ] Confirm whether nRF Cloud location services or on-device
      GNSS-only is the cited configuration — they give very
      different battery-life numbers.
- [ ] nRF9160 variants (regular vs **nRF9161**) have different
      modem firmware features. Pin the exact SKU.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The nRF9160 spec values
> live in the maintainer's private spec database (`specs/Nordic/nRF9160.yaml`, if installed) and are cited to the datasheet
> PDF under product page → Documents & Downloads.
> See that YAML for verified values.

## Source Discipline

- Original reference design published by Nordic on nordicsemi.com /
  in nRF Connect SDK.
- This entry only references Nordic parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
