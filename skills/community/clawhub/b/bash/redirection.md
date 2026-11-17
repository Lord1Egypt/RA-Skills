# Redirection — File Descriptors, Heredocs, Locking

Redirections are applied left to right, BEFORE the command runs, by the shell — not by the command. Both classic bugs (`2>&1 >file`, `sudo cmd > /root/f`) follow from that one sentence.

## Order Matters

- `>file 2>&1` sends both to the file; `2>&1 >file` sends stderr to the OLD stdout (the terminal) and only stdout to the file — the duplication happens at the moment it is written
- `&>file` (bash >=4.0) is the unambiguous shorthand for both; `&>>file` appends
- `$( )` captures stdout only — stderr passes through to the terminal; capture both with `$(cmd 2>&1)` only when you truly want them merged into your data
- Capture stderr separately without a temp file: `err=$( { out=$(cmd); } 2>&1 )` — the inner braces keep the assignment in the current shell
- Redirections attach to the command, not the line: `while read …; done < file` reads the loop's stdin; a redirection on the `read` itself would reopen the file every iteration and loop forever on line 1

## Truncation And Clobbering

- `>` truncates at redirection time, before the command starts: `sort file > file` produces an empty file. Write to a temp and `mv`, or use `sponge` (moreutils) when available
- `sed -i`/`perl -i` avoid this by rewriting through a temp file themselves — that is what makes them safe where a shell redirect is not
- `set -o noclobber` makes `>` fail on an existing file; `>|` overrides it deliberately. Worth enabling in interactive shells, rarely in scripts (it converts a bug into an unexpected failure mid-run)
- `>>` opens with O_APPEND, so each small single write from concurrent processes lands whole at the end on a local filesystem — but a large write can still interleave, and NFS gives no such guarantee; log through one writer or `logger` when several processes share a file

## Common Fd Moves

| Goal | Form |
|---|---|
| Discard output, keep errors | `cmd >/dev/null` |
| Discard everything | `cmd >/dev/null 2>&1` |
| Errors to the same place as output | `cmd >log 2>&1` |
| Swap stdout and stderr | `cmd 3>&1 1>&2 2>&3 3>&-` |
| Send a message to the terminal even when stdout is redirected | `printf '…' >/dev/tty` |
| Keep a copy while still piping | `cmd \| tee log \| next` |
| Log everything the script prints, from inside the script | `exec > >(tee -a run.log) 2>&1` |
| Close a descriptor | `exec 3>&-` |

- `exec >file` (no command) redirects the SCRIPT's own stdout from that point on — the standard way to make a cron job self-logging
- Open a private descriptor for structured output so program data and human logs never mix: `exec 3>report.tsv; printf '%s\t%s\n' … >&3`
- `exec 3<>file` opens read-write on one descriptor; needed for lock files and for talking to a socket via `/dev/tcp/host/port`

## Heredocs and Herestrings

```bash
cat <<'EOF'      # quoted delimiter: NOTHING is expanded — the default for config and script bodies
$HOME stays literal, `cmd` is not run
EOF

cat <<EOF        # unquoted: parameters, $(cmd) and backslashes ARE expanded
deploying $app to $env
EOF

cat <<-EOF       # <<- strips leading TABS only (not spaces) so the block can be indented
	indented with a real tab
EOF
```

- Quote the delimiter unless you specifically want interpolation; an unquoted heredoc that contains `$(` runs a command at generation time
- A heredoc feeding a remote shell is the clean alternative to nested quoting: `ssh host bash -s <<'EOF'` … `EOF`, with values passed as arguments after `-s`
- Herestring `<<< "$var"` feeds one string plus a trailing newline; it materializes as a temp file on most systems, so it is not a hot-loop construct
- Inside `$(…)`, a heredoc must be closed within the substitution; unterminated heredocs produce "unexpected EOF" reported at the end of the file (`debugging.md`)

## Process Substitution

- `<(cmd)` presents a command's output as a filename: `diff <(sort a) <(sort b)`, `comm -13 <(sort old) <(sort new)`
- `>(cmd)` is the write side: `tee >(gzip > out.gz) >(sha256sum > sum) >/dev/null`
- It is what keeps a `while read` loop in the current shell: `done < <(cmd)` instead of `cmd | while` (→ SKILL.md Subshells and State)
- Exit status is NOT propagated: `while read … done < <(failing)` succeeds. When the producer's status matters, write to a temp file first or capture `PIPESTATUS` from a real pipeline
- Bash does not wait for `>(…)` consumers to finish before continuing — a following command may read a half-written file; `wait` after, or use a pipeline
- Requires `/dev/fd`; unavailable under `sh` on some minimal images (`portability.md`)

## Buffering

- A command writing to a pipe switches from line buffering to 4 KB block buffering — the reason `long_cmd | tee log` shows nothing for a minute
- Force line buffering on the producer: `stdbuf -oL cmd | …` (GNU), `unbuffer cmd` (expect), or the tool's own flag (`grep --line-buffered`, `awk` with `fflush()`, `python -u`)
- Interactive-only behavior belongs behind a TTY check, not behind buffering assumptions (`interactive.md`)

## Locking: One Instance At A Time

```bash
# Linux (util-linux flock): self-locking script, exits 1 if another copy holds the lock
exec 9>/var/lock/myjob.lock || exit 1
flock -n 9 || { echo "already running" >&2; exit 1; }
# ... work ...            # the lock releases when fd 9 closes, including on crash
```

- Hold the lock on a FILE DESCRIPTOR, never on the existence of a file: a PID file left behind by a crash blocks every future run until a human deletes it
- macOS has no `flock(1)`; the portable primitive is an atomic `mkdir`:
  ```bash
  lock=/tmp/myjob.lock
  mkdir "$lock" 2>/dev/null || { echo "already running" >&2; exit 1; }
  trap 'rmdir "$lock"' EXIT
  ```
  A `kill -9` still leaves the directory — store the PID inside it and let the next run reclaim a lock whose PID is gone
- Overlapping cron runs are the usual reason to need this at all (`cron.md`)

## Named Pipes

`mkfifo` gives two processes a rendezvous point without a temp file: `mkfifo p; producer > p & consumer < p; rm p`. Both sides block until the other opens, which is a feature for synchronization and a hang when only one side ever arrives — always pair it with a `timeout` (`processes.md`).
