# NGDC GSA API Reference

## Overview

NGDC (National Genomics Data Center / China National Center for Bioinformation): https://ngdc.cncb.ac.cn

Core database: **GSA** (Genome Sequence Archive) — accession prefix `CRA`.

Docs: https://ngdc.cncb.ac.cn/gsa

## Search API

**Endpoint:** `https://ngdc.cncb.ac.cn/search/api/specific`

```
GET https://ngdc.cncb.ac.cn/search/api/specific?q={keywords}&db=gsa&size=20
```

**Headers:** Must include `User-Agent` header (server closes connection without it).

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `q` | Search keywords | "colon cancer scRNA-seq" |
| `db` | Database name | `gsa` (Genome Sequence Archive) |
| `size` | Max results | 20 |
| `start` | Offset (default 0) | 0 |
| `sort` | Sort field (default `score`) | `score`, `recent` |

### Response Format

```json
{
  "code": "200",
  "result": {
    "data": {
      "draw": 1,
      "recordsTotal": 4326,
      "recordsFiltered": 4326,
      "data": [
        {
          "id": "CRA026056",
          "type": "GSA",
          "title": "The scRNA-Seq analysis for the effect of...",
          "url": "https://ngdc.cncb.ac.cn/gsa/browse/CRA026056",
          "attrs": {
            "Release date": "2026-03-26",
            "Center": "GSA",
            "Organization": "Soochow University",
            "Accession": "CRA026056",
            "BioProject": "PRJCA038888"
          }
        }
      ]
    }
  }
}
```

### Filtering

Only entries with `"type": "GSA"` are actual GSA datasets (CRA accessions).
Other types (`Run`, `Experiment`) are raw read records, not datasets.

## Dataset Link Format

- GSA dataset: `https://ngdc.cncb.ac.cn/gsa/browse/{CRA_ID}`
- Download: `https://ngdc.cncb.ac.cn/gsa/download/{CRA_ID}`

## Article / Metadata

GSA entries link to BioProject via `attrs.BioProject` (e.g. `PRJCA038888`).
Cross-reference with NCBI or PubMed for article info.

## Rate Limiting

- No explicit rate limit documented
- Use standard politeness (~1 req/s between calls)
- Include `User-Agent` header to avoid connection drops

## Tips

1. **CRA IDs** are the GSA equivalent of NCBI GSE — these are the primary dataset IDs
2. Search works for Chinese and English keywords
3. For single-cell data, include "scRNA-seq" in query
4. GSA entries often have Chinese institutional affiliations
5. `recordsTotal` tells you total matching results for pagination