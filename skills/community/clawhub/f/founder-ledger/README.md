# founder-ledger

A one-file income ledger and milestone registry for solo founders tracking
their way to their first $1,000. No accounts, no SaaS, no dependencies —
one Python file, one JSON file for your data.

```
python3 founder_ledger.py add 5 "First sale, a t-shirt design" --source shop
python3 founder_ledger.py add 45 "Freelance logo gig deposit" --source client
python3 founder_ledger.py status
```

## Why

Most "revenue tracker" advice for a brand-new solo founder is either a
spreadsheet template you have to set up yourself, or a SaaS product with a
login, a subscription plan, and a database you don't control. This is neither: a
single `.py` file you can read top to bottom in five minutes, that stores
your numbers in a single JSON file next to it. Copy it into any project
directory and it works.

## Install

There is nothing to install. `founder_ledger.py` uses only the Python 3
standard library.

Clone the repo (group members) or install this skill via ClawHub, then
run it directly:

```
python3 founder_ledger.py status
```

## Usage

```
python3 founder_ledger.py add <amount> <description> [--date YYYY-MM-DD] [--source NAME]
python3 founder_ledger.py list [--json]
python3 founder_ledger.py status [--json]
python3 founder_ledger.py undo
```

Data is stored in `./ledger.json` by default. Point at a different file with
`--file path/to/file.json` or the `LEDGER_FILE` environment variable — handy
if you're tracking more than one side project from the same shell.

## Demo

```
$ python3 founder_ledger.py status
total revenue: $0
entries: 0
[------------------------------] 0.0%

milestone registry:
  [ ] $1        not yet
  [ ] $10       not yet
  [ ] $50       not yet
  [ ] $100      not yet
  [ ] $250      not yet
  [ ] $500      not yet
  [ ] $1000     not yet

$ python3 founder_ledger.py add 5 "demo" --date 2026-09-01
added 5.00 on 2026-09-01 -- demo
total: 0 -> 5.00
milestone reached: $1 (on 2026-09-01)

$ python3 founder_ledger.py status
total revenue: $5.00
entries: 1
[------------------------------] 0.5%

milestone registry:
  [x] $1        reached 2026-09-01
  [ ] $10       not yet
  [ ] $50       not yet
  [ ] $100      not yet
  [ ] $250      not yet
  [ ] $500      not yet
  [ ] $1000     not yet

$ python3 founder_ledger.py undo
removed: 5.00 on 2026-09-01 -- demo
note: any milestone already reached stays recorded in the registry.

$ python3 founder_ledger.py status
total revenue: $0
entries: 0
[------------------------------] 0.0%

milestone registry:
  [x] $1        reached 2026-09-01
  [ ] $10       not yet
  [ ] $50       not yet
  [ ] $100      not yet
  [ ] $250      not yet
  [ ] $500      not yet
  [ ] $1000     not yet
```

## Design notes

- **Money is `Decimal`, never `float`.** Amounts are quantized to cents on
  entry, so totals never drift from rounding error.
- **The ledger is append-only.** `undo` removes only the most recent entry
  (for fixing a typo right after you make it) — it never rewrites an
  arbitrary earlier row.
- **The milestone registry is a permanent record, not a live query.** Once
  your running total first crosses $1, $10, $50, $100, $250, $500, or
  $1,000, that crossing (amount, date, which entry caused it) is frozen in
  the registry forever. If you later `undo` an entry and your total drops
  back below a threshold, the milestone stays recorded — your first dollar
  stays your first dollar even if that sale is later reversed. This mirrors
  how you'd want your own "first dollar" story to work: it's a fact about
  what happened, not a number that un-happens if the running total dips.

## Status and falsifier

This is a v1 micro-tool, published to see if it's actually useful to anyone
outside the project that built it. **Falsifier: if this tool has not earned
at least $1 (e.g. a tip, a paid feature request, a "buy me a coffee") or
reached at least 200 stars/installs within 30 days of being published, it
gets archived rather than iterated on further.** That clock starts on the
date this tool is first made publicly reachable (repo visibility flip, or
this ClawHub listing going live) — see
[`docs/provenance.md`](docs/provenance.md) for that date once set, and for
how this was built.

## Support

Found this useful? Tips appreciated: https://buy.stripe.com/7sY28tct7g0r5vQ0QbabK00
(pay what you want, USD 1.00 minimum) — never required.

## License

MIT — see [`LICENSE`](LICENSE).
