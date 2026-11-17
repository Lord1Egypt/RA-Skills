# STM32MP1 Linux Distribution

> **Source:** ST-published OpenSTLinux distribution and reference
> image for the STM32MP157 Cortex-A7 + Cortex-M4 heterogeneous MPU.
> BOM is **ST-only** (single-vendor).

## Overview
An ST-published reference image demonstrating the Cortex-A7 Linux
boot flow (TF-A, U-Boot, kernel, rootfs), Cortex-M4 firmware
co-processor patterns, and the OpenSTLinux ecosystem tooling.

- **Vendor:** STMicroelectronics
- **Published as:** OpenSTLinux distribution + STM32CubeMP1 package
- **Document type:** Reference design (pro-forma BSP / image recipe)
- **EVK:** STM32MP157F-DK2
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.st.com/en/evaluation-tools/stm32mp157f-dk2.html (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/ST/STM32MP157.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/ST/product_families.md` and the datasheet)*

## BOM Candidates (ST only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Heterogeneous Cortex-A7 + Cortex-M4 MPU | **STM32MP157** | [link](../product_families.md) | Multiple SKUs (MP157A / MP157C / MP157F) — cite SKU |
| EVK platform | **STM32MP157F-DK2** | ST product page | Display + touch, multiple connectivity options |

External to ST (out of BOM scope for this single-vendor solution):
- USB cable, Ethernet cable, microSD card, host PC

## Reference Design Verification Status

- [ ] Original ST product page URL HTTP 200 — verification pending.
- [ ] STM32MP157 datasheet not yet downloaded.
- [ ] Pin down exact STM32MP157 SKU (F = crypto / secure boot;
      A = non-secure; C = mid-tier). Reference design should pick one.
- [ ] Confirm OpenSTLinux release tag matches the cited SDK version.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The STM32MP157 spec values
> live in the maintainer's private spec database (`specs/ST/STM32MP157.yaml`, if installed). Datasheet PDF not yet
> downloaded.

## Source Discipline

- Original reference design published by ST on st.com.
- This entry only references ST parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
