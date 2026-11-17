# Smart Watch (multi-vendor observed)

> **Source class:** Third-party teardowns, OEM reference designs, and
> vendor application notes. BOMs here are vendor-neutral; they reflect
> what is commonly observed in shipped products or what multi-vendor
> reference designs recommend. For single-vendor reference designs
> (e.g. Renesas DA1470x, ST STM32WB55 + ST evaluation kit), see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A modern multi-function smart watch for health/fitness tracking and
notifications. Generic, vendor-neutral requirements:

- **Battery life**: target > 5 days typical use on a small Li-Po (~300 mAh).
- **Always-on display**: AMOLED + low-power mode.
- **Wireless**: BLE 5.x mandatory + Wi-Fi (optional) for sync.
- **Sensors**: PPG (heart rate / SpO2), IMU (gesture / step), temp (optional).
- **Touch**: capacitive touch + haptic feedback.
- **Payment**: NFC (optional, for Google Pay / Apple Pay equivalents).
- **Wireless charging**: Qi or proprietary (optional).

Constraints:
- Battery powered, charge-daily-to-weekly.
- IP68 water resistance.
- Cost-sensitive BOM (< $50 total).

## BOM Candidates (multi-vendor, third-party observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| BLE SoC | **DA1470x** | Renesas | Multi-core BLE 5.2 + PMU + GPU; popular in smart-watch DK designs targeting rich UI + low power. | [link](../../semiconductor-vendor/Renesas/product_families.md#da1470x) |
| BLE SoC | **nRF5340** | Nordic | Dual-core BLE 5 / Thread / Matter; network + app processor split. | [link](../../semiconductor-vendor/Nordic/product_families.md#nrf5340) |
| BLE SoC | **STM32WB55** | ST | Dual-core M4+M0+, BLE 5 / 802.15.4. | [link](../../semiconductor-vendor/ST/product_families.md#stm32wb55) |
| BLE SoC | **CC2640R2F** | TI | Mature BLE 5.1 SoC, well-documented low-power reference designs. | [link](../../semiconductor-vendor/TI/product_families.md#cc2640r2f) |
| Wi-Fi+BLE combo | **ESP32-S3** | Espressif | If Wi-Fi is required for sync; dual-core Xtensa LX7. | [link](../../semiconductor-vendor/Espressif/product_families.md#esp32-s3) |
| Battery charger | **ISL9238** | Renesas | Buck-boost battery charger for 1-4 cell Li-ion. | [link](../../semiconductor-vendor/Renesas/product_families.md#isl9238) |
| Humidity / temp sensor (optional) | **HS3001** | Renesas | Optional environmental sensor. Note: marked Obsolete on Renesas product page — verify status before new design. | [link](../../semiconductor-vendor/Renesas/product_families.md#hs3001) |
| NFC wireless charging | **PTX130W + PTX30W** | Renesas (Panthronics) | NFC Forum WLC 2.1 spec for sub-1W wireless charging (no Qi coil needed). | [link](../../semiconductor-vendor/Renesas/product_families.md#ptx130w) |

External (not catalogued in this skill):
- PPG / heart-rate sensor — typical options: AFE44xx (TI), MAX30102 (Maxim/Analog Devices)
- IMU (6-axis) — typical options: LSM6DSO (ST), BMI270 (Bosch)
- AMOLED display controller — typically procured display + driver bundled

## Selection matrix

For design decisions, see each vendor's product_families.md for the
full part list. Top 3 candidates by typical smart-watch requirements:

1. **Renesas DA1470x** — best integrated PMU + GPU + BLE in single SoC;
   lowest BOM for non-Wi-Fi designs.
2. **Nordic nRF5340** — best BLE 5 + Thread/Matter future-proofing;
   network/app core split is clean.
3. **ST STM32WB55** — well-supported by STM32 ecosystem; broad middleware.

For designs that need Wi-Fi sync, swap to **ESP32-S3** (single SoC
handles Wi-Fi + BLE; loses Thread/Matter future-proofing).

## Verification status

- BLE SoC candidates: linked to product_families.md entries with verified
  URLs (see each vendor's 2026-06-29 firecrawl pass for confirmation).
- Battery charger / sensor / NFC parts: linked to Renesas product_families.md.
- External parts (PPG, IMU, display): not catalogued in this skill —
  consult vendor selection guides separately.