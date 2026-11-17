# Debugging — Symptom to Cause

Bash fails quietly: a typo becomes an empty string, an empty string becomes a different command. Work symptom-first; every step below is a check, not a guess.

## The Universal First Three

1. `bash -n script` — parse without executing. Catches unbalanced quotes, `fi`/`done` mismatches, and CRLF damage in one second.
2. `PS4='+ ${BASH_SOURCE##*/}:${LINENO}:${FUNCNAME[0]:-main}: ' bash -x script` — xtrace prints each command AFTER expansion. The first line that differs from what you meant to write is the bug.
3. `shellcheck script` — half of "mystery" bugs are SC2086 (unquoted expansion) or SC2181 (`$?` checked too late). Fix those before theorizing.

## Reading and Aiming xtrace

- The `+` count is nesting depth: `++` is inside a function or `$( )`, `+++` deeper still.
- Keep the trace out of your program's output: `exec 5>trace.log; BASH_XTRACEFD=5; set -x` (`bash >=4.1`). Do this whenever stdout carries data or a CI runner interleaves the streams.
- Trace one region, not the whole script: `set -x` … `set +x`. Inside a function, `local -` (`bash >=4.4`) restores every option on return, so `local -; set -x` traces just that function.
- `set -v` prints lines BEFORE expansion; running `-x` and `-v` together shows source and result side by side — the fastest way to see which expansion misfired.
- Timing without a profiler: `PS4='+ $EPOCHREALTIME ' ` (`bash >=5.0`) puts a microsecond stamp on every command; the gap between two lines is where the time went.
- Secrets: xtrace prints values. Wrap credential handling in `set +x` … `set -x`, or the trace becomes a leak — CI logs are the usual victim.

## Error Message → Cause

| Message | Cause and fix |
|---|---|
| `unexpected EOF while looking for matching '"'` | Unbalanced quote or unterminated heredoc. The reported line is where the file ENDED, not where the bug is — `bash -n`, then look for the last correctly highlighted line |
| `syntax error near unexpected token 'fi'`/`'}'`/`newline` | Missing `then`, `;`, or `do` — or CRLF line endings; check with `file script` (says "CRLF") |
| `$'\r': command not found` | CRLF, always. `sed -i 's/\r$//' script`, and fix the editor/git config that produced it |
| `bad interpreter: No such file or directory` | CRLF in the shebang line, or the interpreter path does not exist |
| `unbound variable` (with `set -u`) | Typo in the name, or a legitimately absent value — write `${var:-}` where absence is allowed; on `bash <4.4` an EMPTY array also trips it: `${arr[@]+"${arr[@]}"}` |
| `bad substitution` | Bash syntax executed by `sh`/dash (`${var^^}`, `${arr[@]}`, `<<<`), or a `bash >=4.0` expansion on macOS 3.2 |
| `ambiguous redirect` | `> $file` where `file` is empty, unset, or contains a space — quote it: `> "$file"` |
| `[: too many arguments` / `unary operator expected` | Unquoted variable with spaces or empty inside `[ ]` — quote it, or switch to `[[ ]]` |
| `command not found` only under cron/CI/sudo | PATH, not the script. Non-interactive shells read no profile; sudoers `secure_path` replaces PATH outright |
| `argument list too long` | The expanded glob or arg list exceeds `getconf ARG_MAX` — pipe through `xargs`, or `find … -exec cmd {} +` |
| `Text file busy` | Overwriting a script while it is running — write to a temp file and `mv` it into place |
| `Permission denied` on `./script` | Missing `+x`, or the filesystem is mounted `noexec` (`/tmp` on hardened hosts) |
| `Exec format error` | No shebang and the file is not a binary the kernel recognizes, or wrong CPU architecture |
| Exit 141, no message | SIGPIPE — a downstream consumer closed early (see SKILL.md Exit Codes) |

## Chain: The Script Stops Mid-Way With No Message

1. That is `set -e` firing. Name the culprit before anything else:
   ```bash
   set -Eeuo pipefail
   trap 'rc=$?; printf "FAIL rc=%d line=%s cmd=%s\n" "$rc" "$LINENO" "$BASH_COMMAND" >&2' ERR
   ```
   `-E` (errtrace) is what makes the ERR trap fire inside functions and subshells; without it the trap is silent exactly where you need it.
2. Full stack: inside the handler, `local i=0; while caller "$i"; do ((i++)); done` prints `line function file` for every frame.
3. If the ERR trap never fires, the exit was deliberate: grep for `exit`, and remember a `return` at top level is an error, not an exit.
4. Still invisible? The script may be dying in a subshell whose failure propagates on assignment — `shopt -s inherit_errexit` (`bash >=4.4`) makes `x=$(failing)` fail visibly.

## Chain: It Hangs

1. Something is reading stdin. Inside a `while read` loop, `ssh`/`mysql`/`ffmpeg` swallow the remaining input and the loop appears to stall — add `ssh -n` or `< /dev/null` to the inner command.
2. A prompt with nowhere to go: `sudo` asking for a password with no TTY, or `read` with no input. Detect the environment instead of assuming: `[[ -t 0 ]]` before prompting.
3. A pipe buffer deadlock: a Linux pipe holds 65536 bytes; a process substitution whose reader never drains blocks the writer forever once it exceeds that. Consume the whole stream or redirect it to a file.
4. Waiting on a child that will not exit: `ps -o pid,ppid,stat,wchan,args --forest -g $(ps -o pgid= -p <pid>)` shows which descendant is alive and in what state.
5. Prevention, not diagnosis: wrap every network or lock call in `timeout 30 cmd` — exit 124 means expiry (SKILL.md Exit Codes).

## Chain: Works In My Terminal, Fails In The Script

| Difference | Check |
|---|---|
| Aliases and shell functions from `~/.bashrc` | Non-interactive shells expand no aliases at all. `type -a cmd` in both contexts; scripts must call the real binary |
| Your interactive shell is zsh or fish | The "working" version was never bash. Re-run with `bash -c '…'` before debugging the script |
| PATH and environment | `diff <(env) <(env -i bash -lc env)` — the delta is what the script will not have |
| Shell options set in your profile (`extglob`, `globstar`) | Scripts start with defaults: `shopt -s` the ones you rely on, in the script |
| Current directory | Interactive you are in the project; the script may run from `/` or `$HOME`. Anchor: `cd "$(dirname "${BASH_SOURCE[0]}")"` |
| Locale | `LC_ALL` changes `sort` order, `[a-z]` ranges, and `printf` decimal separators — pin `LC_ALL=C` for byte-stable behavior |

## Chain: Works As Me, Fails Under sudo Or Another User

- `sudo` resets the environment by default (`env_reset`) and `secure_path` in sudoers overrides PATH even if you exported one. Pass what you need explicitly: `sudo env VAR=x cmd`, or `sudo -E` when policy allows.
- `$HOME` becomes root's for `sudo -i`, stays yours for plain `sudo` — a script writing `~/.cache` writes to two different places depending on the invocation.
- The umask differs between login shells and service managers; files created 0600 for you can land 0644 for the daemon. Set the umask you require in the script.
- Redirection is done by YOUR shell before sudo runs: `sudo cmd > /root/out` fails on permissions; `cmd | sudo tee /root/out >/dev/null` works.

## Chain: Different Result On The Same Input

- Glob and `sort` order follow the locale — `LC_ALL=C` for byte order; anything else is collation-dependent and differs between your laptop and the server.
- Bash caches command locations: after installing or moving a binary, an old path persists until `hash -r`.
- Parallel sections interleave output; a "corrupted" log is usually two writers on one fd (line-buffered writes under 4096 bytes are atomic on Linux pipes, larger ones are not).
- Hash-ordered iteration: associative array traversal order is unspecified — sort the keys when output must be stable.

## Minimal Reproduction

`bash --noprofile --norc -x -c '<the five suspect lines>'` runs with nothing inherited from your environment. Re-add one thing at a time — the addition that breaks it names the cause and the file to open next in SKILL.md Quick Reference.
