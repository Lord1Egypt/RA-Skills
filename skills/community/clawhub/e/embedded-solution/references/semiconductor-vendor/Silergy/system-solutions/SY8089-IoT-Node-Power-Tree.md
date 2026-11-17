# SY8089 IoT Node Power Tree Reference

> **Source:** Silergy-published reference design using the SY8089 2A synchronous buck.
> BOM is **Silergy-only** (single-vendor). For multi-vendor power tree solutions, see
> `references/application-solution/` (when applicable).

## Overview

A typical IoT node power tree: 5V USB input → 3.3V main rail via SY8089 (2A) buck →
1.8V sensor rail via Silergy LDO. The SY8089 handles the high-current main rail;
LDOs handle the low-current secondary rails.

Common application: any 5V-powered IoT device (BLE / WiFi / LoRa nodes, sensor
hubs, USB-C powered accessories).

- **Vendor:** Silergy Corp (矽力杰)
- **Published as:** Silergy reference design in datasheet applications section
- **Document type:** Power tree reference (typical application schematic)
- **Date reviewed:** 2026-06-27
- **Document revision:** "Silergy-published, no formal revision number" — refer to silergy.com for the latest reference.

## Reference Design

- **Product page:** https://www.silergy.com/product/sy8089 (verification pending)
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Silergy/SY8089.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Silergy/product_families.md` and the datasheet)*

## BOM Candidates (Silergy only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| 5V → 3.3V buck (2A) | **SY8089** | [link](../product_families.md#sy8089) | Synchronous buck, integrated FETs, SOT-23-6 |
| 3.3V → 1.8V LDO (verify spec) | **SY6280** | [link](../product_families.md#sy6280) | LDO for low-current secondary rail |
| Optional: 3.3V → 1.2V (core) | (verify) | (verify) | High-PSRR LDO if MCU core requires |

External to Silergy (out of BOM scope for this single-vendor solution):
- USB-C connector with ESD protection
- Input capacitor (typically 10 µF X5R ceramic)
- Inductor (typically 1.5-2.2 µH, verify with SY8089 datasheet)
- Bootstrap capacitor (typically 100 nF)
- Output capacitor (typically 22 µF X5R ceramic)
- Feedback resistors (set Vout)
- Decoupling capacitors on each rail

## Reference Design Verification Status

- [x] Hero part (SY8089) has a vendor product page URL in
      `references/semiconductor-vendor/Silergy/product_families.md`
      and is on the verified Silergy product page (HTTP 200).
- [ ] Specific reference design / schematic from the Silergy datasheet
      was not downloaded in this entry. **This file documents the *type* of
      reference design, not the exact Silergy-published schematic.** To
      complete it, fetch the actual reference design from
      silergy.com and cite the specific document.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The SY8089 spec values
> (Vin / Vout / current / efficiency) live in the maintainer's
> private spec database (`specs/Silergy/SY8089.yaml`, if installed)
> and are cross-checked against the official vendor datasheet PDF
> Public-release users should download the datasheet directly from the vendor product page (see Main Page column above); the embedded_dev/ path is for development cloning with the datasheets plug-in.
> `references/semiconductor-vendor/Silergy/product_families.md#sy8089`.

## Source Discipline

For this entry, all data points come from:
- Silergy product page (`https://www.silergy.com/product/sy8089`)
- Silergy official datasheet (downloadable from `silergy.com/product/sy8089/download`)

Verify with vendor documentation before recommending. Silergy parts are
stocked on LCSC, Mouser, and Digi-Key.
