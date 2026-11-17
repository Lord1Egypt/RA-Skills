# ESP32-C3 BLE Beacon Reference

> **Source:** Espressif-published ESP-IDF example for an Eddystone /
> iBeacon BLE beacon on the cost-optimised ESP32-C3 SoC. BOM is
> **Espressif-only** (single-vendor).

## Overview
An Espressif-published reference design showing a battery-friendly
BLE beacon (broadcast-only, no connection) on the ESP32-C3 single-
core RISC-V SoC. Suitable for asset tracking, retail beacons, and
find-my-device applications.

- **Vendor:** Espressif Systems
- **Published as:** `esp-idf` example
  `bluetooth/bluedroid/ble/ble_eddystone` or `ble_ibeacon`
- **Document type:** Reference design (SDK example)
- **Dev kit:** ESP32-C3-DevKitM-1 or ESP32-C3-DevKitC-02
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.espressif.com/en/products/socs/esp32-c3 (verification pending; site Cloudflare-gated)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Espressif/ESP32-C3.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Espressif/product_families.md` and the datasheet)*

## BOM Candidates (Espressif only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Cost-optimised Wi-Fi+BLE 5 SoC (RISC-V) | **ESP32-C3** | [link](../product_families.md#esp32-c3) | RISC-V single-core 32-bit, BLE 5, 400 KB SRAM |
| Dev kit platform | **ESP32-C3-DevKitM-1** | Espressif product page | Miniature form factor with on-board USB-Serial/JTAG |

External to Espressif (out of BOM scope for this single-vendor solution):
- USB cable (power + programming)
- Host PC with ESP-IDF toolchain
- CR2032 coin cell or other battery for the deployed beacon
- Smartphone with nRF Connect / LightBlue for BLE verification

## Reference Design Verification Status

- [ ] Original Espressif product page URL HTTP 200 — verification pending.
- [x] Datasheet already present at
      product page → Documents & Downloads.
- [ ] Pin ESP32-C3 variant (ESP32-C3-MINI-1 module on DevKitM-1;
      ESP32-C3-WROOM-02 on DevKitC-02). Both work but have different
      antenna / size tradeoffs.
- [ ] Decide whether the beacon should be Eddystone (open), iBeacon
      (Apple-proprietary), or both. ESP-IDF examples cover both.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The ESP32-C3 spec values
> (clock, BLE TX power, sleep current, etc.) live in
> `specs/Espressif/ESP32-C3.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet PDF
> under product page → Documents & Downloads.

## Source Discipline

- Original example published by Espressif on docs.espressif.com / in
  the esp-idf GitHub repository.
- This entry only references Espressif parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.

## Architecture Note

The ESP32-C3 uses the **open-source RISC-V** instruction set
(RV32IMC), unlike the rest of the ESP32 family (Xtensa). ESP-IDF
builds for ESP32-C3 with `riscv32-esp-elf-gcc`. Toolchain support is
mature but slightly different from the Xtensa lineage — keep this
in mind when porting C / FreeRTOS code between ESP32 variants.
