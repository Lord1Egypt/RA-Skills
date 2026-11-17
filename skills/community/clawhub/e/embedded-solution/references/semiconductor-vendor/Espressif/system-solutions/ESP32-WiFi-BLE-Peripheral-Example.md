# ESP32 Wi-Fi + BLE Peripheral Example

> **Source:** Espressif-published ESP-IDF example demonstrating a Wi-Fi
> station + BLE peripheral running concurrently on the ESP32 SoC, on
> the ESP32-DevKitC development board. BOM is **Espressif-only**
> (single-vendor). For multi-vendor teardown-derived solutions see
> `references/application-solution/`.

## Overview
An Espressif-published ESP-IDF example showing a typical IoT node use
case: ESP32 connects to an AP as a Wi-Fi station while simultaneously
running a BLE peripheral role for local provisioning or sensor
broadcast. Built on the official `esp-idf` examples.

- **Vendor:** Espressif Systems
- **Published as:** `esp-idf` examples `wifi/getting_started/station`
  + `bluetooth/bluedroid/ble/gatt_client`
- **Document type:** SDK example (source code + readme)
- **Dev kit:** ESP32-DevKitC (ESP32-WROOM-32 module variant)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.espressif.com/en/products/socs/esp32 (verification pending; site Cloudflare-gated for direct curl, but the documentation subdomain serves the datasheet directly)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Espressif/ESP32.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Espressif/product_families.md` and the datasheet)*

## BOM Candidates (Espressif only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Dual-core Wi-Fi+BT SoC | **ESP32** | [link](../product_families.md#esp32) | Xtensa LX6 dual-core, Wi-Fi b/g/n + Bluetooth 4.2 BR/EDR + BLE |
| Dev kit platform | **ESP32-DevKitC** | Espressif product page | On-board USB-UART bridge, JTAG; uses ESP32-WROOM-32 module |

External to Espressif (out of BOM scope for this single-vendor solution):
- USB cable (power + programming / serial console)
- Host PC with ESP-IDF toolchain
- Wi-Fi AP and a BLE peer device (smartphone) for testing

## Reference Design Verification Status

- [ ] Original Espressif product page URL HTTP 200 — verification pending.
      The documentation subdomain serves the datasheet directly; the
      main site is Cloudflare-gated but reachable via the browser.
- [x] Datasheet already present at
      product page → Documents & Downloads (v5.2).
- [ ] Pin the exact ESP32 variant used (ESP32-WROOM-32 vs ESP32-WROVER
      vs ESP32-SOLO-1). WROOM is the DevKitC default.
- [ ] Confirm ESP-IDF release tag (different tags use slightly
      different example paths).

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The ESP32 spec values
> (clock, CoreMark score, BLE sensitivity, etc.) live in
> `specs/Espressif/ESP32.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet PDF
> under product page → Documents & Downloads.

## Source Discipline

- Original example published by Espressif on docs.espressif.com / in
  the esp-idf GitHub repository.
- This entry only references Espressif parts (single-vendor rule).
- For multi-vendor teardowns (which may include Nordic / TI / NXP
  parts), see `references/application-solution/`.

## Architecture Note

The ESP32 family uses the **Xtensa LX6** core (dual-core 32-bit) — not
ARM Cortex-M. When discussing with engineers unfamiliar with Xtensa,
note that ESP-IDF builds with `xtensa-esp32-elf-gcc`, not the ARM
toolchain. Toolchain availability and ecosystem maturity differ from
ARM Cortex-M peers.
