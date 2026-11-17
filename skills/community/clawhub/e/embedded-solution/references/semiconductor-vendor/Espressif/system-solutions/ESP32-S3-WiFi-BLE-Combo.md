# ESP32-S3 Wi-Fi + BLE Combo Reference (Espressif ESP32 Family)

> **Vendor:** Espressif Systems
> **Part:** ESP32-S3
> **Source:** Espressif ESP32-S3 product page + ESP-IDF documentation
> **Family context:** ESP32 Series — Xtensa LX7 dual-core Wi-Fi+BLE SoC

## Overview

The **ESP32-S3** is Espressif's flagship dual-core Wi-Fi + BLE SoC for
IoT applications. It integrates:

- **Xtensa LX7 dual-core** @ up to 240 MHz
- **Wi-Fi 4** (802.11 b/g/n) + **Bluetooth 5 (LE)**
- **Vector instructions** for AI/ML acceleration (acceleration for
  quantized neural network inference)
- **Memory**: 512 KB SRAM + up to 8 MB QSPI flash + 8 MB QSPI PSRAM
- **Peripherals**: USB OTG, SPI, I2S, I2C, UART, ADC, DAC, RMT, etc.
- **Security**: Secure Boot V2, Flash Encryption, AES/SHA/RSA accelerators

This single-SoC approach + ESP-Matter + ESP RainMaker cloud = the most
widely-adopted IoT platform for makers and small-to-medium OEMs.

## Reference design topology

```
   ┌──────────────────┐    ┌──────────────┐
   │  Wi-Fi Antenna   │    │  BLE Antenna │
   └────────▲─────────┘    └──────▲───────┘
            │                      │
   ┌────────┴──────────────────────┴───────┐
   │           ESP32-S3 SoC                │
   │     (Xtensa LX7 dual-core)            │
   └────────▲─────────────────────────────┘
            │ SPI / I2C
   ┌────────┴─────────┐    ┌──────────────┐
   │  Sensor / Relay  │    │   PSRAM      │
   │  (off-catalog)   │    │  (optional)  │
   └──────────────────┘    └──────────────┘
```

## Key features (from ESP32-S3 family page)

- **CPU**: Dual-core Xtensa LX7 @ 240 MHz
- **Wireless**: Wi-Fi 4 + BLE 5 + IEEE 802.15.4 (Thread/Zigbee)
- **AI**: Vector instructions for NN inference (quantized models)
- **USB**: USB OTG 1.1
- **Memory**: 512 KB SRAM + up to 8 MB QSPI flash + 8 MB QSPI PSRAM
- **Tools**: ESP-IDF + ESP-Matter + Arduino IDE + PlatformIO

## BOM candidates (Espressif-centric)

| Function | Part | Notes |
|----------|------|-------|
| Wi-Fi+BLE SoC | **ESP32-S3-WROOM-1** | Pre-certified module with FCC ID |
| Flash | 8-16 MB QSPI | On-module or external |
| PSRAM (optional) | 8 MB QSPI | For AI / display buffer |
| Antenna | PCB trace or chip antenna | Module has integrated antenna |

## Selection criteria — when to choose ESP32-S3

✅ Choose ESP32-S3 when:
- Need Wi-Fi + BLE in single SoC
- Want mature ESP-IDF + Arduino + PlatformIO ecosystem
- Want Matter support via ESP-Matter
- Want AI/ML acceleration (vector instructions)

❌ Avoid ESP32-S3 when:
- Cost-down (< $5 BOM) — use ESP32-C3 instead
- Need Wi-Fi 6 — use ESP32-C6
- Need cellular — use a different vendor (nRF9160, etc.)

## Verification status

- ESP32-S3 product page: ✅ verified via espressif.com URL (HTTP 200)
- Specs in `specs/Espressif/ESP32-S3.yaml` (datasheet-extracted fields)

## Source documents

- Datasheet: product page → Documents & Downloads
- Espressif product page: https://www.espressif.com/en/products/socs/esp32-s3
- ESP-IDF documentation: https://docs.espressif.com/projects/esp-idf/
- ESP-Matter: https://github.com/espressif/esp-matter