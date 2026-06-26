# Autoimprove Protocol

This is a self-contained protocol for autonomous optimization. Any AI agent can follow it.

## How to Use This File

You are an autonomous optimization agent. Your job is to improve a measurable score by modifying specific files, testing the result, and keeping only changes that improve the score. You never ask for human input. You run until a stopping condition is met.

## Setup

1. Read `improve.md` in the current directory
2. Parse the structured headers to extract:
   - `Change.scope` — description, paths, or globs of what you may modify
   - `Change.exclude` — paths you must never touch
   - `Check.test` — command to verify correctness (must pass for any change to be kept)
   - `Check.test-files` — test file paths (never modify these during the loop)
   - `Check.run` — the command to produce the score
   - `Check.score` — how to extract the score from output
   - `Check.goal` — whether lower or higher is better
   - `Check.guard` — optional secondary metric with threshold that must not be violated
   - `Check.keep_if_equal` — whether to keep changes that match (not improve) the score
   - `Check.timeout` — max time per experiment
   - `Stop.*` — when to stop the loop
3. Resolve `Change.scope` to explicit file paths. If it's natural language, scan the codebase and list the files you will modify. Apply `Change.exclude` to filter.
4. Create `.autoimprove/` directory and `.autoimprove/experiments/` subdirectory
5. If `Check.test` is specified, run it to confirm tests pass before starting
6. Run the score command on the unmodified codebase to establish a baseline
7. Check baseline for errors. If error rate > 20%, stop and report — the eval is unreliable.
8. Save the baseline score and current git commit SHA to `.autoimprove/baseline.json`
9. Budget timer starts NOW (not during setup)

## Loop

Repeat until a stopping condition is met:

1. **Plan**: Read past experiments from `.autoimprove/experiments/`. Skip experiments that appear in a later kept experiment's `supersedes` list. Review what worked, what failed, and why. Propose a new change that you have not tried before.

2. **Implement**: Modify ONLY the files resolved from `Change.scope`. Make a focused, minimal change.

3. **Commit**: `git add <changed files> && git commit -m "autoimprove: <short description>"`. Verify HEAD changed by comparing `git rev-parse HEAD` before and after. If HEAD didn't change, the commit failed — stop and report.

4. **Test**: If `Check.test` is specified, run it. If tests fail: `git reset --hard HEAD~1`, log as "test_failed", continue to next iteration.

5. **Evaluate**: Run the score command (`Check.run`). If it times out, kill it and treat as failure.

6. **Score**: Extract the score from stdout using the extraction method in `Check.score`.

7. **Guard**: If `Check.guard` is specified, extract the guard metric and check the threshold. If violated: `git reset --hard HEAD~1`, log as "guard_failed", continue.

8. **Decide**:
   - If the score command failed (non-zero exit or timeout): `git reset --hard HEAD~1`, log as "error"
   - If the score improved: keep the commit, update the baseline, log as "kept"
   - If the score is equal AND `keep_if_equal` is true: keep the commit, log as "kept_equal"
   - If the score did not improve: `git reset --hard HEAD~1`, log as "discarded"

9. **Log**: Save experiment JSON to `.autoimprove/experiments/NNN-slug.json` with this schema:
   ```json
   {
     "id": <number>,
     "title": "<short description>",
     "status": "kept | kept_equal | discarded | test_failed | guard_failed | error",
     "commit": "<sha if kept, null if discarded>",
     "score": <number or null if error/test_failed>,
     "baseline_score": <number>,
     "delta_pct": <number or null>,
     "duration_s": <number>,
     "reasoning": "<why you tried this>",
     "files_changed": ["<paths>"],
     "supersedes": [<list of experiment IDs this replaces, or empty>],
     "timestamp": "<ISO 8601>"
   }
   ```

10. **Check stopping conditions**:
    - `budget`: wall-clock time since first experiment > budget → stop
    - `rounds`: experiment count >= rounds → stop
    - `target`: score reached target value → stop
    - `stale`: consecutive non-improving experiments >= stale → stop

## Rules

- NEVER modify files outside the resolved `Change.scope`
- NEVER modify test files (`Check.test-files`) during the loop
- NEVER modify the check command, eval script, golden set, or scoring
- NEVER skip the git commit before evaluating
- NEVER proceed without verifying HEAD changed after commit
- ALWAYS log every experiment including failures
- ALWAYS read past experiments before proposing changes
- ALWAYS skip superseded experiments when reading the log
- ALWAYS leave the git tree clean after discarding
- Test failure means immediate discard — no exceptions
- Guard failure means immediate discard — secondary metrics must not regress
- Complexity must justify itself — a marginal improvement with ugly code is not worth keeping
- Deleting code for equal results IS worth keeping
- When stuck after several failures, try a fundamentally different approach instead of variations on the same idea

## Domain Instructions

Read the `## Instructions` section of `improve.md` for domain-specific guidance on what to try and what to avoid.
