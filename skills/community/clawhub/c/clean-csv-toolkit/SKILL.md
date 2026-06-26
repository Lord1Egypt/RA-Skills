---
name: clean-csv-toolkit
description: Local CSV / TSV / JSONL inspection and cleanup toolkit. Profile, validate, deduplicate, diff, preview (head/tail/random sample), filter with a safe predicate language, sort, concat, merge (inner/left/right/outer joins), pivot (group-by aggregations + wide cross-tabs), transform (derived columns with safe expression evaluator: profit = revenue - cost, name = upper(first) + last, year(date), coalesce()), and convert between csv/tsv/jsonl/json/markdown. Pure Python 3 standard library, no pandas, no remote calls. Handles 100k+ rows in under 1 second.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit"}}
---

# clean-csv-toolkit

v0.5.0

A small honest toolkit for the work agents end up doing constantly: read a CSV someone sent you, work out what's in it, clean it up, and forward only the safe rows downstream. Built on Python 3 standard library only. No `pandas`, no `numpy`, no pip installs, no remote calls.

## What this skill does

- `scripts/inspect.py` — profile a `.csv` / `.tsv` / `.jsonl` file: row count, auto-detected column types (`int`, `float`, `bool`, `date`, `datetime`, `string`, `empty`), null counts per column, distinct value counts (capped), three sample values per column, file size, and detected encoding.
- `scripts/validate.py` — check the file against a small JSON schema (required columns, per-column type, min/max, enum, regex, unique). Exits 0/1 so it slots into CI.
- `scripts/dedupe.py` — remove duplicate rows by full-row match or by key columns. Optional `--keep first|last`, `--case-insensitive`, `--trim`, and a JSONL report of every removed row.
- `scripts/diff.py` — compare two files by key column(s) and classify every row as added / removed / changed / unchanged, with a per-column before/after diff for changed rows.
- `scripts/convert.py` — convert between CSV, TSV, JSON Lines, JSON array, and GitHub-flavored Markdown table.
- `scripts/head.py` (NEW in v0.2.0) — print the first N rows in csv / tsv / jsonl / md / aligned format, with optional column subset.
- `scripts/tail.py` (NEW in v0.2.0) — print the last N rows using a streaming ring buffer (works on multi-gigabyte files without loading them).
- `scripts/sample.py` (NEW in v0.2.0) — pick a uniformly random sample of N rows via reservoir sampling. Single-pass, O(N) memory, optional `--seed` for reproducibility, optional `--preserve-order` to keep original row order.
- `scripts/merge.py` (NEW in v0.3.0) — join two files on one or more key columns. Supports `inner` / `left` / `right` / `outer` joins, separate key names per side via `--left-on` and `--right-on`, and duplicate-column disambiguation via `--suffix-left` / `--suffix-right`. Streams the LEFT side, indexes the RIGHT side (peak memory ≈ size of right file).
- `scripts/pivot.py` (NEW in v0.3.0) — group-by aggregations and wide pivot tables. Aggregations: `count`, `sum`, `avg`/`mean`, `min`, `max`, `first`, `last`, `nunique`. Set `--pivot-on COL` to produce a wide cross-tab (e.g. region × product, sum of revenue). Numeric-aware `--sort-by` so `--sort-by revenue_sum --desc` orders correctly.
- `scripts/filter.py` (NEW in v0.4.0) — keep rows that match a safe predicate (`amount > 100`, `status in pending,approved`, `email =~ @example\.com$`, `name is_not_empty`). Supports `==`, `!=`, `<`, `<=`, `>`, `>=`, `=~` (regex), `in`, `contains`, `is_empty` / `is_not_empty` / `is_number` / `is_not_number`. `and` / `or` / parentheses / `not`. NO Python eval — a hand-rolled tokenizer + recursive-descent parser. Optional `--invert`, `--limit`, `--columns`.
- `scripts/sort.py` (NEW in v0.4.0) — stable, type-aware sort. Auto-detects which columns are numeric and sorts them numerically (so `1200 > 899 > 100 > 50`, not `"50" > "1200"`). Per-column direction with `--by amount:desc,region:asc`. Optional `--case-insensitive`, `--limit`, `--numeric` (force numeric on all sort cols).
- `scripts/concat.py` (NEW in v0.4.0) — stack files vertically (UNION ALL). Default mode unions the headers of all inputs; `--strict` requires identical headers; `--add-source COL` tags each row with its source filename; `--dedupe` drops exact-duplicate rows across inputs. Streams one file at a time.
- `scripts/transform.py` (NEW in v0.5.0) — add, modify, rename, drop, cast, or keep columns. Derived columns via a safe expression language (no `eval`): `--add 'profit = revenue - cost'`, `--add 'full_name = upper(first) + " " + upper(last)'`, `--add 'year = year(signup_date)'`, `--add 'safe = coalesce(value, default)'`. Built-in functions: upper, lower, strip, len, abs, round, int, float, str, replace, split, join, coalesce, year, month, day. Chainable with `--cast COL:int|float|bool|string`, `--rename OLD=NEW`, `--drop COL[,...]`, `--keep COL[,...]`.
- `scripts/check_deps.sh` — verify `python3` is available.

## What this skill does not do

- It does not call any LLM, web service, or remote API.
- It does not load a full dataframe into memory just to do simple structural work; the helpers stream rows where possible.
- It does not write outside the input/output paths the caller provides.
- It does not do statistical analysis (mean, percentile, correlation). For that, use a dataframe library.
- It does not parse Excel files (.xls / .xlsx). Export to CSV first.

## Required dependencies

```bash
bash scripts/check_deps.sh
```

Only `python3` is required. The skill uses `csv`, `json`, `re`, `pathlib`, `argparse`, `datetime`, `collections` — all stdlib.

## Workflows

### 0. Quickly preview an unknown CSV (NEW in v0.2.0)

```bash
# First 10 rows in a clean aligned table
python3 scripts/head.py mystery.csv

# Last 5 rows of a multi-GB log
python3 scripts/tail.py huge.csv -n 5

# A reproducible random sample for spot-checking
python3 scripts/sample.py customers.csv -n 20 --seed 42

# Preview only specific columns
python3 scripts/head.py customers.csv --columns id,email,status

# Emit a previewable Markdown table for an agent's reply
python3 scripts/head.py customers.csv -n 5 --as md
```

All three scripts accept `-n N`, `--as csv|tsv|jsonl|md|aligned`, `--output file`, and `--columns col1,col2,...`. `sample.py` additionally accepts `--seed INT` and `--preserve-order`. Default output format is `aligned` — a fixed-width text table sized to the actual data, which is what an agent usually wants to show inline. Default `N` is 10.

Streaming guarantees:
- `head.py` reads at most N+1 rows from the file.
- `tail.py` keeps a bounded `deque(maxlen=N)` and emits only the last N rows.
- `sample.py` uses reservoir sampling (algorithm R): single pass, O(N) memory regardless of file size.

On a 100,000-row / 1.6 MB CSV: `head -n 3` runs in ~50 ms, `tail -n 3` in ~180 ms, `sample -n 5` in ~260 ms.

### 1. Profile an unknown CSV

```bash
python3 scripts/inspect.py customers.csv
```

Output:

```
file:      /path/customers.csv
size:      284 B (284 bytes)
encoding:  utf-8
kind:      csv
rows:      5
columns:   6

  #  name                          type           nulls   null%    distinct  sample
----------------------------------------------------------------------------------------------------
  1  id                            int                0    0.00           5  '1', '2', '3'
  2  email                         string             0    0.00           5  'alice@example.com', ...
  3  name                          string             0    0.00           5  'Alice', 'Bob', 'Carol'
  4  amount                        float              1   20.00           4  '42.50', '100.00', '7.25'
  5  status                        string             0    0.00           3  'approved', 'pending', ...
  6  signup_date                   date               0    0.00           5  '2025-01-15', ...
```

Pass `--json` for machine-readable output that pipes into other tools.

The script auto-detects the dialect (CSV vs TSV vs JSON Lines) and a sensible encoding (`utf-8`, `utf-8-sig`, `cp1252`, `latin-1`). Type inference takes up to 1000 non-empty values per column and picks the most specific type that fits all of them.

### 2. Validate against a schema

Write a `schema.json`:

```json
{
  "required_columns": ["id", "email", "amount", "status"],
  "columns": {
    "id":     {"type": "int", "required": true, "unique": true, "min": 1},
    "email":  {"type": "string", "required": true, "regex": ".+@.+\\..+"},
    "amount": {"type": "float", "min": 0, "max": 100000},
    "status": {"type": "string", "enum": ["pending", "approved", "rejected"]},
    "signup_date": {"type": "date"}
  }
}
```

Then:

```bash
python3 scripts/validate.py customers.csv --schema schema.json
```

A clean file exits 0 with `verdict: pass`. A bad file exits 1 with a detailed error table:

```
   row  column                  kind                    detail
------------------------------------------------------------------------------------------------
     2  email                   regex_mismatch          value did not match regex | value='not-an-email'
     2  amount                  bad_type                value does not match type 'float' | value='abc'
     3  amount                  below_min               value -50.0 < min 0 | value='-50.00'
     3  status                  not_in_enum             value not in allowed set | value='unknown_status'
     4  id                      duplicate_unique        value already seen earlier in this column | value='1'
```

Pass `--json` for a structured report and `--max-errors N` to cap collection on huge files.

### 3. Remove duplicates

By full-row match (any two rows identical in every column):

```bash
python3 scripts/dedupe.py messy.csv clean.csv
```

By a key column (only one canonical row per `id`):

```bash
python3 scripts/dedupe.py messy.csv clean.csv --key id \
  --removed-report removed.jsonl
```

`--keep first` (default) keeps the earlier-occurring row; `--keep last` keeps the later one — useful when later rows are corrections. `--case-insensitive` and `--trim` normalise key values before comparison so `" alice@example.com"` and `"ALICE@example.com"` collapse to one row.

The `--removed-report` writes one JSON object per removed row, with the original 1-based row index, the key tuple that was duplicated, and the full row, so the dedup decision is auditable.

### 4. Diff two files

```bash
python3 scripts/diff.py customers_old.csv customers_new.csv --key id
```

Output:

```
added:      1
removed:    1
changed:    1

--- ADDED (1) ---
  + 6
--- REMOVED (1) ---
  - 4
--- CHANGED (1) ---
  ~ 2
      amount: '100.00' -> '150.00'
      status: 'pending' -> 'approved'
```

Multi-column keys are supported: `--key customer_id,date`. Exit codes are 0 if the files are identical on the key columns, 1 if they differ — so this also works as a CI guard ("fail the build if the snapshot file changed").

### 5. Convert between formats

```bash
python3 scripts/convert.py data.csv data.jsonl       # row -> JSON Lines
python3 scripts/convert.py data.jsonl data.csv       # back
python3 scripts/convert.py data.csv data.json --pretty
python3 scripts/convert.py data.csv data.md          # GitHub-flavored table
python3 scripts/convert.py data.tsv data.csv         # delimiter change
```

Output format is picked from the extension. Allowed extensions: `.csv`, `.tsv`, `.jsonl`, `.json`, `.md`. The Markdown writer escapes `|` and `\n` in cell values so the table stays well-formed.

### 6. Join two files (NEW in v0.3.0)

```bash
# Inner join: only users with at least one order
python3 scripts/merge.py users.csv orders.csv joined.csv \
    --left-on id --right-on user_id

# Left join: keep every user, fill unmatched with empty strings
python3 scripts/merge.py users.csv orders.csv left.csv \
    --left-on id --right-on user_id --how left

# Same key name on both sides: --on shorthand
python3 scripts/merge.py users.csv orders.csv out.csv --on user_id

# Outer join into JSON Lines, machine-readable summary on stdout
python3 scripts/merge.py a.csv b.csv full.jsonl --on key --how outer --json
```

Duplicate non-key columns are auto-renamed with `--suffix-left` / `--suffix-right` (defaults `_x` / `_y`).

### 7. Group-by aggregations and wide pivots (NEW in v0.3.0)

```bash
# Sum revenue per region
python3 scripts/pivot.py sales.csv by_region.csv \
    --group-by region --agg revenue:sum --sort-by revenue_sum --desc

# Multiple aggregations per group
python3 scripts/pivot.py sales.csv detail.csv \
    --group-by region,product \
    --agg "units:sum,revenue:sum,revenue:avg,product:nunique"

# Wide cross-tab: region × product matrix of revenue
python3 scripts/pivot.py sales.csv crosstab.csv \
    --group-by region --pivot-on product --agg revenue:sum --fill 0

# Same wide pivot rendered as Markdown for a report
python3 scripts/pivot.py sales.csv crosstab.md \
    --group-by region --pivot-on product --agg revenue:sum --fill "-"
```

Aggregation functions: `count`, `sum`, `avg`/`mean`, `min`, `max`, `first`, `last`, `nunique`. Output column names follow `<col>_<func>` (e.g. `revenue_sum`). `--sort-by` is numeric-aware: numeric columns are ordered numerically, string columns lexicographically.

### 8. Filter rows (NEW in v0.4.0)

```bash
# Numeric comparison
python3 scripts/filter.py orders.csv big.csv --where "amount > 100"

# Combine boolean conditions
python3 scripts/filter.py orders.csv top.csv \
    --where "status == approved and amount >= 50"

# Set membership (commas are part of the value, not separators)
python3 scripts/filter.py users.csv targeted.csv \
    --where "country in IN,US,UK and signup_year >= 2024"

# Regex match
python3 scripts/filter.py users.csv company.csv \
    --where 'email =~ @example\.com$'

# Null / type checks (no right-hand side)
python3 scripts/filter.py users.csv missing.csv --where "phone is_empty"

# Invert the predicate, write only specific columns, cap at N matches
python3 scripts/filter.py log.csv non_errors.csv \
    --where "level == ERROR" --invert --columns ts,msg --limit 1000
```

The expression language is deliberately small and is parsed by a hand-rolled tokenizer + recursive-descent parser. There is no `eval`, no shell, no subprocess.

### 9. Sort by one or more columns (NEW in v0.4.0)

```bash
# Auto-numeric sort, descending
python3 scripts/sort.py sales.csv s.csv --by amount:desc

# Multi-key: country ascending, signup_date descending (stable)
python3 scripts/sort.py users.csv s.csv --by country:asc,signup_date:desc

# Top 10 by revenue
python3 scripts/sort.py sales.csv top10.csv --by revenue:desc --limit 10

# Case-insensitive string sort
python3 scripts/sort.py contacts.csv s.csv --by name --case-insensitive
```

Each `--by` column is treated numerically when every value parses as a number, otherwise string. `--numeric` forces numeric on all sort columns (non-numeric rows sort last).

### 10. Concatenate multiple files (NEW in v0.4.0)

```bash
# Stack monthly shards into one CSV (header union)
python3 scripts/concat.py all_quarter.csv jan.csv feb.csv mar.csv

# Strict mode: require every input to have an identical header
python3 scripts/concat.py all.csv jan.csv feb.csv mar.csv --strict

# Tag each row with the source filename (without extension)
python3 scripts/concat.py tagged.csv shard_*.csv --add-source origin --source-stem

# Stack + drop duplicate rows across files
python3 scripts/concat.py all.csv jan.csv feb.csv apr.csv --dedupe
```

### 11. Transform columns (NEW in v0.5.0)

```bash
# Add a derived column
python3 scripts/transform.py orders.csv with_profit.csv \
    --add 'profit = revenue - cost'

# Multiple --add operations + cast + final column selection
python3 scripts/transform.py sales.csv clean.csv \
    --add 'profit = revenue - cost' \
    --add 'margin_pct = round(profit / revenue * 100, 1)' \
    --add 'name = lower(strip(first_name)) + "_" + lower(strip(last_name))' \
    --add 'signup_year = year(signup)' \
    --cast revenue:float --cast cost:float \
    --keep id,name,country,revenue,profit,margin_pct,signup_year

# Rename and drop
python3 scripts/transform.py users.csv clean.csv \
    --rename 'signup=joined_date' --drop password_hash

# Boolean comparisons produce 0/1 columns
python3 scripts/transform.py orders.csv flagged.csv \
    --add 'is_high_value = amount > 1000'

# Fallback for missing values
python3 scripts/transform.py users.csv filled.csv \
    --add 'safe_email = coalesce(email, "unknown@example.com")'
```

The expression language is intentionally small: arithmetic (`+ - * / %`), string concat (`+`), comparisons (`== != < <= > >=` → yield 0/1), parentheses, identifiers (column references), string and number literals, and function calls. **No `eval`, no `subprocess`, no shell.** Empty cells that propagate into arithmetic leave the derived value empty for that row instead of crashing the pipeline.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success / validation pass / files identical |
| 1 | validation fail / files differ / no rows in input |
| 2 | bad arguments / unsafe path / missing input / unsupported extension / schema malformed |

This 0/1/2 split is consistent across all five scripts, so they slot into shell pipelines cleanly:

```bash
python3 scripts/validate.py incoming.csv --schema schema.json \
  && python3 scripts/dedupe.py incoming.csv clean.csv --key id \
  && python3 scripts/inspect.py clean.csv
```

## Safety properties

- Pure Python 3 standard library. No third-party dependencies.
- No `subprocess` calls. No shell invocation.
- All file paths are validated against a strict allowlist regex that rejects shell metacharacters (`;`, `|`, `&`, `>`, `<`, `$`, `` ` ``, backslash-newline, etc.).
- Scripts only read the input paths the caller provides and write to the output paths the caller provides. No temp files outside the system's tempdir.
- All inputs and outputs use UTF-8 by default; CSV reads auto-fall-back through utf-8-sig, cp1252, and latin-1 when the file's encoding is non-UTF-8.
- Deterministic: the same input produces the same output every time.

## Performance

- `inspect.py` profiles 10,000 rows in well under one second on a single core (single-pass streaming read).
- All scripts stream rows; they do not load the entire file into memory for processing. The exception is `dedupe.py` and `diff.py`, which build an in-memory dict keyed by row identity — fine for hundreds of thousands of rows on a typical laptop.
- No background threads, no process pool, no caching.

## Known limitations

- Type inference uses regex-shape matching, not locale-aware parsing. `"1,234.56"` is detected as `string`, not `float`. Re-export with a different number format if you need different inference.
- The Markdown writer flattens multi-line cells to single lines (newlines become spaces).
- JSON Lines input must have one JSON object per line. Multi-line JSON arrays are not supported; use the regular CSV/JSONL pipeline.

## v0.5.0 changes

- Added `scripts/transform.py`: derived columns + schema operations. Hand-rolled tokenizer + recursive-descent parser (no `eval`, no subprocess) supports arithmetic (+/-/* / / %), string concat (+), parentheses, function calls, and boolean comparisons that yield 0/1. Built-in functions: upper, lower, strip, len, abs, round, int, float, str, replace, split, join, coalesce, year, month, day. Six op kinds: `--add`, `--set`, `--drop`, `--rename`, `--cast`, `--keep`. Schema is computed symbolically before the streaming pass, so empty cells in arithmetic columns don't crash the whole pipeline — they just leave the derived value empty for that single row.
- Bug fixed during testing: the schema-detection pass was running expressions against an empty-string row, which broke arithmetic. Replaced with a purely-structural schema walk.

## v0.4.0 changes

- Added `scripts/filter.py`: safe-predicate row filter. Hand-rolled tokenizer + recursive-descent parser, NO `eval` and no `subprocess`. Numeric and string compare, regex (`=~`), `in COMMA,LIST`, `contains`, `is_empty` / `is_not_empty` / `is_number` / `is_not_number`. Boolean `and` / `or` / `not` with parentheses. `--invert`, `--limit`, `--columns`.
- Added `scripts/sort.py`: type-aware stable sort with per-column direction (`--by amount:desc,region:asc`). Auto-detects numeric columns. Optional `--case-insensitive`, `--limit`, `--numeric`. 100k rows sorted in ~0.3 s.
- Added `scripts/concat.py`: vertical UNION ALL of multiple CSV / TSV / JSONL files. Header union by default, `--strict` for exact-match check, `--add-source` to tag rows, `--dedupe` to drop exact-duplicate rows. Streams one input at a time, memory does not grow with the number of inputs (unless `--dedupe` is set).
- All three scripts honor the existing safe-path policy and the 0 / 1 / 2 exit-code contract.

## v0.3.0 changes

- Added `scripts/merge.py`: join two CSV / TSV / JSONL files on one or more key columns. Supports inner, left, right, outer joins; separate key names per side; duplicate-column suffixing; CSV / TSV / JSONL output. Single-pass over LEFT, peak memory ≈ size of RIGHT. Merged 50k × 200k rows in ~1.3 s.
- Added `scripts/pivot.py`: group-by aggregations and wide pivot tables. Functions: count, sum, avg, min, max, first, last, nunique. Wide mode produces region × product cross-tabs. Numeric-aware sort. Streamed 100k rows in ~0.7 s.
- All new scripts honor the existing safe-path policy (no shell metacharacters), use exit code 2 for bad arguments / missing files / missing columns, exit 1 for empty results, exit 0 for success. Output extension is validated against an explicit allow-list per script.

## v0.2.0 changes

**Three new preview helpers** (`head.py`, `tail.py`, `sample.py`):

- `head.py` and `tail.py` give shell-style preview that is format-aware and never mangles quoting the way a naive `head` / `tail` would. They auto-detect dialect (csv/tsv/jsonl), let you pick the output format with `--as`, and can re-emit any subset of columns with `--columns`.
- `sample.py` runs reservoir sampling (algorithm R): a single streaming pass, O(N) memory regardless of file size. `--seed INT` makes the sample reproducible so it slots into test suites and CI; `--preserve-order` re-sorts the reservoir back into original row order.
- All three share the same `--as csv|tsv|jsonl|md|aligned`, `--output`, and `--columns` flags, mirroring the convention already used by `convert.py`.
- Default output format is `aligned`, a fixed-width text table that an agent can paste straight into a reply.

**Performance**: on a 100,000-row / 1.6 MB CSV, `head` runs in ~50 ms, `tail` in ~180 ms, `sample` in ~260 ms.

**No breaking changes**: every v0.1.0 CLI flag, output format, and exit-code contract is preserved.

## License

MIT. See `LICENSE`.
