---
name: biomed-dataset-finder
description: "Search NCBI GEO/SRA, NGDC-GSA, and CNGB for biomedical datasets by disease, treatment, species, pathology subtype, and data type. Returns bold dataset ID, links, and article info in a structured table."
---

# Biomedical Dataset Finder

Search public biomedical datasets from NCBI, NGDC, and CNGB by conversational query keywords.

## Usage Trigger

User asks for datasets related to a disease/treatment/species/subtype/data type combination. Examples:
- "Find colon cancer dMMR immunotherapy single-cell data"
- "hepatocellular carcinoma PD-1 scRNA-seq baseline"
- "lung cancer immunotherapy single cell data"

## Data Sources (Priority Order)

| Priority | Source | Database | Accession Prefix |
|----------|--------|----------|-----------------|
| 1st | NCBI | GEO Datasets (gds) | GSE |
| 1st | NCBI | SRA (single-cell queries) | SRP/SRR |
| 1st | NGDC | Genome Sequence Archive | CRA |
| 2nd | CNGB | CNGBdb | CNP (requires token for some data) |

## Workflow

### Step 1 — Parse Query

Extract from user message:
- **Disease/Cancer**: e.g. colon cancer, hepatocellular carcinoma, lung cancer
- **Treatment**: e.g. immunotherapy, PD-1, chemotherapy, baseline therapy
- **Species**: human, mouse (defaults to human if unspecified)
- **Pathology Subtype**: e.g. dMMR, MSI-H, KRAS mutant
- **Data Type**: e.g. scRNA-seq, single-cell, RNA-seq, ChIP-seq, ATAC-seq

If any critical field is missing, ask the user to clarify.

### Step 2 — NCBI Search (Primary)

Use NCBI E-utilities (free, no auth).

1. Search `gds` database (GEO Datasets, NOT `gse`) with combined keywords
2. For each result, pull `accession` (GSE prefix), title, summary, and `pubmedids` (list)
3. Fetch article info (authors, title, journal, year, DOI) for each PMID
4. For single-cell queries, also search `sra` database

Query: `({disease}) AND ({treatment}) AND ({species}) AND ({data_type})`

**Rate limit:** ~3 requests/second.

### Step 3 — NGDC Search (Primary)

API: `https://ngdc.cncb.ac.cn/search/api/specific?q={keywords}&db=gsa&size=20`

Requires `User-Agent` header. Filter response for `type=="GSA"` entries (CRA accessions).

### Step 4 — CNGB Search (Secondary)

If CNGB token provided: search CNGBdb API.
On auth error: ask user if they want to provide token or skip.

### Step 5 — Output

Markdown table with **bold dataset ID**, article info (authors, title, journal, year, DOI), and direct links.

**If no results:** "No public datasets found matching your criteria. Try adjusting keywords or switching data sources."

## Factuality Requirements (Critical — No Hallucinations)

This skill handles scientific research data. **Fabricating a single dataset entry undermines the user's work.**

### Hard Rules

1. **Dataset IDs**: Only use IDs returned by actual API responses. Never invent, guess, or infer IDs.
2. **Article info**: Only populate from actual API/PubMed responses. Leave blank if no data returned.
3. **Links**: Build from verified accession patterns (e.g. `https://.../acc.cgi?acc={GSE}`). Never guess URLs.
4. **"Not found" is valid**: If a source returns 0 results, output the empty result — do not fabricate entries to fill the table.

### Verification Checklist (before presenting results)

- [ ] Every Dataset ID is from an API response, not memory or guess
- [ ] Every Article Title + Authors + Journal is from a PubMed/API response, not reconstructed
- [ ] Every Link follows the confirmed URL pattern for that database
- [ ] If a field is empty in the API response, it must be blank `-` in the table — never fill with plausible text

### Why This Matters

A researcher using wrong dataset IDs or fake article info could: waste weeks on non-existent data, cite non-existent papers, or compromise the validity of their research. The cost of hallucination here is far higher than in general conversation.

## Security Notes

- **User keywords are private** — do NOT log the raw search query string to stderr/stdout. Log only counts (e.g. "Searching 5 keywords...").
- **Token handling** — CNGB token is passed via CLI arg only; never hardcode or log it.
- **No external exfiltration** — results table contains only public dataset metadata; no user-provided content is stored or transmitted elsewhere.

## CLI Tool

```bash
python3 skills/biomed-dataset-finder/scripts/search_datasets.py \
  --disease "colon cancer" --treatment "immunotherapy" \
  --species human --subtype dMMR --type scRNA-seq --max-results 10
```

## API Reference

See `references/ncbi_api.md` for NCBI E-utilities details.
See `references/ngdc_api.md` for NGDC GSA API details.
See `references/cngb_api.md` for CNGBdb API details.