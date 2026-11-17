# ai-code-verification-guard

Deterministic verification guard for AI coding agents: **the script decides, the agent quotes.**

AI coding assistants tend to report "done" without actually verifying. This skill replaces prompt-based self-discipline with a deterministic script (`scripts/verify.mjs`) whose exit code is the only arbiter. The agent may only quote the `VERIFY VERDICT` block — it has no authority to overrule the result.

## Why

Prompt-only verification rules fail silently: the model skips checks and still reports success. A script with a fixed exit-code contract cannot be negotiated with.

- `snapshot` records a behavioral baseline before changes
- `run` executes every check after changes, diffs against the baseline, and flags any pass-to-fail flip as `REGRESSION`
- Four-state verdict: `PASS` / `FAIL` / `REGRESSION` / `UNVERIFIED`, exit codes `0` / `1` / `1` / `2`

## What it checks

| Project type | Checks |
|---|---|
| Node.js (`package.json`) | Lint / format / typecheck / composite check gates / tests — classified by command content, never by naming alone |
| Go | `go build`, `go vet`, `go test` |
| Rust | `cargo check`, `cargo test` |
| Python | `compileall`, `pytest` |
| Bare JS | `node --check` + `node --test` |

Safety by design:

- Never executes modifying or resident commands (`--fix`, `--write`, `--watch`)
- Bare `vitest` (watch-mode trap) is deterministically rewritten to an equivalent `vitest.mjs run` invocation
- Monorepo aware (workspaces / pnpm-workspace / lerna): root-level checks only, scope declared explicitly
- Windows CRLF note for format checks on `core.autocrlf=true` checkouts
- Missing tools → honest `UNVERIFIED`, never a fake pass

## Install

```bash
openclaw skills install ai-code-verification-guard
```

or via ClawHub CLI:

```bash
clawhub install ai-code-verification-guard
```

## Usage

The agent drives it automatically when activated. Manual usage:

```bash
node <skill-path>/scripts/verify.mjs snapshot   # before changes
node <skill-path>/scripts/verify.mjs run        # after changes
```

Requirements: Node.js in PATH. Ecosystem checkers (eslint, tsc, go, cargo, pytest...) are probed from the project itself and reported as UNVERIFIED when missing.

Zero dependencies. Baselines live in `<project>/.verification/` (add it to `.gitignore`).

## Validated against

Real-world battle-tested across 6 projects: a bare JS package, a TypeScript package, `commander.js` (npm), and `vuejs/core` (pnpm monorepo with vitest watch trap, e2e-browser project, `-only` scripts, and CRLF checkout pitfalls).

## License

MIT
