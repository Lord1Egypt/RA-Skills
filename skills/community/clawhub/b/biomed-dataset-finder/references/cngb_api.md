# CNGBdb API Reference

## Overview

CNGB (China National GeneBank) DataBank: https://db.cngb.org

Provides access to Chinese population genetic data, biomedical datasets, and biodiversity data.

Docs: https://db.cngb.org/api

## Authentication

- **Public data**: No token required
- **Controlled-access data**: Requires CNGB token
- **If token required**: Ask user if they want to provide token or skip CNGB search

## Search API

**Base URL:** `https://db.cngb.org/api`

### Dataset Search

```
GET https://db.cngb.org/api/search/dataset
?q={keywords}
&type={data_type}
&species={species}
&page=1
&size=20
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `q` | Search keywords | "colon cancer immunotherapy" |
| `type` | Data type filter | scRNA-seq, RNA-seq, WGS |
| `species` | Species | homo sapiens, mus musculus |
| `page` | Page number | 1 |
| `size` | Results per page | 20 |

### Project Search

```
GET https://db.cngb.org/api/search/project
?q={keywords}
&organism={species}
```

## Response Format

```json
{
  "data": [
    {
      "project_id": "CNP0001234",
      "title": "...",
      "description": "...",
      "organism": "Homo sapiens",
      "data_type": "scRNA-seq",
      "sample_count": 50,
      "pubmed_id": "12345678",
      "doi": "10.xxxx",
      "create_time": "2023-01-01"
    }
  ],
  "total": 100
}
```

## Dataset Link Format

- CNGB Project: `https://db.cngb.org/project/{project_id}`
- Download: `https://db.cngb.org/datastore/download/{project_id}`

## NGDC (National Genomics Data Center)

Also worth checking as complementary Chinese database:
- **URL:** https://ngdc.cncb.ac.cn
- **Databases:** GSA, BioProject China, GENAGE
- **API:** https://ngdc.cncb.ac.cn/api

### GSA Search

```
GET https://ngdc.cncb.ac.cn/gsa/api/search
?q={keywords}
&type=bioproject
```

## Tips

1. CNGB datasets often have Chinese research collaborators
2. Check both CNGB and NGDC for comprehensive Chinese dataset coverage
3. CNGB project IDs typically start with "CNP" prefix
4. NGDC GSA datasets link to BioProject China
