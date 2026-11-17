# Robot Gripper (Third-party teardowns / cross-vendor)

> **Source class:** Third-party teardowns of industrial cobots / robotic
> grippers, online component marketplaces, and engineer community
> schematics. The BOMs here are not endorsed by any single chip vendor —
> they reflect what has actually been observed in shipped products or what
> is being sold as a turnkey reference design by a third party. For a
> single-vendor reference design, see
> `references/semiconductor-vendor/<Vendor>/system-solutions/` instead.

## Overview
A dexterous robot gripper / end-effector for collaborative robots (cobots),
as commonly observed in third-party teardowns and multi-vendor reference
designs. Generic, vendor-neutral requirements:

- **Deterministic motor control**: real-time MCU with hardware PWM + encoder.
- **Force / torque feedback**: ADC front-end for strain-gauge bridge.
- **Position sensing**: inductive or magnetic encoder per joint.
- **Safety**: dual-channel or watchdog, IEC 61508 SIL considerations.
- **Communication**: CAN-FD (typical cobot bus) or EtherCAT.

Constraints:
- Wired power (24 V typical) or battery for mobile manipulators.
- Cost: $50–$300 per gripper channel.
- Industrial temperature: -10 to +60 °C.

## BOM Candidates (multi-vendor, third-party observed)

| Function | Part | Vendor | Why this part appears | Datasheet |
|----------|------|--------|-----------------------|-----------|
| Motor control MCU | **RX72N** | Renesas | 32-bit RXv3, large RAM, Ethernet, hardware PWM — long heritage in motor control designs. | [link](../../semiconductor-vendor/Renesas/product_families.md#rx72n) |
| Motor control MCU (alt, high-end) | **i.MX RT1170** | NXP | Dual-core M7+M4, 1 GHz — if advanced model-based control is needed. | [link](../../semiconductor-vendor/NXP/product_families.md#i-mx-rt1170) |
| Motor control MCU (alt) | **STM32H7** | ST | Cortex-M7, 550 MHz, DSP/AI, STM32 motor-control SDK. | [link](../../semiconductor-vendor/ST/product_families.md#stm32h7) |
| Inductive position sensor | **RL78I1D** | Renesas | Purpose-built for inductive position sensing. | [link](../../semiconductor-vendor/Renesas/product_families.md#rl78i1d) |
| General-purpose MCU (sensor hub) | **RA6M5** | Renesas | Cortex-M33, dual-bank flash, Ethernet + CAN-FD — popular for supervisory sensor hubs. | [link](../../semiconductor-vendor/Renesas/product_families.md#ra6m5) |
| Secure MCU (alt) | **LPC55S69** | NXP | Cortex-M33, TrustZone + CASPER crypto — for secure boot / OTA. | [link](../../semiconductor-vendor/NXP/product_families.md#lpc55s69) |
| Low-cost MCU (cost-sensitive) | **MSPM0G3507** | TI | Cortex-M0+, low cost — for simple on-joint control. | [link](../../semiconductor-vendor/TI/product_families.md#mspm0g3507) |
| Battery / system supervisor | **ISL88705** | Renesas | µP supervisor + watchdog. | [link](../../semiconductor-vendor/Renesas/product_families.md#isl88705) |
| DC/DC buck (motor rail) | **ISL9305** | Renesas | Dual step-down mini-PMIC, suited for system rails. | [link](../../semiconductor-vendor/Renesas/product_families.md#isl9305) |

External (not catalogued in this skill):
- Force / torque sensor front-end (strain gauge + instrumentation amp) —
  application-specific
- Motor drivers / gate drivers — depends on motor type (BLDC, stepper, etc.)
- Magnetic encoder ICs (e.g. AS5048, MA730) — typically separate from MCU

## Third-party Sources (to be expanded as data is collected)

- (pending) Teardown reports of OnRobot, Robotiq, Schunk, DH-Robotics grippers
- (pending) Component-marketplace listings for "cobot gripper controller board"
- (pending) Engineer community posts on cobot-build forums
- (pending) IEEE / MDPI Robotics papers on gripper controller hardware

## Reference Designs

> This section lists **single-vendor** reference designs from chip
> vendors' own websites, included here for completeness. For the full
> single-vendor version of a given solution, see
> `references/semiconductor-vendor/<Vendor>/system-solutions/`.

- Renesas RX72N product page: https://www.renesas.com/rx72n (✅ verified)
- Renesas RL78I1D product page: https://www.renesas.com/rl78i1d (✅ verified)
- NXP i.MX RT1170 product page: https://www.nxp.com/products/i.MX-RT1170 (⏳ verification pending)
- ST STM32H7 product page: https://www.st.com/en/microcontrollers-microprocessors/stm32h7-series.html (⏳ verification pending)
- TI MSPM0G3507 product page: https://www.ti.com/product/MSPM0G3507 (⏳ verification pending)

## Selection Matrix (third-party / community perspective)

| Criterion | RX72N (Renesas) | i.MX RT1170 (NXP) | STM32H7 (ST) | MSPM0G3507 (TI) |
|-----------|-----------------|-------------------|--------------|-------------------|
| Core | RXv3 (proprietary) | M7+M4 dual | M7 | M0+ |
| Max freq | not extracted | not extracted | not extracted | not extracted |
| Hardware PWM | ✅ | ✅ | ✅ | ✅ |
| CAN-FD | ✅ | ✅ | ✅ | ❌ |
| Ethernet | ✅ | ✅ | ✅ | ❌ |
| Floating-point | ✅ | ✅ (FPU) | ✅ (FPU) | ❌ |
| Industrial temp grade | ✅ | ✅ | ✅ | ❌ (consumer) |
| **Numeric specs** | **not extracted** | **not extracted** | **not extracted** | **not extracted** |

## Verification Status

- [x] All BOM parts have a vendor product page URL in
      `references/semiconductor-vendor/<Vendor>/product_families.md`.
- [ ] **All numerical specs must be verified against the actual datasheet
      tables before recommending.**
- [ ] At least one actual third-party source URL must be added to the
      "Third-party Sources" section.
- [ ] Confirm RX72N's PWM resolution vs required torque ripple spec.
- [ ] Confirm CAN-FD timing on the chosen bus topology.
- [ ] For safety certification: confirm RL78I1D's diagnostic coverage meets
      the SIL target (out of skill scope).

## Caveat

This file is a **framework for collecting multi-vendor robot-gripper BOMs**
as observed in real-world designs. It does not yet contain any teardown
evidence. The "Why this part appears" columns are placeholders for adding
source citations.

Robot-gripper designs often use **multiple** of these chips in a
hierarchical topology (one supervisory MCU + N per-joint microcontrollers).
The BOM above lists the building blocks, not the full hierarchy.

For single-vendor reference designs (e.g. Renesas' own RX72N motor-control
kit), see `references/semiconductor-vendor/Renesas/system-solutions/`.

Re-run `scripts/build_application_index.py` after populating YAMLs to
refresh INDEX.md.
