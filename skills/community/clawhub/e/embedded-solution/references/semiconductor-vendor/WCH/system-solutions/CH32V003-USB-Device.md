# CH32V003 USB Device Reference (WCH CH32V RISC-V MCU Family)

> **Vendor:** WCH (南京沁恒微电子)
> **Part:** CH32V003
> **Source:** WCH CH32V003 product page + CH32V003 EVT reference firmware
> **Family context:** CH32V RISC-V MCU family — QingKe V2 RISC-V core

## Overview

The **CH32V003** is WCH's entry-level RISC-V MCU for cost-sensitive
USB device applications. It integrates:

- **QingKe V2 RISC-V core** @ up to 48 MHz
- **Memory**: 2 KB SRAM + 16 KB Flash (with single-wire debug)
- **USB 2.0 Full Speed device** with built-in PHY
- **Peripherals**: 1x USART, 1x I2C, 1x SPI, 8-channel ADC, etc.
- **Package**: QFN-20, TSSOP-20, SOP-16, SOP-8
- **Price**: ~$0.10 in qty 100 (the cheapest USB-capable MCU in market)

Common uses: USB HID devices (keyboard / mouse / custom HID), USB CDC
serial bridges, USB-to-I2C/SPI adapters, USB LED controllers.

## Reference design topology

```
   ┌──────────────────┐
   │   USB-C / microB │
   └────────▲─────────┘
            │ D+ / D-
   ┌────────┴─────────┐
   │  CH32V003 SoC    │
   │ (QingKe V2 RISC-V)│
   └────────▲─────────┘
            │ GPIO / I2C / SPI / UART
   ┌────────┴─────────┐
   │  External Device │
   │  (sensor, etc.)  │
   └──────────────────┘
```

## Key features (from CH32V003 family page)

- **CPU**: 32-bit RISC-V QingKe V2 @ 48 MHz
- **Memory**: 2 KB SRAM + 16 KB Flash (single-wire debug SDI)
- **USB**: USB 2.0 FS device with on-chip PHY and pull-up resistor
- **Peripherals**: 1x USART, 1x I2C, 1x SPI, 18 GPIO, 8-ch 10-bit ADC
- **Packages**: QFN-20 (3×3 mm), TSSOP-20, SOP-16, SOP-8
- **Tools**: MounRiver Studio (WCH's Eclipse-based IDE), WCH-Link programmer
- **Price**: ~$0.10 @ qty 100

## BOM candidates (WCH-centric)

| Function | Part | Notes |
|----------|------|-------|
| USB MCU | **CH32V003** | Main chip |
| USB connector | USB-C or micro-B | Per design |
| Decoupling | 100 nF + 10 µF | Standard |
| Crystal (optional) | Internal 24 MHz RC | No external crystal needed |
| Pull-up resistor | Internal 1.5 kΩ | Built-in, no external needed |

## Selection criteria — when to choose CH32V003

✅ Choose CH32V003 when:
- Need cheapest USB device MCU (~$0.10)
- Small form factor (QFN-20 3×3 mm)
- Don't need high performance (48 MHz is fine)
- Want USB without external PHY / pull-up

❌ Avoid CH32V003 when:
- Need USB host (CH32V003 is device only)
- Need high performance (use CH32V307 @ 144 MHz)
- Need Wi-Fi / BLE (use ESP32-S3 instead)
- Need Linux capability (use Cortex-A SoC)

## Verification status

- CH32V003 product page: ✅ verified via wch-ic.com URL (HTTP 200)
- Specs in `specs/WCH/CH32V003.yaml` (datasheet-extracted fields)

## Source documents

- Datasheet: product page → Documents & Downloads
- WCH product page: https://www.wch-ic.com/products/CH32V003.html
- MounRiver Studio IDE: https://www.wch-ic.com/downloads/MounRiver_Studio.html
- WCH-Link programmer: https://www.wch-ic.com/products/WCH-Link.html