---
name: agent-memory-hierarchy
description: Structure an OpenClaw agent's memory like a computer — using a cache hierarchy (hot/warm/cold), a YAML fact store for directly addressable data, a lookup index for O(1) retrieval, and prose files only for narrative and behavioral context. Use when asked to restructure agent memory, reduce context window token usage, improve memory retrieval speed, migrate from prose-only memory to structured memory, or design a new agent memory system from scratch.
---

# Agent Memory Hierarchy

Agents typically store everything as prose in a single MEMORY.md. This works but wastes tokens and makes retrieval fuzzy. This skill structures memory the way computers do: hot cache, warm storage, cold archives, typed data, and a lookup index.

## Core Principle

**Facts go in YAML. Narrative goes in prose. Everything gets an index.**

Three reasons:
1. YAML is ~40% more token-efficient than prose for the same information
2. Specific facts become directly addressable — no semantic search needed
3. Separation of concerns: behavioral rules, narrative context, and facts are distinct problems

---

## The Three-Layer Architecture

### Layer 1 — Hot Cache (always in context)
**File:** `MEMORY.md`

Contains only:
- Identity summary (2-3 lines)
- Behavioral rules (how the agent must behave)
- Standing permissions
- Narrative context that needs interpretation (relationships, mission, origin story)
- Pointers to Layer 2

Does NOT contain: facts, dates, numbers, file paths, IDs, project statuses, todos.

Target size: under 80 lines / ~1000 tokens.

### Layer 2 — Warm Storage (loaded on demand)
**Files:** `memory/facts.yaml`, `memory/lookup-index.md`, `memory/project-*.md`

**`facts.yaml`** — All structured factual data:
- Identity facts (name, contact, IDs)
- Dates and numbers (age, salary, target year, budget)
- File paths and system config
- Project statuses (one-line each, with pointer to full file)
- Outstanding TODOs
- Services and accounts

**`lookup-index.md`** — Explicit directory table:
```markdown
| I need to know... | Go here |
|---|---|
| Contact info | memory/facts.yaml → identity |
| Project statuses | memory/facts.yaml → projects |
| Book research | workspace/book-research/ |
```

**`project-*.md`** — Full narrative project files, loaded only when working on that project.

### Layer 3 — Cold Storage (rarely accessed)
**Files:** `memory/YYYY-MM-DD.md` (daily logs)

Raw session logs. Never loaded automatically. Retrieved only when investigating history or refreshing long-term memory.

---

## Migration Process

Follow this order when converting an existing prose-only MEMORY.md:

### Step 1: Audit existing MEMORY.md
Read the full file and categorize every piece of information:
- **Fact** → moves to `facts.yaml` (name, email, date, number, path, ID, status)
- **Behavioral rule** → stays in MEMORY.md
- **Narrative/context** → stays in MEMORY.md (relationship descriptions, quotes, origin stories)
- **Project detail** → moves to or stays in `project-*.md`

### Step 2: Build `memory/facts.yaml`
Use this schema pattern:
```yaml
# memory/facts.yaml
# Structured factual data — directly addressable, token-efficient
# Last updated: YYYY-MM-DD

identity:
  full_name: ...
  email: ...
  telegram_id: ...

health:
  condition: ...
  status: ...

technical:
  machine: ...
  os: ...
  workspace: ...

paths:
  api_keys: ...
  error_log: ...

projects:
  project_name: {file: memory/project-name.md, status: "one-line status"}

todos:
  - Todo item one
  - Todo item two
```

Rules for facts.yaml:
- Flat where possible, nested where grouping helps
- One-line values only — no multi-line prose
- If a value needs explanation, it belongs in MEMORY.md prose instead
- Add `# Last updated: YYYY-MM-DD` at top

### Step 3: Build `memory/lookup-index.md`
Create a markdown table mapping "I need to know X" → exact file and section.
Every project file, reference file, and key section should have an entry.
This is your agent's O(1) lookup. When you need something, check here first.

### Step 4: Rewrite MEMORY.md
Remove everything that moved to facts.yaml. What remains:
- 2-3 line identity/mission summary
- Behavioral rules (explicit, imperative)
- Standing permissions
- Narrative sections that require context to understand
- Pointers: `# Structured facts → memory/facts.yaml` and `# Find anything → memory/lookup-index.md`

### Step 5: Verify
After migration, confirm:
- [ ] Every fact in old MEMORY.md is now in facts.yaml
- [ ] lookup-index.md covers every project and reference file
- [ ] MEMORY.md contains no facts (no dates, numbers, paths, IDs)
- [ ] New MEMORY.md is under 80 lines
- [ ] Agent can answer "where is X?" using lookup-index.md without searching

---

## Using the Architecture Day-to-Day

**At session start:** Load MEMORY.md (hot cache) only.

**When you need a specific fact:** Check lookup-index.md → go directly to that file/section.

**When working on a project:** Load the specific `project-*.md` file.

**When updating facts:** Edit `facts.yaml` directly. No need to touch MEMORY.md.

**When updating todos:** Edit `facts.yaml → todos`. One place, always current.

**Maintenance cadence:**
- After each session: update `facts.yaml` if any facts changed
- Weekly: review `MEMORY.md` behavioral rules for accuracy
- Monthly: read recent daily logs, distill lessons into MEMORY.md, archive old logs

---

## What NOT to Structure

Some things resist YAML and belong in prose:

- Relationship dynamics ("she calls me Mols, treat her like a friend not a user")
- Emotional context ("Kim feels like the one who got skipped")
- Mission statements and quotes
- Lessons learned with nuance ("DALL-E 3 is inconsistent for coloring pages — use Canva AI instead")
- Anything where the *why* matters as much as the *what*

When in doubt: if it would lose meaning as a key-value pair, keep it in prose.

---

## Reference Files

- `references/facts-yaml-template.md` — copy-paste starting template for facts.yaml
- `references/lookup-index-template.md` — copy-paste starting template for lookup-index.md
