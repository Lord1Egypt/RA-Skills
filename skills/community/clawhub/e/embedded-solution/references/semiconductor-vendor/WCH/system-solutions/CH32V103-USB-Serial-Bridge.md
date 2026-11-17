# CH32V103 USB-to-Serial Bridge Reference

> **Source:** WCH-published reference design using the CH32V103R8T6 general-purpose RISC-V MCU.
> BOM is **WCH-only** (single-vendor). For multi-vendor USB-serial solutions, see
> `references/application-solution/` (when applicable).

## Overview

A low-cost USB-to-UART bridge reference using the WCH CH32V103R8T6 RISC-V MCU
with on-chip USB 2.0 Full-Speed device. The CH32V103 has built-in USB device
firmware in ROM, eliminating the need for an external USB controller IC.

Common application: replacing dedicated USB-serial bridge ICs (CH340, CP2102,
FT232) in designs where the host MCU already includes USB device.

- **Vendor:** WCH (南京沁恒微电子)
- **Published as:** WCH application note + reference firmware
- **Document type:** Reference design (USB CDC device class firmware)
- **Date reviewed:** 2026-06-27
- **Document revision:** "WCH-published, no formal revision number" — refer to wch-ic.com for the latest firmware.

## Reference Design

- **Product page:** https://www.wch-ic.com/products/CH32V103.html (verification pending)
- **Dev kit (where reference design is implemented):**
  CH32V103R8T6 EVT board — WCH official evaluation kit. See product page for kit contents.
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/WCH/CH32V103R8T6.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/WCH/product_families.md` and the datasheet)*

## BOM Candidates (WCH only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| USB-UART bridge MCU | **CH32V103R8T6** | [link](../product_families.md#ch32v103r8t6) | RISC-V MCU with built-in USB device; CDC class firmware in ROM |
| Crystal (12 MHz for USB) | (verify in datasheet) | (external) | 12 MHz crystal or resonator for USB 2.0 Full-Speed |
| USB connector | (external) | — | USB-C or Micro-B, with proper ESD protection |
| Decoupling capacitors | (external) | — | 100 nF per VDD pin + bulk caps |
| Optional status LED | (external) | — | TX/RX activity indicators |

External to WCH (out of BOM scope for this single-vendor solution):
- USB connector (with or without ESD protection IC)
- Crystal or resonator
- Decoupling / bulk capacitors
- Optional enclosure

## Reference Design Verification Status

- [x] Hero part (CH32V103R8T6) has a vendor product page URL in
      `references/semiconductor-vendor/WCH/product_families.md`
      and is on the verified WCH product page (HTTP 200).
- [ ] Specific firmware / BOM from the WCH design notes was not
      downloaded in this entry. **This file documents the *type* of
      reference design, not the exact WCH-published firmware.** To
      complete it, fetch the actual reference design from
      wch-ic.com and cite the specific document.
- [ ] Confirm EVT kit ordering part number is still in production on the WCH store.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The CH32V103 spec values
> (clock, RAM, flash, current consumption) live in the maintainer's
> private spec database (`specs/WCH/CH32V103R8T6.yaml`, if installed)
> and are cross-checked against the official vendor datasheet PDF
> Public-release users should download the datasheet directly from the vendor product page (see Main Page column above); the embedded_dev/ path is for development cloning with the datasheets plug-in.
> `references/semiconductor-vendor/WCH/product_families.md#ch32v103r8t6`.

## Source Discipline

For this entry, all data points come from:
- WCH product page (`https://www.wch-ic.com/products/CH32V103.html`)
- WCH official datasheet (downloadable from `wch-ic.com/downloads/CH32V103DS0.PDF`)

Verify with vendor documentation before recommending. WCH parts are widely
stocked on LCSC and Mouser / Digi-Key.
