# Deep Researcher — Research Workflow
## 7-Stage Pipeline for 30-40 Page Academic Papers

---

## OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 1: TOPIC ANALYSIS    →  STAGE 2: SOURCE DISCOVERY            │
│  STAGE 3: CONTENT SYNTHESIS →  STAGE 4: CROSS-VERIFICATION           │
│  STAGE 5: CONTENT EXPANSION →  STAGE 6: SYNTHESIS & WRITING         │
│  STAGE 7: REFINEMENT & QA                                              │
└─────────────────────────────────────────────────────────────────────┘
```

Each stage feeds the next. Iteration loops return to earlier stages when triggered.

---

## STAGE 1: TOPIC ANALYSIS

**Objective**: Understand the full breadth and depth of the topic before writing.

1.1 **Validate** — Confirm the topic is researchable in 30-40 pages. Check if sufficient sources exist. Flag if too narrow/broad.
1.2 **Deconstruct** — Extract primary and secondary research questions. Identify scope boundaries (time period, geography, industry).
1.3 **Define success** — What does "comprehensive" mean for this topic? Map to paper objectives.
1.4 **Knowledge check** — Note known seminal works, key theories, current debates.

**Output**: Topic Deconstruction Report (subtopics, research questions, knowledge gaps).

---

## STAGE 2: SOURCE DISCOVERY

**Objective**: Map all available sources across a wide spectrum of databases.

2.1 **Database matrix** — Academic (arXiv, PubMed, IEEE), Economic (World Bank, IMF, OECD), Industry (McKinsey, Gartner), News, Government, Code (GitHub, Hugging Face).
2.2 **Keyword expansion** — Generate 20-30 semantic variants of core terms. Include synonyms, jargon, related field terms.
2.3 **Execute searches** — Use Boolean operators: `(concept A) AND (concept B) NOT (concept C)`. Apply year filters (last 3-10 years).
2.4 **Quality triage** — Flag sources by authority tier (A: peer-reviewed, B: major industry, C: news/web). Bookmark top 100.

**Output**: Source Mapping Document, Keyword Expansion List, Top 50 indexed sources.

---

## STAGE 3: CONTENT SYNTHESIS

**Objective**: Read, digest, and extract key insights from sources.

3.1 **Categorize** — Group sources by theme, methodology, geography, year. Assign to chapter sections.
3.2 **Extract per source**: Core contribution, methodology, key findings (3-5 bullets), limitations.
3.3 **Pattern recognition** — Identify recurring themes, evolution of thinking over time, areas of consensus vs. controversy.
3.4 **Summarize** — 150-200 word summary per source, tagged with concept-area and source type.

**Output**: Synthesized Source Notes (40-60 sources), Cross-reference Map, Draft Literature Review.

---

## STAGE 4: CROSS-VERIFICATION

**Objective**: Ensure information is accurate, diverse, and hallucination-free.

4.1 **Fact-check** — Cross-check all factual claims against ≥2 independent sources. Verify statistics, dates, specific numbers.
4.2 **Triangulate** — Critical insights must have 3+ corroborating sources. Identify areas of disagreement.
4.3 **Bias detection** — Flag if most sources lean one direction. Note potential conflicts of interest.
4.4 **Gap ID** — What key insights are missing? What perspectives are underrepresented?

**Output**: Verification Log, Triangulation Matrix, Bias Assessment.

---

## STAGE 5: CONTENT EXPANSION

**Objective**: Deepen research to fill 30-40 pages with high-quality content.

5.1 **Extended mining** — Return to keyword list, search uncovered angles. Focus on case studies, comparative analyses, historical precedents.
5.2 **Data augmentation** — Add quantitative metrics from World Bank, IMF, OECD datasets.
5.3 **Expert content** — Thought leaders, conference keynotes, public analysis.
5.4 **Comparative research** — Cross-industry, cross-country, cross-time comparisons.

**Output**: Expanded Source List (+10-20 sources), Comparative Analysis, Historical Timeline.

---

## STAGE 6: SYNTHESIS & WRITING

**Objective**: Assemble a coherent, chapter-by-chapter manuscript.

6.1 **Map to template** — Use the 12-section paper structure. Ensure logical flow from background to conclusion.
6.2 **Allocate content** — Map synthesized notes to specific chapter sections. Target 3-4 distinct themes per chapter.
6.3 **Draft** — Write section by section. Maintain formal academic tone. Every claim linked to a source with APA citation.
6.4 **Integrate** — Review transitions. Ensure no repetition. Add tables, figures, diagrams where they clarify content.

**Output**: Full Draft Manuscript (30-40 pages), Chapter Structure Map.

---

## STAGE 7: REFINEMENT & CITATION

**Objective**: Final polish — formatting, citations, quality assurance.

7.1 **Format citations** — Apply APA 7th Edition to all references. Generate proper DOI links.
7.2 **Compile references** — Master list of 40-80 unique sources, alphabetically by author.
7.3 **Run QA checks** — Check length, citation integrity, formatting consistency, logical gaps.
7.4 **Final format** — Ensure page count within range, consistent font/margins/spacing.

**Output**: Final Published Paper + Quality Assurance Report.

---

## ITERATION LOOPS

| Trigger | Action |
|---------|--------|
| Verification reveals hallucination | Return Stage 4 → Stage 3 |
| Critical gaps found in coverage | Return Stage 5 → Stage 2 |
| Writing reveals missing sources | Return Stage 6 → Stage 4 |
| Page count <30 pages | Expand Stage 5, revisit Stage 6 |
| Citation coverage <40 | Return Stage 7 → Stage 2 |

---

## OUTPUT QUALITY TARGETS

| Metric | Target |
|--------|--------|
| Word count | 15,000-18,000 words |
| Unique sources | 40-80 |
| Source types | 4+ different databases |
| Citation density | ≥1 per 150-200 words |
| Source recency | 70%+ from last 5 years |
| Page range | 30-40 pages |