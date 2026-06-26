# Storage Specification

## Wiki Root Directory

All wikis are stored in `.wiki/` directory under working directory:

```
{project_root}/
└── .wiki/
    ├── enterprise-annuity/      # One directory per research topic
    ├── charlie-munger/
    └── public-fund/
```

**Location Selection Logic** (by priority):
1. If current directory has `.wiki/` → Use it
2. If current directory has `.claude/` → Create `.wiki/` at same level
3. If current directory is git repo root → Create `.wiki/` at root
4. Otherwise → Create `.wiki/` in current directory

**Relationship with .gitignore**: Recommend adding `.wiki/` to `.gitignore` (wiki is personal knowledge base, shouldn't be committed with project code). If user wants version control, can `git init` separately inside `.wiki/`.

### Obsidian Compatibility

`.wiki/` directory can be directly opened as Obsidian vault (`Open folder as vault`):

- `[[slug]]` / `[[slug|display]]` → Obsidian Graph View auto-renders topology
- YAML frontmatter → Obsidian Properties panel, can filter by confidence, type, etc.
- `sources/`, `entities/`, `concepts/` directories → Obsidian folder view

**On first `.wiki/` creation**, Agent should initialize `.obsidian/` config directory with graph coloring enabled:

```
.wiki/.obsidian/
├── graph.json       # Graph color scheme (grouped by path and tag)
├── app.json         # {}
├── appearance.json  # {}
└── core-plugins.json # Enable graph, backlink, properties, tag-pane
```

`graph.json` presets 5 color groups:

| Group Rule | Color | Description |
|-----------|-------|-------------|
| `path:sources/` | Blue-gray | Source files |
| `path:entities/` | Cyan-green | Entities |
| `path:concepts/` | Emerald | Concepts |
| `path:analyses/` | Purple | Analyses |
| `[confidence:contested]` | Red | Contested nodes (Obsidian Properties syntax matching frontmatter) |

Also sets:
- `showTags: false` (hide tag nodes from graph — coloring uses `path:` and Properties queries; tags are for search/filter only)
- `showArrow: true` (show relationship direction)
- `textFadeMultiplier: -1.5` (show node labels by default)
- `search: "-path:index -path:log"` (exclude index and log meta files)

If need to exclude `_report.html` and other generated files, add `_*` to Obsidian Settings → Files & Links → Excluded files.

### Visualization Reports

Run `python schema.py --report .wiki/{topic}/` to generate `_report.html`, open in browser to view:

- Statistics panel: page count, type distribution, contested count
- Interactive relationship graph: vis-network.js rendering, draggable, zoomable
- Data table: All structured data points (value + unit + period + confidence)
- Freshness: Sorted by update date
- Coverage Gaps: Orphan pages, missing pages

## Single Wiki Directory Structure

```
.wiki/{topic_name}/
├── data.db                  # Structured data (SQLite, managed by store.py)
├── meta.yaml                # Wiki metadata (ontology type, creation time, description)
├── index.md                 # Page index (Agent auto-maintained)
├── log.md                   # Operation log (append-only)
├── _report.html             # Visualization report (schema.py --report generates)
├── sources/                 # Source file summary pages (immutable)
│   ├── 2026-04-06-policy-doc.md
│   └── 2026-04-03-annual-report.md
├── entities/                # Entity pages (narrative analysis)
│   ├── alpha-corp.md
│   └── regulatory-agency.md
├── concepts/                # Concept pages
│   ├── fiduciary-responsibility.md
│   └── portable-annuity.md
└── analyses/                # Analysis archive pages (query outputs)
    └── market-comparison.md
```

### Data Layering Principle

| Layer | Carrier | Stores What | Why |
|-------|---------|-------------|-----|
| **Narrative** | Markdown pages | Analysis, context, wikilink | Human reading, Obsidian browsing |
| **Data** | data.db (SQLite) | Values, time series, relations, history | Aggregate queries, cross-page comparison, timeline |
| **Metadata** | YAML frontmatter | title, type, created, updated, sources, confidence | Page identity |

**Frontmatter no longer stores `data` and `history` fields.** All structured data written to `data.db`.
Frontmatter only keeps: `title`, `type`, `created`, `updated`, `sources`, `confidence`.
`relations` kept in frontmatter (Obsidian wikilink rendering needs it), also written to `data.db` (query needs it).

### data.db Initialization

When wiki is created, Agent runs `python store.py init .wiki/{topic}/` to initialize database.
Table structure see `store.py`, includes: `pages`, `data_points`, `history`, `relations`.

## meta.yaml

Each wiki's metadata, written at creation, updated during lint:

```yaml
name: my-research-topic
ontology_type: domain           # domain | cognitive | general
description: Research topic description
seed: fibo-pensions             # Optional, references seed filename under seeds/
created: 2026-04-06
last_ingest: 2026-04-06
stats:
  sources: 3
  entities: 8
  concepts: 5
  analyses: 1
  total_pages: 17
  contested_count: 1
```

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Wiki directory name |
| ontology_type | Yes | domain / cognitive / general |
| description | Yes | One-sentence description of research topic |
| seed | No | Seed configuration name, corresponds to `seeds/{name}.md`. Omit for no seed, wiki grows freely |
| created | Yes | Creation date |
| last_ingest | Yes | Last ingest date (Agent updates) |
| stats | Yes | Page statistics (Agent / lint updates) |

## Initialization Templates

### index.md Created for New Wiki

```markdown
# {topic_name} Wiki Index

> 0 pages | Created: {date} | Type: {ontology_type}

## Sources (0)

## Entities (0)

## Concepts (0)

## Analyses (0)
```

### log.md Created for New Wiki

```markdown
# {topic_name} Wiki Log

## {date} — init
- Created wiki: {topic_name}
- Ontology type: {ontology_type}
- Description: {description}
```

## File Size Expectations

| Wiki Scale | Source Files | Total Pages | Disk Usage | Suitable Retrieval |
|------------|--------------|-------------|------------|-------------------|
| Small | 1-10 | 5-30 | < 1 MB | grep + read index |
| Medium | 10-50 | 30-150 | 1-10 MB | grep + read index |
| Large | 50-200 | 150-500 | 10-50 MB | Needs index upgrade (beyond Skill scope) |

**Default mode limit: ~500 pages.** Beyond that, enable SQLite FTS5 index (zero dependencies, Python built-in), supporting BM25 ranking and backlink queries. See `scaling.md` for details.

> Beyond that (need vector retrieval / multi-user collaboration), migrate to external platform.

## Cross-Wiki Operations

`query` defaults to search within single wiki. If user question spans multiple wikis:

```
User: What intersections exist between Munger's investment framework and enterprise annuity domain?

Agent:
1. Read directory list under .wiki/, identify relevant wikis
2. Read charlie-munger/index.md and enterprise-annuity/index.md separately
3. Search relevant pages in both wikis
4. Synthesize answer, label source by wiki
```

## Source File Processing

Different format source files, processing during ingest:

| Format | Processing | Notes |
|--------|-----------|-------|
| Text / Markdown | Read directly | Ideal input format |
| PDF | Read text content (within Agent capability) | Complex layouts may lose structure |
| Excel / CSV | Read data, extract key metrics | Numeric data written to entity page "Key Data" section |
| User oral / conversation text | Ingest as text | Label source as "oral", confidence default medium |
| URL / Webpage | Fetch content with WebFetch, then ingest | Label source URL |

**Agent doesn't store source file originals**—only stores source summary pages. Originals managed by user.
