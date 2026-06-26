---
name: memory-graph
description: Agent-agnostic personal knowledge graph stored as markdown files with YAML frontmatter. Use when you need persistent context about the user's life, projects, tools, people, concepts, or decisions — especially across agent resets or switches. Also use when logging significant activity, searching for context before starting work, creating knowledge nodes for new topics, discovering connections between existing nodes (backfill), or rebuilding indexes. Triggers include needing user context, logging work, "remember this", "what do I know about X", creating/updating knowledge entries, and periodic memory maintenance.
---

# Memory Graph

A file-based personal knowledge graph at `~/memory/`. Any agent can read/write. Human-browsable.

## Structure

```
~/memory/
├── README.md              # full architecture doc
├── graph/                 # knowledge nodes
│   ├── people/
│   ├── projects/
│   ├── concepts/
│   ├── places/
│   ├── tools/
│   └── <any-category>/    # extend freely
├── log/                   # daily activity logs
│   └── YYYY-MM-DD.md
├── indexes/               # computed — NEVER edit directly
│   ├── memory.db          # SQLite (primary index, FTS5 search)
│   └── graph.html         # interactive graph visualization
├── backfill/              # connection discovery
│   ├── suggestions.md
│   └── history.md
└── scripts/               # symlinks → skill's scripts/ directory
    ├── rebuild-indexes.js  # full or incremental index rebuild
    ├── suggest-backfill.js # scoped connection discovery (+ QMD semantic)
    ├── query.js            # CLI structural query tool
    ├── briefing.js         # context assembly for agents
    ├── lint.js             # graph validation and health checks
    ├── visualize.js        # D3.js graph visualization generator
    ├── commit.js           # git auto-commit for graph/log changes
    └── promote.js          # log-to-node promotion suggestions
```

**Script location:** Scripts live in the skill directory (`scripts/`). `~/memory/scripts/` contains symlinks to them. All scripts support `MEMORY_ROOT` env var (defaults to `~/memory`) so they resolve paths correctly regardless of where they're installed.

## Setup

If `~/memory/` does not exist, read `references/setup.md` and follow the scaffolding steps. This creates the folder structure, symlinks scripts, seeds initial nodes, and builds indexes.

If `~/memory/` already exists, proceed to Operations below.

## Node Format

Every node is a markdown file with YAML frontmatter:

```yaml
---
type: project
created: 2026-03-20
updated: 2026-03-20
tags: [side-project, saas]
status: active
relations:
  - { to: people/someone, type: owner }
  - { to: tools/nextjs, type: built-with }
---

# Title

Free-form body.

## Changelog

- 2026-03-20: Created node
```

### Required Fields

- `type` — matches parent folder name
- `created` — ISO date

### Recommended Fields

- `updated` — ISO date, last time node content was meaningfully changed. Used for staleness tracking.

### Optional Fields

- `tags` — flat list for categorization
- `status` — `active`, `archived`, `idea`, `done`, etc.
- `relations` — list of `{ to, type }` objects. `to` is relative path within `graph/` (no `.md`). `type` is any string.
- Add any other fields freely — unknown fields are preserved

### Relation Type Taxonomy

Suggested standard types (non-standard types trigger info-level lint warnings):

- **Structural:** `uses`, `built-with`, `part-of`, `contains`
- **Ownership:** `creator`, `owner`, `maintainer`
- **Conceptual:** `related-to`, `inspired-by`, `alternative-to`, `core-concept-of`, `core-value-of`
- **Temporal:** `led-to`, `preceded-by`, `evolved-into`
- **Contextual:** `home-of`, `lives-in`, `works-at`

### Bidirectionality

Write a relation on **one side only**. The index script computes the reverse.

### Changelog Convention

Nodes can have a `## Changelog` section at the bottom of the body. Format:
```
- YYYY-MM-DD: description of what changed
```

### Node Templates

Templates for common node types are in the skill's `templates/` directory:
- `person.md`, `project.md`, `tool.md`, `concept.md`, `place.md`

Use these as starting points when creating new nodes. Copy and edit — don't modify the templates themselves.

## Operations

### 1. Read for Context (Session Start)

```bash
# Check recent activity
cat ~/memory/log/$(date +%Y-%m-%d).md

# Context briefing for a node (full content + relations + recent logs)
node ~/memory/scripts/briefing.js --node projects/flowmind

# Topic briefing (search-based)
node ~/memory/scripts/briefing.js --topic "immutability"

# Semantic search (if QMD is installed — best for natural language queries)
qmd vsearch "trust and data integrity"     # vector similarity
qmd query "what connects X and Y"          # hybrid + reranking

# Structural search
node ~/memory/scripts/query.js --search "keyword"

# Node details with all relations
node ~/memory/scripts/query.js --node projects/flowmind

# All nodes related to something
node ~/memory/scripts/query.js --related-to people/abdullah

# Filter by type and status
node ~/memory/scripts/query.js --type project --status active

# Browse by tag
node ~/memory/scripts/query.js --tag side-project

# Recently modified nodes
node ~/memory/scripts/query.js --recent 7

# Stale nodes (not updated in N days)
node ~/memory/scripts/query.js --stale 30

# Graph overview
node ~/memory/scripts/query.js --stats
```

### 2. Create a Node

1. Check if node already exists: `ls ~/memory/graph/<category>/`
2. Copy a template from the skill's `templates/` directory to `~/memory/graph/<category>/<name>.md`
3. Fill in frontmatter + body (set `created` and `updated` to today)
4. Scan existing nodes for potential relations (shared tags, mentions)
5. Add discovered relations with `type: suggested` if uncertain
6. Log the creation in today's activity log
7. Rebuild indexes: `node ~/memory/scripts/rebuild-indexes.js --incremental`
8. If QMD is installed: `qmd update && qmd embed` (refreshes semantic search)

### 3. Update a Node

1. Read the current node
2. Update frontmatter and/or body
3. Update the `updated` field to today's date
4. Add entry to `## Changelog` section if significant
5. Log the update
6. Rebuild indexes: `node ~/memory/scripts/rebuild-indexes.js --incremental`

### 4. Log Activity

Append to `~/memory/log/YYYY-MM-DD.md` (create if needed):

```markdown
- **HH:MM** [agent-name] Description {ref: path/to/node, path/to/other}
```

`{ref: ...}` references are backfill signals — they hint at connections between nodes.

### 5. Backfill (Discover Missing Connections)

```bash
# Rebuild indexes first (if not recently done)
node ~/memory/scripts/rebuild-indexes.js --incremental

# Generate suggestions (scoped — uses tags, FTS, log co-refs, + QMD semantic)
node ~/memory/scripts/suggest-backfill.js                                  # all nodes
node ~/memory/scripts/suggest-backfill.js --scope recent                   # last 7 days only
node ~/memory/scripts/suggest-backfill.js --scope node:projects/flowmind   # specific node
node ~/memory/scripts/suggest-backfill.js --no-qmd                         # skip semantic search

# Rebuild with automatic scoped backfill on changed nodes
node ~/memory/scripts/rebuild-indexes.js --incremental --with-backfill
```

Review `~/memory/backfill/suggestions.md`. Accept by adding the relation to the node's frontmatter. Reject by logging in `backfill/history.md`.

### 6. Lint (Validate Graph Health)

```bash
node ~/memory/scripts/lint.js            # check for issues
node ~/memory/scripts/lint.js --fix      # auto-fix (adds missing updated fields)
```

Checks: missing required fields, broken relations, orphan nodes, duplicate titles, non-standard relation types.

### 7. Visualize

```bash
node ~/memory/scripts/visualize.js       # generates ~/memory/indexes/graph.html
open ~/memory/indexes/graph.html         # view in browser
```

Interactive D3.js force-directed graph. Nodes colored by type, sized by connections. Click for details.

### 8. Git Backing

```bash
node ~/memory/scripts/commit.js                        # auto-commit graph/ and log/ changes
node ~/memory/scripts/commit.js --message "custom msg"  # with custom message
```

Stages `graph/`, `log/`, `backfill/history.md`, and `README.md` changes, commits with descriptive message. Does NOT auto-push.

### 9. Log Promotion

```bash
node ~/memory/scripts/promote.js           # find recurring topics without nodes
node ~/memory/scripts/promote.js --min 5   # raise mention threshold
node ~/memory/scripts/promote.js --days 30 # only recent logs
```

Scans logs for entities mentioned 3+ times without existing nodes. Suggests node creation.

### 10. Add a New Category

Create a folder under `graph/`. No config changes. Indexes adapt on rebuild.

## Rules

1. **Read before writing.** Check if a node exists before creating a duplicate.
2. **Log significant work.** Append to `log/YYYY-MM-DD.md` when you do something significant.
3. **Use refs in logs.** If your work touches existing concepts/projects, add `{ref: ...}`.
4. **Scan for connections.** When creating a node, check for related nodes (shared tags, mentions).
5. **Never edit `indexes/`.** Run the rebuild script instead.
6. **Add fields freely.** If a node needs a field that doesn't exist yet, just add it.
7. **Add categories freely.** Need `graph/recipes/`? Create the folder. No config changes.
8. **Preserve unknown fields.** If a node has fields you don't recognize, leave them.
9. **Use `suggested` type for uncertain relations.** Let a human or another agent confirm.
10. **One-side relations only.** Write on whichever node feels natural. Index computes the reverse.
11. **Keep the body useful.** Frontmatter is for machines. The markdown body is for humans.
12. **Set `updated` on changes.** Keep the `updated` field current for temporal tracking.
13. **Use standard relation types.** Prefer the taxonomy above. Run `lint.js` to check.
