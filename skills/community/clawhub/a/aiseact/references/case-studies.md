# AISEACT Reference Cases

> **Important Note**: Cases in this document are for **demonstrating AISEACT methodology application only**, not fixed templates. Each actual task has its uniqueness; apply AISEACT principles flexibly according to specific situations, rather than copying case formats.

---

## How to Use This Document

1. **Learn Methodology**: Understand the thinking process and decision logic in cases
2. **Reference Search Strategies**: Learn the approach to locating primary sources
3. **Avoid Copying**: Specific search keywords and sources need adjustment based on actual tasks
4. **Apply Flexibly**: Apply methods from cases to different scenarios

---

## Case 1: Enterprise Comparative Analysis

### Scenario Description
User wants to understand the comparison between two companies, including why one succeeded and how it differs from another.

### AISEACT Application Process

#### Phase 0: Strategy Planning

**Problem Decomposition**:
- Entity A's core advantages/success factors
- Entity A's basic situation
- Entity B's basic situation
- Comparison dimensions between the two

**Source Prediction**:
- Listed companies → Prospectus, annual reports @ disclosure platforms
- Non-listed companies → Official website, official announcements
- Technology companies → Official website technical documents, GitHub

**Search Round Planning**:
- Round 1: Find announcements, annual reports, official websites
- Round 2: Extract specific data, technical details

#### Phase 1-3: Search Execution

**Round 1 Search**:
- Entity A + prospectus/annual report + site:disclosure_platform
- Entity A + site:official_domain
- Entity B + annual report + site:disclosure_platform
- Entity B + site:official_domain

**Result Filtering**:
- Keep: Prospectus PDF, annual report PDF, official website technical pages
- Exclude: Self-media analysis, 百家号 Baijiahao reprints

**Round 2 Targeted Search**:
- Target information gaps identified in Round 1
- Search for specific technical documents
- Use filetype:pdf to find whitepapers

#### Phase 4-6: Validation and Answer

**Information Validation**:
- Core financial data: Confirmed by annual reports
- Technical parameters: Confirmed by official technical whitepapers
- Market share: Cross-validated 2-3 sources

**Garbage Information Removal**:
- Delete all 百家号 Baijiahao, 搜狐号 Sohu citations
- Replace data in analysis articles with prospectus/annual report data

**Answer Structure**:
```markdown
## Entity A's Core Success Factors
(Based on prospectus, annual report primary sources)

## Comparison with Entity B
| Dimension | Entity A | Entity B | Source |

## Conclusion

---
**Sources**:
[1] Entity A Prospectus - Primary Source
[2] Entity A Annual Report - Primary Source
[3] Entity B Annual Report - Primary Source
```

### Methodology Takeaways

From this case, learn:

1. **Enterprise Research Primary Source Priority**:
   - Listed companies: Prospectus, annual reports @ disclosure platforms
   - Official websites: Products, technology, investor relations pages
   - GitHub (technology companies): Code repositories, technical documents

2. **Search Strategy**:
   - Use `site:` to limit to disclosure platforms
   - Use `filetype:pdf` for official documents
   - Round 1 broad collection, Round 2 targeted supplementation

3. **Comparison Framework Building**:
   - Compare from dimensions like technology, market, finance
   - Every comparison point must have source support

---

## Case 2: Technology Framework Comparison

### Scenario Description
User wants to understand the differences between two technology frameworks and market adoption.

### AISEACT Application Process

#### Source Prediction

**Primary Sources for Technical Questions**:
1. Official documentation (react.dev, vuejs.org, etc.)
2. GitHub repositories (code, README, Releases)
3. Official survey data (Stack Overflow Survey, etc.)
4. Academic papers/standard documents

**Sources to Avoid**:
- CSDN reprint articles
- 简书 Jianshu personal blogs
- Unverified 知乎 Zhihu answers

#### Search Execution

**Round 1**:
```
technology_A official documentation
technology_B official documentation
technology_A site:github.com
technology_B site:github.com
```

**Round 2** (Market data):
```
Stack Overflow Developer Survey technology_A technology_B
State of JS technology_A technology_B
technology_A github stars
```

#### Key Decisions

- **Official documentation** as authoritative source for technical features
- **GitHub data** as reference for community activity
- **Survey data** as reference for market adoption
- Don't cite any self-media analysis articles

### Methodology Takeaways

1. **Technical Question Primary Source Priority**:
   - Official documentation > GitHub > Authoritative surveys > Academic papers

2. **Evaluating Technical Indicators**:
   - Features: Official documentation
   - Community activity: GitHub stars/forks/contributors
   - Market adoption: Authoritative survey data (Stack Overflow, State of JS)

3. **Value of English Search**:
   - Technical field English search results are usually cleaner
   - Official documentation is often in English

---

## Case 3: Policy and Regulation Interpretation

### Scenario Description
User wants to understand the specific content of a policy/regulation and its impact on enterprises.

### AISEACT Application Process

#### Primary Source Location

**Core Sources**:
- Law full text: National People's Congress official website (npc.gov.cn)
- Supporting regulations: Relevant ministry official websites
- Official interpretation: State Council Information Office, authoritative media original reports

**Sources to Avoid**:
- Self-media interpretations
- Analysis articles without legal basis citations

#### Search Execution

```
policy_name site:npc.gov.cn
policy_name full text site:gov.cn filetype:pdf
policy_name supporting measures site:relevant_ministry.gov.cn
```

#### Validation Points

- Is the law the latest version?
- Have supporting implementation rules been released?
- Is official interpretation consistent with the law text?

### Methodology Takeaways

1. **Regulation Information Hierarchy**:
   - Law original text (highest authority)
   - Implementation rules/supporting regulations
   - Official interpretation
   - Authoritative media analysis

2. **Timeliness Check**:
   - Has the law been revised?
   - Retrieve latest version

3. **Applicable Scope Confirmation**:
   - Applicable objects clearly defined in law original text
   - Don't rely on secondary interpretation's "impact analysis"

---

## Case 4: Rumor Verification

### Scenario Description
User asks whether a certain rumor is true.

### AISEACT Process

**Step 1: Find Official Information**
```
company_name announcement site:disclosure_platform
company_name statement site:company_domain
```

**Step 2: Find Authoritative Reports**
- Authoritative media original reports (Caixin, Reuters, etc.)
- Pay attention to report timing

**Step 3: Fact Check**
- Check for official debunking
- Check regulatory agency announcements

**Step 4: Answer**
```markdown
Regarding Company X bankruptcy rumors, verified:

1. **Official Response**: Company X stated on X date that...[Source: Company announcement]
2. **Authoritative Report**: Caixin reported on X date that...[Source: Caixin]
3. **Actual Situation**: According to company's latest financial report...[Source: Annual report]

**Conclusion**: Currently no solid evidence indicates Company X will go bankrupt.

---
**Sources**:
[1] Company X Announcement (X date): ... - Primary Source
[2] Caixin Report: ... - Authoritative Media
[3] Company X Annual Report: ... - Primary Source
```

### Methodology Takeaways

1. **Rumor Verification Source Priority**:
   - Official statement/announcement (highest)
   - Authoritative media original report
   - Regulatory agency announcement
   - All other sources need cautious treatment

2. **Uncertainty Labeling**:
   - If cannot confirm, clearly state "currently no official confirmation"
   - Don't give deterministic judgment

---

## Case 5: Industry Research

### Scenario Description
User wants to understand a certain industry's market size and competitive landscape.

### AISEACT Application Process

#### Primary Source Combination

**Industry Data Multi-Source Validation**:
1. **Government statistics**: Bureau of Statistics yearbooks, industry data
2. **Listed company financial reports**: Industry leaders' annual report data
3. **Industry associations**: Official industry reports
4. **Research institutions**: Gartner, IDC, etc. (need assessment)

#### Search Strategy

```
# Government data
industry_name statistical yearbook site:stats.gov.cn

# Company data
industry_leader annual report site:cninfo.com.cn

# English data
industry_name market size report
industry_name statistics World Bank
```

#### Data Validation

- Are data from different sources consistent?
- Are statistical scopes the same?
- Is publication time recent?

### Methodology Takeaways

1. **Industry Data Characteristics**:
   - Usually no single authoritative source
   - Need multi-source cross-validation
   - Pay attention to statistical scope differences

2. **Listed Company Financial Report Value**:
   - Market share data from industry leaders
   - Comparable company financial indicators
   - Industry trend judgment basis

---

## General Methodology Extracted from Cases

### 1. Primary Source Identification Framework

| Scenario Type | Primary Source Priority | Search Strategy |
|--------------|------------------------|-----------------|
| Company/Organization | Official website, announcements, annual reports | site:official/site:disclosure_platform |
| Technical Questions | Official documentation, GitHub | site:docs_domain/site:github.com |
| Policies/Regulations | Government official websites, legal original text | site:gov.cn/site:relevant_ministry |
| Academic Research | Academic databases, papers | database_name + keywords |
| Industry Data | Bureau of Statistics, company financial reports | site:stats.gov.cn/site:cninfo.com.cn |

### 2. Multi-Round Search Standard Pattern

```
Round 1: Broad search, identify candidate sources and information gaps
Round 2: Targeted search, use site: syntax to locate primary sources
Round 3 (if necessary): Deep verification, cross-validate key information
```

### 3. Universal Quality Assessment Standards

**Immediate Exclusion Red Flags**:
- Content farm domains
- No author attribution, no publication time
- Excessive ads/pop-ups
- Sensational headlines

**Priority Adoption Green Flags**:
- Official domains
- Clear author and organization
- Standardized citations
- Professional layout
- Traceable verification

### 4. Citation Standard Template

**In-text citation**:
```markdown
According to [source_type] disclosure[number], [information_content]...
```

**Source list**:
```markdown
**Sources**:
[number] [source_name]: [full_URL] - [primary/secondary/note]
```

---

## Final Reminder

**Cases are references, not templates.**

Each search task is unique; you should:
1. Understand AISEACT's core methodology
2. Apply flexibly according to specific scenarios
3. Continuously accumulate domain-specific quality sources
4. Maintain strict standards for information quality

---

*Through these cases, you can see how AISEACT elevates AI search from "information搬运" to "authoritative research".*
