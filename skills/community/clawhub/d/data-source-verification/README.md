# Data Source Verification

A systematic workflow skill for verifying that every data point in a research dataset can be traced back to its original source paper. Built from real-world experience managing 66+ data points across 11 materials in a solid electrolyte thermal review paper.

## The Problem

When compiling data from multiple papers into tables, plots, or datasets, values can get misattributed — cited to a paper that doesn't actually contain that data. This can propagate through analysis and into publications undetected.

## What This Skill Does

- **Citation source management** — organized folder structure with PDFs, supplementary info, and CITATION.md metadata per paper
- **Provenance tracking** — every value records: paper, DOI, table/figure number, method, data type (DFT/experimental/derived), verification status
- **Full-chain verification** — PDF → CITATION.md → CSV/data table → manuscript, auditable at every step
- **Discrepancy flagging** — when two sources disagree on a value, both are recorded for user decision
- **Source audit** — scan all citations, report verified vs. needs-confirm vs. missing PDFs
- **Export** — generate provenance summary tables for all data values
- **Red flag detection** — identifies indicators of unreliable or estimated data

## Commands

| Command | Description |
|---|---|
| `init` | Set up Citation_Sources/ directory structure |
| `add <DOI or URL>` | Download PDF, create folder + CITATION.md template |
| `verify <material or value>` | Check that a value traces back to a confirmed PDF |
| `audit` | Scan all citations, report confirmation status |
| `export` | Generate summary table of all values + provenance |

## Installation

### ClawHub
```bash
clawhub install data-source-verification
```

### Manual
Copy `SKILL.md` into your agent's `skills/data-source-verification/` directory.

## Usage

Ask your agent:
- "Set up citation sources for the thermal review paper"
- "Add this DOI and extract the thermal conductivity data"
- "Verify all data sources in the Cahill plot CSV"
- "Run an audit on all citations — which PDFs are missing?"
- "Export a provenance summary for all 11 materials"
- "Check if Asano 2018 actually contains Li₃InCl₆ sound velocity data"

## License

MIT
