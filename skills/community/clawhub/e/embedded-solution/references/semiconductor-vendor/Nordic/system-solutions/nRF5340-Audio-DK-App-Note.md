# nRF5340 Audio DK Application Note

> **Source:** Nordic Semiconductor-published application note for the
> nRF5340 dual-core SoC, demonstrated on the nRF5340 Audio DK. BOM is
> **Nordic-only** (single-vendor). For multi-vendor teardown-derived
> solutions see `references/application-solution/`.

## Overview
A Nordic-published application note walking through low-power
Bluetooth LE Audio / LC3 broadcast / Auracast™ sink role on the
nRF5340's application core (Cortex-M33), with the network / radio
core (Cortex-M0+) running the BLE controller.

- **Vendor:** Nordic Semiconductor
- **Published as:** nRF Connect SDK application note +
  `samples/bluetooth/auracast/` examples
- **Document type:** Eval kit application note (LE Audio bring-up)
- **EVK:** nRF5340 Audio DK (PCA10095)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.nordicsemi.com/Products/Development-hardware/nRF5340-Audio-DK (verification pending; Cloudflare-class risk noted)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Nordic/nRF5340.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Nordic/product_families.md` and the datasheet)*

## BOM Candidates (Nordic only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Dual-core wireless SoC | **nRF5340** | [link](../product_families.md#nrf5340) | Cortex-M33 app + Cortex-M0+ net core, BLE 5.x |
| EVK platform | **nRF5340 Audio DK (PCA10095)** | Nordic product page | On-board DSP, headphone amps, USB, headphone jacks |

External to Nordic (out of BOM scope for this single-vendor solution):
- USB cable, headphones / speakers, host PC with nRF Connect for Desktop

## Reference Design Verification Status

- [ ] Original Nordic product page URL HTTP 200 — verification pending.
      Cloudflare-protected; same indirect-link risk as the nRF52 DK
      entry.
- [x] Datasheet already present at
      product page → Documents & Downloads.
- [ ] Pin the exact SDK example path (`samples/bluetooth/auracast/`
      vs the legacy `samples/bluetooth/le_audio_*` paths — Nordic
      renamed the example during 2024 SDK releases).
- [ ] Confirm whether the application note covers **broadcast
      receiver** (sink) or **broadcast transmitter** (source) or both.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The nRF5340 spec values
> live in the maintainer's private spec database (`specs/Nordic/nRF5340.yaml`, if installed) and are cited to the datasheet
> PDF under product page → Documents & Downloads.
> See that YAML for verified values.

## Source Discipline

- Original application note published by Nordic on nordicsemi.com /
  in the nRF Connect SDK.
- This entry only references Nordic parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
