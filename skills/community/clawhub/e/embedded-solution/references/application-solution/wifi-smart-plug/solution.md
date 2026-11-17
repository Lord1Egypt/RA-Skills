# Wi-Fi Smart Plug (multi-vendor observed)

> **Source class:** Third-party teardowns, OEM reference designs, and
> vendor application notes. BOMs here are vendor-neutral; they reflect
> what is commonly observed in shipped products or what multi-vendor
> reference designs recommend. For single-vendor reference designs
> (e.g. Espressif ESP32-S3 + ESP-IDF), see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A wall-outlet Wi-Fi smart plug with energy monitoring and app/cloud
control. Generic, vendor-neutral requirements:

- **Wireless**: Wi-Fi 4 (802.11 b/g/n) at minimum, ideally Wi-Fi 6.
- **BLE**: optional for setup / BLE commissioning.
- **Power metering**: ±0.5% accuracy voltage / current / power.
- **Relays**: 1× or 2× 16A mechanical relay or 30A SSR.
- **Safety**: over-current, over-voltage, over-temperature protection.
- **OTA**: secure firmware update.

Constraints:
- Mains-powered (no battery).
- UL / CE safety certifications.
- Cost-sensitive BOM (< $15 total).

## BOM Candidates (multi-vendor, third-party observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| Wi-Fi+BLE SoC | **ESP32-S3** | Espressif | Dual-core Xtensa LX7, Wi-Fi 4 + BLE 5, mature ESP-IDF. | [link](../../semiconductor-vendor/Espressif/product_families.md#esp32-s3) |
| Wi-Fi+BLE SoC | **ESP32-C3** | Espressif | Single-core RISC-V, lowest-cost Wi-Fi+BLE option. | [link](../../semiconductor-vendor/Espressif/product_families.md#esp32-c3) |
| Wi-Fi+BLE SoC | **ESP32-C6** | Espressif | RISC-V + 802.15.4 (Thread/Zigbee) + Wi-Fi 6. | [link](../../semiconductor-vendor/Espressif/product_families.md#esp32-c6) |
| Wi-Fi companion | **CC3301** | TI | Add Wi-Fi 6 + BLE 5.4 to a host MCU. | [link](../../semiconductor-vendor/TI/product_families.md#cc3300) |
| MCU + Wi-Fi (multi-vendor) | **nRF7002 + nRF54L15** | Nordic | Premium Matter-ready combo. | [link](../../semiconductor-vendor/Nordic/product_families.md#nrf7002) |
| Power metering IC | BL0937 or HLW8012 | Chinese vendor | Energy monitoring, low cost. | (off-catalog) |
| AC/DC | BP2832A or similar | Chinese vendor | Non-isolated buck for low-power section. | (off-catalog) |
| Relay | HF115F / TRL90 | Chinese vendor | 16A mechanical relay. | (off-catalog) |

## Selection matrix

Top 3 Wi-Fi SoC candidates by typical smart plug requirements:

1. **ESP32-S3** — best price/performance for Wi-Fi + BLE smart plugs.
   Mature ESP-IDF + ESP-Matter + ESP RainMaker cloud. Default choice.
2. **ESP32-C3** — lowest-cost Wi-Fi 4 + BLE 5 SoC. Single-core RISC-V.
   Use when BOM < $10 is mandatory.
3. **ESP32-C6** — Wi-Fi 6 + 802.15.4 (Matter/Thread/Zigbee) + BLE.
   Use when Matter or Wi-Fi 6 is on the roadmap.

For designs that already have a host MCU, add **TI CC3301** (Wi-Fi 6
companion IC) instead of switching to an all-in-one SoC.

For premium Matter-ready designs, use **Nordic nRF54L15 + nRF7002**
combination.

## Verification status

- Wi-Fi+BLE SoC candidates: linked to Espressif / TI / Nordic
  product_families.md (verified 2026-06-29).
- Power metering / AC-DC / relay: not catalogued — Chinese-vendor parts
  widely available on LCSC / JLCPCB.

## Safety / regulatory notes

- **UL 60730** (US): functional safety for household appliances. Affects
  MCU choice (need Class B safety library).
- **IEC 60730** (EU): same standard, EU version.
- **FCC Part 15 / EN 300 328**: RF emissions. Wi-Fi module pre-cert
  (e.g. ESP32-S3 module with FCC ID) saves certification cost.
- **Reinforced isolation**: required between mains and low-voltage
  sections. Use opto-isolated relay driver + isolated AC-DC.