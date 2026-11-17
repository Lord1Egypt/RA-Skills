# nRF54L15 Wearable Demo (Nordic nRF54L Series)

> **Vendor:** Nordic Semiconductor
> **Part:** nRF54L15
> **Source:** Nordic nRF54L15 product page + nRF Connect SDK documentation
> **Family context:** nRF54L Series — 4th-gen ultra-low-power wireless SoC

## Overview

The **nRF54L15** is Nordic's flagship ultra-low-power BLE SoC for
wearable and IoT applications. It integrates:

- **Arm Cortex-M33** application core @ 128 MHz (DSP, FPU)
- **RISC-V coprocessor** @ 128 MHz for SoftPeripherals
- **1.5 MB NVM + 256 KB RAM** (largest in the nRF54L family)
- **22nm process node** — best-in-class power efficiency
- **Multiprotocol radio**: BLE 5.4 + Matter + Thread + Zigbee + Channel Sounding
- **Performance**: 503 CoreMark @ 193 CoreMark/mA (3V)

This single-SoC approach + Nordic's nPM1300 PMIC = lowest-power wearable
reference design in the industry.

## Reference design topology

```
   ┌──────────────────┐
   │   Sensor Hub      │
   │  (PPG / IMU / T) │
   └────────▲─────────┘
            │ I2C / SPI
   ┌────────┴─────────┐    ┌──────────────┐
   │  nRF54L15 SoC    │────│   nPM1300    │
   │ (M33 + RISC-V)   │    │   (PMIC)     │
   └────────▲─────────┘    └──────────────┘
            │ BLE 5.4
   ┌────────┴─────────┐
   │  Battery (Li-Po) │
   └──────────────────┘
```

## Key features (from nRF54L15 family page)

- **Performance**: 503 CoreMark @ 193 CoreMark/mA
- **Memory**: 1.5 MB NVM + 256 KB RAM
- **Wireless**: BLE 5.4 + Matter + Thread + Zigbee + Channel Sounding + Mesh
- **Radio**: 3.4 mA RX, 4.8 mA TX @ 0 dBm; +8 dBm max TX (CSP)
- **Sensitivity**: -96 dBm (BLE 1M), -101 dBm (802.15.4)
- **Sleep**: 0.7-2.9 µA sleep current
- **Companion**: nRF7002 Wi-Fi 6 (adds Wi-Fi)
- **Tools**: nRF Connect SDK + VS Code extension

## BOM candidates (Nordic-centric)

| Function | Part | Notes |
|----------|------|-------|
| BLE SoC | **nRF54L15** | Main chip (QFN48 6×6 or WLCSP) |
| PMIC | nPM1300 | Nordic's companion PMIC, designed for nRF54L |
| Battery charger | nPM1300 integrates | Hardware fuel gauge + charger |
| Battery | 100-300 mAh Li-Po | With NTC |
| Display (optional) | OLED or e-ink | SPI/I2C, off-catalog |
| PPG sensor | AFE44xx or MAX30102 | Off-catalog |

## Selection criteria — when to choose nRF54L15

✅ Choose nRF54L15 when:
- Need best-in-class power efficiency (fitness tracker / wearable)
- Want Matter / Thread / Zigbee future-proofing
- Need large memory (1.5 MB NVM) for OTA updates + application code
- Will pair with nPM1300 PMIC

❌ Avoid nRF54L15 when:
- Cost-down (< $10 BOM) — use nRF52832 or DA14531
- Need Wi-Fi — add nRF7002 companion (or use nRF7002 + nRF54H20)
- Need cellular — use nRF9160 SiP instead

## Verification status

- nRF54L15 product page: ✅ verified via nordicsemi.com URL (HTTP 200)
- Specs in `specs/Nordic/nRF54L15.yaml` (505 CoreMark, 256 KB RAM, BLE 6.0)
- Raw + clean snapshots at
  `references/semiconductor-vendor/Nordic/firecrawl-snapshots/nRF54L15_*.md`

## Source documents

- Datasheet: product page → Documents & Downloads
- Nordic product page: https://www.nordicsemi.com/Products/nRF54L15
- nRF Connect SDK: https://www.nordicsemi.com/Products/Development-software/nrf-connect-sdk
- nPM1300 PMIC: https://www.nordicsemi.com/Products/nPM1300