# Espressif Systems — Product Families

Espressif Systems (Shanghai, China) is a fabless semiconductor company
specialising in Wi-Fi + Bluetooth/BLE SoCs. Their parts are widely used
in IoT, consumer electronics, and industrial wireless.

This document lists every Espressif chip referenced in this skill's
specs/Espressif/*.yaml files, with a brief one-line summary, link
status, and the main product page.

| Part | Family | Status | Datasheet | Link |
|------|--------|--------|-----------|------|
| **ESP32** | Xtensa LX6 dual-core Wi-Fi+BT SoC | ✅ | [link](https://www.espressif.com/en/products/socs/esp32) | [datasheet](product page → Documents & Downloads) |
| **ESP32-S3** | Xtensa LX7 dual-core Wi-Fi+BLE 5 SoC | ✅ | [link](https://www.espressif.com/en/products/socs/esp32-s3) | [datasheet](product page → Documents & Downloads) |
| **ESP32-C3** | RISC-V single-core Wi-Fi+BLE 5 SoC | ✅ | [link](https://www.espressif.com/en/products/socs/esp32-c3) | [datasheet](product page → Documents & Downloads) |

## Status Legend

- ✅  Product page reachable (HTTP 200)
- ❌  Part has been removed/renamed/relocated — do NOT use
- ⏳  Verification pending — recheck before recommending

## Note on Architecture

The ESP32 family uses **Tensilica Xtensa** cores (LX6 / LX7), which is
unusual in the embedded MCU world (most peers use ARM Cortex-M). The
ESP32-C3 family uses the open-source **RISC-V** ISA (RV32IMC). When
describing BOMs to readers unfamiliar with these ISAs, mention them
explicitly.


## ESP32-C6 / ESP32-H2 Series — RISC-V + Matter

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **ESP32-C6** | ✅ | https://www.espressif.com/en/products/socs/esp32-c6 | [datasheet PDF](https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf) |
| **ESP32-H2** | ✅ | https://www.espressif.com/en/products/socs/esp32-h2 | product page → Documents & Downloads |

---

## Status Notes

- All 5 product families verified ✅ as of 2026-06-28 link-verification round.
- YAML files in `specs/Espressif/` (4 yamls: ESP32, ESP32-S3, ESP32-C3, ESP32-C6)
  all verified with datasheet-extracted fields.
- **2026-06-29 v0.4.0 firecrawl pass**: 6 product family pages re-fetched via
  Firecrawl (ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6, ESP32-H2). All
  6 returned real content; saved to
  `references/semiconductor-vendor/Espressif/firecrawl-snapshots/`. Total
  ~63KB clean markdown, 6 credits consumed. No YAML upgrades needed — all 4
  yamls already verified. No numerical parameters added per design policy.
