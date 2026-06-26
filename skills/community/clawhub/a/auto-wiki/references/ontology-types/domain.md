# Domain/Industry Research Collection Strategy

> Applicable for researching an industry or vertical domain. Typical output: entity pages, concept pages, relationship network.
> This document only covers **wiki accumulation phase**, not ontology crystallization.

## Collection Dimensions

### 1. Policy and Regulatory Documents
- **Find**: Ministry regulations, industry standards, regulatory notices, administrative penalty cases
- **Extract**: Effective date, issuing authority, core rules, scope of impact, repeal/replacement relationships
- **Output**: Source page + concept page (system/rules) + entity page (regulatory agencies)

### 2. Industry Data and Statistics
- **Find**: Official statistical bulletins, industry association annual reports, regulatory disclosure data
- **Extract**: Key metrics and scope, time series, YoY changes, statistical scope description
- **Output**: Source page + concept page (metric definitions) + entity page (statistical subjects)

### 3. Research Reports and Analysis
- **Find**: Broker research reports, think tank reports, academic papers, industry white papers
- **Extract**: Core conclusions, evidence and data sources, market forecasts, consistencies/contradictions with other sources
- **Output**: Source page + updates to existing entity/concept pages

### 4. Cases and Examples
- **Find**: Typical enterprise cases, product solutions, event post-mortems, judicial precedents
- **Extract**: Participants, timeline, key decisions and outcomes, generalizable patterns
- **Output**: Source page + entity pages (involved institutions/products)

### 5. Market Participant Profiles
- **Find**: Institution official websites, annual reports, business qualifications, market share, organizational structure
- **Extract**: Institution name/type/role, business scope, AUM, licensed qualifications, key personnel
- **Output**: Entity pages (institutions) + if need to distinguish institution from its roles, create separate pages

### 6. Historical Evolution and Timeline
- **Find**: System evolution history, industry chronicles, policy iteration context
- **Extract**: Key nodes (with dates), system phases, change drivers
- **Output**: Concept pages (system/phase) + update entity page "History" sections

## Entity Identification Rules

**Entity**: Objectively identifiable unique existence (institution, product, fund, plan, natural person). Criteria: has proper name, appears repeatedly in multiple sources, can be "looked up".

**Concept**: System, method, metric, classification that cannot be uniquely instantiated. Criteria: needs definition to understand, easily confused with similar concepts.

### Non-mixing Rules (Anti-patterns)

Using enterprise annuity as example, similar variants exist in any industry:

| Easy to Confuse | Correct Approach | Determination Basis |
|-----------------|------------------|---------------------|
| Institution vs Institution Role | Create separate pages | Same institution can hold multiple roles (same bank is both custodian and account manager) |
| Plan vs Product | Create separate pages | One plan can choose multiple products |
| Metric vs Observation | Create separate pages | "Investment return rate" is metric, "2025 return 5.2%" is observation |
| Classification system vs Instance | Create separate pages | "DB/DC type" is classification, "XX company annuity plan" is instance |

**Create new vs Update**: First search index.md, update if page exists, don't create synonymous page.

## Relationship Labeling

Express relationships in body with natural language + wikilink, no dedicated relationship table needed:

```markdown
[[Some Bank]] serves as trustee managing [[XX Enterprise Annuity Plan]], which invests in [[Some Pension Product-Conservative]].
```

Common verb phrases: `trustee manages`, `regulates`, `subordinate to`, `invests in`, `evolved from...`.

**Relationship dual-write**: frontmatter `relations` field (Obsidian visible) + data.db `relations` table (queryable). Use `[[wikilink]]` naturally in body. Keep all three consistent.

## Page Structure Templates

### Entity Page

Sections: **Overview** (one-sentence positioning) → **Key Data** (scale/share/qualifications, label scope and timepoint) → **Relationships** (wikilink to related entities/concepts) → **History** (timeline, outdated data moves here)

### Concept Page

Sections: **Definition** (one paragraph, label source) → **Applicable Scope** (which subjects/scenarios) → **Common Confusions** (distinction from [[similar concept]])

### Source Page

Sections: **Basic Info** (issuing authority/date/document number) → **Core Content** (3-5 key points) → **Involved Entities and Concepts** (wikilink list, helps ingest locate update targets)

All page frontmatter formats follow wiki-format.md (title / type / created / updated / sources / confidence).
