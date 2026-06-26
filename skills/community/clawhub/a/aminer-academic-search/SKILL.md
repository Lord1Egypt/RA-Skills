---
name: aminer-data-search
version: 1.0.0
description: >
  Academic data search and analysis using AMiner Open Platform APIs. Query scholars,
  papers, institutions, journals, and patents. Includes 6 composite workflows
  (Scholar Profile, Paper Deep Dive, Org Analysis, Venue Papers, Paper QA, Patent 
  Analysis) and 28 individual APIs.
  Triggers: "AMiner", "学术数据", "查论文", "查学者", "学术搜索",
  "academic search", "paper search", "scholar lookup", "citation analysis".
tags: [academic, research, aminer, scholar, paper, journal, patent, citation, chinese, english]
env:
  AMINER_TOKEN: "AMiner API Token (from https://open.aminer.cn/open/board?tab=control)"
---

# AMiner Academic Data Search (学术数据查询)

[AMiner](https://aminer.cn) is a leading global academic data platform. This skill covers all 28 open APIs organized into 6 practical workflows for comprehensive academic research.

- **API Docs**: https://open.aminer.cn/open/doc
- **Console (Token)**: https://open.aminer.cn/open/board?tab=control

---

## Getting Started

### 1. Get API Token
1. Visit [AMiner Console](https://open.aminer.cn/open/board?tab=control)
2. Login and generate an API Token
3. Token goes in `Authorization` header for all requests

### 2. Quick Usage
```bash
# Scholar profile analysis
python scripts/aminer_client.py --token <TOKEN> --action scholar_profile --name "Andrew Ng"

# Paper deep dive (with citation chain)
python scripts/aminer_client.py --token <TOKEN> --action paper_deep_dive --title "Attention is all you need"

# Organization analysis
python scripts/aminer_client.py --token <TOKEN> --action org_analysis --org "清华大学"

# Venue/journal paper monitoring
python scripts/aminer_client.py --token <TOKEN> --action venue_papers --venue "Nature" --year 2024

# Academic Q&A (natural language)
python scripts/aminer_client.py --token <TOKEN> --action paper_qa --query "transformer架构最新进展"

# Patent search
python scripts/aminer_client.py --token <TOKEN> --action patent_search --query "量子计算"
```

---

## Reliability & Error Handling

Built-in resilience:
- **Timeout**: 30s default
- **Retries**: Max 3 with exponential backoff (1s → 2s → 4s) + jitter
- **Retryable**: `408 / 429 / 500 / 502 / 503 / 504`
- **Degradation**: `paper_deep_dive` auto-falls back to `paper_search_pro`; `paper_qa` degrades to `paper_search_pro`
- **Traceability**: Composite workflow output includes `source_api_chain`

---

## Paper Search API Selection Guide

| API | Focus | Use Case | Cost |
|-----|-------|----------|------|
| `paper_search` | Title lookup → `paper_id` | Known paper title | Free |
| `paper_search_pro` | Multi-condition search | Filter by author/org/venue | ¥0.01 |
| `paper_qa_search` | Natural language Q&A | Semantic search | ¥0.05 |
| `paper_list_by_search_venue` | Rich paper info | Analysis/reports | ¥0.30 |
| `paper_list_by_keywords` | Multi-keyword batch | Topic batch retrieval | ¥0.10 |
| `paper_detail_by_condition` | Year + venue filter | Annual venue monitoring | ¥0.20 |

**Recommended routing**:
1. Known title → `paper_search` → `paper_detail` → `paper_relation`
2. Condition filter → `paper_search_pro` → `paper_detail`
3. Natural language → `paper_qa_search` (fallback: `paper_search_pro`)
4. Venue analysis → `venue_search` → `venue_paper_relation` → `paper_detail_by_condition`

---

## 6 Composite Workflows

### 1. Scholar Profile (学者全景分析)
**Use**: Complete academic profile of a scholar.

```
Scholar Search (name → person_id)
    ↓
Parallel:
  ├── Scholar Detail (bio/education/honors)
  ├── Scholar Figure (research areas/interests)
  ├── Scholar Papers (publication list)
  ├── Scholar Patents (patent list)
  └── Scholar Projects (grants/funding)
```

```bash
python scripts/aminer_client.py --token <TOKEN> --action scholar_profile --name "Yann LeCun"
```

### 2. Paper Deep Dive (论文深度挖掘)
**Use**: Full paper info + citation chain.

```
Paper Search (title → paper_id)
    ↓
Paper Detail (abstract/authors/DOI/venue/year)
    ↓
Paper Citations (cited papers → cited_ids)
    ↓
(Optional) Batch paper info for cited papers
```

```bash
python scripts/aminer_client.py --token <TOKEN> --action paper_deep_dive --title "BERT"
```

### 3. Organization Analysis (机构研究力分析)
**Use**: Analyze an institution's research capabilities.

```
Org Disambiguation Pro (raw string → org_id)
    ↓
Parallel:
  ├── Org Detail (intro/type/founded)
  ├── Org Scholars (scholar list)
  ├── Org Papers (paper list)
  └── Org Patents (patent list, up to 10k)
```

```bash
python scripts/aminer_client.py --token <TOKEN> --action org_analysis --org "MIT"
```

### 4. Venue Papers (期刊论文监控)
**Use**: Track papers from a specific journal/venue by year.

```
Venue Search (name → venue_id)
    ↓
Venue Detail (ISSN/type/abbreviation)
    ↓
Venue Papers (venue_id + year → paper_ids)
    ↓
(Optional) Batch paper details
```

```bash
python scripts/aminer_client.py --token <TOKEN> --action venue_papers --venue "NeurIPS" --year 2023
```

### 5. Paper Q&A (学术智能问答)
**Use**: Natural language academic search.

Supports: `query` (natural language), `topic_high/middle/low` (keyword weights), `sci_flag`, `force_citation_sort`, `author_terms`, `org_terms`.

```bash
python scripts/aminer_client.py --token <TOKEN> --action paper_qa \
  --query "用于蛋白质结构预测的深度学习方法"
```

### 6. Patent Analysis (专利链分析)
**Use**: Search patents by technology domain.

```
Patent Search (query → patent_id)
    ↓
Patent Detail (abstract/filing date/assignee/inventor)
```

```bash
python scripts/aminer_client.py --token <TOKEN> --action patent_search --query "量子计算芯片"
```

---

## Full API Reference

| # | API | Method | Cost | Path |
|---|-----|--------|------|------|
| 1 | Paper QA Search | POST | ¥0.05 | `/api/paper/qa/search` |
| 2 | Scholar Search | POST | Free | `/api/person/search` |
| 3 | Paper Search | GET | Free | `/api/paper/search` |
| 4 | Paper Search Pro | GET | ¥0.01 | `/api/paper/search/pro` |
| 5 | Patent Search | POST | Free | `/api/patent/search` |
| 6 | Org Search | POST | Free | `/api/organization/search` |
| 7 | Venue Search | POST | Free | `/api/venue/search` |
| 8 | Scholar Detail | GET | ¥1.00 | `/api/person/detail` |
| 9 | Scholar Projects | GET | ¥3.00 | `/api/project/person/v3/open` |
| 10 | Scholar Papers | GET | ¥1.50 | `/api/person/paper/relation` |
| 11 | Scholar Patents | GET | ¥1.50 | `/api/person/patent/relation` |
| 12 | Scholar Figure | GET | ¥0.50 | `/api/person/figure` |
| 13 | Paper Info | POST | Free | `/api/paper/info` |
| 14 | Paper Detail | GET | ¥0.01 | `/api/paper/detail` |
| 15 | Paper Citation | GET | ¥0.10 | `/api/paper/relation` |
| 16 | Patent Info | GET | Free | `/api/patent/info` |
| 17 | Patent Detail | GET | ¥0.01 | `/api/patent/detail` |
| 18 | Org Detail | POST | ¥0.01 | `/api/organization/detail` |
| 19 | Org Patents | GET | ¥0.10 | `/api/organization/patent/relation` |
| 20 | Org Scholars | GET | ¥0.50 | `/api/organization/person/relation` |
| 21 | Org Papers | GET | ¥0.10 | `/api/organization/paper/relation` |
| 22 | Venue Detail | POST | ¥0.20 | `/api/venue/detail` |
| 23 | Venue Papers | POST | ¥0.10 | `/api/venue/paper/relation` |
| 24 | Org Disambiguation | POST | ¥0.01 | `/api/organization/na` |
| 25 | Org Disambiguation Pro | POST | ¥0.05 | `/api/organization/na/pro` |
| 26 | Paper Search (venue) | GET | ¥0.30 | `/api/paper/list/by/search/venue` |
| 27 | Paper Batch (keywords) | GET | ¥0.10 | `/api/paper/list/citation/by/keywords` |
| 28 | Paper Detail (condition) | GET | ¥0.20 | `/api/paper/platform/allpubs/more/detail/by/ts/org/venue` |

**Base URL**: `https://datacenter.aminer.cn/gateway/open_platform`

---

## References

- Official Docs: https://open.aminer.cn/open/doc
- Console: https://open.aminer.cn/open/board?tab=control
