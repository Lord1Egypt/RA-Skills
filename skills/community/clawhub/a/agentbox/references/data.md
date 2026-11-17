# Data: extract and table

Use this to pull prices, tables, dates, people, links, numbers or emails out of docs, and to filter or sort them.
Extraction is rule-based. It never guesses: check `raw` and `context` before you cite a value.

## Extract

```bash
agentbox extract doc:1 --kind prices
agentbox extract doc:1 doc:2 doc:3 --kind prices --save-table
agentbox extract --from doc:1,doc:2 --kind tables
agentbox extract doc:2 --kind dates --grep 2025
agentbox extract doc:3 --kind people --grep CEO
agentbox extract doc:4 --kind links --site github.com
agentbox extract doc:1 --kind numbers --section 2 --limit 10
agentbox extract report.md --kind emails
```

| `--kind` | Fields in each item |
|---|---|
| `prices` | `value`, `currency`, `period` (month/year), `per` (user/seat), `raw` |
| `tables` | `table` (a `tbl:N`), `title`, `headers`, `rows_count`, `preview` |
| `dates` | `date` (ISO), `precision`, `ambiguous`, `raw` |
| `people` | `name`, `role`, `org`, `confidence` |
| `links` | `text`, `url` |
| `numbers` | `value`, `unit`, `raw` |
| `emails` | `email` |

Every item also has `doc`, `url`, `section`, `line` and `context`. Cite `url`.

- `--save-table` stores all items as `tbl:N` (in `data.table`).
- `--kind tables` stores each table found as its own `tbl:N`.
- `data.total` counts all items; `data.returned` how many are shown. If `truncated` is true, narrow with `--grep` or `--section`.
- `people` matching is a pattern, not real name recognition. Confirm each name and role in `context`.
- `$` is read as USD unless the site's country says otherwise. Check `raw`.

## Table

```bash
agentbox table show tbl:1
agentbox table query tbl:1 --where "Price < 100" --sort -Price --limit 5
agentbox table query tbl:1 --where "per = user" --where "period = month" --sort value --select value,raw,url
agentbox table query tbl:1 --group-by currency --agg "count,avg:value,max:value"
agentbox table query tbl:1 --where "Region = EU" --save
agentbox table import vendors.csv
agentbox table export tbl:2 --out cheapest.md --apply
agentbox table query tbl:1 --format md
```

`--where` syntax: `COLUMN OP VALUE`. OP is one of `=`, `!=`, `<`, `<=`, `>`, `>=`, `contains`, `startswith`.

- Quote the whole condition: `--where "Price < 100"`.
- Repeat `--where` to AND conditions. There is no OR; run two queries.
- Cells like `$1,299/yr`, `€9,99`, `1.2萬` compare as numbers. Dates compare by calendar order. Text compares case-insensitively.
- `--sort Price` is ascending, `--sort -Price` descending. Empty or text cells sort last.
- `--agg` takes `count`, `sum:COL`, `avg:COL`, `min:COL`, `max:COL`. Result columns are named like `avg_value`.
- Order is always: where, group, sort, select.
- Column names are forgiving (`price usd` finds `Price (USD)`). On `unknown_column`, use a name from the error message.

Output: `table query` returns `data.columns`, `data.rows[]`, `data.row_count`. `table show` returns `data.columns[]` with inferred `type`.
`--format md` prints a Markdown table you can paste into a report. `--format csv` prints CSV.
