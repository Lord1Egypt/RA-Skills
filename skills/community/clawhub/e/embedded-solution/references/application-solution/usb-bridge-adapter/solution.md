# USB-UART / USB Bridge Adapter (multi-vendor observed)

> **Source class:** Vendor product pages + multi-vendor reference designs.
> BOMs here are vendor-neutral; for single-vendor reference designs see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A simple USB-to-UART/SPI/I2C bridge adapter for development, debugging,
and field programming. Generic requirements:

- **USB**: USB 2.0 Full Speed or High Speed.
- **Bridge protocols**: UART (most common), SPI, I2C, GPIO.
- **Driver**: free / standard (CDC-ACM for UART, libusb for SPI/I2C).
- **Cost-sensitive**: < $3 BOM for the bridge chip alone.

## BOM Candidates (multi-vendor, observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| USB-UART bridge | **CH340C** | WCH | Ultra-low-cost USB-UART bridge IC; widely cloned. | [link](../../semiconductor-vendor/WCH/product_families.md#ch340c) |
| USB-UART bridge | CH340N / CH340E | WCH | Variants with internal crystal / smaller package. | [link](../../semiconductor-vendor/WCH/product_families.md#ch340c) |
| USB-SPI/I2C/JTAG bridge | **CH32V003** | WCH | Tiny RISC-V MCU for custom USB-SPI/I2C firmware. | [link](../../semiconductor-vendor/WCH/product_families.md#ch32v003) |
| USB MCU (multi-protocol) | **ESP32-S3** | Espressif | USB OTG + Wi-Fi + BLE, for advanced bridges. | [link](../../semiconductor-vendor/Espressif/product_families.md#esp32-s3) |
| USB MCU (low cost) | **STM32G0** | ST | USB 2.0 FS device + crystal-less, for CDC-ACM. | (off-catalog) |

## Selection matrix

1. **WCH CH340C** — cheapest USB-UART IC ($0.10 in qty 100). No firmware
   to write; CDC-ACM driver. Default for low-cost hobby / dev boards.
2. **WCH CH32V003** — if you need SPI/I2C/GPIO bridge with custom
   firmware. Tiny QFN-20, USB device. Programmable via WCH-Link.
3. **Espressif ESP32-S3** — if you need Wi-Fi + BLE + USB bridge. Most
   expensive; use for advanced debug scenarios (e.g. wireless log
   forwarding).

## Verification status

- WCH CH340C / CH32V003: linked to WCH product_families.md.
- ESP32-S3: linked to Espressif product_families.md.
- STM32G0: not catalogued — off-the-shelf USB-UART modules widely
  available from Adafruit / FTDI clones.

## Notes

- **Driver installation**: CH340 needs a third-party CDC-ACM driver on
  Windows; macOS / Linux use built-in cdc_acm. Some "clone" CH340 chips
  have buggy drivers — buy from reputable sources (LCSC, WCH direct).
- **FTDI clone caveat**: avoid FTDI clones — genuine FTDI chips trigger
  bricking of clones via PID reset.