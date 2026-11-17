# i.MX RT1064 EtherCAT Slave Reference (NXP i.MX RT Crossover MCU family)

> **Vendor:** NXP
> **Part:** i.MX RT1064
> **Source:** NXP iMX-RT1064 product page + MCUXpresso SDK documentation
> **Family context:** i.MX RT Crossover MCU (Cortex-M7 @ 600 MHz)

## Overview

The **i.MX RT1064** is NXP's highest-performance Cortex-M7 crossover MCU,
designed for HMI / GUI applications with rich multimedia peripherals:

- **Arm Cortex-M7** application core @ up to 600 MHz (3020 CoreMark)
- **1 MB on-chip SRAM** (up to 512 KB configurable as TCM)
- **Integrated DC-DC converter** for low dynamic power
- **LCD controller** (up to WXGA 1366×768)
- **2D graphics acceleration engine** (PXP)
- **Parallel camera sensor interface**
- **3× I²S** for multi-channel audio
- **Extensive external memory interface** (NAND, eMMC, QuadSPI, Parallel NOR)

For HMI panels + EtherCAT / PROFINET slaves, RT1064 offers the best
performance / BOM ratio in the i.MX RT family.

## Reference design topology

```
   ┌──────────────────┐
   │  WXGA TFT Panel  │
   └────────▲─────────┘
            │ LVDS / RGB
   ┌────────┴─────────┐
   │  i.MX RT1064 SoC │
   │  (M7 @ 600 MHz)  │
   └────────▲─────────┘
            │ RMII / SPI
   ┌────────┴─────────┐
   │  Ethernet PHY    │
   │  (TI DP83826)    │
   └────────▲─────────┘
            │
   ┌────────┴─────────┐
   │ EtherCAT Slave   │
   │ (ET1100 chip)    │
   └──────────────────┘
```

## Key features (from iMX-RT1064 family page)

- **Performance**: 3020 CoreMark / 1284 DMIPS @ 600 MHz
- **Display**: WXGA (1366×768) LCD controller + 2D graphics (PXP)
- **Memory**: 1 MB SRAM (512 KB TCM) + QuadSPI NOR / eMMC / Parallel NOR
- **Audio**: 3× I²S + S/PDIF
- **Camera**: parallel 8/10/16-bit interface
- **Power**: integrated DC-DC, low-power run modes at 24 MHz, 20 ns interrupt latency
- **Tools**: MCUXpresso IDE + SDK + Config Tools (pin / clock / peripheral config)

## BOM candidates (NXP-centric)

| Function | Part | Notes |
|----------|------|-------|
| Host MCU | **i.MX RT1064** | Main chip |
| External flash | QuadSPI NOR 16-64 MB | For code + data |
| SDRAM | 16-32 MB (if needed) | External via SEMC |
| Ethernet PHY | TI DP83826 | Industrial temp, RMII |
| EtherCAT slave controller | Beckhoff ET1100 | Industry standard ESC |
| Display | 7-10" WVGA / WXGA TFT | LVDS or RGB |
| Touch controller | FT5x06 or Goodix GT911 | I2C, off-catalog |
| Wi-Fi + BLE | CC3301 (TI) companion | Optional |
| eMMC | 4-16 GB | For data logging |

## Selection criteria — when to choose i.MX RT1064

✅ Choose RT1064 when:
- Need HMI / GUI with WXGA display
- Need high-performance Cortex-M7 @ 600 MHz
- Need integrated DC-DC for low BOM
- Need 1 MB on-chip SRAM (no external SDRAM for many designs)

❌ Avoid RT1064 when:
- Need Linux (use NXP i.MX 8M Cortex-A MPUs)
- Need multi-protocol wireless (add CC3301 companion)
- Need Thread / Matter / Zigbee as SoC (use RT1170 + 802.15.4 module)

## Verification status

- iMX-RT1064 product page: ✅ verified via nxp.com URL (HTTP 200)
- Specs in `specs/NXP/i.MX_RT1064.yaml` (family-page-extracted, 2026-06-29)
- BOM candidates cross-referenced to NXP product_families.md

## Source documents

- Datasheet: product page → Documents & Downloads
- NXP product page: https://www.nxp.com/products/i.MX-RT1064
- MCUXpresso SDK: https://www.nxp.com/design/design-center/software/development-software/mcuxpresso-software-and-tools-:MCUXPRESSO
- Zephyr port: https://www.nxp.com/design/design-center/software/embedded-software/zephyr-os-for-edge-connected-devices:ZEPHYR-OS-EDGE