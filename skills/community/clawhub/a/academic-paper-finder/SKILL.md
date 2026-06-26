---
name: academic-paper-finder
description: |
  Search biomedical literature, get citation counts, and import to Zotero/EndNote. Use when: 
  (1) User asks to search for papers/literature by DOI, title, author, or keywords
  (2) User wants to find papers with citation counts and Chinese summaries
  (3) User wants to import papers to Zotero by PMID/DOI
  (4) User wants to generate RIS file for EndNote
  (5) User provides a research topic and wants to find relevant authoritative papers
---

# Academic Paper Finder

Search PubMed and import papers to Zotero or generate RIS file for EndNote.

## Setup

Requires environment variables:
- `ZOTERO_API_KEY` - Zotero API key (from https://www.zotero.org/settings/keys/new)
- `ZOTERO_USER_ID` - Your Zotero user ID

## Quick Start

### 1. Search Paper by DOI

```bash
python3 scripts/pubmed_search.py --doi "10.1016/j.cell.2014.07.013"
```

### 2. Search by Title

```bash
python3 scripts/pubmed_search.py --title "circulating tumor cell clusters"
```

### 3. Search by Author

```bash
python3 scripts/pubmed_search.py --author "Aceto N" --year 2014
```

### 4. Add to Zotero

```bash
# By PMID
python3 scripts/zotero_add.py --pmid 25171411

# By DOI
python3 scripts/zotero_add.py --doi "10.1016/j.cell.2014.07.013"
```

### 5. Batch Import (Multiple PMIDs)

```bash
python3 scripts/batch_import.py --pmids "25171411,30728496,41212905"
```

### 6. Generate RIS for EndNote

```bash
python3 scripts/generate_ris.py --pmids "25171411,30728496" --output literature.ris
```

## Scripts

- `pubmed_search.py` - Search PubMed by DOI/title/author
- `zotero_add.py` - Add paper to Zotero by PMID/DOI
- `batch_import.py` - Batch add multiple papers
- `generate_ris.py` - Generate RIS file for EndNote

## Examples

### Get PMID from Citation

When user provides a citation like:
```
Aceto, N.; Bardia, A.; Miyamoto, D. T.; Donaldson, M. C.; Wittner, B. S.; Spencer, J. A.; Yu, M.; Pely, A.; Ting, K.; Haber, D. A.; Maheswaran, S. Circulating Tumor Cell Clusters Are Oligoclonal Precursors of Breast Cancer Metastasis. Cell 2014, 158 (5), 1110–1122. https://doi.org/10.1016/j.cell.2014.07.013.
```

1. Extract DOI: `10.1016/j.cell.2014.07.013`
2. Search: `python3 scripts/pubmed_search.py --doi "10.1016/j.cell.2014.07.013"`
3. Result: PMID 25171411
4. Add to Zotero: `python3 scripts/zotero_add.py --pmid 25171411`

### Batch Import for EndNote

User has multiple papers and wants to import to EndNote:

```bash
# List all PMIDs
python3 scripts/generate_ris.py --pmids "25171411,30728496,41212905,41651843,19945376" --output my_papers.ris
```

Then import the RIS file to EndNote: File → Import → Select .ris file.
