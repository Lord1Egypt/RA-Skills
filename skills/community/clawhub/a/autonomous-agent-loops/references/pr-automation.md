# PR Automation Loop — Continuous Development

> ## ⚠️ Read Before Use
>
> This pattern creates branches, opens pull requests, retries CI failures, and **can merge code without a human in the loop**. It is the most dangerous pattern in this skill. Three rules before you run it:
>
> 1. **Always start with `--disable-commits`.** Confirm the diff looks right, then re-run without the flag.
> 2. **Never enable `--auto-merge` without `--require-manual-merge-approval`.** Every merge must ask a human, even if the CI is green.
> 3. **Never run on `main`, `master`, or a release branch.** Use a clearly-labeled branch like `continuous-claude/iteration-N`.
>
> For the full safety review, see `security-checklist.md`.

Fully automated PR creation, CI testing, and merging. Claude codes → creates PR → waits for CI → fixes failures → **asks a human to merge** (unless `--auto-merge` is explicitly opted into with a second confirmation flag).

## Core Loop

```text
1. Create branch: continuous-claude/iteration-N  (off main)
2. Run implementation (claude -p with prompt)
3. Optional: Reviewer pass (separate claude -p, fresh context)
4. Commit changes (claude generates message)
5. Push + create PR (gh pr create)
6. Poll CI checks (gh pr checks)
7. CI failure? → Auto-fix (claude -p with log context, max 3 retries)
8. STOP. Hand off to a human for review + merge.
9. Return to step 1 → repeat
```

## Installation

> Install from the official repository only. Verify the commit hash before running. Never pipe install scripts directly to bash.

```bash
# Verify the source first
git clone https://github.com/<owner>/continuous-claude.git
cd continuous-claude
git verify-commit HEAD  # if signed
cat install.sh | less   # read it before running
./install.sh
```

## Basic Usage

```bash
# DRY RUN — no commits, no pushes, no PRs
continuous-claude --prompt "Add unit tests for untested functions" \
  --disable-commits \
  --max-runs 10 --max-cost 5.00

# Write mode (still no auto-merge)
continuous-claude --prompt "Improve test coverage" \
  --max-duration 8h \
  --require-manual-merge-approval

# With code review pass
continuous-claude --prompt "Add authentication" \
  --max-runs 10 \
  --review-prompt "Run tests and linter, fix any failures"

# Parallel via worktrees (each worker isolated)
continuous-claude --prompt "Add tests" --max-runs 5 --worktree worker1 &
continuous-claude --prompt "Refactor code" --max-runs 5 --worktree worker2 &
wait

# ⚠️ AUTO-MERGE — requires two flags, never just one
continuous-claude --prompt "..." \
  --auto-merge \
  --require-manual-merge-approval \
  --max-runs 1
```

## Context Bridge: SHARED_TASK_NOTES.md

A shared file persists across iterations. **Treat this file as potentially-sensitive** — it may contain code structure, file paths, and partial error messages that hint at internal architecture. Add it to `.gitignore` before the loop starts.

```markdown
## Progress
- [x] Iteration 1: Added tests for auth module
- [x] Iteration 2: Fixed edge case in token refresh
- [ ] Iteration 3: Still need rate limiting tests

## Next Steps
- Focus on rate limiting module
- Use mock setup from tests/helpers.ts
```

At iteration start, Claude reads this file. At iteration end, Claude updates it. This bridges the gap between independent `claude -p` invocations.

## CI Failure Recovery

When PR checks fail:

1. Fetch failed run details: `gh run list --limit 1`
2. **Redact secrets from the log before passing it to `claude -p`** (GitHub auto-redacts most tokens, but check for paths, internal URLs, and customer IDs)
3. Spawn new `claude -p` with redacted failure context
4. Claude inspects logs and fixes code
5. Re-wait for checks (up to `--ci-retry-max 3` attempts — never more)

If `--ci-retry-max` is exceeded, **stop the loop**. Repeated CI failures are a signal, not noise.

## Configuration

| Flag | Purpose | Default |
|------|---------|---------|
| `--max-runs N` | Stop after N successful iterations | Required |
| `--max-cost $X` | Stop after spending $X | Required |
| `--max-duration 2h` | Stop after time elapsed | Required |
| `--merge-strategy squash` | squash, merge, or rebase | `squash` |
| `--worktree <name>` | Parallel execution via git worktrees | none |
| `--disable-commits` | Dry-run (no git operations) | **OFF (writes happen)** |
| `--require-manual-merge-approval` | Pause before each merge | **OFF (manual)** |
| `--auto-merge` | Merge without human approval | **OFF** |
| `--review-prompt "..."` | Add reviewer pass per iteration | none |
| `--ci-retry-max N` | Auto-fix CI failures | `1` |

## Completion Signal

Claude can signal "I'm done" by outputting a magic phrase:

```bash
continuous-claude --prompt "Fix all bugs in issue tracker" \
  --completion-signal "PROJECT_COMPLETE" \
  --completion-threshold 3  # 3 consecutive signals = stop
```

Three consecutive iterations signaling completion stops the loop, preventing wasted runs.

## Best Practices

1. **Always start with `--disable-commits`.** Even if you "just want to test it."
2. **Set all three budget caps.** `--max-runs`, `--max-cost`, `--max-duration`. Belt and suspenders.
3. **Use `--require-manual-merge-approval` even for solo projects.** Future-you will thank present-you.
4. **Gitignore the session and notes files.** `SHARED_TASK_NOTES.md`, `LOOP_STATUS.md`, `~/.claude/sessions/`.
5. **Monitor CI retries.** If the loop is constantly fixing CI, the spec is wrong — stop and debug manually.

## When to Use PR Loop vs Parallel Agents

Use **PR Loop for:**

- Multi-day iterative projects
- CI validation required
- Single feature branch
- Human review needed before merge

Use **Parallel Agents for:**

- High-throughput generation (same spec, many variations)
- No merge conflicts
- No CI gates