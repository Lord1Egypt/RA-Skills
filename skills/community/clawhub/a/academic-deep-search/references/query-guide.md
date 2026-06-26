# Query Guide

Use this file when you need more concrete search syntax or answer templates.

## Query Construction

### Biomedical Topics

Prefer:

- MeSH terms when available
- exact phrases in quotes
- journal filters only after confirming the indexed journal name
- small sets of synonyms rather than very broad keyword dumps

Example pattern:

```text
("concept A"[MeSH] OR "concept B"[MeSH])
AND "disease or condition"[MeSH]
AND "method or intervention"[MeSH]
```

### General Rules Across Databases

- use English search terms for the query itself
- use quotes for exact phrases
- use `AND`, `OR`, and `NOT` carefully
- verify field-tag syntax before assuming it works
- prefer native database filters over vague web searching

## Source Selection Heuristic

- PubMed or PMC: best default for biomedical questions
- Specific journal requested by user: restrict to that journal
- URL provided by user: read it directly first
- Other disciplines: use a field-appropriate database before general web search

## Reading Priorities

### Body Mode

Read:

- Methods
- Results
- Discussion when interpretation matters

Extract:

- experiment type
- markers or molecules
- direction of change
- sample or model context
- citation details

### Figure Mode

Read:

- figure captions
- the Results paragraphs that cite the figure

Extract:

- figure label or panel
- what the figure demonstrates
- caption wording or a concise paraphrase
- source metadata

## Output Templates

### Body Mode

```markdown
### Experiment Type: Western Blot

| Marker | Reported Change | Context | Reference |
|--------|------------------|---------|-----------|
| X | Increased | Mouse lung tissue | PMID/PMCID |

Sources: PMID1, PMID2
```

### Figure Mode

```markdown
[Paper Title] | [Journal] | [Year] | [PMID/PMCID/DOI]
Figure: Fig. 2A
What it shows: Brief explanation
Caption note: Short direct summary or careful paraphrase
Why it is representative: One sentence
```

## Failure Handling

If you cannot find enough evidence:

- say which databases were searched
- state whether full text was available
- explain whether the limitation was topic novelty, source restriction, or search-term ambiguity
- propose the next most sensible search adjustment
