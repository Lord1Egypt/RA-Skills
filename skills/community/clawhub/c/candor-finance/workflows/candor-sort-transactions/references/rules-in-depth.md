# Rules in depth

## How a rule behaves

- A rule is declarative. While active it applies to every record it matches,
  past and future, pending and posted, refunds included. Saving it starts a
  background walk; rows update as it lands.
- A rule changes how records read: category, label, cashflow role, review
  status, or tags. Category and role are independent. `set_category` only
  regroups; `set_cashflow_role` changes whether a record counts as income,
  expense, transfer, debt payment, or refund.
- Add `match_direction`, `match_account_role`, or an amount bound only when
  the meaning depends on it. Rent paid by card depends on the account's
  role; the role survives a reconnect and an account id does not.

## Read the reach

```sh
candor rules get RULE_ID --reason "Read the rule's walk and counts"
candor rules preview RULE_ID --reason "Read a sample of what the saved rule reaches"
```

`materialization.status` moves through pending, applying, and applied;
`applied_count` says how many records it reached. A nonzero `skipped_count`
names records that already carry the most applications a record can hold;
they keep their current fields.

The preview's `matched_count` is every match. `matches` is a sample of up to
25 rows covering each distinct label first, each with its `proposed` change.
Judge from the sample and `match_label_counts`; you do not need every row.
`scan_truncated` means the counts are lower bounds; the rule still applies to
all matches.

## Exceptions and priority

An exception is a second rule with a smaller `priority` number than the rule
it overrides. The default is 50 and a smaller number wins for label,
category, role, and review status, so give an exception 10. Tags are added
and removed in application order instead. An exact correction beats every
rule on those same fields. Both rules stay active.

## Undo

```sh
candor rules disable RULE_ID --reason "The anchor reached a second merchant"
candor rules revert APPLICATION_ID --reason "Keep this one record out of the rule"
```

Disabling reverts every application in the background, and `rules get`
then reports `reverted`. Reverting one application keeps that record out of
the rule for good, through later syncs; use it for a deliberate exception,
and a correction when the record needs a different meaning. The record's
`applied_rules` carries the application id.

## Explain a record that reads wrong

```sh
candor transactions get TRANSACTION_ID --reason "Explain why the record reads this way"
candor transactions get TRANSACTION_ID --rules all --reason "List every active rule and the criterion each failed"
```

- `effective_category.provenance` says whether a rule, a correction, the
  record itself, or the bank's category supplied the value.
- `rules_considered` lists rules that matched or applied, with `applied` and
  `not_applied_reason`; with the rules scope set to all, each active rule
  shows `matched` and `failed_criteria`. `omitted_count` says how many active
  rules did not match.
- `pending`: the rule matches and its walk has not reached this record yet.
  Read `rules get` for progress.
- `reverted`: an earlier application was undone here on purpose and will not
  return. Read the actions around `reverted_at` for why, and leave it.
- A `disabled` rule was switched off on purpose. Do not recreate it for one
  record.
- When two applied rules disagree, the smaller `priority` number wins; on a
  tie the newer rule wins. Disable the one that should not apply rather than
  writing a third rule for the same merchant.
- `truncated` means the workspace has more active rules than one explanation
  lists. Read the rules list for the merchant before concluding none covers
  it.

## Tags for goals

A `tagged` goal reads the monthly net (or money in, or money out) of
transactions carrying its tags. Tag income and costs alike when the figure is
a net. Dry-run first, then save:

```sh
candor rules preview --match-merchant-contains "ETSY" --add-tag shop --reason "Check which records the shop tag would reach"
candor rules create --name "Etsy is the shop" --match-merchant-contains "ETSY" --add-tag shop --authority person_stated --basis-reason "The person said Etsy deposits are shop sales." --reason "Tag the shop's sales for its goal"
```

A rule keeps tagging new transactions as they arrive. Read tagged rows with
`candor transactions list --tag shop --limit 100 --reason "Check what the shop tag covers"`.
