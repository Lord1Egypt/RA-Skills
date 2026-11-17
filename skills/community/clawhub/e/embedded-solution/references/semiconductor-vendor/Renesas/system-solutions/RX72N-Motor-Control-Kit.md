# RX72N Motor Control Kit

> **Source:** Renesas-published RX72N motor-control reference design
> using the 32-bit RXv3 core with single-precision FPU and a Renesas
> motor-control inverter board. BOM is **Renesas-only**
> (single-vendor).

## Overview
A Renesas-published reference design for high-end industrial motor
control (FOC + PFC) on the RX72N MCU, paired with a Renesas-branded
inverter board and Renesas Motor Workbench.

- **Vendor:** Renesas Electronics
- **Published as:** Application Note + RX72N motor-control example
  (Renesas Motor Workbench)
- **Document type:** Reference design (pro-forma BOM + inverter
  topology)
- **EVK:** RX72N Renesas Solution Starter Kit (RSK) + Renesas
  Motor Workbench inverter daughter-board
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.renesas.com/en/products/microcontrollers-microprocessors/rx-32-bit-performance-efficiency-mcus/rx72n-microcontrollers (verification pending)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Renesas/RX72N.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Renesas/product_families.md` and the datasheet)*

## BOM Candidates (Renesas only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| 32-bit RXv3 MCU with FPU | **RX72N** | [link](../product_families.md#rx72n) | Cortex-class perf with RXv3 core, FPU, TFU |
| EVK platform | **RX72N RSK + Motor Workbench inverter** | Renesas product page | On-board J-Link, Renesas-branded inverter stage |

External to Renesas (out of BOM scope for this single-vendor solution):
- 3-phase PMSM / induction motor, USB cable, host PC

## Reference Design Verification Status

- [ ] Original Renesas product page URL HTTP 200 — verification pending.
- [x] Datasheet already present at
      product page → Documents & Downloads.
- [ ] Confirm the exact RX72N SKU (R5F572N / R5F572M — these differ
      on flash, RAM, and crypto accelerators).
- [ ] Confirm whether the cited design uses **RX72N** as standalone
      controller or as **master + RXv3 helper**. Some Renesas motor
      control kits use **dual-RX** configurations.
- [ ] Pin the inverter daughter-board model number — the BOM depends
      on which Renesas Motor Workbench kit is cited.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The RX72N spec values
> live in the maintainer's private spec database (`specs/Renesas/RX72N.yaml`, if installed) and are cited to the datasheet
> PDF under product page → Documents & Downloads.
> See that YAML for verified values.

## Source Discipline

- Original reference design published by Renesas on renesas.com.
- This entry only references Renesas parts (single-vendor rule).
- For multi-vendor teardowns, see `references/application-solution/`.
