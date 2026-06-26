---
name: biorxiv
version: 1.1.0
description: Access bioRxiv preprint repository for biology preprints. Use for: (1) Fetching recent preprints from specific categories like bioinformatics, genomics, molecular-biology, etc., (2) Getting papers by date range, (3) Listing available subject collections, (4) Retrieving paper metadata including titles, authors, DOIs, dates, and categories. No authentication required.
---

# bioRxiv Skill

This skill provides access to the bioRxiv preprint repository using the official bioRxiv API.

## When to Use

- User asks for recent biology preprints
- User wants papers from specific bioRxiv categories (bioinformatics, genomics, etc.)
- User needs paper metadata (title, authors, DOI, date, category)
- User asks for preprints from a specific date range

## Quick Start

### List Available Collections

```bash
python scripts/biorxiv.py --list
```

### Fetch Recent Papers

```bash
# Default: bioinformatics papers
python scripts/biorxiv.py --collection bioinformatics

# Other collections
python scripts/biorxiv.py --collection genomics
python scripts/biorxiv.py --collection neuroscience
python scripts/biorxiv.py --collection microbiology

# Specific date range
python scripts/biorxiv.py --collection bioinformatics --start 2026-03-01 --end 2026-03-09

# Limit results
python scripts/biorxiv.py --collection bioinformatics --limit 10
```

### Output as JSON

```bash
python scripts/biorxiv.py --collection bioinformatics --json
```

## Available Collections

- bioinformatics
- genomics
- molecular-biology
- cell-biology
- genetics
- evolutionary-biology
- ecology
- neuroscience
- plant-biology
- microbiology
- immunology
- cancer-biology
- biochemistry
- biophysics
- structural-biology
- systems-biology
- synthetic-biology
- developmental-biology
- computational-biology

## API Notes

### Official bioRxiv API
- **Base URL:** `https://api.biorxiv.org/details/biorxiv/{start_date}/{end_date}/{cursor}`
- **No authentication required**
- Returns up to 100 papers per call
- Supports category filtering via query parameter

### API Endpoints
- `/details/biorxiv/[start]/[end]/[cursor]` — Paper metadata
- `/pub/[start]/[end]/[cursor]` — Published articles only

## Usage Patterns

### Summarize Recent Papers

1. Fetch papers from desired collection
2. Parse titles and abstracts
3. Group by theme if multiple
4. Provide concise summary

### Find Papers by Topic

1. Search across multiple relevant collections
2. Filter by keywords in titles
3. Return most relevant results
