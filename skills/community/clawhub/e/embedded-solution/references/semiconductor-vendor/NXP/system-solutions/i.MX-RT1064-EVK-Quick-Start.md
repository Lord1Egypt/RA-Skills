# i.MX RT1064 EVK Quick Start

> **Source:** NXP-published MIMXRT1060-EVK evaluation kit getting-started
> guide. BOM is **NXP-only** (single-vendor). For multi-vendor teardown-
> derived solutions see `references/application-solution/`.

## Overview
An NXP-published evaluation kit guide for the i.MX RT1064 crossover MCU,
demonstrating out-of-box firmware bring-up, on-board accelerometer / push-
button use, and the MCUXpresso IDE / SDK debug flow.

- **Vendor:** NXP Semiconductors
- **Published as:** EVK Quick Start Guide + MCUXpresso SDK examples
- **Document type:** Eval kit guide (vendor-published)
- **EVK:** MIMXRT1060-EVK (formerly MIMXRT1064-EVK)
- **Date reviewed:** 2026-06-23

## Reference Design

- **Product page:** https://www.nxp.com/design/development-boards/i-mx-rt1064-evk (verification pending — link_status not yet verified)
- **Datasheet:** _not yet downloaded — fetch from vendor product page (see Main Page column above)_
- **YAML:** `specs/NXP/i.MX_RT1064.yaml` *(maintainer-only — not shipped in the public release; for verification use `references/semiconductor-vendor/NXP/product_families.md` and the datasheet)*

## BOM Candidates (NXP only)

| Function | Part | Datasheet | Notes |
|----------|------|-----------|-------|
| Crossover MCU | **i.MX RT1064** | [link](../product_families.md) | Cortex-M7 @ 600 MHz, no on-chip flash |
| EVK platform (only relevant for the example) | **MIMXRT1060-EVK** | NXP product page | On-board HyperFlash, DCDC, PMIC, MEMS sensors |

External to NXP (out of BOM scope for this single-vendor solution):
- USB-C cable (power + debug)
- Host PC with MCUXpresso IDE

## Reference Design Verification Status

- [ ] Original NXP product page URL HTTP 200 — **not yet verified**;
      link_status to be set after a fetch. Tavily/network access is
      the same Cloudflare-class risk noted in the Nordic nRF52 DK
      entry, so flag as `link_status: indirect` until direct fetch
      succeeds.
- [ ] Datasheet for i.MX RT1064 not yet downloaded. Run the
      skill's NXP datasheet fetcher once available, then cite it
      here instead of the placeholder.
- [ ] Confirm MIMXRT1060-EVK part number (NXP has rebranded some
      RT1064 SKUs as RT1060 EVK). Hero part remains i.MX RT1064.

## Numerical Specs

> Per the skill's no-fabrication policy, **no numerical parameters are
> written into this system-solution file**. The i.MX RT1064 spec values
> (clock, RAM, peripherals) live in the maintainer's private spec database (`specs/NXP/i.MX_RT1064.yaml`, if installed). A
> datasheet PDF is **not yet downloaded** — once present under
> `vendor product page`, the YAML should cite it explicitly.

## Source Discipline

- Original guide published by NXP on nxp.com.
- This entry only references NXP parts (single-vendor rule).
- If you want a multi-vendor teardown-derived solution that may include
  Renesas / TI / ST parts, see `references/application-solution/`.
