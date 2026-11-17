---
name: agentic-maestro
description: "Delegate coding work to sub-agents efficiently with a strong orchestrator and cheaper executors: when to spawn, how to write a precise brief, how to spawn on Claude Code (Agent tool or claude -p), Codex (codex exec) or OpenCode (opencode run), and how to run build -> review -> fix -> merge with an independent reviewer. Use when spawning or delegating implementation, fixes, integration, reviews or parallel agents, when writing an executor brief, or when running a multi-agent build pipeline."
license: MIT
compatibility: Claude Code, Codex, OpenCode (any Agent Skills host); Node.js 18+ and bash for the scripts
---

# agentic-maestro

The strong model is the **maestro**: it holds all the context, makes every design decision and writes
precise parts. Cheaper models are the **players**: each executes one part exactly, without the whole
score. Precise briefs plus an independent review are the safeguard, not a guarantee; the executor's
intelligence changes the cost, not the safeguard.

Files: `templates/` (brief, fix-brief, integration-brief, the shared `_rules.md`, a Claude Code agent
definition, an example brief spec), `scripts/` (below), `references/harnesses.md` (spawn calls per
harness), `references/checklist.md` (pre-review checklist and how it grows), `references/operations.md`
(concurrency, lanes, git, reviewer prompts, context, cost ledger).

| Script | Does |
|---|---|
| `scripts/brief.mjs <spec.json> --out <file>` | Assembles a brief from a JSON spec; refuses missing values, excerpts or keywords |
| `scripts/spawn.mjs --harness claude\|codex\|opencode ...` | Runs one headless agent; writes `result.json` (session id, exit, tokens) and a ledger row |
| `scripts/scope-check.sh <worktree> <base> <allowed>...` | Lists changed files outside the brief's map |
| `scripts/excerpt.sh`, `scripts/conv.sh` | A pattern excerpt; the matching convention bullets, verbatim |
| `scripts/codemap.mjs <repo> [groups] \| --generic` | Generates `docs/CODEMAP.md` (JS/TS workspaces, or any git repo) |
| `scripts/gate.sh <cmd>` | Machine-wide lock: at most N heavy checks at once |

## 0. Spawn or do it yourself

A spawn costs a brief (~5–12 KB of orchestrator output), a review and a commit. Do it inline when ANY
holds: the change is one file or under ~50 changed lines; writing the brief would take longer than the
change; it is a one-line fix to a review finding; the task needs judgement the brief cannot pin down.
Spawn when the work is self-contained behind exact rulings, touches several files or packages, or can
run in parallel with other lanes. For facts you need to WRITE a brief (where is the pattern, who calls
X), a cheap read-only scout that returns paths and facts — not file dumps — is fine; design stays here.

## Part A — Writing a brief

### Roles
- The orchestrator specifies **observable** behaviour exactly: interfaces, limits, error codes and the
  critical invariants. It never writes "decide how to…".
- Routine implementation choices — local names, helper structure, internal layout — are the executor's.
- The executor implements exactly the brief, reads only its map plus their imports, callers, types and
  tests, and reports anything else as a blocked question.

### Sections (template order — stable blocks first, so parallel lanes share a cached prefix)
1. **Rules**: `templates/_rules.md`, identical in every brief (logging with exit codes, bounded reading,
   gates once, stop after 3 identical errors, scope, tests are evidence, safety, blocked questions).
2. **Role**, then **Conventions**: only the project rules that apply, quoted verbatim (`conv.sh`).
3. **Checklist**: only the areas the feature touches (`references/checklist.md` format).
4. **Workspace**: baseline SHA, exact working directory, branch, env exports, prerequisites, "do not
   commit".
5. **Feature**: id and acceptance criteria quoted exactly, plus the spec lines that define it.
6. **Rulings** R1..Rn: exact semantics — names, codes, limits, formulas, refusal behaviour, versioning,
   and the dependency contracts not to break. Near-code precision for security, money, persistence and
   parsing. Anything that parses, validates or gates is FAIL-CLOSED.
7. **Done means**: the exact assertions the tests must prove.
8. **Map**: the only files it may create or change, ONE existing feature as the pattern, and the
   `docs/CODEMAP.md` sections to read.
9. **Excerpts**: usually ~2 key functions of the pattern (`excerpt.sh`).
10. **Gates**: exact per-package commands, wrapped by `gate.sh` when lanes run in parallel.
11. **Report**: the fixed block (STATUS / FILES / one line per ruling / one line per gate / CHECKLIST /
    BLOCKED), so a report is scanned in seconds and grepped across lanes.

Use `scripts/brief.mjs` (see `templates/brief-spec.example.json`): it fills the template, pulls
excerpts, conventions and checklist areas, prefixes gates, and refuses on any gap. ~12 KB is a
guideline for context cost, not a limit.

### Fix briefs (`templates/fix-brief.md`)
- Each finding quoted with file:line, then the exact ruling and the test that proves it.
- Only the affected files; never "re-read the feature".
- Repeat the rules, workspace, conventions, invariants and still-valid rulings: a fresh session knows
  nothing.
- Always a FRESH session per round; never resume the builder (its transcript multiplies cost).
- Same component with findings 3 rounds in a row: the brief carries a **structural ruling** that removes
  the whole category ("the caller can no longer name the destination; derive it"), not another patch.

### Integration briefs (`templates/integration-brief.md`)
- Exact merge order with commit messages and the SHA each merged branch must contain.
- Renumbering (migrations, decision records) with every reference; code that moved since the branch cut.
- Authority: commit and push ONLY on the integration branch; the orchestrator merges to main.
- The invariants that must hold after the merge, each tested; semantic conflicts are reported, never
  resolved by the executor.

## Part B — Running the pipeline

1. **Plan**: resolve every ambiguity as explicit rulings before any build. Split the work into lanes,
   each with the files it owns; give shared hotspots (barrels, lockfiles, migration numbers, generated
   files) to one lane or to integration, and pick each lane's executor by risk (below).
2. **Spawn**: one executor per lane with its brief, in its own worktree, as a tracked background job
   (`references/harnesses.md`). Record each session id.
3. **Blocked questions**: answer in the SAME session (`SendMessage` / `spawn.mjs --resume <id>`) while
   its context is small — the executor finished everything else first. Only fix rounds start fresh.
4. **Check scope, then commit**: `scope-check.sh <worktree> <base> <map...>`; out-of-map files are
   reverted or ruled on BEFORE review. Check `git status`, commit (the orchestrator commits).
5. **Review and verify in parallel** on that commit: an independent reviewer (a different model family)
   and your own light verification.
6. **Arbitrate**: per finding, AGREE with an exact fix ruling, or DISAGREE / DEFER with a reason. Never
   forward raw findings. Tag each agreed finding with a category; a category recurring in a second
   feature becomes a project checklist rule (`references/checklist.md`).
7. **Fix**: a fresh executor with the fix brief.
8. **Re-review**: resume the reviewer's OWN session id (never "the last session"); it reads the fix
   diff PLUS the invariants the fix touches and any open findings — never the fix diff alone.
9. **Integrate** the batch; the reviewer reviews the final integrated commit (SHA).
10. **Merge** small batches of 1–3 features as soon as each passes.

### Merge acceptance
Gates pass on the exact commit being merged; no unresolved P1/P2 findings; every deferral has a written
reason; the approval is tied to one immutable commit SHA.

### Reviewer grounding
Every review receives the original requirements/acceptance text, the brief's rulings, read access to the
repository and the dependency contracts, and explicit permission to challenge a ruling ("if a ruling
itself is wrong, say so"). Prompt shape: `references/operations.md`.

### Verification levels
- **Executor**: per-package checks of the packages it changed.
- **Orchestrator (light)**: whole-repo typecheck and lint once, plus the suites of the changed packages
  and the apps that consume them. Judge by exit codes, never by piped output.
- **Full fresh-clone battery**: once at the end, or overnight. Not per merge.
- Refactors that move files also run tests that scan source text or file lists (architecture tests).

### Model, effort and cost
- Orchestrate with the strongest affordable model (plan, rule, arbitrate, merge).
- Route executors by **risk and observed history up front**: plumbing, schemas, CRUD, UI and refactors
  go to a cheap model at high effort; security rules, parsers of untrusted input, money, renderers and
  determinism, and cross-system end-to-end work go to a strong model from the start, at max effort for
  new builds. Fix rounds and integration: high is enough.
- Track cost per feature (orchestration + execution + review + rework) in the ledger
  (`references/operations.md`) and let it move component classes between executors.

### Keep the orchestrator's context small
Read the report block and `result.json`, not transcripts; read the full report and logs only when the
status is not done, an exit code is non-zero or the verdict is not PASS. Use `excerpt.sh` and the code
map instead of opening large files.
