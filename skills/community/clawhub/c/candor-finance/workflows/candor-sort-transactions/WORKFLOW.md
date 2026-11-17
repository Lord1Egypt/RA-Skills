
# Sort transactions

Leave the person's records reading the way they mean them, from now on: one
record corrected when it alone is wrong, a rule when a merchant always means
the same thing, tags for money a goal tracks, and a recurring list of the
bills and subscriptions that really repeat. Every change stays reversible and
you say what changed.

## Workflow

Work through these steps in order:

```text
- [ ] 1. Open and read what changed and what no rule has reached
- [ ] 2. Settle the scope and what each record means
- [ ] 3. Pick the smallest fix: correction, split, rule, or tag
- [ ] 4. Check a rule's reach before and after saving it
- [ ] 5. Curate the recurring list when it is in scope
- [ ] 6. Verify the records now read right
```

**1. Open and read.** `candor open` if this conversation has not opened
Candor yet. On a routine pass, start from
`new_since_checkpoint.transactions.page` and follow its continuation before
acknowledging. For a cleanup, read what no rule, correction, or split has
reached, and the names already in use:

```sh
candor transactions list --unmatched --limit 1000 --reason "Read the records no rule has reached"
candor data query categories --since START --until END --reason "Read the category names already in use"
candor rules list --limit 100 --reason "Read the rules already saved"
```

Each row shows `merchant_name`, `description`, `source_category`,
`category_provenance`, `cashflow_role`, and `applied_rules`. The unmatched
read adds `label_counts`; work from the top, since one rule per label covers
the most rows. Unmatched means no rule reached it, not that it is wrong.

**2. Settle the scope and meaning.** Fix what the person named, or what is
plainly wrong. Merchant text and the bank's category are evidence, not the
person's word. Ask only when a record's meaning is missing and matters. A
request to fix, clean up, or organize an area covers the inspected,
reversible fixes inside it; do not ask again for each one. When their
explanation says something durable about their life (a side business, work
expenses their employer repays, a parent they pay bills for), save it as a
note with its topic as well as fixing the records.

**3. Pick the smallest fix.**

- **One record means something different:** a correction.

```sh
candor transactions get TRANSACTION_ID --reason "Read the record before correcting it"
candor corrections create TRANSACTION_ID --category CATEGORY --reason "Apply the category the person gave"
```

- **One purchase covers several things:** a split, with parts that add up
  exactly to the amount. Undo with `candor transactions split revert TRANSACTION_ID --reason "Undo the split"`.

```sh
candor transactions split set --file SPLIT.json --reason "Split the Costco run into groceries and household"
```

- **A merchant always means the same thing:** one rule anchored on the
  merchant name. Use `person_stated` when they told you, `agent_verified`
  when the records did. Add `set_cashflow_role` when the bank calls a purchase
  a transfer or income, since budgets count the role, not the category.
- **Money a goal tracks** (a side business, a rental, a trip): a rule that
  adds a tag, so a `tagged` goal can read its monthly net.

**4. Check a rule's reach.** Dry-run the draft before saving it:

```sh
candor rules preview --match-merchant-contains "BLUE BOTTLE" --set-category Coffee --reason "Check which records the coffee rule would reach"
candor rules create --name "Blue Bottle is Coffee" --match-merchant-contains "BLUE BOTTLE" --set-category Coffee --authority person_stated --basis-reason "The person said Blue Bottle is coffee." --reason "Make Blue Bottle always read as coffee"
candor rules get RULE_ID --reason "Read how far the rule has applied"
```

The preview's `match_label_counts` counts every match by label, so a second
merchant hiding behind the anchor shows up as its own label. A rule applies
on create to every record it matches, past and future, refunds included.
`rules get` reports the walk (`pending`, `applying`, `applied`) and
`applied_count`. A label that should not change means the anchor is too wide:
disable the rule and write a narrower one, or add an exception (see the rules
reference).

**5. Curate the recurring list** when they ask to tidy bills or
subscriptions, or a routine pass shows new candidates:

```sh
candor recurring list --status candidate --limit 100 --reason "Judge detected series awaiting a decision"
candor recurring get RECURRING_ITEM_ID --reason "Read the postings behind a series"
candor recurring update --ids ID_A,ID_B --status active --reason "Confirm two clear subscriptions"
```

Confirm predictable bills and subscriptions; leave usage-based charges and
repeat shopping as they are. Set the `kind` when detection read it wrong.
Stop a series that really ended; dismiss one that was never a series. See the
recurring reference for dates, amount ranges, aliases, and declaring a bill
Candor has not seen.

**6. Verify.** Re-read the affected records. Say what now reads right, what
you left alone and why, and what is still unclear. If a fix moved money into
or out of a category a budget line counts, or a tag a goal reads, check that
figure (`budget status` or the goal's `progress`) and say in one line how it
changed, once `rules get` reports a new rule `applied`, so the figure covers
every record it reaches. This is upkeep; do not turn it into a planning
conversation unless they ask.

## How to answer

Lead with what changed in their terms, then what you left alone, then one
question if something is still open.

```text
Fixed. Blue Bottle now always reads as Coffee: 23 past charges and every new one.

- The two Amazon charges in May were a gift card and a refund, so I left them alone.
- Your recurring list now has Spotify, the gym, and car insurance confirmed. The weekly Trader Joe's runs are not bills, so they stay off it.

Want me to tag the Etsy sales and supplies so your shop's goal can track what it nets each month?
```

## Gotchas

- An adequate bank category can stand. Do not write a rule just to clear the
  unmatched list.
- A rule has no apply step and cannot be edited in place. It applies when
  created; disabling it undoes every application it made.
- A rule needs a subject: a merchant name, description, source
  classification, current category, or one account. Direction or an amount
  alone is refused.
- Reuse a category name that already exists before inventing one; budget
  lines and goals join on the name.
- Bank-side records (transfers, payroll, card payments) have no merchant
  name and their descriptions carry amounts or store numbers. Anchor on a
  fragment that stays the same.
- Repetition is not a bill. Do not confirm a transfer or a shopping habit
  just because it recurs.
- A recurring rename changes only the display name. Write a merchant rule
  when the transaction labels should change too.
- Do not overwrite a meaning the person stated or an earlier session saved
  without resolving the conflict with them.
- A price increase, a duplicate, or a charge that should have stopped is
  money to pursue: hand it to `candor-find-money`.

## Go deeper

- [Rules in depth](references/rules-in-depth.md): exceptions and priority,
  explaining why a record reads wrong, undoing a rule on one record.
- [Recurring curation](references/recurring-curation.md): statuses, expected
  windows, amount ranges, a series' full history, renamed payees, and
  declaring a bill Candor has not seen.
