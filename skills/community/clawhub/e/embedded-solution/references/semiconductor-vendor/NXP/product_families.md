# NXP Semiconductors Product Families Reference

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
> This reference file ONLY contains **parts whose NXP product page is reachable** (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When an NXP part is recommended, the agent MUST:
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

## i.MX RT Crossover MCU (Arm Cortex-M7 / dual M7+M4)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **i.MX RT1064** | ✅ | https://www.nxp.com/products/i.MX-RT1064 | product page → Documents & Downloads |
| **i.MX RT1170** | ✅ | https://www.nxp.com/products/i.MX-RT1170 | product page → Documents & Downloads |

## Kinetis MCU (Arm Cortex-M4)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **K66** | ✅ | https://www.nxp.com/products/K66_180 | product page → Documents & Downloads |

## KW Family (Automotive BLE MCU)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **KW45** | ✅ | https://www.nxp.com/products/KW45 | product page → Documents & Downloads |

## LPC MCU (Arm Cortex-M33)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **LPC55S69** | ✅ | https://www.nxp.com/products/LPC55S6x | product page → Documents & Downloads |

---

## Filename Note

i.MX parts use `.` in their part numbers. YAML filenames replace `.` with `_`
to avoid filesystem ambiguity (e.g. `i.MX_RT1064.yaml`). The `part:` field
preserves the original spelling.

## Family Hub Pages (Verification Pending)

| Family | Main Page |
|--------|-----------|
| **i.MX RT Crossover MCUs** | https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus |
| **Kinetis MCUs** | https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/kinetis-cortex-m-mcus |
| **LPC Microcontrollers** | https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/lpc-cortex-m-mcus |
| **Automotive MCUs (KW)** | https://www.nxp.com/products/processors-and-microcontrollers/automotive-mcus |

---

## Evaluation Boards (links pending verification — do not use without HTTP 200 check)

- i.MX RT1064 EVK (unverified)
- i.MX RT1170 EVK (unverified)
- LPCXpresso55S69 (unverified)
- FRDM-K66 (unverified)
- KW45 EVK (unverified)

## Status Notes

- Verified round 2026-06-21 (see `.link_verification_report.md`):
  Nordic 5 ✅ (via Tavily, Cloudflare-protected), NXP 5 (3 ✅ + 2 URL fixes),
  ST 5 (4 ✅ + 1 URL fix), TI 5 ✅. No ❌ in this round.
- The catalog will transition from ⏳ to ✅ / ❌ after a Tavily/web_fetch pass.
- YAML files in `specs/NXP/` exist as placeholders and contain no numerical specs. *(2026-06-28: 3 of 5 NXP YAMLs (K66, LPC55S69, i.MX_RT1170) now have full extracted spec data. KW45 and i.MX-RT1064 remain as stale-mirror catalog gaps; see their YAML notes for the 2 NXP /docs/ URLs that returned 'Not found'.)*
- **2026-06-29 v0.4.0 firecrawl pass**: 5 family hub pages attempted, 2 reachable
  via Firecrawl (iMX-RT crossover MCUs, ARM-MCU umbrella). 3 individual product
  pages fetched (iMX-RT1064 119KB raw, iMX-RT1170 300KB raw, KW45 108KB raw).
  All 3 previously ⏳ entries (iMX-RT1064, iMX-RT1170, KW45) promoted to ✅.
  Empty placeholder yamls (specs: {}) for iMX-RT1064 and KW45 filled with
  family-page data. NXP catalog now at 5/5 ✅ verified (no ❌ in this round).
  Snapshots saved to references/semiconductor-vendor/NXP/firecrawl-snapshots/.
  No numerical parameters added per design policy.
