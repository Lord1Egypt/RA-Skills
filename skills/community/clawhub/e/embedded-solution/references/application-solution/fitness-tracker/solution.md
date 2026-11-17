# Fitness Tracker / Health Wearable (multi-vendor observed)

> **Source class:** Third-party teardowns, OEM reference designs, and
> vendor application notes. BOMs here are vendor-neutral; they reflect
> what is commonly observed in shipped products or what multi-vendor
> reference designs recommend. For single-vendor reference designs
> (e.g. Nordic nRF54L15 + nPM1300 PMIC), see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A fitness band / tracker with heart-rate monitoring, step counting, and
phone connectivity. Generic, vendor-neutral requirements:

- **Battery life**: target > 14 days typical use on a small Li-Po (~100 mAh).
- **Wireless**: BLE 5.x mandatory for phone pairing + data sync.
- **Sensors**: PPG (heart rate / SpO2), IMU (6-axis for steps).
- **Display**: optional small OLED or e-ink.
- **Cost-sensitive BOM**: < $20 total.

Constraints:
- Battery powered, charge-daily-to-monthly.
- IP67 water resistance.
- Small form factor (single-sided flex PCB, < 30 mm width).

## BOM Candidates (multi-vendor, third-party observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| BLE SoC | **nRF54L15** | Nordic | Ultra-low-power Cortex-M33, 503 CoreMark @ 128 MHz, 1.5 MB NVM, Matter / Thread / Zigbee optional. | [link](../../semiconductor-vendor/Nordic/product_families.md#nrf54l15) |
| BLE SoC | **nRF52840** | Nordic | Mature Cortex-M4, BLE 5.4, USB, NFC. Lower-cost fallback. | [link](../../semiconductor-vendor/Nordic/product_families.md#nrf52840) |
| BLE SoC | **DA14531** | Renesas | Ultra-low-cost BLE 5.1 SoC for cost-down designs. | [link](../../semiconductor-vendor/Renesas/product_families.md#da14531) |
| BLE SoC | **CC2640R2F** | TI | Mature BLE 5.1 SoC, low-power reference designs. | [link](../../semiconductor-vendor/TI/product_families.md#cc2640r2f) |
| PMIC | nPM1300 | Nordic | Nordic's own PMIC, designed to pair with nRF54L series. | (off-catalog) |
| Battery charger | ISL9238 or BQ25895 | Renesas / TI | 1-cell Li-ion linear / buck-boost charger. | [link](../../semiconductor-vendor/Renesas/product_families.md#isl9238) |
| Humidity / temp sensor (optional) | HS3001 | Renesas | Optional environmental sensor. Note: marked Obsolete — verify status. | [link](../../semiconductor-vendor/Renesas/product_families.md#hs3001) |

External (not catalogued in this skill):
- PPG / heart-rate sensor — typical options: AFE44xx (TI), MAX30102 (Maxim/AD)
- IMU (6-axis) — typical options: LSM6DSO (ST), BMI270 (Bosch)

## Selection matrix

Top 3 BLE SoC candidates by typical fitness tracker requirements:

1. **Nordic nRF54L15** — best power efficiency (193 CoreMark/mA), most
   memory (1.5 MB NVM), Matter / Thread / Zigbee optional for future
   smart-home integration. Higher cost than nRF52840.
2. **Nordic nRF52840** — mature, lower cost, USB + NFC built-in. Safe
   default for designs that don't need Matter.
3. **TI CC2640R2F** — best low-power reference designs (SensorTag
   family), mature SDK. Cost-down choice when BLE 5.1 is sufficient.

For ultra-cost-sensitive designs (< $10 BOM), drop to **Renesas DA14531**
or even **TI CC2640** (non-R2).

## Verification status

- BLE SoC candidates: linked to product_families.md with verified URLs
  (see Nordic / Renesas / TI 2026-06-29 firecrawl passes).
- Battery charger / sensor / PMIC: linked to Renesas product_families.md.
- External parts (PPG, IMU): not catalogued — consult vendor selection guides.

## Power profile notes

For 14-day battery life target on 100 mAh Li-Po:
- Average current budget: ~300 µA (24h × 100 mAh / 14 days = 7.14 mAh/day
  = 297 µA average)
- Most current goes to: PPG sensor (~50 µA avg), BLE advertising bursts
  (~500 µA active), IMU wake-on-motion (~10 µA avg)
- Choose BLE SoC with: sleep current < 1 µA with RAM retention, fast
  wake-up, efficient radio. nRF54L15 is best-in-class; CC2640R2F also good.