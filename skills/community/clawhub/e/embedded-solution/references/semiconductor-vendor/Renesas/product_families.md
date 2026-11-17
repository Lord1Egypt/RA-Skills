# Renesas Product Families Reference

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
> This reference file ONLY contains **parts whose Renesas product page is reachable** (HTTP 200) as of the last verification round.
> All numerical parameters have been **removed** from this file because they cannot be verified from a single product-page fetch.
> When a Renesas part is recommended, the agent MUST:
> 1. Open the verified product page below to confirm the part still exists.
> 2. From the product page, navigate to "Documents & Downloads" → download the latest datasheet PDF.
> 3. Extract every numerical parameter with `pdfplumber` and cite the table/page.
> 4. NEVER transcribe numbers from this file into a response — they are not authoritative.
>
> **Public-release users:** datasheet PDFs are vendor-copyrighted and not bundled with this skill. Always download from the vendor product page listed in the "Main Page" column below.

## Link Verification Status

| Status | Meaning |
|--------|---------|
| ✅ | Main page returns HTTP 200 |
| ❌ | Main page returns 404 — part has been removed, renamed, or relocated. Do NOT use. |
| ⏳ | Not yet verified. Use only after a manual HTTP 200 check. |

---

## BLE SoC Family

### DA1459x Series (SmartBond™)

| Part | Link Status | Main Page | Datasheet Source |
|------|-------------|-----------|------------------|
| **DA14594** | ✅ | https://www.renesas.com/da14594 | product page → Documents & Downloads |
| **DA14592** | ✅ | https://www.renesas.com/da14592 | [datasheet PDF](https://www.renesas.com/en/document/dst/da14592-datasheet) |
| **DA14531** | ✅ | https://www.renesas.com/da14531 | product page → Documents & Downloads |
| ~~DA14591~~ | ❌ removed | — | — |

### DA1469x Series (High Integration)

| Part | Link Status | Main Page | Datasheet Source |
|------|-------------|-----------|------------------|
| **DA14697** | ✅ | https://www.renesas.com/da14697 | product page → Documents & Downloads |
| **DA1470x** | ✅ | https://www.renesas.com/da1470x | product page → Documents & Downloads |
| ~~DA1469C~~ | ❌ removed | — | — |

---

## RA Family (Cortex-M33 MCU)

| Part | Link Status | Main Page | Datasheet Source |
|------|-------------|-----------|------------------|
| **RA6M5** | ✅ | https://www.renesas.com/ra6m5 | product page → Documents & Downloads |
| **RA6M4** | ✅ | https://www.renesas.com/ra6m4 | product page → Documents & Downloads |
| **RA6M3** | ✅ | https://www.renesas.com/ra6m3 | product page → Documents & Downloads |
| **RA6M2** | ✅ | https://www.renesas.com/ra6m2 | product page → Documents & Downloads |
| **RA4M3** | ✅ | https://www.renesas.com/ra4m3 | product page → Documents & Downloads |
| **RA4M2** | ✅ | https://www.renesas.com/ra4m2 | product page → Documents & Downloads |
| ~~RA2M1~~ | ❌ removed | — | — |

---

## RL78 Family (Low Power 8/16-bit)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **RL78G23** | ✅ | https://www.renesas.com/rl78g23 | product page → Documents & Downloads |
| **RL78G14** | ✅ | https://www.renesas.com/rl78g14 | product page → Documents & Downloads |
| **RL78H1D** | ✅ | https://www.renesas.com/rl78h1d | product page → Documents & Downloads |
| **RL78I1D** | ✅ | https://www.renesas.com/rl78i1d | product page → Documents & Downloads |

---

## RX Family (32-bit)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **RX72N** | ✅ | https://www.renesas.com/rx72n | product page → Documents & Downloads |
| **RX71M** | ✅ | https://www.renesas.com/rx71m | product page → Documents & Downloads |
| **RX66T** | ✅ | https://www.renesas.com/rx66t | product page → Documents & Downloads |
| **RX65N** | ✅ | https://www.renesas.com/rx65n | product page → Documents & Downloads |
| **RX231** | ✅ | https://www.renesas.com/rx231 | product page → Documents & Downloads |
| **RX140** | ✅ | https://www.renesas.com/rx140 | product page → Documents & Downloads |

---

## Power Management ICs

### DC/DC Buck

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **ISL9305** | ✅ | https://www.renesas.com/isl9305 | product page → Documents & Downloads |
| ~~ISL91302~~ | ❌ removed | — | — |
| ~~ISL91303~~ | ❌ removed | — | — |
| ~~RAA21033~~ | ❌ removed | — | — |

### Voltage Supervisors / Reset ICs

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **ISL88813** | ✅ | https://www.renesas.com/isl88813 | product page → Documents & Downloads |
| **ISL88705** | ✅ | https://www.renesas.com/isl88705 | product page → Documents & Downloads |
| ~~ISL88013~~ | ❌ not used in this catalog | — | — |

### Battery Charger

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **ISL9205** | ✅ | https://www.renesas.com/isl9205 | product page → Documents & Downloads |
| **ISL9238** | ✅ | https://www.renesas.com/isl9238 | product page → Documents & Downloads |
| ~~ISL9240~~ | ❌ removed | — | — |

---

## NFC Wireless Charging (Panthronics — Renesas)

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **PTX30W** | ✅ | https://www.renesas.com/ptx30w | product page → Documents & Downloads |
| **PTX130W** | ✅ | https://www.renesas.com/ptx130w | product page → Documents & Downloads |

---

## Sensors

### Humidity / Temperature

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **HS3001** | ✅ | https://www.renesas.com/hs3001 | product page → Documents & Downloads |
| **HS3002** | ✅ | https://www.renesas.com/hs3002 | product page → Documents & Downloads |
| **HS3003** | ✅ | https://www.renesas.com/hs3003 | product page → Documents & Downloads |

---

## Family Hub Pages (Verified)

| Family | Main Page |
|--------|-----------|
| **RA Family** | https://www.renesas.com/ra-family |
| **RX Family** | https://www.renesas.com/rx-family |
| **RL78 Family** | https://www.renesas.com/rl78-family |

---

## Evaluation Boards (links pending verification — do not use without HTTP 200 check)

The following EVK links are NOT pre-verified. Before recommending an EVK, fetch the URL and confirm it returns HTTP 200. If 404, do NOT recommend the EVK by name — instead, search the family page.

- DA14594 EVK (unverified)
- DA1470x EVK (unverified)
- RA6M4 EK (unverified)


## Renesas RA Family — ultra-low-power Cortex-M23 / M33

| Part | Link Status | Main Page | Datasheet Path |
|------|-------------|-----------|----------------|
| **RA4M1** | ✅ | https://www.renesas.com/ra/ra4m1 | product page → Documents & Downloads |

---

## Status Notes

- **2026-06-29 v0.4.0 firecrawl pass**: 4 family hub pages re-verified via Firecrawl
  (RA Family, RL78 Family, MCU overview, Power Management) — saved as clean markdown
  snapshots under `references/semiconductor-vendor/Renesas/firecrawl-snapshots/`.
  Initial guesses `ra-family`/`rl78-family`/`rx-family` returned 404 — Renesas uses
  `/products/microcontrollers-microprocessors/...` paths now. PTX130W (Panthronics
  NFC WLC Poller IC) fetched individually; placeholder yaml promoted to verified.
  No numerical parameters added to this file per design policy.
