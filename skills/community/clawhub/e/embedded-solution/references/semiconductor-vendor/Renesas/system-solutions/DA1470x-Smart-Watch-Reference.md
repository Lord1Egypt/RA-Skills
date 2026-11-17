# DA1470x Smart Watch Reference (Renesas DA14xxx family)

> **Vendor:** Renesas
> **Part:** DA1470x
> **Source:** Renesas DA1470x product page + DA1470x SmartBond™ SDK documentation
> **Family context:** SmartBond™ DA14xxx BLE SoC family

## Overview

The **DA1470x** is Renesas' high-end SmartBond™ BLE SoC designed for
always-on wearable applications (smart watches, fitness bands, AR glasses).
It integrates:

- **Multi-core CPU**: Cortex-M33F application core + Cortex-M0+ radio core
- **Power Management Unit (PMU)**: integrated buck DC/DC + LDOs
- **GPU + Display controller**: supports up to 480x480 AMOLED round displays
- **Rich peripherals**: SPI/QSPI/I2C/UART/USB + 12-bit ADC + crypto accelerator
- **Memory**: up to 16 MB flash + 512 KB SRAM on-chip

This single-SoC approach eliminates the need for an external PMIC in many
wearable designs, reducing BOM cost and PCB area.

## Reference design topology

```
   ┌──────────────────┐
   │   AMOLED Display │
   └────────▲─────────┘
            │ SPI / QSPI
   ┌────────┴─────────┐    ┌──────────────┐
   │   DA1470x SoC    │────│  Sensor Hub  │
   │  (M33 + M0+)     │    │ (PPG/IMU/T)  │
   └────────▲─────────┘    └──────────────┘
            │ I2C / SPI
   ┌────────┴─────────┐
   │  Battery (Li-Po) │
   └──────────────────┘
            ▲
            │ (integrated PMU)
            │
   ┌────────┴─────────┐
   │   DA1470x PMIC   │
   │  (internal LDO)  │
   └──────────────────┘
```

## Key features (from DA1470x family page)

- **BLE 5.2**: full feature set incl. LE Audio, direction finding
- **Display**: integrated GPU supports up to 480×480 AMOLED round
- **PMU**: integrated buck DC/DC + multiple LDOs (no external PMIC needed)
- **Audio**: PDM + I2S interfaces for digital microphones / speaker amps
- **Touch**: integrated capacitive touch controller
- **Security**: Secure boot, hardware crypto (AES-256, SHA-256, TRNG)

## BOM candidates (Renesas-centric)

| Function | Part | Notes |
|----------|------|-------|
| BLE SoC + PMIC | **DA1470x** | Single chip — replaces SoC + external PMIC |
| Display | AMOLED 1.43" 466×466 round | Raystar, BOE, or similar |
| Battery charger | **ISL9238** | Buck-boost for 1-cell Li-ion |
| Battery | 300 mAh Li-Po | With NTC for thermal monitoring |
| PPG sensor | AFE44xx or MAX30102 | Off-catalog; see Renesas sensor partner list |
| IMU | LSM6DSO or BMI270 | Off-catalog |
| Wireless charging (optional) | **PTX130W** + **PTX30W** pair | NFC Forum WLC 2.1 (see PTX130W.yaml) |

## Selection criteria — when to choose DA1470x

✅ Choose DA1470x when:
- Need a single-SoC BLE + PMIC + display controller solution
- Target BOM < $30 (excluding display + sensors)
- Want integrated GPU for rich watch faces

❌ Avoid DA1470x when:
- Need Wi-Fi sync (no integrated Wi-Fi — add ESP32-S3 or external)
- Need Thread / Matter (BLE-only, no 802.15.4)
- Need cost-down to < $15 BOM (use DA14531 instead)

## Verification status

- DA1470x family page: ✅ verified via Renesas product URL (HTTP 200)
- Specs in `specs/Renesas/DA1470x.yaml` (datasheet-extracted fields)
- BOM candidates above cross-referenced to Renesas product_families.md

## Source documents

- Datasheet: product page → Documents & Downloads
- Renesas product page: https://www.renesas.com/da1470x
- DA1470x SmartBond SDK: https://www.renesas.com/products/da1470x
- PMIC integration note: see Renesas application note library