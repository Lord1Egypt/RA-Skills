# Research Methodology Reference

## Table of Contents
1. [Question Decomposition](#question-decomposition)
2. [Search Strategy Matrix](#search-strategy-matrix)
3. [Source Evaluation Framework](#source-evaluation-framework)
4. [Synthesis Patterns](#synthesis-patterns)
5. [Bias Checklist](#bias-checklist)
6. [Report Templates](#report-templates)

---

## Question Decomposition

### The PICO Framework (adapted for general research)
- **P**opulation/Problem: What is being studied?
- **I**ntervention/Input: What change, action, or factor is being examined?
- **C**omparison: What is it being compared to?
- **O**utcome: What are the expected results or effects?

### Decomposition Patterns

**Causal questions** ("Why does X happen?"):
1. What is X precisely? (definition)
2. What are the proposed mechanisms? (how)
3. What evidence supports each mechanism? (evidence)
4. What alternative explanations exist? (alternatives)
5. What is the current expert consensus? (consensus)

**Comparative questions** ("Which is better, X or Y?"):
1. What are X and Y precisely? (definitions)
2. What criteria matter for comparison? (dimensions)
3. How does each perform on each criterion? (data)
4. What are the tradeoffs? (analysis)
5. Under what conditions does each excel? (context)

**Predictive questions** ("What will happen with X?"):
1. What is the current state of X? (baseline)
2. What trends are visible? (trajectory)
3. What do experts predict? (forecasts)
4. What are the key uncertainties? (risks)
5. What historical analogies apply? (precedent)

**Exploratory questions** ("What is X?"):
1. How is X defined? (definition)
2. What is its history/origin? (context)
3. What are its key components? (structure)
4. How does it relate to adjacent concepts? (connections)
5. What is its current state and trajectory? (status)

---

## Search Strategy Matrix

| Research depth | Searches | Fetches | Time budget | Sources target |
|---------------|----------|---------|-------------|----------------|
| Quick         | 3-5      | 2-3     | 2-3 min     | 3-5            |
| Standard      | 8-15     | 5-10    | 5-10 min    | 8-15           |
| Deep          | 20-40    | 10-20   | 15-30 min   | 15-30          |
| Exhaustive    | 50+      | 20+     | 30-60 min   | 30+            |

### Search Angle Rotation

For each sub-question, rotate through these angles:

1. **Direct:** The question as-is
2. **Academic:** Add "research", "study", "paper", "review"
3. **Practical:** Add "how to", "guide", "tutorial", "example"
4. **Critical:** Add "problems with", "criticism", "limitations", "risks"
5. **Quantitative:** Add "data", "statistics", "numbers", "benchmark"
6. **Expert:** Add "expert opinion", specific known authorities in the field
7. **Recent:** Use freshness:"week" or freshness:"month"
8. **Historical:** Use date_before for baseline comparisons

### Domain-Specific Search Strategies

**Technology/Software:**
- Search Hacker News discussions: `site:news.ycombinator.com <topic>`
- Search GitHub: `site:github.com <topic>`
- Search Stack Overflow: `site:stackoverflow.com <topic>`
- Check official docs: `site:<product-domain> <feature>`

**Science/Medicine:**
- PubMed/NCBI: `site:ncbi.nlm.nih.gov <topic>`
- Nature/Science: `site:nature.com OR site:science.org <topic>`
- Preprints: `site:arxiv.org OR site:biorxiv.org <topic>`

**Business/Market:**
- Industry reports: `<topic> "market size" OR "market share" OR "industry report"`
- Company filings: `<company> "10-K" OR "annual report" OR "earnings"`
- Analyst coverage: `<topic> "analyst" OR "forecast" OR "outlook"`

**Policy/Regulation:**
- Government sources: `site:*.gov <topic>`
- Think tanks: `<topic> "policy brief" OR "white paper"`
- Legal: `<topic> "regulation" OR "legislation" OR "compliance"`

---

## Source Evaluation Framework

### CRAAP Test (Currency, Relevance, Authority, Accuracy, Purpose)

| Criterion   | Questions to ask |
|------------|-----------------|
| Currency   | When was it published? Updated? Are links functional? |
| Relevance  | Does it address the research question? At what depth? |
| Authority  | Who is the author? What are their credentials? Who publishes the source? |
| Accuracy   | Is it supported by evidence? Has it been peer-reviewed? Can claims be verified? |
| Purpose    | Why does this exist? Inform, persuade, sell, entertain? Any bias? |

### Source Classification

**Primary sources:** Original research, raw data, official documents, firsthand accounts
**Secondary sources:** Analysis of primary sources, review articles, textbooks, news coverage
**Tertiary sources:** Encyclopedias, indexes, databases that compile from secondary sources

### Red Flags

- No author attribution
- No date or very old date on time-sensitive topics
- Emotional language without supporting evidence
- Claims without citations
- Circular citations (A cites B which cites A)
- Conflicts of interest (vendor writing about own product)
- Sample size issues in studies
- Survivorship bias in case studies

---

## Synthesis Patterns

### Convergence Pattern
When multiple independent sources agree:
> "Multiple independent analyses converge on [finding]. [Source A] found X through [method], while [Source B] independently confirmed X via [different method]. [Source C] provides additional support through [yet another approach]."

### Divergence Pattern
When sources disagree:
> "Evidence on [topic] is mixed. [Source A] argues X based on [evidence], while [Source B] contends Y due to [different evidence]. The disagreement appears to stem from [methodological difference / different definitions / different time periods / different populations]."

### Evolution Pattern
When understanding has changed over time:
> "The consensus on [topic] has shifted. Early work by [Source A, date] suggested X. However, [Source B, later date] challenged this by demonstrating Y. Current understanding, as reflected in [Source C, recent], now holds that Z."

### Gap Pattern
When information is incomplete:
> "While [what is known] is well-established ([sources]), [what remains unknown] has not been adequately addressed in available literature. This gap matters because [why it matters]."

---

## Bias Checklist

Before finalizing any report, check for these biases:

- [ ] **Confirmation bias:** Did I weight sources that confirm my initial hypothesis more heavily?
- [ ] **Recency bias:** Did I overweight recent sources at the expense of foundational work?
- [ ] **Authority bias:** Did I accept claims from prestigious sources without scrutiny?
- [ ] **Availability bias:** Did I rely on easily-found sources over harder-to-find but more relevant ones?
- [ ] **Selection bias:** Did my search terms inadvertently exclude relevant perspectives?
- [ ] **Anchoring:** Did the first source I found disproportionately shape my conclusions?
- [ ] **Publication bias:** Am I missing null results or negative findings?
- [ ] **Geographic/cultural bias:** Did I only search in English / from one cultural perspective?
- [ ] **Survivor bias:** Am I only seeing successful examples?
- [ ] **Dunning-Kruger:** Am I overconfident in an area where I lack deep expertise?

---

## Report Templates

### Quick Report Template

```markdown
# <Title>

**Date:** YYYY-MM-DD | **Depth:** quick | **Confidence:** HIGH/MEDIUM/LOW

## Answer
<Direct answer in 2-3 sentences>

## Key Evidence
- <Point 1> [1]
- <Point 2> [2]
- <Point 3> [3]

## Caveats
<What could change this answer>

## Sources
[1] ...
[2] ...
[3] ...
```

### Standard Report Template

```markdown
# Research Report: <Title>

**Date:** YYYY-MM-DD
**Depth:** standard
**Confidence:** HIGH/MEDIUM/LOW

## Executive Summary
<2-5 sentences>

## Key Findings

### 1. <Finding headline>
<Explanation with citations [n]>
**Confidence:** HIGH/MEDIUM/LOW

### 2. <Finding headline>
...

## Counterarguments & Limitations
...

## Sources
[1] Title — URL (date)
...
```

### Deep/Exhaustive Report Template

```markdown
# Research Report: <Title>

**Date:** YYYY-MM-DD
**Depth:** deep/exhaustive
**Confidence:** HIGH/MEDIUM/LOW
**Tags:** tag1, tag2

## Executive Summary
<3-5 sentences>

## Background & Context
<Why this question matters, what prompted it>

## Methodology
<Search strategy, sources consulted, date range, limitations>

## Key Findings

### 1. <Finding headline>
<Detailed explanation with inline citations>
**Confidence:** HIGH/MEDIUM/LOW
**Evidence quality:** <note on source types and strength>

### 2. <Finding headline>
...

## Analysis & Interpretation
<What the findings mean together, patterns, implications>

## Counterarguments & Alternative Interpretations
<Steelmanned opposing views>

## Knowledge Gaps & Future Questions
<What remains unknown, what would change the conclusions>

## Recommendations (if applicable)
<Actionable next steps based on findings>

## Appendix
### A. Detailed Source Evaluation
### B. Search Queries Used
### C. Rejected Sources & Reasons

## Sources
[1] Title — URL (date, author)
...
```
