# autoimprove

Autonomous optimization loop for AI agents. Describe what to improve, how to measure it, and walk away.

Inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) and [Shopify Liquid PR #2056](https://github.com/Shopify/liquid/pull/2056).

## How it works

```
/autoimprove              →  Checks what's ready, what's missing
                          →  No improve.md? → scaffolds one
                          →  No eval harness? → builds one interactively
                          →  No tests? → generates goal-aware tests
                          →  Establishes baseline score
                          →  LOOP:
                               Propose change → git commit (verified)
                               → run tests → pass? → run benchmark
                               → check guards → score improved?
                               → yes: keep → no: git reset
                               → log experiment → repeat
                          →  Print summary
```

One command. The agent detects what's missing and walks you through setup before starting the loop. You don't need to know which sub-commands exist.

## Quick start

The fastest path: just run `/autoimprove` in your project. It will detect the repo type, ask you a few questions, and scaffold everything.

Or create an `improve.md` yourself for full control:

```markdown
# autoimprove: make-it-faster

## Change
scope: the checkout handler and its database queries

## Check
test: go test ./...
run: go test -bench=. -benchmem
score: ns/op:\s+([\d.]+)
goal: lower
guard: allocs/op: ([\d.]+) < 500
timeout: 3m

## Stop
budget: 4h
stale: 15

## Instructions

Reduce allocations and avoid unnecessary work in hot paths.
Try buffer reuse, fast-path patterns, and byte-level operations.
Don't change the public API.
```

2. Run it:

```bash
# Inside Claude Code
/autoimprove

# Headless (overnight)
claude -p "run /autoimprove on improve.md" --allowedTools bash,read,write,edit
```

## The `improve.md` format

A single markdown file — part config, part prompt. You describe what you want in natural language, and the agent handles the rest.

### Change — what to optimize

Describe the scope naturally. The agent resolves it to specific files and confirms before starting:

```markdown
## Change
scope: the template parsing engine
exclude: test/, benchmark/
```

The agent will scan the codebase and propose:

```
Resolved scope "the template parsing engine" to:
  - lib/liquid/parser.rb
  - lib/liquid/lexer.rb
  - lib/liquid/variable.rb

These are the ONLY files that will be modified. Confirm? [y/n]
```

Once confirmed, the boundary is locked. `exclude` prevents the agent from touching files it should never modify — especially evaluation code. Without `exclude: eval/`, an agent could "improve" the score by modifying how it's measured rather than improving the actual code. The agent should never grade its own homework.

You can also use explicit paths or globs:

```markdown
## Change
scope: src/handlers/**/*.go
```

### Check — how to measure

Tests, scoring, and guards are separated. Tests gate correctness, the score measures improvement, guards prevent regressions on secondary metrics:

```markdown
## Check
test: go test ./...                    # must pass — hard gate
test-files: test/                      # immutable during loop
run: go test -bench=. -benchmem       # produces the score
score: ns/op:\s+([\d.]+)              # how to extract the number
goal: lower                            # or higher
guard: allocs/op: ([\d.]+) < 500       # secondary metric that must not regress
keep_if_equal: true                    # keep bug fixes and simplifications
timeout: 3m
```

Score extraction supports three formats:
- Convention: `SCORE: 42.5` in stdout
- Regex: `ns/op:\s+([\d.]+)` with a capture group
- jq: `.results.mean_time` for JSON output

**Guard metrics** protect against improving one metric by tanking another. If the guard threshold is violated, the experiment is discarded regardless of the primary score.

**keep_if_equal** (default: false) keeps changes that don't regress, even if they don't improve the score. Useful for bug fixes, code simplifications, and UX improvements that don't affect the measured metric.

### Stop — when to quit

```markdown
## Stop
budget: 4h       # wall-clock time (starts at first experiment, not during setup)
rounds: 100      # max experiments
target: 500      # stop when score reaches this
stale: 15        # stop after 15 consecutive failures
```

Whichever condition hits first. Budget time counts from the first experiment, not from bootstrap or eval setup.

### Agent — for headless mode

```markdown
## Agent
provider: claude
model: sonnet
```

### Instructions — domain guidance

Everything after `## Instructions` is free-form. Tell the agent what to try, what to avoid, and any domain knowledge that helps.

## Auto-guided setup

You don't need to run setup commands manually. `/autoimprove` detects what's missing and walks you through each step:

1. **No improve.md?** Detects repo type and scaffolds one. Supports 10 domain templates: perf, ml, automl, docker, k8s, prompt, sql, frontend, ci, rag.

2. **No eval harness?** For domains with objective metrics (bytes, seconds), helps write the check command. For domains needing human judgment (RAG, prompt, automl), runs eval-init: scaffolds an eval script, runs the system with sample inputs, asks you to label results, builds a golden set.

3. **No tests?** Runs goal-aware bootstrap. The optimization goal predicts what the agent will break:
   - Speed: tests for unicode, nil, concurrency, error handling
   - Size: tests for features, runtime deps, health checks
   - Accuracy: tests for data leakage, reproducibility, valid outputs
   - RAG: tests for format consistency, hallucination, empty results

4. **Baseline established.** Error rate checked. If >20%, blocks until fixed.

5. **Loop starts.**

Tests are mutable during setup, **immutable during the loop**. Two phases, never mixed.

You can still run individual setup steps standalone if you prefer:

```bash
/autoimprove init --type rag      # scaffold improve.md
/autoimprove eval-init            # scaffold eval + golden set
/autoimprove bootstrap --generate # generate tests
```

## Agent-agnostic

The skill works inside Claude Code, but the format works with any agent. Export a standalone protocol:

```bash
/autoimprove --export    # generates program.md
```

Then point any agent at it:

```bash
codex -p "follow program.md"
gemini -p "follow program.md"
aider --message "follow program.md"
```

## Experiment log

Every experiment is logged to `.autoimprove/experiments/` as structured JSON:

```
.autoimprove/
  baseline.json
  experiments/
    001-reduce-allocations.json
    002-cache-integer-tostring.json
```

Each experiment records: what was tried, why, what changed, the score, whether it was kept or discarded, and which earlier experiments it supersedes (so the agent doesn't retry obsolete approaches).

```bash
# View results outside Claude Code
ls .autoimprove/experiments/*.json | xargs jq '{id, title, status, score, delta_pct}'
```

## How is this different from AutoML?

AutoML searches a predefined parameter grid. Autoimprove lets an AI agent make creative, open-ended changes — rewrite algorithms, delete code, try novel approaches. The search space is unbounded.

| | AutoML | Autoimprove |
|---|---|---|
| Search space | Predefined grid | Open-ended |
| Changes | Numeric knobs | Creative — rewrite code, try new algorithms |
| Strategy | Bayesian optimization | AI reasoning about what might work |
| Ceiling | Best from your grid | Unbounded discovery |

## License

MIT
