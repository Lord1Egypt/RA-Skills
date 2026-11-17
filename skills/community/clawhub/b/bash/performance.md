# Performance — The Fork Cost Model

There is one cost model for shell scripts: **builtins are nearly free, external commands cost a process**. Everything slow in a Bash script is a fork you did not notice, usually inside a loop.

## Measure The Cost On Your Box First

```bash
time ( for i in $(seq 1 1000); do /bin/true; done )     # 1000 process spawns
time ( for i in $(seq 1 1000); do : ; done )            # 1000 builtin no-ops
```

Typical result on Linux: the first is around 0.5-1.5 s, the second is milliseconds; macOS and WSL spawn processes several times slower than Linux. Run it before optimizing — the ratio, not the absolute number, is what tells you whether a loop is worth rewriting.

Consequence with arithmetic you can check: a loop over a 10,000-line file that runs three external commands per line is 30,000 spawns ≈ 30 s at 1 ms each, while one `awk` pass over the same file is a single spawn.

## Fork Inventory (what actually costs a process)

| Costs a process | Free (builtin) |
|---|---|
| `$(cmd)`, backticks, `<(cmd)`, `>(cmd)` | `${var#…}`, `${var//…}`, `${#var}` |
| Every pipeline stage | `[[ … ]]`, `(( … ))`, `case` |
| `( subshell )` | `{ grouping; }` |
| `basename`, `dirname`, `expr`, `seq`, `cat`, `echo` when it is `/bin/echo` | parameter expansion, `printf` builtin, `read`, `mapfile` |
| `grep`/`sed`/`awk` invoked per line | the same tools invoked once over the whole stream |

- `$(< file)` reads a file with no fork; `$(cat file)` forks twice
- `printf -v var …` builds a string with no fork; `var=$(printf …)` forks
- A pipeline's stages run CONCURRENTLY, so `a | b | c` costs three spawns but overlaps their work — a pipeline is not the thing to eliminate, a per-iteration spawn is

## The Five Rewrites That Deliver

```bash
name=$(basename "$f")        → name=${f##*/}
dir=$(dirname "$f")          → dir=${f%/*}
n=$(expr "$n" + 1)           → n=$(( n + 1 ))
if echo "$s" | grep -q foo   → if [[ $s == *foo* ]]
cat file | grep p | awk '{…}'→ awk '/p/ {…}' file
```

- Sort and dedupe in one tool: `sort -u` instead of `sort | uniq`; `awk '!seen[$0]++'` when order must be preserved
- Load a file once: `mapfile -t lines < file` (`bash >=4.0`) rather than repeated `head`/`sed -n` calls over the same file
- Hoist invariants out of loops: `command -v jq` probes, `date` calls, and config reads belong before the loop, cached in a variable
- Memoize expensive lookups in an associative array: `[[ -n ${cache[$k]+x} ]] || cache[$k]=$(lookup "$k")` turns N calls into N-distinct calls

## Loop Or Stream

Rewrite a `while read` loop into a single `awk`/`sort` pass when the body is pure text transformation. Keep the loop when the body orchestrates commands (one `ssh`, one `curl`, one `convert` per item) — there the fork IS the work, and the lever is concurrency instead (`processes.md`).

Rough decision points, in items:

- Under ~1,000 items with a builtin-only body: the loop is fine, do not touch it
- ~1,000-10,000 items with one external command per item (the common middle case): stream it if the body is pure text; if the body IS the work (one `ssh`, `curl`, or `convert` per item), keep the loop and parallelize instead — `xargs -P` or a `wait -n` pool (`processes.md`). 5,000 items at 200 ms of network latency each is ~17 min serial, ~2 min at `-P 8`
- Over ~10,000 items with any external command per item: rewrite as a stream, or accept minutes
- Over ~100,000 items, or any join/group-by across two datasets: leave Bash (SKILL.md Core Rule 9) — `awk`, `sqlite3`, or a real language

## I/O Patterns

- Redirect the loop, not each write: `for …; do printf …; done > out` opens the file once; `printf … >> out` inside the loop reopens it every iteration
- Read once, write once. A loop that appends to a file and then greps it again per iteration is quadratic on disk as well as in forks
- `LC_ALL=C` speeds up `sort`, `grep`, and `awk` on ASCII data by skipping multibyte collation — often a large win on big files, and it also makes the order deterministic (`text-processing.md`)
- `grep -F` for fixed strings, and put the cheapest filter first in a pipeline so later stages see fewer lines
- `sort` on large inputs: give it memory and parallelism (`sort -S 25% --parallel=4`, GNU) rather than pre-splitting by hand

## Bash-Level Costs Worth Knowing

- Array reslicing (`q=("${q[@]:1}")`) copies the whole array: O(n) per pop, O(n²) for a queue drain — use an index cursor instead (`arrays.md`)
- Linear membership scans over a large indexed array are O(n) per lookup; an associative array makes it O(1)
- Very large arrays live in the shell's memory; check the real cost with `ps -o rss= -p $$` before assuming a million elements is fine
- `set -x` slows everything measurably and floods the log; never leave it enabled in a hot loop
- Startup cost matters for scripts called thousands of times (git hooks, xargs bodies): a script that sources a 500-line library pays that on every invocation

## Prove The Improvement

```bash
TIMEFORMAT='%R real  %U user  %S sys'
time ./script.sh big-input > /dev/null     # before and after, same input, same machine
```

- `$SECONDS` (builtin, whole seconds) times phases inside the script without a fork; `EPOCHREALTIME` (`bash >=5.0`) gives sub-second precision
- Time the whole script, not the fragment you suspect: the intuition about which line is slow is wrong often enough that measuring twice is cheaper than rewriting the wrong loop
- Stop when the runtime is no longer the constraint. A 200 ms script that runs once a day does not need any of this; a 200 ms git hook run 500 times a day does
