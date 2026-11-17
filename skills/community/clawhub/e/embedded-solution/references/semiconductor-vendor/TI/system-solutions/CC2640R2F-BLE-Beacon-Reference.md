# CC2640R2F BLE Beacon Reference (TI SimpleLink™ Wireless MCU family)

> **Vendor:** Texas Instruments
> **Part:** CC2640R2F
> **Source:** TI CC2640R2F product page + CC2640R2F SDK documentation
> **Family context:** SimpleLink™ CC26xx / CC13xx multi-standard wireless MCU family

## Overview

The **CC2640R2F** is TI's mainstream BLE 5.1 SoC for cost-sensitive
wireless applications: BLE beacons, BLE peripherals, simple sensor
nodes. It integrates:

- **Arm Cortex-M3** application core (48 MHz)
- **Arm Cortex-M0** radio core (dedicated to BLE stack)
- **Memory**: 128 KB flash + 28 KB SRAM
- **Radio**: BLE 5.1 + proprietary 2.4 GHz modes
- **Security**: AES-128 hardware accelerator + true random number generator

For high-volume cost-sensitive designs (asset tracking beacons, retail
beacons, simple sensor nodes), CC2640R2F is TI's go-to choice.

## Reference design topology

```
   ┌──────────────────┐
   │   Battery (CR2032)│
   └────────▲─────────┘
            │
   ┌────────┴─────────┐
   │   CC2640R2F SoC  │
   │  (M3 + M0)       │
   └────────▲─────────┘
            │ GPIO / I2C
   ┌────────┴─────────┐
   │  Sensor (optional)│
   │  (temp, accel, etc)│
   └──────────────────┘
```

## Key features (from CC2640R2F family page)

- **BLE 5.1**: full feature set incl. LE Coded PHY (long range), advertising extensions
- **Direction finding**: AoA / AoD support (with antenna array add-on)
- **Multi-protocol**: supports BLE 5 + proprietary 2.4 GHz (CC2652R / CC1352R
  add Zigbee / Thread; CC2640R2F is BLE-only for cost reasons)
- **Low power**: < 1 µA sleep current with RTC + RAM retention
- **Security**: AES-128 crypto + secure boot + TRNG
- **Tools**: CCS (Code Composer Studio) + TI SysConfig pinmux tool

## BOM candidates (TI-centric)

| Function | Part | Notes |
|----------|------|-------|
| BLE SoC | **CC2640R2F** | Main chip |
| Crystal | 32.768 kHz + 24 MHz | Two-crystal reference design |
| Antenna | Chip antenna (Johanson 2450AT18B100) or PCB trace | TI reference designs include both |
| Decoupling caps | 100 nF + 1 µF + 10 µF | Standard BLE SoC decoupling |
| Optional sensor | TMP117 (temp) or OPT3001 (light) | I2C, off-catalog |

## Selection criteria — when to choose CC2640R2F

✅ Choose CC2640R2F when:
- Need BLE 5.1 beacon / sensor node at lowest cost
- Battery life > 1 year on CR2032
- Don't need Zigbee / Thread / Matter

❌ Avoid CC2640R2F when:
- Need multi-protocol mesh (use CC2652R for Zigbee/Thread)
- Need Wi-Fi (add CC3301 companion or use CC3220/CC3235 SoC)
- Need Matter / Thread specifically (use CC2652R or CC1352P)

## Verification status

- CC2640R2F product page: ✅ verified via ti.com URL (HTTP 200)
- Specs in `specs/TI/CC2640R2F.yaml` (datasheet-extracted fields)
- BOM candidates cross-referenced to TI product_families.md

## Source documents

- Datasheet: product page → Documents & Downloads
- TI product page: https://www.ti.com/product/CC2640R2F
- BLE5-Stack SDK: https://www.ti.com/tool/BLE-STACK
- TI Reference Designs: search "CC2640R2F reference design" on ti.com