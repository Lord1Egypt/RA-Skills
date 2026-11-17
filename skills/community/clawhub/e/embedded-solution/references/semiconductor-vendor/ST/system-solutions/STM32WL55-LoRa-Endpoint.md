# STM32WL55 LoRa Endpoint

> **Source:** ST-published STM32CubeWL LoRaWAN endpoint example
> running on the NUCLEO-WL55JC1 / NUCLEO-WL55JC2 evaluation boards.
> BOM is **ST-only** (single-vendor).

## Overview
An ST-published LoRaWAN Class A / Class C endpoint example on the
STM32WL55 sub-GHz wireless MCU, including LoRaWAN stack bring-up,
regional band configuration, and OTA activation.

- **Vendor:** STMicroelectronics
- **Published as:** STM32CubeWL package example
  `Projects/NUCLEO-WL55JC1/Applications/LoRaWAN/LoRaWAN_End_Node`
- **Document type:** SDK example (source code + readme)
- **EVK:** NUCLEO-WL55JC1 (high-frequency band) or NUCLEO-WL55JC2
  (low-frequency band)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.st.com/en/evaluation-tools/nucleo-wl55jc1.html (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/ST/STM32WL55.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/ST/product_families.md` and the datasheet)*

## BOM Candidates (ST only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Sub-GHz LoRa SoC | **STM32WL55** | [link](../product_families.md) | Cortex-M4 + integrated sub-GHz radio, multi-modem (LoRa / (G)FSK / BPSK) |
| EVK platform | **NUCLEO-WL55JC1** | ST product page | On-board ST-LINK, Arduino headers, SMA antenna |

External to ST (out of BOM scope for this single-vendor solution):
- USB cable, SMA antenna, host PC, LoRaWAN gateway for testing

## Reference Design Verification Status

- [ ] Original ST product page URL HTTP 200 — verification pending.
- [ ] STM32WL55 datasheet not yet downloaded.
- [ ] Confirm whether to cite NUCLEO-WL55JC1 (high band, 868/915 MHz
      range) or NUCLEO-WL55JC2 (low band, 433/470 MHz range) — they
      are **not** interchangeable. Pick the one matching the YAML.
- [ ] Confirm the LoRaWAN stack version (LoRaMac-node fork in
      STM32CubeWL) — ST updates this independently.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The STM32WL55 spec values
> live in the maintainer's private spec database (`specs/ST/STM32WL55.yaml`, if installed). Datasheet PDF not yet
> downloaded.

## Source Discipline

- Original example published by ST on st.com / in ST GitHub repos.
- This entry only references ST parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
