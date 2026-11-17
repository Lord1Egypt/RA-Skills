# Arrays and Maps — Lists, Sets, Counters

Bash has exactly two containers: indexed arrays and associative arrays (`bash >=4.0`). There is no nesting — an array of arrays does not exist. When the data needs a second dimension, either flatten the key (`map["$host:$port"]`) or leave Bash (SKILL.md Core Rule 9).

## The Trap List

- `arr=($(cmd))` splits on whitespace AND globs — `mapfile -t arr < <(cmd)` (bash >=4.0); on 3.2, `while IFS= read -r l; do arr+=("$l"); done < <(cmd)`
- `mapfile` without `-t` keeps a trailing `\n` on every element — always `-t`
- Associative arrays need `declare -A` (bash >=4.0) — without it, string keys silently evaluate to index 0 and overwrite each other
- Associative iteration order is unspecified — sort `"${!map[@]}"` when output must be stable
- `${#arr}` is the length of element 0 — `${#arr[@]}` is the count
- Unquoted `${arr[@]}` splits and globs — always `"${arr[@]}"`; keys: `"${!arr[@]}"`
- Empty array + `set -u`: `"${arr[@]}"` errors on bash <4.4 — portable guard: `${arr[@]+"${arr[@]}"}`
- `arr+=(item)` appends an element — `arr+=item` string-appends to element 0, no error
- `for i in {1..$n}` — brace expansion runs before variable expansion, you get the literal `{1..3}` — use `for ((i=1; i<=n; i++))`
- `unset arr[2]` — quote it: `unset 'arr[2]'`, or a file named `arr2` glob-matches; the index gap stays, indices never shift
- Sparse gaps: `copy=("${arr[@]}")` re-indexes 0..n and loses original indices — iterate `"${!arr[@]}"` if indices carry meaning
- `${arr[-1]}` needs bash >=4.3 — portable last element: `${arr[@]: -1}` (the space is required; without it `:-` becomes default-value syntax)
- Slices: `${arr[@]:1:2}` — elements 1 and 2; works on `$@` too: `"${@:2}"` = args from the 2nd on
- Expansions apply per element: `"${arr[@]%.txt}"` strips the suffix from every element
- Arrays cannot be exported: the environment holds strings only, so `export arr` passes nothing to a child process. Serialize with `${arr[@]@A}` (bash >=4.4) or pass the elements as arguments

## Associative Arrays In Practice

```bash
declare -A count                       # in a function: local -A count
while read -r ip _; do
  count["$ip"]=$(( ${count["$ip"]:-0} + 1 ))   # :-0 makes the first hit work
done < access.log
for ip in "${!count[@]}"; do printf '%d %s\n' "${count[$ip]}" "$ip"; done | sort -rn | head
```

- Quote the key on every access: `${map["$k"]}`. An unquoted key containing spaces or `*` is re-parsed, and `map[*]`/`map[@]` are the whole-array forms — a key literally named `@` is unreachable
- Existence vs emptiness: `[[ -n ${map[$k]+x} ]]` is true for a key set to the empty string; `[[ -n ${map[$k]:-} ]]` is not. `[[ -v map[$k] ]]` reads better wherever the array form of `-v` is available
- Empty keys are legal and invisible in output — validate keys before inserting when they come from parsed input
- Deleting: `unset 'map[key]'`; clearing all: `map=()` keeps the `-A` attribute, `unset map` destroys it

## Sets, Dedup, and Membership

- A set is an associative array with dummy values: `declare -A seen; seen["$x"]=1; [[ -n ${seen[$x]+x} ]]`
- Membership on an INDEXED array costs a linear scan — the loop is fine for tens of items, wrong for thousands (`performance.md`)
- One-line membership without a loop, exact-match safe:
  ```bash
  in_array() { local n=$1; shift; local e; for e in "$@"; do [[ $e == "$n" ]] && return 0; done; return 1; }
  in_array "$host" "${allowed[@]}"
  ```
- Dedup preserving order: feed a `seen` map. Dedup without order: `mapfile -t uniq < <(printf '%s\n' "${arr[@]}" | sort -u)` — one fork, and it breaks on elements containing newlines (use `sort -zu` with `mapfile -d ''`, bash >=4.4)

## Sorting

- Bash has no sort builtin. Route through `sort` and read back with `mapfile`:
  ```bash
  mapfile -t sorted < <(printf '%s\n' "${arr[@]}" | sort -V)   # -V version order, -n numeric, LC_ALL=C for byte order
  ```
- Sorting a map by value: emit `value<TAB>key` lines, `sort -k1,1nr`, read back. Trying to sort in place with nested loops is how a 200-line Bash script starts

## Stacks, Queues, and Argument Lists

- Stack: `stack+=("$x")` to push; `top=${stack[-1]}; unset 'stack[-1]'` to pop (bash >=4.3)
- Queue: `head=${q[0]}; q=("${q[@]:1}")` — the reslice is O(n), acceptable for hundreds of items, not for a hot loop
- Positional parameters are the third array: `set -- a b c` replaces them, `shift` consumes, `"$@"` forwards. That is the portable stack on bash 3.2
- Command builders (`opts=(--flag val)` then `cmd "${opts[@]}"`) are SKILL.md Core Rule 3 — the single highest-value use of arrays in scripts

## Functions and Arrays

- By value: `f "${arr[@]}"` then `local items=("$@")` — copies, safe, works on 3.2
- By reference: `f arr` then `local -n ref=$1` (bash >=4.3). The nameref must not share the caller's variable name or bash errors with "circular name reference" — prefix parameters (`local -n _ref=$1`) to avoid the collision
- Returning an array: assign into a nameref, or print one element per line and let the caller `mapfile`. Never echo elements space-separated — that re-creates the splitting bug the array existed to prevent
- `declare -p arr` prints the exact reconstruction, attributes included: the fastest way to see whether an element really contains what you think
