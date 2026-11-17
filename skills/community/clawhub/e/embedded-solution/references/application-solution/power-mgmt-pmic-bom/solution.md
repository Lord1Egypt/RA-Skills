# Power Management IC Selection (multi-vendor observed)

> **Source class:** Vendor product pages + multi-vendor reference designs.
> BOMs here are vendor-neutral; for single-vendor reference designs see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A power management BOM for a typical IoT device (MCU + wireless + sensors).
Generic requirements:

- **Rails**: 3.3V (MCU + wireless), 1.8V (MCU core), 5V (USB / sensors)
- **Source**: USB, 1-cell Li-ion, or 2x AA batteries
- **Efficiency**: > 85% for always-on rails, > 90% for high-current rails
- **Quiescent current**: < 10 µA for always-on rails
- **Cost-sensitive**: < $1 BOM for the power section

## BOM Candidates (multi-vendor, observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| DC-DC buck (3.3V, 500mA) | **SY8089** | Silergy | 1.5 MHz sync buck, tiny SOT-23-5. | [link](../../semiconductor-vendor/Silergy/product_families.md#sy8089) |
| DC-DC buck (3.3V, 1A) | **SY8120i** | Silergy | 1.5 MHz sync buck, SOT-23-6. | [link](../../semiconductor-vendor/Silergy/product_families.md#sy8120i) |
| DC-DC buck (high current) | **SY8032** | Silergy | 3A sync buck. | [link](../../semiconductor-vendor/Silergy/product_families.md#sy8032abc) |
| LDO (low-Iq) | **SGM8903** | SGMicro | 500mA LDO, 1.5 µA Iq. | [link](../../semiconductor-vendor/SGMicro/product_families.md#sgm8903) |
| LDO (low-noise) | **SGM6601** | SGMicro | Low-noise LDO for RF supply. | [link](../../semiconductor-vendor/SGMicro/product_families.md#sgm6601) |
| Load switch | **SY6280** | Silergy | 2A load switch with adjustable rise time. | [link](../../semiconductor-vendor/Silergy/product_families.md#sy6280) |
| USB switch / MUX | **SGM3157** | SGMicro | 300 MHz SPDT analog switch. | [link](../../semiconductor-vendor/SGMicro/product_families.md#sgm3157) |
| Battery charger (1-cell Li-ion) | ISL9238 | Renesas | Buck-boost charger (off-catalog here). | [link](../../semiconductor-vendor/Renesas/product_families.md#isl9238) |

## Selection matrix

Top 3 buck converters for typical IoT BOM:

1. **Silergy SY8120i** — 1A sync buck @ 1.5 MHz, $0.20. Best for 3.3V
   rail with 500 mA peak load.
2. **Silergy SY8089** — lower-cost ($0.15), 500 mA, same topology. For
   cost-down designs.
3. **Silergy SY8032** — 3A buck. For designs that need higher current
   (e.g. ESP32-S3 with peak 500 mA Wi-Fi TX).

Top 3 LDOs for always-on rails:

1. **SGMicro SGM8903** — 1.5 µA Iq, 500 mA. Best for always-on rail.
2. **SGMicro SGM6601** — low-noise (8 µVrms). For RF supply.
3. **Renesas ISL9205** — different vendor family. See Renesas
   product_families.md.

## Verification status

- Silergy parts: linked to Silergy product_families.md (verified 2026-06-29
  firecrawl pass; per-product pages blocked by JS rendering — see Status Notes).
- SGMicro parts: linked to SGMicro product_families.md (verified 2026-06-29).
- Renesas ISL9238: linked to Renesas product_families.md (verified 2026-06-29).

## Notes

- **Quiescent current budget**: a typical IoT device spends 99% of its
  time in sleep. Total Iq budget is ~10 µA across all always-on rails.
  Pick LDOs with < 5 µA Iq each.
- **Inductor sizing**: 1.5 MHz switching allows 1-2.2 µH inductors.
  Smaller inductance = smaller solution size but higher ripple.
- **PCB layout**: buck converters are sensitive to feedback loop routing.
  Keep feedback trace short, away from switching node. Use 4-layer PCB
  with ground plane for high-current rails.