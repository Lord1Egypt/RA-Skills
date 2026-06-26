# Memory Graph — Setup Guide

Follow these steps to scaffold the memory framework from scratch. Requires Node.js 22+ (built-in `node:sqlite`).

## 1. Create Directory Structure

```bash
mkdir -p ~/memory/{graph/{people,projects,concepts,places,tools},log,indexes,backfill,scripts}
```

## 2. Link Scripts

Scripts live in the skill directory (`scripts/`). Symlink them into `~/memory/scripts/` so they're accessible from the memory root:

```bash
# Determine the skill directory. Adjust SKILL_DIR if installed elsewhere.
# Common locations:
#   ~/.agents/skills/memory-graph    (clawhub / manual install)
#   ~/projects/memory-graph          (dev / project copy)
SKILL_DIR=~/.agents/skills/memory-graph

# If scripts/ isn't in the installed skill (e.g. clawhub installs only SKILL.md + references/),
# point to a local clone or project copy that has the scripts/ and templates/ directories.

for f in "$SKILL_DIR"/scripts/*.js; do
  ln -sf "$f" ~/memory/scripts/"$(basename "$f")"
done
```

All scripts support the `MEMORY_ROOT` environment variable (defaults to `~/memory`). This means they work correctly through symlinks regardless of where the skill is installed.

### Scripts Reference

| Script | Purpose |
|--------|---------|
| `rebuild-indexes.js` | SQLite index rebuild. Default is full rebuild. Supports `--incremental`, `--with-backfill` |
| `query.js` | CLI query tool: `--search`, `--node`, `--related-to`, `--tag`, `--type`, `--stats`, `--recent`, `--stale` |
| `suggest-backfill.js` | Scoped connection discovery via tags, FTS, log co-refs, QMD semantic |
| `briefing.js` | Context assembly: `--node <path>` or `--topic <query>` for agent briefings |
| `lint.js` | Graph validation: missing fields, broken relations, orphans, duplicates. `--fix` to auto-fix |
| `visualize.js` | Generate interactive D3.js graph HTML at `indexes/graph.html` |
| `commit.js` | Auto-commit graph/ and log/ changes. `--message` for custom message |
| `promote.js` | Find recurring log topics without nodes. `--min N`, `--days N` |

## 3. Templates

Node templates are in the skill's `templates/` directory:

- `person.md` — people nodes
- `project.md` — project nodes
- `tool.md` — tool/service nodes
- `concept.md` — idea/concept nodes
- `place.md` — location nodes

Use them as starting points when creating new nodes:

```bash
cp "$SKILL_DIR"/templates/project.md ~/memory/graph/projects/my-project.md
# Edit the file with actual content
```

## 4. Create README.md

Copy the README template from the skill's `references/` directory, or write one covering:

- What it is (file-based knowledge graph, agent-agnostic, human-readable)
- Directory structure (graph/, log/, indexes/, backfill/, scripts/)
- Node format (YAML frontmatter + markdown body)
- Relation format, bidirectionality, type taxonomy
- Log format and backfill signals
- Agent rules
- Changelog convention, git backing
- Philosophy

A comprehensive example README is typically generated during first setup. See the main SKILL.md for the canonical documentation of all conventions.

## 5. Initialize Backfill Files

Create `~/memory/backfill/suggestions.md`:
```markdown
# Backfill Suggestions

_No pending suggestions._
```

Create `~/memory/backfill/history.md`:
```markdown
# Backfill History

Audit trail of accepted and rejected suggestions.

_No history yet._
```

## 6. Initialize Git Repository

```bash
cd ~/memory
git init

# Create .gitignore
cat > .gitignore << 'EOF'
indexes/
backfill/suggestions.md
EOF

git add .
git commit -m "initial memory graph"
```

This tracks `graph/` and `log/` in version control. Indexes and suggestion files are excluded (they're derived/ephemeral).

After initial setup, use `commit.js` to auto-commit changes:

```bash
node ~/memory/scripts/commit.js
```

## 7. Seed Initial Nodes

Create nodes for known entities from user context. Each follows the node format in the main SKILL.md. Start with:

- `graph/people/` — the user, key people
- `graph/projects/` — active and planned projects
- `graph/tools/` — tech stack, services
- `graph/concepts/` — important ideas, values
- `graph/places/` — significant locations

Use templates as starting points:

```bash
cp "$SKILL_DIR"/templates/person.md ~/memory/graph/people/username.md
# Edit the file with actual content
```

## 8. Build Indexes and Verify

```bash
node ~/memory/scripts/rebuild-indexes.js
node ~/memory/scripts/query.js --stats
node ~/memory/scripts/lint.js
node ~/memory/scripts/visualize.js
node ~/memory/scripts/suggest-backfill.js
```

The framework is ready. Return to the main SKILL.md for ongoing usage.

## 9. OpenClaw Agent Integration (Optional)

If you're an OpenClaw agent with your own workspace memory (MEMORY.md, AGENTS.md, daily files), integrate the two systems to avoid duplication.

### Slim Down MEMORY.md

Move factual knowledge out of your MEMORY.md into graph nodes. MEMORY.md should only contain:

- **Agent-specific context** — your personality, tone, working relationship with the user
- **Operational lessons** — mistakes you made, things you learned about how to work
- **Preferences** — how the user likes to be communicated with, what to avoid

Things that should be **graph nodes instead**:
- Project details, architecture, status, tech stack
- People — names, roles, relationships
- Tools, services, accounts
- Concepts, decisions, values

### Update AGENTS.md

Add a section explaining the two memory systems so future sessions understand the split:

```markdown
### Two Memory Systems

1. **Memory Graph** (`~/memory/`) — agent-agnostic knowledge graph. Facts about projects,
   people, tools, concepts, decisions. Structured, queryable, shared across all agents.
   Use the `memory-graph` skill. Log activity to `~/memory/log/YYYY-MM-DD.md`.

2. **Workspace Memory** (this folder) — agent-specific. Personality, relationship context,
   operational lessons, session notes. MEMORY.md for long-term agent context.
   memory/YYYY-MM-DD.md for session-specific notes.

**Rule:** Don't duplicate facts in MEMORY.md that belong in the graph. If it's about a
project, person, tool, or concept — it's a graph node. If it's about how you work or
your relationship with the user — it stays here.
```

### Update Heartbeat / Memory Maintenance

Add graph maintenance to your periodic tasks:

- Check if recent activity should create new graph nodes
- Run `node ~/memory/scripts/suggest-backfill.js --scope recent` after creating nodes
- During memory reviews, migrate any factual content from MEMORY.md to graph nodes

### Dual Logging

- **Graph log** (`~/memory/log/YYYY-MM-DD.md`) — significant activity, shared across agents
- **Workspace daily files** — session-specific notes only you need

Don't double-log. If it matters to any agent, log it in the graph. If it's just your operational context, keep it local.
