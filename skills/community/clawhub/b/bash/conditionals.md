# Conditionals — Tests, Patterns, Regex, Arithmetic

Three syntaxes, three jobs: `[[ ]]` for strings, files, and patterns; `(( ))` for numbers; `[ ]` only when the script must run under POSIX sh. Mixing them up produces conditions that are silently always-true.

## Choosing The Construct

| Comparison | Write | Never |
|---|---|---|
| Strings equal | `[[ $a == "$b" ]]` | `[ $a = $b ]` (splits, breaks when empty) |
| Numbers | `(( a > b ))` or `[[ $a -gt $b ]]` | `[[ $a > $b ]]` — that is LEXICAL |
| Glob match | `[[ $f == *.txt ]]` | quoting the pattern makes it literal |
| Regex match | `re='^v[0-9]+$'; [[ $v =~ $re ]]` | inline quoted patterns (quoted parts go literal) |
| Empty / non-empty | `[[ -z ${s:-} ]]` / `[[ -n ${s:-} ]]` | `[ $s ]`, ambiguous with `-n`-like values |
| File exists | `[[ -e $f ]]` | `ls "$f" >/dev/null 2>&1` |
| Anything, in POSIX sh | `[ "$a" = "$b" ]` with every value quoted | bashisms that die with "unexpected operator" |

## [ vs [[

- `[ $var = "x" ]` breaks when var is empty or has spaces — quote inside `[ ]` always; `[[ $var = x ]]` doesn't word-split, unquoted left side is safe
- `<` and `>` inside `[ ]` are redirects — you just created a file named `9`. Use `-lt`/`-gt`, or `[[ ]]` where they compare
- `[[ $a < $b ]]` is still LEXICAL string comparison — `[[ 10 < 9 ]]` is true (1 sorts before 9). Numbers go in `(( ))` or `-lt`
- `==` and `=` are identical inside `[[ ]]`; POSIX `[` only guarantees `=`
- `[[ -v var ]]` (bash >=4.2) is true for set-but-EMPTY variables — `[[ -n ${var:-} ]]` is not; pick by which case you mean
- `[ a -a b ]` and `[ a -o b ]` are deprecated and ambiguous with operands that look like operators — use `[[ a && b ]]`, or two `[ ]` joined with `&&`
- Inside `[[ ]]`, `&&`/`||` bind tighter than in the shell and need no escaping; parentheses group: `[[ ( $a || $b ) && $c ]]`

## The Right Side Of == Is A Pattern

```bash
pat='*.log'
[[ $f == $pat  ]]   # GLOB MATCH — pat is expanded as a pattern
[[ $f == "$pat" ]]  # literal comparison against the six characters *.log
```

This one rule explains most "my comparison matches everything" bugs: an unquoted variable on the right of `==`, `!=`, or `case` is a pattern, and a value of `*` matches anything. Quote unless you mean matching.

## Patterns And case

- `case` patterns are globs with `|` alternation — `*.txt|*.md)` works, regex doesn't; `;&` falls through (bash >=4.0), `;;&` continues testing later patterns
- `case` is faster and clearer than an `if` chain for dispatch, and it needs no quoting on the subject: `case $cmd in start|up) … ;; *) usage ;; esac`
- Always include a `*)` default branch — a dispatch table with no default silently accepts typos
- `shopt -s extglob` unlocks `?(a)` `*(a)` `+(a)` `@(a|b)` `!(a)`: `[[ $f == !(*.tmp) ]]`, `rm -- !(keep.txt)`. The negation form is the readable alternative to a chain of `!=` tests
- `shopt -s nocasematch` makes `[[ ]]` and `case` case-insensitive — set it locally and unset it, since it changes every comparison in scope

## Regex

- Keep the pattern in a variable — `re='^[0-9]+ (GET|POST)'; [[ $line =~ $re ]]`. Quoting any part of an inline pattern makes that part literal, the classic silent regex breakage
- Captures land in `BASH_REMATCH`: `${BASH_REMATCH[1]}` = first group, `${BASH_REMATCH[0]}` = whole match. Copy them out immediately; the next `[[ =~ ]]` overwrites the array
- Bash uses POSIX ERE, not PCRE: no `\d`, no `\w`, no lazy `*?`, no lookahead. Character classes are `[[:digit:]]`, `[[:alpha:]]`, `[[:space:]]`
- A literal `.` or `+` inside a bracket expression is literal; outside it needs a backslash — and a backslash inside a quoted portion of the pattern is itself literal, so build the pattern with single quotes and no shell escaping
- Matching is unanchored: `[[ v1.2 =~ [0-9] ]]` is true. Anchor with `^…$` when validating a whole value
- ERE has no non-greedy operator; when you need one the job belongs to `sed`/`awk`/`jq` rather than to a bigger regex

## Arithmetic

- `(( n > 5 ))` for numbers — but a variable holding a non-numeric string silently evaluates to 0, and untrusted content can execute code via subscripts (→ SKILL.md Core Rule 8)
- Leading zeros mean octal: `$((08))` is an error ("value too great for base") — force decimal with base prefix: `m=08; echo $((10#$m))` → 8
- `(( ))` returns status 1 when the value is 0 — the `((i++))` + `set -e` interaction (→ SKILL.md Traps)
- Integer only: `(( 7/2 ))` is 3 and `(( 1.5 > 1 ))` is a syntax error. Compare decimals with `awk 'BEGIN{exit !(1.5 > 1)}'` or scale to integers
- Ternary and assignment work inside: `(( max = a > b ? a : b ))`
- Empty string is 0 under `(( ))` but an error under `set -u` when the variable is unset — write `(( ${n:-0} > 5 ))` for values that may be absent

## Comparing Versions

`[[ 1.10 > 1.9 ]]` is false (lexical) and `(( ))` cannot parse dotted versions. The dependable comparison is a sort:

```bash
# true when $have >= $want
[[ "$(printf '%s\n%s\n' "$want" "$have" | sort -V | head -n1)" == "$want" ]]
```

`sort -V` is GNU and BSD-modern; on a host without it, compare field by field after `IFS=. read -r maj min patch <<< "$v"`.

## File Tests

- `-e` exists (any type) · `-f` regular file · `-d` directory · `-L` symlink itself (`-f` follows the link)
- A broken symlink is `-L` true and `-e` false — the pair that identifies it
- `-r`/`-w`/`-x` test YOUR effective permissions, not the mode bits — running as root they are true for almost everything, so a root-run script cannot use them to validate a user's access
- `-s` exists AND non-empty — the common "did the command produce output" check
- `file1 -nt file2` newer-than — rebuild-if-stale logic without make. On a MISSING file2 it is true, and on missing file1 it is false: guard both paths, since the "rebuild everything" and "rebuild nothing" outcomes look identical in the code
- Every file test is a race: the answer is stale the instant it returns. For anything security-relevant, act and handle the error instead of testing first (`security.md`)

## Short-Circuit Chains Are Not if/else

`a && b || c` runs `c` whenever `b` fails, not only when `a` fails — the classic silent-double-execution bug. Use it only when `b` cannot fail (`echo`), and write a real `if` otherwise.
