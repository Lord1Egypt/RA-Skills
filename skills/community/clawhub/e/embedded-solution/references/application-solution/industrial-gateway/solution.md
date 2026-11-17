# Industrial Gateway / HMI (multi-vendor observed)

> **Source class:** Third-party teardowns, OEM reference designs, and
> vendor application notes. BOMs here are vendor-neutral; they reflect
> what is commonly observed in shipped products or what multi-vendor
> reference designs recommend. For single-vendor reference designs
> (e.g. NXP i.MX RT1064 + MCUXpresso), see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A high-performance industrial gateway / HMI panel for factory automation,
machine control, or building management. Generic, vendor-neutral requirements:

- **Real-time control**: EtherCAT / PROFINET / Modbus TCP master
- **HMI display**: 7-10" color TFT (WVGA / WXGA)
- **Wireless**: Wi-Fi + BLE for commissioning / OTA
- **Wired**: 2x Ethernet (one for fieldbus, one for uplink)
- **Storage**: eMMC / SD card for logging
- **Operating system**: Linux or RTOS (Zephyr / FreeRTOS)

Constraints:
- Industrial temperature range (-40 to +85 °C).
- 5-10 year product life.
- Cost-sensitive BOM (< $150 main board, excluding display + housing).

## BOM Candidates (multi-vendor, third-party observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| Host MCU (high-perf) | **i.MX RT1064** | NXP | Cortex-M7 @ 600 MHz, WXGA LCD, 2D GPU, integrated DC-DC. | [link](../../semiconductor-vendor/NXP/product_families.md#imx-rt1064) |
| Host MCU (heterogeneous) | **i.MX RT1170** | NXP | Cortex-M7 + Cortex-M4, for offloading real-time tasks to M4 core. | [link](../../semiconductor-vendor/NXP/product_families.md#imx-rt1170) |
| Host MCU (mid-range) | **LPC55S69** | NXP | Cortex-M33 @ 150 MHz, lower cost, no HMI peripherals. | [link](../../semiconductor-vendor/NXP/product_families.md#lpc55s69) |
| Host MCU (cost-down) | **K66** | NXP | Cortex-M4 @ 180 MHz, mature, low cost. | [link](../../semiconductor-vendor/NXP/product_families.md#k66) |
| Wi-Fi + BLE companion | **CC3301** | TI | Wi-Fi 6 + BLE 5.4 companion IC. | [link](../../semiconductor-vendor/TI/product_families.md#cc3300) |
| Wi-Fi + BLE SoC (all-in-one) | **ESP32-S3** | Espressif | If prefer all-in-one over host + companion. | [link](../../semiconductor-vendor/Espressif/product_families.md#esp32-s3) |

External (not catalogued in this skill):
- Ethernet PHY (e.g. TI DP83826 for industrial)
- TFT display panel
- Touch controller (e.g. FT5x06)
- eMMC / SD card slot

## Selection matrix

Top 3 host MCU candidates by typical industrial gateway / HMI requirements:

1. **NXP i.MX RT1064** — best Cortex-M7 single-core for WXGA + 2D GPU HMI.
   600 MHz + 1 MB SRAM + integrated DC-DC = lowest BOM for HMI panels.
2. **NXP i.MX RT1170** — heterogeneous dual-core (M7 + M4) for designs that
   need real-time control offloaded to the M4 while the M7 handles HMI.
3. **NXP LPC55S69** — Cortex-M33 + TrustZone for secure designs without HMI.
   Lower cost than RT1064/RT1170 but no display controller.

For designs needing cost-down (no display, no 2D GPU), drop to **K66**
or even to **LPC55S69** — saves ~$5-10 per part.

## Verification status

- MCU candidates: linked to NXP product_families.md with verified URLs
  (see 2026-06-29 firecrawl pass).
- Wi-Fi + BLE candidates: TI / Espressif product_families.md.
- External parts (Ethernet PHY, display, touch controller): not catalogued
  in this skill — consult vendor selection guides separately.

## Operating system notes

- **Bare metal / FreeRTOS**: works on all candidates above. Lower RAM
  requirement (256 KB SRAM suffices for most designs).
- **Zephyr**: officially supported on NXP i.MX RT + LPC55S69 families.
  TI CC2640R2F too.
- **Linux**: not suitable for these Cortex-M parts. For Linux-capable
  designs, switch to NXP i.MX 8M or similar Cortex-A MPUs.