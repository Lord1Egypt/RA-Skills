# ExpertPack Schemas Reference

Condensed from the full schemas in the ExpertPack repo. Use this when creating or validating packs.

## Pack Types

**person** - Human knowledge (stories, mind, relationships)
**person:agent** - AI agent operational identity, prescriptive mind, tools
**product** - Product concepts, workflows, troubleshooting
**process** - Sequential phases, decisions, checklists
**composite** - Orchestrates multiple packs with roles and conflict rules

## Core Files (all packs)
- `manifest.yaml` - Required. Declares type, version, tiers, EK ratio.
- `overview.md` - Required. Entry point with lead summary.

## Context Tier System
Declared in manifest.yaml:
- **Tier 1 (always)**: Loaded in every session (manifest, overview, glossary). Keep total <5KB.
- **Tier 2 (searchable)**: Indexed for RAG retrieval.
- **Tier 3 (on-demand)**: Loaded only on explicit request (verbatim, raw data).

## EK Ratio in Manifest
```yaml
ek_ratio:
  value: 0.78
  measured_at: "2026-03-01"
  sample_size: 240
  models: ["gpt-4.1", "claude-3.7"]
```

## File Size & Naming Rules
- 1-3KB preferred per content file
- kebab-case for filenames and slugs
- Markdown canonical: all knowledge in .md
- One topic per file
- ## headers for chunk boundaries

## Product Pack Structure
```
manifest.yaml
overview.md
concepts/
workflows/
interfaces/
troubleshooting/
faq/
glossary.md
```

## Process Pack Structure
```
manifest.yaml
overview.md
phases/
decisions/
checklists/
gotchas/
```

## Person Pack Structure
```
manifest.yaml
overview.md
facts/
mind/
relationships/
presentation/
summaries/
meta/privacy.md
```

## Agent Pack (person:agent)
Adds operational/, mind/ with values, skills, tensions, etc.

## Composite Manifest
```yaml
type: composite
packs:
  - path: "../packs/some-pack"
    role: knowledge
conflicts:
  priority: [...]
```

## Entity Relation Graph (optional)
`relations.yaml` at pack root — typed, directional relationships between entities.
Use for packs with 20+ cross-referencing entities, especially product packs and composites.

```yaml
entities:
  - id: territory
    type: concept
    label: "Territory"
    file: concepts/territories.md
relations:
  - from: territory
    rel: contains
    to: account
    properties:
      cardinality: one_to_many
```

Navigation aid, not content. Markdown files always win on conflicts. Aim for 15–30 key relationships, not exhaustive graphs.

## Chunking Strategy (schema 2.4+)
Content files declare how they should be chunked for RAG via directory defaults or frontmatter override.

**Strategies:** `atomic` (never split) or `sectioned` (split on ## headers, default).

**Directory defaults:**
- `workflows/` → atomic (procedures are indivisible)
- `troubleshooting/errors/`, `troubleshooting/diagnostics/`, `troubleshooting/common-mistakes/` → atomic
- `interfaces/`, `concepts/`, `faq/`, `propositions/`, `summaries/`, `commercial/` → sectioned
- All others → sectioned

**Per-file override:**
```yaml
---
retrieval:
  strategy: atomic
---
```

Precedence: frontmatter > directory default > sectioned fallback.

When splitting (sectioned), chunks carry sequence metadata: `part X of Y | sequence: {glob}`.

## Volatile Data & Refresh Intervals

For time-bound EK (pricing, API specs, current metrics, leaderboards), isolate in a `volatile/` subdirectory.
Declare a refresh interval in the file's frontmatter:

```yaml
---
volatile:
  refresh: P30D          # ISO 8601 duration — how often to refresh
  source: https://example.com/pricing
  fetched_at: "2026-04-01"
  expires_at: "2026-05-01"   # computed: fetched_at + refresh
---
```

**Rules:**
- `volatile/` files are always Tier 2 (Searchable) — never Tier 1
- Static and volatile content never coexist in the same file
- Volatile files are **excluded from EK ratio measurement** — declare `volatile_excluded: true` in the manifest's `ek_ratio` block
- Staleness check is passive: at session start the agent checks `expires_at` across `volatile/*.md`; if stale, the agent alerts the user — refresh is always user-initiated (agent fetches from `source` URL only when the user explicitly requests it, or alerts the user to update manually if no URL is set)
- The existing `<!-- refresh -->` inline block in core.md remains the standard for *individual volatile facts within static files*; frontmatter TTL is for *fully volatile files* in `volatile/`

**Manifest addition:**
```yaml
ek_ratio:
  value: 0.78
  measured_at: "2026-04-01"
  sample_size: 240
  models: ["gpt-5", "claude-opus-4"]
  volatile_excluded: true   # volatile/ files excluded from measurement
```

**Directory default:** `volatile/` → `atomic` chunking strategy (volatile files are retrieved whole).

## Provenance Metadata (schema v3.0+)

Every content file may carry provenance fields in its YAML frontmatter. These are tooling metadata — strip them at deploy time (ep-strip-frontmatter.py) so they don't dilute RAG embeddings.

```yaml
---
id: territory-overview          # stable slug, unique within pack
content_hash: sha256:abc123     # hash of body content (excludes frontmatter)
verified_at: "2026-04-10"       # ISO date of last human or agent review
verified_by: "agent"            # "human" | "agent" | "import"
---
```

Manifest freshness block (optional, in `manifest.yaml`):
```yaml
freshness:
  refresh_cycle: P90D     # ISO 8601 duration
  coverage_pct: 85        # percentage of files with provenance
  last_review: "2026-04-10"
```

Validator: `ep-validate --provenance` adds W-PROV-01 (missing id), W-PROV-02 (missing hash), W-PROV-03 (missing verified_at), W-PROV-04 (missing verified_by) as warnings.

## Graph Export (schema v3.1+)

`_graph.yaml` at the pack root is a GraphRAG-compatible adjacency file generated by `ep-graph-export.py`. It encodes:
- Wikilinks (`[[filename]]` in body text) → `links_to` edges
- `related:` frontmatter lists → `related_to` edges
- Context hints (`<!-- context: filename -->`) → `context_for` edges

Sample:
```yaml
nodes:
  - id: territory-overview
    file: concepts/territories.md
edges:
  - from: territory-overview
    to: account-structure
    kind: links_to
```

The graph is a navigation/analysis artifact — it does not replace Markdown content. Regenerate it after major structural changes. Commit to the pack repo alongside content files.

## Key Rules
- NO secrets ever
- Distill knowledge, do not copy raw state
- Provenance in frontmatter (strip at deploy time)
- Lead summaries, propositions, glossary for retrieval
- Respect privacy and EK focus

Full details: https://github.com/brianhearn/ExpertPack/schemas
See also: https://expertpack.ai
```

The schemas.md is approximately 3.2KB.