# Expected output skeleton — Fixture 17 (without-skill baseline)

## What this file is

This is the **canonical baseline** that a generic LLM produces when
the embedded-solution skill is *not* loaded. It is stored here as a
regression fixture — do NOT use this as the "right answer".

Use it to:
1. Score any model-without-skill response against the rubric
2. Demonstrate to new users the value the skill adds
3. Verify the with-skill version is meaningfully better

## Canonical baseline (2026-06-28)

The following is what a modern LLM (no skill) typically produces for
the prompt *"Without using the skill of embedded-solution, make
comparison table for popular BLE devices"*. It is reproduced here
verbatim from a baseline capture.

### Quick Picks (per use case)

| Use case | Recommended | Rationale |
|---|---|---|
| Flagship / multi-protocol | Nordic **nRF5340** | BLE 5.4 dual-core M33+M0+, 1 MB flash, multi-protocol |
| Mass consumer | Nordic **nRF52840** | BLE 5.0, 1 MB flash, mature ecosystem |
| Entry / minimal BOM | TI **CC2640R2F** | BLE 5.1, Cortex-M3, < $2 module |
| Thread + Matter | Nordic **nRF52840 + nRF802.15.4** companion | Matter-over-Thread |
| WiFi + BLE all-in-one | Espressif **ESP32-S3** | BLE 5.0 + WiFi, single chip |
| Ultra-low-power sensor | TI **CC2642R** | BLE 5.x, low-power |
| Wearable + large flash | Nordic **nRF5340** | Flash headroom for OTA |

### Top 5 Comparison Table

| Part | BLE | Core | Flash | RAM | TX | Main application |
|------|-----|------|-------|-----|----|-------------------|
| **nRF5340** | 5.4 | M33 app + M0+ net | 1 MB | 256 KB | +8 dBm | Flagship dual-core |
| **nRF52840** | 5.0 | M4F | 1 MB | 256 KB | +8 dBm | General flagship |
| **nRF52832** | 5.0 | M4 | 512 KB | 64 KB | +4 dBm | Mass consumer |
| **ESP32-S3** | 5.0 | Xtensa LX7 dual | 8 MB PSRAM opt | 512 KB | — | WiFi + BLE |
| **CC2640R2F** | 5.1 | M3 | 275 KB | 28 KB | +5 dBm | Entry level |

### Extended Comparison

| Spec | nRF5340 | nRF52840 | nRF52832 | ESP32-S3 | CC2640R2F |
|------|---------|----------|----------|----------|-----------|
| Core | Cortex-M33 (app) + M0+ (net) | Cortex-M4F | Cortex-M4 | Xtensa LX7 dual | Cortex-M3 |
| Clock | 128 MHz | 64 MHz | 64 MHz | 240 MHz | 48 MHz |
| BLE version | **5.4** | 5.0 | 5.0 | 5.0 | 5.1 |
| Flash | 1 MB | 1 MB | 512 KB | 8 MB ext | 275 KB |
| RAM | 256 KB | 256 KB | 64 KB | 512 KB | 28 KB |
| WiFi | ❌ | ❌ | ❌ | ✅ | ❌ |
| 802.15.4 | ❌ | ❌ | ❌ | ❌ | ❌ |
| TX power | +8 dBm | +8 dBm | +4 dBm | +20 dBm | +5 dBm |
| RX sensitivity | -98 dBm @ 1M | -95 dBm @ 1M | -96 dBm @ 1M | -97 dBm | -97 dBm |
| Active TX 0dBm current | 5.4 mA | 5.4 mA | 5.4 mA | ~240 mA (WiFi) | 6.1 mA |
| Sleep current | 1.9 µA | 1.9 µA | 1.9 µA | 10 µA | 1 µA |
| Voltage range | 1.7-5.5V | 1.7-5.5V | 1.7-5.5V | 2.3-3.6V | 1.8-3.8V |
| Package | aQFN73 / WLCSP | aQFN73 | QFN48 / WLCSP | QFN56 | QFN32 |

### 6 known issues with this baseline

1. **Fabricated BLE version numbers** — nRF5340 is BLE 5.2/5.3, not 5.4
2. **No comparison discipline** — gives "Top 1" recommendations in the
   use-case table; the with-skill answer forces Top 3 + single comparison
   table
3. **No tier / source citation** — every cell is ungrounded; no URL,
   no verification date, no datasheet anchor
4. **Missing the actual newest part** — TI CC2340R5 (the true BLE 5.4
   SoC as of 2026-06) is absent; the with-skill answer surfaces it
5. **Inflated confidence** — every cell is filled, no "not verified"
   marker anywhere; the with-skill answer explicitly marks gaps
6. **Conflated specs** — application-core flash and network-core flash
   summed without explanation; external PSRAM reported as "flash"
   without flagging it as external

## How to score this baseline against the rubric

Use `evaluation-rubric.md` 5 axes × 5 pts each = 25 max.

| Axis | Expected score (without skill) | Why |
|------|-------------------------------|-----|
| Factual accuracy | 1-2 / 5 | BLE version wrong, flash conflated, missing parts |
| Top-3 discipline | 1 / 5 | Use-case table is Top-1 per row, not Top-3 + compare |
| No fabrication | 1 / 5 | Inflated cells without "not verified" markers |
| Search priority | 0 / 5 | No tier / URL / date anywhere |
| Source citation | 0 / 5 | No source anchors at all |

**Expected total: 3-4 / 25.**

## How to verify the with-skill version is meaningfully better

The with-skill version should score ≥ 20 / 25 on the same rubric. The
delta (16+ points) is the skill's structural value-add — the model
itself doesn't change, only the constraints applied to its output.

## Maintenance

If you regenerate the baseline (newer LLM, different prompt seed,
etc.), update this file with the new canonical answer and adjust the
expected score in the table above. Newer LLMs may score higher on
"Factual accuracy" if they have been retrained with updated BLE SoC
data, but the structural axes (Top-3 discipline, search priority,
source citation) should remain near zero without the skill.