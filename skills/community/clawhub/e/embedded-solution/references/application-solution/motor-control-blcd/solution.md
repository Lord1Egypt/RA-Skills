# Motor Control / BLDC Driver (multi-vendor observed)

> **Source class:** Vendor product pages + multi-vendor reference designs.
> BOMs here are vendor-neutral; for single-vendor reference designs see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A BLDC / PMSM motor driver for small appliances, fans, pumps, drones.
Generic requirements:

- **Motor**: 3-phase BLDC / PMSM, 12-48V, up to 30A peak.
- **PWM**: 3-phase complementary PWM @ 20-50 kHz.
- **Feedback**: Hall sensors (3x digital) or FOC (sensorless via ADC).
- **Protection**: over-current, over-voltage, over-temperature, locked rotor.
- **Cost-sensitive**: < $10 BOM for the control section.

## BOM Candidates (multi-vendor, observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| MCU (Cortex-M4, mainstream) | **GD32F303xx** | GigaDevice | STM32F103-compatible, lower cost, 120 MHz. | [link](../../semiconductor-vendor/GigaDevice/product_families.md#gd32f303xx) |
| MCU (Cortex-M4, high-perf) | **GD32F450xx** | GigaDevice | 200 MHz Cortex-M4F, USB HS, Ethernet. | [link](../../semiconductor-vendor/GigaDevice/product_families.md#gd32f450xx) |
| MCU (Cortex-M0+, low-power) | **GD32E230xx** | GigaDevice | Entry-level for simple 6-step commutation. | [link](../../semiconductor-vendor/GigaDevice/product_families.md#gd32e230xx) |
| MCU (RISC-V) | **GD32VF103** | GigaDevice | RISC-V alternative to STM32F103. | [link](../../semiconductor-vendor/GigaDevice/product_families.md#gd32vf103) |
| Motor driver IC (multi-vendor) | DRV8313 / L6234 | TI / ST | Integrated 3-phase FET driver. | (off-catalog) |
| Gate driver + FETs | IRS2003 + IRF7507 | Infineon / IR | Discrete 3-phase bridge. | (off-catalog) |

## Selection matrix

1. **GD32F303xx** — STM32F103 pin-compatible drop-in replacement at
   lower cost. 120 MHz Cortex-M4. Most common for BLDC.
2. **GD32F450xx** — when FOC with sensorless high-speed operation
   needed. 200 MHz Cortex-M4F with FPU + DSP instructions.
3. **GD32E230xx** — cost-down for simple 6-step commutation (no FOC).
   72 MHz Cortex-M0+.

## Verification status

- MCU candidates: linked to GigaDevice product_families.md (verified
  2026-06-29 firecrawl pass + datasheet-extracted yamls).
- Motor driver ICs: not catalogued — see TI / ST / Infineon reference
  designs for 3-phase bridge topologies.

## Notes

- **FOC vs 6-step**: FOC gives smoother torque + lower acoustic noise
  but needs ~3× more CPU. GD32F303xx can do FOC for motors up to ~10K
  RPM; GD32F450xx for high-speed applications.
- **Sensorless FOC**: requires BEMF ADC sampling, common in drone /
  fan applications. GD32F303xx has 3x 12-bit ADC @ 1 MSPS — sufficient
  for most BLDC sensorless FOC designs.