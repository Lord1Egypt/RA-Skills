# FairSplit CLI Reference

Full flag reference for `scripts/ledger.py`. Every subcommand also accepts
`--help`. All amounts are plain decimal strings (`"1200.50"`, not
pre-multiplied) -- the script handles the conversion to integer cents.

`--data-dir` is a global flag (goes *before* the subcommand) and defaults to
`$FAIRSPLIT_DATA_DIR`, or `~/.hermes/data/fairsplit` if that's unset. The
`fairsplit.data_dir` skill setting is injected into the agent's context, not
into the script's environment, so the agent should pass it explicitly on
every call. A leading `~` (and `$VARS`) in the path is expanded by the
script, so a quoted path works.

Amounts, weights, and `--fx-rate` must be finite decimal numbers. `add`
rejects zero or negative amounts and negative weights with a non-zero exit
and an `error:` line on stderr.

## `init`

Create a new group.

```bash
ledger.py init --group "Goa Trip" --currency INR --members "Alice,Bob,Priya" [--force]
```

- `--group` (required) -- display name; also used to derive the on-disk
  slug (`goa-trip.json`)
- `--currency` -- ISO 4217 code, default `USD`
- `--members` -- comma-separated starting members (optional; `add` and
  `add-member` can grow this list later)
- `--force` -- overwrite an existing group of the same name (**destroys**
  its expense history -- confirm with the user first)

## `add-member`

```bash
ledger.py add-member --group "Goa Trip" --member "Dev"
```

Adds someone to the group's member list with no expenses. Useful so they
show up in `balances` at zero even before they've paid for or owe anything.

## `add`

Record one expense.

```bash
ledger.py add --group "Goa Trip" \
  --payer Alice --amount 1000 --description "Dinner" \
  [--currency INR] [--fx-rate 1.0] \
  [--category food] [--date 2026-09-21] \
  [--participants "Alice,Bob,Priya"] \
  [--split equal|exact|shares|percent] [--detail "..."]
```

- `--payer` (required) -- who fronted the money. Auto-added to the group's
  member list if new.
- `--amount` (required) -- decimal string, in `--currency` (or the group's
  home currency if `--currency` is omitted)
- `--currency` -- the currency this particular expense was actually paid
  in. If it differs from the group's home currency, `--fx-rate` is
  required (home-currency units per 1 unit of this expense's currency).
  The original amount/currency/rate are kept on the record; everything
  downstream (balances, settlement) uses the converted, home-currency
  amount.
- `--participants` -- comma-separated; defaults to the whole group. Doesn't
  need to include the payer, but usually should if the payer also consumed
  a share.
- `--split`:
  - `equal` (default) -- even split; any leftover cent(s) from integer
    division go to participants in alphabetical order, one cent each, so
    the allocation is always reproducible
  - `exact --detail "Alice:300,Bob:300,Priya:300"` -- named amounts; must
    sum to `--amount` exactly (in the home currency) or the command fails
  - `shares --detail "Alice:1,Bob:2,Priya:1"` -- proportional integer or
    decimal weights; the *last* participant listed absorbs any rounding
    remainder (so shares always sum exactly to the total)
  - `percent --detail "Alice:60,Bob:40"` -- same mechanics as `shares`,
    weights don't strictly need to sum to 100 (they're normalized), but
    for sanity they generally should

## `undo`

```bash
ledger.py undo --group "Goa Trip" --id e4
```

Deletes one expense by its id (ids look like `e1`, `e2`, ... and are
printed by `add` and `history`). There's no separate "edit" -- undo, then
re-add with corrected numbers.

## `balances`

```bash
ledger.py balances --group "Goa Trip"
```

Prints each member's net position: positive means the group owes them
money, negative means they owe the group, zero means settled up for now.

## `settle`

```bash
ledger.py settle --group "Goa Trip"
```

Computes the minimum-payment settlement plan: at most `members - 1`
transactions that bring every balance to zero. See
`settlement-algorithm.md` for how this works.

## `history`

```bash
ledger.py history --group "Goa Trip" [--person Alice] [--category food] [--limit 10]
```

Lists expenses, most recent last. Filters combine with AND.

## `export`

```bash
ledger.py export --group "Goa Trip" --format md --out summary.md
ledger.py export --group "Goa Trip" --format csv --out expenses.csv
```

- `md` -- a human-readable summary: expense table + current balances
- `csv` -- one row per expense, for spreadsheets or archiving
- `--out` -- defaults to `<group-slug>-summary.md` / `<group-slug>-expenses.csv`
  in the current working directory if omitted

## `list-groups`

```bash
ledger.py list-groups
```

Lists every group found in the data directory, with currency, expense
count, and how many members currently have a nonzero balance.

## `fx`

```bash
ledger.py fx --base USD --quote INR
```

Best-effort, keyless lookup against Frankfurter's ECB-backed rate API. Only
needed if you want a live rate to feed into `add --fx-rate`. Both codes must be three-letter ISO 4217 codes (case
doesn't matter). It's entirely
optional and the rest of the skill works fine without network access. If it
fails (no network, rate limited, currency not covered), just ask the user
for the rate.

## Recording a settle-up payment

When someone actually pays back what they owe, record it as an expense paid
by the sender, with the recipient as the only participant:

```bash
ledger.py add --group "Goa Trip" --payer Priya --amount 241.66 \
  --participants Alice --description "Settle-up" --category settlement
```

This moves both balances toward zero; `settle` then shows whatever is
still outstanding.

## Recurring splits (e.g. monthly rent)

FairSplit itself doesn't schedule anything -- it's a plain CLI, so
recurring expenses go through Hermes's own cron system rather than a
feature of the skill:

```bash
hermes cron create \
  --schedule "0 9 1 * *" \
  --prompt "Use the fairsplit skill: add this month's rent (₹30000, equal split) to the 'Flat 4B' group, then post the current settle-up plan to this chat." \
  --skill fairsplit
```

That's a normal cron job pointed at a normal prompt -- nothing
FairSplit-specific is needed beyond telling the agent which skill and what
to do each run.
