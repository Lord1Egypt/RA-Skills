# Home Security Panel (multi-vendor observed)

> **Source class:** Third-party teardowns, OEM reference designs, and
> vendor application notes. BOMs here are vendor-neutral; they reflect
> what is commonly observed in shipped products or what multi-vendor
> reference designs recommend. For single-vendor reference designs
> (e.g. TI CC2640R2F + TI SensorTag), see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A wireless home security control panel with keypad/touch, alarm siren
trigger, and Z-Wave/Zigbee/BLE mesh sensor connectivity. Generic,
vendor-neutral requirements:

- **Always-on**: mains-powered with battery backup.
- **Wireless**: BLE 5.x + 802.15.4 (Thread/Zigbee) for sensor mesh.
- **Sub-1GHz**: optional (TI CC13xx) for long-range outdoor sensors.
- **Tamper detection**: case-open + wall-removal sensors.
- **Siren driver**: 12V / 1A driver for external siren.
- **Cellular backup**: optional LTE-M / NB-IoT for alarm reporting.

Constraints:
- Cost-sensitive BOM (< $80 main panel, excluding sensors).
- Long product life (5+ years, security certification).
- Regulatory: UL 1023 (US), EN 50131 (EU).

## BOM Candidates (multi-vendor, third-party observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| BLE SoC (panel-side) | **CC2640R2F** | TI | Mature BLE 5.1 SoC, well-documented low-power + security (AES-128) reference designs. | [link](../../semiconductor-vendor/TI/product_families.md#cc2640r2f) |
| BLE SoC (panel-side) | **CC2652R** | TI | Multi-protocol (BLE 5 + 802.15.4 Zigbee/Thread/Matter) — single SoC for mesh + phone pairing. | [link](../../semiconductor-vendor/TI/product_families.md#cc2652r) |
| Sub-1GHz (outdoor sensors) | **CC1310** | TI | Long-range Sub-1GHz for outdoor motion / doorbell sensors (up to 1 km line-of-sight). | [link](../../semiconductor-vendor/TI/product_families.md#cc1310) |
| Wi-Fi + BLE companion | **CC3301** | TI | Add Wi-Fi 6 + BLE 5.4 to a host MCU for cloud connectivity. | [link](../../semiconductor-vendor/TI/product_families.md#cc3300) |
| Multi-vendor alternative | **EFR32MG24** | Silicon Labs | Matter-ready multi-protocol SoC with strong security (SESIP3). | [link](../../semiconductor-vendor/SiliconLabs/product_families.md) |
| Siren driver | TPA3116D2 or DRV8870 | TI / TI | Class-D amp / brushed DC driver for 12V siren. | (off-catalog) |
| Tamper switch | SW-18010 | generic | Mechanical vibration / tilt switch. | (off-catalog) |
| Backup battery charger | BQ25895 | TI | 1-cell Li-ion + boost to 12V for siren. | (off-catalog) |

## Selection matrix

Top 3 panel-side MCU candidates by typical home-security requirements:

1. **TI CC2652R** — best multi-protocol in single SoC (BLE 5 + Thread/Zigbee/Matter).
   Future-proofs for Matter-based sensor ecosystems. Mature SDK + Zigbee stack.
2. **TI CC2640R2F** — simpler / cheaper if BLE-only is acceptable. Best for
   traditional phone-paired security panels without Matter/Zigbee.
3. **Silicon Labs EFR32MG24** — Matter-ready with SESIP3 security certification.
   Best if pre-certifying for EN 42021 / SESIP3 is on the roadmap.

For Sub-1GHz outdoor sensors (motion / doorbell), add **TI CC1310** in the
sensor nodes — pairs with CC2652R (which also supports Sub-1GHz on some variants).

For cloud connectivity (Wi-Fi), add **TI CC3301** as a companion IC to the
panel MCU (CC3301 = Wi-Fi 6 + BLE 5.4; CC3300 = Wi-Fi 6 only).

## Verification status

- BLE SoC candidates: linked to TI / SiliconLabs product_families.md with
  verified URLs (see each vendor's 2026-06-29 firecrawl pass).
- Siren driver / tamper switch / battery charger: not catalogued in this
  skill — consult vendor selection guides separately.

## Regulatory notes

- UL 1023 (US household security): tamper detection + supervised loop
  required. Affects BOM (need supervised-zone current monitoring).
- EN 50131 (EU intruder alarm): security grade 2 minimum. Affects MCU
  choice (need hardware crypto + secure boot).
- FCC Part 15 (US RF): affects antenna design for BLE / Sub-1GHz.