---
name: embedded-solution
description: >
  Recommend embedded system solutions: chip selection, BOM design, vendor
  comparison, and reference design matching across multiple semiconductor
  vendors. Triggers when user mentions embedded systems, electronic
  products, smart devices, technical solutions, chips, hardware, datasheets,
  firmware, or development boards (when used for embedded system design —
  NOT for pure software/learning questions).
  All component specs MUST be fetched from official vendor sources. Never
  fabricate part numbers, parameters, or pricing.
version: 0.6.0
author: wangp-gh
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: hardware
    tags: [embedded, semiconductor, datasheet, BOM, MCU, SoC, sensor, power, BLE, WiFi, motor-control, smart-glasses, smart-ring, robot-gripper, no-fabrication]
---

# Embedded Solution Skill

## ⚠️ Absolute Rule: No Fabrication

**If you do not find a parameter in an official source, you MUST say "not verified" or "not found". You may NOT estimate, extrapolate, assume, or make up a value under any circumstances.**

This rule applies to:
- ❌ Part numbers (do not invent chips that don't exist)
- ❌ Specifications (current, voltage, package, etc.)
- ❌ Pricing (always mark as "depends on quote / distributor")
- ❌ Reference designs (do not invent URLs)
- ❌ Vendor capabilities (do not claim a vendor supports a protocol they don't)

## Anti-patterns

Common mistakes when responding. These are the failure modes that show up in agent traces — don't repeat them.

| Don't do this | Do this instead |
|---------------|------------------|
| **Quote numerical specs from memory** (CoreMark, RX sensitivity, sleep current, BLE version, etc.) | Always cite a verified source: `[D]` datasheet page, `[#]` catalogue, `[D-HTML @ tier N]` product page. Numbers drift; "I remember" is fabrication. |
| **Recommend before Step 5 clarification** (chip picked when wireless protocol or operating environment is unknown) | Complete Step 5 first; or — when cost-of-being-wrong is low — state assumption explicitly and proceed. |
| **Single recommendation when alternatives exist** (one chip with no comparison) | Default to top 3 + comparison table. Use single pick only when the catalogue has 1 entry. |
| **"Create a new solution.md" by default on every novel topic** | Skips the v0.4.4+ Tier 3 capability path; gets slow + risks fabrication outside the catalogue | Use **Option A — fetch + cite inline** by default. Curate a solution.md (**Option B**) only when the topic recurs or the user asks. |
| **Cite a chip without `product_families.md` anchor** | Anchor every chip to its `product_families.md` row so the user can verify the part exists in this catalogue. |
| **Keep fetching past the first tier that answered** (re-download vendor PDF when Tier 1 YAML already covers it) | Stop at the first tier that fully answers the parameter; one fetch per tier per field. |
| **Lump multiple questions into one message** ("could you clarify A, B, C, D, E?") | Ask **one decision at a time** with enumerated a/b/c options (Step 5 rule). |
| **Pick Tier 3 tool by brand name** (`use web_fetch` or `use tavily_extract` only) | Pick by capability (URL → markdown, or PDF → text). Any tool satisfying the contract qualifies at that tier; see Tier 3 step 3c/3d. |
| **Drop out-of-catalog parts from a market comparison** (user asked for 5 candidates, you silently dropped 2) | Escalate the missing parts to Tier 4 with `[T4]` marker + URL + timestamp. See `scripts/test_outofcatalog.py` (fixture 19). |
| **Claim pin-compatible / pin-incompatible / single BOM total / stock status as facts** | All of these need a vendor source + range (e.g. "$6–8 passive track / $11–15 active track, verify with distributor"). |
| **Always download the datasheet PDF for a single headline spec** | Use the **HTML-first fast path** (Tier 3 step 3d): product pages expose 3-7 headline specs in 5-10 s; only fall back to full PDF when the parameter needs the electrical-characteristics table. |
| **Write a 1000-word essay when 3 bullets + table would do** | Lead with the comparison table; prose supports the table, not the other way around. |
| **Block with 5 questions before recommending anything** | Default to a reasonable assumption, state it, and proceed (see Step 5); only ask when the cost of being wrong is high (AEC-Q100, FDA, regulatory locking). |
| **"Read the datasheet at <URL> to compare"** / leave spec values blank for the user to fill in | Fetch the datasheet, extract the spec, cite URL + timestamp. Only mark `not verified` after mirrors have been tried. |
| **Default to L1 (HTML-only) when user wants a comparison table** — leaves the table 30–60% empty because product pages don't expose electrical characteristics | When the user's query is a **comparison** (`X vs Y`, `对比 X 和 Y`, `compare X to Y`, `X 和 Y 哪个好`, etc.), after Tier 3d HTML-first completes, **auto-escalate to L2 = Tier 3c PDF fallback (curl + pdfplumber)** for any cell still showing `not in HTML` or `[~]`. Pattern-match these keywords; don't ask the user. Cost: 30-90 s per chip per PDF (parallel-fetch PDFs, then extract p.1). Outcome: ≥ 95% cell coverage instead of 41%. |

## When to Trigger

This skill triggers when the user mentions any of:

- **Embedded systems**: MCU, SoC, RTOS, firmware, drivers, BSP, HAL
- **Electronic products**: smart devices, IoT, wearables, robots, sensors
- **Technical solutions**: BOM, system design, component selection, vendor comparison
- **Chips / ICs**: microcontroller, processor, BLE, WiFi, motor driver, power management
- **Hardware design**: schematic, PCB, datasheet, reference design
- **Datasheets**: datasheet, spec sheet, data sheet
- **Firmware**: firmware, driver, SDK, middleware, BSP
- **Development boards**: dev kit, evaluation board, starter kit (when used for embedded design)

### Do NOT trigger for

- Pure software/learning questions (e.g., "how to write Hello World in Rust on ESP32")
- General programming (Python, JavaScript, algorithms)
- Web / cloud / database questions
- Math / theory without hardware context

## Core Principle

**All chip parameters come from official sources only.**
Never use pre-filled hardcoded specs. Every parameter must be verified against:
1. The chip's official datasheet PDF (downloaded to `embedded_dev/<vendor>/datasheet/`)
2. The official vendor product page on the vendor's website

**Critical distinction:**
- **Descriptive text** (e.g., "optimized for low power") = NOT a specification.
- **Tables with Min/Typ/Max columns** = specification. These are the only acceptable numerical sources.
- **Product page bullet lists** = often descriptive. Prefer datasheet tables for numerical values.

## Search Priority

When looking up chip data, BOM candidates, or reference designs, **always follow this 4-tier order — cheapest source first**. **Stop at the first tier that yields a usable answer for each parameter.** Do not keep fetching once a tier is sufficient.

| Tier | Source | When to use | Cost / speed | Install mode |
|------|--------|-------------|--------------|--------------|
| **1** | `specs/<Vendor>/<Part>.yaml` | First stop. Use a YAML field if it covers the parameter you need. Stop here if the field is present and the YAML's `link_status` is `verified_...` or `partial_verified_...`. | Fastest, zero network | Only if **specs plug-in** is installed |
| **2** | `embedded_dev/<vendor>/datasheet/<Part>_datasheet.pdf` | When Tier 1 is missing the field, or the YAML is a placeholder, or the YAML's `link_status` is `placeholder_...` and you need the actual datasheet body to fill the gap. The local PDF is a **trustworthy mirror** — do NOT re-fetch from the vendor URL once you have it locally. | Local PDF read (pdfplumber); zero network once installed | Only if **datasheets plug-in** is installed |
| **3** | `references/semiconductor-vendor/<Vendor>/product_families.md` + vendor URL fetch | Always available (built into the skill). Two sub-steps: (a) read the row for vendor URL + verification status, (b) follow the URL to fetch the datasheet / product page if you need actual spec values. Use this when Tier 1/2 are not installed OR do not cover the parameter. | Local file read for (a); network fetch for (b) | Always |
| **4** | Other reliable data sources | When Tiers 1–3 do not cover the parameter. Includes external datasheet mirrors (overseas: AllDatasheet → Mouser → Digi-Key → Reichelt → vendor site; domestic CN vendors: vendor CN site → LCSC → HQChip → Szlcsc → Semiee → OSHWHUB); plus any vendor or distributor URL surfaced in search but not in `references/`. | Network | Always |

**Rules**:

- **Stop early. The first tier that fully answers the question is the end.** Don't continue fetching to "double-check" or to gather extra data the user didn't ask for.
- Always cite the tier + URL/file anchor + timestamp. No "I remembered it" facts.
- **Tier 1 is conditional on the verified marker + recency.** Don't blindly trust every YAML field — some are placeholders or stale. For placeholder fields, the field is treated as missing and you fall through to Tier 2 (local datasheet) or Tier 3 (vendor URL).
- **Tier 2 is offline-first**: if the datasheets plug-in is installed, the local PDF is authoritative for that part. Re-fetching the vendor URL is wasted network and risks getting a different revision than what's already on disk.
- Tier 3 is two-step: read the `product_families.md` row for the URL/status, then fetch the URL for actual values when needed. Don't skip step 3b just because you found the URL — fetch the spec.
- Tier 4 is region-aware: domestic-CN mirrors first for GigaDevice / WCH / GD / QH / Nation Tech / HDSC; overseas mirrors first for ST / TI / Nordic / NXP / Renesas / Silicon Labs / Espressif.
- If Tier 4 is needed, return to Step 6 output template — only the source depth changes, the format stays the same.
- **Dual install modes** (public release without plug-ins vs dev clone / with plug-ins) are handled transparently: each tier is independently conditional on the relevant plug-in being installed.

**Per-parameter, not per-chip**: Each spec field (RAM, flash, current, ...) goes through the 4 tiers independently. A chip may have RAM verified from Tier 1 YAML, flash from Tier 2 local datasheet, core count from Tier 3 product_families.md, and pricing from Tier 4 distributor — that's normal and the citation format should make each tier explicit.

## Workflow

### Step 1: Understand the Application

1. Identify the **target application** (e.g., "smart ring", "robot joint", "smart glasses").
2. Identify **key requirements**:
   - Wireless (BLE / WiFi / NFC / LoRa)?
   - Processing power (Cortex-M0+ vs M33 vs M7)?
   - Power consumption (battery life target)?
   - Sensors (IMU, PPG, temperature, etc.)?
   - Size / cost / BOM constraints?
3. Identify **constraints**: battery powered, IP rating, operating temp range, regulatory.

### Step 2: Check Application Solution Index

Read `references/application-solution/INDEX.md` (auto-generated by `scripts/build_application_index.py`):

- **If a matching solution exists** → go to Step 3
- **If no matching solution exists** → pick one of three options based on cost:
  - **Option A — fetch + cite inline (default, recommended)**. For a one-shot comparison or quick list, generate the answer directly using the Tier 1–4 search path (Step 4) and present it as a comparison table with citations — exactly as Step 6 would. **Do not** create a new solution.md unless the user explicitly asks. Citations may reference `references/application-solution/INDEX.md#<related>` when a sibling solution informs the BOM. This is now the default path because v0.4.4+ capability-driven fetches (3d HTML-first, 3c Tier A/B/C) make in-session lookup both fast and reliable.
  - **Option B — curate a new solution file** (only when justified). Promote to `references/application-solution/<topic>/solution.md` when (a) the application recurs across many user requests, or (b) the user explicitly says "save this for reuse" / "start a new reference design". Follow the structure of an existing solution (Overview / BOM Candidates / Reference Designs / Selection Matrix / Verification Status); run every BOM spec through Step 4 once and anchor each cell with a tier marker.
  - **Option C — disambiguate** (last resort). Ask **one** targeted question only when none of the 7 default dimensions (Step 5) can be assumed. Otherwise default silently per the Step 5 reversible-cost rule.

### Step 3: Read Solution Document

For each existing solution, `solution.md` contains:

1. **Overview** — application context, key requirements
2. **BOM Candidates** — chips grouped by function (BLE SoC, sensor, power, etc.), with vendor + part number + verification status
3. **Reference Designs** — vendor-provided reference designs that match this application
4. **Selection Matrix** — trade-off table with recommendations
5. **Verification Status** — which BOM specs have been verified against vendor datasheets

### Step 4: Verify Each BOM Component (fetch, don't punt)

**Principle**: the skill exists to deliver verified chip specs to the user. **The skill fetches datasheets itself; the user should never have to read a 300-page PDF just to compare two BLE SoCs.** If a parameter is in any catalogue or datasheet, the skill extracts it; the user gets a filled-in comparison table, not a list of links.

**Stop-early rule** (per the Search Priority section above): walk the 4 tiers in order — Tier 1 specs → Tier 2 local datasheet → Tier 3 product_families + vendor URL → Tier 4 external mirrors — and **stop at the first tier that yields a usable answer for the parameter you need**. Don't continue fetching to "double-check" or to gather extra data the user didn't ask for.

**Comparison-query trigger (v0.6.0 — added 2026-07-05)**: when the user's query contains **comparison keywords** (`对比`, `vs`, `compare`, `X 和 Y`, `X or Y`, `difference between`, `which is better`, `spec table`, `对比表`), do not stop at Tier 3d HTML-first alone. After Tier 3d completes, **auto-escalate to Tier 3c PDF (curl + pdfplumber) for any parameter still marked `not in HTML`** so the comparison table reaches ≥ 95% cell coverage. Pattern-match the keywords in the user message; do not ask. Cost: 30-90 s per chip per PDF, run in parallel. Outcome: comparison tables become decision-ready, not 41% empty. See the matching Anti-pattern ("Default to L1 when user wants a comparison table") and the Step 6 escalation offer below.

**v0.4.3 — Out-of-catalog escalation** (added 2026-07-02; see Anti-patterns "Drop out-of-catalog parts" for the rule, and `scripts/test_outofcatalog.py` fixture 19 for the end-to-end regression on a 17-row BLE SoC comparison).

For each candidate chip and each parameter you need, evaluate the tiers in order:

1. **Tier 1 — `specs/<Vendor>/<Part>.yaml`** (only if specs plug-in is installed). YAML field present AND `link_status` is `verified_...` or `partial_verified_...` → use as-is, cite YAML anchor + verification date; **stop here**. Field missing or `link_status` is `placeholder_...` → treat as missing, fall through.

2. **Tier 2 — `embedded_dev/<vendor>/datasheet/<Part>_datasheet.pdf`** (only if datasheets plug-in is installed). The local PDF is a **trustworthy mirror** — do NOT re-fetch from vendor once it is local. Cite the local PDF path + page number; **stop here**.

3. **Tier 3 — `references/semiconductor-vendor/<Vendor>/product_families.md` + vendor URL fetch**. Always available.
   - 3a. Read the catalogue row for URL + verification status (✅/⏳/❌).
   - 3b. If the row's status alone answers the question (e.g. part NRND), stop here.
   - **3c. PDF body fetch (capability-driven)** — pick the highest-capability tool the agent has, in this preference order:
     - **Tier A — server-side repair**: `tavily_extract extract_depth=advanced` / Firecrawl scrape / Jina Reader. URL-in, markdown-out; transparently fixes truncated downloads.
     - **Tier B — direct PDF + local parse**: HTTP-fetch the PDF to a temp path, then parse with `pdfplumber` / `pdftotext` / any other available PDF parser.
     - **Tier C — broken / unknown**: fall through to Tier 4 mirrors; if those also fail, walk the catalogue row instead.
     - **Don't claim a result you couldn't parse**: one retry on a different tool, then `not verified — PDF parse failed`. Never infer.
   - **3d. HTML-first fast path (⭐, preferred over 3c)** — vendor product pages (`renesas.com/<part>`, `st.com/.../`, `nxp.com/products/`) render headline specs without a 35 MB PDF. Pick the highest-capability URL→markdown tool the agent has, in this preference order:
     - **Tier 1**: any tool that does `URL → clean markdown` (e.g. `web_fetch extractMode=markdown`, Firecrawl MCP, Jina Reader)
     - **Tier 2**: keyword-routed page extraction (`tavily_extract extract_depth=basic`, `web_fetch text` + HTML-strip)
     - **Tier 3**: raw HTTP body (`exec curl | head -2000`) — cite as `[#] unstructured`
     - **Tier 4 (none)**: fall through to 3c
     - **Do NOT use a `web_search` / keyword-search tool as a URL fetcher** — snippets, not page body.
   - **3d CAN answer**: status badge, top-line (core / freq / RAM / Flash), voltage range, package list, temp grade, wireless version, **headline** low-power current (feature-rank only).
   - **3d CANNOT answer**: Min/Typ/Max electrical tables, register maps, mechanical drawings, custom SKU variants — fall through to 3c.
   - **3d → 3c fallback**: if Tier 1/2 markdown lacks the parameter, do NOT retry the same URL on a lower tier — fall through to 3c immediately. Don't ping the same URL twice.
   - **Truncated-PDF repair**: if 3c Tier B returns EOF / 0-byte / garbled, fall back to 3c Tier A (server-side repair). Verified pattern, see MEMORY.md 2026-07-01.
   - **Cost**: 3d typical 5-10 s + 1 MB; 3c typical 30-90 s + 6-35 MB. HTML-first saves 1-2 min/part for headline-only comparisons.
   - Citation examples: `(240 MHz, renesas.com/da14706 (URL → markdown @ tier 1), 2026-07-04 13:13 GMT+8, [D-HTML @ tier 1])` — treat `[D-HTML]` as `[#]` for ranking; promote to `[D]` after datasheet-table cross-check.

4. **Tier 4 — External datasheet mirrors** (after Tiers 1–3 exhausted). Try in order, stop at first hit.
   - **Overseas** parts: AllDatasheet → Mouser (`pdfDocs/`, `datasheet/2/389/`) → Digi-Key → Reichelt → vendor site (last resort, often Cloudflare-gated).
   - **Domestic CN** parts (GigaDevice / WCH / GD / QH / Nation Tech / HDSC): vendor CN site → LCSC → HQChip → Szlcsc → Semiee → OSHWHUB.
   - **Fallback rules**: if one mirror 404s or returns HTML, log + try the next. If the vendor site is Cloudflare-gated (st.com, silabs.com), do NOT retry it — go straight to mirrors. If all mirrors fail → `not verified` + give up.

5. **Cite every parameter** with tier + source + timestamp. Examples:
   - `[D]` Tier 2: `embedded_dev/nordic/datasheet/nRF52832_datasheet.pdf p.12, verified 2026-06-28`
   - `[#]` Tier 3 product page: `references/.../product_families.md#<part>, vendor URL fetched 2026-07-04`
   - `[D-HTML @ tier N]` Tier 3d product page: vendor URL, fetch timestamp
   - `[D] Tier 4 mirror`: `<mirror URL> p.12 datasheet rev 1.1, fetched 2026-06-27`

6. **If a parameter truly cannot be confirmed from any tier** (no YAML field, datasheets plug-in not installed, catalogue row incomplete, all mirrors failed) → mark `not verified` + state what you tried across tiers: `tried specs/ (no YAML), tried embedded_dev/ (plug-in not installed), tried product_families.md (no row), tried 6 mirrors (alldatasheet no match, mouser no PDF, lcsc 404, vendor Cloudflare) — give up; see vendor URL`. Never invent a value.

### Step 5: Handle Uncertainty — Defaults First, Confirm Only When Reversible-Cost Is High

**Principle**: default to a reasonable assumption and proceed. The user came for a chip pick, not a questionnaire. Only stop to confirm when the cost of being wrong is high and irreversible.

**Decision rule** (apply per ambiguity dimension):

| Reversible-cost level | When | Skill behaviour |
|------------------------|------|------------------|
| **Low** (user can swap chip after seeing BOM cost) | Cost-sensitive product, prototype, hobby project | **Pick the conservative middle option silently. State assumption. Move on.** |
| **Medium** (swap = a few days of PCB rework) | Production design, mixed wireless, unknown volume | **Pick a sensible default, but flag as a confirm-once gate.** |
| **High** (swap = new certification, respin, $$$ tooling) | AEC-Q100 automotive, FDA medical, ATEX, regulatory-locked | **Ask the 1 most binding question before proceeding.** No default. |

**Always state the assumption** so the user can override. Format: `*[Assumed: BLE 5.x; tell me if you need Wi-Fi or Thread.]*`

**Do not ask questions when you can pick a sensible default.** The 7 ambiguity dimensions below all have a default:

| Dimension | Default if user is silent | Override trigger |
|-----------|---------------------------|-----------------|
| Power source | Li-Po, days–weeks | User says coin cell / USB / mains |
| Wireless protocol | BLE only | User mentions Wi-Fi, Thread, LoRa, cellular, or "no wireless" |
| BOM cost target | Balanced $5–20 | User says "cheap", "premium", or quotes a target |
| Sourcing preference | Domestic-friendly (mixed OK) | User says "China-domestic only" / "overseas only" |
| Operating environment | Indoor consumer 0–40°C | User says industrial / automotive / outdoor / extreme |
| Regulatory / certification | CE/FCC | User names SRRC / TELEC / KC / UL etc. |
| Production volume | 1k–100k | User says prototype / hobby / mass production |

**Only escalate to a question** when cost-of-being-wrong is **High** (AEC-Q100, FDA, ATEX), user said "ask me before assuming", or three defaults in a row contradict each other (USB-powered + 5-year battery + outdoor). **Ask one decision at a time** with enumerated a/b/c options (typically: wireless protocol + operating environment first). Don't batch 5 questions.

**If user says "you decide"**: pick the conservative middle default, state it, and proceed.

**Examples**:

*Low cost, default + state*: `"BLE 5.x single-chip (assumed; tell me if you need Wi-Fi/Thread)"` → Step 6 immediately.
*Medium cost, confirm-once*: `"Proceeding with (b) Li-Po + balanced cost; re-rank if your volume is <1k or >100k."`
*High cost, ask 1*: `"Automotive (-40..+125°C, AEC-Q100) — grade 2 (≤105°C Tj) or grade 1 (≤125°C Tj)? Changes the candidate list."`

### Step 6: Provide Solution — Top 3 + Comparison

By default, recommend the **top 3 most suitable candidates** with an explicit comparison, not a single pick. The user makes the final trade-off decision. Adapt the depth to the request: a quick "which BLE SoC?" can be 3 short bullets; a full BOM design should be a multi-row comparison table.

For each candidate in the top 3, output:

1. **Chip name and vendor product page URL** (from `references/semiconductor-vendor/<Vendor>/product_families.md`).
2. **Key parameters — already fetched by the skill** (cores, flash, RAM, wireless version, key current/voltage, package). Each value should carry a citation like `(32 KB RAM, p.12 datasheet rev 1.1, fetched 2026-06-27 from mouser.com/pdfDocs/stm32wb55cc.pdf)`. If a parameter could not be fetched, mark `not verified — tried st.com (Cloudflare), mouser/pdfDocs (no PDF), alldatasheet (no match)` so the user knows what was attempted. Do NOT leave the user to read the PDF themselves — that defeats the purpose of the skill.
3. **Why it's suitable** for the target application (1–2 sentences tied to the user's stated requirements).
4. **Trade-offs** vs the other two candidates (1–2 sentences — e.g. "lower cost but no integrated PMU").

Then include a **comparison table** spanning all three:

| Criterion | Candidate A | Candidate B | Candidate C |
|-----------|-------------|-------------|-------------|
| Vendor | ... | ... | ... |
| Key params (cores / flash / RAM / BLE ver) | ... | ... | ... |
| Fit for user's top 3 requirements | ... | ... | ... |
| Main trade-off | ... | ... | ... |
| Verification status | ✅ / ⏳ / ❌ / partial | ... | ... |

End with a **Source** line: link to each vendor's `product_families.md` entry and cite the datasheet page numbers used for verification.

**When fewer than 3 candidates are appropriate** (e.g. the BOM function has only 1–2 viable parts in the catalogue), present what exists and say so explicitly — do NOT pad with weak candidates to hit 3.


### Step 7: External / Out-of-Scope Lookup (after Tier 4 exhausted)

If Step 2 finds **no matching application-solution** AND Step 4's four-tier search (Tier 1 specs → Tier 2 local datasheet → Tier 3 product_families + vendor URL → Tier 4 external mirrors) has not surfaced a usable candidate, widen the search. Use the **cheapest source that can actually answer the question** — don't burn a web search when a vendor page will do.

This step is **after** the Search Priority 4-tier system has been fully walked. It is the last-resort fallback, not a substitute for Tier 4.

Escalate in this order, stopping at the first source that yields a usable answer:

1. **Vendor-published reference designs already linked from this skill** — `references/semiconductor-vendor/<Vendor>/system-solutions/` (single-vendor reference designs, see INDEX.md). Free, already curated.
2. **Third-party teardowns already linked from this skill** — `references/application-solution/<topic>/solution.md` "Third-party Sources" sections. Real-world observed BOMs.
3. **Web search** (e.g. `web_search` tool) — for the specific question ("DA14531 stock status 2026", "smart home gateway reference design"). Prefer vendor URLs and recognised distributors (Mouser, Digi-Key, LCSC) over forums.
4. **Component marketplaces** (Mouser, Digi-Key, LCSC) — for stock / price / lifecycle status when the user asks "can I buy it now?".
5. **Engineer community** (EEVblog, hackaday.io, element14) — for design intent and teardown observations when no official source covers it.

When you go outside the skill's curated files, **always cite the URL you used** so the user can verify. After widening the search, return to Step 6 (top 3 + comparison) — the output template does not change, only the source depth.

## Verification Before Responding

Before sending any result, run this checklist:

- [ ] Did I check `references/application-solution/INDEX.md` first?
- [ ] Does every chip in the BOM have a vendor product page URL from `references/semiconductor-vendor/<Vendor>/product_families.md`?
- [ ] Is every numerical parameter from a vendor datasheet (not from memory)?
- [ ] For any parameter I cannot find → did I explicitly write "not verified"?
- [ ] If the application has constraints I don't know → did I ask the user?
- [ ] Did I provide top 3 candidates with a comparison table (Step 6), not a single pick?
- [ ] If I went outside this skill's files (Step 7), did I cite the URL?
- [ ] For each parameter, did I follow the **4-tier Search Priority** and stop at the first tier that fully answers it? Citation should show which tier (Tier 1 specs YAML verified + recent / Tier 2 local datasheet / Tier 3 product_families.md + vendor URL fetch / Tier 4 external mirror).
