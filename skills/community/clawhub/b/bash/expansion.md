# Expansion — Parameters, Braces, and String Surgery Without Forks

Every transformation here is a builtin: no fork, no `sed`, no `basename`. In a loop over thousands of items that is the difference between seconds and minutes.

## Expansion Order (why some bugs are unfixable by more quotes)

Bash expands in this fixed order: brace → tilde → parameter/arithmetic/command → word splitting → filename globbing → quote removal.

- `for i in {1..$n}` fails because braces expand BEFORE `$n` exists as a value — use `for ((i=1; i<=n; i++))` or `seq`.
- `~$user` does not expand either: tilde expansion happens before parameter expansion. Use `getent passwd "$user"` or `eval` only on a validated name.
- A glob produced by an expansion IS re-globbed (word splitting and globbing come after) — the reason unquoted `$var` can match files.
- Quote removal is last, which is why `"${var}"` never re-splits: there is no splitting pass after it.

## Defaults, Guards, and Assignment

- `${var:-default}` fires if unset OR empty — `${var-default}` only if unset. The set-but-empty case is where scripts diverge
- `${var:=default}` also assigns; `${var:-default}` doesn't touch var
- `${var:?msg}` aborts with msg if unset/empty — inline guard, the mechanism behind `rm -rf "${dir:?}/"` (→ SKILL.md Traps)
- `${var+set}` / `${var:+set}` are the inverse: expand only when the variable EXISTS — the safe way to add an optional flag: `cmd ${flag:+--flag "$flag"}`
- `${var:-$(cmd)}` runs cmd whenever the default is needed — side effects included
- Under `set -u`, `${var:-}` is the sanctioned "may legitimately be absent" marker; reaching for `set +u` instead hides real typos

## Substrings and Length

- `${#var}` character count; `${#arr[@]}` element count (`${#arr}` is the length of element 0)
- `${var:0:5}` first 5 characters; `${var:5}` from position 5 to the end
- `${var: -3}` last 3 chars — the space is mandatory; `${var:-3}` is default-value syntax
- Counting is in CHARACTERS in the current locale — under `LC_ALL=C` multibyte characters split into bytes, which is what you want for byte-exact work and never what you want for user-visible truncation
- Positional parameters slice too: `"${@:2}"` = args from the 2nd on, `"${@:2:3}"` = three of them

## Path Surgery (worked example, `f=/a/b/c.tar.gz`)

- `${f##*/}` → `c.tar.gz` (basename) · `${f%/*}` → `/a/b` (dirname)
- `${f##*.}` → `gz` (extension) · `${f%%.*}` → `/a/b/c` — but if a DIRECTORY contains a dot (`/v1.2/c.tar.gz`) it eats the path too; strip the dir first: `b=${f##*/}; echo "${b%%.*}"` → `c`
- `#`/`%` = shortest from start/end; `##`/`%%` = longest. Patterns are globs, not regex: `*` wildcards, `.` is literal
- Edge cases the builtins get wrong and `dirname` does not: `f=file` (no slash) leaves `${f%/*}` as `file`, not `.`; `f=/` collapses to empty. Guard with `d=${f%/*}; d=${d:-/}` when the input can be either

## Replace and Transform

- `${var/pat/rep}` first match — `${var//pat/rep}` all; empty replacement deletes: `${var//pat}`
- Anchors: `${var/#pat/rep}` only at the start, `${var/%pat/rep}` only at the end
- Strip Windows line endings after reading CRLF files: `${line//$'\r'/}`
- Case: `${var^^}` upper, `${var,,}` lower (bash >=4.0) — first character only with a single `^`/`,`; on macOS 3.2 pipe through `tr '[:upper:]' '[:lower:]'`
- Expansions don't nest: `${${f##*/}%.*}` is a syntax error — two assignments, two lines
- Per-element on arrays: `"${arr[@]/#/prefix-}"` prepends to every element; `"${arr[@]%.txt}"` strips from each
- The replacement side is NOT a pattern but IS subject to `&` meaning "the match" in bash 5.2+; escape a literal ampersand as `\&`

## Brace Expansion (text generation, not matching)

- `{a,b}` alternatives and `{1..10}` ranges are pure text generation — they run even when nothing on disk matches, unlike globs
- Step and padding: `{1..10..2}` → 1 3 5 7 9; `{01..12}` keeps the zero padding — the readable way to build month or shard lists
- Combining: `mkdir -p logs/{app,db}/{2025,2026}` creates four directories in one fork
- The backup idiom: `cp config.yaml{,.bak}` → `cp config.yaml config.yaml.bak`; `mv file{.txt,.md}` renames
- Nothing is quoted after expansion, so a value with spaces inside a brace list still needs its own quotes

## Arithmetic Expansion

- `$(( ))` yields a value; `(( ))` yields a status. `n=$((n+1))` for a number, `(( n++ ))` when you can afford the status trap (→ SKILL.md Traps)
- Inside `$(( ))`, `$` on names is optional and quotes are unnecessary: `$(( total * qty ))`
- Integers only. Money and averages either scale to integers (cents, milliseconds) or go to `awk '{printf "%.2f", …}'` / `bc -l`
- `$(( 10#$m ))` forces base 10 — the fix for values with leading zeros (→ `conditionals.md` for the octal error itself)

## Indirection and Introspection

- `${!var}` expands the variable NAMED BY var — read-only indirection
- `declare -n ref=name` (bash >=4.3) — read AND write through the alias; prefer it over `eval` for dynamic names
- `${!prefix@}` lists variable NAMES starting with prefix, not values — the clean way to iterate a config namespace: `for k in "${!CFG_@}"; do printf '%s=%s\n' "$k" "${!k}"; done`
- `${var@Q}` quotes a value safely for reuse in generated commands (bash >=4.4) — `printf '%q'` on older bash
- `${var@A}` (bash >=4.4) prints an assignment statement that recreates the variable, arrays included — the portable way to ship state to a subshell or a remote `bash -s`
- `declare -p var` does the same at debug time and shows the attributes (`-i` integer, `-a` array, `-A` map, `-x` exported)

## Reading Files Without Forking

- `content=$(<file)` is a builtin read; `$(cat file)` forks twice for the same result
- Both strip ALL trailing newlines. When the exact bytes matter: `content=$(cat file; printf x); content=${content%x}`
- `printf -v var '%s' "$x"` (bash >=3.1) assigns formatted text without a subshell — the fast path for building strings in loops
- `mapfile -t lines < file` (bash >=4.0) loads a file into an array in one read; a `while read` loop over the same file costs one read syscall per line
