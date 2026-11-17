# Smart Glasses (Third-party teardowns / cross-vendor)

> **Source class:** Third-party teardowns, online component marketplaces,
> and engineer community schematics. The BOMs here are not endorsed by any
> single chip vendor — they reflect what has actually been observed in
> shipped products or what is being sold as a turnkey reference design by
> a third party. For a single-vendor reference design, see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
Smart glasses for AR/assistive-reality, audio playback, camera input, and
heads-up notifications, as commonly observed in third-party teardowns and
multi-vendor reference designs. Generic, vendor-neutral requirements:

- **Mid-tier processing**: Cortex-M4/M33 minimum, optional Cortex-A for full AR.
- **Wireless**: BLE mandatory; WiFi optional for high-bandwidth data sync.
- **Audio**: BT audio (A2DP) or wired; small speaker/AMOLED driver.
- **Display**: optional micro-display (OLED or LCoS) + display driver.
- **Camera**: optional, low-MP sensor with MIPI-CSI.

Constraints:
- Battery powered (200–500 mAh typical).
- Lightweight < 50 g frame weight.
- Cost: < $50 BOM for audio-only, < $150 BOM for AR-display variant.

## BOM Candidates (multi-vendor, third-party observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| BLE SoC (audio glasses) | **DA14697** | Renesas | High-end SmartBond, BLE 5.x, audio codec interface. Common in hearables/audio wearable teardowns. | [link](../../semiconductor-vendor/Renesas/product_families.md#da14697) |
| BLE SoC (alt, multiprotocol) | **nRF5340** | Nordic | Dual-core M33, BLE 5.1/Matter/Thread, audio via PDM/I2S. | [link](../../semiconductor-vendor/Nordic/product_families.md#nrf5340) |
| BLE SoC (alt, multiprotocol) | **CC2652R** | TI | Cortex-M4F, multi-protocol (BLE/Thread/Zigbee/Matter), audio. | [link](../../semiconductor-vendor/TI/product_families.md#cc2652r) |
| High-end MPU (AR variant) | **i.MX RT1170** | NXP | Dual-core M7+M4, 1 GHz capable, MIPI-CSI/DSI for camera + display. | [link](../../semiconductor-vendor/NXP/product_families.md#i-mx-rt1170) |
| High-end MPU (alt) | **STM32MP157** | ST | Cortex-A7 + Cortex-M4, Linux capable for full AR stack. | [link](../../semiconductor-vendor/ST/product_families.md#stmp32mp157) |
| Pressure sensor (altitude / weather) | **PTX30W** | Renesas | Optional altimeter for outdoor AR applications. | [link](../../semiconductor-vendor/Renesas/product_families.md#ptx30w) |

External (not catalogued in this skill):
- Micro-display panels (LCoS, micro-OLED) — eMagin, Sony, JBD
- Camera modules (MIPI-CSI) — OmniVision, Sony
- Audio codecs — Cirrus Logic, Qualcomm
- PMIC / battery management for high-current displays

## Third-party Sources (to be expanded as data is collected)

- (pending) Teardown reports of Ray-Ban Meta, Even Realities G1, Brilliant Labs Frame
- (pending) Component-marketplace listings for "smart glasses reference design"
- (pending) Engineer community posts (EEVblog, hackaday, Reddit r/AR_MR)

## Reference Designs

> This section lists **single-vendor** reference designs from chip
> vendors' own websites, included here for completeness. For the full
> single-vendor version of a given solution, see
> `references/semiconductor-vendor/<Vendor>/system-solutions/`.

- Renesas DA14697 product page: https://www.renesas.com/da14697 (✅ verified)
- Nordic nRF5340 product page: https://www.nordicsemi.com/Products/nRF5340 (✅ verified 2026-06-21)
- TI CC2652R product page: https://www.ti.com/product/CC2652R (⏳ verification pending — Cloudflare gated)
- NXP i.MX RT1170 product page: https://www.nxp.com/products/i.MX-RT1170 (⏳ verification pending — main page 404; NXP Community mirror used for datasheet)
- ST STM32MP157 product page: https://www.st.com/en/microcontrollers-microprocessors/stm32mp1-series.html (⏳ verification pending — Cloudflare gated)

## Selection Matrix (third-party / community perspective)

| Criterion | DA14697 (Renesas) | nRF5340 (Nordic) | CC2652R (TI) | i.MX RT1170 (NXP) | STM32MP157 (ST) |
|-----------|-------------------|-------------------|----------------|-------------------|------------------|
| Form factor | BLE SoC | BLE SoC | BLE SoC | MPU (M7+M4) | MPU (A7+M4) |
| Cores | M33 app + M0+ radio | M33 @ 128 MHz TZ | M4 | M7 + M4 | A7 + M4 |
| Max clock | 96 MHz (app) | 128 MHz (app core) | not extracted | 1000 MHz | not extracted |
| Flash | external QSPI | 256 kB | not extracted | not extracted | not extracted |
| RAM | cache-based | 256 kB | 80 kB | 768 KB | not extracted |
| BLE | 5.2 | 5.2 | 5.2 | ❌ (no radio) | ❌ (no radio) |
| WiFi | ❌ | ❌ | ❌ | via companion chip | via companion chip |
| Standby current | not extracted | not extracted | **0.94 µA** | not extracted | not extracted |
| Shutdown current | not extracted | not extracted | **150 nA** | not extracted | not extracted |
| RX sensitivity | -97 dBm | -98 dBm | not extracted | n/a | n/a |
| TX power | +6 dBm | not extracted | not extracted | n/a | n/a |
| CoreMark | not extracted | 514 | not extracted | not extracted | not extracted |
| Camera (MIPI-CSI) | ❌ | ❌ | ❌ | ✅ | ✅ |
| Display (MIPI-DSI) | ❌ | ❌ | ❌ | ✅ | ✅ |
| Linux capable | ❌ | ❌ | ❌ | ❌ (RTOS only) | ✅ |

## Verification Status

- [x] All BOM parts have a vendor product page URL in
      `references/semiconductor-vendor/<Vendor>/product_families.md`
      or are noted as external.
- [x] **DA14697**: 9+ spec fields populated (cores / BLE / flash / RAM
      caveat / TX power / RX sensitivity / link budget). Manually extracted
      2026-06-20.
- [x] **nRF5340**: 7 spec fields (cores / flash / RAM / BLE / vcc /
      coremark / RX sensitivity). Auto-extracted 2026-06-25.
- [x] **CC2652R**: 5 spec fields (BLE / RAM / cores / standby / shutdown).
      Auto-extracted 2026-06-23.
- [x] **i.MX RT1170**: 3 spec fields (cores / max clock / RAM). NXP
      Community mirror used (nxp.com /docs/ URL was 404).
- [ ] **STM32MP157**: spec YAML is empty. ST datasheet is Cloudflare-gated
      from st.com; can't auto-extract until network access to st.com is
      available.
- [ ] At least one actual third-party source URL must be added to the
      "Third-party Sources" section.
- [ ] For AR variant: verify MIPI-CSI/DSI lane counts vs target camera/display.
- [ ] Audio variant: verify PDM/I2S clock rates vs chosen audio codec.

## Caveat

This file is a **framework for collecting multi-vendor smart-glasses BOMs**
as observed in real-world designs. Two distinct sub-applications are
covered: (a) audio-only smart glasses, and (b) AR-display smart glasses.
They share the audio path but diverge on the MPU and display.

The BLE SoC selection (DA14697 / nRF5340 / CC2652R) is interchangeable for
the audio variant; the actual choice should be driven by **vendor support
for the specific audio codec** chosen (not analysed in this skill yet).

The AR variant's MPU choice (i.MX RT1170 vs STM32MP157) is dominated by
the software stack: bare-metal/RTOS favors RT1170, Linux favors MP157.

For single-vendor reference designs, see each vendor's `system-solutions/`.

Re-run `scripts/build_application_index.py` after populating YAMLs to
refresh INDEX.md.
