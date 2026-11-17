# Error Handling — Strict Mode, Traps, and Exit Paths

The three `set -e` killers practitioners actually hit — `local` masking, `((i++))`, `grep -q` SIGPIPE — live in SKILL.md Traps. Mechanics and design below.

## Where set -e Is Blind

- Not in an `if`/`while` condition — and that immunity extends to the ENTIRE body of any function called there: `if myfunc; then` runs all of `myfunc` with `-e` off
- Not after `||` or `&&` — `cmd || true` is the idiomatic "allowed to fail"; in `a && b && c` only the LAST command's status can kill the script
- Not inside `$(cmd)` in an assignment — the subshell's failure vanishes; fix with `shopt -s inherit_errexit` (bash >=4.4)
- Not for a negated command: `! cmd` never triggers `-e`
- `exit` in a subshell exits only the subshell — the parent continues
- Consequence: `-e` is a net for the straight-line 80%, not a control-flow mechanism. Anything you actually care about gets an explicit check

## Pipelines

- Exit code is the LAST command's — `bad | good` returns 0 without `set -o pipefail`
- `pipefail` says a pipeline failed but not which segment — read `PIPESTATUS`, and copy it immediately: `st=("${PIPESTATUS[@]}")` — any command, even `[[`, resets it
- Early-exit consumers (`head`, `grep -q`) close the pipe; the producer dies with SIGPIPE = exit 141 (128+13) — under pipefail that reads as failure even when the pipeline did its job
- Variables set inside a pipe segment don't persist — subshell (→ SKILL.md Subshells and State)
- Worked check of a two-stage pipeline:
  ```bash
  set -o pipefail
  out=$(producer | jq -r .id) || { st=("${PIPESTATUS[@]}"); die "producer=${st[0]} jq=${st[1]}"; }
  ```

## Traps and Cleanup

- `trap cleanup EXIT` fires on error and normal exit alike; `kill -9` bypasses every trap — make cleanup idempotent (`rm -f`, not `rm`)
- A second `trap ... EXIT` REPLACES the first silently — one handler per script; extend by appending inside it, and read the current one with `trap -p EXIT`
- Single-quote the trap body so it expands when it FIRES, not when it is registered (→ SKILL.md Traps)
- `ERR` traps don't fire inside functions or subshells unless you `set -E` (errtrace)
- Register the trap on the line immediately after the resource exists — never before it, never three lines later:
  ```bash
  tmp=$(mktemp -d) || die "mktemp failed"
  trap 'rm -rf "$tmp"' EXIT        # the very next line
  ```
- Signals need their own handlers if the exit code must stay honest: `trap 'cleanup; exit 130' INT` and `trap 'cleanup; exit 143' TERM` preserve the 128+signal convention (SKILL.md Exit Codes)
- Cleanup must not clobber the status: capture it first — `cleanup() { rc=$?; rm -f "$tmp"; return "$rc"; }` — or a successful `rm` converts a failure into a success
- Unregister when a resource is deliberately handed off: `trap - EXIT` after the temp dir has been renamed into place

## Returning Status From Functions

- `return` outside a function is an error — `exit` at top level, `return` in functions
- A function's status is its last command's status unless you `return` explicitly; a trailing `echo` or `[[ ]]` silently becomes the return value
- Sourced libraries return, never exit — `exit` in a sourced function kills the caller's shell (→ SKILL.md Traps)
- Distinguish "failed" from "answered no": `is_ready` returning 1 for "not ready" collides with 1 for "broke". Reserve `return 2` for real errors and say so in the function header

## Exit Code Discipline

- 1 = generic failure, 2 = usage error, then a small documented set of ≥3 codes for conditions callers branch on. Codes above 125 collide with the shell's own conventions (SKILL.md Exit Codes)
- Propagate rather than invent: `cmd; rc=$?; ((rc == 0)) || exit "$rc"` keeps the original code visible to CI or a systemd unit
- Codes are mod 256: `exit 300` reports 44, `exit -1` reports 255
- `die() { printf '%s\n' "$*" >&2; exit "${2:-1}"; }` — one abort helper, message on stderr, code settable

## Reporting

- `die() { printf '%s\n' "$*" >&2; exit 1; }` — errors go to stderr so `$(...)` callers don't capture them as data
- Include context in the message: `die "config not found: $cfg"` — the failing VALUE, not just the fact
- One message per failure: the lowest layer that knows the value prints; upper layers stay silent. Two half-truths is the usual outcome of everyone reporting
- Non-fatal warnings also go to stderr — stdout is the data channel, and mixing them breaks every `$( )` caller

## Retries That Do Not Lie

Retry only idempotent operations, bounded, with backoff, surfacing the last error:

```bash
retry() {                         # retry <attempts> <cmd...>
  local -i n=$1 i=0; shift
  until "$@"; do
    (( ++i >= n )) && { printf 'giving up after %d attempts: %s\n' "$n" "$*" >&2; return 1; }
    sleep "$(( 2 ** i ))"         # 2s, 4s, 8s — total wait for n=4 is 14s
  done
}
```

- A retried non-idempotent POST duplicates work; add a request id and make it idempotent before wrapping it
- Never retry argument-class failures: a bad flag fails identically every time and buys nothing but the backoff delay

## Partial Failure In Loops

`set -e` aborts the whole batch on the first bad item — rarely what a batch job wants:

```bash
failed=0
for host in "${hosts[@]}"; do
  process "$host" || { printf 'FAILED %s\n' "$host" >&2; failed=$((failed+1)); }
done
(( failed == 0 )) || exit 1       # one nonzero exit summarizing the batch
```

Decide per loop: "all or nothing" (abort on first) or "best effort with a report" (collect, summarize, exit nonzero). A loop that does neither reports success while half the work failed.
