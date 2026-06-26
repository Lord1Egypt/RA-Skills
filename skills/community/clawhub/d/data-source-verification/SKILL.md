---
name: data-source-verification
description: Verify numerical data against original papers and maintain traceable provenance for every value in datasets, tables, and plots. Includes citation source management, PDF-based verification, and audit reporting.
version: 2.0.0
homepage: https://github.com/Larry-of-cosmotim/data-source-verification
metadata:
  openclaw:
    emoji: 🔍
---

# Data Source Verification

A systematic workflow for verifying that every data point in a research dataset can be traced back to its original source paper, figure, table, or text passage.

## When to Use

- Building datasets from literature (CSV, JSON, tables)
- Populating tables or plots with values from multiple papers
- Reviewing existing datasets for data integrity
- Before submitting any paper that includes compiled data

## Core Rule

**Every numerical value must be traceable to a specific location in the original paper.** If you cannot find the value in the cited source, it is unverified and must be flagged — never included as confirmed data.

## Data Provenance Chain

```
Source PDF → CITATION.md (extracted values) → CSV/data table → LaTeX manuscript
```

Every link in this chain must be auditable. If someone asks "where did this number come from?", the answer should be: paper X, Table Y, column Z — and we have the PDF to prove it.

---

## Citation Source Management

### Project Setup (`init`)

Create a `Citation_Sources/` directory for the project:

```
Citation_Sources/
  AuthorLastName_Year_Journal_ShortTitle/
    Author_Year_Topic.pdf          ← original paper
    Author_Year_Topic_SI.pdf       ← supplementary info (if any)
    CITATION.md                    ← structured metadata + data provenance
```

### CITATION.md Template

Every cited paper gets a CITATION.md file:

```markdown
# Author et al. Year — Short Description
**Title**: Full title
**Authors**: Author list
**Journal**: Journal Vol, Pages (Year)
**DOI**: 10.xxxx/xxxxx
**Data used**: [exact values extracted, with table/figure reference]
**PDF**: ✅ Confirmed | ❌ NOT DOWNLOADED — [reason]
**Status**: CONFIRMED | ⚠️ NEEDS CONFIRM — [reason]
**Notes**: [any caveats, discrepancies, proxy assumptions]
```

### Adding a Source (`add`)

When adding a new citation:

1. Create the folder: `Citation_Sources/AuthorLastName_Year_Journal_ShortTitle/`
2. Download the original PDF — always try to get the actual paper, not just the abstract
3. Download supplementary information if it contains data
4. Create CITATION.md from the template
5. Extract the specific values you need, recording exact table/figure/page locations
6. Mark the PDF status and verification status

---

## Verification Workflow

### Step 1: Collect with Provenance

When extracting data from a paper, record ALL of the following for each value:

```
Value: 0.65 W/m·K
Paper: Cheng et al. 2021
DOI: 10.1002/smll.202101693
Location: Table 2, row 3
Method: TDTR (time-domain thermoreflectance)
Data type: Experimental
Verified: YES — value confirmed in Table 2
```

Never record a value without filling in the Location, Data type, and Verified fields.

### Step 2: Verify Against Original

For each data point:

1. **Always download the original PDF** — don't trust web scraping, abstracts, or secondary sources
2. **Find the exact value** in a table, figure, or text passage
3. **Record where you found it** — table number, figure number, page, equation
4. **Note the measurement method** — experimental technique, simulation, estimate
5. **Check units** — convert if needed, note the original units
6. **Track the data type**: DFT-calculated, experimentally measured, or derived (note assumptions)

If the paper is behind a paywall and you cannot verify:
- Mark as `⚠️ NEEDS CONFIRM — paywall`
- Note this limitation in CITATION.md

### Step 3: Cross-Check the Full Chain

Verify consistency at every step:

```
Value in PDF → Value in CITATION.md → Value in data table/CSV → Value in manuscript
```

Any mismatch at any step is a flag.

### Step 4: Flag Problems

Mark any value with one of these status levels:

| Status | Meaning | Action |
|---|---|---|
| `VERIFIED` | Found exact value in cited paper at stated location | Include in dataset |
| `APPROXIMATE` | Value is close but not exact (e.g., read from figure) | Include with note |
| `UNVERIFIED` | Cannot find value in cited paper | Flag — do not use without user approval |
| `MISATTRIBUTED` | Cited paper does not contain this data at all | Remove from dataset, alert user immediately |
| `ESTIMATED` | Value was calculated or estimated, not directly measured | Include with clear label |
| `⚠️ NEEDS CONFIRM` | PDF not available (paywall) or value needs double-check | Flag for manual verification |

### Step 5: Flag Discrepancies

When multiple sources report different values for the same quantity:
- Record both values with their sources
- Note the discrepancy explicitly (e.g., "B = 45 GPa (Author A, Table 2) vs B = 86 GPa (Author B, Fig. 3)")
- Check if the difference is due to measurement method, sample preparation, or temperature
- Let the user decide which value to use — do not silently pick one

---

## Dataset Format

When building compiled datasets, always include provenance columns:

**CSV format:**
```csv
Material,Property,Value,Unit,Source_Paper,DOI,Source_Location,Method,Data_Type,Verified,Notes
Li6PS5Cl,kappa,0.69,W/m·K,Cheng 2021,10.1002/smll.202101693,Table 2,TDTR,experimental,YES,
Li3InCl6,v_longitudinal,2800,m/s,Asano 2018,10.1002/adma.201803075,NOT FOUND,Unknown,unknown,MISATTRIBUTED,Paper contains no Li3InCl6 sound velocity data
```

**JSON format:**
```json
{
  "material": "Li6PS5Cl",
  "property": "thermal_conductivity",
  "value": 0.69,
  "unit": "W/m·K",
  "source": {
    "paper": "Cheng et al. 2021",
    "doi": "10.1002/smll.202101693",
    "location": "Table 2, row 5",
    "method": "TDTR",
    "dataType": "experimental",
    "verified": true
  }
}
```

---

## Audit Workflow (`audit`)

Scan all CITATION.md files and generate a report:

1. **List all unique sources** in Citation_Sources/
2. **For each source**, check:
   - PDF downloaded? (✅ or ❌)
   - CITATION.md complete? (all fields filled)
   - Values confirmed against PDF?
3. **Generate audit summary:**

```markdown
## Audit Report — [Project Name]
Date: [timestamp]

### Summary
- Total sources: [N]
- PDFs confirmed: [N] / [N]
- Values verified: [N] / [N]
- Needs confirmation: [N]
- Missing PDFs: [N]

### Source Details

| Paper | PDF | Values | Verified | Status |
|---|---|---|---|---|
| Cheng 2021 | ✅ | 3 | 3/3 | CONFIRMED |
| Asano 2018 | ✅ | 2 | 1/2 | ⚠️ 1 MISATTRIBUTED |
| Wang 2014 | ❌ | 4 | 0/4 | ⚠️ NEEDS CONFIRM |

### Flagged Values
- Li3InCl6 v_longitudinal: MISATTRIBUTED to Asano 2018 — paper contains no LIC data
- LGPS density: conflicting values (2.0 vs 1.9 g/cm³) between Wang 2014 and Kamaya 2011
```

4. **Report findings** — list verified, flagged, and misattributed values
5. **Recommend action** for each flagged value

---

## Export (`export`)

Generate a summary table of all data values and their provenance:

```markdown
## Data Provenance Summary — [Project Name]

| Material | Property | Value | Unit | Source | Location | Data Type | Status |
|---|---|---|---|---|---|---|---|
| LLZTO | κ | 0.42 | W/m·K | Muy 2019 | Table 1 | experimental | VERIFIED |
| LAGP | v_avg | 4700 | m/s | Rohde 2021 | Table S2 | experimental | VERIFIED |
| Li3InCl6 | v_avg | 1849 | m/s | Qiu 2025 | Table 1 | DFT | VERIFIED |
```

---

## Red Flags

Watch for these indicators of unreliable data:

- Value attributed to a paper but no specific table/figure cited
- "Estimated from family properties" without a clear methodology
- Values that appear in reviews but cannot be traced to original measurements
- Round numbers that suggest estimation rather than measurement (e.g., 2800 m/s vs 2837 m/s)
- Same value appearing in multiple papers without independent measurement
- DFT values presented as experimental without noting the distinction
- Discrepancies between different sources for the same quantity left unaddressed

## Rules

1. **Never assume a citation is correct** — always verify against the original paper
2. **Always download the PDF** — don't trust abstracts, web scraping, or secondary sources
3. **Secondary sources are not verification** — a review paper citing a value does not confirm it
4. **Flag immediately** when a value cannot be found in its cited source
5. **Track data type** — distinguish DFT-calculated, experimentally measured, and derived values
6. **Flag discrepancies** — when two sources disagree, note both values and let the user decide
7. **Prefer measured over estimated** — clearly label the difference
8. **Document everything** — future researchers need the audit trail
9. **When in doubt, exclude** — a smaller verified dataset beats a larger unverified one
