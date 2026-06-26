---
name: doc-orchestrator
description: Orchestrate multi-chapter document generation using sub-agents. Use when producing long structured documents (PRDs, technical specs, research reports, design docs, worldbuilding) that exceed single-agent context limits. Handles dependency analysis, contract-first decomposition, serial/parallel scheduling, file isolation, state persistence, and consistency validation.
---

# Doc Orchestrator

Generate long, multi-chapter documents by coordinating sub-agents with a **contract-first, serial-then-parallel** strategy and **persistent orchestration state**.

## When This Applies

- Document has **3+ chapters/sections** with cross-references
- Total expected output **> 500 lines**
- Multiple sections share definitions (names, enums, constants, values)

## Core Principles

1. **Contract First** — Define all shared definitions before delegating
2. **File Isolation** — Each sub-agent writes to its own file; main agent merges
3. **State Persistence** — Write orchestration state to JSON so context compaction can't break the workflow

## Workflow

### Phase 1 — Analyze Dependencies

Build a dependency graph. For each pair ask: "Does chapter B need chapter A's output?"

Classify:
- **Contract** — defines shared values (main agent writes directly)
- **Serial** — has upstream dependency (spawn after dependency completes)
- **Parallel** — no unresolved dependencies (run concurrently)

Optimize: if multiple chapters depend only on the contract, they can run in parallel.

### Phase 2 — Initialize State File

Create `{task-dir}/{TASK-ID}-orchestration.json`:

```json
{
  "document": "Document Title",
  "contract_file": "TASK-XXX-contract.md",
  "final_file": "TASK-XXX-final.md",
  "chapters": {
    "ch1": {"title": "Overview", "status": "done", "file": "TASK-XXX-contract.md", "deps": []},
    "ch2": {"title": "Characters", "status": "pending", "file": "TASK-XXX-ch2.md", "deps": ["ch1"]},
    "ch3": {"title": "Abilities", "status": "pending", "file": "TASK-XXX-ch3.md", "deps": ["ch1"]},
    "ch4": {"title": "Factions", "status": "pending", "file": "TASK-XXX-ch4.md", "deps": ["ch1", "ch2"]}
  }
}
```

Status values: `pending` | `running` | `done` | `failed`

**Update this file after every state change.** After context compaction, `read` this file to restore full state.

### Phase 3 — Write the Contract

Main agent writes all contract chapters directly. Include a **Global Conventions** table:

```markdown
## Global Conventions
| Item        | Value       | Referenced by  |
|-------------|-------------|----------------|
| Score range | 1-5 integer | ch5 API, ch6   |
```

This is the single source of truth.

### Phase 4 — Execute (Serial + Parallel)

For each chapter whose deps are all `done`:
1. Update state: `"status": "running"`
2. Spawn sub-agent with the prompt template (see below)
3. On completion: update state to `"done"`; check what new chapters are unblocked
4. On failure: update state to `"failed"`; decide retry or main-agent fallback

Spawn all unblocked chapters in parallel. Wait for serial dependencies.

**After context compaction:** `read` the orchestration JSON to recover state, then continue.

### Phase 5 — Merge & Validate

Concatenate files in chapter order. During merge:

1. **Strip duplicate document titles** — Sub-agents often repeat the top-level `# Document Title`. Remove all occurrences except the one in the contract file:
   ```bash
   # Remove duplicate H1 titles during merge (keep only from contract)
   cat contract.md > final.md
   for f in ch2.md ch3.md ... ; do
     sed '/^# Document Title$/d' "$f" >> final.md
   done
   ```

2. **Run consistency checks:**
   ```bash
   grep -n "conflicting_value" final.md
   grep -o "'[a-z_]*'" final.md | sort | uniq
   ```

3. Fix any issues before delivering.

## Sub-Agent Prompt Template

```
## Task: Write [Chapter Title] for [Document Name]

**Read first:** `path/to/contract.md`
Pay attention to Global Conventions table (section X.X).

**Write to:** `path/to/output-chN.md` (new file, do NOT modify other files)

**IMPORTANT formatting rules:**
- Do NOT include the document title (# Document Title) — it belongs only in the contract
- Start your file directly with the chapter heading (## Chapter N: Title)
- Do NOT repeat definitions from the contract; reference them

### Content requirements:
[chapter-specific requirements]

### Constraints (must match contract):
- [constraint 1]
- [constraint 2]
```

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Rely on context memory for orchestration state | Persist state to JSON file |
| Let sub-agents write to the same file | Each writes own file; main agent merges |
| Skip formatting rules in prompt | Explicitly say "no document title, start with ## chapter heading" |
| Assume sub-agents won't hit content filters | Have fallback: main agent writes sensitive chapters directly |
| Skip consistency check after merge | Always grep for known conflict patterns |
| Use bigger model to brute-force long output | Smaller model + smaller task > bigger model + huge task |
| Poll sub-agents in a loop | Use push-based completion (auto-announce) |

## Decision Flowchart

```
Document request received
  |
  +-- < 500 lines expected? --> Write directly (no orchestration)
  |
  +-- 500-1500 lines, no cross-refs? --> Simple parallel (each chapter = own file)
  |
  +-- > 500 lines WITH cross-references?
       |
       1. Analyze dependency graph
       2. Create orchestration state JSON
       3. Main agent writes contract chapters
       4. Serial chain for dependent chapters
       5. Parallel burst for independent chapters
       6. Merge + strip duplicate titles + validate
       7. Deliver
```

## Lessons from Real Usage

### Test 1: PRD (9 chapters, technical)
| Metric | Naive Parallel (v1) | Contract-First (v2) |
|--------|--------------------|--------------------|
| Output | 1,405 lines | 3,055 lines |
| Consistency | Score 1-5 vs 1-10 conflict | Zero conflicts |
| File integrity | Chapters overwritten | All preserved |
| Rework | 4 chapters rewritten | None |

### Test 2: Worldbuilding Bible (7 chapters, creative writing)
| Metric | Result |
|--------|--------|
| Output | 2,170 lines |
| Consistency | Zero conflicts (names, factions, abilities all matched) |
| Issues hit | Content filter blocked ch5 twice; ch6 output wrong chapter content |
| Recovery | Main agent wrote ch5 directly; ch6 retried successfully |
| Duplicate titles | 4 of 6 sub-agent files repeated doc title (fixed in merge) |

### Key Takeaways
- **Content filters**: Sensitive topics (war, conflict) may trigger model safety filters in sub-agents. Fallback: main agent writes those chapters, or rephrase with softer language
- **Wrong output**: Sub-agents occasionally output content for the wrong chapter. Always verify file content, not just file existence
- **Title duplication**: Sub-agents copy the document title from the contract file. Prompt template now explicitly forbids this; merge step strips duplicates as safety net
