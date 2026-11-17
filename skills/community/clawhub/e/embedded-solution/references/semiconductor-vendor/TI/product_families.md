# Texas Instruments Product Families Reference

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
> This reference file ONLY contains **parts whose TI product page is reachable** (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When a TI part is recommended, the agent MUST:
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

## SimpleLink Wireless MCU (CC Family)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CC2640R2F** | ⏳ | https://www.ti.com/product/CC2640R2F | product page → Documents & Downloads |
| **CC2652R** | ⏳ | https://www.ti.com/product/CC2652R | product page → Documents & Downloads |
| **CC1310** | ⏳ | https://www.ti.com/product/CC1310 | product page → Documents & Downloads |
| **CC2340R5** | ⏳ | https://www.ti.com/product/CC2340R5 | product page → Documents & Downloads |

## MSP General Purpose MCU (Cortex-M0+)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **MSPM0G3507** | ⏳ | https://www.ti.com/product/MSPM0G3507 | product page → Documents & Downloads |

---

## Family Hub Pages (Verification Pending)

| Family | Main Page |
|--------|-----------|
| **SimpleLink Wireless MCUs** | https://www.ti.com/microcontrollers-mcus-processors/wireless-mcus/overview.html |
| **MSP Microcontrollers** | https://www.ti.com/microcontrollers-mcus-processors/msp-microcontrollers/overview.html |
| **C2000 Real-Time MCUs** | https://www.ti.com/microcontrollers-mcus-processors/c2000-real-time-mcus/overview.html |

---

## Evaluation Boards (links pending verification — do not use without HTTP 200 check)

- CC2640R2F LaunchPad (unverified)
- CC2652R LaunchPad (unverified)
- CC1310 LaunchPad (unverified)
- CC2340R5 LaunchPad (unverified)
- MSPM0G3507 LaunchPad (unverified)

## Status Notes

- All entries are placeholders pending first link-verification round.
- The catalog will transition from ⏳ to ✅ / ❌ after a Tavily/web_fetch pass.
- YAML files in `specs/TI/` exist as placeholders and contain no numerical specs. *(2026-06-28: 4 of 6 TI YAMLs (CC1310, CC2640R2F, CC2652R, MSPM0G3507) now have full extracted spec data. CC2340R5 extractor was finding wrong values (BLE 1.2 / Cortex-M0 instead of BLE 5.3 / Cortex-M0+) so promote was refused; CC3300 (WiFi 6 + BLE companion) remains placeholder — no PDF in catalog.)*
- **2026-06-29 v0.4.0 firecrawl pass**: 2 family hub pages reachable via Firecrawl
  (C2000-MCU, ARM-MCU overview). Initial guesses `wireless-mcus/overview.html`,
  `msp-microcontrollers/overview.html`, `simplelink-mcus/overview.html` returned
  404 — TI has reorganized those URLs. Real content captured via the umbrella
  `microcontrollers-mcus-processors/overview.html` page (13KB raw → 6.5KB clean).
  CC3300 product page fetched individually (60KB raw → 20KB clean); placeholder
  yaml promoted to verified. Snapshots saved to
  `references/semiconductor-vendor/TI/firecrawl-snapshots/`. No numerical
  parameters added per design policy.


## CC33xx Series — WiFi 6 + BLE companion IC

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CC3300** | ✅ | https://www.ti.com/product/CC3300 | product page → Documents & Downloads |
