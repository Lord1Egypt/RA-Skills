# adversarial-code-review

Multi-perspective adversarial code review with git-isolated worktrees. Two independent reviewers (Architect + Inspector) each produce JSON findings, two cross-review passes pressure-test them, and a synthesis rapporteur collapses everything into a single ranked report.

For Hermes Agent, Claude Code, Codex, or any LLM CLI.

## How it works

```
ARCHITECT ──→ reviews code (architecture, security, concurrency)
INSPECTOR ──→ reviews code (bugs, edge cases, error handling)
CROSS_1 ────→ challenges INSPECTOR findings with ARCHITECT perspective
CROSS_2 ────→ challenges ARCHITECT findings with INSPECTOR perspective
SYNTHESIS ──→ ranks, cross-validates, produces final report
```

## Comparison

| Feature | adversarial-code-review | adverse (addyosmani) | alecnielsen/adversarial-review | agent-review-panel |
|---------|------------------------|---------------------|-------------------------------|-------------------|
| Cross-model debate | ✅ Architect↔Inspector | ❌ Single-reviewer | ❌ Single-round | ✅ 4-6 panel |
| Git worktree isolation | ✅ | ❌ | ❌ | ❌ |
| Cross-review rounds | ✅ 2 rounds of devil's advocate | ❌ | ❌ | ❌ |
| JSON findings with schema | ✅ | ❌ | ❌ | ❌ |
| --project-dir mode | ✅ Review existing codebase | ❌ | ❌ | ❌ |

## Quick start

```bash
# Review changes on a branch
python3 scripts/adversarial_review.py --diff-git

# Review a whole project directory
python3 scripts/adversarial_review.py --project-dir /path/to/project \
  --a-cmd "claude-tmux --model best" \
  --b-cmd "codex exec -C /path/to/project"
```

## Output

Artifacts land in `--out` (default `.adversarial-review`):

- `final.json` — machine-readable verdict (`APPROVE|REQUEST_CHANGES|REJECT`)
- `review.md` — ranked report with per-finding evidence
- `01_architect.txt` … `05_synthesis.txt` — per-phase raw output

## Dependencies

- Python ≥ 3.11
- Git ≥ 2.5
- Two LLM CLIs (one for architect, one for inspector)

Uses `adversarial-common` as the shared engine.

## License

0BSD — see [LICENSE](LICENSE).
