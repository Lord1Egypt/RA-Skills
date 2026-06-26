# PR Automation Loop — Continuous Development

Fully automated PR creation, CI testing, and merging. Claude codes → creates PR → waits for CI → fixes failures → merges.

## Core Loop

```text
1. Create branch: continuous-claude/iteration-N
2. Run implementation (claude -p with prompt)
3. Optional: Reviewer pass (separate claude -p)
4. Commit changes (claude generates message)
5. Push + create PR (gh pr create)
6. Poll CI checks (gh pr checks)
7. CI failure? → Auto-fix (claude -p with log context)
8. Merge PR (squash/merge/rebase)
9. Return to main → repeat
```

## Installation

> Install from official repository after code review. Do not pipe scripts directly to bash.

## Basic Usage

```bash
# 10 iterations, max $5 spend
continuous-claude --prompt "Add unit tests for untested functions" \
  --max-runs 10 --max-cost 5.00

# Time-boxed
continuous-claude --prompt "Improve test coverage" --max-duration 8h

# With code review pass
continuous-claude --prompt "Add authentication" \
  --max-runs 10 \
  --review-prompt "Run tests and linter, fix any failures"

# Parallel via worktrees
continuous-claude --prompt "Add tests" --max-runs 5 --worktree worker1 &
continuous-claude --prompt "Refactor code" --max-runs 5 --worktree worker2 &
wait
```

## Context Bridge: SHARED_TASK_NOTES.md

Critical innovation: a shared file that persists across iterations.

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
2. Spawn new `claude -p` with failure context
3. Claude inspects logs and fixes code
4. Re-wait for checks (up to `--ci-retry-max` attempts)

## Configuration

| Flag | Purpose |
|------|---------|
| `--max-runs N` | Stop after N successful iterations |
| `--max-cost $X` | Stop after spending $X |
| `--max-duration 2h` | Stop after time elapsed |
| `--merge-strategy squash` | squash, merge, or rebase |
| `--worktree <name>` | Parallel execution via git worktrees |
| `--disable-commits` | Dry-run (no git operations) |
| `--review-prompt "..."` | Add reviewer pass per iteration |
| `--ci-retry-max N` | Auto-fix CI failures (default: 1) |

## Completion Signal

Claude can signal "I'm done" by outputting a magic phrase:

```bash
continuous-claude --prompt "Fix all bugs in issue tracker" \
  --completion-signal "PROJECT_COMPLETE" \
  --completion-threshold 3  # 3 consecutive signals = stop
```

Three consecutive iterations signaling completion stops the loop, preventing wasted runs.

## Best Practices

1. **Write clear prompts** — Each iteration should be actionable
2. **Set cost limits** — Prevent runaway spending
3. **Review before merge** — Check final result before auto-merge enables
4. **Use SHARED_TASK_NOTES.md** — Track progress across iterations
5. **Monitor CI retries** — If constantly failing, stop loop and debug manually

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
