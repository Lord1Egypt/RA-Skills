# Repo Execution

## Fast Preflight

Before any write-capable Codex run, confirm:

```bash
pwd
git status --short
rg --files | head -50
```

The goal is to lock the repo root, current dirtiness, and broad codebase shape before Codex starts editing.

## Interactive Repo Work

Use interactive Codex when you need exploration, back-and-forth steering, or mid-run intervention:

```bash
codex -C /path/to/repo
```

Prefer this for unfamiliar repos, ambiguous tasks, or tasks likely to change scope after inspection.

## Bounded Non-Interactive Work

Use `codex exec` when the task and the safety posture are already clear:

```bash
codex exec -C /path/to/repo \
  -s workspace-write \
  -a on-request \
  "Inspect the failing test, patch minimally, run the targeted test, and summarize the outcome."
```

Useful flags:
- `--ephemeral` for runs that should not leave session state on disk
- `--json` for machine-readable event output
- `--output-schema schema.json` when the final answer must match a contract
- `--skip-git-repo-check` only for deliberate non-repo work

## Review Mode

Use review mode when findings matter more than code edits:

```bash
codex review -C /path/to/repo
```

Or in bounded exec form:

```bash
codex exec review -C /path/to/repo
```

Treat review output as severity-ranked findings, not as generic prose.

## Resume and Fork

When prior work exists, prefer continuity over re-prompting:

```bash
codex resume --last
codex fork --last
```

- `resume` when the same thread should continue
- `fork` when you want a variation without polluting the original path
