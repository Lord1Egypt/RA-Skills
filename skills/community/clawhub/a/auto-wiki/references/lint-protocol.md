# Lint Protocol

> Lint is not just checking problems, it's **governance**—merging, archiving, fixing. Prevents wiki from becoming an information graveyard.

## Flow

```
1. Scan all pages
   ├─ Read meta.yaml for wiki basic info
   ├─ Read index.md for page list
   ├─ Traverse sources/ entities/ concepts/ analyses/ directories
   └─ Compare index vs actual files (find index omissions or extras)

2. Check item by item (7 checks)
   ├─ 2.1 Validation — Page format compliance
   ├─ 2.2 Contradiction — Contradictions between pages
   ├─ 2.3 Duplication — Duplicate pages
   ├─ 2.4 Orphan — Orphaned pages
   ├─ 2.5 Broken Link — Broken links
   ├─ 2.6 Staleness — Outdated content
   └─ 2.7 Coverage — Knowledge coverage gaps

3. Execute fixes (auto + pending confirmation)
   ├─ Auto-fix: index sync, broken link repair, format completion
   └─ Pending confirmation: Merge duplicates, archive outdated, label conflicts

4. Output health report
5. Update meta.yaml statistics
6. Append log.md
```

## Two Levels

Lint has two levels. Structural checks can auto-run full pages; semantic checks require Agent to understand content page by page, cost grows linearly with page count.

| Level | Included Checks | Execution | Cost |
|-------|-----------------|-----------|------|
| **Structural** (must run) | Validation, Orphan, Broken Link, Staleness | Full scan, deterministic output | O(N) file reads |
| **Semantic** (on-demand) | Contradiction, Duplication, Coverage | Agent sampling or user-specified scope | O(N²) semantic comparison |

**Default behavior**: `lint` only runs structural. User says "deep lint" or "check conflicts" to run semantic.

**Semantic scope control**:
- wiki < 50 pages: Full scan
- wiki 50-200 pages: Only pages touched by ingest in last 30 days + their related pages
- wiki > 200 pages: User must specify scope (e.g., "check conflicts under entities/")

---

## 7 Check Details

### 2.1 Validation (Format Validation) — Structural

Check each page per Validation Rules in wiki-format.md:

| Rule | Auto-fix? |
|------|-----------|
| Missing frontmatter field | Yes — Add defaults (type=entity, confidence=medium) |
| Invalid type value | No — Report, wait user confirmation |
| Empty sources (non-source types) | No — Report, suggest association |
| Slug inconsistent with filename | No — Report |
| Date format error | Yes — Attempt auto-correction |

### 2.2 Contradiction (Conflict Detection) — Semantic

Scan entity and concept pages, check:
- Same fact has different values/conclusions in different pages
- Entity page has `contested` label—check if new source can resolve

```
Found conflict:
- alpha-corp.md says AUM 1200 billion (source: 2026-policy-doc)
- industry-overview.md says institution market share implies approx 1000 billion (source: industry-report-2025)
→ Label both pages confidence → contested
```

### 2.3 Duplication (Duplicate Detection) — Semantic

Check if two pages describe same entity/concept:
- Similar filenames (e.g., `alpha-corp.md` and `alpha-annuity.md`)
- Similar titles
- High content overlap

**Action**: Merge into one page, keep more complete version, merge unique info from other. Requires user confirmation.

### 2.4 Orphan (Orphan Detection) — Structural

Page has no incoming links (no other page references it via `[[slug]]`).

**Action**:
1. Check if there should be pages referencing it → Yes → Add wikilink
2. Still no association → Suggest archive or delete

### 2.5 Broken Link (Broken Link Detection) — Structural

Page has `[[slug]]` but corresponding file doesn't exist.

**Action**:
1. If can infer which page it should be (slug spelling close) → Fix wikilink
2. Otherwise → Create stub page (only frontmatter + "TODO"), or remove broken link

### 2.6 Staleness (Outdated Detection) — Structural

| Condition | Determination |
|-----------|---------------|
| Page `updated` > 6 months ago, and confidence ≤ medium | Staleness candidate |
| All page sources > 12 months old | Staleness candidate |
| Page confidence is low and never reinforced by ingest | Staleness candidate |

**Action**: Label "pending verification" or suggest archive. Don't auto-delete.

### 2.7 Coverage (Coverage Assessment) — Semantic

Not finding errors, but finding gaps. Detect across 5 categories:

#### Gap-1: Page Missing

Referenced by other pages via `[[slug]]` but the actual file doesn't exist. Different from Broken Link—Broken Link is a spelling error, Page Missing is knowledge itself that's absent.

- Detection: Traverse all wikilinks, find references to non-existent pages
- Threshold: 3+ pages reference the same non-existent slug → Not a typo, it's a knowledge gap
- Output: `{ gap_type: "page_missing", slug: "xxx", referenced_by: [...] }`

#### Gap-2: Concept Missing

Multiple entity pages repeatedly mention the same term/concept, but there is no independent concept page explaining it.

- Detection: Extract high-frequency terms from entities/ body text, check if concepts/ has corresponding page
- Threshold: A term appears in 3+ different pages but no independent concept page → Gap
- Output: `{ gap_type: "concept_missing", term: "xxx", mentioned_in: [...] }`

#### Gap-3: Data Missing

Entity page mentions a metric but data.db has no corresponding value, or value lacks key dimensions (no period, no source).

- Detection: Scan page body for metric names, cross-check data.db
- Output: `{ gap_type: "data_missing", page: "xxx", field: "xxx" }`

#### Gap-4: Single Source

Page confidence relies on a single source, and that source is not primary/authoritative.

- Detection: sources list length = 1 and source_type is not "primary" or "authoritative-secondary"
- Output: `{ gap_type: "single_source", page: "xxx", current_source: "xxx" }`

#### Gap-5: Outdated

Different from Staleness—Staleness labels stale candidates, Outdated focuses on data that has newer time points available but wiki hasn't kept up.

- Detection: data.db data period > 12 months ago, and the domain typically has annual updates
- Output: `{ gap_type: "outdated", page: "xxx", field: "xxx", last_period: "xxx" }`

#### Gap-6: Validator Gap — only when wiki declares a validator

If meta.yaml declares a `seed` and the corresponding seed file points to a `validator`, Coverage additionally runs validator checks:

- Detection: Call validator (e.g., FIBO SPARQL) to query required relations (`someValuesFrom` constraints) for entity types, compare against relations built in wiki
- Example: FIBO says PensionFund must have a Trustee relation, but the wiki entity page lacks this relation → Gap
- Output: `{ gap_type: "validator_gap", page: "xxx", missing_relation: "hasTrustee", standard: "FIBO" }`
- Degradation: If validator unreachable, silently skip and note in report "External validator unreachable, skipped"

This category detects not "missing information" but "logical incompleteness" — you say this is a PensionFund, but by industry standard definition, it needs at least a management company, custodian, and supervisory authority.

#### Coverage Heuristics (supplementary)

Beyond the 6 categories above, retain original heuristic checks:
- Entity referenced by 5 other pages but content is thin (< 100 words) → Suggest deepening
- Few pages of certain type (e.g., concepts/) but many entities/ → Suggest extracting concepts
- Many source pages but few analysis pages → Suggest comprehensive analysis

## Health Report Format

```
## Wiki Health Report: {topic name}
Generated: {date}

### Overview
- Total pages: 42 (sources: 12, entities: 15, concepts: 10, analyses: 5)
- Health: Good / Needs Attention / Needs Intervention
- confidence distribution: high 30 / medium 8 / low 2 / contested 2

### This Run Fixes
- [Auto] index.md sync (added 2 missing entries)
- [Auto] Fixed 1 broken link (portable-annuity → portable-annuity-scheme)
- [Pending] Merge alpha-corp.md and alpha-annuity.md (suspected duplicate)

### Pending Issues
- Conflicts: 2 (list specific pages and conflict points)
- Outdated: 1 page suggested for archive (portfolio-category, 6 months no update)

### Coverage Suggestions
- entities/beta-corp.md content thin (only 50 words), referenced by 4 pages, suggest ingest more materials
- concepts/ only 10 pages while entities/ has 15 pages, suggest extract more concept pages

### Statistics
- Most active source: 2026-policy-doc (referenced by 8 pages)
- Most isolated entity: portfolio-category (0 incoming links)
- Recent ingest: 2026-04-06 (3 days ago)
```

## Gap Report Format (for deep-dive)

When Coverage check is triggered by deep-dive, output a structured Gap Report in addition to the health report:

```
## Gap Report: {topic}
Generated: {date}
Scope: {full | specified range}

### Gaps Found: {N}

| # | Category | Target | Detail | Priority | Search Direction |
|---|----------|--------|--------|----------|------------------|
| 1 | page_missing | portable-annuity | Referenced by 4 pages | high | Search "portable enterprise annuity policy" |
| 2 | concept_missing | trustee qualification | Mentioned in 5 entity pages | high | Search "enterprise annuity trustee requirements" |
| 3 | single_source | alpha-corp | Only source: industry-report-2025 | medium | Search "Alpha Corp pension annual report" |

### Priority Rules
- high: page_missing (3+ references), concept_missing (5+ mentions)
- medium: single_source, data_missing
- low: outdated (data age 12-24 months)
```

### Scope Control (deep-dive scenario)

When triggered by deep-dive, Coverage accepts optional scope parameters:
- `deep-dive {topic}` → Limit to specified wiki
- `deep-dive {topic} entities/` → Limit to subdirectory
- `deep-dive {topic} --max-gaps N` → Limit max gaps (default 10)
- No scope specified → Follow semantic level scope rules (<50 pages full scan, 50-200 pages last 30 days, >200 pages require specification)
