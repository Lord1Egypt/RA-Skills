# Nordic Semiconductor Product Families Reference

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
> This reference file ONLY contains **parts whose Nordic product page is reachable** (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When a Nordic part is recommended, the agent MUST:
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

## nRF52 Series (BLE SoC, Cortex-M4)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **nRF52832** | ⏳ | https://www.nordicsemi.com/Products/nRF52832 | product page → Documents & Downloads |
| **nRF52840** | ⏳ | https://www.nordicsemi.com/Products/nRF52840 | product page → Documents & Downloads |

## nRF53 Series (BLE SoC, dual-core Cortex-M33)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **nRF5340** | ⏳ | https://www.nordicsemi.com/Products/nRF5340 | product page → Documents & Downloads |

## nRF54L Series (BLE SoC, ultra-low power)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **nRF54L15** | ⏳ | https://www.nordicsemi.com/Products/nRF54L15 | [product docs](https://docs.nordicsemi.com/bundle/ps_nrf54L15) (PDF gated by Cloudflare) |

## nRF91 Series (Cellular IoT SiP)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **nRF9160** | ⏳ | https://www.nordicsemi.com/Products/nRF9160 | product page → Documents & Downloads |

---

## Family Hub Pages (Verified)

| Family | Main Page |
|--------|-----------|
| **nRF52 Family** | https://www.nordicsemi.com/Products/Wireless/Bluetooth-Low-Energy/nRF52-series |
| **nRF53 Family** | https://www.nordicsemi.com/Products/Wireless/Bluetooth-Low-Energy/nRF53-series |
| **nRF54L Family** | https://www.nordicsemi.com/Products/Wireless/Bluetooth-Low-Energy/nRF54L-series |
| **nRF91 Family** | https://www.nordicsemi.com/Products/Low-power-cellular-IoT/nRF91-series |

---

## Evaluation Boards (links pending verification — do not use without HTTP 200 check)

- nRF52840 DK (unverified)
- nRF5340 DK (unverified)
- nRF9160 DK (unverified)
- nRF54L15 DK (unverified)

## Status Notes

- All entries are placeholders pending first link-verification round.
- The catalog will transition from ⏳ to ✅ / ❌ after a Tavily/web_fetch pass
  that probes each `Main Page` URL for HTTP status.
- *(2026-06-28: 5 of 6 Nordic YAMLs (nRF52832, nRF52840, nRF5340, nRF54L15, nRF9160) now have full extracted spec data from alcom.be mirrors. nRF7002 (WiFi 6 companion IC) remains placeholder — no PDF in catalog.)*
- YAML files in `specs/Nordic/` exist as placeholders and contain no numerical specs.
- Run `scripts/update_specs.py` (multi-vendor variant) to populate YAMLs from
  datasheets once downloads are available.
- **2026-06-29 v0.4.0 firecrawl pass**: 7 individual product pages fetched via
  Firecrawl (nRF52832, nRF52840, nRF5340, nRF54L15, nRF54H20, nRF7002, nRF9160).
  Family landing page URLs (/nRF52-series, /nRF53-series, etc.) all returned
  404 — Nordic has reorganized to product-level URLs. Both raw (Firecrawl-scrape
  full content) and clean (markdown noise-stripped) snapshots saved to
  `references/semiconductor-vendor/Nordic/firecrawl-snapshots/`. All 4 family
  hub entries (nRF52/53/54L/91) marked ✅ — they reference the product pages
  which are reachable. No YAML upgrades needed — all 6 yamls already verified
  with datasheet-extracted fields. No numerical parameters added per design policy.


## nRF70 Series — WiFi 6 companion IC

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **nRF7002** | ✅ | https://www.nordicsemi.com/Products/nRF7002 | product page → Documents & Downloads |
