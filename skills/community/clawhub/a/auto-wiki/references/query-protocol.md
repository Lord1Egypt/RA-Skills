# Query Protocol

> Answer questions based on wiki accumulation. Not RAG—don't search raw documents, search compiled wiki pages.

## Flow

```
1. Understand question
   ├─ Identify target wiki (inferred from question, or user specified)
   ├─ Extract keywords (entity names, concept names, date ranges)
   └─ Determine question type (fact query / comparative analysis / trend judgment / open exploration)

2. Search wiki
   ├─ Read index.md, match page titles and descriptions by keywords
   ├─ Read matched pages (usually 3-8)
   ├─ If page has [[wikilink]], follow link to read related pages (one level expansion)
   └─ Note confidence field: contested pages need special labeling

3. Synthesize answer
   ├─ Synthesize based on read page content
   ├─ Label each key claim with source page: [[page-slug]]
   ├─ If involving contested info, clearly state:
   │   "On XX, wiki contains conflict: Source A says..., Source B says..."
   └─ If info insufficient, clearly state gap and suggest ingest direction

4. Optional archive
   ├─ If answer contains valuable new analysis (not simple repetition of page content)
   ├─ Prompt user: "Should this analysis be archived to wiki?"
   └─ User agrees → Write to analyses/{slug}.md, update index
```

## Response Format

### Fact Query

```
Based on {N} source files accumulated in wiki:

{Direct answer}

Sources: [[page-1]], [[page-2]]
```

### Comparative Analysis

```
Based on wiki records, comparison of {A} and {B}:

| Dimension | {A} | {B} |
|-----------|-----|-----|
| ... | ... | ... |

Sources: [[page-1]], [[page-2]], [[page-3]]

Note: On XX dimension, wiki data is limited (only 1 source), suggest supplement.
```

### Insufficient Information

```
Wiki information on {topic} is insufficient:
- Related pages: {N}
- Source files: {N}
- Gap: {specifically what's missing}

Suggest ingesting:
- {Suggested material type 1}
- {Suggested material type 2}
```

## Cross-Wiki Query

When question spans multiple wikis:

1. List all wiki directories under `.wiki/`
2. Read index.md of each potentially relevant wiki
3. Search separately
4. Label sources by wiki when synthesizing answer:

```
Synthesizing content from enterprise-annuity wiki and charlie-munger wiki:

{Analysis}

Sources:
- enterprise-annuity: [[alpha-corp]], [[fiduciary-responsibility]]
- charlie-munger: [[circle-of-competence]], [[margin-of-safety]]
```

## Query Performance

| Wiki Scale | Query Strategy | Expected Latency |
|------------|----------------|------------------|
| < 30 pages | Read index + directly read matched pages | Fast (< 5s) |
| 30-150 pages | Read index + grep keywords + read top matches | Medium (5-15s) |
| 150-500 pages | Read index + grep + batch read | Slow (15-30s) |
| > 500 pages | Beyond Skill design scope | Suggest migration to platform |
