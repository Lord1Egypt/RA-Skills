# Detailed Workflow

## Step 1: Anchor identification

**Goal**: Identify the core paper(s), researcher(s), and technology domain.

**Forward direction**:
1. Given a researcher name or paper, locate their representative paper(s):
   - Google Scholar author profile → sort by citations
   - If a specific paper is named, use that directly
   - Target: 1-3 anchor papers that best represent the core technology
2. Extract metadata: title, authors, affiliations, year, abstract, key metrics reported
3. Identify the technology domain and core technical problem being solved

**Reverse direction**:
1. Given a company name, find its academic footprint:
   - Search for papers authored by company founders/CTO/key researchers
   - Search for papers that the company's patents cite as prior art
   - Look for university affiliations of founders (LinkedIn, company website, news)
2. From the company's academic footprint, select 1-3 anchor papers
3. Same metadata extraction as forward direction

**Output**: Anchor paper list + researcher profile + technology domain definition

## Step 2: Backward citation mining

**Goal**: Find prior art and earlier researchers in the same technology lineage.

**Operations**:
1. Extract all references from the anchor paper:
   - Semantic Scholar API: `https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references`
   - Google Scholar: "Cited by" section → manually review
   - Web of Science: Cited References
2. Focus on references that are:
   - Same technology domain (not general methodology references)
   - From different research groups (not self-citations)
   - Published within a relevant time window (typically 2-10 years before anchor paper)
3. For key backward references, extract: who published earlier? what performance did they achieve? did their approach differ fundamentally?

**Special case — Literature Review mining**:
The anchor paper's literature review section often explicitly compares against prior work. This is THE richest source of competitor identification — the authors themselves tell you who they consider competitors. Extract every named prior work from the introduction and related-work sections.

**Output**: Backward citation list + timeline of prior art + identified earlier researchers

## Step 3: Forward citation mining

**Goal**: Find researchers who built on the anchor paper's work.

**Operations**:
1. Get all papers that cite the anchor paper:
   - Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations`
   - Google Scholar: "Cited by N" link
2. Filter by:
   - Publication date (focus on recent 2-5 years for active competitors)
   - Citation count of citing paper (highly-cited citing papers = strong signal)
   - Author overlap (exclude self-citations and same-group papers)
3. For high-signal citing papers, extract: institution, research group, performance metrics, whether they improved on the anchor paper's results

**Signal strength indicators**:
- Citing paper explicitly compares against anchor paper's results → **strong** competitor signal
- Citing paper uses anchor paper's method as baseline → **medium** signal
- Citing paper mentions anchor paper only in background → **weak** signal (filtered out in Step 4)

**Output**: Forward citation list + identified posterior researchers + improvement indicators

## Step 4: Similarity filtering

**Goal**: Filter the combined backward+forward citation pool to retain only genuine technology competitors.

**Not all citations are competitors.** Many papers cite the anchor paper for tangential reasons (shared methodology, general background, same journal). This step separates signal from noise.

**Filtering criteria** (score each paper 0-3, keep ≥2):

| Criterion | Score 2 | Score 1 | Score 0 |
|-----------|---------|---------|---------|
| Technology overlap | Same technical problem + same approach family | Same problem, different approach | Different problem |
| Performance comparison | Explicitly compares metrics against anchor | Mentions anchor results in passing | No comparison |
| Improvement claim | Claims better performance than anchor | Shows comparable performance | Shows worse or no comparison |
| Research group independence | Different institution + no co-authors with anchor group | Same institution, different group | Same group (self-citation) |

**Filter**: Total score ≥ 4 (out of 8 max) → retain as competitor candidate.

**Output**: Filtered competitor candidate list with similarity scores

## Step 5: Performance & timeline benchmarking

**Goal**: Compare key performance metrics across all competitor candidates. Place them on a technology maturity timeline.

**Operations**:
1. Extract reported performance metrics from each paper (the specific metric depends on domain — e.g., conversion efficiency, insertion loss, bandwidth, accuracy)
2. Build a comparison table:

| Researcher | Institution | Year | Key Metric | vs Anchor | Trend |
|-----------|-------------|------|------------|-----------|-------|
| Anchor (Chen) | UESTC | 2018 | Loss 0.5dB | — | — |
| Researcher B (Bo) | PKU | 2020 | Loss 0.3dB | **Better** | ↑ |
| Researcher C | ZJU | 2021 | Loss 0.45dB | Comparable | → |

3. Timeline analysis:
   - Who published first? (priority claim)
   - Who achieved best performance? (technology lead)
   - Whose performance is improving fastest? (momentum)
   - Gap analysis: how far behind/ahead is each competitor?

**Output**: Performance comparison table + timeline visualization + gap analysis

## Step 6: Author-to-company mapping

**Goal**: For each high-scoring competitor candidate, verify commercialization status.

**Operations** (for each researcher):

1. **Patent search**:
   - Search researcher name + institution in PatSnap / tushare / Google Patents
   - Check if patents overlap with the technology domain
   - Patent-to-paper timeline: did they patent before or after publishing?

2. **Company registration**:
   - Search researcher name in Tianyancha / Qichacha
   - Check for legal entities where researcher is 法定代表人/股东/高管
   - Cross-reference company business scope with technology domain

3. **Funding & investment**:
   - WebSearch: "[researcher name] 融资" / "[researcher name] 创业" / "[researcher name] startup"
   - Check 36Kr, ITjuzi, Crunchbase for company profiles
   - University technology transfer office announcements

4. **Product/ commercialization signals**:
   - Company website, product pages
   - Conference demos, trade show participation
   - Customer announcements, partnership news

**Commercialization status levels**:
- **Level 0**: Papers only, no patents or company
- **Level 1**: Papers + patents filed, no company
- **Level 2**: Company registered, no product/funding announced
- **Level 3**: Company + funding raised, pre-product
- **Level 4**: Product launched, customers announced

**Output**: Per-researcher commercialization profile + status level

## Step 7: Competitor matrix output

**Goal**: Synthesize findings into a strategic competitor intelligence report.

**Competitor positioning matrix** (2x2):

```
Technology Maturity (x-axis: low → high)
                  ↑
Commercialization  |  "Lab Rival"          |  "Imminent Threat"
Progress           |  (strong papers,      |  (papers + patents +
(y-axis)           |   no commercialization)|  company + funding)
                  |------------------------|
                  |  "Dormant"             |  "Academic Leader"
                  |  (old papers,          |  (highly cited,
                  |   no recent activity)  |   no commercialization)
                  └────────────────────────────────────────→
```

**Report sections**:
1. **Executive summary**: Top 3 competitors ranked by threat level
2. **Anchor profile**: The target paper/researcher/company summary
3. **Citation graph overview**: N backward + M forward → K after filtering
4. **Competitor profiles** (per competitor):
   - Researcher identity + institution
   - Key papers + performance metrics
   - Patent portfolio summary
   - Commercialization status + evidence
   - Technology positioning (better/worse/different approach)
   - Threat assessment (high/medium/low)
5. **Timeline visualization**: Publication/commercialization timeline
6. **Competitor matrix**: 2x2 positioning of all candidates
7. **Follow-up recommendations**: Which competitors to monitor, what signals to watch for

---

# Directional Variations

## Forward-direction specifics

- Start from paper/professor → competitors are hidden in citation network
- Backward mining is MORE important (who did this earlier?)
- Key question: "Who else is solving this same problem?"
- Example: 陈开鑫 2018 阶梯型 SSC → backward finds earlier work → forward finds 薄方 2020 楔形 SSC

## Reverse-direction specifics

- Start from company → first find academic footprint, then trace citations
- Forward mining is MORE important (who is building on the company's foundational research?)
- Key question: "Which academic groups could challenge this company's technology in 2-5 years?"
- Example: Given company founded by 薄方 → find 陈开鑫's earlier work through backward tracing from 薄方's papers
