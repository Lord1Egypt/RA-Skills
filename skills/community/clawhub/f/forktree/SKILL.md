---
name: forktree
description: Use the forktree Python CLI to safely create, list, remove, and garbage-collect git worktrees from a shell pipeline, CI job, or unattended coding agent. Wraps `git worktree` with safety pre-flights, TOML configuration, and a strict stdout/stderr contract.
homepage: https://github.com/BottaniCals/forktree
metadata: {'openclaw': {'requires': {'bins': ['forktree']}}}
---

# forktree — safe `git worktree` CLI for agents

`forktree` is a stdlib-only Python 3.11+ CLI that wraps `git worktree add/list/remove` with seven safety pre-flights, TOML config resolution, and a strict data-on-stdout / diagnostics-on-stderr contract. No third-party dependencies.

Use `forktree <subcommand> --help` for the per-subcommand flag reference when you need it.

## Verify it's wired

```bash
command -v forktree                              # on PATH
python3 -c "import forktree"                     # package importable
forktree --help                                  # usage renders
forktree doctor                                  # always exits 0; diagnostics on stderr
```

## Subcommands

| Subcommand | What it does                                                     |
| ---------- | ---------------------------------------------------------------- |
| `create`   | Create a new worktree after seven safety pre-flights.            |
| `list`     | List existing worktrees for a project (`--porcelain`, `--json`). |
| `remove`   | Remove a worktree (optional `--force-if-lossless`).              |
| `gc`       | Garbage-collect stale worktrees by age and merge status.         |
| `init`     | Write `.forktree.toml` with the effective resolved config.       |
| `doctor`   | Print diagnostics report (always exits `0`).                     |

## Output contract

- **stdout** = data only.
  - `create` → one line: absolute path of the new worktree.
  - `list --porcelain` → one TSV line per worktree, no header.
  - `list --json` → JSON array of objects; compact in a pipe, pretty in a TTY.
  - `gc --dry-run` → one slug per line (sorted).
  - Everything else: empty on stdout.
- **stderr** = progress under `-v`, warnings, errors, and `doctor` diagnostics.
- Errors are formatted exactly as: `forktree: <subcommand>: <one-line reason>`.

## Exit codes

| Code | Meaning                                             |
| ---- | --------------------------------------------------- |
| `0`  | Success                                             |
| `1`  | Preflight refused the operation                     |
| `2`  | Git op failed, setup hook failed, or usage error    |
| `3`  | Config error under `--strict` / `FORKTREE_STRICT=1` |

## Canonical agent idiom

The whole point of the tool — capture stdout into a variable, route stderr to a file:

```bash
wt=$(forktree create "$project_path" "$slug" 2>/tmp/forktree.err) || {
    cat /tmp/forktree.err
    exit 1
}
cd "$wt"
```

If `forktree create` exits non-zero, the worktree was not created. Don't retry without reading stderr first — the pre-flight refused the operation for a reason.

## Configuration

TOML resolution order: **CLI flags > project `.forktree.toml` > `~/.config/forktree/config.toml` > built-in defaults**. Missing files fall back silently. Malformed TOML under `--strict` exits `3`. Full config schema in the README.

Environment variables:

- `FORKTREE_STRICT=1` — equivalent to `--strict` on every subcommand.
- `NO_COLOR=1` — disable ANSI color in human output.

## Gotchas

- **Stdout is data, stderr is diagnostics.** `... | jq` is pipe-clean — but parse errors land on stderr, so for control flow check the exit code and read stderr on failure rather than relying on stdout content.
- **`forktree create` exit ≠ zero means no worktree.** Don't `cd "$wt"` without checking the exit; the variable is empty when the pre-flight refused.
- **`gc` is the cleanup path, not `remove`.** `gc` evaluates idle_days + merge status; `remove` deletes one worktree by path. Use `gc --dry-run` first when uncertain.
- **Setup hook (`[worktree].setup_script`) is opt-in and removes the worktree on non-zero exit.** Check the README before enabling — silent teardown on hook failure is by design.
