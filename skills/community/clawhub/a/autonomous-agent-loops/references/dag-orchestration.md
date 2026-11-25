# DAG Orchestration — RFC-Driven Multi-Unit Workflows

> ## ⚠️ Read Before Use
>
> This is the most powerful pattern in this skill. It decomposes an RFC into a dependency graph, runs each unit through tiered quality pipelines, and lands via a merge queue. The merge-conflict recovery flow was rewritten in 1.0.1 to **never include full diffs in agent prompts** — see `Merge-Conflict Recovery` below.

The most sophisticated pattern: decompose an RFC into a dependency DAG, run each unit through tiered quality pipelines, land via merge queue with explicit human approval at each merge.

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
│  └─ Merge Queue (rebase + test →     │
│     human approval → land)            │
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

## Merge Queue with Conflict Recovery

After quality pipelines complete, units enter the merge queue:

```text
Unit branch
    │
    ├─ Rebase onto main
    │   └─ Conflict? → Conflict-recovery flow (see below)
    │
    ├─ Run tests
    │   └─ Fail? → Conflict-recovery flow (see below)
    │
    └─ Pass → Request human approval → Land → Delete branch
```

**Land requires explicit human approval.** The merge queue prepares the merge but does not execute it. A human reviews the prepared diff and approves with `dag merge approve <unit-id>`.

### Merge-Conflict Recovery (1.0.1 Rewrite)

When a rebase conflict or test failure occurs, the unit does NOT get "evicted" with full diffs fed back into the agent prompt (the previous design, which was both unsafe and wasteful). Instead:

1. **Pause the unit.** Mark it as `blocked:conflict` in the DAG state file.
2. **Write a structured `MERGE_NOTES.md`** at the unit's worktree root. Contents:
   - The conflicting files (paths only, no diffs)
   - The units/branches involved in the conflict
   - The test command that failed and its exit code (no log content)
   - A timestamp
3. **Surface `MERGE_NOTES.md` to a human.** No automatic retry, no auto-feed to the next agent pass. A human reads the note and decides whether to:
   - Reorder the DAG so the conflicting units are sequenced
   - Manually resolve the conflict
   - Adjust unit scopes to reduce overlap
4. **Only after human approval**, the orchestrator restarts the unit with a fresh context window and a one-line summary of the conflict ("unit-X conflicted with unit-Y on file-Z; human resolved as [resolution]").

**Why this design:**

- **No full diffs in agent prompts.** Full diffs of internal code, paths, and structure are exactly the kind of context that should not be amplified through automated loops. The previous "capture context" pattern was both an exfiltration risk and a context-bloat trap.
- **Human in the loop at the high-leverage point.** Reordering a DAG is one of the cheapest, highest-impact interventions. It's the right place for human judgment.
- **Bounded recovery.** No retry storm, no context accumulation, no chance for the loop to "discover" that capturing more context helps.

## Worktree Isolation

Each unit runs in isolated worktree. Pipeline stages **share** the same worktree, preserving state (context files, code changes) across research → plan → implement → test → review.

Worktrees must be created under the repo's `.worktrees/<unit-id>/` directory — never in `~`, `/tmp`, or any shared location. The orchestrator validates the path before creating the worktree.

## Key Design Principles

1. **Deterministic execution** — Upfront decomposition locks parallelism/ordering
2. **Human review at leverage points** — DAG reordering + final merge approval
3. **Separate concerns** — Each stage separate context window
4. **Bounded conflict recovery** — Structured notes, human decision, no diff amplification
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