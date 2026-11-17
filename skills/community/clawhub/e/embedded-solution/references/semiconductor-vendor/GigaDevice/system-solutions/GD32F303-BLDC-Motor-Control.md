# GD32F303xx BLDC Motor Control Reference (GigaDevice GD32F303 Series)

> **Vendor:** GigaDevice
> **Part:** GD32F303xx
> **Source:** GigaDevice GD32F303 product page + GD32 firmware library
> **Family context:** GD32F30x — Cortex-M4 mainstream MCU

## Overview

The **GD32F303xx** is GigaDevice's mainstream Cortex-M4 MCU, designed
as a drop-in replacement for STM32F103 (with significantly higher
performance at similar price). Key specs:

- **Cortex-M4F** @ up to **120 MHz** (with FPU + DSP instructions)
- **Memory**: up to 3072 KB Flash + 48 KB SRAM + 1x USB FS
- **Peripherals**: 3x USART, 3x SPI, 2x I2C, 1x USB FS, 1x CAN, 3x 12-bit ADC
- **PWM**: 2x advanced timer (TIM0/TIM7) with 4 complementary PWM channels
- **Price**: ~$1.20 in qty 100

For BLDC / PMSM motor control, the GD32F303xx is one of the most
popular Cortex-M4 choices in the cost-sensitive segment.

## Reference design topology

```
   ┌──────────────────┐
   │  Hall Sensors    │  (3x digital)
   └────────▲─────────┘
            │ GPIO
   ┌────────┴─────────┐
   │ GD32F303xx SoC   │
   │  Cortex-M4F      │◄──── TIM0/7 PWM outputs (3-phase)
   └────────▲─────────┘
            │
   ┌────────┴─────────┐
   │  Gate Driver     │  (DRV8313 / IRS2003+IRF7507)
   └────────▲─────────┘
            │
   ┌────────┴─────────┐
   │   3-Phase FET    │  (BLDC motor)
   │      Bridge      │
   └──────────────────┘
```

## Key features (from GD32F303xx family page)

- **Performance**: 150 DMIPS @ 120 MHz
- **Memory**: 16-3072 KB Flash + 8-48 KB SRAM
- **PWM**: 4-channel complementary @ up to 1.5 MHz PWM clock
- **ADC**: 3x 12-bit @ 1 MSPS, with injected trigger for current sensing
- **Connectivity**: CAN, USB FS, 3x USART, 3x SPI, 2x I2C
- **Tools**: GigaDevice GD32Eclipse + Keil + IAR + GCC

## BOM candidates (GigaDevice-centric)

| Function | Part | Notes |
|----------|------|-------|
| MCU | **GD32F303xx** | Main chip |
| Gate driver | DRV8313 (TI) or IRS2003+IRF7507 | 3-phase bridge driver |
| FETs (integrated) | DRV8313 internal FETs | For ≤ 2.5A peak |
| FETs (discrete) | IRF7507 (or similar) | For higher current |
| Current sense | 3x 0.01Ω shunt + op-amp | Low-side current sensing |
| Hall sensor inputs | 3x 10 kΩ pull-up | + 100 nF filter cap |

## Selection criteria — when to choose GD32F303xx

✅ Choose GD32F303xx when:
- Need STM32F103-compatible layout (drop-in)
- Cost-sensitive (~$1.20 @ qty 100)
- 120 MHz + FPU + DSP is enough (don't need 200 MHz F4)

❌ Avoid GD32F303xx when:
- Need 200 MHz for high-speed FOC — use GD32F450xx
- Need USB HS / Ethernet — use GD32F450xx
- Need low-power Cortex-M0+ — use GD32E230xx

## Verification status

- GD32F303xx product page: ✅ verified via gigadevice.com URL (HTTP 200)
- Specs in `specs/GigaDevice/GD32F303xx.yaml` (datasheet-extracted fields)

## Source documents

- Datasheet: product page → Documents & Downloads
- GigaDevice product page: https://www.gigadevice.com/product/mcu/main-stream-mcus/gd32f30x-series
- GD32 firmware library: https://www.gigadevice.com/product/mcu/main-stream-mcus/gd32f30x-series