# Functions and Script Structure

A script past 50 lines is a program: it needs a shape. The shape that survives review is "definitions first, one `main`, execution last" — because it is also the shape that can be sourced by a test (`testing.md`).

## The Layout

```bash
#!/usr/bin/env bash
# what it does, one line. usage: script [-v] TARGET
set -euo pipefail

readonly VERSION=1.4.0
: "${LOG_LEVEL:=info}"            # env-overridable defaults, never hardcoded behavior

usage() { …; }
parse_args() { …; }
do_work() { …; }

main() {
  parse_args "$@"
  require_cmds jq curl
  do_work
}

[[ ${BASH_SOURCE[0]} == "$0" ]] && main "$@"
```

- Constants `readonly` and uppercase; everything else lowercase and `local`. The case convention is the only marker Bash gives you for "do not reassign"
- `main "$@"` last: nothing executes while the file is being read, so a test can source it and call one function
- `require_cmds() { local c; for c in "$@"; do command -v "$c" >/dev/null || die "missing dependency: $c"; done; }` — fail at second one with a name, not at minute nine with "command not found"

## Scope Is Dynamic, Not Lexical

A function sees the locals of whoever called it. This is the invisible distinction that separates Bash from every language people compare it to:

```bash
outer() { local tmp=/outer; inner; }
inner() { printf '%s\n' "$tmp"; }   # prints /outer — inner never declared it
```

- Consequence 1: forgetting `local` in a helper silently overwrites the caller's variable of the same name. Declare EVERY variable in a function `local`, including loop counters
- Consequence 2: generic names (`i`, `tmp`, `file`, `line`) collide across call levels. Prefix a library's internals (`_log_fmt`) and its globals (`LIB_STATE`)
- `local x=$(cmd)` masks the command's failure (→ SKILL.md Traps): declare, then assign
- `local -a arr` / `local -A map` for containers; `local -n ref` for by-reference parameters (`bash >=4.3`), which must not share the caller's name
- `declare -g` (`bash >=4.2`) sets a global from inside a function when that is genuinely what you mean — the explicit form beats an accidental one

## Returning Values

- Status is not a value: `return` takes 0-255 and means success/failure. Returning a count through `return` breaks the moment the count exceeds 255
- Print the value, capture it: `v=$(compute)`. Costs a fork, composes with everything
- Write through a nameref for hot loops and large payloads: `compute_into result "$input"` with `local -n out=$1` — no fork, at the price of coupling (SKILL.md Where Experts Disagree)
- Multiple values: print them TAB-separated and `IFS=$'\t' read -r a b < <(f)`, or fill an array through a nameref. Never echo them space-separated for the caller to re-split
- A function's status is its last command's — a trailing `[[ ]]` or `echo` becomes the return value by accident; end with an explicit `return 0` when the last statement is incidental

## Libraries and Sourcing

```bash
# lib/common.sh — no shebang needed, but keep one for editors and shellcheck
[[ -n ${_COMMON_SH:-} ]] && return 0   # idempotent: sourcing twice is a no-op
readonly _COMMON_SH=1
```

- A library never runs `set -e`/`set -u` (it would mutate the caller's shell) and never calls `exit` (it would kill the caller's shell). It defines functions and returns
- Source by absolute path derived from the script's own location, so the library is found regardless of the working directory:
  ```bash
  here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
  # shellcheck source=lib/common.sh
  source "$here/lib/common.sh"
  ```
- The `# shellcheck source=` comment is what lets the linter follow it; without it, every library function reads as undefined (`testing.md`)
- `source` and `.` are identical; `source` accepts a filename, and with no slash in the name it searches PATH — always pass a path with a slash
- `export -f fn` exports a function to child BASH processes only, through a specially named environment variable. It does not work for non-bash children and is a frequent source of surprise — pass data, not functions

## Logging Helpers That Do Not Fight Your Output

```bash
log()  { printf '%s [%s] %s\n' "$(date -u +%FT%TZ)" "$1" "${*:2}" >&2; }
info() { [[ $LOG_LEVEL == debug || $LOG_LEVEL == info ]] && log INFO "$@"; return 0; }
debug() { [[ $LOG_LEVEL == debug ]] && log DEBUG "$@"; return 0; }
```

- Logs go to stderr, always: stdout is the script's data and a caller may be capturing it
- The trailing `return 0` matters — a failed `[[ ]]` as the last command makes the function return 1 and, under `set -e` inside another function's `if`, produces bewildering control flow
- One timestamp format for the whole tool, UTC and ISO-8601, so `sort` on the log is chronological

## Loading User Configuration

Read the values declared in SKILL.md Configuration from `~/Clawic/data/bash/config.yaml` when they exist and fall back to the defaults; never prompt for them. Parse with `yq` if available, otherwise read only the flat `key: value` lines you know:

```bash
cfg=$HOME/Clawic/data/bash/config.yaml            # the canonical location, unconditionally
[[ -r $cfg ]] && while IFS=': ' read -r k v; do
  case $k in indent_style|lint_gate|bash_floor) printf -v "cfg_$k" '%s' "$v" ;; esac
done < "$cfg"
```

Never `source` a YAML or INI file to "parse" it — that executes whatever is inside, which is code execution from a config file (`security.md`).

## Recursion and Limits

- Recursion works and is almost never the right answer in Bash; `FUNCNEST=100` (`bash >=4.2`, so not on stock macOS 3.2) caps runaway depth and turns a hang into an error
- Deep call chains cost real time: each level is a variable-scope frame, and any command substitution inside is still a fork (`performance.md`)
- The moment a function needs a data structure to recurse over, you are past SKILL.md Core Rule 9 — switch languages rather than simulating a tree with delimited strings
