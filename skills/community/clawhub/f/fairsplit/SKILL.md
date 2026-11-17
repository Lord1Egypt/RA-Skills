---
name: fairsplit
description: Split group expenses and settle up in the fewest payments.
version: 1.0.0
author: Himadri Ganguly
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [finance, expenses, group, roommates, travel, settlement, money]
    category: finance
    requires_toolsets: [terminal]
    config:
      - key: fairsplit.data_dir
        description: "Directory where group expense ledgers (one JSON file per group) are stored"
        default: "~/.hermes/data/fairsplit"
        prompt: "Where should FairSplit store your group ledgers?"
      - key: fairsplit.default_currency
        description: "ISO 4217 currency code used for new groups when the user doesn't specify one"
        default: "USD"
        prompt: "Default currency for new groups (e.g. USD, EUR, INR)"
---

# FairSplit

Track who paid for what in a shared trip, flat, or event, and work out the
smallest possible set of payments that settles everyone up. Everything lives
in one JSON file per group on disk -- no Splitwise account, no bank linking,
no API key, nothing to sign up for. It works just as well for a weekend trip
chat as it does for a flatmates' group that has been running for years.

All the actual arithmetic (splitting, currency conversion, and the
settlement plan) is done by a tested script, not by the model doing mental
math -- money bugs are the kind of bug nobody notices until someone's
short a real payment.

## When to Use

Load this skill when the user:

- Says things like "split this bill", "who owes who", "settle up", "add an
  expense", or mentions a shared trip/flat/event fund
- Wants to record who paid for something and how to divide it
- Asks for a balance summary or a plan for who should pay whom
- Wants a shareable summary (CSV/Markdown) of a trip's expenses

Don't use it for:

- Moving real money, requesting payments, or linking bank/UPI/PayPal
  accounts -- FairSplit only records and calculates
- Personal budgeting or tracking one person's spending (no group, nobody
  to settle with)
- Tax, accounting, or invoicing work that needs an audit trail

## Prerequisites

- Python 3.8+ on the machine running the `terminal` tool. Nothing to
  `pip install` -- `scripts/ledger.py` uses only the standard library.
- No API keys or environment variables are required.
- Outbound network access is needed *only* for the optional `fx` command.

## How to Run

Run every command through the `terminal` tool with the bundled script:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/ledger.py --data-dir "<fairsplit.data_dir>" <command> [options]
```

`--data-dir` is a global flag and goes *before* the subcommand. The
configured `fairsplit.data_dir` and `fairsplit.default_currency` values are
injected into your context when this skill loads, but they are **not**
passed to the script automatically -- always pass the configured
`--data-dir`, and pass `--currency` on `init` (falling back to
`fairsplit.default_currency`). Without `--data-dir` the script uses
`$FAIRSPLIT_DATA_DIR`, then `~/.hermes/data/fairsplit`. A leading `~` is
expanded by the script, so quoting the path is fine.

On Windows, use `python` instead of `python3` if `python3` isn't on PATH.

## Quick Reference

The examples below omit `--data-dir` for brevity; include it in real calls.

| Command       | Purpose                                              |
| ------------- | ----------------------------------------------------- |
| `init`        | Create a new group with a home currency and members  |
| `add`         | Record one expense                                    |
| `add-member`  | Add a person to an existing group                      |
| `balances`    | Show each member's net position                       |
| `settle`      | Compute the minimum-payment settlement plan            |
| `history`     | List recorded expenses, optionally filtered            |
| `undo`        | Delete an expense by id                                 |
| `export`      | Write a CSV or Markdown summary to disk                 |
| `list-groups` | List every group in the data directory                  |
| `fx`          | Best-effort keyless exchange-rate lookup (optional)      |

Every command has `--help`. Full flag reference: `references/cli-reference.md`.

## Procedure

### 1. Find or create the group

Ask what the group/trip is called if it isn't obvious from context (a chat
title, or something the user already named). Check whether it exists first:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/ledger.py list-groups
```

If it doesn't exist yet, create it. Get the member names and a home
currency (fall back to the configured `fairsplit.default_currency` if the
user doesn't say -- the script itself defaults to `USD`, so pass it):

```bash
python3 ${HERMES_SKILL_DIR}/scripts/ledger.py init --group "Goa Trip" --currency INR --members "Alice,Bob,Priya"
```

You don't need every member up front -- `add` auto-adds anyone new it sees
as a payer or participant, and `add-member` covers someone joining later
with no expenses yet.

### 2. Record expenses as they come up

Default to an equal split -- it's what the user means unless they say
otherwise:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/ledger.py add --group "Goa Trip" \
  --payer Alice --amount 1000 --description "Dinner" --split equal
```

Omit `--participants` to split across the whole group. For anything other
than a plain even split, ask a *specific* clarifying question rather than
guessing ("should this be split evenly, or does someone owe a different
share?") and pick the right split type:

- `--split equal` -- default, divides evenly (remainder cents go to
  whoever sorts first alphabetically, deterministically)
- `--split exact --detail "Alice:300,Bob:300,Priya:300"` -- named amounts
  that must add up to the total exactly
- `--split shares --detail "Alice:1,Bob:2,Priya:1"` -- proportional
  weights (e.g. Bob had two portions)
- `--split percent --detail "Alice:60,Bob:40"` -- percentages of the total

**Reading a receipt photo:** if the user shares a photo of a receipt and the
model can see images, read the merchant, line items, tax, and total
directly from the image and propose a split (e.g. itemized, or one `add`
call per person's items) -- then confirm the numbers with the user *before*
running `add`, since a misread digit is a real-money mistake. If the model
can't see images, ask the user to read out the total and any items that
need splitting unevenly.

### 3. Answer balance and settlement questions

```bash
python3 ${HERMES_SKILL_DIR}/scripts/ledger.py balances --group "Goa Trip"
python3 ${HERMES_SKILL_DIR}/scripts/ledger.py settle --group "Goa Trip"
```

`settle` is the useful one to lead with in most replies -- it collapses
everyone's tangled IOUs into the minimum number of actual payments (at most
`members - 1`), not a naive pairwise list. Report it like "Priya pays Alice
241.66, Priya pays Bob 16.67" rather than dumping raw balances on the user.

### 4. Wrap up a trip or period

```bash
python3 ${HERMES_SKILL_DIR}/scripts/ledger.py export --group "Goa Trip" --format md --out /tmp/goa-trip-summary.md
```

Read the file back and paste the summary into the chat (or hand back the
path if the user wants to forward it themselves -- see Pitfalls below for
how attachments are and aren't delivered).

## Pitfalls

- **Never do the arithmetic yourself.** Splitting, rounding, currency
  conversion, and settlement all go through `ledger.py`. Money is stored in
  integer cents internally specifically so nothing drifts by a fraction of
  a cent across dozens of expenses -- re-deriving numbers by hand
  reintroduces exactly that bug.
- **`exact` split amounts must sum to the total, to the cent.** The script
  refuses (non-zero exit, clear stderr message) rather than silently
  absorbing the difference. If the user's numbers don't add up, say so and
  ask which figure is wrong instead of fudging one participant's share.
- **A different `--currency` on `add` requires `--fx-rate`.** The `fx`
  command does a best-effort keyless lookup (Frankfurter/ECB) but needs
  outbound network access, which may not be available in every sandbox --
  if it fails, just ask the user for the rate (or the converted amount) and
  pass `--fx-rate` directly. Everything downstream (balances, settlement)
  always operates in the group's single home currency; the original
  amount/currency/rate are kept on the expense record for reference.
- **Deleting an expense changes past balances**, not just future ones --
  say so before running `undo` if the group has already been told a
  settlement plan based on it.
- **Exported files are plain CSV/Markdown, not images** -- they don't
  trigger the media auto-delivery described in the Skills System docs
  (that's for image/audio paths). Read the file back and either paste its
  contents into the chat, or tell the user the path if they're working
  locally. Don't claim it "sent as an attachment" unless the platform you're
  on actually does that for arbitrary files.
- **One JSON file per group, not per platform.** The same group ledger
  works whether the conversation is happening in Telegram, Discord, the
  CLI, or anywhere else -- don't create a second group for the same trip
  just because the question came from a different chat. When in doubt,
  run `list-groups` and ask which one the user means.
- **`init --force` wipes the group's expense history.** Only use it when
  the user explicitly wants to reset a group, and confirm first.
- **Amounts must be positive.** `add` rejects zero, negative, `NaN`, and
  non-numeric amounts. There's no "refund" expense type: to reverse an
  expense, `undo` it. To record a settle-up payment (or any money one
  person handed back to another), add an expense *paid by the person who
  sent the money* with the recipient as the only participant, e.g. after
  "Priya pays Alice 241.66": `add --payer Priya --amount 241.66
  --participants Alice --description "Settle-up" --category settlement`.
- **Names are case-sensitive.** `alice` and `Alice` are two different
  people. Reuse the exact spelling `init` or `balances` printed.

## Verification

After recording an expense, always show the per-person shares the script
printed (it prints them automatically) so the user can catch a mistake
immediately, before more expenses stack on top of a wrong split.

Before reporting a settlement plan, sanity-check that it isn't the "warning:
balances do not sum to zero" case `balances` prints -- that only happens if
the JSON file was hand-edited outside the script, and means the ledger
needs manual repair before the settlement plan can be trusted.

## Advanced

See `references/cli-reference.md` for the full flag reference (including
`history` filters and `export` formats) and `references/settlement-algorithm.md`
for how the minimum-payment settlement plan is computed and why storage
uses integer minor units. For a recurring split (e.g. monthly rent), wire a
cron job that runs an `add` command on a schedule -- see the "Recurring
splits" section of the CLI reference for a ready-to-use example.

## Development

`examples/stress_test.py` is a stdlib-only regression test: it generates
200 random expenses across 5 people and asserts balances sum to exactly
zero and settlement never exceeds `members - 1` payments. Run it after
changing anything in `scripts/ledger.py`:

```bash
python3 ${HERMES_SKILL_DIR}/examples/stress_test.py
```
