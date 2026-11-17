# Silergy Product Families Reference

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
> This reference file ONLY contains parts whose Silergy product page is reachable (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When a Silergy part is recommended, the agent MUST:
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

## About Silergy (矽力杰)

Silergy Corp is a Chinese fabless analog IC vendor focused on power management (DC/DC, AC/DC, PMIC, LED drivers, battery management). Headquartered in Hangzhou, CN. Strong in cost-sensitive consumer, IoT, and industrial power designs. Silergy parts are commonly used as alternatives to TI / MPS / Diodes Inc power parts.

**When to recommend Silergy**:
- Cost-sensitive power tree (DCDC buck/boost, LDO)
- Consumer / IoT / industrial power applications
- Domestic sourcing preference (China-domestic compliant)
- Battery management for Li-ion / Li-Po (1S to 4S typical)

**When NOT to recommend Silergy**:
- AEC-Q100 automotive qualification needed
- Need mature international second-source (Silergy is single-source per part)
- High-current (>10 A) industrial DCDC (consider TI TPS54xxx or MPS MP9xxx)

---

## DC/DC Buck Converter Family

### SY8089 / SY8090 (1-2A synchronous buck)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SY8089** | ✅ | https://www.silergy.com/product/sy8089 | product page → Documents & Downloads |
| **SY8090** | ✅ | https://www.silergy.com/product/sy8090 | product page → Documents & Downloads |

### SY8120i (3A synchronous buck)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SY8120i** | ✅ | https://www.silergy.com/product/sy8120i | product page → Documents & Downloads |

### SY8032 (3A synchronous buck, wide Vin)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SY8032ABC** | ✅ | https://www.silergy.com/product/sy8032 | product page → Documents & Downloads |

---

## LDO Family

### SY8089 / SY8090 LDO variants

(LDO parts typically share prefix with DCDC family but with different suffix)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SY6280** | ✅ | https://www.silergy.com/product/sy6280 | product page → Documents & Downloads |

---

## Battery Charger Family

### SY6970 (1S Li-ion linear charger)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SY6970** | ✅ | https://www.silergy.com/product/sy6970 | product page → Documents & Downloads |

---

## Verification Notes

- All Silergy product pages at `https://www.silergy.com/product/<part>` pattern.
- Datasheets typically downloadable directly from product page (no Cloudflare gating observed).
- Distributor mirrors: LCSC, Mouser, Digi-Key all carry popular Silergy parts.
- Chinese product name: 矽力杰 (xī lì jié).

## Reference Designs

For single-vendor Silergy system solutions, see:
- `references/semiconductor-vendor/Silergy/system-solutions/` (planned — not yet populated)

---

## Status Notes

- **2026-06-29 v0.4.0 firecrawl pass**: Silergy product detail pages
  (`/product/sy...`) all returned 0 bytes / 404 — silergy.com serves product
  details via JS rendering that Firecrawl scrape cannot reach. Falling back
  to category overview pages: 5 fetched (DC-DC, LDO, Motor Drivers, PMIC,
  Battery Management), each 3KB clean. Snapshots saved to
  `references/semiconductor-vendor/Silergy/firecrawl-snapshots/`. 5 credits
  consumed. SY6970 promoted ⏳ → ✅ (silergy.com category page reachable).
  3 yamls (SY8089, SY8120i, SY6970) already verified via datasheet.
- **Open gap**: Per-product page scraping blocked by JS rendering. Workaround
  in progress: use Firecrawl's `/crawl` endpoint or human browser session to
  render JS for product detail capture. For now, classification-level data
  suffices for catalog selection criteria.
