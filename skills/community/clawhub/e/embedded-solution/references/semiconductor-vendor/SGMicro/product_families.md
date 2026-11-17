# SG Micro Product Families Reference

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
> This reference file ONLY contains parts whose SG Micro product page is reachable (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When a SG Micro part is recommended, the agent MUST:
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

## About SG Micro (圣邦微电子)

SG Micro Corp (圣邦微电子, stock code 300661) is a leading Chinese fabless analog IC vendor. Products span op-amps, comparators, LDOs, DC/DC converters, analog switches, audio amplifiers, and motor drivers. Strong in cost-sensitive consumer and industrial designs.

**When to recommend SG Micro**:
- Cost-sensitive analog signal chain
- Domestic sourcing preference
- General-purpose op-amp / comparator / LDO with standard specs
- Audio amplifier for small speaker / piezo buzzer
- Analog switch for signal routing

**When NOT to recommend SG Micro**:
- Ultra-low-noise precision analog (use TI / ADI)
- AEC-Q100 automotive qualification needed
- Need mature international second-source

---

## Analog Switch Family

### SGM3157 (single-pole double-throw analog switch)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SGM3157** | ✅ | https://www.sg-micro.com/product/sgm3157 | product page → Documents & Downloads |

### SGM6601 (high-side load switch)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SGM6601** | ✅ | https://www.sg-micro.com/product/sgm6601 | product page → Documents & Downloads |

---

## Audio Amplifier Family

### SGM8903 (Class-D mono audio amplifier)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SGM8903** | ✅ | https://www.sg-micro.com/product/sgm8903 | product page → Documents & Downloads |

### SGM8902 (Class-AB headphone amplifier)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SGM8902** | ✅ | https://www.sg-micro.com/product/sgm8902 | product page → Documents & Downloads |

---

## Operational Amplifier Family

### SGM358 (low-power dual op-amp)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **SGM358** | ✅ | https://www.sg-micro.com/product/sgm358 | product page → Documents & Downloads |

---

## Verification Notes

- All SG Micro product pages at `https://www.sg-micro.com/product/<part>` pattern.
- Datasheets typically downloadable directly from product page.
- Distributor mirrors: LCSC, Mouser, Digi-Key carry popular parts.
- Chinese product name: 圣邦微电子.

## Reference Designs

For single-vendor SG Micro system solutions, see:
- `references/semiconductor-vendor/SGMicro/system-solutions/` (planned — not yet populated)

---

## Status Notes

- **2026-06-29 v0.4.0 firecrawl pass**: 5 SGMicro product pages fetched via
  Firecrawl (SGM3157, SGM6601, SGM8903, SGM8902, SGM358). All returned real
  content with cookie banner at top + product specs / ordering info below.
  Snapshots saved to
  `references/semiconductor-vendor/SGMicro/firecrawl-snapshots/`. 5 credits
  consumed. SGM8902 promoted ⏳ → ✅. 2 yamls in `specs/SGMicro/` (SGM3157,
  SGM8903) already verified via datasheet — no upgrade needed.
