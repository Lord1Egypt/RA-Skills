# AISEACT Detailed Workflow

This document provides the complete AISEACT workflow, a reusable methodology guide.

---

## Workflow Overview

```
Phase 0: Search Strategy Planning ← Most Critical! Think before searching
    ↓
Phase 1: Round 1 Search - Broad Collection (identify reliable sources)
    ↓
Phase 2: Assessment and Gap Analysis ← Determines Round 2 direction
    ↓
Phase 3: Round 2 Search - Targeted Supplement (find primary sources)
    ↓
Phase 4: Primary Source Validation + Cross-Validation
    ↓
Phase 5: Logical Closure Check
    ↓
Phase 6: Answer Generation (standardized citation)
```

---

## Phase 0: Search Strategy Planning (Think before searching!)

**Core Principle**: Do not search immediately! Spend 1-2 minutes planning strategy first.

### 0.1 Problem Decomposition

Decompose user questions into information requirement lists:

| Decomposition Dimension | Analysis Points |
|------------------------|-----------------|
| **Core Need** | What does the user really want to know? |
| **Information Type** | Need factual data? Comparative analysis? Operation guide? |
| **Time Requirements** | Need latest information or historical background? |
| **Depth Requirements** | Need overview or in-depth analysis? |

**Example Thought Process**:
> User asks: "What makes Entity A successful, and how does it differ from Entity B?"
> 
> Decomposition:
> - Entity A's core advantages/success factors
> - Entity A's basic situation
> - Entity B's basic situation
> - Comparison dimensions between the two (need to establish comparison framework)

### 0.2 Source Prediction

Predict where primary sources are most likely to be found:

| Information Type | Likely Primary Sources | Search Strategy |
|------------------|------------------------|-----------------|
| Company/Organization info | Official website, announcements, annual reports | site:official_domain / site:disclosure_platform |
| Policies/Regulations | Government official websites | site:gov.cn / site:relevant_ministry_domain |
| Technical info | Official documentation, GitHub | site:docs_domain / site:github.com |
| Academic info | Academic databases | database_name + keywords |

### 0.3 Search Round Planning

**Round 1 Search**:
- **Objective**: Broad collection, understand situation, identify reliable sources
- **Keywords**: Core topic words
- **Expected Output**: Candidate source list, preliminary information framework

**Round 2 Search**:
- **Objective**: Targeted supplementation, find primary sources
- **Keywords**: site:limitation + specific information types
- **Expected Output**: Official documents, official data

**Round 3 (if necessary)**:
- **Objective**: Deep verification, cross-validate key information
- **Trigger**: Key information has disputes or needs additional confirmation

### 0.4 Filtering Strategy

**Explicitly excluded source types**:
- Content farms (百家号, 搜狐号, etc.)
- Unattributed scraper sites
- Obviously rewritten self-media
- Machine-translated websites

---

## Phase 1: Round 1 Search - Broad Collection

### 1.1 Execute Search

**Strategy**: Use multiple keyword combinations to collect candidate sources.

**Keyword Combination Principles**:
- Core topic words
- Core topic + attribute words (official website, announcement, whitepaper)
- English keywords (for cleaner results)

### 1.2 Result Filtering (Critical!)

**Immediately exclude URL patterns**:
- Content farm domains
- Self-media platforms (non-verified accounts)
- Websites without clear source identification

**Priority click URL patterns**:
- Official website domains
- Government domains (gov.cn/gov)
- Information disclosure platforms
- Academic databases
- Technology official repositories

### 1.3 Information Extraction

Record the following information:

| Field | Description |
|-------|-------------|
| Information Point | Specific information obtained |
| Source URL | Complete link |
| Credibility Rating | 5-star assessment |
| Is Primary | Whether it's a primary source |
| Notes | Needs verification/supplementation |

### 1.4 Output

- Candidate source list (preliminarily filtered)
- Obtained information point list
- Preliminarily identified information gaps

---

## Phase 2: Assessment and Gap Analysis

### 2.1 Credibility Assessment

**Rating Standards** (5-star scale):

| Rating | Standard | Citation Advice |
|--------|----------|-----------------|
| ⭐⭐⭐⭐⭐ | Primary official source | Can prioritize citation |
| ⭐⭐⭐⭐ | Authoritative media original | Can cite with confidence |
| ⭐⭐⭐ | General media/analysis | Needs cross-validation |
| ⭐⭐ | Self-media/UGC | Try to avoid |
| ⭐ | Content farm | Prohibited |

### 2.2 Information Gap Identification

**Checklist**:
- [ ] Is key data obtained?
- [ ] Is there official source support?
- [ ] Are comparison dimensions complete?
- [ ] Is the timeline clear?
- [ ] Is cross-validation needed?

**Gap Classification**:

| Gap Type | Handling Strategy |
|----------|-------------------|
| Data missing | Round 2 search for official data |
| Primary source missing | Trace to original source |
| Validation missing | Find additional independent sources |
| Contradictory info | Assess source authority, or present multiple perspectives |

### 2.3 Round 2 Search Planning

Plan specific search strategies for each gap:

| Gap | Search Strategy | Expected Source Type |
|-----|-----------------|---------------------|
| [Specific gap] | [Search syntax] | [Expected source] |

---

## Phase 3: Round 2 Search - Targeted Supplement

### 3.1 Execute Targeted Search

**Use precise search syntax** to directly locate primary sources:

**General Search Patterns**:

```
# Mode 1: Limit to official domain
target_name site:official_domain

# Mode 2: Limit document type
target_name filetype:pdf

# Mode 3: Limit to disclosure platform
target_name announcement/report site:disclosure_platform

# Mode 4: English search
target_name official document/report
```

### 3.2 Primary Source Extraction

**Extract key information from official documents**:

| Document Type | Extraction Points |
|---------------|-------------------|
| Prospectus/Annual Report | Financial data, business model, market position, risk factors |
| Technical Whitepaper | Technical architecture, core advantages, product specifications |
| Official Announcement | Major events, strategic adjustments, latest developments |
| Policy Document | Specific clauses, applicable scope, implementation time |

### 3.3 Secondary Source Tracing

**Tracing Methods**:
1. Check citation links in secondary articles
2. Search for data sources mentioned in the article
3. Directly search data keywords + official source limitations

**Tracing Example Thought**:
> A media article mentions "30% market share"
> 
> Tracing search:
> - "market share 30%" + site:disclosure_platform
> - Find original data in prospectus or annual report

---

## Phase 4: Primary Source Validation

### 4.1 Primary Source Completeness Check

**Check Matrix**:

| Information Type | Has Primary Source | Source | Quality Assessment |
|------------------|-------------------|--------|-------------------|
| [Type 1] | Yes/No | [Source] | [Assessment] |
| [Type 2] | Yes/No | [Source] | [Assessment] |

### 4.2 Cross-Validation Execution

**Validation Standards**:
- **Key data**: At least 2-3 independent sources
- **Important claims**: At least 1 primary source + 1 independent report
- **Controversial info**: Present multiple perspectives

**Validation Method**:
1. Find multiple sources for the same information
2. Compare if information is consistent
3. If inconsistent, analyze reasons for differences
4. Prioritize primary sources

### 4.3 Contradiction Handling

**Handling process when source contradictions are found**:

1. **Check time dimension**
   - Has information been updated?
   - Prioritize latest official data

2. **Assess source authority**
   - Primary official source > Authoritative media > General media

3. **Present controversy**
   - Honestly explain different opinions exist
   - List different sources and bases
   - Provide judgment rationale (if determinable)

---

## Phase 5: Logical Closure Check

### 5.1 Answer Completeness Check

**Coverage Check**:
- [ ] All aspects of user question covered
- [ ] All sub-questions have information support
- [ ] Comparison dimensions complete (if applicable)

**Support Check**:
- [ ] Every conclusion has source labeling
- [ ] Data, facts have specific sources
- [ ] Opinions and facts distinguished

### 5.2 Information Quality Check

**Source Quality**:
- [ ] No content farm sources
- [ ] No unverified self-media
- [ ] Sufficient primary source proportion

**Citation Standards**:
- [ ] All citations accessible for verification
- [ ] Source nature labeled
- [ ] Complete URLs provided

### 5.3 Garbage Information Removal

**Cleanup Actions**:
- Delete all low-quality source citations
- Replace data in analysis articles with primary sources
- Information without primary sources clearly label uncertainty

---

## Phase 6: Answer Generation

### 6.1 Structure Planning

**Standard Structure**:
```markdown
## [Direct Answer]
Concise and clear core answer

## [Detailed Analysis]
### 1. [Sub-topic 1]
(Detailed explanation based on primary sources)

### 2. [Sub-topic 2]
(Detailed explanation based on primary sources)

### 3. [Comparison/Analysis] (if applicable)
| Dimension | A | B |
|-----------|---|---|

## [Conclusion]
Summarize key findings

---
**Sources**:
[1] [Source name]: [Full URL] - [Primary/Secondary]
```

### 6.2 Citation Standards

**In-text citation format**:
```markdown
According to [Official Source] disclosure[1], [key information]...

Additionally, [Another Source] shows[2]...
```

**Source list format**:
```markdown
**Sources**:
[1] [Source name]: [Full URL] - [Primary/Secondary]
[2] [Source name]: [Full URL] - [Primary/Secondary]
```

### 6.3 Transparency Labeling

**Must label situations**:
- Secondary information: Indicate "According to media reports..."
- Cannot verify: "Currently no exact data found in public information..."
- Controversial: "On this issue, different sources have different opinions..."
- Information timeliness: "This data as of X year X month..."

---

## Checklist Summary

### Phase 0 Checklist
- [ ] Decomposed user question's information needs
- [ ] Predicted likely primary source locations
- [ ] Planned at least two rounds of search
- [ ] Explicitly identified garbage sources to avoid

### Phase 1 Checklist
- [ ] Executed multiple keyword searches
- [ ] Excluded content farm sources
- [ ] Recorded candidate source list

### Phase 2 Checklist
- [ ] Rated candidate sources for credibility
- [ ] Identified information gaps
- [ ] Planned Round 2 targeted search strategies

### Phase 3 Checklist
- [ ] Used site: syntax to locate official sources
- [ ] Extracted key data from official documents
- [ ] Traced secondary sources to original sources

### Phase 4 Checklist
- [ ] Key data has primary sources
- [ ] Important information cross-validated
- [ ] Source contradictions handled

### Phase 5 Checklist
- [ ] All aspects of user question covered
- [ ] Every conclusion has source support
- [ ] All garbage sources cleared

### Phase 6 Checklist
- [ ] Citation format standardized
- [ ] Information nature labeled
- [ ] Uncertainties explained

---

## Usage Instructions

This document provides a **reusable methodology framework**. Actual application requires:

1. **Adjust according to specific scenarios**: Different fields have different primary sources
2. **Flexibly master strictness**: Emergency situations may appropriately lower verification requirements (but must explain)
3. **Continuously accumulate experience**: Record effective primary sources, form domain knowledge

---

*Follow this workflow to ensure AI search quality and credibility.*
