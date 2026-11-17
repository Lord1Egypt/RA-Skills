# Silicon Labs Product Families Reference

> **v0.4.0+ Status (2026-06-30):** Several yaml entries in
> `specs/<VENDOR>/*.yaml` are tagged
> `link_status: pending-datasheet-2026-06-30 (no-PDF-yet; family-page-extract only)`.
> These are sourced from vendor product page markdown via Firecrawl, not from
> a downloaded datasheet PDF. Treat their spec values as APPROXIMATE /
> MARKETING-LEVEL until cross-validated against the datasheet. See
> `VERIFICATION.md` at repo root for the full v0.4.0+ verification policy.
> This note supersedes the legacy ⚠️ IMPORTANT — Data Verification Policy below
> for any yaml created in the v0.4.0+ era (2026-06-29 onwards).


> **⚠️ IMPORTANT — Data Verification Policy**
>
> This reference file ONLY contains **parts whose Silicon Labs product page is reachable** (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When a Silicon Labs part is recommended, the agent MUST:
> 1. Open the verified link below to confirm the part still exists.
> 2. From the vendor product page, navigate to "Documents & Downloads" and download the latest datasheet PDF.
> 3. Extract every numerical parameter with `pdfplumber` and cite the table/page.
> 4. NEVER transcribe numbers from this file into a response — they are not authoritative.

## Link Verification Status

| Status | Meaning |
|--------|---------|
| ✅ | Main page returns HTTP 200 |
| ❌ | Main page returns 404 — part has been removed, renamed, or relocated. Do NOT use. |
| ⏳ | Not yet verified. Use only after a manual HTTP 200 check. |

---

## EFR32BG Series (Bluetooth Low Energy SoC, Cortex-M33)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **EFR32BG22** | ⏳ | https://www.silabs.com/wireless/bluetooth/efr32bg22-series-2-socs | product page → Documents & Downloads |
| **EFR32BG24** | ⏳ | https://www.silabs.com/wireless/bluetooth/efr32bg24-series-2-socs | product page → Documents & Downloads |

## EFR32MG Series (Multi-protocol SoC, Cortex-M33)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **EFR32MG21** | ⏳ | https://www.silabs.com/wireless/zigbee/efr32mg21-series-2-socs | product page → Documents & Downloads |
| **EFR32MG24** | ⏳ | https://www.silabs.com/wireless/zigbee/efr32mg24-series-2-socs | product page → Documents & Downloads |

---

## Family Hub Pages (Verification Pending)

- **EFR32 Series 2 (all)**: https://www.silabs.com/wireless/wireless-mcu
- **Bluetooth SoCs**: https://www.silabs.com/wireless/bluetooth
- **Zigbee / Thread / Matter SoCs**: https://www.silabs.com/wireless/zigbee
- **Modules (BGM, MGM, etc.)**: https://www.silabs.com/wireless/wireless-modules

## Verification Notes (Round 1, 2026-06-26)

| Part | Verified Source | Notes |
|------|----------------|-------|
| EFR32BG22 | alcom.be mirror (`https://alcom.be/uploads/efr32bg22-datasheet.pdf`) | 101 pages, 1.4 MB. Cloudflare-gated silabs.com serves same PDF. |
| EFR32BG24 | alcom.be mirror (`https://alcom.be/uploads/efr32bg24-datasheet.pdf`) | 118 pages, 1.9 MB. |
| EFR32MG21 | alcom.be mirror (`https://alcom.be/uploads/Silicon-Labs-efr32mg21-datasheet.pdf`) | 76 pages, 1.5 MB. |
| EFR32MG24 | alcom.be mirror (`https://alcom.be/uploads/Silicon-Labs-efr32mg24-datasheet.pdf`) | 132 pages, 2.4 MB. |

All four EFR32 Series 2 datasheets verified reachable via the
**Alcom** European distributor mirror (alcom.be / alcom.nl).
`silabs.com` is Cloudflare-gated from this environment; we document
alcom as the canonical mirror for these parts.

## Application Notes

- **Cortex-M33 core**: ARMv8-M TrustZone mainline, FPU, DSP.
- **Series 2 radios**: 2.4 GHz proprietary / IEEE 802.15.4 / Bluetooth 5.x / Matter / Thread / Zigbee (per family).
- **Secure Vault**: hardware root-of-trust, secure boot, secure debug; "Mid" or "High" tier depending on OPN.
- **AI/ML accelerator (MVP)**: present on Series 2 devices (BG24/MG24) but not BG22.


## EFR32BG27 Series — next-gen Series 2 BLE SoC

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **EFR32BG27** | ⏳ | https://www.silabs.com/wireless/bluetooth/efr32bg27-series-2-socs | product page → Documents & Downloads |

---

## Status Notes

- **2026-06-29 v0.4.0 firecrawl pass + silabs/ consolidation**:
  Consolidated duplicate silabs/ and siliconlabs/ datasheet directories under the canonical silabs/ path.
  directories had EFR32BG22/24/27, EFR32MG21/24 datasheets; 2 PDFs were
  identical (BG22, BG27) and 3 differed in size (BG24, MG21, MG24) —
  the `silabs/` versions were preserved as the authoritative source
  (referenced by `specs/SiliconLabs/*.yaml` which had been populated
  via the alcom.be mirror route on 2026-06-28).
    - Updated: 5 system-solutions templates (`references/.../system-solutions/*.md`)
    to reference `silabs/datasheet/` instead of `siliconlabs/datasheet/`.
  - No specs yaml changes needed — already pointed to `silabs/`.
- No firecrawl scrape performed for SiliconLabs product pages (silabs.com
  Cloudflare-gated per v0.4.0 plan; alcom.be mirrors used for yaml specs).
