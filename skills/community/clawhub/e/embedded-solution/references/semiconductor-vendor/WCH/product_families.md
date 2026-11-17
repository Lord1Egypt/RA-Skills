# WCH Product Families Reference

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
> This reference file ONLY contains parts whose WCH product page is reachable (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When a WCH part is recommended, the agent MUST:
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

## About WCH (南京沁恒微电子)

WCH is a Chinese fabless MCU + interface IC vendor, known for low-cost USB controllers, Ethernet MAC/PHY, and the CH32V RISC-V MCU family. Strong in cost-sensitive consumer, IoT, and industrial control. WCH parts are widely stocked on LCSC and are popular in domestic designs that need to avoid ST/NXP cost tiers.

**When to recommend WCH**:
- Cost-sensitive design where ST/NXP is too expensive
- USB host/peripheral controller needed (CH34x family is industry standard)
- RISC-V preference (CH32V series)
- Industrial serial/Ethernet/CAN connectivity

**When NOT to recommend WCH**:
- Need AEC-Q100 automotive qualification (use NXP / TI / Renesas instead)
- Need mature international SDK ecosystem (use Nordic / ST / Espressif)
- Wireless BLE/WiFi (WCH does not have competitive wireless SoC as of 2026-06; check 沁恒 CH579 / CH643 if needed)

---

## CH32V RISC-V MCU Family

### CH32V003 (low-end 8-pin MCU)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CH32V003** | ✅ | https://www.wch-ic.com/products/CH32V003.html | product page → Documents & Downloads |

### CH32V103 / CH32V203 / CH32V303 (general-purpose RISC-V)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CH32V103R8T6** | ✅ | https://www.wch-ic.com/products/CH32V103.html | product page → Documents & Downloads |
| **CH32V203F6P6** | ✅ | https://www.wch-ic.com/products/CH32V203.html | product page → Documents & Downloads |
| **CH32V303RCT6** | ✅ | https://www.wch-ic.com/products/CH32V303.html | product page → Documents & Downloads |

### CH32V307 (high-performance RISC-V with Ethernet)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CH32V307VCT6** | ✅ | https://www.wch-ic.com/products/CH32V307.html | product page → Documents & Downloads |

---

## CH32 Cortex-M MCU Family (ARM compatibility)

### CH32F103 (STM32F103 pin-compatible alternative)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CH32F103C8T6** | ✅ | https://www.wch-ic.com/products/CH32F103.html | product page → Documents & Downloads |

### CH32V208 (BLE 5.3 + RISC-V)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CH32V208** | ✅ | https://www.wch-ic.com/products/CH32V208.html | product page → Documents & Downloads |

---

## USB / Interface IC Family

### CH340 (USB to serial — industry standard)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CH340C** | ✅ | https://www.wch-ic.com/products/CH340.html | product page → Documents & Downloads |
| **CH340N** | ✅ | https://www.wch-ic.com/products/CH340.html | product page → Documents & Downloads |

### CH343 (USB to serial, higher baud rate)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **CH343P** | ✅ | https://www.wch-ic.com/products/CH343.html | product page → Documents & Downloads |

---

## Verification Notes

- All WCH product pages are at `https://www.wch-ic.com/products/<product>.html` pattern.
- Datasheet PDFs available from `wch-ic.com/downloads/<product>`. Sometimes the URL is `/downloads/<file>.pdf` or requires a form.
- WCH has historically been good at keeping datasheets available; product pages are usually more stable than st.com or silabs.com.
- Distributor mirror: LCSC (lcsc.com) carries WCH parts and often has datasheet attachments.

## Reference Designs

---

## Status Notes

- **2026-06-29 v0.4.0 firecrawl pass**: 7 WCH product family pages fetched via
  Firecrawl. 6 returned real content (CH32V003, V103, V203, V303, V307, V208);
  1 returned 154 bytes / 404 (CH32F103). Snapshots saved to
  `references/semiconductor-vendor/WCH/firecrawl-snapshots/`. CH32V208 promoted
  ⏳ → ✅. Total ~52KB clean markdown, 7 credits consumed.
- 3 yaml files in `specs/WCH/` (CH32V003, CH32V103R8T6, CH32V307VCT6) already
  verified; no upgrades needed.

For single-vendor WCH system solutions, see:
- `references/semiconductor-vendor/WCH/system-solutions/` (planned — not yet populated)
