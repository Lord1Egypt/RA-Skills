# DA14531 BLE Beacon Reference

> **Source:** Renesas-published reference design for the DA14531 SmartBond
> TINY™ Bluetooth 5.1 SoC. BOM is **Renesas-only** (single-vendor).
> For multi-vendor BLE beacon solutions derived from third-party teardowns,
> see `references/application-solution/ble-beacon/solution.md` instead.

## Overview
A Renesas-published reference design demonstrating a sub-1 mA active BLE
beacon node based on the DA14531 SmartBond TINY. Intended as a starting
point for coin-cell powered asset tracking, retail beacons, and
find-my-device applications.

- **Vendor:** Renesas Electronics
- **Published as:** Part of the DA14531 product family documentation set
  (linked from https://www.renesas.com/en/products/da14531)
- **Document type:** Reference design (pro-forma BOM, suggested peripherals)
- **Date reviewed:** 2026-06-21
- **Document revision:** "renesas-published, no formal revision number" —
  refer to renesas.com for the latest design notes.

## Reference Design

- **Product page:** https://www.renesas.com/en/products/da14531 (✅ verified 2026-06-21)
- **Dev kit (where reference design is implemented):**
  DA14531MOD-00DEVKT-P — SmartBond TINY Development Kit Pro (includes
  motherboard + daughterboard + cables for the DA14531 module).
  See product page for kit contents.
- **Datasheet:** product page → Documents & Downloads
- **YAML:** `specs/Renesas/DA14531.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Renesas/product_families.md` and the datasheet)*

## BOM Candidates (Renesas only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| BLE SoC | **DA14531** | [link](../product_families.md#da14531) | SmartBond TINY, BLE 5.1, Cortex-M0+, OTP, integrated DC-DC |
| Battery charger (optional) | **ISL9205** | [link](../product_families.md#isl9205) | Single-cell Li-ion linear charger, DFN-10 / QFN-16 |
| Temperature/humidity sensor (optional, application-dependent) | **HS3001** ⚠️ | [link](../product_families.md#hs3001) | RH/T sensor. **Marked Obsolete on the Renesas product page (verified 2026-06-21) — do not use for new designs; consider a drop-in replacement or omit for coin-cell beacon.** |

External to Renesas (out of BOM scope for this single-vendor solution):
- Coin-cell battery (CR2032 typically) and holder
- PCB antenna or chip antenna
- Decoupling capacitors, pull-ups, optional reset circuit

## Reference Design Verification Status

- [x] Hero part (DA14531) has a vendor product page URL in `references/semiconductor-vendor/Renesas/product_families.md` and is
      on the verified Renesas product page (HTTP 200).
- [x] ISL9205 / HS3001 reference parts have vendor product page URLs in `references/semiconductor-vendor/Renesas/product_families.md` and are
      on the verified Renesas product pages.
- [ ] Specific schematic / BOM from the Renesas design notes was not
      downloaded in this entry. **This file documents the *type* of
      reference design, not the exact Renesas-published schematic.** To
      complete it, fetch the actual reference design PDF from
      renesas.com and cite the specific document.
- [ ] Confirm DevKit Pro ordering part number
      (DA14531MOD-00DEVKT-P) is still in production on Renesas store.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The DA14531 spec values
> (BLE version, RAM, flash, current consumption) live in
> `specs/Renesas/DA14531.yaml` (maintainer's private spec database, not shipped in public release) and are cited to the datasheet PDF under
> `vendor product page`. See that YAML for verified values.

## Source Discipline

- Original reference design published by Renesas on renesas.com.
- This entry only references Renesas parts (single-vendor rule).
- If you want a multi-vendor teardown-derived BLE beacon BOM (which
  may include Nordic / TI / ST parts), see
  `references/application-solution/ble-beacon/solution.md` instead.
