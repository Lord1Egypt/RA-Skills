# SKILL: command-execution

## Purpose
Execute terminal commands safely with deterministic preflight checks, risk classification, and auditable outputs.

## When to Use
- Running tests, builds, linters, or migrations.
- Inspecting the repo (search, list files, check versions).
- Any command execution that could affect the environment.

## Inputs
- `command` (required, string): exact command to run.
- `purpose` (required, string): why this command is needed.
- `expected_effects` (optional, string[]): what should happen (files created, tests run).
- `risk_level` (optional, enum: `low|medium|high`): if known.

## Steps
1. Classify command risk:
   - read-only (safe)
   - write (moderate)
   - destructive/network/system (high)
2. Block/require confirmation for high-risk patterns:
   - recursive deletes (`rm -rf`, `Remove-Item -Recurse -Force`)
   - format/disk ops
   - piping remote scripts (`curl ... | sh`)
3. If supported, prefer dry-run flags first (e.g., `--dry-run`, `-n`, `--check`).
4. Execute the command and capture:
   - exit code
   - stdout/stderr
   - elapsed time (if available)
5. Interpret results against `expected_effects`.
6. If command failed:
   - stop
   - summarize error
   - propose next diagnostic steps

## Validation
- Exit code is checked (not ignored).
- Output is summarized with the relevant error lines.
- Side effects match expectation (no surprise modifications).

## Output
```yaml
command: "<command>"
purpose: "<purpose>"
result: "success|blocked|failed"
exit_code: <int|null>
highlights: ["<key output lines>"]
next_steps: ["..."]
```

## Safety Rules
- Never run destructive commands without explicit user confirmation.
- Never run unknown installers or remote scripts without review.
- Prefer minimal, scoped commands (avoid global state changes).

## Example
Run tests:
- `command`: `pnpm test`
- `purpose`: “Validate behavior after refactor”
- Output: exit code + failing test names + next diagnostic step.

