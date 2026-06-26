# NCBI E-utilities API Reference

## Overview

NCBI provides E-utilities for programmatic access to their databases. Free, no authentication required for reasonable usage (~10 req/s).

Docs: https://www.ncbi.nlm.nih.gov/home/develop/api/

## Key Endpoints

### 1. GEO Datasets — ESearch + ESummary

**Database name is `gds`** (NOT `gse` — `gse` is the accession prefix only).

**ESearch** (search): `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
```
?db=gds
&term={keywords}
&retmax=20
&sort=relevance
&retmode=json
```

**ESummary** (details): `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi`
```
?db=gds
&id={gds_id1},{gds_id2},...
&retmode=json
```

Key response fields:
- `accession` — the GSE prefix ID (e.g. `GSE123456`) ✅ use this as dataset ID
- `uid` — internal numeric ID (do NOT use as dataset ID)
- `pubmedids` — list of PubMed IDs (may be empty)
- `title` — dataset title
- `summary` — dataset description
- `taxon` — species

### 2. SRA — ESearch + ELink

**ESearch** (search): `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
```
?db=sra
&term={keywords}
&retmax=20
&retmode=json
```

**ELink** (to BioProject/PubMed): `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi`
```
?dbfrom=sra
&id={srp_id}
&linkname=bioproject_sra
&retmode=json
```

### 3. PubMed — ESearch + ESummary

Get article info by PMCID or DOI:
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={doi}&retmode=json
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json
```

## Query Building

Combine keywords with AND/OR:
```
({disease}) AND ({treatment}) AND ({species}) AND ({data_type}) AND ("single cell"[Data Type])
```

Examples:
```
"colon cancer" AND "immunotherapy" AND "human" AND "scRNA-seq"
"hepatocellular carcinoma" AND "PD-1" AND "single cell"
"dMMR" AND "colon cancer" AND "scRNA"
```

## Rate Limiting

- ~10 requests/second max
- Add `&usehistory=y` for large result sets
- Include User-Agent header

## Response Parsing

GEO ESummary response:
```json
{
  "result": {
    "uids": ["GSE123456"],
    "GSE123456": {
      "title": "...",
      "summary": "...",
      "overall_design": "...",
      "pubmed_id": "12345678",
      "gse_type": "Expression profiling by high throughput sequencing"
    }
  }
}
```

## Common Dataset Types

| Type | NCBI Database | Prefix |
|------|--------------|--------|
| Gene expression | GEO | GSE |
| Raw reads | SRA | SRP/SRR |
| Whole genome | SRA | PRJNA |
| Single-cell | SRA/GEO | GSE/SRP |
| Methylation | GEO | GSE |
| Proteomics | PRIDE | PXD |

## Tips

1. GEO datasets with scRNA-seq often have "single cell" or "scRNA" in title/summary
2. SRA Run Selector: `https://www.ncbi.nlm.nih.gov/Traces/study/` for download links
3. For single-cell data, also check SRA's single-cell portal
4. Link to GEO dataset: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={GSE}`
5. Link to SRA study: `https://www.ncbi.nlm.nih.gov/bioproject/{PRJNA}`
