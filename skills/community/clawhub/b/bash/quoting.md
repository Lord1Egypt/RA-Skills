# Quoting, Word Splitting, and Building Commands Safely

One model explains 90% of quoting bugs: after substitution, bash splits the RESULT on `$IFS` and then glob-expands each piece — unless the substitution was inside double quotes. Quoting does not "escape characters"; it turns off that second pass.

## What Actually Happens To `$var`

| Written | With `var='a  b*'` | Why |
|---|---|---|
| `cmd $var` | two args: `a`, then every file matching `b*` (or literal `b*`) | split on IFS, then globbed |
| `cmd "$var"` | one arg: `a  b*` | no split, no glob, spacing preserved |
| `cmd '$var'` | one arg: `$var` | single quotes stop substitution itself |
| `cmd ${var}x` | same as unquoted — braces only delimit the NAME | braces are not quoting |
| `arr=($var)` | splits and globs into elements | the one place splitting is usually intended — and the reason `arr=($(cmd))` is a trap |

- IFS default is space, tab, newline. Sequences of those collapse and leading/trailing ones are dropped; any OTHER IFS character delimits one field each, so `IFS=,` on `a,,b` yields three fields with an empty middle.
- Assignment is exempt: `x=$var` never splits, no quotes required. So is the right side of `[[ = ]]` and `case`.
- Globbing off entirely: `set -f` (`noglob`). Reach for it when handling patterns you must NOT expand, and turn it back on with `set +f`.

## When Unquoted Is Correct

Three cases, all deliberate, each carrying a comment:

- You want word splitting of a value you control: `# shellcheck disable=SC2086 -- flags must split`
- Glob patterns on the right of `[[ $f == *.txt ]]` — quoting the pattern makes it a literal string, the classic silent match failure
- Numeric context inside `(( ))`, where splitting cannot apply

Everything else is quoted. `"$@"` in particular: `$@` unquoted destroys empty arguments, and `"$*"` collapses all arguments into one.

## Build Commands As Arrays

String-building a command re-enters the parser and loses the boundary between "data" and "syntax":

```bash
# WRONG: the quotes become literal characters inside one argument
opts="--exclude '*.log' --bwlimit=1000"
rsync $opts src/ dst/            # rsync sees --exclude and '*.log' with the quotes attached as literal characters

# RIGHT: one array element = one argv entry, forever
opts=(--exclude '*.log' --bwlimit=1000)
[[ $dry == 1 ]] && opts+=(--dry-run)
rsync "${opts[@]}" src/ dst/
```

- Same rule for an optional flag: never `cmd ${verbose:+-v}` when it could carry a value; build the array.
- Empty arrays under `set -u` need `bash >=4.4`; below that use `${opts[@]+"${opts[@]}"}`.
- Dry-run for free: `printf '%q ' "${cmd[@]}"; echo` prints exactly what will run, re-pasteable into a shell.

## The `--` And `./` Habits

- `rm -- "$f"`, `grep -- "$pattern" file`: `--` ends option parsing, so a value beginning with `-` is treated as data. Without it, a file named `-rf` is an argument to `rm` you did not intend.
- Not every tool honors `--`; the universal fallback is a path prefix: `rm ./"$f"`.
- `grep -e "$pat"` and `find . -name "$name"` are the option-safe forms for tools whose value could start with a dash.

## Quoting Across A Second Parser

Anything that hands a STRING to another shell re-parses it. One level of quoting is consumed per hop:

- `ssh host "cmd $arg"` — the remote shell splits `$arg` again. Correct: `ssh host "$(printf '%q ' cmd "$arg")"`, or better, avoid the string: `ssh host bash -s <<'EOF'` … `EOF` and pass data on stdin.
- `su -c`, `bash -c`, `sudo sh -c`, `xargs sh -c`, `find -exec sh -c` — same hop, same fix. With `find`, keep the data out of the string: `find . -exec sh -c 'process "$1"' _ {} \;` passes the filename as `$1` instead of interpolating it.
- `printf '%q'` quotes for bash specifically; `${var@Q}` (`bash >=4.4`) does the same inline. Neither is safe for a remote shell that is not bash (busybox `ash` accepts most of it; `csh` does not).
- Never build a remote command with `eval`. If you think you need `eval`, you need an array plus `"$@"`, or stdin.
- `awk -v x="$val" '…'` and `jq --arg x "$val" '…'` pass values as DATA; interpolating `$val` into the program text makes user input part of the program.

## Filenames That Fight Back

- Anything except `/` and NUL is legal in a filename: newlines, backslashes, leading dashes, terminal escape sequences.
- Therefore NUL is the only safe delimiter between filenames: `find … -print0` with `while IFS= read -r -d ''`, `xargs -0`, `sort -z`, `grep -z`.
- Bash strings cannot hold NUL: `$(find … -print0)` silently drops the separators (bash warns "ignored null byte"). Never round-trip a NUL-delimited stream through a variable — pipe it or use `mapfile -d ''` (`bash >=4.4`).
- Printing a hostile name to a terminal can execute escape sequences: use `printf '%q\n' "$f"` in logs and error messages.

## Diagnosing A Quoting Bug In One Line

```bash
printf '<%s>\n' "$var" "${arr[@]}"   # one <…> per argument: boundaries become visible
```

If you see one `<…>` where you expected three (or three where you expected one), the bug is exactly here — not in the command that consumed them.
