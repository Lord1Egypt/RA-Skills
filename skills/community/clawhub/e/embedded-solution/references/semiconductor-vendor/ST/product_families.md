# STMicroelectronics Product Families Reference

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
> This reference file ONLY contains **parts whose ST product page is reachable** (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When an ST part is recommended, the agent MUST:
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

## STM32 Wireless MCU (Cortex-M4 + wireless coprocessor)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **STM32WB55** | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32wb55rg.html | product page → Documents & Downloads |
| **STM32WL55** | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32wl-series.html | product page → Documents & Downloads |

## STM32 Ultra-Low-Power (Cortex-M33)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **STM32U575** | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32u5-series.html | product page → Documents & Downloads |
| **STM32U585** | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32u5-series.html | product page → Documents & Downloads |
| **STM32U5** *(family alias)* | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32u5-series.html | product page → Documents & Downloads |

> **ST does not publish separate U575 / U585 product pages on st.com** — both
> share the same family landing page. The datasheet document ID is the only
> reliable way to distinguish them: DS13737 = U575, DS13086 = U585. The
> discriminator is the crypto block: U575 = HASH only, U585 = HASH + AES + PKA
> + OTFDEC/SAES. Use the per-variant YAML for crypto-sensitive designs.

## STM32 High-Performance (Cortex-M7)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **STM32H7** | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32h7-series.html | product page → Documents & Downloads |

## STM32 MPU (Cortex-A7 + Cortex-M4 heterogeneous)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **STM32MP157** | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32mp1-series.html | product page → Documents & Downloads |

---

## Family Hub Pages (Verification Pending)

| Family | Main Page |
|--------|-----------|
| **STM32 32-bit Arm Cortex MCUs** | https://www.st.com/en/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus.html |
| **STM32 Wireless MCUs** | https://www.st.com/en/microcontrollers-microprocessors/stm32-wireless-mcus.html |
| **STM32 MPUs** | https://www.st.com/en/microcontrollers-microprocessors/stm32-mpus.html |

---

## Evaluation Boards (links pending verification — do not use without HTTP 200 check)

- STM32WB55 Nucleo (unverified)
- STM32WL55 Nucleo (unverified)
- STM32U575 Nucleo (unverified)
- STM32H747 Discovery (unverified)
- STM32MP157 Discovery (unverified)

## Status Notes

- Verified round 2026-06-21 (see `.link_verification_report.md`):
  Nordic 5 ✅ (via Tavily, Cloudflare-protected), NXP 5 (3 ✅ + 2 URL fixes),
  ST 5 (4 ✅ + 1 URL fix), TI 5 ✅. No ❌ in this round.
- The catalog will transition from ⏳ to ✅ / ❌ after a Tavily/web_fetch pass.
- YAML files in `specs/ST/` exist as placeholders and contain no numerical specs. *(2026-06-28: 6 of 8 ST parts now have full extracted spec data: STM32U575, STM32U585, STM32U5 family alias, STM32H7, STM32MP157, STM32WB55, STM32WL55, STM32G0. Remaining placeholder: STM32WBA — datasheet unreachable as of 2026-06-28, see STM32WBA row below.)*
- **2026-06-29 v0.4.0 firecrawl pass** (see `.planning/v0.4.0-firecrawl-integration.md`):
  7 ST family pages re-verified via Firecrawl (`scrape` keyed mode, 1 credit each,
  cache hits on previously seen URLs). All 7 promoted from ⏳ to ✅ in the tables
  above. Raw + clean snapshots for each family saved to
  `references/semiconductor-vendor/ST/firecrawl-snapshots/` (~140 KB total).
  ST catalog now at 8/8 parts ✅ verified (STM32WBA no longer placeholder).
  st.com PDF datasheet CDN still 401 to unauthenticated scrape — per-variant deep
  specs (current, RF sensitivity) remain an open gap; family-page level data is
  now reliably extractable for catalog selection.


## STM32G0 Series — entry-level Cortex-M0+

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **STM32G0** | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32g0-series.html | product page → Documents & Downloads |


## STM32WBA Series — BLE 5.3 + 802.15.4 single-chip with secure element

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **STM32WBA** | ✅ | https://www.st.com/en/microcontrollers-microprocessors/stm32wba-series.html | product page → Documents & Downloads |

> **2026-06-29 update (v0.4.0 firecrawl pass)**: st.com WBA series page is now reachable
> via Firecrawl scrape (HTTP 200, 28 KB markdown). Family-level summary (Cortex-M33,
> flash/RAM ranges, protocols, security) was extracted into `specs/ST/STM32WBA.yaml`
> (link_status: verified_2026-06-29 (family-page-extract)). Per-datasheet values
> (RX sensitivity, active-mode current, exact pinouts) remain unverified — the
> st.com PDF datasheet CDN still returns 401 to unauthenticated scrape. Use the
> family-page snapshot for selection criteria; defer to per-variant datasheet for
> power-budget / RF design.
