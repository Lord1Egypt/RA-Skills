# DAG Orchestration — RFC-Driven Multi-Unit Workflows

The most sophisticated pattern: decompose an RFC into a dependency DAG, run each unit through tiered quality pipelines, land via merge queue.

## Architecture

```text
RFC/Spec
    │
    ▼
DECOMPOSITION (AI)
Break into work units with dependency DAG
    │
    ▼
┌───────────────────────────────────────┐
│  For each DAG layer (parallel):       │
│  ├─ Quality Pipelines (per unit)      │
│  │  research → plan → implement       │
│  │  → test → review → fix → final     │
│  └─ Merge Queue (rebase + test + land)│
└───────────────────────────────────────┘
```

## RFC Decomposition

AI reads the RFC and produces work units:

```typescript
interface WorkUnit {
  id: string;                  // kebab-case
  name: string;                // Human-readable
  rfcSections: string[];       // Which RFC sections this addresses
  description: string;         // Detailed description
  deps: string[];              // Dependencies (other unit IDs)
  acceptance: string[];        // Concrete acceptance criteria
  tier: "trivial" | "small" | "medium" | "large";
}
```

**Decomposition rules:**

- Prefer fewer, cohesive units (minimize merge risk)
- Minimize cross-unit file overlap (avoid conflicts)
- Keep tests WITH implementation (never separate)
- Dependencies only where real code dependency exists

## Complexity Tiers

Different tiers get different pipeline depths:

| Tier | Stages | Time |
|------|--------|------|
| **trivial** | implement → test | 5 min |
| **small** | implement → test → code-review | 15 min |
| **medium** | research → plan → implement → test → reviews → fix | 1 hour |
| **large** | same as medium + final-review | 2 hours |

This prevents expensive operations on simple changes while ensuring architectural changes get thorough scrutiny.

## Separate Context Windows (Author-Bias Elimination)

Each stage runs with a different agent/model:

| Stage | Purpose |
|-------|---------|
| Research | Read codebase + RFC, produce context |
| Plan | Design implementation steps |
| Implement | Write code following plan |
| Test | Run build + test suite |
| Code Review | Quality + security check |
| Review Fix | Address review issues |
| Final Review | Final quality gate |

**Critical:** The reviewer never wrote the code it reviews. Eliminates author bias.

## Merge Queue with Eviction

After quality pipelines complete, units enter the merge queue:

```text
Unit branch
    │
    ├─ Rebase onto main
    │   └─ Conflict? → EVICT (capture context)
    │
    ├─ Run tests
    │   └─ Fail? → EVICT
    │
    └─ Pass → Fast-forward + delete branch
```

**Eviction Recovery:**
When evicted, full context is captured and fed back to implementer on next pass:

```markdown
## MERGE CONFLICT — RESOLVE

Your previous implementation conflicted with another unit.
Restructure to avoid these files/lines:

{full diffs}
```

## Worktree Isolation

Each unit runs in isolated worktree. Pipeline stages **share** the same worktree, preserving state (context files, code changes) across research → plan → implement → test → review.

## Key Design Principles

1. **Deterministic execution** — Upfront decomposition locks parallelism/ordering
2. **Human review at leverage points** — Work plan is highest-leverage intervention
3. **Separate concerns** — Each stage separate context window
4. **Conflict recovery with context** — Full eviction context enables intelligent re-runs
5. **Tier-driven depth** — Trivial changes skip research; large changes get max scrutiny
6. **Resumable** — Full state persisted; resume from any point

## When to Use DAG vs Simpler Patterns

Use **DAG for:**

- Multiple interdependent work units
- Parallel implementation needed
- Merge conflicts likely
- Multi-day feature development
- RFC/spec already complete

Use **Sequential for:**

- Single focused change
- No parallel work
- Simple workflows

Use **Parallel Agents for:**

- Many variations of same thing
- No merge coordination needed
- Spec-driven generation
