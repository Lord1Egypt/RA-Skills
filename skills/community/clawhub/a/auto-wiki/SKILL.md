---
name: knowledge-compiler
version: 0.2.0
description: |
  Knowledge compiler: teaches agents to incrementally compile source files into persistent wikis for cross-session knowledge accumulation.
  Runtime dependencies: Python 3.8+ (stdlib + pydantic). Optional enhancements: WebSearch (active search), external MCP validator (logic validation).

  Five modes, automatically routed based on user intent:
  
  recall → User wants to answer questions based on existing knowledge.
  Trigger words: recall, knowledge mode, open wiki, answer with knowledge, according to wiki,
  based on accumulation, check wiki, does wiki have, researched before, previously organized.
  
  ingest → User provided new material, wants to compile into wiki.
  Trigger words: ingest, compile, organize this, digest this, study this, archive,
  add this in, accumulate, research this, help me organize, add to knowledge base.
  
  query → User asked a specific question, wants to find answer from wiki (one-time).
  Trigger words: query, answer according to wiki, what does wiki say, check it.
  
  lint → User wants to check wiki health.
  Trigger words: lint, check wiki, wiki health, clean up, any conflicts.

  deep-dive → User wants Agent to automatically find knowledge gaps and fill them.
  Trigger words: deep-dive, deep dive, fill gaps, research gaps, level up,
  auto-complete wiki, knowledge completion, comprehensive fill.
  Note: deep-dive is not an independent mode, it's a combined pipeline of lint(Coverage) + ingest(search-fill).
---

# Knowledge Compiler

> Agents do research, pull data, write reports—the wiki connects these outputs. The more you use the agent, the more it understands your domain.

## Runtime Dependencies & Permissions

| Dependency | Required? | Description |
|------------|-----------|-------------|
| **Python 3.8+** | ✅ Required | `schema.py` (frontmatter validation), `store.py` (SQLite data management), `build_index.py` (FTS5 indexing) are Python scripts. Uses only stdlib (`sqlite3`, `json`, `pathlib`) + `pydantic` |
| **pydantic** | ✅ Required | Frontmatter validation in `schema.py`. `pip install pydantic` |
| **Filesystem write** | ✅ Required | Creates and edits Markdown, SQLite, `.obsidian/` config under `.wiki/{topic}/`. **Will confirm location with user before first `.wiki/` creation** |
| **WebSearch / WebFetch** | ❌ Optional | Needed for active mode (agent searches for materials autonomously). Not needed for passive mode (user provides files) |
| **External validator (MCP)** | ❌ Optional | Only called during lint when wiki declares a validator. Silently skipped when unreachable, zero impact. **No user credentials needed** — `Mcp-Session-Id` is standard MCP protocol session handshake, handled automatically by the agent |
| **Domain data MCP** | ❌ Optional | deep-dive and active ingest can use domain data MCP for enhanced search quality. Falls back to WebSearch when absent |

> **Core promise**: Passive mode (user provides files → agent compiles) only requires Python 3 + filesystem access, zero network dependencies. All network calls are optional enhancements, and the environment check on first use will inform the user of available capabilities.

## Quick Start

```
User: /auto-wiki recall personal-pension
Agent: [Scan .wiki/personal-pension/ → Read index.md → Load data.db summary]
Agent: Entered recall mode. Current wiki: 22 pages / 8 data points / 2 contested.
       Subsequent questions will be answered by checking wiki first.

User: What are the reasons for low participation rates?
Agent: [Read wiki pages enrollment-friction, tax-incentive-effect, etc.]
Agent: According to 6 sources accumulated in wiki... (cite specific pages and data)
       ⚠️ Note: Tax incentive effects are contested (77.8% vs 25%), see [[participation-willingness]]
```

```
User: ingest this industry report into XX wiki
Agent: [Read report → Search existing wiki → Compare old vs new → Update 3 pages, create 1 page]
Agent: Ingested into XX wiki: updated 3 pages (list), created 1 page (list)
```

## Core Philosophy

Agents help you research, write reports, and pull data every day—but then forget everything. The next time you ask about the same domain, it starts from scratch.

This skill solves one thing: **giving agents a knowledge base that accumulates over time.**

It's not RAG (retrieving from documents on each query), but compilation—after reading source files, the agent writes key information into **existing wiki pages**, comparing with old knowledge, merging, and flagging conflicts. Before executing any task next time, it reads the wiki and works from the accumulated foundation.

## Four Modes

| Mode | Trigger | What Agent Does |
|------|---------|-----------------|
| **recall** | `recall` / `recall {topic}` | Load wiki context, answer all subsequent questions by checking wiki first |
| **ingest** | User provides source file or text | Read source → Search wiki → Compare old vs new → Update/create pages → Update index |
| **query** | User asks a question (one-time) | Read index → Find relevant pages → Synthesize answer → Archive valuable analysis |
| **lint** | User says "check wiki" | Scan all pages → Merge duplicates → Archive outdated → Report conflicts and health |
| **deep-dive** | `deep-dive` / "level up" | Run Coverage lint → Present gap report → User confirms → Search + ingest to fill gaps |

> deep-dive is not a 5th independent mode—it's a combined pipeline of lint (Coverage) and ingest (with search tools). Requires search tools (active mode).

Recall mode vs query difference: query is one-time operation (ask one question, check wiki once). Recall mode is continuous state—after entering, every question in this conversation goes through wiki first.

---

## Recall Mode

### Entering

Triggered when user says `/auto-wiki recall` or `/auto-wiki recall {topic}`.

Agent executes:

1. **Scan `.wiki/` directory**, list available wiki topics
2. If user specified topic → Load that wiki; If not specified → List optional topics for user to choose
3. **Read index.md** → Get all page list and structure
4. **Read data.db summary** → `python references/store.py dump .wiki/{topic}/`, get data point count, relation count, contested count
5. **Report to user**:
   ```
   Entered recall mode: {topic}
   - Pages: {N} (sources: X, entities: Y, concepts: Z)
   - Data points: {N} | Relations: {N} | Contested: {N}
   Subsequent questions will be answered by checking wiki first. Say "exit recall mode" to return to normal.
   ```

### Response Flow

After entering recall mode, upon receiving each user question:

1. **Extract keywords from question** (entity names, concept names, metric names)
2. **Match in index.md** for relevant pages (title + description)
3. **Query data.db for relevant data points**:
   ```sql
   SELECT * FROM data_points WHERE field LIKE '%keyword%' OR page_slug LIKE '%keyword%'
   ```
4. **Read matched wiki pages** (usually 2-5), expand one level along wikilinks
5. **Synthesize answer**, must:
   - Cite specific pages: `[[slug]]`
   - Cite specific data: value + unit + period + source
   - If involving contested info, proactively label
   - If wiki info insufficient, clearly state "no accumulation in this aspect in wiki, suggest ingesting XX"
6. **Do not fabricate information not in wiki**. Better to say "don't know" than pretend wiki has it

### Exit

Exit when user says `exit recall`, switches to other operations (ingest/lint), or starts a new topic.

---

## Execution Flow

### Phase 0: Identify Research Topic and Ontology Type

After receiving user input, determine three things: **operation type**, **target wiki**, **ontology type**.

| User Input | Operation | Target Wiki | Ontology Type |
|-----------|-----------|-------------|---------------|
| "Help me organize this report" + file | ingest | Inferred from content, or ask user | domain |
| "ingest into personal pension" + file | ingest | personal-pension | domain |
| "Research Charlie Munger" + materials | ingest | charlie-munger | cognitive |
| "What is personal pension participation rate?" | query | Inferred from question, or ask user | — |
| "Check the pension wiki" | lint | personal-pension | — |

**Ontology type** determines wiki page structure and collection strategy:

| Ontology Type | Research Target | Page Focus | Reference |
|--------------|-----------------|------------|-----------|
| **cognitive** | Person (mental models, decision patterns) | MentalModel, Heuristic, Value, StylePattern | `references/ontology-types/cognitive.md` |
| **domain** | Domain (institutions, systems, metrics) | Entity, Concept, Metric | `references/ontology-types/domain.md` |
| **general** | Neither of the above | Default entity/concept structure | — |

**A wiki has only one type.** If research spans both person and domain (e.g., "Munger's investment framework applied to enterprise annuity"), it belongs to two wikis, with cross-wiki query for synthesis. Don't mix cognitive and domain page structures in one wiki.

**If wiki directory doesn't exist**, first confirm creation location with user (default `.wiki/{topic}/` under current repository root), then create initial structure per `references/storage-spec.md` (including meta.yaml, index.md template, log.md template). Suggest user add `.wiki/` to `.gitignore` if not already present.

**Domain seed**: If the target domain has a corresponding seed file (`seeds/{name}.md`), declare `seed: {name}` in meta.yaml. Seeds provide standard terminology, relationship templates, and anti-confusion rules, letting wikis start from a normalized foundation. Domains without seeds grow freely — both paths work. Seeds are community-contributable plugins — anyone can write a markdown file for their vertical domain. See `references/seed-ontologies.md`.

**On first use**, perform environment check (see `references/source-validation.md`), informing user of available capabilities (passive mode vs active mode).

### Reference Loading Strategy

Don't read all references at once. Load on-demand by operation type:

| Operation | Required | Read on First Use | Read When Tools Available |
|-----------|----------|-------------------|---------------------------|
| **ingest** | `ingest-protocol.md`, `wiki-format.md`, `schema.py` | `storage-spec.md` (if wiki doesn't exist), `seed-ontologies.md` + `seeds/{name}.md` (if seed declared in meta.yaml) | `fact-check.md`, `source-validation.md` |
| **query** | `query-protocol.md` | — | — |
| **lint** | `lint-protocol.md`, `schema.py` | — | `validators/{name}.md` (if seed declared validator) |
| **deep-dive** | `lint-protocol.md`, `ingest-protocol.md`, `source-validation.md`, `wiki-format.md`, `schema.py` | `storage-spec.md` (if wiki doesn't exist) | `fact-check.md` |

**Not needed**: `scaling.md` only relevant when page count > 500; `ontology-types/` only when creating new wiki and need to determine type.

### Phase 1: Ingest (Knowledge Compilation)

**This is the core operation.** Detailed protocol in `references/ingest-protocol.md`.

Brief flow:

1. **Read source file**, extract key information
2. **Validate key data** (if tools available)—see `references/fact-check.md`
3. **Write source summary page** (`sources/{date}-{slug}.md`)
4. **Search wiki for existing related pages** (read index.md, grep key entity names)
5. **Compare old vs new page by page**:
   - New info **supports** existing conclusion → add citation, boost confidence
   - New info **overturns** existing conclusion → write value to data.db (old value auto-enters history table), rewrite body analysis
   - New info **conflicts** and can't determine → present both views, confidence → `contested`
6. **Create new pages** (only for entities/concepts not yet in wiki)
7. **Update index.md + append log.md**
8. **Schema validation**—run `python references/schema.py {page.md}` on all created/modified pages to ensure frontmatter compliance. Fix immediately if failed

After ingest, report to user:
```
Ingested into {topic} wiki:
- Created: {N} pages (list)
- Updated: {N} pages (list + brief reason)
- Conflicts: {N} (list conflict points)
- Validation: {N} pages all passed / {M} pages have issues (list)
```

### Phase 2: Query (Knowledge Retrieval)

**Detailed protocol in `references/query-protocol.md`.**

1. Read index.md, identify pages relevant to question
2. Read matched pages + follow wikilinks to related pages (one level)
3. Synthesize answer based on page content, **cite source pages**:
   ```
   Based on {N} source files accumulated in wiki:
   ... analysis content ...
   Sources: [[alpha-corp]], [[2026-policy-doc]]
   ```
4. If involving contested info, clearly label the conflict
5. If answer contains valuable new analysis, prompt user to archive

**If wiki info insufficient**, clearly state the gap:
```
Wiki information on XX is insufficient. Currently only 2 relevant source files.
Suggest ingesting more materials about XX.
```

### Phase 3: Lint (Knowledge Governance)

**Detailed protocol in `references/lint-protocol.md` (7 checks + health report format).**

Lint has two levels:

| Level | Trigger | Check Items | Cost |
|-------|---------|-------------|------|
| **Structural** (default) | `lint` / `check wiki` | Validation, Orphan, Broken Link, Staleness | Full scan, deterministic |
| **Semantic** (on-demand) | `deep lint` / `check conflicts` | Contradiction, Duplication, Coverage | Agent semantic understanding, scope-controlled |

1. **Structural**: Auto-scan all pages, fix format, broken links, orphans, staleness
2. **Semantic** (user triggered): Detect conflicts, duplicates, coverage gaps. Wiki < 50 pages = full scan, 50-200 pages = only last 30 days' ingest-touched pages, > 200 pages = user must specify scope
3. **Report health**:
```
Wiki Health Report: {topic}
- Total pages: 42 (sources: 12, entities: 15, concepts: 10, analyses: 5)
- Health: Good
- Structural fixes: Fixed 1 broken link, archived 1 stale page
- [Semantic] Pending human review: 2 conflicts (list)
- Suggestion: Few source files in XX domain (only 1), recommend supplement
```

### Phase 4: Deep-Dive (Knowledge Completion Pipeline)

**deep-dive = lint(Coverage) + ingest(search-fill)**. Not an independent mode, but a combined pipeline.

**Prerequisite**: Requires search tools (active mode). Without search tools, only outputs gap report without auto-filling. Prompts user to manually ingest.

**Flow**:

```
1. Run lint Coverage check (5-category gap detection)
   → Output structured Gap Report (see lint-protocol.md)

2. Present Gap Report, request user confirmation
   → User can: accept all / select subset / limit scope / cancel
   → This step cannot be skipped — prevents unsupervised batch writes

3. For each confirmed gap, execute from-lint ingest flow
   → Search → User confirms source → Standard ingest
   → See From-Lint section in ingest-protocol.md

4. Output completion report: filled / unable to fill / recommendations
```

**Trigger words**: `deep-dive`, `deep dive`, `fill gaps`, `research gaps`, `level up`

**Example**:
```
User: deep-dive treasury-futures
Agent: [Running Coverage lint...]
Agent: Found 6 knowledge gaps:
       1. [high] page_missing: stock-bond-correlation (referenced by 4 pages)
       2. [high] concept_missing: basis (mentioned in 5 entity pages)
       3. [medium] single_source: treasury-futures-basics (only 1 source)
       ...
       Which to fill? (all / select numbers / cancel)

User: 1, 2

Agent: [Searching "stock bond correlation treasury futures"...]
Agent: Found 2 candidate sources:
       - [authoritative-secondary] CICC Fixed Income "Stock-Bond Correlation Analysis" ← Recommended
       - [secondary] Blog post ← Skip (blacklisted channel)
       Confirm using CICC report?

User: confirm

Agent: [Execute standard ingest → Create concepts/stock-bond-correlation.md]
Agent: Completion done. Created 2 pages, updated 0 pages, 1 gap unable to fill (suggest providing materials manually).
```

---

## Wiki Page Format

See `references/wiki-format.md` for details. Brief summary:

- Each page is markdown with frontmatter (title, type, created, updated, sources, confidence)
- 5 page types: source / entity / concept / analysis / mental-model
- Use `[[slug]]` for inter-page links
- index.md is the directory, log.md is the operation log

## Ontology Type Reference

When research target is a **person**, see `references/ontology-types/cognitive.md` for collection strategy—page types focus on mental models, heuristics, value systems, expression styles.

When research target is a **domain**, see `references/ontology-types/domain.md` for collection strategy—page types focus on institutional entities, system concepts, quantitative metrics.

Both share the same wiki infrastructure (ingest/query/lint), differing only in page classification and collection emphasis.

## Vertical Domain Adaptation

The skill core is a domain-agnostic compilation engine. Vertical domain expertise is injected through two plugin layers:

| Layer | Carrier | Purpose | Required? |
|-------|---------|---------|-----------|
| **Seed** | `seeds/{name}.md` | Cold-start vocabulary: standard terms, relationship templates, anti-confusion rules | Optional |
| **Validator** | `validators/{name}.md` | Runtime logical validation: relationship legality, required relation completeness | Optional |

Without plugins, wikis grow freely — suitable for exploratory research. With plugins, wikis start from industry standards with normalized naming, clear relationship structures, and detectable logic gaps.

**Community-contributable**: Write a seed file (markdown) for your vertical domain — declare 20-50 core terms and anti-confusion rules, and wikis in that domain start from a normalized foundation.

Currently available:
- `seeds/fibo-pensions.md` — Enterprise annuity / pensions (based on FIBO standard)
- `validators/fibo-mcp.md` — FIBO SPARQL logical validation (627K inferred triples)

## What This Skill Doesn't Do

- **No vector retrieval**. Small scale uses index + grep, large scale uses SQLite FTS5 + BM25 (see `references/scaling.md`). Vector retrieval is left to platform-level tools.
- **No multi-user collaboration**. Wiki directory is local files, one wiki per user.
- **No replacement for professional data tools**. Domain data acquisition uses corresponding MCP/tools; this skill only receives their outputs and compiles into wiki.

## Relationship with Other Tools

This skill doesn't replace any professional tool, it **connects** them:

```
Any research tool produces analysis → ingest into corresponding wiki
Any data tool pulls data           → ingest into corresponding wiki
Domain seeds provide starting line  → standard terms + anti-confusion rules
External validators check logic     → lint checks knowledge structure completeness

Next time executing tasks, agent reads relevant wiki → works with accumulated knowledge
```
