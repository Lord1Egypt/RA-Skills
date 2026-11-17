# Smart Ring (Third-party teardowns / cross-vendor)

> **Source class:** Third-party teardowns, online component marketplaces,
> and engineer community schematics. The BOMs here are not endorsed by any
> single chip vendor — they reflect what has actually been observed in
> shipped products or what is being sold as a turnkey reference design by
> a third party. For a single-vendor reference design (e.g. Renesas' own
> DA1470x smart-ring reference), see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A wearable smart ring for health/fitness tracking and contactless payment,
as commonly observed in third-party teardowns and as offered by
multi-vendor reference designs. Generic, vendor-neutral requirements:

- **Ultra-low power**: target > 7 days battery life on a small Li-Po or coin cell.
- **Small form factor**: < 50 mg weight, < 10 mm width, single-sided flex PCB.
- **Wireless**: BLE 5.x mandatory (for phone pairing + payments).
- **Sensors**: at minimum PPG (heart rate / SpO2) and IMU (gesture / activity).
- **Secure element**: optional, for payment (NFC + secure element path).

Constraints:
- Battery powered (≤ 100 mAh typical).
- IP rating: IP67/IP68 desired.
- Cost-sensitive BOM (< $20 total).

## BOM Candidates (multi-vendor, third-party observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| BLE SoC | **DA1470x** | Renesas | Multi-core BLE 5.2 + PMU + GPU; popular choice in design articles and DK designs targeting ring form factors. | [link](../../semiconductor-vendor/Renesas/product_families.md#da1470x) |
| BLE SoC | **nRF54L15** | Nordic | Ultra-low-power Cortex-M33; often shown in Nordic SDK wearable demos. | [link](../../semiconductor-vendor/Nordic/product_families.md#nrf54l15) |
| BLE SoC | **STM32WB55** | ST | Dual-core M4+M0+, BLE 5 / 802.15.4 — appears in ST community projects. | [link](../../semiconductor-vendor/ST/product_families.md#stm32wb55) |
| BLE SoC | **CC2640R2F** | TI | Mature BLE 5.1 SoC, well-documented low-power reference designs. | [link](../../semiconductor-vendor/TI/product_families.md#cc2640r2f) |
| Battery charger | **ISL9205** | Renesas | Single-cell Li-ion linear charger family, small DFN-10/QFN-16 package. | [link](../../semiconductor-vendor/Renesas/product_families.md#isl9205) |
| Humidity / temp sensor (optional) | **HS3001** | Renesas | Optional environmental sensor. Note: marked Obsolete on Renesas product page — verify status before new design. | [link](../../semiconductor-vendor/Renesas/product_families.md#hs3001) |

External (not catalogued in this skill):
- PPG / heart-rate sensor — typical options: AFE44xx (TI), MAX30102 (Maxim/Analog Devices)
- IMU (6-axis) — typical options: LSM6DSO (ST), BMI270 (Bosch)
- For payment variants: NFC controller + secure element — typical options: NXP SN100T, ST ST25

## Third-party Sources (to be expanded as data is collected)

- (pending) Teardown reports of Oura Ring, Ultrahuman Ring, RingConn — these
  are the canonical references for ring form-factor constraints, even though
  the exact part numbers are not always disclosed.
- (pending) Component-marketplace listings for "smart ring reference design"
  on LCSC, Mouser, Digi-Key Marketplace, etc.
- (pending) Engineer community posts on EEVblog, hackaday.io, element14.

## Reference Designs

> This section lists **single-vendor** reference designs from chip
> vendors' own websites, included here for completeness. For the full
> single-vendor version of a given solution, see
> `references/semiconductor-vendor/<Vendor>/system-solutions/`.

- Renesas DA1470x product page: https://www.renesas.com/da1470x (✅ verified)
- Nordic nRF54L15 product page: https://www.nordicsemi.com/Products/nRF54L15 (✅ verified 2026-06-21)
- ST STM32WB55 product page: https://www.st.com/en/microcontrollers-microprocessors/stm32wb55.html (⏳ verification pending)
- TI CC2640R2F product page: https://www.ti.com/product/CC2640R2F (⏳ verification pending)

## Selection Matrix (third-party / community perspective)

| Criterion | DA1470x (Renesas) | nRF54L15 (Nordic) | STM32WB55 (ST) | CC2640R2F (TI) |
|-----------|-------------------|-------------------|----------------|-----------------|
| BLE version | 5.2 | **6.0** (nRF54L, 2024 release) | 5.x | 5.1 |
| Cores | not extracted | Arm Cortex-M33 @ 128 MHz with TrustZone | not extracted | Cortex-M3 @ 48 MHz |
| Flash / RAM | not extracted | 1.5 MB (NVM) / 256 KB | not extracted | 275 KB / 28 KB |
| Supply voltage | not extracted | 1.7 to 3.6 V | not extracted | 1.8 to 3.8 V |
| Integrated PMU | ✅ | ❌ | ❌ | ❌ |
| Multi-core (app + radio) | ✅ | ❌ (single core) | ✅ | ❌ (single core) |
| CoreMark | not extracted | 505 | not extracted | not extracted |
| RX sensitivity | not extracted | -96 dBm (1 Mbps BLE) | not extracted | not extracted |
| Standby current | not extracted | not extracted | not extracted | 1.1 µA |
| Shutdown current | not extracted | not extracted | not extracted | 100 nA |
| Vendor maturity for wearables | High | High | Medium | High |

> **Numerical specs** are sourced from the maintainer's private spec
> database (`specs/<Vendor>/<Part>.yaml`, populated by
> `scripts/update_specs.py`) and cross-checked against official vendor
> datasheets fetched at runtime from the URLs in
> `references/semiconductor-vendor/<Vendor>/product_families.md`. Cells
> marked "not extracted" mean the corresponding datasheet value has not
> yet been confirmed against the official vendor document. DA1470x /
> STM32WB55 still need manual datasheet verification by the user before
> recommending (DA1470x is a Renesas-internal PDF; STM32WB55 PDF is
> Cloudflare-gated from st.com).

## Verification Status

- [x] All BOM parts have a vendor product page URL in
      `references/semiconductor-vendor/<Vendor>/product_families.md`
      or are noted as "external" (out of skill scope).
- [x] **nRF54L15**: 7 spec fields populated (cores / flash / ram /
      ble_version / coremark / rx_sensitivity / vcc).
- [x] **CC2640R2F**: 8 spec fields populated (cores / flash / ram /
      ble_version / supply_voltage / active_rx_ma / standby_ua /
      shutdown_na / wireless).
- [x] **DA1470x** (✅ human-verified 2026-06-25): 41 spec fields
      populated including cores (Cortex-M33 + Cortex-M0+ sensor node
      controller), 1.5 MB SRAM, external SPI flash, GPU, hibernation
      current 0.4 µA, deep sleep 16.9 µA, VAD sleep 25.9 µA, supply
      range 2.9-4.75 V (VBAT), -40 to 85 °C operating temp, VFBGA142
      6.2x6 mm package. DA1470x is the only BLE SoC in this family
      with integrated 2D GPU and display controller.
- [ ] **STM32WB55**: spec YAML exists but is empty. ST datasheet is
      Cloudflare-gated from st.com; Mouser mirror
      (`stm32wb55cc-1588841.pdf`) added 2026-06-25, ready to download
      + extract on next update_specs run.
- [ ] At least one actual third-party source URL must be added to the
      "Third-party Sources" section before this solution is considered
      non-placeholder.
- [ ] Compare published sleep current vs target 7-day battery life.
- [ ] Confirm package sizes fit < 10 mm PCB width.

## Caveat

This file is a **framework for collecting multi-vendor smart-ring BOMs** as
observed in real-world designs. It does not yet contain any teardown
evidence. The list of "Why this part appears" columns is the seed for
adding source citations, not a vendor endorsement.

For the **single-vendor** version of a smart-ring reference design, see
`references/semiconductor-vendor/Renesas/system-solutions/` (Renesas'
own DA1470x-based ring demo) or the equivalent under the other vendors.

Re-run `scripts/build_application_index.py` after populating YAMLs to
refresh INDEX.md.
