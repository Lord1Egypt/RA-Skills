---
name: deep-researcher
description: "Generate comprehensive 30-40 page academic research papers with full citations. Trigger: deep research, generate research paper, academic paper, literature review, research report, 30-40 page paper, comprehensive analysis, full citations, scholarly work."
metadata:
  builtin_skill_version: "1.1"
  openclaw_native: true
  replaces: knowledge-digest
  triggers:
    - "deep research"
    - "generate research paper"
    - "academic paper"
    - "literature review"
    - "research report"
    - "comprehensive analysis"
    - "scholarly paper"
    - "long research paper"
    - "research paper 30 pages"
    - "full citations research"
---

# Deep Researcher — Academic Research Paper Generator

Generate comprehensive, academic-grade research papers (30-40 pages) with 40-80 unique citations, following a rigorous 7-stage workflow. Adapts to any field — AI, medicine, economics, social sciences, engineering, and more.

## Workflow Overview

```
STAGE 1: Topic Analysis      → Decompose topic into sub-questions
STAGE 2: Source Discovery    → Query academic & industry databases
STAGE 3: Content Synthesis  → Extract, summarize, map source relationships
STAGE 4: Cross-Verification  → Triangulate claims, verify facts
STAGE 5: Content Expansion   → Fill gaps, add case studies, data
STAGE 6: Synthesis & Writing → Assemble paper chapter-by-chapter
STAGE 7: Refinement & QA     → Polish, format citations, validate
```

---

## Stage 1: Topic Analysis

Decompose the research topic into 12-15 subtopics. Identify:
- Primary research questions
- Scope boundaries (time period, geography, industry)
- Feasibility for 30-40 page scope
- Key theories and seminal works to anchor the paper

**Output**: Topic Deconstruction Report with subtopics, research questions, and knowledge gaps.

---

## Stage 2: Source Discovery

Query multiple source categories using OpenClaw's native tools:

| Category | Sources | Tool |
|----------|---------|------|
| Academic | arXiv, Google Scholar, PubMed, Semantic Scholar | `batch_web_search` |
| Economic | World Bank API, IMF, OECD Stats | `batch_web_search` |
| Industry | McKinsey Insights, Statista, Gartner | `batch_web_search` + `extract_content_from_websites` |
| Code/AI | GitHub, Hugging Face, arXiv (CS) | `batch_web_search` |
| News | Reuters, BBC, RSS feeds | `batch_web_search` |
| Patents | Google Patents | `batch_web_search` |

**Tool**: `batch_web_search` (up to 10 concurrent queries)

For each search, extract: title, authors, year, DOI/URL, abstract, key findings.

**Output**: 40-80 candidate sources organized by category and relevance.

---

## Stage 3: Content Synthesis

For each major source:
- Extract core contribution, methodology, key findings (3-5 bullet points), limitations
- Group by theme, methodology, and chapter alignment
- Identify patterns: recurring themes, contradictions, gaps

**Output**: Synthesized source notes (150-200 words per source), cross-reference map, draft literature review.

---

## Stage 4: Cross-Verification

- Every factual claim must be backed by ≥1 source
- Critical claims (statistics, dates, specific findings) verified against 2-3 independent sources
- Flag sources with potential bias or industry funding
- Identify underrepresented perspectives

**Output**: Verification log, triangulation matrix, bias assessment.

---

## Stage 5: Content Expansion

- Search for case studies, historical precedents, comparative analyses
- Add quantitative data from World Bank, IMF, OECD where relevant
- Include expert viewpoints, industry reports, conference proceedings
- Aim for 15-20 distinct subtopics covered

**Output**: Expanded source list (+10-20 sources), comparative analysis, historical timeline.

---

## Stage 6: Synthesis & Writing

Assemble the paper using the **Standard Research Paper Structure** below. Integrate citations in APA 7th format. Write 15,000-18,000 words targeting 30-40 pages.

### Standard Research Paper Structure

```
1. Title Page          (clear title, keywords, date)
2. Abstract            (300-500 words, 3-5 keywords)
3. Executive Summary   (1-2 pages, key takeaways for decision-makers)
4. Chapter 1: Introduction        (3-4 pages)
   - Background & context
   - Problem statement
   - Research objectives & questions
   - Significance & scope
5. Chapter 2: Literature Review   (6-8 pages)
   - Theoretical framework
   - Key themes (organized thematically)
   - Major studies & seminal works
   - Gaps in existing research
6. Chapter 3: Methodology         (4-5 pages)
   - Research design (qualitative/quantitative/mixed)
   - Data sources & search strategy
   - Inclusion/exclusion criteria
   - Analysis techniques & AI tools used
7. Chapter 4: Data Collection     (3-4 pages)
   - Sample/data description
   - Collection procedures
   - Ethical considerations
8. Chapter 5: Analysis & Findings  (8-10 pages)
   - Descriptive findings
   - Quantitative/qualitative results
   - Comparative and longitudinal analysis
   - Visual elements (tables, figures)
9. Chapter 6: Discussion          (3-4 pages)
   - Interpretation of key findings
   - Theoretical & practical implications
   - Limitations & counterarguments
10. Chapter 7: Conclusion         (2-3 pages)
    - Summary of contributions
    - Actionable recommendations
    - Future research directions
11. References                    (5-8 pages, 40-80 sources)
12. Appendices                    (optional)
```

**Citation style**: APA 7th Edition (Author, Year) — default. Also supports MLA 9th and Chicago Notes/Bibliography.

---

## Stage 7: Refinement & QA

Run the quality checklist:

### Accuracy
- [ ] 0% hallucinated claims — every claim backed by ≥1 source
- [ ] All statistics cross-checked against primary sources
- [ ] All dates within ±1 day of source
- [ ] All DOIs resolve correctly

### Completeness
- [ ] 30-40 page target (15,000-18,000 words)
- [ ] ≥40 unique citations
- [ ] 15-20 distinct subtopics covered
- [ ] All 7 chapters present
- [ ] 5+ figures/tables

### Coverage
- [ ] 4+ different source types (academic, industry, news, government)
- [ ] 70%+ sources from last 5 years
- [ ] 3+ distinct viewpoints represented
- [ ] At least 1 counterargument documented

### Citation Integrity
- [ ] All in-text citations appear in References
- [ ] All References have in-text citations
- [ ] No orphan URLs
- [ ] APA 7th formatting consistent throughout

### Literary Quality
- [ ] Formal academic tone, no slang
- [ ] Third-person perspective
- [ ] Clear transitions between chapters
- [ ] No repetition or redundancy
- [ ] Consistent terminology

**Output**: Final polished paper + QA report

---

## Output Formats

| Format | Description | Tool |
|--------|-------------|------|
| **Markdown** | Default, editable | Direct output |
| **PDF** | Academic submission | `minimax-pdf` skill |
| **DOCX** | Word processing | `minimax-docx` skill |

Request with: `"[topic] — output as PDF"` or `"[topic] — output as DOCX"`

---

## APA 7th Citation Quick Reference

**In-text**: `(Author, Year)` or `Author (Year) showed that...`

**Reference entry (Journal)**:
```
Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), Page.Range. https://doi.org/xxxxx
```

**Reference entry (Book)**:
```
Author, A. A. (Year). Title of book (Edition ed.). Publisher.
```

**Reference entry (Web)**:
```
Author, A. A. (Year, Month Day). Title of page. Website Name. https://url
```

---

## Citation Density Rule

Target: ≥1 citation per 150-200 words across the full paper. This ensures every claim is evidence-backed and academically rigorous.

---

## Source Priority Matrix

| Priority | Source Types | Cost |
|----------|-------------|------|
| **HIGH** | arXiv, PubMed, World Bank, IMF, OECD, Hugging Face, GitHub | Free |
| **MEDIUM** | Google Scholar, IEEE, McKinsey, Gartner, Statista | Free/Premium |
| **LOW** | News feeds, Twitter, Reddit, news blogs | Free |

Always prioritize free, authoritative, open-access sources first.

---

## Data Sources Registry

### Academic
- **arXiv**: `https://export.arxiv.org/api/query` — cutting-edge AI/ML/theory, no API key
- **Google Scholar**: `batch_web_search` — comprehensive peer-reviewed coverage
- **PubMed/PMC**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` — biomedical, life sciences
- **Semantic Scholar**: `https://api.semanticscholar.org/` — CS academic sources

### Economic & Policy
- **World Bank**: `https://api.worldbank.org/v2/` — free, no key required
- **IMF**: `https://api.imf.org/` — macroeconomic data
- **OECD**: `https://stats.oecd.org/` — comparative policy data

### Technology & AI
- **Hugging Face**: `https://api.huggingface.co/` — ML models, datasets, papers
- **GitHub API**: `https://api.github.com/` — code trends, repositories
- **Google Patents**: `https://patents.google.com/` — innovation trends

### Industry
- **McKinsey Insights**: Public articles and reports
- **Gartner**: Industry analysis (subscription)
- **Statista**: Statistics and market data (subscription)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Insufficient sources" | Expand keyword list; use Boolean operators (AND/OR/NOT); try alternative databases |
| "Page count too short" | Expand Stage 5 (content expansion); add case studies, comparative data, visual elements |
| "Citation gaps" | Return to Stage 2; search for missing angles; add industry reports and government data |
| "Hallucination risk" | Always verify facts via Cross-Verification stage; cite primary sources only |
| "Formatting inconsistent" | Run APA 7th reference check; ensure all in-text citations match reference list |

---

## Iteration Triggers

- **From Stage 4 → Stage 3**: Cross-verification reveals hallucination or insufficient evidence
- **From Stage 5 → Stage 2**: Expansion search finds critical gaps in core coverage
- **From Stage 6 → Stage 4**: Writing reveals missing critical sources
- **Page count <30**: Expand Stage 5, then revisit Stage 6

---

## Integration Notes

This skill replaces and significantly extends the `knowledge-digest` skill's research capabilities. Where knowledge-digest focuses on learning materials from existing documents, deep-researcher generates original academic research from primary and secondary sources across multiple databases.

Both skills can coexist — use `deep-researcher` for original paper creation, `knowledge-digest` for study aids from existing materials.