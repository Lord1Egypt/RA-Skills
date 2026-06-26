# Memory Graph 🧠

A file-based personal knowledge graph for AI agents and humans.

Markdown files with YAML frontmatter. No database required — SQLite indexes are derived, rebuildable, disposable. Your files are the source of truth.

![Memory Graph Visualization](docs/preview.png)

## Why

- **Agent-agnostic** — any AI agent (Claude, Codex, GPT, local LLMs) can read and write to it
- **Human-readable** — it's just markdown files in folders. Browse them, edit them, `grep` them
- **Portable** — no vendor lock-in, no proprietary format, no server needed
- **Persistent** — survives agent resets, reinstalls, and migrations
- **Connected** — relations between nodes surface naturally over time via automated backfill

## What It Looks Like

```
~/memory/
├── graph/                 # knowledge nodes
│   ├── people/
│   │   └── john.md
│   ├── projects/
│   │   └── my-app.md
│   ├── tools/
│   │   └── typescript.md
│   ├── concepts/
│   └── places/
├── log/                   # chronological activity logs
│   └── 2026-03-20.md
├── indexes/               # computed (never edit)
│   ├── memory.db          # SQLite + FTS5 full-text search
│   └── graph.html         # interactive visualization
├── backfill/              # connection discovery
└── scripts/               # symlinks to this skill's scripts/
```

## A Node

Every piece of knowledge is a markdown file:

```yaml
---
type: project
created: 2026-03-20
updated: 2026-03-20
tags: [side-project, saas]
status: active
relations:
  - { to: people/john, type: creator }
  - { to: tools/nextjs, type: built-with }
---

# My App

Description, notes, context — whatever is useful.

## Changelog

- 2026-03-20: Created node
```

Relations are **one-directional in source, bidirectional in index** — write on one side, the index computes the reverse automatically.

## Scripts

All scripts are zero-dependency Node.js 22+ (uses built-in `node:sqlite`).

| Script | What it does |
|--------|-------------|
| **query.js** | Search, browse, filter the graph (`--search`, `--node`, `--tag`, `--type`, `--stats`, `--stale`) |
| **briefing.js** | Generate a context briefing for agents — full node + relations + recent activity (`--node`, `--topic`) |
| **rebuild-indexes.js** | Build/rebuild SQLite index from graph files (`--incremental`, `--with-backfill`) |
| **suggest-backfill.js** | Discover missing connections via tag overlap, FTS, log co-references, and optional [QMD](https://github.com/tobi/qmd) semantic search (`--scope`, `--min-score`) |
| **lint.js** | Validate graph health — missing fields, broken relations, orphan nodes, type consistency (`--fix`) |
| **visualize.js** | Generate an interactive D3.js force-directed graph visualization |
| **commit.js** | Auto-commit changes with descriptive messages (`--message`) |
| **promote.js** | Find recurring log topics that deserve their own node (`--min`, `--days`) |

### Examples

```bash
# Search the graph
node ~/memory/scripts/query.js --search "typescript"

# Get a full briefing for an agent
node ~/memory/scripts/briefing.js --node projects/my-app

# Find stale nodes (not updated in 90+ days)  
node ~/memory/scripts/query.js --stale 90

# Validate the graph
node ~/memory/scripts/lint.js

# Discover missing connections
node ~/memory/scripts/suggest-backfill.js --scope recent

# Generate an interactive graph visualization
node ~/memory/scripts/visualize.js
open ~/memory/indexes/graph.html

# Auto-commit changes
node ~/memory/scripts/commit.js
```

## Key Features

### Context Assembly (briefing.js)

Agents don't need raw data — they need *context*. The briefing script assembles:
- Target node's full content
- All directly related nodes (1 hop) with key fields
- 2nd-hop relations (titles only)
- Recent log entries that reference the node
- Staleness information

One command gives an agent everything it needs to be useful.

### Retroactive Association (suggest-backfill.js)

The most human thing about memory: new information activates old connections. The backfill system:
1. Finds candidates via shared tags, FTS keyword overlap, and log co-references
2. Optionally uses [QMD](https://github.com/tobi/qmd) for semantic similarity search
3. Scores and ranks suggestions by confidence
4. Outputs to `backfill/suggestions.md` for human review

### Temporal Awareness

Nodes track `created` and `updated` dates. The `--stale` flag surfaces nodes that haven't been touched in a while. Briefings include staleness info so agents know how fresh their context is.

### Relation Type Taxonomy

Suggested standard types (enforced as info-level lint hints, not errors):

| Category | Types |
|----------|-------|
| Structural | `uses`, `built-with`, `part-of`, `contains` |
| Ownership | `creator`, `owner`, `maintainer` |
| Conceptual | `related-to`, `inspired-by`, `alternative-to`, `core-concept-of`, `core-value-of` |
| Temporal | `led-to`, `preceded-by`, `evolved-into` |
| Contextual | `home-of`, `lives-in`, `works-at` |

Custom types work fine — the taxonomy is a guide, not a constraint.

## Installation

### As an Agent Skill

If you're using [OpenClaw](https://github.com/openclaw/openclaw) or a similar agent framework:

```bash
# Install the skill
clawhub install memory-graph

# Or manually copy to your skills directory
cp -r ~/projects/memory-graph ~/.agents/skills/memory-graph
```

### Setup

Requires **Node.js 22+** (uses built-in `node:sqlite`). No `npm install` needed.

```bash
# 1. Create the memory directory structure
mkdir -p ~/memory/{graph/{people,projects,concepts,places,tools},log,indexes,backfill,scripts}

# 2. Symlink scripts from the installed skill
SKILL_DIR=~/.agents/skills/memory-graph  # adjust if installed elsewhere
for f in "$SKILL_DIR"/scripts/*.js; do
  ln -sf "$f" ~/memory/scripts/"$(basename "$f")"
done

# 3. Build indexes
node ~/memory/scripts/rebuild-indexes.js

# 4. (Optional) Initialize git for version history
cd ~/memory && git init
echo -e "indexes/\nbackfill/suggestions.md" > .gitignore
git add . && git commit -m "initial memory graph"
```

See [references/setup.md](references/setup.md) for the full setup guide including seed nodes, templates, and agent integration.

## Templates

The `templates/` directory has starter files for common node types:

- `person.md` — people
- `project.md` — projects  
- `tool.md` — tools and services
- `concept.md` — ideas and concepts
- `place.md` — locations

Copy, fill in, and place in the appropriate `graph/` subdirectory.

## Design Philosophy

- **Files over databases.** Readable, portable, version-controllable.
- **Convention over enforcement.** No schema validation. Consistency comes from agents following conventions.
- **Indexes are views, not truth.** The markdown files are the database. Everything else is derived.
- **Connections are living.** Nodes are never "done" — they can always grow new edges.
- **Simple now, extend later.** Start with folders and frontmatter. Add tooling only when the pain justifies it.

## Scaling

The file-per-node design works at any scale. What evolves is the tooling:

| Scale | What works |
|-------|-----------|
| 0–50K nodes | SQLite + FTS5, incremental rebuilds, scoped backfill |
| 5K+ per category | Nested subcategories (no code changes needed) |
| 10K+ nodes | QMD semantic search for smarter backfill |
| 50K+ nodes | Archive layer for inactive nodes and old logs |

The design invariant: **markdown files are always the source of truth.** Everything else is derived, rebuildable, disposable.

## Requirements

- **Node.js 22+** (built-in `node:sqlite`)
- No external npm dependencies
- Optional: [QMD](https://github.com/tobi/qmd) for semantic search in backfill

## License

MIT
