# Text Processing — Where Bash Stops and awk/sed/jq Start

The decision rule: if the transformation is per-line and stateless, a single `awk`/`sed` pass beats a Bash loop by an order of magnitude and is shorter. If it orchestrates commands per item, the loop is right. Mixing them — a `while read` loop that calls `grep` and `cut` on every line — is the slowest possible arrangement (`performance.md`).

## Pick The Tool

| Job | Tool | Note |
|---|---|---|
| Select lines matching a fixed string | `grep -F` | `-F` skips regex compilation and cannot be broken by metacharacters in the pattern |
| Select whole-word or whole-line matches | `grep -w` / `grep -x` | `grep host` also matches `localhost.bak` |
| Extract a fixed column from clean data | `cut -f2 -d,` | Fails on quoted CSV fields — see below |
| Extract, compute, or reformat by field | `awk` | Also the answer to "sum column 3 grouped by column 1" |
| Substitute in a stream | `sed 's/…/…/g'` | In-place editing flags differ GNU vs BSD (`portability.md`) |
| Structured JSON | `jq` | Never grep JSON; a reordered or reformatted document breaks the pattern |
| Structured YAML/TOML | `yq`, or a Python one-liner | Same reason |
| Count occurrences | `sort \| uniq -c \| sort -rn` | `uniq` only collapses ADJACENT duplicates — the first `sort` is mandatory |
| Join two datasets on a key | `join -t, -1 1 -2 1 a b` | Both inputs must be sorted on the key with the SAME collation (`LC_ALL=C`) |
| Set operations on two lists | `comm -13 <(sort a) <(sort b)` | -13 = only in b; -23 = only in a; -12 = common |
| Anything else | Bash loop with the pattern below | Then measure it |

## awk In Five Idioms

```bash
awk -F, '$3 > 100 {print $1}' data.csv                 # filter by a numeric field
awk -F, '{sum[$1] += $3} END {for (k in sum) print k, sum[k]}' data.csv   # group and sum
awk 'NR > 1' file                                      # drop the header line
awk -v key="$user" -F, '$1 == key' data.csv            # pass a shell value as DATA, never interpolated
awk '{print $NF}' file                                 # last field, whatever the count
```

- `-v name=value` is the only correct way to get a shell variable into awk: interpolating `'"$var"'` into the program makes user input part of the program text
- Default field separator is runs of whitespace with leading/trailing trimmed, which is why `awk '{print $2}'` handles ragged `ps` output that `cut` cannot
- `awk` implementations differ (gawk, mawk, BSD awk): `gensub`, `asort`, and `length(array)` are gawk extensions. Stick to POSIX awk in anything shipped to other machines

## Reading Structured Data Safely

- Key=value and TSV lines split cleanly with `read`:
  ```bash
  while IFS=$'\t' read -r name count rest; do …; done < data.tsv
  ```
  Name the trailing field (`rest`) or the last variable silently absorbs every remaining column
- Real CSV — quoted fields, embedded commas and newlines — cannot be parsed with `IFS=,`. Convert once with a real parser (`python3 -c 'import csv,sys;…'`, `mlr`, `csvkit`) and work in TSV afterwards; hand-rolled CSV parsing in Bash is where scripts go to die
- JSON into shell variables, one fork, no eval:
  ```bash
  read -r id status < <(jq -r '[.id, .status] | @tsv' resp.json)
  mapfile -t names < <(jq -r '.items[].name' resp.json)          # one per line
  ```
- Pass shell values into jq as arguments: `jq --arg u "$user" '.users[] | select(.name == $u)'`
- `jq -r` strips the quotes; without it every value carries them into your comparisons. `jq -e` sets exit status 1 when the result is null or false — the way to test for presence

## grep Exit Codes Are Load-Bearing

- 0 = matched, 1 = no match, 2 = actual error (unreadable file, bad pattern). Under `set -e`, "no match" kills the script: write `grep -q … || true` when absence is a legitimate outcome, and distinguish 2 when it is not:
  ```bash
  if out=$(grep -F "$needle" file); then found=1; elif (( $? == 1 )); then found=0; else die "grep failed"; fi
  ```
- `grep -q` exits at the first match and closes the pipe — upstream producers die with SIGPIPE 141 (→ SKILL.md Traps)
- A file with a NUL byte makes grep report "Binary file … matches" and print nothing; `grep -a` forces text mode
- Patterns from variables need `-e`: `grep -e "$pat"` survives a pattern starting with `-`; `grep -F -- "$pat"` when it is a literal

## sed Without Regret

- Delimiters are free: `sed 's|/old/path|/new/path|'` avoids escaping every slash
- `sed -n '5,10p'` prints a line range; `sed -n '/START/,/END/p'` prints between markers; `sed '$d'` deletes the last line
- Backreferences are `\1` in BRE (`sed`) and `$1` in Perl; capture groups need `\(` `\)` in BRE or `sed -E` for ERE
- Editing files in place is where portability bites: `sed -i` (GNU) vs `sed -i ''` (BSD). The portable form is a temp file plus `mv` (`files.md`)
- Multi-line and conditional edits belong in awk or a real language; `sed` hold-space programs are write-only code

## Whitespace, Encoding, Line Endings

- Trim in Bash without a fork: `${v#"${v%%[![:space:]]*}"}` strips leading, `${v%"${v##*[![:space:]]}"}` strips trailing
- Strip CRLF from a whole file: `sed 's/\r$//'`, or `tr -d '\r'` when no other CR can legitimately appear
- `tr` works on characters, not strings: `tr -d '\r'` deletes carriage returns, `tr ',' '\t'` swaps delimiters, `tr -s ' '` squeezes runs
- `LC_ALL=C` makes `sort`, `[a-z]`, and byte counting deterministic and fast; without it, sort order depends on the machine's locale and a pipeline can produce different output on two hosts (`debugging.md`)
- UTF-8 sequences survive every tool above as long as you never index by byte; `${#var}` counts characters in the current locale (`expansion.md`)

## Timestamps and Durations

- One format for everything a machine will read: `date -u +%FT%TZ` (ISO-8601, UTC). It sorts lexically, which means `sort` on a log is chronological and `[[ $a < $b ]]` compares times correctly
- Epoch seconds are the arithmetic form: `now=$(date +%s)`, `age=$(( now - then ))`. Convert back with `date -d @"$e"` (GNU) or `date -r "$e"` (BSD) — the split covered in `portability.md`
- `EPOCHSECONDS` (`bash >=5.0`) gives the same number with no fork; `$SECONDS` counts elapsed seconds since the shell started, also builtin
- Format a duration without a helper: `printf '%02d:%02d:%02d\n' $((s/3600)) $((s%3600/60)) $((s%60))`
- Date arithmetic ("7 days ago") has no portable builtin form: `date -d '7 days ago' +%F` on GNU, `date -v-7d +%F` on BSD, or compute in epoch seconds (`$(( now - 7*86400 ))`) — the epoch form is wrong across a DST boundary by an hour, which matters for local-time reports and not for retention cutoffs
- Never parse a locale-formatted date back into a value; keep the machine format in the data and format for humans only at the last printf

## Building Output

- `printf` with a format is the only reliable emitter: `printf '%s\t%s\n' "$a" "$b"` — `echo` mangles values starting with `-` and interprets backslashes on some shells
- A format string is reused until arguments run out: `printf '%s\n' "${arr[@]}" ` prints one element per line, no loop
- Aligning columns for humans is `column -t`, not manual padding; keep the machine-readable TSV as the real output and pipe it through `column -t` only when the output is a TTY (`interactive.md`)
