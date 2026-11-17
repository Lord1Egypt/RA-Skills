# KW45 Automotive BLE Reference

> **Source:** NXP-published reference design for the KW45 automotive
> BLE 5.3 MCU, targeting wireless car-access / battery-management
> telematics nodes. BOM is **NXP-only** (single-vendor).

## Overview
An NXP-published reference design demonstrating low-power BLE
advertising, secure OTA update, and CAN-FD bridging on the KW45
automotive-grade wireless MCU.

- **Vendor:** NXP Semiconductors
- **Published as:** Application Note + KW45 SDK examples
- **Document type:** Reference design (pro-forma BOM + suggested peripherals)
- **EVK:** FRDM-KW45
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.nxp.com/design/development-boards/frdm-kw45 (verification pending)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/NXP/KW45.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/NXP/product_families.md` and the datasheet)*

## BOM Candidates (NXP only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Automotive BLE 5.3 MCU | **KW45** | [link](../product_families.md) | Cortex-M33, AEC-Q100, CAN-FD + BLE |
| EVK CAN-FD transceiver (NXP) | **TJA1043** | [link](../product_families.md) | NXP Mantis family high-speed CAN-FD transceiver — verify exact part against FRDM-KW45 schematic before publication |

External to NXP (out of BOM scope for this single-vendor solution):
- USB cable, 12 V automotive supply, host PC

## Reference Design Verification Status

- [ ] Original NXP product page URL HTTP 200 — verification pending.
- [ ] KW45 datasheet not yet downloaded.
- [ ] Confirm AEC-Q100 grade (KW45 is offered in multiple grades —
      pick the one cited in the reference design).
- [x] **CAN-FD transceiver ownership resolved.** NXP's Mantis-family
      TJA1043 / TJA1057 / TJA1443 are the most likely on-board
      CAN-FD transceivers on the FRDM-KW45, all NXP-internal. BOM
      now lists **TJA1043 (NXP)** as a tentative second row; verify
      the exact part number against the published FRDM-KW45 schematic
      before publication. No multi-vendor split is needed.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The KW45 spec values live
> in `specs/NXP/KW45.yaml` (maintainer's private spec database, not shipped in public release). Datasheet PDF not yet downloaded.

## Source Discipline

- Original reference design published by NXP on nxp.com.
- This entry only references NXP parts (single-vendor rule). The FRDM-
      KW45 may carry a third-party CAN-FD transceiver on-board; if so,
      that part belongs in a multi-vendor teardown in
      `references/application-solution/`, **not** in this file.
- For multi-vendor teardowns, see `references/application-solution/`.
