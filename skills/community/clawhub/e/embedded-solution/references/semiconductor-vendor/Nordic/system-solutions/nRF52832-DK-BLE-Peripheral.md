# nRF52832 DK BLE Peripheral Example

> **Source:** Nordic Semiconductor-published nRF5 SDK example, run on
> the official nRF52 DK development kit. BOM is **Nordic-only**
> (single-vendor). For multi-vendor BLE beacon / peripheral solutions
> derived from third-party teardowns, see
> `references/application-solution/ble-beacon/solution.md` instead.

## Overview
A Nordic-published SDK example demonstrating a standard BLE peripheral
role (advertising, GATT service exposure, connection state handling) on
the nRF52832 SoC, using the nRF52 DK as the development platform.

- **Vendor:** Nordic Semiconductor
- **Published as:** `nRF5 SDK` (or `nRF Connect SDK`) example
  `samples/bluetooth/peripheral` (or `examples/ble_peripheral` in
  nRF5 SDK)
- **Document type:** SDK example (source code + readme)
- **Dev kit:** nRF52 DK (PCA10040) — Nordic's official dev kit for the
  nRF52832 SoC
- **Date reviewed:** 2026-06-21

## Reference Design

- **Dev kit page:** https://www.nordicsemi.com/Products/Development-hardware/nRF52-DK/GetStarted
  (Tavily-cross-checked; nordicsemi.com is Cloudflare-protected for
  direct fetch, but the dev kit page is referenced in Nordic's SDK
  documentation and Q&A threads)
- **SoC product page:** https://www.nordicsemi.com/Products/nRF52832
  (✅ verified via Tavily)
- **SDK location (typical):** `nrf5sdk/examples/ble_peripheral/ble_app_peripheral/`
  or in nRF Connect SDK `samples/bluetooth/peripheral/`
- **YAML:** `specs/Nordic/nRF52832.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/Nordic/product_families.md` and the datasheet)*

## BOM Candidates (Nordic only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| BLE SoC | **nRF52832** | [link](../product_families.md#nrf52832) | Cortex-M4, BLE 5, multiprotocol; 512KB flash / 64KB RAM |
| Dev kit platform (only relevant for the example) | **nRF52 DK (PCA10040)** | nRF52 DK product page | Nordic's official DK; on-board J-Link OB debugger |

External to Nordic (out of BOM scope for this single-vendor solution):
- USB cable (for power / programming)
- Host PC with nRF Connect for Desktop
- Smartphone or peer BLE device for testing

## Reference Design Verification Status

- [x] Hero part (nRF52832) has a vendor product page URL in `references/semiconductor-vendor/Nordic/product_families.md` and
      is referenced from Nordic's product page (Tavily-verified).
- [ ] nRF52 DK product page is Cloudflare-blocked for direct fetch but
      cross-confirmed via Nordic's Q&A forum (devzone.nordicsemi.com) and
      the SDK install paths. **Mark as `link_status: indirect` until
      a non-Cloudflare fetch is possible.**
- [ ] Specific SDK example path differs between nRF5 SDK and nRF Connect
      SDK — verify which SDK is in use before citing example source code.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The nRF52832 spec values
> live in the maintainer's private spec database (`specs/Nordic/nRF52832.yaml`, if installed) and are cited to the datasheet
> PDF under product page → Documents & Downloads.
> See that YAML for verified values.

## Source Discipline

- Original example published by Nordic on nordicsemi.com / in Nordic
  SDK repositories.
- This entry only references Nordic parts (single-vendor rule).
- If you want a multi-vendor teardown-derived BLE peripheral BOM (which
  may include TI / ST / Renesas parts), see
  `references/application-solution/ble-beacon/solution.md` instead.
