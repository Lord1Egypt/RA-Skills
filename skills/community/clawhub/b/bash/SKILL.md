---
name: Bash
slug: bash
version: 1.0.6
description: >-
  Writes, debugs, and hardens Bash shell scripts — quoting, arrays, strict mode,
  traps, argument parsing, and macOS/Linux portability. Use when writing or
  reviewing any script, one-liner, cron job, deploy script, container entrypoint,
  or CI step; when a script breaks on spaces in filenames, exits silently,
  ignores set -e, hangs, or returns the wrong exit code; when quoting, IFS,
  globs, arrays, heredocs, process substitution, trap, getopts, or mapfile
  misbehave; when shellcheck flags SC2086 and friends; when unbound variable,
  bad substitution, command not found, ambiguous redirect, or unexpected end of
  file show up; when a script works by hand but fails under cron, systemd, sudo,
  or a CI runner; or when porting between macOS bash 3.2, GNU/Linux, WSL, and
  POSIX sh. Not for interactive zsh or fish configuration, not for PowerShell, and
  not for host-level cron, systemd, or permission failures (linux).
homepage: https://clawic.com/skills/bash
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🖥️
    requires:
      bins:
      - bash
    os:
    - linux
    - darwin
    displayName: Bash
    configPaths:
    - ~/Clawic/data/bash/
---

User preferences live in `~/Clawic/data/bash/config.yaml` (see Configuration); nothing else is stored on the user's machine. If you have data at an old location (`~/bash/` or `~/clawic/bash/`), move it to `~/Clawic/data/bash/`.

## When To Use

- Writing or reviewing any Bash beyond a one-liner: CI steps, deploy scripts, cron tasks, entrypoints, glue code
- Debugging scripts that break on spaces in filenames, fail silently, hang, or exit with the wrong code
- Hardening an existing script: strict mode, cleanup traps, argument parsing, re-runnability, portability
- Porting a script between macOS and Linux, or down to POSIX sh
- Deciding whether the task belongs in Bash at all (Core Rule 9)
- Not for POSIX-sh-only targets (dash, busybox, alpine `/bin/sh`) — most patterns here are bashisms; `portability.md` covers the downgrade

## Quick Reference

| Situation | Play |
|-----------|------|
| Breaks on spaces or hostile filenames | Quote every expansion, iterate with `find -print0` + `while IFS= read -r -d ''` → `quoting.md` |
| `set -e` missed a failure, cleanup never ran | The five blind spots (conditions, `\|\|`/`&&`, `$( )`, `! cmd`, `exit` in a subshell) → `errors.md` |
| Pipeline "fails" but each command worked | Exit code 141 = SIGPIPE from an early-exit consumer; `PIPESTATUS` names the segment → `errors.md` |
| Wrong output and you cannot see why | `PS4='+ ${BASH_SOURCE##*/}:${LINENO}: ' bash -x script` → `debugging.md` |
| Command built from variables misfires | Build it as an array (`cmd=(rsync -a); cmd+=(--dry-run); "${cmd[@]}"`), never as a string → `quoting.md` |
| Comparison wrong: `[` vs `[[`, numeric vs lexical | `[[ 10 < 9 ]]` is TRUE (lexical); numbers belong in `(( ))` or `-lt` → `conditionals.md` |
| Runs fine by hand, fails from cron | Cron has no login shell: minimal PATH, no profile, `$HOME` as cwd, `%` means newline → `cron.md` |
| Works locally, fails in the CI runner | Each step is a fresh non-interactive shell; strict mode does not carry over → `ci.md` |
| Script takes minutes on a large file | Count forks: one external command per line is the cost — batch into awk/sort → `performance.md` |
| `unbound variable` / `bad substitution` / `ambiguous redirect` | Symptom→cause chains → `debugging.md` |
| Must run on macOS stock bash or an old server | Version Floors below, then GNU-vs-BSD flags → `portability.md` |
| Flags, `--help`, subcommands, usage exit codes | `getopts` with a silent optstring, then `shift $((OPTIND-1))` → `arguments.md` |
| Redirection order, heredocs, one-instance locking | Redirections apply left to right before the command runs → `redirection.md` |
| Paths, globs, temp files, deletes that must be safe | Resolve once with `cd … && pwd -P`; write temp + `mv` → `files.md` |
| Parsing CSV/JSON/logs, choosing awk vs sed vs jq | Per-line and stateless → one `awk` pass; never grep JSON → `text-processing.md` |
| Background jobs, signals, timeouts, N in parallel | `pid=$!` then `wait "$pid"`; `xargs -P` for fan-out → `processes.md` |
| String surgery: defaults, trim, replace, basename | Builtin expansions, no forks → `expansion.md` |
| Lists, dictionaries, sets, counters | `mapfile -t` to load, `declare -A` for maps → `arrays.md` |
| Splitting into functions or a sourced library | `main "$@"` behind a `BASH_SOURCE` guard; scope is dynamic → `functions.md` |
| Prompts, confirmations, color, progress | Gate every one of them on `[[ -t 1 ]]` → `interactive.md` |
| Calling an API, webhook, or health check | curl exits 0 on a 500 — capture `%{http_code}` and branch → `http.md` |
| Untrusted input, secrets, temp-file races, sudo | Keep values as data, never as syntax → `security.md` |
| Adding tests, stubbing commands, lint in CI | `bash -n`, shellcheck, then bats with PATH stubs → `testing.md` |
| Anything else | Core Rules below, then reproduce with `bash -x` on the smallest input that still fails |

Each file above is one sub-job and is self-contained: read SKILL.md by default, open exactly one guide when the situation matches.

## Core Rules

1. Open every script with `#!/usr/bin/env bash` and `set -euo pipefail`, then learn the `-e` holes (`errors.md`) instead of dropping strict mode — the holes are enumerable; silent failures are not.
2. Quote every expansion: `"$var"`, `"$(cmd)"`, `"${arr[@]}"`. An unquoted expansion is a deliberate act that carries a comment saying why. Word splitting plus globbing is Bash's #1 bug class (shellcheck SC2086).
3. Build commands as arrays, never as strings. `opts="--exclude '*.log'"; rsync $opts src dst` passes the quotes as literal characters; `opts=(--exclude '*.log'); rsync "${opts[@]}" src dst` passes `--exclude` and `*.log` as two clean arguments. Conditional flags append: `[[ $dry == 1 ]] && opts+=(--dry-run)`.
4. Run shellcheck before shipping, blocking at `lint_gate` severity. Suppress only with the code and a reason on the same line: `# shellcheck disable=SC2086 -- flags must split`.
5. Know your floor: macOS `/bin/bash` is 3.2 forever (GPLv3 freeze). If the script uses any `bash >=4.0` feature (Version Floors), state the floor in a header comment and enforce it: `((BASH_VERSINFO[0] >= 4)) || { echo "needs bash 4+" >&2; exit 1; }`.
6. Never parse `ls`. Iterate with globs or `find -print0`: filenames may contain newlines, so NUL is the only delimiter a filename cannot contain.
7. Test the failure path before delivering: swap one command for `false`, confirm the script stops, the trap fires, and the exit code is nonzero. A cleanup you never saw run is a cleanup you do not have.
8. Untrusted input never reaches `eval`, arithmetic, or array subscripts: `(( $userinput ))` executes commands via `arr[$(cmd)]` subscripts. Gate with a regex first: `[[ $n =~ ^[0-9]+$ ]] || die "not a number: $n"`.
9. Past `rewrite_threshold` lines (default 100, the Google Shell Style Guide cutoff) or once you need nested data structures, rewrite in Python or similar. Bash orchestrates processes; it does not model data.

## Script Skeleton

```bash
#!/usr/bin/env bash
# Requires bash >= 4.4 (inherit_errexit). Run: script.sh [-n] <target>
set -euo pipefail
shopt -s inherit_errexit 2>/dev/null || true   # bash >=4.4: $(cmd) failures propagate

die() { printf '%s\n' "$*" >&2; exit 1; }

tmp=$(mktemp) || die "mktemp failed"
trap 'rm -f "$tmp"' EXIT   # single-quoted: expands when it FIRES, not now
                           # fires on error and normal exit; kill -9 bypasses all traps
```

## Quoting

- `"$var"`, `"$(cmd)"`, `"${arr[@]}"` — always. `$(cmd)` strips ALL trailing newlines, not just one.
- Single quotes are literal; `$'...'` interprets escapes: `$'\t'`, `$'\r'`, `$'\0'`.
- Filenames from variables get `--` or `./`: `rm -- "$f"` survives a file named `-rf`.
- `echo "$var"` breaks when var is `-n`, `-e`, or has backslashes — `printf '%s\n' "$var"` never does.
- Arguments to `ssh`/`su -c`/`bash -c` are re-parsed by the receiving shell — build them with `printf '%q '` (`quoting.md`).
- `${arr[*]}` joins with the first char of IFS into one word; `"${arr[@]}"` preserves elements. Joining is the only reason to write `[*]`.

## Version Floors

| Feature | Needs |
|---------|-------|
| `printf -v var`, `+=` append | bash >=3.1 |
| `declare -A`, `mapfile`, `${var^^}`/`${var,,}`, `globstar`, `;&` fallthrough, `\|&` | bash >=4.0 |
| `[[ -v var ]]`, `shopt -s lastpipe`, `declare -g` | bash >=4.2 |
| `${arr[-1]}`, `declare -n` namerefs, `wait -n` | bash >=4.3 |
| `inherit_errexit`, `${var@Q}`, `mapfile -d`, empty `"${arr[@]}"` safe under `set -u` | bash >=4.4 |
| `EPOCHSECONDS`/`EPOCHREALTIME`, `SRANDOM` (5.1) | bash >=5.0 |

macOS `/bin/bash` stays at 3.2. `#!/usr/bin/env bash` finds a Homebrew bash on PATH; `#!/bin/bash` never will. Check at runtime with `BASH_VERSINFO`, not by parsing `bash --version`.

## Exit Codes

Formula: a code above 128 means killed by signal `code − 128`. Codes are mod 256 — `exit 256` reports 0, `exit -1` reports 255.

| Code | Meaning | First move |
|------|---------|-----------|
| 1 | Generic failure — also `(( expr ))` evaluating to 0 | Read the last command, then the `((` traps below |
| 2 | Shell syntax or builtin usage error | `bash -n script` locates it; conventionally also "wrong CLI usage" (`arguments.md`) |
| 126 | Found but not executable | `chmod +x`, or the shebang interpreter is not executable |
| 127 | Command not found | PATH (the cron classic), typo, or a missing shebang interpreter ("bad interpreter") |
| 130 | SIGINT (128+2) | User pressed Ctrl-C — propagate it, do not swallow it |
| 137 | SIGKILL (128+9) | OOM killer or `kill -9`; no trap ever ran, so cleanup did not happen |
| 141 | SIGPIPE (128+13) | A consumer (`head`, `grep -q`) closed the pipe early — usually success misread as failure |
| 143 | SIGTERM (128+15) | Orderly external stop (systemd, CI timeout) — trap it to clean up |
| 124 | GNU `timeout` expired (125 = timeout itself failed) | Raise the timeout or fix the hang (`processes.md`) |
| 255 | `ssh` transport error, and any `exit` with a negative or >255 value wrapped | Distinguish ssh's own failure from the remote command's |

## Subshells and State

- Every pipe segment runs in a subshell: `cmd | while read -r x; do ((n++)); done` loses `n`. Fix: `done < <(cmd)`, or `shopt -s lastpipe` (bash >=4.2, scripts only).
- `( )` is a subshell, `{ ...; }` is the current shell — `exit` inside `( )` or `$( )` exits only that subshell.
- Background jobs: `cmd & pid=$!` then `wait "$pid"` — `wait` returns the job's exit code, your only way to check it.
- `cd` inside `( )` to visit a directory without having to `cd` back.

## Robust Iteration

- Globs: `shopt -s nullglob` first — otherwise `for f in *.txt` in an empty dir runs once with the literal string `*.txt`.
- Hostile filenames or recursion: `while IFS= read -r -d '' f; do ...; done < <(find . -name '*.log' -print0)`.
- Lines of a file: `while IFS= read -r line; do ...; done < file` — `IFS=` keeps leading whitespace, `-r` keeps backslashes. A final line without a trailing newline is still skipped: append `|| [[ -n $line ]]` to the read.
- Any command inside the loop that reads stdin (`ssh`, `ffmpeg`, `mysql`) eats the rest of the input and the loop ends after one pass — pass `ssh -n` or redirect `< /dev/null`.
- Split a string: `IFS=, read -ra fields <<< "$csv"`. Join: `(IFS=,; echo "${arr[*]}")` — the subshell keeps the IFS change local.

## Output Gates

Before delivering any script, check:

- Every expansion quoted, or the unquoted one carries a comment saying why
- Commands with variable flags built as arrays, not concatenated strings
- shellcheck clean at `lint_gate`, or each disable names its SC code and reason
- Failure path exercised: injected `false`, watched the trap fire and the exit code go nonzero
- Bash floor stated in a header comment and matching `bash_floor` if any `bash >=4.0` feature is used
- No `eval`; no unvalidated input inside `(( ))` or array subscripts
- Re-runnable: a run that dies halfway leaves nothing half-written — temp file plus `mv`, `mkdir -p`, `rm -f`
- Destructive steps gated per `destructive_confirm`; no secret can appear in `set -x` output or `ps`

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/bash/config.yaml`. Never interview the user — record a preference the moment it is stated.

| Variable | Type | Default | Effect |
|---|---|---|---|
| bash_floor | 3.2 \| 4.4 \| 5.x | 4.4 | Gates which Version Floors features may be used unguarded; `3.2` bans `mapfile`, `declare -A`, namerefs and emits the portable fallbacks instead |
| target_os | linux \| macos \| both | both | Picks GNU or BSD flag forms in every emitted command (`sed -i`, `date`, `stat`, `readlink`); `both` restricts to the intersection (`portability.md`) |
| strict_mode | set-euo \| explicit-checks | set-euo | Chooses the Script Skeleton and which school reviews enforce (Where Experts Disagree) |
| lint_gate | error \| warning \| style \| none | warning | Severity at or above which shellcheck findings block delivery (`shellcheck -S <value>`); Output Gates use it |
| rewrite_threshold | number (lines) | 100 | Length at which Core Rule 9 recommends another language |
| indent_style | 2-spaces \| 4-spaces \| tabs | 2-spaces | Formatting of emitted scripts and the `shfmt -i` value |
| destructive_confirm | bool | true | Emitted scripts guard deletes, overwrites, and remote pushes behind `--yes` or a dry-run pass |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling**: shellcheck/shfmt/bats availability, GNU coreutils on macOS (`gsed`, `gdate`), jq vs python for JSON — affects `testing.md` gates and every parsing example
- **Conventions**: function and variable naming, usage/help layout, log line format, script header content — affects `functions.md` and `arguments.md` output
- **Platform**: bash floor and OS mix, POSIX-sh-only targets, alpine images where `/bin/sh` is ash and bash may be absent — affects `portability.md` guidance
- **Safety posture**: whether scripts may `sudo`, dry-run first, banned constructs (`eval`, `curl | sh`, `rm -rf` on a variable) — affects `security.md` and destructive workflows
- **Runtime home**: where the script actually runs unattended — cron, systemd timer, launchd, CI runner, container entrypoint — affects `cron.md` and `ci.md` advice
- **Output**: verbosity, color only when the output is a TTY, timestamps, quiet or machine-readable logging — affects `interactive.md` and logging helpers

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `local out=$(cmd)` | `local` returns 0, masking cmd's failure — `set -e` never fires | `local out; out=$(cmd)` |
| `((count++))` when count is 0 | expression evaluates to 0 → exit status 1 → `set -e` kills the script | `count=$((count+1))` |
| `grep -q` downstream under pipefail | early exit sends SIGPIPE upstream; producer dies with 141 (128+13) and the pipeline "fails" on success | capture first: `out=$(cmd)`, then grep the variable |
| `rm -rf "$dir/"` | empty/unset `dir` → `rm -rf /` | `rm -rf "${dir:?}/"` aborts if empty |
| `trap "rm -rf $tmp" EXIT` (double quotes) | the body expands NOW, when `tmp` may still be empty — you registered `rm -rf` | single quotes: `trap 'rm -rf "$tmp"' EXIT` |
| Checking `$?` after a log line | the `echo` overwrote it | `rc=$?` on the very next line |
| `which cmd` to test existence | external, output format varies (SC2230) | `command -v cmd >/dev/null` |
| `cd "$dir"` without a check | without `-e`, everything after runs in the wrong directory | `cd "$dir" \|\| exit 1` — habit survives scripts that lack `-e` |
| `sudo cmd > /root/out` | the redirection is performed by YOUR shell before sudo runs — permission denied | `cmd \| sudo tee /root/out >/dev/null` |
| `set -euo pipefail` in a sourced library | it mutates the caller's shell and breaks their error handling | set options in executables only; libraries return codes (`functions.md`) |

## Where Experts Disagree

- `set -e`: the strict-mode school makes it mandatory; the Google Shell Style Guide school argues its exceptions (conditions, `||`, command substitution) make it false comfort and prefers explicit `|| die`. Boundary: short glue scripts → strict mode; sourced libraries and functions whose return codes callers inspect → explicit handling. Never mix philosophies in one file.
- Bash vs POSIX sh: write sh only when the target set actually contains dash/busybox/alpine. "Portable by default" costs arrays, `[[ ]]`, and `set -o pipefail` for hosts you may never meet.
- Returning values from functions: print to stdout and capture (composable, costs a fork per call) vs write through a nameref or a documented global (no fork, couples caller and callee). Boundary: hot loops and large payloads → nameref (`bash >=4.3`); everything else → stdout.
- Long options: GNU `getopt(1)` parses them but does not exist usably on macOS (BSD getopt has no long options); a hand-rolled `while`/`case` loop is portable and you own the error messages. Boundary: Linux-only tooling → `getopt`; anything shipped to laptops → hand-rolled (`arguments.md`).

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/bash (install if the user confirms):

- `linux` — when the bug is the system, not the script: permissions, cron daemon config, systemd units, OOM
- `regex` — when the `=~` pattern itself is the hard part
- `github-actions` — when the script lives in CI and the failure is workflow wiring, not shell
- `cli-design` — when the question is the tool's interface: subcommand layout, flag naming, help text contract

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/bash.
